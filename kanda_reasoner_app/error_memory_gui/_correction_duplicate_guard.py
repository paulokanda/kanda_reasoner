# project-path: kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py
"""Duplicate cleanup guard for Error Memory correction actions.

Heuristic Correction and Correct with AI are preview/correction actions.  When
Lessons already contains duplicate records for the same error, correction would
create or preserve yet another copy.  The safe behavior is to delete draft or
not-active-ready saved duplicate Lessons, consume the loaded pending candidate
when one exists, clear the work windows, and stop correction.
"""
from __future__ import annotations

from typing import Any

from kanda_reasoner_app.error_memory_gui._duplicate_pending_cleanup import (
    delete_matching_pending_duplicate_candidates,
)
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    DuplicateLessonMatch,
    resolve_duplicate_lesson_copies,
)
from kanda_reasoner_app.error_memory_gui._window_sync import clear_error_memory_work_windows

__all__ = [
    "consume_duplicate_correction_candidate",
]


def _loaded_pending_marker(tab: Any) -> str:
    """Return the loaded pending source marker, when one is active."""
    return str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip()


def _consume_pending_candidate(tab: Any, lesson: dict[str, Any]) -> bool:
    """Consume the loaded pending candidate, when one is active."""
    consumer = getattr(tab, "_consume_loaded_pending_intake_file_if_matches", None)
    if not callable(consumer):
        return False
    try:
        return bool(consumer(lesson, allow_lesson_id_change=True))
    except Exception:
        return False


def _project_root_for_tab(tab: Any) -> Any:
    """Return the best project root value available on the tab."""
    project_getter = getattr(tab, "_current_project_root", None)
    if callable(project_getter):
        try:
            return project_getter()
        except Exception:
            pass
    return getattr(tab, "_project_root", "")


def _show_duplicate_correction_message(
    tab: Any,
    *,
    action_label: str,
    match: DuplicateLessonMatch,
    consumed: bool,
    pending_deleted: int = 0,
    pending_failures: tuple[str, ...] = (),
) -> None:
    """Show the correction duplicate cleanup result in the normal float window."""
    if match.deleted_lesson_ids:
        message = (
            "Candidate and duplicate saved Lessons deleted because this "
            "error is already duplicated in Lessons."
        )
    elif consumed:
        message = (
            "Candidate deleted because an active-ready Lesson already exists. "
            "No saved Lesson was deleted."
        )
    else:
        message = (
            "Correction skipped because this error already has duplicate "
            "entries in Lessons. No pending candidate file was loaded."
        )
    details = (
        "Action: " + action_label + "\n"
        "Preserved lesson_id: " + str(match.lesson_id or "") + "\n"
        "Preserved status: " + str(match.status or "unknown") + "\n"
        "Deleted saved lesson_id(s): " + ", ".join(match.deleted_lesson_ids or ("None",)) + "\n"
        "Deleted pending duplicate file(s): " + str(pending_deleted) + "\n"
        "Skipped saved lesson_id(s): " + ", ".join(match.skipped_lesson_ids or ("None",)) + "\n"
        "Pending cleanup failures: " + "; ".join(pending_failures or ("None",)) + "\n"
        "Duplicate reason: " + str(match.reason or "")
    )
    notifier = getattr(tab, "_show_action_done", None)
    if callable(notifier):
        notifier("Error Memory duplicate cleanup", message, details)
        return
    try:
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.information(tab, "Error Memory duplicate cleanup", message + "\n\n" + details)
    except Exception:
        return


def consume_duplicate_correction_candidate(
    tab: Any,
    lesson: dict[str, Any],
    *,
    action_label: str,
) -> bool:
    """Return True when duplicate Lessons were resolved before correction.

    A single saved Lesson is the target only when no pending candidate is loaded.
    If a pending candidate or another saved Lesson matches the same error
    family, this helper deletes draft/not-active-ready saved duplicates,
    consumes pending candidates, clears the windows, and tells the caller to
    stop.
    """
    if not isinstance(lesson, dict):
        return False
    project_root = _project_root_for_tab(tab)
    had_pending = bool(_loaded_pending_marker(tab))
    selected_id = str(getattr(tab, "_selected_lesson_id", "") or lesson.get("lesson_id", "")).strip()
    try:
        match = resolve_duplicate_lesson_copies(
            project_root,
            lesson,
            candidate_has_pending_source=had_pending,
            delete_candidate_lesson_id=selected_id,
        )
    except Exception:
        match = None

    if match is None:
        return False

    pending_deleted, pending_failures = delete_matching_pending_duplicate_candidates(tab, lesson)
    consumed = _consume_pending_candidate(tab, lesson) if had_pending else False

    reloader = getattr(tab, "_reload_table", None)
    if callable(reloader):
        try:
            reloader()
        except Exception:
            pass
    clear_error_memory_work_windows(tab)
    _show_duplicate_correction_message(
        tab,
        action_label=action_label,
        match=match,
        consumed=consumed,
        pending_deleted=pending_deleted,
        pending_failures=pending_failures,
    )
    return True
