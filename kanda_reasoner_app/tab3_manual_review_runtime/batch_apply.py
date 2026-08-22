# project-path: kanda_reasoner_app/tab3_manual_review_runtime/batch_apply.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Render approved manual docstring review drafts as proposals.
# EXPORTS       : _apply_approved_review_batch
# DEPENDS ON    : manual_docstring_review_support.py
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Render approved manual docstring review drafts without Project mutation."""

from __future__ import annotations

import hashlib
from pathlib import Path

from kanda_reasoner_app.project_source_proposal_boundary import (
    proposal_only_message,
)

from .review_support import (
    _manual_review_is_inside_project_root,
    _manual_review_safe_int,
    _project_root_for_owner,
)


def _apply_approved_review_batch(owner: object, locations: list[dict]) -> str:
    """Render approved drafts as proposal-only evidence."""
    approved = _approved_locations(locations)
    if not approved:
        return "Approved batch proposal: no approved locations with draft text."
    by_file = _group_by_file(approved)
    reports: list[str] = [
        "Approved batch proposal-only: " + str(len(approved)) + " location(s)."
    ]
    for file_name, file_locations in by_file.items():
        reports.append(_propose_one_file(owner, file_name, file_locations))
    return "\n".join(reports)


def _approved_locations(locations: list[dict]) -> list[dict]:
    """Return approved locations that have draft text."""
    return [
        location
        for location in locations or []
        if str(location.get("approval_state", "")).lower() == "approved"
        and str(location.get("draft_docstring", "")).strip()
    ]


def _group_by_file(locations: list[dict]) -> dict[str, list[dict]]:
    """Group approved locations by file path."""
    grouped: dict[str, list[dict]] = {}
    for location in locations:
        file_name = str(location.get("file", "") or "").strip()
        if not file_name:
            continue
        grouped.setdefault(file_name, []).append(location)
    return grouped


def _propose_one_file(owner: object, file_name: str, locations: list[dict]) -> str:
    """Validate one in-memory proposal without writing Project source."""
    path = _resolve_source_path(owner, file_name)
    if not _manual_review_is_inside_project_root(owner, path):
        return "SKIP outside project root: " + file_name
    try:
        original = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return "SKIP read failed: " + file_name + " :: " + str(exc)
    updated = _insert_docstrings(original, locations)
    try:
        compile(updated, str(path), "exec")
    except (SyntaxError, ValueError) as exc:
        return "PROPOSAL_INVALID " + file_name + " :: " + str(exc)
    original_hash = _sha256_text(original)
    proposed_hash = _sha256_text(updated)
    marker = proposal_only_message("manual-docstring-batch")
    return (
        "PROPOSAL_ONLY "
        + file_name
        + " :: original_sha256="
        + original_hash
        + " proposed_sha256="
        + proposed_hash
        + " :: "
        + marker
    )


def _resolve_source_path(owner: object, file_name: str) -> Path:
    """Resolve a source path inside the selected project root."""
    path = Path(file_name)
    if path.is_absolute():
        return path
    return _project_root_for_owner(owner) / path


def _insert_docstrings(source_text: str, locations: list[dict]) -> str:
    """Insert approved docstrings by descending line number in memory."""
    lines = source_text.splitlines()
    for location in sorted(
        locations,
        key=lambda item: _manual_review_safe_int(item.get("line", 0)),
        reverse=True,
    ):
        line_number = max(1, _manual_review_safe_int(location.get("line", 1)))
        index = min(max(line_number - 1, 0), len(lines))
        draft = _normal_docstring(str(location.get("draft_docstring", "")))
        indent = _insertion_indent(lines[index] if index < len(lines) else "")
        block = [(indent + line if line else "") for line in draft.splitlines()]
        lines[index:index] = block
    return "\n".join(lines) + "\n"


def _normal_docstring(text: str) -> str:
    """Return text as a triple-quoted docstring block."""
    draft = text.strip()
    if not draft.startswith((chr(34) * 3, chr(39) * 3)):
        draft = (
            (chr(34) * 3)
            + draft.strip(chr(34) + chr(39) + "\n ")
            + (chr(34) * 3)
        )
    return draft


def _insertion_indent(line_text: str) -> str:
    """Return insertion indent for a source line."""
    indent = line_text[: len(line_text) - len(line_text.lstrip(" "))]
    if line_text.lstrip().startswith(("def ", "async def ", "class ")):
        indent += "    "
    return indent


def _sha256_text(text: str) -> str:
    """Return the SHA-256 digest of UTF-8 proposal text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
