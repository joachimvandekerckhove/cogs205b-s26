# Project brief: neural emulators for drift-diffusion-model parameter recovery

I want to build a research code base, from scratch, that trains fast neural
emulators of a drift-diffusion model (DDM) simulator, packages them into
JAGS-callable modules, and uses them inside a Bayesian parameter-recovery study.
Please read this entire brief first and then produce a detailed plan (file
tree, milestones, smoke-test strategy, risks). Do not write code yet.

## Scientific and engineering goals

1. Scientific goal: recover latent DDM parameters from observed behavioral
   summary statistics using Bayesian inference (JAGS).
2. Engineering goal: replace the expensive Monte Carlo DDM simulator with a
   neural network that is accurate, smooth, and fast enough to be called
   inside an MCMC inner loop.

Concretely, the final deliverable is a single `make all` command that, on a
fresh Linux box with the right system dependencies, runs:

    simulate training data
      -> train neural emulators (4 model families)
      -> export each emulator to a `.jnnx` package (ONNX + metadata + scalers)
      -> generate and install a native C++ JAGS module from each package
      -> run a parameter-recovery study per family with py2jags
      -> produce head-to-head comparison figures and tables

## The four model families

Implement four families in parallel, sharing as much code as possible:

| Family    | Inputs            | Network outputs                                   | JAGS likelihood                                     | Module name        |
|-----------|-------------------|----------------------------------------------------|-----------------------------------------------------|--------------------|
| ddm3      | v, a, t0          | 3 raw summary means                                | independent normals over raw summaries              | ddm3_emulator      |
| ddm4      | v, a, t0, w       | 5 raw summary means                                | independent normals over raw summaries              | ddm4_emulator      |
| ddm3cov   | v, a, t0          | 3 transformed means + 6 Cholesky terms (9 total)   | dmnorm over transformed summary vector              | ddm3cov_emulator   |
| ddm4cov   | v, a, t0, w       | 5 transformed means + 15 Cholesky terms (20 total) | dmnorm over transformed summary vector              | ddm4cov_emulator   |

Summary statistics for the four-parameter (biased) variants are
`rt_mean_corr, rt_var_corr, rt_mean_err, rt_var_err, err_rate`. The
three-parameter variants drop the correct/error split and use
`rt_mean, rt_var, choice_prob`.

The base families (`ddm3`, `ddm4`) predict raw physical summaries directly so
the ONNX graph has a clean "raw in, raw out" contract. The covariance-aware
families (`ddm3cov`, `ddm4cov`) predict the parameters of a multivariate
normal in a learned transformed space; the JAGS likelihood for those is a
single `dmnorm` whose precision matrix is reconstructed from a Cholesky
factor.

## Simulator

DDM with symmetric bounds at +/- a/2, drift v, nondecision time t0, and
relative starting-point bias w. Discrete Euler update with dt = 0.001 s,
sigma = 1.0, max_time = 10.0 s. The four-parameter starting point is
x0 = a * (w - 0.5). The simulator returns reaction times and binary choices
(correct = upper bound = 1).

Training-domain parameter ranges (must be stored in package metadata):

    v  in [-4.0, 4.0]
    a  in [0.25, 3.0]
    t0 in [0.10, 0.60]
    w  in [0.05, 0.95]  (ddm4/ddm4cov only)

Recovery-study ranges are narrower (interior of the training domain):

    v  in [-2.0, 2.0],  a in [0.5, 2.0],
    t0 in [0.15, 0.45], w in [0.15, 0.85]

Use seeded NumPy RNGs. The dataset generator must use a fixed global seed for
the parameter draws and a deterministic row-dependent seed for the simulator
noise so that any individual row is regeneratable.

## Training data

Streaming CSV writer, one row per parameter draw, chunked to disk. Default
target sizes (overridable via env vars): ~5e6 attempted rows, ~1e4 trials per
row. Smoke-test defaults: a few thousand rows with a few hundred trials.
Drop rows whose summaries are not all finite (some parameter regimes produce
too few correct or error trials to define variances).

## Neural-network training

Per family, organize code as a small importable package
(`ddm3/`, `ddm4/`, `ddm3cov/`, `ddm4cov/`) with files like `data.py`,
`models.py`, `train.py`, `export.py`, `figures.py`, plus covariance-aware
extras `loss.py`. Shared rules across families:

- Standardize inputs with sklearn's StandardScaler (fit on the training fold
  only, never on the full data set).
- For non-negative RT summaries, apply log1p before standardizing targets.
  For probability-like summaries (err_rate, choice_prob), leave them in
  raw space before standardizing. Provide a fully invertible target transform class.
