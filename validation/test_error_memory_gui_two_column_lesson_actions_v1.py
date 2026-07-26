"""Validation for Error Memory two-column GUI and lesson actions v1."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from kanda_reasoner_app.error_memory.models import build_lesson
from kanda_reasoner_app.error_memory.paths import resolve_error_memory_index_path
from kanda_reasoner_app.error_memory.store import delete_lesson, list_lessons, save_lesson


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_store_delete_undo_round_trip() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "Project With Spaces"
        project_root.mkdir()
        lesson = build_lesson(
            selected_project_root=project_root,
            raw_error_text="KeyError: 'ml_pilot_activation_state'",
            operation_phase="validation",
            symptom="Validation failed with KeyError for missing ml_pilot_activation_state.",
            root_cause="GUI producer did not return the validation-visible key.",
            wrong_assumption="Only validation/test logic needed the new key.",
            correct_fix="Update the GUI state producer and rerun validation.",
            long_term_prevention="Update producer, consumer, and regression test together.",
            do_not_repeat_rule="Do not add validation-visible GUI keys only to tests.",
            prevention_triggers=["KeyError", "ml_pilot_activation_state"],
            validation_evidence=["VALIDATION OK: synthetic"],
            status="active",
        )
        saved_path = save_lesson(project_root, lesson)
        _assert(saved_path.exists(), "save_lesson did not write the lesson file")
        lessons = list_lessons(project_root, include_inactive=True)
        _assert(len(lessons) == 1, "lesson was not listed after save")
        deleted = delete_lesson(project_root, lesson["lesson_id"])
        _assert(deleted["lesson_id"] == lesson["lesson_id"], "delete_lesson did not return deleted payload")
        _assert(not saved_path.exists(), "delete_lesson did not remove the lesson file")
        after_delete = list_lessons(project_root, include_inactive=True)
        _assert(after_delete == [], "lesson still listed after delete")
        index_payload = json.loads(resolve_error_memory_index_path(project_root).read_text(encoding="utf-8-sig"))
        _assert(index_payload.get("lessons") == [], "index not rebuilt empty after delete")
        restored_path = save_lesson(project_root, deleted)
        _assert(restored_path.exists(), "undo save did not restore lesson")
        restored = list_lessons(project_root, include_inactive=True)
        _assert(len(restored) == 1 and restored[0]["lesson_id"] == lesson["lesson_id"], "restored lesson not listed")


def test_gui_source_has_two_columns_and_lesson_actions() -> None:
    source_path = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    text = source_path.read_text(encoding="utf-8-sig")
    required_fragments = [
        "QSplitter(Qt.Horizontal)",
        "AI-assisted error lesson intake",
        "Project context",
        "Last received lesson Preview",
        "Lessons",
        "QTableWidget.SelectRows",
        "Save",
        "Undo",
        "Delete",
        "_load_selected_lesson_into_preview",
        "_save_preview_lesson",
        "_delete_selected_lesson",
        "_undo_lesson_action",
        "delete_lesson",
    ]
    for fragment in required_fragments:
        _assert(fragment in text, "GUI source missing required fragment: " + fragment)


def main() -> None:
    test_store_delete_undo_round_trip()
    test_gui_source_has_two_columns_and_lesson_actions()
    print("VALIDATION OK: error-memory-gui-two-column-lesson-actions-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
