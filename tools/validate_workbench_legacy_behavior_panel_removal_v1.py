# project-path: tools/validate_workbench_legacy_behavior_panel_removal_v1.py
"""Validate removal of obsolete legacy behavior controls from the Workbench tab."""
from __future__ import annotations

from pathlib import Path

FEATURE_ID = "large-file-refactor-workbench-legacy-behavior-panel-removal-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)


def main() -> None:
    """Run focused source-contract checks for the Workbench GUI cleanup."""
    workbench_gui = _read("workbench_gui.py")
    completion_gui = _read("workbench_completion_gui.py")
    aqr_gui = _read("advanced_quality_review_gui.py")
    exchange_gui = _read("external_ai_candidate_exchange_gui.py")
    diff_gui = _read("workbench_diff_review_assistant_gui.py")
    tutorial = _read("LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md")
    behavior_bridge = _read("workbench_behavior_gui_bridge.py")
    completion_bridge = _read("workbench_completion_apply_bridge.py")

    _validate_legacy_panel_not_wired(workbench_gui)
    _validate_current_workflow_controls_preserved(
        workbench_gui,
        completion_gui,
        aqr_gui,
        exchange_gui,
        diff_gui,
    )
    _validate_behavior_engine_remains_internal(behavior_bridge, completion_bridge)
    _validate_tutorial_current(tutorial)
    _validate_module_sizes()

    print("LEGACY_BEHAVIOR_PANEL_GUI_WIRING_REMOVED: PASS")
    print("LEGACY_BEHAVIOR_COMMAND_FIELD_REMOVED_FROM_TAB: PASS")
    print("LEGACY_BEHAVIOR_RUN_BUTTON_REMOVED_FROM_TAB: PASS")
    print("CURRENT_SEQUENTIAL_WORKBENCH_CONTROLS_PRESERVED: PASS")
    print("CURRENT_AQR_ASSISTED_REVIEW_AND_AI_EXCHANGE_CONTROLS_PRESERVED: PASS")
    print("BEHAVIOR_VALIDATION_ENGINE_REMAINS_JOURNALED_INTERNAL_SUPPORT: PASS")
    print("WORKBENCH_TUTORIAL_MATCHES_VISIBLE_GUI: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("WORKBENCH_LEGACY_BEHAVIOR_PANEL_REMOVAL: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _read(name: str) -> str:
    """Read one Workbench package file as UTF-8 text."""
    return (PACKAGE / name).read_text(encoding="utf-8")


def _validate_legacy_panel_not_wired(workbench_gui: str) -> None:
    """Reject every obsolete behavior-panel wiring point from the visible tab shell."""
    forbidden = (
        "build_behavior_validation_section",
        "sync_behavior_validation_buttons",
        "_large_file_refactor_workbench_behavior_command_edit",
        "_large_file_refactor_workbench_behavior_button",
        "_large_file_refactor_workbench_behavior_gate_label",
        "_large_file_refactor_workbench_behavior_output",
        "Legacy Compatibility",
        "Run Optional Behavior Validation",
    )
    for marker in forbidden:
        assert marker not in workbench_gui, marker


def _validate_current_workflow_controls_preserved(
    workbench_gui: str,
    completion_gui: str,
    aqr_gui: str,
    exchange_gui: str,
    diff_gui: str,
) -> None:
    """Prove the cleanup did not remove current governed controls."""
    required_workbench = (
        'QPushButton("Load Latest Planner Plan")',
        'QPushButton("Recheck Source Hash")',
        'QPushButton("Analyze Dependency Readiness")',
        'QPushButton("Generate Real Preview")',
        'QPushButton("Validate Real Preview")',
        'QPushButton("Prepare Preflight Backup Readiness")',
        'QPushButton("Build Source Apply Payload")',
    )
    for marker in required_workbench:
        assert marker in workbench_gui, marker

    required_completion = (
        'QPushButton("Prepare Completion Evidence")',
        'QPushButton("Prepare Transaction Summary")',
        'QPushButton("Refactor Large Module")',
        'QPushButton("Rollback Journaled Transaction")',
        'QCheckBox("I reviewed the semantic diff")',
        'QCheckBox("I acknowledge all listed warnings")',
        'QCheckBox("I confirm this exact transaction summary")',
    )
    for marker in required_completion:
        assert marker in completion_gui, marker

    for marker in (
        'QPushButton("Run Advanced Quality Review")',
        'QPushButton("Cancel")',
    ):
        assert marker in aqr_gui, marker

    for marker in (
        'QPushButton("Copy Candidates to AI")',
        'QPushButton("Import AI Answer")',
        'QPushButton("Refactoring Folder")',
        'QPushButton("Refactoring Folder Path")',
        'QPushButton("Clean Refactoring Folder")',
    ):
        assert marker in exchange_gui, marker

    for marker in (
        'QPushButton("Heuristic")',
        'QPushButton("Local AI")',
        'QPushButton("Web AI")',
        'QPushButton("Receive From Web AI")',
    ):
        assert marker in diff_gui, marker


def _validate_behavior_engine_remains_internal(
    behavior_bridge: str,
    completion_bridge: str,
) -> None:
    """Keep behavior execution support available to the governed journaled flow."""
    assert "run_workbench_behavior_validation" in behavior_bridge
    assert "run_workbench_behavior_validation" in completion_bridge
    assert "WorkbenchBehaviorValidationResult" in completion_bridge


def _validate_tutorial_current(tutorial: str) -> None:
    """Require documentation to describe the removed panel and current replacement route."""
    lowered = tutorial.lower()
    assert "deprecated legacy optional behavior-validation gui has been removed" in lowered
    assert "parallel legacy command field or button" in lowered
    assert "run optional behavior validation" not in lowered
    assert "legacy compatibility" not in lowered


def _validate_module_sizes() -> None:
    """Apply the current Workbench 101-499 physical-line policy to touched Python files."""
    paths = (
        PACKAGE / "workbench_gui.py",
        PROJECT_ROOT / "tools" / "validate_large_file_refactor_workbench_gui_progression_v1.py",
        Path(__file__).resolve(),
    )
    for path in paths:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert 100 < line_count < 500, f"SIZE_POLICY:{path}:{line_count}"


if __name__ == "__main__":
    main()
