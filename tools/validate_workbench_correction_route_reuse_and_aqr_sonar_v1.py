# project-path: tools/validate_workbench_correction_route_reuse_and_aqr_sonar_v1.py
"""Validate reusable correction alternatives, AQR terminal classification, and sonar wiring."""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

__all__ = [
    "main",
]

FEATURE_ID = "workbench-correction-route-reuse-and-aqr-sonar-v1"
ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def text(name: str) -> str:
    return (PLANNER / name).read_text(encoding="utf-8")


def main() -> int:
    gui = text("workbench_stage_correction_gui.py")
    context = text("workbench_stage_correction_context.py")
    heuristic = text("workbench_heuristic_correction_qt_controller.py")
    local_ai = text("workbench_local_ai_correction_qt_controller.py")
    route_switch = text("workbench_stage_correction_route_switch.py")
    aqr_gui = text("advanced_quality_review_gui.py")
    sonar = text("advanced_quality_review_sonar.py")

    require(
        'heuristic.setEnabled(bool(needed and not heuristic_running))' in gui
        and 'local_button.setEnabled(bool(needed and not local_running))' in gui
        and 'button.setEnabled(bool(needed))' in gui,
        "CORRECTION_ALTERNATIVES_REMAIN_REUSABLE_WHILE_STAGE_CORRECTABLE",
    )
    require(
        'stage not in timed_out_stages' not in gui
        and 'if state.waiting or state.background_job_alive' not in heuristic
        and 'if state.waiting or state.background_job_alive' not in local_ai,
        "CORRECTION_TIMEOUT_OR_STALE_BACKGROUND_JOB_DOES_NOT_CONSUME_ROUTE",
    )
    require(
        'abandon_local_ai_before_heuristic(' in gui
        and 'abandon_heuristic_before_local_ai(' in gui
        and 'abandon_workers_before_web_receive(' in gui
        and 'cancel_local_ai_correction(' in route_switch
        and 'cancel_heuristic_correction(' in route_switch,
        "CORRECTION_ROUTE_SWITCH_ABANDONS_PRIOR_WORKER_FAIL_CLOSED",
    )
    require(
        'if stage == "ADVANCED_QUALITY_REVIEW" and result is None:' in context
        and '_large_file_refactor_workbench_aqr_terminal_status' in context,
        "AQR_TECHNICAL_FAILURE_CLASSIFIED_FROM_TERMINAL_EVIDENCE",
    )

    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        workbench_stage_correction_context as context_mod,
    )

    class Output:
        def __init__(self, value: str) -> None:
            self._value = value
        def toPlainText(self) -> str:
            return self._value

    failed = SimpleNamespace(
        _large_file_refactor_workbench_advanced_quality_review=None,
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="ruff process failed",
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_output=Output("AQR failed"),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
    )
    require(
        context_mod.stage_correction_needed(failed, "ADVANCED_QUALITY_REVIEW", "E:/project"),
        "AQR_RESULT_NONE_WITH_FAILED_TERMINAL_STATUS_OPENS_CORRECTION",
    )
    not_run = SimpleNamespace(
        _large_file_refactor_workbench_advanced_quality_review=None,
        _large_file_refactor_workbench_aqr_terminal_status="",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="",
        _large_file_refactor_workbench_aqr_stage_states={},
        _large_file_refactor_workbench_aqr_output=Output("AQR not run"),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
    )
    require(
        not context_mod.stage_correction_needed(not_run, "ADVANCED_QUALITY_REVIEW", "E:/project"),
        "AQR_NOT_REACHED_REMAINS_NON_CORRECTABLE",
    )

    require(
        'start_aqr_sonar(window)' in aqr_gui
        and 'update_aqr_sonar(window, stage, message)' in aqr_gui
        and 'finish_aqr_sonar_success' in aqr_gui
        and 'finish_aqr_sonar_blocked' in aqr_gui,
        "AQR_SONAR_BOUND_TO_REAL_CONTROLLER_LIFECYCLE",
    )
    require(
        'GreenSonarActivityMonitor' in sonar
        and 'Preflight remains closed' in sonar
        and 'Correction routes remain available' in sonar,
        "AQR_SONAR_PRESENTATION_ONLY_FAIL_CLOSED_FEEDBACK",
    )

    for path in [
        PLANNER / "workbench_stage_correction_context.py",
        PLANNER / "workbench_stage_correction_gui.py",
        PLANNER / "advanced_quality_review_gui.py",
        PLANNER / "advanced_quality_review_sonar.py",
        PLANNER / "workbench_stage_correction_route_switch.py",
    ]:
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        require("\ufeff" not in source, "SOURCE_ASCII_UTF8_NO_BOM_" + path.stem.upper())
        line_count = len(source.splitlines())
        require(101 <= line_count <= 499, "MODULE_SIZE_POLICY_101_499_" + path.stem.upper())

    print("WORKBENCH_CORRECTION_ROUTE_REUSE_AND_AQR_SONAR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
