# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/_file_address_headers.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Managed project-path header auditing and safe insertion
# EXPORTS       : private helpers consumed through file_processing.py
# DEPENDS ON    : none
# REFACTOR DATE : 2026-07-12
# ------------------------------------------------------
"""Audit, insert, and update managed project-path source headers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

_HEADER_SCAN_LIMIT = 30
_MANAGED_FILE_ADDRESS_PREFIX = "# project-path: "


@dataclass
class _FileAddressHeaderResult:
    """Describe one file-address header audit or edit result."""

    action: str
    expected_line: str
    old_line: str = ""
    line_number: int | None = None
    reason: str = ""


def _relative_project_path_for_header(root: Path, path: Path) -> str:
    """Return a project-relative POSIX path, or an empty string if outside root."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return ""


def _expected_file_address_line(root: Path, path: Path) -> str:
    """Return the managed file-address header line for one source file."""
    rel_path = _relative_project_path_for_header(root, path)
    if not rel_path:
        return ""
    return _MANAGED_FILE_ADDRESS_PREFIX + rel_path


def _looks_like_legacy_file_address_header(line: str) -> bool:
    """Return whether a comment looks like an old bare file-address header."""
    stripped = line.strip()
    if not stripped.startswith("#"):
        return False
    payload = stripped[1:].strip()
    lowered = payload.lower()
    if not payload or lowered.startswith("project-path:"):
        return False
    if " " in payload or "\t" in payload:
        return False
    if not lowered.endswith(".py"):
        return False
    return "/" in payload or "\\" in payload


def _audit_file_address_header(
    text: str,
    expected_line: str,
) -> _FileAddressHeaderResult:
    """Audit the top header zone for managed or legacy file-address comments."""
    if not expected_line:
        return _FileAddressHeaderResult(
            action="skipped_outside_project_root",
            expected_line="",
            reason="file is outside the selected project root",
        )

    for index, line in enumerate(text.splitlines()[:_HEADER_SCAN_LIMIT]):
        stripped = line.strip()
        line_number = index + 1
        if stripped == expected_line:
            return _FileAddressHeaderResult(
                action="exact",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="managed project-path header already present",
            )
        if stripped.startswith(_MANAGED_FILE_ADDRESS_PREFIX):
            return _FileAddressHeaderResult(
                action="stale_managed",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="stale managed project-path header will be updated",
            )
        if _looks_like_legacy_file_address_header(stripped):
            return _FileAddressHeaderResult(
                action="legacy_possible",
                expected_line=expected_line,
                old_line=stripped,
                line_number=line_number,
                reason="legacy possible file-address header found; not duplicated",
            )

    return _FileAddressHeaderResult(
        action="absent",
        expected_line=expected_line,
        reason="managed project-path header missing",
    )


def _is_coding_comment(line: str) -> bool:
    """Return whether a line is a Python coding declaration."""
    stripped = line.lstrip().lower()
    return stripped.startswith("#") and "coding" in stripped


def _is_legal_header_comment(line: str) -> bool:
    """Return whether a comment should remain above the project-path header."""
    stripped = line.strip().lower()
    if not stripped.startswith("#"):
        return False
    return (
        stripped.startswith("# spdx-")
        or stripped.startswith("# copyright")
        or stripped.startswith("# license")
    )


def _file_address_insert_index(lines: list[str]) -> int:
    """Return where to insert a managed project-path header."""
    index = 0
    if index < len(lines) and lines[index].startswith("#!"):
        index += 1

    if index < len(lines) and _is_coding_comment(lines[index]):
        index += 1

    while index < len(lines):
        line = lines[index]
        if line.strip() == "":
            index += 1
            continue
        if _is_legal_header_comment(line):
            index += 1
            continue
        break

    return index


def _compose_lines_with_original_final_newline(
    lines: list[str],
    original_text: str,
) -> str:
    """Join lines and preserve a final newline when the source had one."""
    desired = "\n".join(lines)
    if original_text.endswith("\n") or original_text == "":
        desired += "\n"
    return desired


def _apply_file_address_header(
    text: str,
    root: Path,
    path: Path,
) -> tuple[str, _FileAddressHeaderResult]:
    """Insert or update a managed project-path header when safe."""
    expected_line = _expected_file_address_line(root, path)
    audit = _audit_file_address_header(text, expected_line)

    if audit.action in {"exact", "legacy_possible", "skipped_outside_project_root"}:
        return text, audit

    lines = text.splitlines()
    if audit.action == "stale_managed" and audit.line_number is not None:
        lines[audit.line_number - 1] = expected_line
        desired = _compose_lines_with_original_final_newline(lines, text)
        return desired, _FileAddressHeaderResult(
            action="updated_stale_managed",
            expected_line=expected_line,
            old_line=audit.old_line,
            line_number=audit.line_number,
            reason="stale managed project-path header updated",
        )

    insert_index = _file_address_insert_index(lines)
    lines.insert(insert_index, expected_line)
    desired = _compose_lines_with_original_final_newline(lines, text)
    return desired, _FileAddressHeaderResult(
        action="inserted",
        expected_line=expected_line,
        line_number=insert_index + 1,
        reason="managed project-path header inserted",
    )
