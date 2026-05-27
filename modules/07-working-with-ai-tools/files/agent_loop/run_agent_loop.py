#!/usr/bin/env python3
"""
Programmatic prompt -> generate -> test -> feedback loop using GeminiSimpleAPI.

Companion script for the agent-loop homework (warm-up and BayesFactor).

Setup:
    pip install numpy
    export GEMINI_API_KEY=...

Usage:
    Edit the modifiable parameters below, write task.txt in PROJECT_DIR, then:
    python run_agent_loop.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Allow running from this directory without installing the package.
_FILES_DIR = Path(__file__).resolve().parent.parent
if str(_FILES_DIR) not in sys.path:
    sys.path.insert(0, str(_FILES_DIR))

from agent_loop_helpers import build_prompt  # noqa: E402
from gemini_simple_api import GeminiSimpleAPI  # noqa: E402

SCRIPT_DIR = Path(__file__).parent

# Modifiable parameters

PROJECT_DIR         = SCRIPT_DIR / "warmup"
PROMPT_FILE         = PROJECT_DIR / "task.txt"
SOURCE_FILE         = PROJECT_DIR / "fisher.py"
TEST_DIR            = PROJECT_DIR / "tests"
TEST_FILE           = TEST_DIR / "test_fisher.py"

MAX_ATTEMPTS        = 3
INCLUDE_SOURCE_FILE = True
INCLUDE_TEST_FILE   = False
MODEL               = "gemini-2.5-flash-lite"


# Set test files to read-only (no effect if the agent runs as root).
for test_path in TEST_DIR.glob("test_*.py"):
    test_path.chmod(0o444)


def run_tests() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(TEST_DIR)],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


client = GeminiSimpleAPI(
    api_key_file=None,
    model=MODEL,
    working_dir=PROJECT_DIR,
    protected_directories=[TEST_DIR],
)

base_prompt = PROMPT_FILE.read_text()

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n=== Attempt {attempt} ===")

    prompt_text = build_prompt(
        base_prompt,
        project_dir=PROJECT_DIR,
        source_file=SOURCE_FILE,
        attempt=attempt,
    )

    attachments = []
    if INCLUDE_SOURCE_FILE and SOURCE_FILE.is_file():
        attachments.append(SOURCE_FILE)
    if INCLUDE_TEST_FILE and TEST_FILE.is_file():
        attachments.append(TEST_FILE)

    files, notes = client.prompt(
        prompt=prompt_text,
        attachments=attachments,
        verbose=False,
    )

    print(f"Notes: {notes}")
    code, output = run_tests()
    print(f"Output: {output}")

    attempt_dir = PROJECT_DIR / f"attempt_{attempt}"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    (attempt_dir / "output.txt").write_text(output)
    (attempt_dir / "prompt.txt").write_text(prompt_text)
    if notes:
        (attempt_dir / "notes.txt").write_text(notes)
    for file in files:
        shutil.copy(file, attempt_dir / file.name)

    input("Press Enter to continue...")
    if code == 0:
        print(f"\nTests passed on attempt {attempt}.")
        break
else:
    print(f"\nStopped after {MAX_ATTEMPTS} attempts; tests still failing.")
    sys.exit(1)
