"""Bulk draft generation helpers for Tab 3 review corrections."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import review_engine_status_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import review_status_visibility
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _save_manual_review_state,
)

__all__ = [
    "BulkDraftSummary",
    "generate_bulk_drafts",
    "undo_last_bulk_draft_generation",
]

_BULK_DRAFT_FIELD_NAMES = (
    "draft_docstring",
    "ai_draft_docstring",
    "ai_provider",
    "ai_status",
    "ai_error",
    "ai_used_fallback",
    "selected_draft_source",
    "ai_docstring_verbosity",
)


@dataclass
class BulkDraftSummary:
    """Summary counters for one bulk draft-generation run."""

    scope: str
    generated: int = 0
    fallback: int = 0
    skipped: int = 0
    failed: int = 0

    def output_line(self) -> str:
        """Return a compact output line for the Tab 3 Output panel."""
        return (
            "[review] bulk draft generation complete"
            + " | scope="
            + self.scope
            + " | generated="
            + str(self.generated)
            + " | fallback="
            + str(self.fallback)
            + " | skipped="
            + str(self.skipped)
            + " | failed="
            + str(self.failed)
            + "\n"
        )


def generate_bulk_drafts(owner: object, scope: str) -> BulkDraftSummary:
    """Generate review drafts for selected, visible, or all reviewable rows."""
    normalized_scope = _normalize_scope(scope)
    mode = review_engine_status_runtime.correction_mode_from_owner(owner)
    rows = _rows_for_scope(owner, normalized_scope)
    summary = BulkDraftSummary(scope=normalized_scope)

    if not rows:
        _append_output(owner, "[review] no rows found for bulk draft generation.\n")
        _refresh_visible_state(owner)
        return summary

    if normalized_scope == "all" and not _confirm_generate_all_drafts(owner, rows):
        _append_output(owner, "[review] Generate All Drafts cancelled.\n")
        _refresh_visible_state(owner)
        return summary

    snapshot = _build_bulk_snapshot(rows)

    for row in rows:
        _generate_one_bulk_draft(owner, row, mode, summary)

    if summary.generated > 0:
        setattr(owner, "_last_bulk_draft_snapshot", snapshot)
    else:
        setattr(owner, "_last_bulk_draft_snapshot", [])

    _append_output(owner, summary.output_line())
    _refresh_visible_state(owner)
    return summary


def undo_last_bulk_draft_generation(owner: object) -> int:
    """Restore draft fields changed by the most recent bulk generation run."""
    snapshot = getattr(owner, "_last_bulk_draft_snapshot", None)
    if not snapshot:
        _append_output(owner, "[review] no bulk draft generation to undo.\n")
        _refresh_visible_state(owner)
        return 0

    restored = 0
    for entry in snapshot:
        row = entry.get("row") if isinstance(entry, dict) else None
        fields = entry.get("fields") if isinstance(entry, dict) else None
        present = entry.get("present") if isinstance(entry, dict) else None
        if not isinstance(row, dict) or not isinstance(fields, dict):
            continue
        _restore_bulk_snapshot_row(row, fields, set(present or ()))
        _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
        restored += 1

    setattr(owner, "_last_bulk_draft_snapshot", [])
    _append_output(
        owner,
        "[review] restored " + str(restored) + " row(s) from last bulk draft generation.\n",
    )
    _refresh_visible_state(owner)
    return restored


def _build_bulk_snapshot(rows: list[dict]) -> list[dict]:
    """Return draft-field snapshots for rows before a bulk overwrite."""
    snapshot: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        fields = {name: row.get(name) for name in _BULK_DRAFT_FIELD_NAMES}
        present = [name for name in _BULK_DRAFT_FIELD_NAMES if name in row]
        snapshot.append({"row": row, "fields": fields, "present": present})
    return snapshot


def _restore_bulk_snapshot_row(row: dict, fields: dict, present: set[str]) -> None:
    """Restore one row's draft fields from a bulk snapshot."""
    for name in _BULK_DRAFT_FIELD_NAMES:
        if name in present:
            row[name] = fields.get(name)
        elif name in row:
            row.pop(name, None)


