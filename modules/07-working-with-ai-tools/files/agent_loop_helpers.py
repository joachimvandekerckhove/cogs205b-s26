"""Shared helpers for programmatic generate-test-fix agent loops."""

from __future__ import annotations

from pathlib import Path


def _attempt_number(path: Path) -> int:
    return int(path.name.removeprefix("attempt_"))


def list_previous_attempt_dirs(project_dir: Path, before_attempt: int) -> list[Path]:
    """Return archived attempt directories for attempts 1 .. before_attempt-1."""
    if before_attempt <= 1:
        return []
    dirs = [
        path
        for path in project_dir.glob("attempt_*")
        if path.is_dir() and _attempt_number(path) < before_attempt
    ]
    return sorted(dirs, key=_attempt_number)


def previous_attempt_attachment_paths(
    *,
    project_dir: Path,
    source_file: Path,
    before_attempt: int,
) -> list[Path]:
    """Return archived source, notes, and test output for every prior attempt."""
    paths: list[Path] = []
    for attempt_dir in list_previous_attempt_dirs(project_dir, before_attempt):
        for name in (source_file.name, "notes.txt", "output.txt"):
            path = attempt_dir / name
            if path.is_file():
                paths.append(path)
    return paths


def build_attachments(
    *,
    project_dir: Path,
    source_file: Path,
    test_file: Path | None,
    attempt: int,
    include_source_file: bool = True,
    include_test_file: bool = True,
) -> list[Path]:
    """
    Build the attachment list for the current attempt.

    Includes, in order:
    - archived files from every previous attempt (source, notes, test output)
    - the current source file
    - the test file
    """
    attachments: list[Path] = []
    attachments.extend(
        previous_attempt_attachment_paths(
            project_dir=project_dir,
            source_file=source_file,
            before_attempt=attempt,
        )
    )
    if include_source_file and source_file.is_file():
        attachments.append(source_file)
    if include_test_file and test_file is not None and test_file.is_file():
        attachments.append(test_file)
    return attachments


def format_previous_attempts(
    *,
    project_dir: Path,
    source_file: Path,
    before_attempt: int,
) -> str:
    """Format source code, model notes, and test output for every prior attempt."""
    attempt_dirs = list_previous_attempt_dirs(project_dir, before_attempt)
    if not attempt_dirs:
        return ""

    parts = [
        "\n\n## Previous attempts\n",
        "Every prior attempt is included below and attached as files from "
        "`attempt_N/` directories. Revise the implementation so all tests pass. "
        "Do not modify the test file.\n",
    ]

    for attempt_dir in attempt_dirs:
        attempt_num = _attempt_number(attempt_dir)
        parts.append(f"\n### Attempt {attempt_num}\n")

        notes_file = attempt_dir / "notes.txt"
        if notes_file.is_file() and notes_file.read_text().strip():
            parts.append(
                f"\n**Model notes (`{notes_file}`):**\n"
                f"```\n{notes_file.read_text().strip()}\n```\n"
            )

        archived_source = attempt_dir / source_file.name
        if archived_source.is_file():
            parts.append(
                f"\n**Source code (`{archived_source}`):**\n"
                f"```python\n{archived_source.read_text()}\n```\n"
            )

        output_file = attempt_dir / "output.txt"
        if output_file.is_file():
            parts.append(
                f"\n**Test output (`{output_file}`):**\n"
                f"```\n{output_file.read_text().strip()}\n```\n"
            )

    return "".join(parts)


def build_prompt(
    base_prompt: str,
    *,
    project_dir: Path,
    source_file: Path,
    attempt: int,
) -> str:
    """
    Assemble the prompt for the current attempt.

    On attempt 1, returns ``base_prompt`` only.
    On later attempts, inlines archived source, notes, and test output from
    *every* previous attempt directory (``attempt_1/`` .. ``attempt_{N-1}/``).
    """
    return base_prompt + format_previous_attempts(
        project_dir=project_dir,
        source_file=source_file,
        before_attempt=attempt,
    )
