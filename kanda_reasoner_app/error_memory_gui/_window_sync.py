# project-path: kanda_reasoner_app/error_memory_gui/_window_sync.py
"""Shared Error Memory intake/editor synchronization helpers."""
from __future__ import annotations

from typing import Any

from kanda_reasoner_app.error_memory_gui._draft_intake_lifecycle import (
    render_incoming_draft_in_work_windows,
)

__all__ = [
    "apply_corrected_lesson_to_work_windows",
    "clear_error_memory_work_windows",
]


def apply_corrected_lesson_to_work_windows(tab: Any, lesson_block: Any) -> None:
    """Load one AI-corrected result as a draft review candidate.

    This is a preview/synchronization action only. It never consumes the
    pending intake file and never promotes a lesson to active. Memorize Error
    remains the explicit human promotion/commit boundary.
    """
    lesson = dict(getattr(lesson_block, "lesson", {}) or {})
    render_incoming_draft_in_work_windows(tab, lesson)


def clear_error_memory_work_windows(tab: Any) -> None:
    """Clear both Error Memory work windows after a successful resolution.

    Successful save/status actions move the lesson into the Lessons store. After
    that point, the AI-assisted intake window and Error Editor must not keep a
    stale draft copy of the same Error Memory item.
    """
    raw_edit = getattr(tab, "raw_error_edit", None)
    if raw_edit is not None:
        raw_edit.clear()

    preview_edit = getattr(tab, "received_preview_edit", None)
    if preview_edit is not None:
        preview_edit.clear()

    table = getattr(tab, "lessons_table", None)
    if table is not None:
        try:
            table.blockSignals(True)
            table.clearSelection()
        finally:
            try:
                table.blockSignals(False)
            except Exception:
                pass

    tab._last_received_lesson = None
    tab._selected_lesson_id = ""
    tab._loaded_pending_intake_file = ""
    tab._loaded_pending_intake_lesson_id = ""

    refresher = getattr(tab, "_refresh_heuristic_correction_button_state", None)
    if callable(refresher):
        refresher()