def _confirm_generate_all_drafts(owner: object, rows: list[dict]) -> bool:
    """Return whether Generate All Drafts should proceed."""
    hook = getattr(owner, "_confirm_bulk_draft_generation", None)
    if callable(hook):
        try:
            return bool(hook("all", len(rows)))
        except TypeError:
            return bool(hook())

    try:
        QMessageBox = _qt_widget("QMessageBox")
    except Exception:
        return True

    message = (
        "Generate draft corrections for all review rows?\n\n"
        + "This may overwrite existing generated drafts in memory and in the "
        + "manual review sidecar. It will not modify Python source files.\n\n"
        + "Rows selected: "
        + str(len(rows))
        + "\n\nContinue?"
    )
    result = QMessageBox.warning(
        owner,
        "Generate All Drafts",
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    return result == QMessageBox.Yes


def _generate_one_bulk_draft(
    owner: object,
    row: dict,
    mode: str,
    summary: BulkDraftSummary,
) -> None:
    """Generate and persist one row draft, updating summary counters."""
    if not inline_preview_runtime.is_reviewable_docstring_row(row):
        summary.skipped += 1
        return

    module_text = _read_text(_row_source_path(owner, row)) or ""
    draft = _suggest_docstring_for_row(owner, row, mode, module_text).strip()
    if not draft:
        summary.failed += 1
        _append_output(owner, "[review] draft generation failed for " + _row_identity(row) + "\n")
        return

    row["draft_docstring"] = draft
    if mode == "heuristics":
        row["selected_draft_source"] = "heuristic"
        row.setdefault("ai_status", "")

    if mode == "ai" and bool(row.get("ai_used_fallback")):
        summary.fallback += 1

    summary.generated += 1
    _save_manual_review_state(owner, row, draft)
    review_status_visibility.append_draft_generation_output(owner, row, mode)


def _rows_for_scope(owner: object, scope: str) -> list[dict]:
    """Return mutable report rows for one bulk generation scope."""
    if scope == "selected":
        row = _current_review_row(owner)
        return [row] if row else []
    if scope == "visible":
        return _visible_filtered_rows(owner)
    return [row for row in getattr(owner, "_report_rows", []) or [] if isinstance(row, dict)]


def _normalize_scope(scope: str) -> str:
    """Return a supported bulk scope string."""
    value = str(scope or "").strip().lower().replace(" ", "_")
    if value in {"selected", "selected_row", "current"}:
        return "selected"
    if value in {"visible", "visible_rows", "filtered"}:
        return "visible"
    return "all"


def _visible_filtered_rows(owner: object) -> list[dict]:
    """Return rows visible under the active review filter."""
    matcher = getattr(owner, "_matches_review_filter", None)
    rows: list[dict] = []
    for row in getattr(owner, "_report_rows", []) or []:
        if isinstance(row, dict) and (not callable(matcher) or matcher(row)):
            rows.append(row)
    return rows


def _current_review_row(owner: object) -> dict | None:
    """Return the row attached to the current review-list item."""
    review_list = getattr(owner, "_review_list", None)
    current_item = getattr(review_list, "currentItem", None)
    item = current_item() if callable(current_item) else None
    return _row_from_item_data(item)


def _row_from_item_data(item: object | None) -> dict | None:
    """Return row data from a Qt item or lightweight test double."""
    if item is None:
        return None
    for name in ("row_data", "_row"):
        value = getattr(item, name, None)
        if isinstance(value, dict):
            return value
    data_method = getattr(item, "data", None)
    if not callable(data_method):
        return None
    for role in (256, None):
        try:
            value = data_method() if role is None else data_method(role)
        except (TypeError, RuntimeError):
            continue
        if isinstance(value, dict):
            return value
    return None


def _suggest_docstring_for_row(owner: object, row: dict, mode: str, module_text: str) -> str:
    """Return a correction draft for a row using AI or heuristics."""
    if mode == "ai":
        module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime"
        )
        return module.generate_ai_review_draft_for_row(owner, row, module_text)
    module = import_module(
        "kanda_reasoner_app.tab3_manual_review_runtime.heuristic_suggestion"
    )
    return module._suggest_manual_review_heuristic(row, module_text)


def _row_source_path(owner: object, row: dict) -> Path:
    """Return the source path for a report row."""
    file_name = str(row.get("file") or row.get("path") or "").strip()
    path = Path(file_name)
    if path.is_absolute():
        return path
    root_edit = getattr(owner, "_root_path_edit", None)
    text_method = getattr(root_edit, "text", None)
    root_text = str(text_method() or "").strip() if callable(text_method) else ""
    return Path(root_text or ".") / path


def _read_text(path: Path) -> str | None:
    """Return UTF-8 source text, or None when it cannot be read."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _refresh_visible_state(owner: object) -> None:
    """Refresh review snippets, status labels, and summary after bulk generation."""
    try:
        inline_module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime"
        )
        inline_module.refresh_inline_corrector_for_selection(owner, _current_review_row(owner))
    except Exception:
        pass
    refresh_summary = getattr(owner, "_refresh_review_summary", None)
    if callable(refresh_summary):
        refresh_summary()


def _append_output(owner: object, text: str) -> None:
    """Append text to the Tab 3 output panel when available."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)


def _qt_widget(name: str) -> Any:
    """Return a PySide6.QtWidgets object lazily."""
    module = import_module("PySide" + "6.QtWidgets")
    return getattr(module, name)


def _row_identity(row: dict) -> str:
    """Return a compact row identity for output messages."""
    return str(row.get("file", "")) + ":" + str(row.get("line") or row.get("insert_line") or "")