- Optimize MSE in transformed space; report R^2 in original physical units.
- Use Adam (lr=1e-3, weight_decay=1e-5), batch_size=2048,
  ReduceLROnPlateau (factor 0.5, patience 5, min_lr 1e-6), early stopping
  on validation loss with patience ~15 epochs, and MAX_EPOCHS env-var
  override for smoke tests.
- Set seeds (Python, NumPy, torch) and a small thread-budget helper so the
  job is friendly on shared CPU hosts.

Base families (ddm3, ddm4):

- Provide a small catalogue of MLP architectures (deep-wide, deep-narrow,
  wide-shallow, bottleneck, residual; optionally SIREN-style and dropout
  variants) selectable via a configuration object.
- Run an architecture search on a subsample, then 5-fold cross-validation on
  the winner. Tie-breaking rule: among architectures with overall_r2 >=
  0.999 prefer the one with the fewest parameters.
- Persist `architecture_search_results.json`, `best_architecture.json`,
  `final_summary.json`, plus diagnostic figures
  (pred-vs-actual, residuals, learning curves, per-fold R^2).

Covariance-aware families (ddm3cov, ddm4cov):

- Single fixed dual-head architecture (MLP backbone, `mu_head` for the
  transformed mean, `r_head` for the upper-triangular Cholesky factor).
- Initialize the Cholesky head so the implied precision is close to the
  identity (zero weights/biases, with diagonal handled via an exp(log_diag)
  parameterization).
- Two-phase training:
    Phase 1: freeze the Cholesky head and train mu_head with MSE.
    Phase 2: unfreeze and optimize the full multivariate-normal NLL,
             precision = R^T R, with a small L2 penalty on log diagonals
             (e.g. 1e-3) for numerical stability.
- Persist `best.pt`, `target_transform.pkl`, `nn_fit_summary.json`,
  `train_history.json`.

## Export and JNNX packaging

Use the JNNX library (Python package + CLIs `validate-jnnx`,
`generate-module`, `validate-module`). Treat the `.jnnx` package as a
machine-readable contract.

Each package directory must contain at least:
- `model.onnx`
- `metadata.json` (module_name, function_name, input parameters with min/max,
  output parameters)
- `scalers.json` (describing the external interface; explicit about whether
  scaling is baked into the graph)
- `README.md`
- Covariance-aware packages also include `target_transform.pkl`.

Bake input standardization into the ONNX graph for base families so external
callers (and JAGS) work in raw units; apply `expm1` and clamp to [0, 1]
inside the graph to invert the target transform. For covariance-aware
families, accept raw parameters but return transformed means + Cholesky
terms (the matching JAGS likelihood is in transformed space).

After exporting, immediately reload the ONNX file in onnxruntime and assert
that ONNX outputs match the PyTorch wrapper on a held-out batch to within
floating-point tolerance.

Generated JAGS modules are built with the system C++ toolchain against an
ONNX Runtime C++ SDK pointed to by `ONNXRUNTIME_DIR` (must contain
`include/` and `lib/`). The Python `onnxruntime` wheel alone is not enough.

## JAGS recovery study (py2jags)

Per family, simulate a moderate-size cohort of synthetic subjects (e.g. 25)
at known parameter values drawn from the narrower recovery ranges. For each
subject, simulate ~500-2000 trials, compute summary statistics, and run
JAGS with the appropriate emulator module.

Base families:
- Dynamic JAGS model string per subject so that subjects with no correct or
  no error trials simply omit the corresponding likelihood block instead of
  using sentinel values.
- A helper that builds a per-subject data dict matching the model string exactly.
- Heuristic precisions reflecting sample-size-and-variance-dependent confidence
  in each summary.

Covariance-aware families:
- Static JAGS model string. Observed summaries are passed through the
  exported `target_transform.pkl` to obtain the standardized vector
  `obs_std[1:k]`. Inside JAGS, reconstruct R from the Cholesky terms output
  by the emulator, compute `Omega = R^T R`, and use `dmnorm(mu_std, Omega)`.

In both branches:
- Compute an MLE point estimate using the exported ONNX emulator (e.g. via
  scipy.optimize) before launching MCMC. Use it as a warm start, jittered
  per chain and clipped to the prior support, written as R-dump init files.
- Default sampler config: 4 chains, ~2000 burn-in, ~5000 samples, thin=2.
- Monitor v, a, t0 (and w where applicable).
- For each subject and parameter, store posterior mean, median, sd, 95% CI,
  Rhat, ESS, and CI width.
- Aggregate to per-family JSON summaries plus per-subject CSVs, and produce
  scatter, bias, coverage, and CI-width figures.

