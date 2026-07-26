"""Validation for Error Memory GUI lesson status workflow v1."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kanda_reasoner_app.error_memory.models import active_ready, build_lesson
from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_active_ready_gate() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_gui_status_") as tmp:
        project_root = Path(tmp) / "status_workflow_project"
        project_root.mkdir(parents=True, exist_ok=True)
        draft = build_lesson(
            selected_project_root=project_root,
            raw_error_text="KeyError: 'ml_pilot_activation_state'",
            operation_phase="validation",
            symptom="Validation failed with KeyError for missing ml_pilot_activation_state.",
            root_cause="GUI producer did not return the validation-visible key.",
            wrong_assumption="Only validation/test logic needed the new key.",
            correct_fix="Update the GUI state producer and rerun validation.",
            long_term_prevention="Update producer, consumer, and regression together.",
            do_not_repeat_rule="Do not add validation-visible GUI keys only to tests.",
            prevention_triggers=["KeyError", "ml_pilot_activation_state"],
            validation_evidence=["Validation failed before correction."],
            status="draft",
        )
        _assert(active_ready(draft), "complete draft shape should be active-ready apart from validation evidence gate")
        draft["status"] = "deprecated"
        save_lesson(project_root, draft)
        saved = list_lessons(project_root, include_inactive=True)[0]
        _assert(saved["status"] == "deprecated", "status save/reload did not preserve deprecated status")
        saved["status"] = "superseded"
        saved["superseded_by"] = "lesson-aaaaaaaaaaaa"
        save_lesson(project_root, saved)
        saved_again = list_lessons(project_root, include_inactive=True)[0]
        _assert(saved_again["status"] == "superseded", "status save/reload did not preserve superseded status")
        _assert(saved_again["superseded_by"] == "lesson-aaaaaaaaaaaa", "superseded_by not saved")


def test_gui_source_has_status_workflow_controls() -> None:
    source_path = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
    text = source_path.read_text(encoding="utf-8-sig")
    required_fragments = [
        "Mark Draft",
        "Mark Active",
        "Deprecate",
        "Supersede",
        "_set_selected_lesson_status",
        "_supersede_selected_lesson",
        "_validation_evidence_is_passing",
        "VALIDATION OK",
        "STATUS: IN_SYNC",
        "active_ready",
        "utc_now_iso",
        "QInputDialog",
        "superseded_by",
    ]
    for fragment in required_fragments:
        _assert(fragment in text, "GUI source missing required fragment: " + fragment)


def main() -> None:
    test_active_ready_gate()
    test_gui_source_has_status_workflow_controls()
    print("VALIDATION OK: error-memory-gui-status-workflow-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
