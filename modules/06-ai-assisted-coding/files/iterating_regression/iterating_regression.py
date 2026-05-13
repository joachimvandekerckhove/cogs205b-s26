#!/usr/bin/env python3
"""
Programmatic prompt→generate→test→feedback loop using GeminiSimpleAPI.

Companion script for 063-programmatic-access.md.

Setup:
    pip install numpy
    export GEMINI_API_KEY=...

Usage:
    python iterating_regression.py
"""

import subprocess
import sys
from pathlib import Path

# Allow running from this directory without installing the package.
_FILES_DIR = Path(__file__).resolve().parent.parent
if str(_FILES_DIR) not in sys.path:
    sys.path.insert(0, str(_FILES_DIR))

from gemini_simple_api import GeminiSimpleAPI  # noqa: E402

TASK_DIR = Path(__file__).parent
TEST_DIR = TASK_DIR / "tests"
TEST_FILE = TEST_DIR / "test_regression.py"

MAX_ATTEMPTS = 3
INCLUDE_TEST_FILE = True
USE_GOOD_PROMPT = False

if USE_GOOD_PROMPT:
    PROMPT_FILE = TASK_DIR / "prompt.txt"
else:
    PROMPT_FILE = TASK_DIR / "bad-prompt.txt"

def run_tests() -> tuple[int, str]:
    result = subprocess.run(
        ["python", "-m", "unittest", "discover", "-s", TEST_DIR],
        cwd=TASK_DIR,
        capture_output=True,
        text=True,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


client = GeminiSimpleAPI(
    api_key_file=None,
    model="gemini-2.5-flash-lite",
    working_dir=TASK_DIR,
)

prompt_text = PROMPT_FILE.read_text()

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n=== Attempt {attempt} ===")
    files, notes = client.prompt(
        prompt=prompt_text,
        attachments=[TEST_FILE] if INCLUDE_TEST_FILE else [],
        verbose=True,
    )
    # Here you could do a quick validation that the test suite was not modified
    print(f"Notes: {notes}")
    code, output = run_tests()
    print(f"Output: {output}")
    input("Press Enter to continue...")
    if code == 0:
        print(f"\nTests passed on attempt {attempt}.")
        break
    prompt_text += (
        f"\n\n## Attempt {attempt} failed\n"
        f"```\n{output}\n```\n"
        "Fix the failures above."
    )
else:
    print(f"\nStopped after {MAX_ATTEMPTS} attempts; tests still failing.")
    sys.exit(1)
