#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Closed-loop agent pattern from Module 06 slides:

    while not tests_pass():
        proposed_patch = model.generate_patch(...)
        apply_patch(proposed_patch)
        run tests

This script uses Gemini (via ``GeminiSimpleAPI``) to propose full-file updates as
structured JSON, writes them under a project root, and repeats until tests pass
or ``--max-iters`` is reached.

Requirements:
    - ``GEMINI_API_KEY`` in the environment, or a JSON key file (see
      ``GeminiSimpleAPI`` in ``../gemini_simple_api.py``).
    - A project directory with Python tests discoverable by unittest.

Example (from your BayesFactor homework root, with tests in ``tests/``):

    export GEMINI_API_KEY=...
    python files/agent_loop/run_agent_loop.py \\
        --project . \\
        --task-file task.txt \\
        --model gemini-2.5-flash-lite
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

# Import sibling ``gemini_simple_api`` from ``files/``.
_FILES_PARENT = Path(__file__).resolve().parent.parent
if str(_FILES_PARENT) not in sys.path:
    sys.path.insert(0, str(_FILES_PARENT))

from gemini_simple_api import GeminiSimpleAPI  # noqa: E402


def tests_pass(project: Path, test_cmd: Sequence[str]) -> bool:
    code, _ = run_tests(project, test_cmd)
    return code == 0


def run_tests(project: Path, test_cmd: Sequence[str]) -> tuple[int, str]:
    """Run test command; return (exit code, combined stdout/stderr)."""
    proc = subprocess.run(
        list(test_cmd),
        cwd=project,
        capture_output=True,
        text=True,
        timeout=600,
    )
    out_parts: list[str] = []
    if proc.stdout:
        out_parts.append(proc.stdout)
    if proc.stderr:
        out_parts.append(proc.stderr)
    combined = "\n".join(out_parts).strip()
    return proc.returncode, combined


def default_context_files(project: Path) -> list[Path]:
    """Typical layout for the course BayesFactor homework."""
    paths: list[Path] = []
    candidate = project / "bayes_factor.py"
    if candidate.is_file():
        paths.append(candidate.resolve())
    test_dir = project / "tests"
    if test_dir.is_dir():
        paths.extend(sorted(test_dir.rglob("*.py")))
    if not paths:
        # Fall back: all Python files directly under project (shallow).
        paths.extend(sorted(project.glob("*.py")))
    # De-duplicate, stable order
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(rp)
    return unique


def collect_context_files(project: Path, includes: Sequence[str] | None) -> list[Path]:
    if includes:
        out: list[Path] = []
        for pattern in includes:
            # Glob relative to project root only.
            for p in sorted(project.glob(pattern)):
                if p.is_file() and p.suffix.lower() == ".py":
                    out.append(p.resolve())
        if not out:
            raise FileNotFoundError(
                f"No .py files matched --include patterns under {project}"
            )
        return sorted(set(out))
    return default_context_files(project)


