# project-path: kanda_reasoner_app/error_memory_gui/_memorize_flow.py
"""Memorize active-ready lesson workflow helpers for the Error Memory tab.

The public tab keeps facade wrappers.  This private helper owns the active
Memorize Error promotion workflow and intentionally does not import the
``error_memory_tab`` facade.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.models import active_ready, utc_now_iso
from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
from kanda_reasoner_app.error_memory_gui._duplicate_pending_cleanup import (
    delete_matching_pending_duplicate_candidates,
)
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    DuplicateLessonMatch,
    resolve_duplicate_lesson_copies,
)
from kanda_reasoner_app.error_memory_gui._window_sync import clear_error_memory_work_windows
from kanda_reasoner_app.error_memory_gui._owner_lane import (
    backend_for_current_work_item,
)

__all__ = [
    "candidate_text_for_memorize",
    "clear_ai_assisted_intake_after_memorize",
    "consume_loaded_pending_intake_file_if_matches",
    "memorize_error_from_text_window",
    "selected_saved_draft_id_for_memorize",
    "resolve_duplicate_memorize_candidate",
    "save_active_ready_lesson",
    "select_saved_active_lesson_row",
]


def _message_box():
    """Support message box behavior.
    """
    
    from PySide6.QtWidgets import QMessageBox

    return QMessageBox


def _qt_user_role():
    """Support qt user role behavior.
    """
    
    from PySide6.QtCore import Qt

    return Qt.UserRole


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


def candidate_text_for_memorize(tab: Any) -> tuple[str, str]:
    """Prefer the editable lesson JSON, then the intake text window."""
    editor_text = tab.received_preview_edit.toPlainText().strip()
    if tab._text_has_formatted_lesson_payload(editor_text):
        return (editor_text, 'Error Editor')
    raw_text = tab.raw_error_edit.toPlainText().strip()
    if tab._text_has_formatted_lesson_payload(raw_text):
        return (raw_text, 'AI-assisted error lesson intake')
    return ('', '')


def save_active_ready_lesson(tab: Any, lesson: dict[str, Any], success_prefix: str) -> Path | None:
    """Save an active-ready lesson and update editor/table state."""
    QMessageBox = _message_box()
    lesson = dict(lesson)
    lesson['status'] = 'active'
    if not active_ready(lesson):
        tab.received_preview_edit.setPlainText(
            json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)
        )
        _show_error(
            tab,
            title="Lesson is not active-ready",
            message=(
                "This lesson is not active-ready. Complete the missing items "
                "before saving as active.\n\nMissing or invalid items:\n- "
                + tab._active_ready_missing_text(lesson)
            ),
        )
        return None
    lesson['updated_at_utc'] = utc_now_iso()
    try:
        path = save_lesson(backend_for_current_work_item(tab), lesson)
    except Exception as exc:
        _show_error(tab, title='Error Memory save failed', message=str(exc))
        return None
    tab._consume_loaded_pending_intake_file_if_matches(lesson, allow_lesson_id_change=True)
    tab._selected_lesson_id = str(lesson.get('lesson_id', ''))
    tab._last_received_lesson = lesson
    tab.received_preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))
    tab._reload_table()
    clear_error_memory_work_windows(tab)
    tab._show_action_done('Error Memory', success_prefix + '.', str(path))
    return path


def consume_loaded_pending_intake_file_if_matches(tab: Any, lesson: dict[str, Any], *, allow_lesson_id_change: bool = False) -> bool:
    """Remove the loaded pending intake source after a successful save.

    Draft saves keep the conservative lesson_id match by default.  Active
    Memorize Error promotion may allow a lesson_id change because the user
    intentionally selected one pending item, sent it to AI for correction,
    pasted the corrected lesson, and clicked Memorize Error.
    """
    marker = str(tab._loaded_pending_intake_file or '').strip()
    if not marker:
        return False
    loaded_lesson_id = str(tab._loaded_pending_intake_lesson_id or '').strip()
    saved_lesson_id = str(lesson.get('lesson_id', '')).strip()
    if (not allow_lesson_id_change) and loaded_lesson_id and saved_lesson_id and loaded_lesson_id != saved_lesson_id:
        return False
    try:
        pending_path = Path(marker).expanduser().resolve(strict=False)
    except Exception:
        return False
    try:
        if pending_path.exists() and pending_path.is_file():
            pending_path.unlink()
    except Exception:
        pass
    tab._dismissed_pending_intake_files.add(str(pending_path))
    if loaded_lesson_id:
        tab._dismissed_pending_intake_lesson_ids.add(loaded_lesson_id)
    tab._loaded_pending_intake_file = ''
    tab._loaded_pending_intake_lesson_id = ''
    return True



def resolve_duplicate_memorize_candidate(
    tab: Any,
    lesson: dict[str, Any],
) -> DuplicateLessonMatch | None:
    """Delete duplicate saved Lessons and consume the current candidate.

    A single saved Lesson is treated as the target only when no separate pending
    candidate is loaded.  If a pending candidate or another saved Lesson matches
    the same error family, this helper deletes draft/invalid duplicate saved
    records, consumes pending candidates, clears both work windows, and stops
    Memorize Error from inserting another copy.
    """
    target_backend = backend_for_current_work_item(tab)
    had_pending = bool(str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip())
    selected_id = str(getattr(tab, "_selected_lesson_id", "") or lesson.get("lesson_id", "")).strip()
    match = resolve_duplicate_lesson_copies(
        target_backend,
        lesson,
        candidate_has_pending_source=had_pending,
        delete_candidate_lesson_id=selected_id,
    )
    pending_deleted = 0
    pending_failures: tuple[str, ...] = ()

    if match is None:
        return None

    pending_deleted, pending_failures = delete_matching_pending_duplicate_candidates(tab, lesson)
    tab._consume_loaded_pending_intake_file_if_matches(
        lesson,
        allow_lesson_id_change=True,
    )
    tab._reload_table()
    clear_error_memory_work_windows(tab)

    if match.deleted_lesson_ids:
        message = (
            "Candidate and duplicate saved Lessons deleted because this "
            "error is already duplicated in Lessons."
        )
    else:
        message = (
            "Candidate deleted because an active-ready Lesson already exists. "
            "No saved Lesson was deleted."
        )
    details = (
        "Preserved lesson_id: " + str(match.lesson_id or "") + "\n"
        "Preserved status: " + str(match.status or "unknown") + "\n"
        "Deleted saved lesson_id(s): " + ", ".join(match.deleted_lesson_ids or ("None",)) + "\n"
        "Deleted pending duplicate file(s): " + str(pending_deleted) + "\n"
        "Skipped saved lesson_id(s): " + ", ".join(match.skipped_lesson_ids or ("None",)) + "\n"
        "Pending cleanup failures: " + "; ".join(pending_failures or ("None",)) + "\n"
        "Duplicate reason: " + match.reason
    )
    tab._show_action_done(
        "Error Memory duplicate cleanup",
        message,
        details,
    )
    return match


def _selected_lesson_id_for_memorize(tab: Any) -> str:
    """Return the saved lesson id currently targeted by Memorize Error."""
    selector = getattr(tab, "_selected_lesson_id_from_table", None)
    if callable(selector):
        try:
            selected = str(selector() or "").strip()
        except Exception:
            selected = ""
        if selected:
            return selected
    return str(getattr(tab, "_selected_lesson_id", "") or "").strip()


def selected_saved_draft_id_for_memorize(tab: Any) -> str:
    """Return selected saved draft id for explicit Memorize promotion.

    Pending intake rows are not treated as saved-draft targets here; their
    source file consumption remains owned by the existing pending-intake save
    path.  This helper protects the selected saved draft when Correct with AI
    leaves an AI-generated lesson_id in the editor text.
    """
    if str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip():
        return ""
    lesson_id = _selected_lesson_id_for_memorize(tab)
    if not lesson_id:
        return ""
    try:
        lessons = list_lessons(tab._current_project_root(), include_inactive=True)
    except Exception:
        return ""
    for item in lessons:
        if str(item.get("lesson_id", "") or "").strip() != lesson_id:
            continue
        if str(item.get("status", "") or "").strip().lower() == "draft":
            return lesson_id
        return ""
    return ""


def _warn_selected_draft_not_active_ready(tab: Any, lesson: dict[str, Any]) -> None:
    """Keep corrected selected-draft text visible when active promotion fails."""
    message = (
        "Memorize Error did not promote this draft because required "
        "active-ready fields are still missing. The corrected text was kept "
        "in Error Editor for review.\n\nMissing or invalid items:\n- "
        + tab._active_ready_missing_text(lesson)
    )
    tab.received_preview_edit.setPlainText(
        json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)
    )
    _show_error(tab, title="Lesson is not active-ready", message=message)

def select_saved_active_lesson_row(tab: Any, lesson_id: str) -> bool:
    """Select the saved active lesson row after pending intake promotion."""
    normalized_id = str(lesson_id or '').strip()
    if not normalized_id:
        return False
    user_role = _qt_user_role()
    for row in range(tab.lessons_table.rowCount()):
        if tab._row_kind_for_row(row) != 'lesson':
            continue
        item = tab.lessons_table.item(row, 4)
        if item is None:
            continue
        row_lesson_id = str(item.data(user_role) or item.text() or '').strip()
        if row_lesson_id != normalized_id:
            continue
        tab.lessons_table.selectRow(row)
        tab.lessons_table.scrollToItem(item)
        tab._selected_lesson_id = normalized_id
        return True
    return False


def clear_ai_assisted_intake_after_memorize(tab: Any, lesson: dict[str, Any]) -> None:
    """Consume pending intake, reload the table, and clear both windows."""
    tab._consume_loaded_pending_intake_file_if_matches(lesson, allow_lesson_id_change=True)
    tab._reload_table()
    clear_error_memory_work_windows(tab)


def _pending_intended_status_for_memorize(
    lesson: dict[str, Any],
) -> str | None:
    """Return a validated intended status for one pending transport candidate."""
    if str(lesson.get("status") or "").strip().lower() != "pending":
        return None
    intended_status = str(lesson.get("intended_status") or "").strip().lower()
    if intended_status not in {"active", "draft"}:
        raise ValueError(
            "Pending Error Memory lesson intended_status must be active or draft."
        )
    return intended_status


def memorize_error_from_text_window(tab: Any) -> None:
    """Promote the current formatted lesson through the human Error Memory gate."""
    QMessageBox = _message_box()
    text, source_label = tab._candidate_text_for_memorize()
    if not text:
        QMessageBox.warning(tab, 'Formatted lesson required', 'Memorize Error accepts only a KANDA_ERROR_LESSON_JSON block, one valid lesson JSON object, or the edited JSON currently shown in Error Editor.')
        return
    try:
        lesson = tab._lesson_from_formatted_text(text)
        pending_intended_status = _pending_intended_status_for_memorize(lesson)
    except Exception as exc:
        _show_error(tab, title='Error Memory', message='Could not parse formatted lesson:\n' + str(exc))
        return
    if pending_intended_status is not None:
        lesson = dict(lesson)
        lesson['status'] = pending_intended_status
        lesson.pop('intended_status', None)
    selected_draft_id = selected_saved_draft_id_for_memorize(tab)
    if selected_draft_id:
        lesson['lesson_id'] = selected_draft_id
    if tab._resolve_duplicate_memorize_candidate(dict(lesson)) is not None:
        return
    if pending_intended_status == 'draft':
        tab._save_draft_lesson_from_partial(
            dict(lesson),
            source_text=text,
            success_prefix='Memorized Error lesson as draft',
        )
        return
    if not active_ready(dict(lesson)):
        if selected_draft_id:
            _warn_selected_draft_not_active_ready(tab, dict(lesson))
            return
        tab._save_draft_lesson_from_partial(
            dict(lesson),
            source_text=text,
            success_prefix='Memorized Error lesson as draft',
        )
        return
    lesson['status'] = 'active'
    lesson['promotion_status'] = 'active_ready'
    path = tab._save_active_ready_lesson(lesson, 'Memorized active Error Memory lesson')
    if path is not None:
        tab._clear_ai_assisted_intake_after_memorize(lesson)
