# Agent loop example

Runnable version of the pseudo-code in [062-ai-coding-landscape.md](../../062-ai-coding-landscape.md) (“Worked example: an agent loop”).

## Script

- [`run_agent_loop.py`](./run_agent_loop.py)

## What it does

1. Runs your test command under `--project` (default: `python -m unittest discover -s tests`).
2. If tests fail, attaches selected Python files and the test output to **Gemini**.
3. Asks the model for full updated file contents as structured JSON (same schema as [`../gemini_simple_api.py`](../gemini_simple_api.py)).
4. Writes those files under the project root (with `..` and path-escape checks).
5. Repeats until tests pass or `--max-iters` is reached.

## Setup

- Set **`GEMINI_API_KEY`** in the environment, *or* pass `--api-key-file` pointing to `{"api_key": "..."}` JSON.
- Run from an environment where `python` (or your `--test-cmd`) and the project’s dependencies are available.

## Example

From your BayesFactor homework root:

```bash
export GEMINI_API_KEY=...

printf '%s\n' 'Implement log_bayes_factor() so all tests pass. Do not change tests.' > task.txt

python path/to/run_agent_loop.py \
  --project . \
  --task-file task.txt \
  --model gemini-2.5-flash-lite \
  --max-iters 5
```

Custom globs for context files:

```bash
python path/to/run_agent_loop.py \
  --project . \
  --task "Fix evidence_spike integration." \
  --include "bayes_factor.py" \
  --include "tests/**/*.py"
```

Dry run (no API call; shows test output and prompt preview):

```bash
python path/to/run_agent_loop.py --project . --task "noop" --dry-run
```

## Caveats

- This is a **teaching** script: it grants the model permission to overwrite files you attach. Use a clean branch and review diffs, same as in lecture.
- Attachments can get large; prefer narrow `--include` globs for big projects.
- The model may still propose incorrect or over-broad edits—human review remains required for real work.
