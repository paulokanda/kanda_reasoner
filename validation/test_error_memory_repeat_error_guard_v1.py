"""Validation for advisory Error Memory Repeat Error Guard v1."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kanda_reasoner_app.error_memory.guard import analyze_error_against_lessons
from kanda_reasoner_app.error_memory.models import build_lesson
from kanda_reasoner_app.error_memory.store import save_lesson


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _make_project(tmp: str) -> Path:
    project_root = Path(tmp) / "repeat_guard_project"
    project_root.mkdir(parents=True, exist_ok=True)
    return project_root


def test_exact_keyerror_repeat_is_detected() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_guard_") as tmp:
        project_root = _make_project(tmp)
        lesson = build_lesson(
            selected_project_root=project_root,
            raw_error_text="Validation failed with KeyError for missing ml_pilot_activation_state.\n\nKeyError: 'ml_pilot_activation_state'",
            operation_phase="validation",
            symptom="Validation failed with KeyError for missing ml_pilot_activation_state.",
            root_cause="GUI state producer did not return the validation-visible key.",
            wrong_assumption="Only validation needed the new key.",
            correct_fix="Update the GUI state producer and rerun validation.",
            long_term_prevention="Update producer, consumer, and validation together.",
            do_not_repeat_rule="Do not add validation-visible GUI keys only to tests.",
            prevention_triggers=["missing ml_pilot_activation_state", "KeyError for missing GUI state key"],
            validation_evidence=["Validation failed before correction."],
            status="draft",
        )
        save_lesson(project_root, lesson)
        report = analyze_error_against_lessons(
            project_root,
            "Validation failed again. KeyError: 'ml_pilot_activation_state'",
            operation_phase="validation",
        )
        _assert(report["hard_blocking"] is False, "guard must remain advisory-only")
        _assert(report["disposition"] == "EXACT_REPEAT_RISK", "exact repeat was not detected")
        _assert(report["recommendation"] == "PROCEED_WITH_CAUTION", "wrong recommendation for exact repeat")
        _assert(report["matches"], "expected at least one match")
        _assert(report["matches"][0]["lesson_id"] == lesson["lesson_id"], "matched wrong lesson")
        _assert(report["matches"][0]["match_confidence"] == "exact", "wrong confidence for exact repeat")


def test_no_match_remains_proceed() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_guard_nomatch_") as tmp:
        project_root = _make_project(tmp)
        lesson = build_lesson(
            selected_project_root=project_root,
            raw_error_text="ModuleNotFoundError: No module named 'kanda_reasoner_app.error_memory.intake'",
            operation_phase="validation",
            symptom="Validation failed because a new import dependency file was missing.",
            root_cause="Patch referenced a helper module that was not included.",
            wrong_assumption="Existing package already had the helper.",
            correct_fix="Include the missing module and validate imports.",
            long_term_prevention="When adding imports, include every new module in the patch.",
            do_not_repeat_rule="Do not reference a new module without shipping it in the patch ZIP.",
            prevention_triggers=["ModuleNotFoundError", "missing helper module"],
            validation_evidence=["Validation failed before correction."],
            status="draft",
        )
        save_lesson(project_root, lesson)
        report = analyze_error_against_lessons(
            project_root,
            "ValueError: invalid JSON lesson status",
            operation_phase="validation",
        )
        _assert(report["disposition"] in {"NO_MATCH", "WEAK_CONTEXT_MATCH"}, "unrelated error matched too strongly")
        _assert(report["hard_blocking"] is False, "guard must not hard block unrelated errors")


def test_gui_source_exposes_guard_button() -> None:
    source = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py").read_text(encoding="utf-8-sig")
    for fragment in [
        "Check Against Lessons",
        "analyze_error_against_lessons",
        "_check_against_lessons",
        "_show_repeat_guard_report",
        "Advisory-only",
    ]:
        _assert(fragment in source, "GUI source missing Repeat Error Guard fragment: " + fragment)


def main() -> None:
    test_exact_keyerror_repeat_is_detected()
    test_no_match_remains_proceed()
    test_gui_source_exposes_guard_button()
    print("VALIDATION OK: error-memory-repeat-error-guard-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