def apply_multifile_response(project_root: Path, files: list[dict[str, Any]]) -> list[Path]:
    """
    Write model-returned files under ``project_root``.

    Rejects ``..`` and paths that would escape the project root.
    """
    root = project_root.resolve()
    written: list[Path] = []
    for item in files:
        rel_raw = str(item["relative_path"]).replace("\\", "/").lstrip("/")
        if not rel_raw or rel_raw.endswith("/"):
            raise ValueError(f"Invalid relative_path: {item.get('relative_path')!r}")
        rel = Path(rel_raw)
        if ".." in rel.parts:
            raise ValueError(f"Unsafe relative_path (no '..'): {rel_raw!r}")
        dest = (root / rel).resolve()
        if dest == root:
            raise ValueError(f"Refusing to write project root as a file: {rel_raw!r}")
        if root not in dest.parents:
            raise ValueError(f"Path escapes project root: {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(item["content"], encoding="utf-8")
        written.append(dest)
    return written


def build_prompt(
    *,
    task: str,
    test_cmd: Sequence[str],
    last_output: str,
    iteration: int,
    max_iters: int,
) -> str:
    return f"""You are editing a Python project so that its unit tests pass.

## Task (human instructions)
{task.strip()}

## Test command
```text
{" ".join(test_cmd)}
```

## Constraints
- Respond ONLY with JSON matching the required schema (files array + optional notes).
- Each file must include **name** (basename), **relative_path** (POSIX path from project root), and **content** (full file text).
- **relative_path** must not contain ``..`` or absolute components.
- Include every source file you changed. You may include unchanged files only if needed for clarity.
- Do not wrap Python source in markdown fences inside **content**.
- Prefer minimal, correct fixes over large refactors.

## Last test run (stdout + stderr)
```text
{last_output if last_output.strip() else "(empty)"}
```

## Loop
Iteration {iteration} of {max_iters}. If the output above shows failures, fix them.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a test-fix loop with Gemini structured file output."
    )
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="Project root (e.g. BayesFactor homework directory).",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="",
        help="Inline task description (what to implement or fix).",
    )
    parser.add_argument(
        "--task-file",
        type=Path,
        default=None,
        help="Path to a text file with the task description (overrides empty --task).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-flash-lite",
        help="Gemini model id (must be in GeminiSimpleAPI.MODEL_LIST).",
    )
    parser.add_argument(
        "--max-iters",
        type=int,
        default=5,
        help="Maximum Gemini edit rounds (default: 5).",
    )
    parser.add_argument(
        "--test-cmd",
        type=str,
        nargs="+",
        default=["python", "-m", "unittest", "discover", "-s", "tests"],
        help="Command to run tests (default: unittest discover).",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=None,
        help=(
            "Glob relative to --project for context .py files (repeatable). "
            "Example: --include 'bayes_factor.py' --include 'tests/**/*.py'. "
            "If omitted, uses bayes_factor.py and tests/**/*.py when present."
        ),
    )
    parser.add_argument(
        "--api-key-file",
        type=Path,
        default=None,
        help="Optional JSON file {{\"api_key\": \"...\"}} if GEMINI_API_KEY is unset.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts and planned context files only; do not call Gemini.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project = args.project.expanduser().resolve()
    if not project.is_dir():
        sys.exit(f"Not a directory: {project}")

    task = args.task.strip()
    if args.task_file is not None:
        if not args.task_file.is_file():
            sys.exit(f"Task file not found: {args.task_file}")
        task = args.task_file.read_text(encoding="utf-8").strip()
    if not task:
        sys.exit("Provide --task or --task-file with non-empty instructions.")

    key_file = args.api_key_file
    if key_file is None:
        # Dummy path: ``GeminiSimpleAPI`` uses ``GEMINI_API_KEY`` first.
        key_file = Path(__file__).resolve().parent / ".gemini-key-placeholder"

    context_paths = collect_context_files(project, args.include)
    print("Context files attached to:")
    for p in context_paths:
        print(f"  - {p.relative_to(project)}")

    if args.dry_run:
        code, out = run_tests(project, args.test_cmd)
        print(f"\nDry-run: tests exit code = {code}")
        print(out[:4000])
        prompt = build_prompt(
            task=task,
            test_cmd=args.test_cmd,
            last_output=out,
            iteration=1,
            max_iters=args.max_iters,
        )
        print("\n--- Prompt preview ---\n")
        print(prompt[:6000])
        return

    if shutil.which(args.test_cmd[0]) is None:
        sys.exit(
            f"Command not found: {args.test_cmd[0]!r}. "
            "Use a venv or pass full path (e.g. python3)."
        )

    client = GeminiSimpleAPI(
        api_key_file=key_file,
        model=args.model,
        working_dir=project,
    )

    last_output = ""

    for iteration in range(1, args.max_iters + 1):
        code, combined = run_tests(project, args.test_cmd)
        if code == 0:
            print(f"Tests passed after iteration {iteration - 1} (or before first edit).")
            return
        last_output = combined
        print(f"\n=== Iteration {iteration}/{args.max_iters} ===")
        print(f"Tests failed (exit {code}). Output (truncated):\n")
        preview = combined if len(combined) <= 12000 else combined[:12000] + "\n... [truncated]"
        print(preview)

        prompt = build_prompt(
            task=task,
            test_cmd=args.test_cmd,
            last_output=last_output,
            iteration=iteration,
            max_iters=args.max_iters,
        )

        try:
            data = client.generate_content_structured(
                prompt,
                attachments=context_paths,
            )
        except Exception as err:
            print(f"Gemini request failed: {err}", file=sys.stderr)
            sys.exit(1)

        files = data.get("files") or []
        if not files:
            print("Model returned no files; stopping.", file=sys.stderr)
            sys.exit(1)

        notes = data.get("notes", "")
        if notes:
            print(f"\nModel notes: {notes}")

        try:
            written = apply_multifile_response(project, files)
        except (ValueError, KeyError, OSError) as err:
            print(f"Refusing or failed to apply patch: {err}", file=sys.stderr)
            sys.exit(1)

        print("\nWrote:")
        for w in written:
            print(f"  + {w.relative_to(project)}")

        # Refresh context paths so later turns see updated files (same paths).
        context_paths[:] = collect_context_files(project, args.include)

    # Final test
    code, combined = run_tests(project, args.test_cmd)
    if code == 0:
        print("\nTests passed.")
        return

    print(
        f"\nStopped after {args.max_iters} iterations; tests still failing (exit {code}).\n",
        file=sys.stderr,
    )
    print(combined[:8000], file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
