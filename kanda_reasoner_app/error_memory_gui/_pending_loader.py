# project-path: kanda_reasoner_app/error_memory_gui/_pending_loader.py
"""Pending-intake loading helpers for the Error Memory tab.

This private helper owns pending intake auto-load, duplicate-warning, and
pending-row-to-editor loading behavior for the public ErrorMemoryTab facade.
Qt imports stay local so helper import smoke remains headless-safe, and this
module never imports the origin facade upward.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.store import list_lessons
from kanda_reasoner_app.error_memory_gui._draft_intake_lifecycle import (
    formatted_draft_lesson_block,
    normalize_incoming_lesson_to_draft,
    persist_incoming_draft_in_lesson_library,
)
from kanda_reasoner_app.error_memory_gui._owner_lane import (
    backend_for_current_work_item,
)
from kanda_reasoner_app.error_memory.tool_intake import is_tool_pending_intake_path

__all__ = [
    "delete_pending_file_quietly",
    "lesson_id_exists_in_lessons",
    "load_pending_ai_assisted_error_lesson_intake",
    "load_pending_ai_assisted_error_lesson_intake_now",
    "load_pending_intake_row_into_editor",
    "show_duplicate_pending_intake_warning",
]


def load_pending_ai_assisted_error_lesson_intake_now(tab: Any, project_root: str | Path | None = None) -> bool:
    """Public host hook: load one staged pending lesson into both text windows."""
    if project_root is not None:
        try:
            root = tab._existing_directory_from_text(str(project_root))
            if root is not None:
                tab._project_root = root
                root_text = str(tab._project_root)
                if tab.project_root_value_label.text().strip() != root_text:
                    tab._syncing_project_root_field = True
                    try:
                        tab.project_root_value_label.setText(root_text)
                    finally:
                        tab._syncing_project_root_field = False
        except Exception:
            pass
    return tab._load_pending_ai_assisted_error_lesson_intake()


def load_pending_ai_assisted_error_lesson_intake(tab: Any, *, mirror_loaded_json_to_error_editor: bool = False) -> bool:
    """Auto-load the newest pending_review lesson for human review.

    The mirror_loaded_json_to_error_editor argument is preserved for facade
    compatibility with the previous method signature.
    """
    del mirror_loaded_json_to_error_editor
    for row in tab._pending_lesson_rows_for_table():
        if row.get('kind') not in {'pending_review', 'pending_tool_review'}:
            continue
        candidate = Path(str(row.get('pending_path', ''))).expanduser().resolve(strict=False)
        marker = str(candidate)
        if marker == tab._loaded_pending_intake_file or marker in tab._dismissed_pending_intake_files:
            continue
        if str(row.get('lesson_id', '')).strip() in tab._dismissed_pending_intake_lesson_ids:
            continue
        if tab._load_pending_intake_row_into_editor(candidate, str(row.get('kind', 'pending_review')), show_duplicate_warning=False):
            return True
    return False


def show_duplicate_pending_intake_warning(tab: Any, lesson_id: str, pending_file: Path) -> None:
    """Compatibility hook kept quiet after Memorize Error duplicate guard.

    Duplicate pending candidates are now handled by the Memorize Error
    duplicate guard. Selecting a pending row should not interrupt review with a
    modal warning; the user can load the candidate and press Memorize Error,
    which will consume the duplicate candidate without saving a second Lesson.
    """
    del tab, lesson_id, pending_file


def lesson_id_exists_in_lessons(tab: Any, lesson_id: str) -> bool:
    """Return whether a lesson_id already exists in canonical Lessons storage."""
    target = str(lesson_id or '').strip()
    if not target:
        return False
    try:
        return any(
            str(item.get('lesson_id', '')).strip() == target
            for item in list_lessons(
                backend_for_current_work_item(tab),
                include_inactive=True,
            )
        )
    except Exception:
        return False


def load_pending_intake_row_into_editor(tab: Any, pending_file: Path, row_kind: str, *, show_duplicate_warning: bool = True) -> bool:
    """Load one pending Lessons-table row into the intake and editor windows."""
    from PySide6.QtWidgets import QMessageBox

    del row_kind
    del show_duplicate_warning
    candidate = Path(pending_file).expanduser().resolve(strict=False)
    if not candidate.exists() or not candidate.is_file():
        QMessageBox.warning(tab, 'Pending Error Memory item missing', 'The pending intake file no longer exists:\n' + str(candidate))
        tab._reload_table()
        return False
    try:
        text = candidate.read_text(encoding='utf-8-sig', errors='replace').strip()
    except Exception as exc:
        QMessageBox.warning(tab, 'Pending Error Memory item failed to load', str(exc))
        return False
    if not text:
        QMessageBox.warning(tab, 'Pending Error Memory item is empty', str(candidate))
        return False
    marker = str(candidate)
    lesson: dict[str, Any]
    lesson_id = ''
    if tab._text_is_formatted_error_lesson_payload(text):
        try:
            lesson = tab._lesson_from_formatted_text(text)
        except Exception:
            lesson = tab._draft_lesson_from_pending_raw_text(candidate, text)
        lesson = normalize_incoming_lesson_to_draft(lesson)
    else:
        lesson = normalize_incoming_lesson_to_draft(
            tab._draft_lesson_from_pending_raw_text(candidate, text)
        )
    lesson_id = str(lesson.get("lesson_id", "")).strip()

    tab._loaded_pending_intake_file = marker
    tab._loaded_pending_intake_lesson_id = lesson_id
    try:
        persisted, _path = persist_incoming_draft_in_lesson_library(
            tab,
            lesson,
            pending_path=candidate if is_tool_pending_intake_path(candidate) else None,
        )
    except Exception as exc:
        tab._loaded_pending_intake_file = ''
        tab._loaded_pending_intake_lesson_id = ''
        QMessageBox.warning(
            tab,
            'Pending Error Memory draft admission failed',
            (
                'The candidate was not admitted into Lessons, so the work windows '
                'were left unchanged. The pending source was preserved.\n\n'
                + str(exc)
            ),
        )
        return False

    tab._loaded_pending_intake_file = ''
    tab._loaded_pending_intake_lesson_id = ''
    tab._selected_lesson_id = str(persisted.get('lesson_id') or lesson_id)
    tab._last_received_lesson = dict(persisted)
    memorize = getattr(tab, "memorize_error_button", None)
    if memorize is not None:
        memorize.setEnabled(True)
    return True


def delete_pending_file_quietly(path: Path) -> bool:
    """Delete one pending intake source without raising into the loader."""
    try:
        candidate = Path(path).expanduser().resolve(strict=False)
        if candidate.exists() and candidate.is_file():
            candidate.unlink()
            return True
    except Exception:
        return False
    return False
