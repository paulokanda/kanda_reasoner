"""Runtime implementation for the Tab 3 report review panel."""

from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path
from typing import Any

from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _apply_saved_manual_review_state,
    _format_review_row_context,
    _manual_review_action_hint_for_row,
    _manual_review_severity_for_row,
    _manual_review_status_for_row,
)

from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    refresh_inline_corrector_for_selection,
)
from kanda_reasoner_app.tab3_manual_review_runtime.inline_preview_runtime import (
    is_reviewable_docstring_row,
)


def _review_status_for_row(row: dict) -> str:
    """Return the manual-review status for one report row."""
    return _manual_review_status_for_row(row)


def _review_severity_for_row(row: dict) -> str:
    """Return the manual-review severity for one report row."""
    return _manual_review_severity_for_row(row)


def _review_action_hint_for_row(row: dict) -> str:
    """Return the review action hint for one report row."""
    return _manual_review_action_hint_for_row(row)


def _load_report_rows(owner: object) -> None:
    """Load JSONL report rows into the Tab 3 review panel."""
    path = Path(owner._effective_report_path())
    rows: list[dict] = []
    if path.is_file():
        rows = _read_report_rows(path)
    rows = _apply_saved_manual_review_state(owner, rows)
    owner._report_rows = rows
    _refresh_review_summary(owner)
    _populate_review_list(owner)


def _refresh_review_summary(owner: object) -> None:
    """Refresh the summary label for loaded report rows."""
    rows = list(getattr(owner, "_report_rows", []) or [])
    reviewable_rows = [row for row in rows if is_reviewable_docstring_row(row)]
    total = len(rows)
    reviewable = len(reviewable_rows)
    needs_review = sum(1 for row in reviewable_rows if _row_needs_review(owner, row))
    errors = sum(1 for row in reviewable_rows if _review_severity_for_row(row) == "error")
    warnings = sum(1 for row in reviewable_rows if _review_severity_for_row(row) == "warning")
    owner._review_summary.setText(
        "Docstring rows: "
        + str(reviewable)
        + " | report rows: "
        + str(total)
        + " | needs review: "
        + str(needs_review)
        + " | warnings: "
        + str(warnings)
        + " | errors: "
        + str(errors)
    )


def _row_needs_review(owner: object, row: dict) -> bool:
    """Return whether a report row should be reviewed by default."""
    del owner
    return _review_status_for_row(row) in {
        "ready_for_review",
        "fallback_review_required",
        "blocked_or_rejected",
    }


def _matches_review_filter(owner: object, row: dict) -> bool:
    """Return whether a row matches the active review filter."""
    current = owner._review_filter_combo.currentText().strip().lower()
    status = _review_status_for_row(row)
    severity = _review_severity_for_row(row)
    source = str(row.get("generation_source") or row.get("source") or "").lower()
    confidence = str(row.get("confidence") or "").lower()

    if not is_reviewable_docstring_row(row):
        return False
    if current == "all":
        return True
    if current == "needs review":
        return _row_needs_review(owner, row)
    if current == "ready for review":
        return status == "ready_for_review"
    if current == "fallback review":
        return status == "fallback_review_required"
    if current == "blocked/rejected":
        return status == "blocked_or_rejected"
    if current == "warnings/errors":
        return severity in {"warning", "error"}
    if current == "ai only":
        return source in {"ai", "local_ai", "structured_ai"}
    if current == "fallback only":
        return source in {"fallback", "heuristic", "heuristic_fallback"}
    if current == "low confidence":
        return confidence == "low"
    return True


def _populate_review_list(owner: object) -> None:
    """Populate the review list from loaded rows."""
    Qt = _qt_core("Qt")
    QListWidgetItem = _qt_widgets("QListWidgetItem")

    owner._review_list.clear()
    for row in getattr(owner, "_report_rows", []) or []:
        if not _matches_review_filter(owner, row):
            continue
        item = QListWidgetItem(_row_title(row))
        item.setData(Qt.UserRole, row)
        owner._review_list.addItem(item)
    if owner._review_list.count() > 0 and owner._review_list.currentRow() < 0:
        owner._review_list.setCurrentRow(0)
    else:
        refresh_inline_corrector_for_selection(owner, _row_from_item(owner._review_list.currentItem()))
    _refresh_review_summary(owner)


def _show_review_item_details(owner: object, current: Any, previous: Any = None) -> None:
    """Show JSON and source context for the selected review row."""
    del previous
    row = _row_from_item(current)
    owner._review_details.setPlainText(_format_review_row_context(owner, row))
    refresh_inline_corrector_for_selection(owner, row)


def _open_docstring_review_window(owner: object, item: Any = None) -> None:
    """Open the manual docstring review dialog for one selected row."""
    if item is None:
        item = owner._review_list.currentItem()
    row = _row_from_item(item)
    if not row:
        return
    module_name = (
        "kanda_reasoner_app.insert_missing_docstrings_gui."
        + "insert_missing_docstrings_gui_help.manual_docstring_review_editor"
    )
    editor_module = import_module(module_name)
    dialog = editor_module.DocstringReviewEditorDialog(owner, row)
    exec_method = getattr(dialog, "exec", None)
    if callable(exec_method):
        exec_method()
    _populate_review_list(owner)
    _show_review_item_details(owner, row)


def _read_report_rows(path: Path) -> list[dict]:
    """Read report rows from JSON or JSONL content."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    stripped = text.strip()
    if not stripped:
        return []
    if stripped.startswith("["):
        return _rows_from_json_array(stripped)
    rows: list[dict] = []
    for line in text.splitlines():
        row = _row_from_json_line(line)
        if row is not None:
            rows.append(row)
    return rows


def _rows_from_json_array(text: str) -> list[dict]:
    """Return rows from a JSON array report."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def _row_from_json_line(line: str) -> dict | None:
    """Return one row from a JSONL line."""
    stripped = line.strip()
    if not stripped:
        return None
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _row_title(row: dict) -> str:
    """Return a compact list title for one report row."""
    status = _review_status_for_row(row)
    file_name = str(row.get("file") or row.get("path") or "<unknown>")
    line = str(row.get("line") or row.get("insert_line") or "")
    target = str(row.get("target_name") or row.get("name") or "<module>")
    return status + " | " + file_name + ":" + line + " | " + target


def _row_from_item(item: Any) -> dict | None:
    """Return stable row data from a row dict or a QListWidgetItem."""
    if item is None:
        return None
    if isinstance(item, dict):
        return item
    Qt = _qt_core("Qt")
    try:
        data = item.data(Qt.UserRole)
    except RuntimeError:
        return None
    return data if isinstance(data, dict) else None



def _qt_core(name: str) -> Any:
    """Return one Qt core object lazily."""
    module = import_module("PySide" + "6.QtCore")
    return getattr(module, name)


def _qt_widgets(name: str) -> Any:
    """Return one Qt widget class lazily."""
    module = import_module("PySide" + "6.QtWidgets")
    return getattr(module, name)
