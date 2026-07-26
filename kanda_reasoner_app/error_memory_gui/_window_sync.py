# project-path: kanda_reasoner_app/error_memory_gui/_window_sync.py
"""Shared Error Memory intake/editor synchronization helpers."""
from __future__ import annotations

import json
from typing import Any

__all__ = [
    "apply_corrected_lesson_to_work_windows",
    "clear_error_memory_work_windows",
]


def apply_corrected_lesson_to_work_windows(tab: Any, lesson_block: Any) -> None:
    """Populate intake and editor from one AI-corrected lesson block.

    This is a preview/synchronization action only. It never consumes the
    pending intake file; save/status actions remain the commit point.
    """
    lesson = dict(getattr(lesson_block, "lesson", {}) or {})
    formatted_text = str(getattr(lesson_block, "formatted_text", "") or "").strip()
    if not formatted_text:
        formatted_text = json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)

    raw_edit = getattr(tab, "raw_error_edit", None)
    if raw_edit is not None:
        raw_edit.setPlainText(formatted_text)

    preview_edit = getattr(tab, "received_preview_edit", None)
    if preview_edit is not None:
        preview_edit.setPlainText(json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False))

    tab._last_received_lesson = lesson
    tab._selected_lesson_id = str(lesson.get("lesson_id", ""))

    refresher = getattr(tab, "_refresh_heuristic_correction_button_state", None)
    if callable(refresher):
        refresher()


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
