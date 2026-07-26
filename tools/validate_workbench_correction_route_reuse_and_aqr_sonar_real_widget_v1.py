# project-path: tools/validate_workbench_correction_route_reuse_and_aqr_sonar_real_widget_v1.py
"""Validate real Qt correction-button projection and AQR sonar visibility."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QPA_FONTDIR", str(Path(os.environ.get("TEMP", "."))))

from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_stage_correction_gui as correction_gui,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_sonar import (
    finish_aqr_sonar_blocked,
    start_aqr_sonar,
    update_aqr_sonar,
)

FEATURE_ID = "workbench-correction-route-reuse-and-aqr-sonar-real-widget-v1"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    window.resize(1200, 800)
    window._large_file_refactor_workbench_aqr_output = QPlainTextEdit(window)
    window._large_file_refactor_workbench_advanced_quality_review = None
    window._large_file_refactor_workbench_aqr_terminal_status = "FAILED"
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = "technical failure"
    window._large_file_refactor_workbench_aqr_stage_states = {"RUFF": "FAILED"}
    window._large_file_refactor_workbench_intake = None
    window._large_file_refactor_workbench_dependency_readiness = None
    window._large_file_refactor_workbench_real_preview = None
    window._large_file_refactor_workbench_structural_validation = None
    window._large_file_refactor_workbench_preflight_backup = None
    window._large_file_refactor_workbench_source_payload = None
    window._large_file_refactor_workbench_completion_evidence = None

    row = correction_gui.build_workbench_stage_correction_row(
        window,
        "ADVANCED_QUALITY_REVIEW",
        lambda _window: "E:/project",
        lambda _window: None,
    )
    row.show()
    window.show()
    app.processEvents()
    require(window.isVisible(), "REAL_WIDGET_HOST_VISIBLE_BEFORE_SONAR_ASSERTION")
    correction_gui.sync_workbench_stage_correction_controls(
        window, lambda _window: "E:/project"
    )
    app.processEvents()
    bundle = window._large_file_refactor_workbench_correction_controls[
        "ADVANCED_QUALITY_REVIEW"
    ]
    require(bundle["heuristic"].isEnabled(), "CORRECTABLE_STAGE_HEURISTIC_ACTIVE")
    require(bundle["local_ai"].isEnabled(), "CORRECTABLE_STAGE_LOCAL_AI_ACTIVE")
    require(bundle["web_copy"].isEnabled(), "CORRECTABLE_STAGE_WEB_COPY_ACTIVE")
    require(bundle["web_receive"].isEnabled(), "CORRECTABLE_STAGE_WEB_RECEIVE_ACTIVE")

    original_heuristic = correction_gui.heuristic_execution_state
    original_local = correction_gui.local_ai_execution_state
    try:
        correction_gui.heuristic_execution_state = lambda _window: SimpleNamespace(
            waiting=True, active_stage="ADVANCED_QUALITY_REVIEW",
            progress_phase="ANALYZE_SOURCE", background_job_alive=True
        )
        correction_gui.local_ai_execution_state = lambda _window: SimpleNamespace(
            waiting=False, active_stage="", progress_phase="", background_job_alive=False
        )
        correction_gui.sync_workbench_stage_correction_controls(
            window, lambda _window: "E:/project"
        )
        require(not bundle["heuristic"].isEnabled(), "ACTIVE_HEURISTIC_START_TEMPORARILY_BUSY")
        require(bundle["local_ai"].isEnabled(), "LOCAL_AI_REMAINS_ACTIVE_DURING_HEURISTIC")
        require(bundle["web_copy"].isEnabled(), "WEB_COPY_REMAINS_ACTIVE_DURING_HEURISTIC")
        require(bundle["web_receive"].isEnabled(), "WEB_RECEIVE_REMAINS_ACTIVE_DURING_HEURISTIC")

        correction_gui.heuristic_execution_state = lambda _window: SimpleNamespace(
            waiting=False, active_stage="", progress_phase="", background_job_alive=False
        )
        correction_gui.local_ai_execution_state = lambda _window: SimpleNamespace(
            waiting=True, active_stage="ADVANCED_QUALITY_REVIEW",
            progress_phase="TARGETED_REPAIR_ATTEMPT_1", background_job_alive=True
        )
        correction_gui.sync_workbench_stage_correction_controls(
            window, lambda _window: "E:/project"
        )
        require(bundle["heuristic"].isEnabled(), "HEURISTIC_REMAINS_ACTIVE_DURING_LOCAL_AI")
        require(not bundle["local_ai"].isEnabled(), "ACTIVE_LOCAL_AI_START_TEMPORARILY_BUSY")
        require(bundle["web_copy"].isEnabled(), "WEB_COPY_REMAINS_ACTIVE_DURING_LOCAL_AI")
        require(bundle["web_receive"].isEnabled(), "WEB_RECEIVE_REMAINS_ACTIVE_DURING_LOCAL_AI")
    finally:
        correction_gui.heuristic_execution_state = original_heuristic
        correction_gui.local_ai_execution_state = original_local

    start_aqr_sonar(window)
    app.processEvents()
    monitor = window._large_file_refactor_workbench_aqr_sonar_monitor
    require(monitor.widget().isVisible(), "AQR_SONAR_VISIBLE_WHILE_RUNNING")
    require(
        monitor.widget().isVisibleTo(window),
        "AQR_SONAR_VISIBLE_TO_REAL_WIDGET_HOST",
    )
    update_aqr_sonar(window, "RUFF", "RUNNING")
    app.processEvents()
    require(monitor.widget().isVisible(), "AQR_SONAR_REMAINS_VISIBLE_DURING_PROGRESS")
    finish_aqr_sonar_blocked(window, "RUFF failed")
    app.processEvents()
    require(monitor.widget().isVisible(), "AQR_SONAR_TERMINAL_FEEDBACK_VISIBLE")
    monitor.set_idle()
    app.processEvents()
    require(not monitor.widget().isVisible(), "AQR_SONAR_SETTLES_TO_IDLE")
    window.close()
    app.processEvents()

    print("WORKBENCH_CORRECTION_ROUTE_REUSE_AND_AQR_SONAR_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
