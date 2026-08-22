# project-path: kanda_reasoner_app/error_memory_gui/_table_view.py
"""Lessons-table rendering and selection helpers for the Error Memory tab.

This private helper owns Lessons table row rendering, table metadata access,
and selection-to-editor loading for the public tab facade. It keeps
Qt imports local so helper import smoke stays headless-safe, and it does not
import the origin module upward into the facade.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
)
from kanda_reasoner_app.error_memory.store import list_lessons
from kanda_reasoner_app.error_memory_gui._lesson_status_summary import (
    normalized_lesson_status,
    render_lesson_status_summary,
    status_matches_summary_priority,
)

__all__ = [
    "formatted_lesson_block",
    "lesson_id_for_row",
    "lesson_from_current_windows_or_selection",
    "lesson_json_text_for_windows",
    "load_selected_lesson_into_preview",
    "pending_path_for_row",
    "reload_table",
    "row_kind_for_row",
    "selected_lesson_id_from_table",
    "set_ai_assisted_intake_and_error_editor_from_pending_text",
]



def _row_status_for_table(kind: str, payload: dict[str, Any]) -> str:
    """Return the status key used for status-summary prioritization."""
    if kind == "pending":
        return normalized_lesson_status(payload.get("status") or payload.get("kind"))
    return normalized_lesson_status(payload.get("status"))


def _ordered_lesson_rows(
    pending_rows: list[dict[str, Any]],
    lessons: list[dict[str, Any]],
    priority_status: str,
) -> list[tuple[str, dict[str, Any]]]:
    """Return pending and saved rows with the clicked status first."""
    rows: list[tuple[str, dict[str, Any], int, str]] = []
    index = 0
    for pending in pending_rows:
        rows.append(("pending", pending, index, _row_status_for_table("pending", pending)))
        index += 1
    for lesson in lessons:
        rows.append(("lesson", lesson, index, _row_status_for_table("lesson", lesson)))
        index += 1
    preferred = normalized_lesson_status(priority_status)
    if preferred:
        rows.sort(
            key=lambda item: (
                0 if status_matches_summary_priority(item[3], preferred) else 1,
                item[2],
            )
        )
    return [(kind, payload) for kind, payload, _index, _status in rows]

def formatted_lesson_block(lesson: dict[str, Any]) -> str:
    """Return the copy/paste formatted lesson block used by AI intake."""
    return (
        ERROR_LESSON_JSON_BEGIN
        + "\n"
        + json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n"
        + ERROR_LESSON_JSON_END
    )


def lesson_json_text_for_windows(lesson: dict[str, Any]) -> str:
    """Return the canonical JSON text shown in both Error Memory windows."""
    return json.dumps(dict(lesson), indent=2, sort_keys=True, ensure_ascii=False)


def reload_table(tab: Any, *, row_kind_role: int, pending_path_role: int) -> None:
    """Render saved and virtual pending lessons into the Lessons table."""
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QTableWidgetItem

    provider = getattr(tab, "_canonical_error_memory_lessons", None)
    if callable(provider):
        try:
            lessons = list(provider())
        except Exception:
            lessons = []
    else:
        try:
            project_root = tab._current_project_root()
            lessons = (
                list_lessons(project_root, include_inactive=True)
                if project_root is not None
                else []
            )
        except Exception:
            lessons = []
    pending_rows = tab._pending_lesson_rows_for_table()
    render_lesson_status_summary(tab, lessons, pending_rows)
    priority_status = getattr(tab, "_lesson_status_priority_status", "")
    row_records = _ordered_lesson_rows(pending_rows, lessons, priority_status)
    tab.lessons_table.blockSignals(True)
    try:
        tab.lessons_table.setRowCount(len(row_records))
        for row, row_record in enumerate(row_records):
            row_kind, payload = row_record
            values = [
                payload.get('status', ''),
                payload.get('symptom', ''),
                payload.get('do_not_repeat_rule', ''),
                payload.get('updated_at_utc', ''),
                payload.get('lesson_id', ''),
            ]
            if row_kind == 'pending':
                stored_row_kind = str(payload.get('kind', 'pending_edit'))
                pending_path = str(payload.get('pending_path', ''))
            else:
                stored_row_kind = 'lesson'
                pending_path = ''
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.UserRole, str(payload.get('lesson_id', '')))
                item.setData(row_kind_role, stored_row_kind)
                item.setData(pending_path_role, pending_path)
                tab.lessons_table.setItem(row, col, item)
    finally:
        tab.lessons_table.blockSignals(False)
    tab.lessons_table.resizeColumnsToContents()


def row_kind_for_row(table: Any, row: int, *, row_kind_role: int) -> str:
    """Return the virtual row kind for one Lessons table row."""
    if row < 0:
        return ''
    item = table.item(row, 4)
    if item is None:
        return ''
    return str(item.data(row_kind_role) or 'lesson')


def pending_path_for_row(table: Any, row: int, *, pending_path_role: int) -> str:
    """Return the pending source path attached to one Lessons table row."""
    if row < 0:
        return ''
    item = table.item(row, 4)
    if item is None:
        return ''
    return str(item.data(pending_path_role) or '')


def lesson_id_for_row(tab: Any, row: int) -> str:
    """Return the canonical lesson_id for one non-pending Lessons table row."""
    from PySide6.QtCore import Qt

    if row < 0 or tab._row_kind_for_row(row) != 'lesson':
        return ''
    item = tab.lessons_table.item(row, 4)
    if item is None:
        return ''
    return str(item.data(Qt.UserRole) or item.text() or '')


def selected_lesson_id_from_table(tab: Any) -> str:
    """Return the selected canonical lesson_id, or the last selected id."""
    selected = tab.lessons_table.selectionModel().selectedRows() if tab.lessons_table.selectionModel() else []
    if not selected:
        return tab._selected_lesson_id
    return tab._lesson_id_for_row(selected[0].row())


def set_ai_assisted_intake_and_error_editor_from_pending_text(tab: Any, formatted_text: str, lesson: dict[str, Any]) -> None:
    """Render pending-intake text and Error Editor JSON from one lesson."""
    tab.raw_error_edit.setPlainText(formatted_text.strip())
    tab.received_preview_edit.setPlainText(lesson_json_text_for_windows(lesson))
    tab._refresh_heuristic_correction_button_state()



def lesson_from_current_windows_or_selection(tab: Any) -> dict[str, Any] | None:
    """Return the lesson currently visible in Error Editor, intake, or table.

    This helper is imported by the Error Memory table/draft mixin.  Keeping it
    in _table_view preserves the post-refactor import surface while avoiding
    an upward import into the public ErrorMemoryTab facade.
    """
    for text in (tab.received_preview_edit.toPlainText(), tab.raw_error_edit.toPlainText()):
        stripped = str(text or '').strip()
        if not stripped:
            continue
        try:
            lesson = tab._lesson_from_formatted_text(stripped)
        except Exception:
            continue
        if isinstance(lesson, dict) and str(lesson.get('lesson_id', '')).strip():
            return dict(lesson)
    return tab._lesson_from_preview_or_selection()

def load_selected_lesson_into_preview(tab: Any) -> None:
    """Load selected saved or pending Lessons row into the editor surfaces."""
    from PySide6.QtWidgets import QMessageBox

    selected = tab.lessons_table.selectionModel().selectedRows() if tab.lessons_table.selectionModel() else []
    if selected:
        row = selected[0].row()
        row_kind = tab._row_kind_for_row(row)
        pending_path = tab._pending_path_for_row(row)
        if row_kind.startswith('pending') and pending_path:
            tab._load_pending_intake_row_into_editor(Path(pending_path), row_kind)
            return
    lesson_id = tab._selected_lesson_id_from_table()
    if not lesson_id:
        return
    try:
        provider = getattr(tab, "_canonical_error_memory_lessons", None)
        if callable(provider):
            lessons = list(provider())
        else:
            lessons = list_lessons(tab._current_project_root(), include_inactive=True)
        lesson = next((item for item in lessons if item.get('lesson_id') == lesson_id), None)
        if lesson is None:
            return
    except Exception as exc:
        QMessageBox.warning(tab, 'Error Memory', 'Could not load selected lesson: ' + str(exc))
        return
    tab._selected_lesson_id = lesson_id
    tab._last_received_lesson = dict(lesson)
    tab._loaded_pending_intake_file = ''
    tab._loaded_pending_intake_lesson_id = ''
    tab.raw_error_edit.clear()
    tab.received_preview_edit.clear()
    tab.raw_error_edit.setPlainText(tab._formatted_lesson_block(lesson))
    tab.received_preview_edit.setPlainText(lesson_json_text_for_windows(lesson))
