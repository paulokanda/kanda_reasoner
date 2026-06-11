"""Inline correction workflow for Tab 3 manual docstring review."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import review_status_visibility
from kanda_reasoner_app.tab3_manual_review_runtime import review_engine_status_runtime
from kanda_reasoner_app.tab3_manual_review_runtime.review_persistence_fields import (
    clear_persisted_draft_fields,
)
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _save_manual_review_state,
)

__all__ = [
    "refresh_inline_corrector_for_selection",
    "refresh_correction_engine_status",
    "refresh_review_draft_status",
    "generate_current_draft",
    "reset_filtered_review_selection",
    "approve_current_row",
    "approve_visible_rows",
    "reject_current_row",
    "save_all_approved_corrections",
    "save_current_correction",
    "select_next_filtered_review_item",
    "undo_current_correction",
    "wire_inline_corrector_events",
]


def wire_inline_corrector_events(window: object) -> None:
    """Connect optional inline-corrector widgets when they exist."""
    _connect(
        getattr(window, "_review_previous_button", None),
        "clicked",
        lambda *args: select_next_filtered_review_item(window, -1),
    )
    _connect(
        getattr(window, "_review_next_button", None),
        "clicked",
        lambda *args: select_next_filtered_review_item(window, 1),
    )
    _connect(
        getattr(window, "_review_reset_button", None),
        "clicked",
        lambda *args: reset_filtered_review_selection(window),
    )
    _connect(
        getattr(window, "_review_generate_draft_button", None),
        "clicked",
        lambda *args: generate_current_draft(window),
    )
    _connect(
        getattr(window, "_review_save_change_button", None),
        "clicked",
        lambda *args: save_current_correction(window),
    )
    _connect(
        getattr(window, "_review_approve_row_button", None),
        "clicked",
        lambda *args: approve_current_row(window),
    )
    _connect(
        getattr(window, "_review_reject_row_button", None),
        "clicked",
        lambda *args: reject_current_row(window),
    )
    _connect(
        getattr(window, "_review_undo_button", None),
        "clicked",
        lambda *args: undo_current_correction(window),
    )
    _connect(
        getattr(window, "_review_save_all_button", None),
        "clicked",
        lambda *args: approve_visible_rows(window),
    )
    _connect(
        getattr(window, "_ai_enabled_checkbox", None),
        "toggled",
        lambda checked: _handle_ai_enabled_changed(window, checked),
    )
    refresh_correction_engine_status(window)
    refresh_review_draft_status(window, _current_review_row(window))


def refresh_correction_engine_status(owner: object) -> None:
    """Refresh the read-only correction engine status label."""
    review_engine_status_runtime.apply_correction_engine_status(owner)


def refresh_review_draft_status(owner: object, row: dict | None = None) -> None:
    """Refresh the visible draft-generation status label."""
    current_row = row if row is not None else _current_review_row(owner)
    review_status_visibility.apply_review_draft_status(owner, current_row)


def _handle_ai_enabled_changed(owner: object, checked: bool) -> None:
    """Update engine status and refresh snippets after Local AI changes."""
    del checked
    refresh_correction_engine_status(owner)
    refresh_inline_corrector_for_selection(owner, _current_review_row(owner))


def refresh_inline_corrector_for_selection(owner: object, row: dict | None) -> None:
    """Refresh original and corrected snippets for the selected report row."""
    _set_plain_text(
        owner,
        "_review_original_snippet",
        inline_preview_runtime.build_original_snippet_text(owner, row),
    )
    _set_plain_text(
        owner,
        "_review_corrected_snippet",
        inline_preview_runtime.build_corrected_snippet_text(
            owner,
            row,
            _selected_correction_mode(owner),
        ),
    )
    refresh_review_draft_status(owner, row)


def select_next_filtered_review_item(owner: object, direction: int) -> None:
    """Move to previous or next visible review item in the filtered list."""
    review_list = getattr(owner, "_review_list", None)
    if review_list is None:
        return
    count = _safe_int(_safe_call(review_list, "count", 0), 0)
    if count <= 0:
        return
    current = _safe_int(_safe_call(review_list, "currentRow", -1), -1)
    step = 1 if direction >= 0 else -1
    next_row = 0 if current < 0 else (current + step) % count
    setter = getattr(review_list, "setCurrentRow", None)
    if callable(setter):
        setter(next_row)
        _refresh_current_review_selection(owner)


def reset_filtered_review_selection(owner: object) -> None:
    """Reset the filtered review list navigation to the first visible row."""
    review_list = getattr(owner, "_review_list", None)
    if review_list is None:
        return
    if _safe_int(_safe_call(review_list, "count", 0), 0) <= 0:
        refresh_inline_corrector_for_selection(owner, None)
        return
    setter = getattr(review_list, "setCurrentRow", None)
    if callable(setter):
        setter(0)
        _refresh_current_review_selection(owner)


def generate_current_draft(owner: object) -> None:
    """Generate a draft for the selected row without saving approval state."""
    row = _current_review_row(owner)
    if not row:
        _append_output(owner, "[review] no selected row to generate a draft.\n")
        return
    if not inline_preview_runtime.is_reviewable_docstring_row(row):
        _append_output(owner, "[review] selected row is not a missing-docstring row.\n")
        return
    mode = _selected_correction_mode(owner)
    draft = _suggest_docstring_for_row(owner, row, mode).strip()
    if not draft:
        _append_output(owner, "[review] no correction draft was generated.\n")
        return
    row["draft_docstring"] = draft
    if mode == "heuristics":
        row["selected_draft_source"] = "heuristic"
        row.setdefault("ai_status", "")
    review_status_visibility.append_draft_generation_output(owner, row, mode)
    _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
    _refresh_after_row_change(owner, row)


def save_current_correction(owner: object) -> None:
    """Save the selected visible draft as a review decision without approval."""
    row = _current_review_row(owner)
    if not row:
        _append_output(owner, "[review] no selected row to save.\n")
        return
    if not inline_preview_runtime.is_reviewable_docstring_row(row):
        _append_output(owner, "[review] selected row is not a missing-docstring row.\n")
        return
    draft = _visible_review_draft(row, _selected_correction_mode(owner))
    if not draft.strip():
        _append_output(
            owner,
            "[review] no generated draft to save. Click Generate Draft first.\n",
        )
        return
    row["classification"] = "review_saved"
    row["approval_state"] = "review_saved"
    row["draft_docstring"] = draft
    _save_manual_review_state(owner, row, draft)
    _append_output(owner, "[review] saved review decision for " + _row_identity(row) + "\n")
    _refresh_after_row_change(owner, row)


def undo_current_correction(owner: object) -> None:
    """Clear the saved correction state for the selected row."""
    row = _current_review_row(owner)
    if not row:
        _append_output(owner, "[review] no selected row to undo.\n")
        return
    row["classification"] = "unsaved/new"
    row["approval_state"] = ""
    clear_persisted_draft_fields(row)
    _save_manual_review_state(owner, row, "")
    _append_output(owner, "[review] cleared correction for " + _row_identity(row) + "\n")
    _refresh_after_row_change(owner, row)


def approve_current_row(owner: object) -> None:
    """Approve the selected saved review decision without writing source files."""
    row = _current_review_row(owner)
    if not row:
        _append_output(owner, "[review] no selected row to approve.\n")
        return
    if not inline_preview_runtime.is_reviewable_docstring_row(row):
        _append_output(owner, "[review] selected row is not a missing-docstring row.\n")
        return
    if not str(row.get("draft_docstring") or "").strip():
        _append_output(owner, "[review] no saved draft to approve. Click Generate Draft first.\n")
        return
    row["classification"] = "approved"
    row["approval_state"] = "approved"
    _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
    _append_output(owner, "[review] approved row " + _row_identity(row) + "\n")
    _refresh_after_row_change(owner, row)


def reject_current_row(owner: object) -> None:
    """Reject the selected review row without writing source files."""
    row = _current_review_row(owner)
    if not row:
        _append_output(owner, "[review] no selected row to reject.\n")
        return
    row["classification"] = "rejected"
    row["approval_state"] = "rejected"
    _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
    _append_output(owner, "[review] rejected row " + _row_identity(row) + "\n")
    _refresh_after_row_change(owner, row)


def approve_visible_rows(owner: object) -> None:
    """Warn, then approve visible rows with saved drafts without writing source files."""
    rows = _visible_filtered_rows(owner)
    candidates = [
        row
        for row in rows
        if inline_preview_runtime.is_reviewable_docstring_row(row)
        and str(row.get("draft_docstring") or row.get("suggested_docstring") or "").strip()
    ]
    if not candidates:
        _append_output(owner, "[review] no visible rows have saved draft corrections.\n")
        return
    if not _confirm_bulk_approval(owner, len(candidates)):
        _append_output(owner, "[review] Approve Visible Rows cancelled.\n")
        return
    for row in candidates:
        if not str(row.get("draft_docstring") or "").strip():
            row["draft_docstring"] = str(row.get("suggested_docstring") or "")
        row["classification"] = "approved"
        row["approval_state"] = "approved"
        _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
    _append_output(
        owner,
        "[review] approved " + str(len(candidates)) + " visible row(s).\n",
    )
    refresher = getattr(owner, "_populate_review_list", None)
    if callable(refresher):
        refresher()


def save_all_approved_corrections(owner: object) -> None:
    """Compatibility alias for approve_visible_rows."""
    approve_visible_rows(owner)


def _selected_correction_mode(owner: object) -> str:
    """Return ai or heuristics from the single Local AI checkbox source."""
    return review_engine_status_runtime.correction_mode_from_owner(owner)


def _local_ai_enabled(owner: object) -> bool:
    """Return whether the Local AI checkbox is enabled and checked."""
    return review_engine_status_runtime.local_ai_enabled_from_owner(owner)


def _current_review_row(owner: object) -> dict | None:
    """Return the current row from the visible review list."""
    review_list = getattr(owner, "_review_list", None)
    if review_list is None:
        return None
    item = _safe_call(review_list, "currentItem", None)
    return _row_from_item_data(item)


def _refresh_current_review_selection(owner: object) -> None:
    """Refresh preview widgets after navigation changes the current row."""
    refresh_inline_corrector_for_selection(owner, _current_review_row(owner))


def _row_from_item_data(item: object | None) -> dict | None:
    """Return row data from a Qt item or lightweight test double."""
    if item is None:
        return None
    direct = getattr(item, "row_data", None)
    if isinstance(direct, dict):
        return direct
    direct = getattr(item, "_row", None)
    if isinstance(direct, dict):
        return direct
    data_method = getattr(item, "data", None)
    if not callable(data_method):
        return None
    roles: list[object] = []
    try:
        roles.append(_qt_core("Qt").UserRole)
    except Exception:
        roles.append(256)
    roles.append(256)
    roles.append(None)
    for role in roles:
        try:
            data = data_method() if role is None else data_method(role)
        except TypeError:
            continue
        except RuntimeError:
            return None
        if isinstance(data, dict):
            return data
    return None


def _visible_filtered_rows(owner: object) -> list[dict]:
    """Return rows visible under the active filter."""
    matcher = getattr(owner, "_matches_review_filter", None)
    rows: list[dict] = []
    for row in getattr(owner, "_report_rows", []) or []:
        if not callable(matcher) or matcher(row):
            rows.append(row)
    return rows


def _suggest_docstring_for_row(owner: object, row: dict, mode: str) -> str:
    """Return a correction draft for a row using AI or heuristics."""
    path = _row_source_path(owner, row)
    module_text = _read_text(path) or ""
    if mode == "ai":
        module = import_module(
            "kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime"
        )
        return module.generate_ai_review_draft_for_row(owner, row, module_text)
    module = import_module(
        "kanda_reasoner_app.tab3_manual_review_runtime.heuristic_suggestion"
    )
    return module._suggest_manual_review_heuristic(row, module_text)


def _visible_review_draft(row: dict, mode: str) -> str:
    """Return the already generated draft that should be saved."""
    if mode == "ai":
        for key in ("ai_draft_docstring", "draft_docstring"):
            draft = str(row.get(key) or "").strip()
            if draft:
                return draft
        return ""
    return str(row.get("draft_docstring") or "").strip()


def _refresh_after_row_change(owner: object, row: dict) -> None:
    """Refresh visible widgets after changing one row."""
    refresh_inline_corrector_for_selection(owner, row)
    review_list = getattr(owner, "_review_list", None)
    current_item_getter = getattr(review_list, "currentItem", None)
    current_item = current_item_getter() if callable(current_item_getter) else None
    if current_item is not None:
        set_text = getattr(current_item, "setText", None)
        if callable(set_text):
            set_text(_row_title(row))
    refresh_summary = getattr(owner, "_refresh_review_summary", None)
    if callable(refresh_summary):
        refresh_summary()


def _confirm_bulk_approval(owner: object, count: int) -> bool:
    """Return whether the user confirms risky bulk row approval."""
    QMessageBox = _qt_widget("QMessageBox")
    message = (
        "It is risky to approve all visible rows without reviewing each one.\n\n"
        + "This will not modify source files. It will mark "
        + str(count)
        + " visible row(s) as approved for a later apply step. Continue?"
    )
    result = QMessageBox.warning(
        owner,
        "Risky Bulk Approval",
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    return result == QMessageBox.Yes


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


def _row_identity(row: dict) -> str:
    """Return a compact row identity for output messages."""
    return str(row.get("file", "")) + ":" + str(row.get("line") or row.get("insert_line") or "")


def _row_title(row: dict) -> str:
    """Return a compact list title after inline correction changes."""
    state = str(row.get("classification") or row.get("review_status") or "review")
    target_name = str(row.get("target_name") or "<module>")
    return state + " | " + _row_identity(row) + " | " + target_name


def _set_plain_text(owner: object, widget_name: str, text: str) -> None:
    """Set plain text on an optional widget."""
    widget = getattr(owner, widget_name, None)
    setter = getattr(widget, "setPlainText", None)
    if callable(setter):
        setter(text)


def _append_output(owner: object, text: str) -> None:
    """Append text to the Tab 3 output if possible."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)



def _safe_call(obj: object, method_name: str, default: object) -> object:
    """Call a no-argument method defensively."""
    method = getattr(obj, method_name, None)
    if not callable(method):
        return default
    try:
        return method()
    except Exception:
        return default


def _safe_int(value: object, default: int) -> int:
    """Return an integer while preserving valid zero values."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _connect(widget: object | None, signal_name: str, slot: Any) -> None:
    """Connect a Qt signal if the widget exists."""
    signal = getattr(widget, signal_name, None)
    connect = getattr(signal, "connect", None)
    if callable(connect):
        connect(slot)


def _qt_core(name: str) -> Any:
    """Return a PySide6.QtCore object lazily."""
    module = import_module("PySide" + "6.QtCore")
    return getattr(module, name)


def _qt_widget(name: str) -> Any:
    """Return a PySide6.QtWidgets object lazily."""
    module = import_module("PySide" + "6.QtWidgets")
    return getattr(module, name)
