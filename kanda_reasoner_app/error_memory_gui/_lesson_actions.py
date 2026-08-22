# project-path: kanda_reasoner_app/error_memory_gui/_lesson_actions.py
"""Lesson action helpers for the Error Memory tab.

This module owns selected lesson save/delete/status action workflows that are
called by the public tab facade.  It intentionally does not import
``error_memory_tab``; callers pass the tab object so the public import path remains stable.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.models import active_ready, active_ready_missing_reasons, utc_now_iso
from kanda_reasoner_app.error_memory.store import delete_lesson, list_lessons, save_lesson
from kanda_reasoner_app.error_memory_gui._window_sync import clear_error_memory_work_windows
from kanda_reasoner_app.error_memory_gui._owner_lane import (
    backend_for_current_work_item,
)

__all__ = [
    "delete_selected_lesson",
    "lesson_from_preview_or_selection",
    "save_draft_lesson_from_partial",
    "save_preview_lesson",
    "set_selected_lesson_status",
    "supersede_selected_lesson",
    "undo_lesson_action",
]


def _message_box():
    """Support message box behavior.
    """
    
    from PySide6.QtWidgets import QMessageBox

    return QMessageBox


def _input_dialog():
    """Support input dialog behavior.
    """
    
    from PySide6.QtWidgets import QInputDialog

    return QInputDialog


def _show_error(parent: Any, *, title: str, message: str) -> None:
    """Support show error behavior.
    
    Parameters
    ----------
    parent : Any
        The parent value.
    title : str
        The title value.
    message : str
        The message text.
    """
    
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    show_error_copy_close_window(parent, title=title, message=message)


def save_preview_lesson(tab: Any) -> None:
    """Save the JSON currently shown in Error Editor."""
    QMessageBox = _message_box()
    text = tab.received_preview_edit.toPlainText().strip()
    if not text:
        QMessageBox.warning(tab, 'Error Memory', 'No lesson JSON is shown in Error Editor.')
        return
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        _show_error(tab, title='Error Memory', message='Error Editor is not valid JSON:\n' + str(exc))
        return
    if not isinstance(payload, dict):
        _show_error(tab, title='Error Memory', message='Error Editor JSON must be one lesson object.')
        return
    if not str(payload.get('lesson_id', '')).strip():
        _show_error(tab, title='Error Memory', message='Error Editor JSON is missing lesson_id.')
        return
    try:
        path = save_lesson(backend_for_current_work_item(tab), payload)
    except Exception as exc:
        _show_error(tab, title='Error Memory save failed', message=str(exc))
        return
    tab._consume_loaded_pending_intake_file_if_matches(payload, allow_lesson_id_change=True)
    tab._selected_lesson_id = str(payload.get('lesson_id', ''))
    tab._last_received_lesson = payload
    tab._reload_table()
    clear_error_memory_work_windows(tab)
    tab._show_action_done('Error Memory', 'Saved lesson.', str(path))


def delete_selected_lesson(tab: Any) -> None:
    """Delete the selected lesson and keep Undo state on the tab."""
    QMessageBox = _message_box()
    lesson_id = tab._selected_lesson_id_from_table()
    if not lesson_id:
        QMessageBox.warning(tab, 'Error Memory', 'Select a lesson in the Lessons table first.')
        return
    answer = QMessageBox.question(tab, 'Delete Error Memory lesson', 'Delete selected lesson from project_error_memory?\n\n' + lesson_id + '\n\nUse Undo to restore it before deleting another lesson.')
    if answer != QMessageBox.Yes:
        return
    try:
        tab._undo_deleted_lesson = delete_lesson(tab._current_project_root(), lesson_id)
    except Exception as exc:
        _show_error(tab, title='Error Memory delete failed', message=str(exc))
        return
    tab._selected_lesson_id = ''
    tab.received_preview_edit.setPlainText(json.dumps(tab._undo_deleted_lesson, indent=2, sort_keys=True, ensure_ascii=False))
    tab._reload_table()
    tab._show_action_done('Error Memory', 'Deleted lesson.', 'Use Undo to restore it if needed.')


def lesson_from_preview_or_selection(tab: Any) -> dict[str, Any] | None:
    """Return the preview lesson JSON or load the selected lesson."""
    text = tab.received_preview_edit.toPlainText().strip()
    if text:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict) and str(payload.get('lesson_id', '')).strip():
            return payload
    lesson_id = tab._selected_lesson_id_from_table()
    if not lesson_id:
        return None
    lessons = list_lessons(tab._current_project_root(), include_inactive=True)
    return next((item for item in lessons if item.get('lesson_id') == lesson_id), None)


def save_draft_lesson_from_partial(tab: Any, lesson: dict[str, Any], *, source_text: str, success_prefix: str) -> Path | None:
    """Canonicalize and save an incomplete lesson as a draft."""
    draft = tab._canonical_draft_lesson_from_partial(dict(lesson or {}), source_text=source_text)
    draft['status'] = 'draft'
    draft['updated_at_utc'] = utc_now_iso()
    try:
        path = save_lesson(backend_for_current_work_item(tab), draft)
    except Exception as exc:
        _show_error(tab, title='Error Memory draft save failed', message=str(exc))
        return None
    tab._selected_lesson_id = str(draft.get('lesson_id', ''))
    tab._last_received_lesson = draft
    tab.received_preview_edit.setPlainText(json.dumps(draft, indent=2, sort_keys=True, ensure_ascii=False))
    tab._consume_loaded_pending_intake_file_if_matches(draft, allow_lesson_id_change=True)
    tab._reload_table()
    clear_error_memory_work_windows(tab)
    missing_text = tab._active_ready_missing_text(draft)
    if missing_text == 'None. This lesson is active-ready.':
        detail = 'Saved as draft. It is active-ready, but it was not promoted to active. Use Mark Active after review.'
    else:
        detail = 'Saved as draft and consumed the matching pending intake source when present. It was not promoted to active and still needs AI correction or manual completion.\n\nMissing active-ready items:\n- ' + missing_text
    tab._show_action_done('Error Memory', success_prefix + '.', str(path) + '\n\n' + detail)
    return path


def set_selected_lesson_status(tab: Any, status: str) -> None:
    """Set the selected/preview lesson status and save it safely."""
    QMessageBox = _message_box()
    lesson = tab._lesson_from_preview_or_selection()
    if lesson is None:
        QMessageBox.warning(tab, 'Error Memory', 'Select a lesson or load one into Error Editor first.')
        return
    if status == 'active':
        if not active_ready(lesson):
            missing_reasons = active_ready_missing_reasons(dict(lesson))
            QMessageBox.warning(tab, 'Cannot mark active', 'This lesson is not ready for active status. Active lessons must have the same required fields, prevention triggers, and redaction metadata required by Memorize Error.\n\nMissing or invalid items:\n- ' + '\n- '.join(missing_reasons[:20]))
            return
        answer = QMessageBox.question(tab, 'Mark lesson active', 'Mark this lesson ACTIVE?\n\nOnly active lessons are exported as enforced guidance for AI. Confirm this only after you reviewed the Error Editor content.')
        if answer != QMessageBox.Yes:
            return
    if status == 'deprecated':
        answer = QMessageBox.question(tab, 'Deprecate lesson', 'Deprecate this lesson? It will remain in memory but should not be used as active guidance.')
        if answer != QMessageBox.Yes:
            return
    if status == 'active':
        lesson['status'] = 'active'

        # A loaded pending intake candidate has not crossed the human
        # Memorize Error commit boundary yet.  Mark Active is therefore a
        # preview/status action for that candidate, not a second save path.
        pending_path = str(
            getattr(tab, '_loaded_pending_intake_file', '') or ''
        ).strip()
        if pending_path:
            lesson.pop('intended_status', None)
            tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
            tab._last_received_lesson = dict(lesson)
            tab.received_preview_edit.setPlainText(
                json.dumps(
                    lesson,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                )
            )
            tab.raw_error_edit.setPlainText(
                tab._formatted_lesson_block(lesson)
            )
            tab._refresh_heuristic_correction_button_state()
            tab._show_action_done(
                'Error Memory',
                'Marked pending lesson active in preview.',
                (
                    'Nothing was saved or consumed. Review the corrected '
                    'active lesson, then press Memorize Error to perform the '
                    'single human-controlled canonical write.'
                ),
            )
            return

        # Existing saved lessons keep their status-update behavior.
        tab._save_active_ready_lesson(
            lesson,
            'Updated lesson status to active',
        )
        return
    if status == 'draft':
        source_text = tab.received_preview_edit.toPlainText().strip() or tab.raw_error_edit.toPlainText().strip()
        tab._save_draft_lesson_from_partial(dict(lesson), source_text=source_text, success_prefix='Updated lesson status to draft')
        return
    lesson['status'] = status
    lesson['updated_at_utc'] = utc_now_iso()
    try:
        path = save_lesson(backend_for_current_work_item(tab), lesson)
    except Exception as exc:
        _show_error(tab, title='Error Memory status update failed', message=str(exc))
        return
    tab._consume_loaded_pending_intake_file_if_matches(lesson, allow_lesson_id_change=True)
    tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
    tab._last_received_lesson = lesson
    tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))
    tab._reload_table()
    clear_error_memory_work_windows(tab)
    tab._show_action_done('Error Memory', 'Updated lesson status to ' + status + '.', str(path))


def supersede_selected_lesson(tab: Any) -> None:
    """Mark the selected lesson as superseded by another lesson id."""
    QMessageBox = _message_box()
    QInputDialog = _input_dialog()
    lesson = tab._lesson_from_preview_or_selection()
    if lesson is None:
        QMessageBox.warning(tab, 'Error Memory', 'Select a lesson or load one into Error Editor first.')
        return
    replacement_id, ok = QInputDialog.getText(tab, 'Supersede lesson', 'Replacement lesson_id, for example lesson-05cffd935c8b:')
    if not ok:
        return
    replacement_id = replacement_id.strip()
    if not replacement_id.startswith('lesson-'):
        QMessageBox.warning(tab, 'Error Memory', 'Replacement ID must start with lesson-.')
        return
    lesson['status'] = 'superseded'
    lesson['superseded_by'] = replacement_id
    lesson['updated_at_utc'] = utc_now_iso()
    try:
        path = save_lesson(backend_for_current_work_item(tab), lesson)
    except Exception as exc:
        _show_error(tab, title='Error Memory supersede failed', message=str(exc))
        return
    tab._consume_loaded_pending_intake_file_if_matches(lesson, allow_lesson_id_change=True)
    tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
    tab._last_received_lesson = lesson
    tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))
    tab._reload_table()
    clear_error_memory_work_windows(tab)
    tab._show_action_done('Error Memory', 'Superseded lesson.', str(path))


def undo_lesson_action(tab: Any) -> None:
    """Restore a deleted lesson or reload the selected lesson into preview."""
    QMessageBox = _message_box()
    if tab._undo_deleted_lesson:
        try:
            path = save_lesson(tab._current_project_root(), tab._undo_deleted_lesson)
        except Exception as exc:
            _show_error(tab, title='Error Memory undo failed', message=str(exc))
            return
        tab._selected_lesson_id = str(tab._undo_deleted_lesson.get('lesson_id', ''))
        tab.received_preview_edit.setPlainText(json.dumps(tab._undo_deleted_lesson, indent=2, sort_keys=True, ensure_ascii=False))
        tab._undo_deleted_lesson = None
        tab._reload_table()
        tab._show_action_done('Error Memory', 'Restored deleted lesson.', str(path))
        return
    lesson_id = tab._selected_lesson_id_from_table()
    if not lesson_id:
        QMessageBox.information(tab, 'Error Memory', 'Nothing to undo. Select a lesson to reload it into preview.')
        return
    tab._load_selected_lesson_into_preview()