## Comparisons

After all four recoveries run, produce head-to-head artifacts:
- `figures/publication_head_to_head.png` and matching JSON
- `docs/publication_head_to_head.md` table with NN R^2, n/n_conv,
  JAGS wall time, mean |bias|, mean 95% coverage, and worst R-hat per family.
- Plus a `ddm3 vs ddm3cov` and `ddm4 vs ddm4cov` block comparing recovery R^2,
  bias, coverage, R-hat, and JAGS wall time.

## Build orchestration

Single top-level Makefile with phony targets `help`, `all`, `train`,
`export`, `jnnx`, `jags`, `compare`, `clean`. Use small stamp files under
`tmp/make/` and a handful of representative artifact paths
(e.g. `models/ddm4.jnnx/model.onnx`, `results/ddm4/final_summary.json`,
`figures/ddm4_jags_recovery_summary.json`,
`figures/publication_head_to_head.json`) to anchor each stage so that re-runs
are incremental. Delegate the heavy lifting to a single Python orchestrator
script (`scripts/run_publication_e2e.py --only {train,export,jnnx,jags,compare}`).
Make every long-running command honor `PYTHONUNBUFFERED=1` and respect a
`DDM3_JAGS_PARALLEL` env var.

## Environment and dependencies

- Python >= 3.10 in a dedicated venv. Install everything via `python -m pip`
  to avoid the "pip not on PATH" footgun.
- Python deps: numpy, pandas, scipy, scikit-learn, matplotlib, seaborn,
  torch, onnx, onnxruntime, and
  `py2jags @ git+https://github.com/joachimvandekerckhove/py2jags.git`.
- System deps: JAGS (e.g. `apt install jags`), a C++ toolchain
  (`g++`, `make`), and a downloaded ONNX Runtime C++ SDK referenced by
  `ONNXRUNTIME_DIR`.
- JNNX CLI tools (`validate-jnnx`, `generate-module`, `validate-module`)
  available on PATH, either pip-installed from upstream or vendored under
  `agent/jnnx/` and installed editable.

## Repository layout (target)

    pyproject.toml
    README.md
    Makefile
    data/
    results/{ddm3,ddm4,ddm3cov,ddm4cov}/
    models/{ddm3,ddm4,ddm3cov,ddm4cov}.jnnx/
    figures/
    docs/
    scripts/
      generate_<family>_data.py
      run_publication_e2e.py
      build_publication_head_to_head.py
      jags_recovery_watchdog.py
    ddm3/  ddm4/  ddm3cov/  ddm4cov/
      __init__.py
      data.py
      models.py
      simulate.py
      train.py
      export.py
      figures.py
      jags_models.py      # static templates
      jags_dynamic.py     # ddm3/ddm4 only; per-subject template builder
      jags_recovery.py
      loss.py             # *cov families only
    agent/jnnx/           # vendored JNNX (optional)
    tests/

## Reproducibility, smoke tests, and observability

- Every stage must write a JSON summary and at least one diagnostic figure.
- Provide env-var smoke knobs for each stage (e.g. `DDM4_N_ROWS`,
  `DDM4_TRIALS_PER_ROW`, `DDM4_MAX_EPOCHS`, `DDM4_PATIENCE`, and an
  analogous `<FAMILY>_SMOKE=1`) so the whole pipeline can be exercised
  end-to-end in a few minutes before scaling up.
- For JAGS runs, log to a file with `PYTHONUNBUFFERED=1`, expose subject
  progress, and ship a watchdog helper (`scripts/jags_recovery_watchdog.py`)
  that can identify and SIGTERM hung `jags-terminal` child processes.
- Pin a "debug from left to right" order in the README:
  simulator -> CSV -> loader/transform -> training metrics ->
  PyTorch-vs-ONNX agreement -> `validate-jnnx` -> JAGS module load ->
  tiny recovery -> full recovery -> comparison.

## What I want from you first

Before writing any code, produce:

1. A milestone plan with clear acceptance criteria per milestone (one
   milestone per pipeline stage, plus an explicit "smoke run end-to-end"
   milestone before any full-scale run).
2. The proposed repository file tree, annotated with the responsibility of
   each file.
3. A short list of the riskiest unknowns (e.g. ONNX <-> JAGS contract,
   covariance-aware loss numerics, JAGS module install path, dynamic vs
   static JAGS model strings) and how you plan to de-risk each one early.
4. A draft of the Makefile and the `scripts/run_publication_e2e.py`
   command-line surface, with the artifact paths each stage will create.

Once the plan is approved, implement the project incrementally, stage by
stage, validating each stage's artifacts before moving on.