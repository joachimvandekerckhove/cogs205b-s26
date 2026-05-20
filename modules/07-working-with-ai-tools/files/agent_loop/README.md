# Agent loop example

Runnable version of the pseudo-code in [062-ai-coding-landscape.md](../../062-ai-coding-landscape.md) (“Worked example: an agent loop”).

## Script

- [`run_agent_loop.py`](./run_agent_loop.py)

## What it does

1. Reads `task.txt` from `PROJECT_DIR`.
2. Calls Gemini (via `GeminiSimpleAPI`) to write updated files under `PROJECT_DIR`.
3. Runs `python -m unittest discover -s tests`.
4. Appends test output to the prompt and repeats until tests pass or `MAX_ATTEMPTS` is reached.

Same structure as [`../iterating_regression/iterating_regression.py`](../iterating_regression/iterating_regression.py).

## Setup

- Set **`GEMINI_API_KEY`** in the environment.
- Edit the modifiable parameters at the top of `run_agent_loop.py` (`PROJECT_DIR`, `SOURCE_FILE`, `PROMPT_FILE`, etc.).
- Write **`task.txt`** (or the path you set in `PROMPT_FILE`) in `PROJECT_DIR`.

## Example (warm-up)

```bash
export GEMINI_API_KEY=...

# In warmup/, create task.txt with your one-sentence task.

cd files/agent_loop
python run_agent_loop.py
```

For BayesFactor, set `PROJECT_DIR` to your homework repo root, `SOURCE_FILE` to `bayes_factor.py`, and point `TEST_DIR` / `TEST_FILE` at your test suite.

## Caveats

- This is a **teaching** script: the model can overwrite files under `PROJECT_DIR`. Use a clean branch and review diffs.
- Test files under `tests/` are marked read-only and listed in `protected_directories`; the API still blocks writes there when protection works.
- Human review remains required for real work.
