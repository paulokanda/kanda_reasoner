# project-path: _inject_missing_module_docstrings.py
"""Inject missing module docstrings for Project Reasoner maintenance scripts."""

from __future__ import annotations

__all__ = [
    "main",
    "build_docstring",
]

import ast
import io
import re
import shutil
import subprocess
import sys
import time
import tokenize
from pathlib import Path

from kanda_reasoner_app import CANONICAL_PACKAGE_NAME, LEGACY_PACKAGE_NAME
from kanda_reasoner_app.project_root_resolver import resolve_active_project_root


PROJECT_ROOT = resolve_active_project_root()
MANAGE_ARCHITECTURE = (
    PROJECT_ROOT
    / CANONICAL_PACKAGE_NAME
    / "manage_architecture"
    / "manage_architecture.py"
)

BACKUP_ROOT = (
    PROJECT_ROOT
    / "project_freeze_ledger"
    / "docstring_injection_backups"
    / time.strftime("%Y%m%d_%H%M%S")
)

MISSING_RE = re.compile(
    r"WARNING\s+MISSING_DOCSTRING\s+(.+?)\s+::\s+Missing module docstring\."
)


PACKAGE_ROLE_SUFFIXES = [
    (
        "reasoner_context_collector/",
        "Support static evidence collection for Project Reasoner.",
    ),
    (
        "reasoner_runtime_collector/",
        "Support runtime evidence collection for Project Reasoner.",
    ),
    (
        "project_reasoner_v10/",
        "Support V10 project reasoning and evidence handling.",
    ),
    (
        "insert_missing_docstrings_gui/",
        "Support missing-docstring insertion workflows.",
    ),
    (
        "json_splitter/",
        "Support JSON splitting and split-output validation workflows.",
    ),
    (
        "runtime_scenarios/",
        "Support runtime scenario evidence generation.",
    ),
]

ROLE_PREFIXES = [
    (package_name + "/" + suffix, sentence)
    for package_name in (CANONICAL_PACKAGE_NAME, LEGACY_PACKAGE_NAME)
    for suffix, sentence in PACKAGE_ROLE_SUFFIXES
]


def run_validate() -> str:
    """Run Tab 1 validation and return combined output."""
    command = [
        sys.executable,
        str(MANAGE_ARCHITECTURE),
        "--root",
        str(PROJECT_ROOT),
        "--validate",
    ]
    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
    )
    return result.stdout + "\n" + result.stderr


def parse_missing_paths(output: str) -> list[Path]:
    """Extract missing-module-docstring paths from validation output."""
    paths: list[Path] = []
    seen: set[str] = set()

    for line in output.splitlines():
        match = MISSING_RE.search(line)
        if not match:
            continue

        rel_text = match.group(1).strip().replace("/", "\\")
        if rel_text in seen:
            continue

        path = PROJECT_ROOT / rel_text
        paths.append(path)
        seen.add(rel_text)

    return paths


def detect_encoding(path: Path) -> str:
    """Detect Python source encoding."""
    with path.open("rb") as handle:
        encoding, _ = tokenize.detect_encoding(handle.readline)
    return encoding


def read_text(path: Path) -> tuple[str, str, str]:
    """Read source text with detected encoding and newline style."""
    encoding = detect_encoding(path)
    raw = path.read_bytes()
    text = raw.decode(encoding, errors="replace")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text, encoding, newline


def has_module_docstring(text: str) -> bool:
    """Return whether the module already has a docstring."""
    tree = ast.parse(text)
    return ast.get_docstring(tree) is not None


def normalize_rel_path(path: Path) -> str:
    """Return a project-relative POSIX-style path."""
    try:
        rel = path.relative_to(PROJECT_ROOT)
    except ValueError:
        rel = path
    return rel.as_posix()


def build_docstring(path: Path) -> str:
    """Build a safe module docstring from the project-relative path."""
    rel = normalize_rel_path(path)

    for prefix, sentence in ROLE_PREFIXES:
        if rel.startswith(prefix):
            return sentence

    stem = path.stem.replace("_", " ").replace("-", " ").strip()
    if stem:
        return "Support the " + stem + " module for Project Reasoner."

    return "Support Project Reasoner module behavior."


