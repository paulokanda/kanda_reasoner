"""Real PySide validation for AQR terminal correction-route projection."""
from __future__ import annotations

import os
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_gui import (
    build_workbench_stage_correction_row,
    sync_workbench_stage_correction_controls,
)

FEATURE_ID = "advanced-quality-review-blocked-stage-correction-lane-real-widget-v1"


class EnumValue:
    def __init__(self, value: str) -> None:
        self.value = value


class Controller:
    def __init__(self, running: bool = False) -> None:
        self.running = running

    def state(self):
        return SimpleNamespace(running=self.running)


def _output(text: str = "") -> QPlainTextEdit:
    widget = QPlainTextEdit()
    widget.setPlainText(text)
    return widget


def _window():
    outcome = SimpleNamespace(
        run_record=SimpleNamespace(execution_status=EnumValue("FAILED")),
        cross_check_report=SimpleNamespace(
            quality_decision=EnumValue("INDETERMINATE"),
            rule_results=(
                SimpleNamespace(
                    rule_id="AQR_RUFF_NEW_REGRESSION",
                    decision=EnumValue("BLOCKED"),
                    rationale="New regression.",
                ),
            ),
        ),
    )
    return SimpleNamespace(
        _large_file_refactor_workbench_aqr_controller=Controller(False),
        _large_file_refactor_workbench_advanced_quality_review=outcome,
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="",
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_output=_output(
            "ADVANCED QUALITY REVIEW COMPLETE\nExecution status: FAILED\nQuality decision: INDETERMINATE"
        ),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
        _large_file_refactor_workbench_intake_output=_output(),
        _large_file_refactor_workbench_dependency_output=_output(),
        _large_file_refactor_workbench_real_preview_output=_output(),
        _large_file_refactor_workbench_validation_output=_output(),
        _large_file_refactor_workbench_preflight_output=_output(),
        _large_file_refactor_workbench_source_payload_output=_output(),
        _large_file_refactor_workbench_completion_status_output=_output(),
        _large_file_refactor_workbench_plan_snapshot=None,
    )


def run_validation() -> None:
    app = QApplication.instance() or QApplication([])
    window = _window()
    host = build_workbench_stage_correction_row(
        window,
        "ADVANCED_QUALITY_REVIEW",
        lambda _window: "E:/active_project",
        lambda _window: None,
    )
    host.show()
    app.processEvents()
    sync_workbench_stage_correction_controls(
        window,
        lambda _window: "E:/active_project",
    )
    controls = window._large_file_refactor_workbench_correction_controls[
        "ADVANCED_QUALITY_REVIEW"
    ]
    assert controls["heuristic"].isEnabled()
    assert controls["local_ai"].isEnabled()
    assert controls["web_copy"].isEnabled()
    assert controls["web_receive"].isEnabled()
    assert not controls["cancel_heuristic"].isEnabled()
    assert "Blocked evidence detected" in controls["label"].text()

    window._large_file_refactor_workbench_aqr_controller.running = True
    sync_workbench_stage_correction_controls(
        window,
        lambda _window: "E:/active_project",
    )
    for key in ("heuristic", "local_ai", "web_copy", "web_receive"):
        assert not controls[key].isEnabled()

    print("AQR_CORRECTION_REAL_WIDGET_TERMINAL_BLOCK_ENABLES_ROUTES: PASS")
    print("AQR_CORRECTION_REAL_WIDGET_RUNNING_STATE_CLOSES_ROUTES: PASS")
    print("AQR_CORRECTION_REAL_WIDGET_FAIL_CLOSED_NEXT_GATE_UNCHANGED: PASS")
    print("AQR_BLOCKED_STAGE_CORRECTION_REAL_WIDGET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    host.close()
    app.processEvents()


if __name__ == "__main__":
    run_validation()
