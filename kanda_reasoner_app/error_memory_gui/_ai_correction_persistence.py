# project-path: kanda_reasoner_app/error_memory_gui/_ai_correction_persistence.py
"""Persistence helpers for AI-corrected Error Memory draft lessons."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.error_memory.models import active_ready, utc_now_iso
from kanda_reasoner_app.error_memory.store import delete_lesson, list_lessons, save_lesson

__all__ = [
    "DraftCorrectionSaveResult",
    "save_corrected_selected_draft",
    "selected_saved_draft_lesson_id",
]


@dataclass(frozen=True)
class DraftCorrectionSaveResult:
    """Result of saving an AI-corrected selected draft back to Lessons."""

    saved: bool
    detail: str = ""
    error: str = ""


def _current_project_root(tab: Any) -> Any:
    """Return the selected project root from the Error Memory tab."""
    getter = getattr(tab, "_current_project_root", None)
    if callable(getter):
        return getter()
    return getattr(tab, "_project_root", "")


def _table_selected_lesson_id(tab: Any) -> str:
    """Return the selected saved lesson id without trusting editor text."""
    selector = getattr(tab, "_selected_lesson_id_from_table", None)
    if callable(selector):
        try:
            selected = str(selector() or "").strip()
        except Exception:
            selected = ""
        if selected:
            return selected
    return str(getattr(tab, "_selected_lesson_id", "") or "").strip()


def selected_saved_draft_lesson_id(tab: Any) -> str:
    """Return the selected saved draft id before AI output mutates GUI state.

    Pending intake rows are not saved implicitly.  This helper must be called
    before the corrected AI lesson is copied into the work windows, because the
    preview sync helper intentionally updates ``tab._selected_lesson_id`` to the
    AI output lesson id.
    """
    if str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip():
        return ""
    lesson_id = _table_selected_lesson_id(tab)
    if not lesson_id:
        return ""
    try:
        lessons = list_lessons(_current_project_root(tab), include_inactive=True)
    except Exception:
        return ""
    for lesson in lessons:
        if str(lesson.get("lesson_id", "")).strip() != lesson_id:
            continue
        if str(lesson.get("status", "")).strip().lower() == "draft":
            return lesson_id
        return ""
    return ""


def _selected_saved_draft(
    tab: Any,
    *,
    selected_lesson_id: str = "",
) -> dict[str, Any] | None:
    """Return the selected saved draft lesson when correction may update it."""
    if str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip():
        return None
    lesson_id = str(selected_lesson_id or "").strip()
    if not lesson_id:
        lesson_id = selected_saved_draft_lesson_id(tab)
    if not lesson_id:
        return None
    lessons = list_lessons(_current_project_root(tab), include_inactive=True)
    for lesson in lessons:
        if str(lesson.get("lesson_id", "")).strip() != lesson_id:
            continue
        if str(lesson.get("status", "")).strip().lower() != "draft":
            return None
        return dict(lesson)
    return None




def _lesson_ids(project_root: Any) -> set[str]:
    """Return saved lesson ids for duplicate-cleanup checks."""
    ids: set[str] = set()
    for lesson in list_lessons(project_root, include_inactive=True):
        lesson_id = str(lesson.get("lesson_id", "") or "").strip()
        if lesson_id:
            ids.add(lesson_id)
    return ids


def _remove_new_ai_output_lesson(
    project_root: Any,
    *,
    before_ids: set[str],
    target_lesson_id: str,
    ai_output_lesson_id: str,
) -> str:
    """Remove an AI-generated duplicate row created during draft correction.

    The selected draft id is the only persistence target for Correct with AI.
    If a stale or redirected save path creates a second row using the AI output
    id during this operation, remove only that newly created row. Existing
    saved rows are protected by the before_ids snapshot.
    """
    ai_id = str(ai_output_lesson_id or "").strip()
    target_id = str(target_lesson_id or "").strip()
    if not ai_id or not target_id or ai_id == target_id:
        return ""
    if ai_id in before_ids:
        return ""
    try:
        after_ids = _lesson_ids(project_root)
    except Exception as exc:
        return "Could not inspect Lessons after correction save: " + str(exc)
    if ai_id not in after_ids:
        return ""
    try:
        delete_lesson(project_root, ai_id)
    except Exception as exc:
        return "Could not remove unexpected AI-generated lesson_id " + ai_id + ": " + str(exc)
    return ""


def _find_lesson(project_root: Any, lesson_id: str) -> dict[str, Any] | None:
    """Return one saved lesson by id."""
    wanted = str(lesson_id or "").strip()
    if not wanted:
        return None
    for lesson in list_lessons(project_root, include_inactive=True):
        if str(lesson.get("lesson_id", "") or "").strip() == wanted:
            return dict(lesson)
    return None

def _sync_editor_windows(tab: Any, lesson: dict[str, Any]) -> None:
    """Show the saved corrected draft in both Error Memory work windows."""
    json_text = json.dumps(lesson, indent=2, sort_keys=True, ensure_ascii=False)
    raw_edit = getattr(tab, "raw_error_edit", None)
    preview_edit = getattr(tab, "received_preview_edit", None)
    formatter = getattr(tab, "_formatted_lesson_block", None)
    if raw_edit is not None:
        if callable(formatter):
            raw_edit.setPlainText(str(formatter(lesson)))
        else:
            raw_edit.setPlainText(json_text)
    if preview_edit is not None:
        preview_edit.setPlainText(json_text)


def save_corrected_selected_draft(
    tab: Any,
    corrected_lesson: dict[str, Any],
    *,
    selected_lesson_id: str = "",
) -> DraftCorrectionSaveResult:
    """Save an AI correction over the selected saved draft, when safe.

    Correct with AI remains a review workflow for pending rows and non-draft
    Lessons.  For an existing selected draft row, however, the user explicitly
    asked the correction result to update the Lessons list.  The selected draft
    id is captured before preview synchronization so an AI-generated lesson_id
    cannot redirect persistence to a new or unrelated row.
    """
    selected_draft = _selected_saved_draft(tab, selected_lesson_id=selected_lesson_id)
    if selected_draft is None:
        return DraftCorrectionSaveResult(saved=False)
    project_root = _current_project_root(tab)
    before_ids = _lesson_ids(project_root)
    lesson = dict(corrected_lesson or {})
    ai_output_lesson_id = str(lesson.get("lesson_id", "") or "").strip()
    lesson_id = str(selected_draft.get("lesson_id", "")).strip()
    if not lesson_id:
        return DraftCorrectionSaveResult(saved=False)
    lesson["lesson_id"] = lesson_id
    lesson["status"] = "draft"
    lesson.setdefault("created_at_utc", selected_draft.get("created_at_utc") or utc_now_iso())
    lesson["updated_at_utc"] = utc_now_iso()
    if active_ready(dict(lesson)):
        lesson["promotion_status"] = "active_ready"
        readiness = "The corrected draft is active-ready after review."
    else:
        lesson["promotion_status"] = "needs_ai_review"
        readiness = "The corrected draft still needs review before Mark Active."
    try:
        path = save_lesson(project_root, lesson)
    except Exception as exc:
        return DraftCorrectionSaveResult(saved=False, error=str(exc))
    cleanup_error = _remove_new_ai_output_lesson(
        project_root,
        before_ids=before_ids,
        target_lesson_id=lesson_id,
        ai_output_lesson_id=ai_output_lesson_id,
    )
    if cleanup_error:
        return DraftCorrectionSaveResult(saved=False, error=cleanup_error)
    saved_lesson = _find_lesson(project_root, lesson_id)
    if saved_lesson is None:
        return DraftCorrectionSaveResult(
            saved=False,
            error="Corrected draft was not found after save: " + lesson_id,
        )
    lesson = saved_lesson
    tab._selected_lesson_id = lesson_id
    tab._last_received_lesson = lesson
    _sync_editor_windows(tab, lesson)
    reloader = getattr(tab, "_reload_table", None)
    if callable(reloader):
        reloader()
    return DraftCorrectionSaveResult(
        saved=True,
        detail=(
            "Saved corrected draft back into Lessons and refreshed the list. "
            + readiness
            + " Status remains draft until Mark Active is explicitly confirmed. Path: "
            + str(path)
        ),
    )
