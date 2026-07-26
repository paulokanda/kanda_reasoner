# project-path: kanda_reasoner_app/error_memory_gui/_draft_deletion.py
"""Non-GUI helpers for Error Memory draft deletion identity and store cleanup."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

from kanda_reasoner_app.error_memory.models import active_ready
from kanda_reasoner_app.error_memory.store import delete_lesson, list_lessons, rebuild_index

__all__ = [
    "delete_matching_canonical_draft_lessons",
    "draft_delete_identity_from_sources",
]


def _append_unique_text(values: list[str], value: str) -> str:
    """Append a stripped text value once and return the stripped value."""
    text_value = str(value or "").strip()
    if text_value and text_value not in values:
        values.append(text_value)
    return text_value


def _append_unique_path(values: list[str], value: str) -> str:
    """Append a stripped explicit path/marker once and return the stripped value."""
    marker = str(value or "").strip()
    if marker and marker not in values:
        values.append(marker)
    return marker


def draft_delete_identity_from_sources(
    *,
    raw_error_text: str,
    received_preview_text: str,
    last_dismissed_pending_intake_text: str,
    loaded_pending_intake_lesson_id: str,
    last_dismissed_pending_intake_lesson_id: str,
    selected_lesson_id: str,
    current_lesson: dict[str, Any] | None,
    loaded_pending_intake_file: str,
    last_dismissed_pending_intake_file: str,
    lesson_id_from_text: Callable[[str], str],
) -> tuple[set[str], list[str], list[str]]:
    """Collect identifiers that describe the current or dismissed draft.

    This helper is intentionally UI-free. The GUI facade supplies visible text,
    selected lesson metadata, and loaded/dismissed pending markers. The helper
    only deduplicates identity evidence and extracts loose lesson IDs from text.
    """
    lesson_ids: set[str] = set()
    visible_texts: list[str] = []
    explicit_paths: list[str] = []

    for value in (raw_error_text, received_preview_text, last_dismissed_pending_intake_text):
        text_value = _append_unique_text(visible_texts, value)
        if text_value:
            extracted_id = str(lesson_id_from_text(text_value) or "").strip()
            if extracted_id:
                lesson_ids.add(extracted_id)

    for value in (
        loaded_pending_intake_lesson_id,
        last_dismissed_pending_intake_lesson_id,
        selected_lesson_id,
    ):
        lesson_id = str(value or "").strip()
        if lesson_id:
            lesson_ids.add(lesson_id)

    if isinstance(current_lesson, dict):
        lesson_id = str(current_lesson.get("lesson_id", "")).strip()
        if lesson_id:
            lesson_ids.add(lesson_id)

    for value in (loaded_pending_intake_file, last_dismissed_pending_intake_file):
        _append_unique_path(explicit_paths, value)

    return (lesson_ids, visible_texts, explicit_paths)


def delete_matching_canonical_draft_lessons(
    project_root: str | Path,
    lesson_ids: Iterable[str],
) -> tuple[int, list[str], list[str]]:
    """Delete saved draft or invalid-active lesson records matching lesson IDs.

    Active-ready saved lessons are intentionally preserved. This mirrors the GUI
    delete-draft safety rule while keeping store cleanup out of the GUI class.
    """
    root = Path(project_root)
    deleted_count = 0
    skipped: list[str] = []
    failures: list[str] = []
    for lesson_id in sorted({str(item or "").strip() for item in lesson_ids if str(item or "").strip()}):
        try:
            lessons = list_lessons(root, include_inactive=True)
            stored = next((item for item in lessons if item.get("lesson_id") == lesson_id), None)
            if not isinstance(stored, dict):
                continue
            stored_status = str(stored.get("status", "")).strip().lower()
            can_delete = stored_status == "draft" or not active_ready(dict(stored))
            if can_delete:
                delete_lesson(root, lesson_id)
                deleted_count += 1
            else:
                skipped.append(lesson_id + " (active-ready saved lesson preserved)")
        except Exception as exc:
            failures.append(lesson_id + " -> " + str(exc))
    try:
        rebuild_index(root)
    except Exception as exc:
        failures.append("index rebuild -> " + str(exc))
    return (deleted_count, skipped, failures)
