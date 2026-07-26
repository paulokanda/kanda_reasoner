"""Validate Workbench Local AI correction UI settlement and progression projection repair."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
FEATURE_ID = "workbench-local-ai-correction-ui-settlement-projection-repair-v1"


def _read(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


def main() -> None:
    controller = _read("workbench_local_ai_correction_qt_controller.py")
    gui = _read("workbench_stage_correction_gui.py")
    progression = _read("workbench_gui_progression.py")
    workbench_gui = _read("workbench_gui.py")
    tutorial = _read("LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md")

    for marker in (
        'job["ui_result_settled"] = True',
        "_request_thread_quit(job)",
        "thread.quit()",
        "_sync_after_result(window, generation, sync_callback)",
        "QTimer.singleShot(",
    ):
        assert marker in controller, marker
    print("LOCAL_AI_RESULT_SETTLEMENT_EXPLICIT_THREAD_QUIT: PASS")
    print("LOCAL_AI_RESULT_SETTLEMENT_NEXT_EVENT_TURN_SYNC: PASS")

    for marker in (
        "_schedule_global_workbench_projection(window)",
        '"_large_file_refactor_workbench_global_sync_callback"',
        "callback(window)",
        "QTimer.singleShot(0, lambda: callback(window))",
    ):
        assert marker in gui, marker
    assert "setEnabled(True)" not in gui
    assert "setEnabled(True)" not in controller
    print("LOCAL_AI_ACCEPTED_INTAKE_REPROJECTS_GLOBAL_WORKBENCH_CONTROLS: PASS")
    print("LOCAL_AI_SETTLEMENT_DOES_NOT_FORCE_ENABLE_GATES: PASS")

    assert "dependency_analysis_enabled=plan_loaded" in progression
    assert '"_large_file_refactor_workbench_dependency_button", progression.dependency_analysis_enabled' in workbench_gui
    assert "sync_advanced_quality_review_controls(window, progression)" in workbench_gui
    assert "sync_workbench_stage_correction_controls(window, _root_text)" in workbench_gui
    print("LOCAL_AI_POST_RELOAD_NEXT_ACTION_DERIVED_FROM_PROGRESSION_MODEL: PASS")

    assert "Analyze Dependency Readiness becomes the next available action" in tutorial
    assert "Correction buttons do not remain as workflow authority" in tutorial
    print("LOCAL_AI_SETTLEMENT_TUTORIAL_SYNC: PASS")

    touched = (
        "workbench_local_ai_correction_qt_controller.py",
        "workbench_stage_correction_gui.py",
    )
    for name in touched:
        path = PKG / name
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=str(path))
        line_count = len(text.splitlines())
        assert 1 <= line_count <= 500, (name, line_count)
        text.encode("ascii")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    print("WORKBENCH_LOCAL_AI_CORRECTION_UI_SETTLEMENT_PROJECTION_REPAIR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
