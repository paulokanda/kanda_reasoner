"""Preview helpers for Tab 3 inline docstring correction."""

from __future__ import annotations

import re
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.ai_style_diagnostics_runtime import (
    append_ai_style_trace,
    short_trace_text,
)

from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _docstring_text_from_row,
    _manual_review_safe_int,
    _project_root_for_owner,
)

__all__ = [
    "build_corrected_snippet_text",
    "build_original_snippet_text",
    "is_reviewable_docstring_row",
]

DEFAULT_SNIPPET_RADIUS = 10
REVIEWABLE_TARGET_KINDS = {"module", "class", "function", "method"}


def is_reviewable_docstring_row(row: dict | None) -> bool:
    """Return whether a report row represents a missing docstring draft."""
    if not isinstance(row, dict):
        return False
    action = str(row.get("action") or "").strip().lower()
    kind = str(row.get("target_kind") or row.get("kind") or "").strip().lower()
    reason = str(row.get("reason") or "").strip().lower()
    if action != "inserted":
        return False
    if kind not in REVIEWABLE_TARGET_KINDS:
        return False
    if "already exists" in reason:
        return False
    return True


def build_original_snippet_text(owner: object, row: dict | None) -> str:
    """Return a source snippet before inserting the selected docstring."""
    if not row:
        return "No review item selected."
    path = _row_source_path(owner, row)
    text = _read_text(path)
    if text is None:
        return "Could not read source file: " + str(path)
    line_number = _row_line_number(row)
    return _format_numbered_snippet(text, line_number, DEFAULT_SNIPPET_RADIUS)


def build_corrected_snippet_text(
    owner: object,
    row: dict | None,
    mode: str = "heuristics",
) -> str:
    """Return a source snippet preview after inserting the selected docstring."""
    del mode
    if not row:
        return "No review item selected."
    if not is_reviewable_docstring_row(row):
        return (
            "This report row is not a missing-docstring correction row.\n"
            "Only inserted module, class, function, and method docstring rows "
            "are previewed here."
        )
    path = _row_source_path(owner, row)
    text = _read_text(path)
    if text is None:
        return "Could not read source file: " + str(path)
    draft = _row_draft_docstring(row)
    if not draft:
        return "No draft docstring is available for this row yet."
    append_ai_style_trace(
        owner,
        "preview_input",
        draft=short_trace_text(draft),
        row_draft=short_trace_text(row.get("draft_docstring", "")),
        ai_draft=short_trace_text(row.get("ai_draft_docstring", "")),
        style=row.get("ai_docstring_verbosity", ""),
    )
    updated = _preview_single_docstring_insert(text, row, draft)
    return _format_numbered_snippet(
        updated,
        _row_line_number(row),
        DEFAULT_SNIPPET_RADIUS + 4,
    )


def _row_draft_docstring(row: dict) -> str:
    """Return the best existing draft text for a review row."""
    for key in ("draft_docstring", "suggested_docstring", "docstring"):
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return ""


def _preview_single_docstring_insert(source_text: str, row: dict, draft: str) -> str:
    """Return source text with one docstring inserted for preview only."""
    lines = source_text.splitlines()
    insert_index, indent = _preview_insertion_point(lines, row)
    docstring = _normal_docstring(draft)
    block = [indent + line if line else "" for line in docstring.splitlines()]
    lines[insert_index:insert_index] = block
    return "\n".join(lines) + "\n"


def _preview_insertion_point(lines: list[str], row: dict) -> tuple[int, str]:
    """Return the preview insertion index and indentation for one row."""
    if not lines:
        return 0, ""
    line_number = max(1, _row_line_number(row))
    start_index = min(max(line_number - 1, 0), len(lines) - 1)
    if _row_targets_module(row):
        return _module_insert_index(lines), ""
    definition_index = _find_definition_index(lines, start_index, row)
    if definition_index is not None:
        return definition_index + 1, _definition_docstring_indent(lines[definition_index])
    fallback_line = lines[start_index] if start_index < len(lines) else ""
    return min(start_index, len(lines)), _insertion_indent(fallback_line)