def is_coding_comment(line: str) -> bool:
    """Return whether a line is a Python coding declaration."""
    lowered = line.lower()
    return line.lstrip().startswith("#") and "coding" in lowered


def is_header_comment(line: str) -> bool:
    """Return whether a comment should stay before the module docstring."""
    stripped = line.strip()
    lowered = stripped.lower()

    if not stripped.startswith("#"):
        return False

    if stripped.startswith("#!"):
        return True

    if "coding" in lowered:
        return True

    if lowered.startswith("# spdx-"):
        return True

    if "copyright" in lowered:
        return True

    if lowered.startswith("# project-path:"):
        return True

    return False


def insertion_index(lines: list[str]) -> int:
    """Return where to insert a module docstring."""
    index = 0

    if index < len(lines) and lines[index].startswith("#!"):
        index += 1

    if index < len(lines) and is_coding_comment(lines[index]):
        index += 1

    while index < len(lines) and is_header_comment(lines[index]):
        index += 1

    while index < len(lines) and lines[index].strip() == "":
        index += 1

    return index


def inject_docstring(text: str, docstring: str, newline: str) -> str:
    """Insert a module docstring without changing the rest of the file."""
    lines = text.splitlines()
    had_final_newline = text.endswith(("\n", "\r\n"))

    index = insertion_index(lines)

    doc_lines = [
        '"""' + docstring + '"""',
        "",
    ]

    new_lines = lines[:index] + doc_lines + lines[index:]
    new_text = newline.join(new_lines)

    if had_final_newline:
        new_text += newline

    return new_text


def backup_file(path: Path) -> None:
    """Copy the original file to the backup folder."""
    rel = path.relative_to(PROJECT_ROOT)
    dst = BACKUP_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)


def compile_file(path: Path) -> tuple[bool, str]:
    """Compile one Python file."""
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    """Inject missing module docstrings based on current Tab 1 output."""
    print("Running Tab 1 validation to find missing module docstrings...")
    output = run_validate()
    paths = parse_missing_paths(output)
    paths = [
        path for path in paths
        if path.name != "_inject_missing_module_docstrings.py"
    ]

    if not paths:
        print("No MISSING_DOCSTRING findings found.")
        return 0

    print("Files with missing module docstring: " + str(len(paths)))
    for path in paths:
        print("  " + normalize_rel_path(path))

    print("")
    answer = input("Type YES to inject module docstrings into these files: ")
    if answer.strip().upper() != "YES":
        print("Cancelled. No files changed.")
        return 0

    touched: list[Path] = []
    skipped: list[str] = []

    for path in paths:
        if not path.exists():
            skipped.append(str(path) + " -> missing file")
            continue

        try:
            text, encoding, newline = read_text(path)
        except (OSError, UnicodeError, SyntaxError) as exc:
            skipped.append(str(path) + " -> read failed: " + str(exc))
            continue

        try:
            if has_module_docstring(text):
                skipped.append(str(path) + " -> already has module docstring")
                continue
        except SyntaxError as exc:
            skipped.append(str(path) + " -> syntax error, skipped: " + str(exc))
            continue

        docstring = build_docstring(path)
        new_text = inject_docstring(text, docstring, newline)

        try:
            backup_file(path)
            path.write_text(new_text, encoding=encoding, newline="")
            touched.append(path)
            print("Injected: " + normalize_rel_path(path))
        except OSError as exc:
            skipped.append(str(path) + " -> write failed: " + str(exc))

    print("")
    print("Compiling touched files...")
    failed = False
    for path in touched:
        ok, compile_output = compile_file(path)
        if ok:
            print("OK: " + normalize_rel_path(path))
        else:
            failed = True
            print("FAIL: " + normalize_rel_path(path))
            if compile_output:
                print(compile_output)

    print("")
    print("Summary")
    print("Touched: " + str(len(touched)))
    print("Skipped: " + str(len(skipped)))
    print("Backup folder: " + str(BACKUP_ROOT))

    if skipped:
        print("")
        print("Skipped details:")
        for item in skipped:
            print("  " + item)

    if failed:
        print("")
        print("At least one touched file failed py_compile.")
        print("Use the backup folder to restore affected files if needed.")
        return 1

    print("")
    print("Done. Re-run Tab 1 validate to confirm MISSING_DOCSTRING decreased.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
