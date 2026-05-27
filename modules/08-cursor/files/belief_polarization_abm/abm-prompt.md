# Project brief: belief-polarization agent-based model

I want to build a self-contained Python simulation of belief polarization in a
population, using a bounded-confidence interaction rule. Please read this entire
brief first and then produce a detailed plan (file structure, class design,
and figure list). Do not write code yet.

## Scientific goal

Demonstrate how population-level polarization can emerge from individually
plausible belief-update rules. Specifically:

- Each agent holds a continuous belief on the interval [-1, 1], where -1 is
  one extreme position and +1 is the opposite extreme.
- At each time step, a randomly chosen agent interacts with a randomly chosen
  ring neighbor (left or right on a circular topology).
- The interaction follows a *bounded-confidence* rule:
  - If the two agents' beliefs are within a tolerance threshold tau, the focal
    agent moves toward the neighbor by a fraction alpha of the difference
    (attraction).
  - If the difference exceeds tau, the focal agent moves away from the neighbor
    by a small fraction beta (repulsion).
- Beliefs are always clipped to [-1, 1] after each update.

The model has four parameters:

| Parameter   | Role                                    | Default |
|-------------|------------------------------------------|---------|
| `alpha`     | Attraction step size                    | 0.10    |
| `beta`      | Repulsion step size                     | 0.03    |
| `tolerance` | Threshold tau separating regimes        | 0.35    |
| `n_agents`  | Population size (ring topology)         | 100     |

Initial beliefs are drawn from N(0, 0.25), clipped to [-1, 1].

The main scientific question is: how does varying tau change the degree of
final polarization? The model should make this easy to explore systematically.

## Engineering goals

1. Object-oriented design: an `Agent` class that owns its belief and update
   logic; a `BeliefPolarizationABM` class that owns the agent list, the RNG,
   the interaction topology, and the simulation history.
2. A `run_demo` function that orchestrates a full demo run and saves four
   diagnostic figures to a specified output directory.
3. A `tolerance_sweep` function that varies tau across a grid, averages
   polarization over multiple random seeds, and returns the results for
   plotting.
4. All figures saved as PNG files to a caller-specified `Path`; no GUI windows
   (use `matplotlib.use("Agg")`).
5. A `RunSummary` dataclass returned by `run_demo` with scalar summary
   statistics and the output directory.
6. A `__main__` block so the file can be run directly with
   `python belief_polarization_abm.py`.

## Class and function design

### `Agent`

Each agent owns its `belief` value (a float in [-1, 1]) and an interaction
method that applies the bounded-confidence update in-place and clips the result
to [-1, 1]. The update rule:

```
difference = other.belief - self.belief
if abs(difference) < tolerance:
    self.belief += alpha * difference   # attraction
else:
    self.belief -= beta * difference    # repulsion
self.belief = clip(self.belief, -1.0, 1.0)
```

### `BeliefPolarizationABM`

The model owns the agent list, the RNG, and the history of belief snapshots.
Construction draws initial beliefs from N(0, 0.25), clips to [-1, 1], and
records the initial snapshot. Key behaviors:

- A `step` method picks a random agent and a random ring neighbor, then
  delegates the update to the agent.
- A `run(n_steps, record_every)` method advances the simulation and returns
  the full history as a 2-D array of shape `(n_snapshots, n_agents)`.
- Convenience metrics: mean `|belief|` (polarization), variance, and fraction
  of agents above a belief-extremity threshold.

### `RunSummary`

A small dataclass returned by `run_demo` containing scalar end-of-run summary
statistics and the output directory path.

### Plotting functions

Four module-level functions, each accepting a data argument and an output
`Path`, saving one PNG, and closing the figure:

- Belief trajectories over time (one line per agent, up to a cap).
- Final belief distribution (histogram over [-1, 1]).
- Mean |belief| over recorded time (polarization trajectory).
- Mean final polarization vs. tolerance (the sweep result).

### `tolerance_sweep`

Accepts iterables of tolerance values and random seeds, runs the model at each
combination, and returns two aligned arrays: tolerance values and mean final
polarization averaged across seeds.

### `run_demo`

Orchestrates a full demo: creates the output directory, runs the model with
default parameters, saves all four figures, runs the tolerance sweep across
nine evenly spaced values from 0.10 to 0.90 with ten seeds, and returns a
`RunSummary`.

### `main`

A `__main__` block that calls `run_demo` with output in
`<script_dir>/figures/abm/` and prints a short summary to stdout.

## File structure

```
belief_polarization_abm/
    belief_polarization_abm.py    # entire model, plotting, and __main__
    test_belief_polarization_abm.py  # I will provide this
    figures/
        abm/                      # created at runtime by run_demo / main
            belief_trajectories.png
            final_distribution.png
            polarization_over_time.png
            tolerance_sweep.png
```

## Dependencies

- Python >= 3.10
- `numpy`
- `matplotlib`

No other third-party libraries. Use only the standard library beyond those two.

## Style rules

- `from __future__ import annotations` at the top.
- Type annotations on all function signatures.
- No comments that merely restate what the code does; only comments that
  explain non-obvious decisions.
- Use `np.random.default_rng` (not the legacy `np.random` API).
- Beliefs are stored as Python `float` on each `Agent`, not as array slices.

## What I want from you first

Before writing any code, produce:

1. A brief description of the class hierarchy and how data flows from
   `Agent` up through `BeliefPolarizationABM` to the plotting functions.
2. Confirmation of the shapes returned by `run` and `tolerance_sweep`.
3. A note on any edge cases in the bounded-confidence update worth handling
   explicitly.

Once the plan is confirmed, implement `belief_polarization_abm.py`.