def _module_insert_index(lines: list[str]) -> int:
    """Return where a module docstring should be previewed.

    Module docstrings may follow shebangs, encoding cookies, blank lines,
    and top-of-file comments. They must be inserted before any
    ``from __future__`` import or other executable statement.
    """
    index = 0
    if index < len(lines) and lines[index].startswith("#!"):
        index += 1
    if index < len(lines) and _is_encoding_cookie(lines[index]):
        index += 1
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("#"):
            index += 1
            continue
        break
    return index


def _is_encoding_cookie(line_text: str) -> bool:
    """Return whether a line is a Python source encoding cookie."""
    return re.search(r"coding[:=]\s*[-\w.]+", line_text) is not None


def _row_targets_module(row: dict) -> bool:
    """Return whether the review row describes a module docstring."""
    kind = str(row.get("target_kind") or row.get("kind") or "").strip().lower()
    return kind == "module"


def _find_definition_index(lines: list[str], start_index: int, row: dict) -> int | None:
    """Find the def/class line associated with a review row near start_index."""
    target_name = str(row.get("target_name") or row.get("name") or "").strip()
    target_leaf = target_name.rsplit(".", 1)[-1]
    search_order = _nearby_indexes(len(lines), start_index, before=6, after=8)
    for index in search_order:
        stripped = lines[index].lstrip()
        if not _is_definition_line(stripped):
            continue
        if target_leaf and not _definition_matches_target(stripped, target_leaf):
            continue
        return index
    for index in search_order:
        stripped = lines[index].lstrip()
        if _is_definition_line(stripped):
            return index
    return None


def _nearby_indexes(length: int, center: int, before: int, after: int) -> list[int]:
    """Return nearby valid line indexes, preferring center and following lines."""
    indexes: list[int] = []
    for offset in range(0, after + 1):
        index = center + offset
        if 0 <= index < length:
            indexes.append(index)
    for offset in range(1, before + 1):
        index = center - offset
        if 0 <= index < length:
            indexes.append(index)
    return indexes


def _is_definition_line(stripped: str) -> bool:
    """Return whether a stripped line starts a class or function block."""
    return stripped.startswith(("def ", "async def ", "class "))


def _definition_matches_target(stripped: str, target_name: str) -> bool:
    """Return whether a definition line appears to define target_name."""
    if stripped.startswith("async def "):
        prefix = "async def "
    elif stripped.startswith("def "):
        prefix = "def "
    elif stripped.startswith("class "):
        prefix = "class "
    else:
        return False
    remainder = stripped[len(prefix):]
    return remainder.startswith(target_name + "(") or remainder.startswith(target_name + ":")


def _definition_docstring_indent(line_text: str) -> str:
    """Return indentation for a docstring inside a def or class block."""
    base = line_text[: len(line_text) - len(line_text.lstrip(" "))]
    return base + "    "


def _format_numbered_snippet(source_text: str, line_number: int, radius: int) -> str:
    """Return a numbered source snippet around a one-based line number."""
    lines = source_text.splitlines()
    if not lines:
        return "Source file is empty."
    line_number = max(1, line_number)
    start = max(1, line_number - radius)
    end = min(len(lines), line_number + radius)
    return "\n".join(
        str(index).rjust(5) + " | " + lines[index - 1]
        for index in range(start, end + 1)
    )


def _row_source_path(owner: object, row: dict) -> Path:
    """Return the source path for a report row."""
    file_name = str(row.get("file") or row.get("path") or "").strip()
    path = Path(file_name)
    if path.is_absolute():
        return path
    return _project_root_for_owner(owner) / path


def _row_line_number(row: dict) -> int:
    """Return the insertion line for a report row."""
    return _manual_review_safe_int(row.get("line") or row.get("insert_line") or 1) or 1


def _read_text(path: Path) -> str | None:
    """Return UTF-8 source text, or None when it cannot be read."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _normal_docstring(text: str) -> str:
    """Return text as a triple-quoted docstring block."""
    draft = text.strip() or _docstring_text_from_row({})
    if not draft.startswith((chr(34) * 3, chr(39) * 3)):
        draft = (
            (chr(34) * 3)
            + draft.strip(chr(34) + chr(39) + "\n ")
            + (chr(34) * 3)
        )
    return draft


def _insertion_indent(line_text: str) -> str:
    """Return indentation for a docstring inserted before a source line."""
    indent = line_text[: len(line_text) - len(line_text.lstrip(" "))]
    if line_text.lstrip().startswith(("def ", "async def ", "class ")):
        indent += "    "
    return indent
