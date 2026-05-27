#!/usr/bin/env python3
"""
Programmatic prompt -> generate -> test -> feedback loop using GeminiSimpleAPI.

Module 07 homework solution: implement BayesFactor via gemma-4-31b-it.

Setup:
    pip install scipy
    export GEMINI_API_KEY=...

Usage:
    cd homework-solution
    python agent_loop.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

_FILES_DIR = Path(__file__).resolve().parent.parent / "files"
if str(_FILES_DIR) not in sys.path:
    sys.path.insert(0, str(_FILES_DIR))

from agent_loop_helpers import build_attachments, build_prompt  # noqa: E402
from gemini_simple_api import GeminiSimpleAPI  # noqa: E402

PROJECT_DIR = Path(__file__).parent
PROMPT_FILE = PROJECT_DIR / "task.txt"
SOURCE_FILE = PROJECT_DIR / "bayes_factor.py"
TEST_DIR = PROJECT_DIR / "tests"
TEST_FILE = TEST_DIR / "test_bayes_factor.py"

MAX_ATTEMPTS = 10
INCLUDE_SOURCE_FILE = True
INCLUDE_TEST_FILE = True
MODEL = "gemma-4-31b-it"

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

    attachments = build_attachments(
        project_dir=PROJECT_DIR,
        source_file=SOURCE_FILE,
        test_file=TEST_FILE,
        attempt=attempt,
        include_source_file=INCLUDE_SOURCE_FILE,
        include_test_file=INCLUDE_TEST_FILE,
    )
    if attachments:
        print("Attachments:")
        for path in attachments:
            print(f"  - {path}")

    files, notes = client.prompt(
        prompt=prompt_text,
        attachments=attachments,
        verbose=True,
    )

    if notes:
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

    if code == 0:
        print(f"\nTests passed on attempt {attempt}.")
        break
else:
    print(f"\nStopped after {MAX_ATTEMPTS} attempts; tests still failing.")
    sys.exit(1)
