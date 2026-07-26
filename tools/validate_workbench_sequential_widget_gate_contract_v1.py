"""Validate that the real-widget regression follows the Workbench progression contract."""
from __future__ import annotations

import ast
from pathlib import Path

__all__ = [
    "main",
]

ROOT = Path(__file__).resolve().parents[1]
PLANNER_ROOT = (
    ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)
PROGRESSION = PLANNER_ROOT / "workbench_gui_progression.py"
WIDGET_VALIDATOR = (
    ROOT / "tools" / "validate_large_file_refactor_workbench_real_widget_attemptability_v1.py"
)
FEATURE_ID = "architecture-review-workbench-sequential-widget-gate-contract-v1"


def _require(text: str, needle: str, marker: str) -> None:
    if needle not in text:
        raise AssertionError(marker + ":MISSING:" + needle)
    print(marker + ": PASS")


def main() -> None:
    progression_text = PROGRESSION.read_text(encoding="utf-8", errors="strict")
    widget_text = WIDGET_VALIDATOR.read_text(encoding="utf-8", errors="strict")

    ast.parse(progression_text, filename=str(PROGRESSION))
    ast.parse(widget_text, filename=str(WIDGET_VALIDATOR))

    _require(
        progression_text,
        "dependency_analysis_enabled=plan_loaded",
        "INITIAL_SEQUENTIAL_GATES_MATCH_PROGRESSION_MODEL",
    )
    _require(
        widget_text,
        "_assert_initial_sequential_gates_closed(window)",
        "REAL_WIDGET_INITIAL_STATE_FAILS_CLOSED",
    )
    _require(
        widget_text,
        '"_large_file_refactor_workbench_dependency_button",',
        "PLAN_INTAKE_ENABLES_DEPENDENCY_ONLY",
    )
    _require(
        widget_text,
        "_assert_only_next_stage_enabled(",
        "REAL_WIDGET_VALIDATES_NEXT_STAGE_ONLY",
    )

    if "_assert_attemptable(window)" in widget_text:
        raise AssertionError("REAL_WIDGET_VALIDATOR_STILL_ASSUMES_ALL_BUTTONS_PREOPEN")
    print("REAL_WIDGET_VALIDATOR_NO_ALL_BUTTONS_PREOPEN_ASSUMPTION: PASS")

    if "ATTEMPTABLE_BUTTON_DISABLED:" in widget_text:
        raise AssertionError("LEGACY_ATTEMPTABLE_BUTTON_ASSERTION_STILL_PRESENT")
    print("LEGACY_ATTEMPTABLE_BUTTON_ASSERTION_REMOVED: PASS")

    touched = (PROGRESSION, WIDGET_VALIDATOR)
    for path in touched:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            raise AssertionError(f"MODULE_TOO_LARGE:{path.relative_to(ROOT)}:{line_count}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("WORKBENCH_SEQUENTIAL_WIDGET_GATE_CONTRACT: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
