"""Real Qt validation for unresolved AQR correction-session button projection."""
from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_aqr_correction_session import (
    clear_aqr_correction_session,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_gui import (
    build_workbench_stage_correction_row,
    sync_workbench_stage_correction_controls,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


class _Text:
    def __init__(self, text: str) -> None:
        self._text = text

    def toPlainText(self) -> str:
        return self._text


def main() -> int:
    app = QApplication.instance() or QApplication([])
    window = SimpleNamespace(
        _large_file_refactor_workbench_advanced_quality_review=None,
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="",
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_output=_Text("AQR FAILED"),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
        _large_file_refactor_workbench_aqr_identity_hash="failed-aqr-id",
        _large_file_refactor_workbench_plan_snapshot=None,
    )
    row = build_workbench_stage_correction_row(
        window,
        "ADVANCED_QUALITY_REVIEW",
        lambda _window: "E:/project",
        lambda _window: None,
    )
    row.show()
    app.processEvents()
    sync_workbench_stage_correction_controls(window, lambda _window: "E:/project")
    controls = window._large_file_refactor_workbench_correction_controls[
        "ADVANCED_QUALITY_REVIEW"
    ]
    for key, marker in (
        ("heuristic", "AQR_SESSION_HEURISTIC_ACTIVE_ON_FAILURE"),
        ("local_ai", "AQR_SESSION_LOCAL_AI_ACTIVE_ON_FAILURE"),
        ("web_copy", "AQR_SESSION_WEB_COPY_ACTIVE_ON_FAILURE"),
        ("web_receive", "AQR_SESSION_WEB_RECEIVE_ACTIVE_ON_FAILURE"),
    ):
        require(controls[key].isEnabled(), marker)

    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_output = _Text(
        "Snapshot changed. Run a fresh AQR after Structural Validation passes."
    )
    sync_workbench_stage_correction_controls(window, lambda _window: "E:/project")
    for key, marker in (
        ("heuristic", "AQR_SESSION_HEURISTIC_REMAINS_ACTIVE_AFTER_CANDIDATE"),
        ("local_ai", "AQR_SESSION_LOCAL_AI_REMAINS_ACTIVE_AFTER_CANDIDATE"),
        ("web_copy", "AQR_SESSION_WEB_COPY_REMAINS_ACTIVE_AFTER_CANDIDATE"),
        ("web_receive", "AQR_SESSION_WEB_RECEIVE_REMAINS_ACTIVE_AFTER_CANDIDATE"),
    ):
        require(controls[key].isEnabled(), marker)

    clear_aqr_correction_session(window)
    sync_workbench_stage_correction_controls(window, lambda _window: "E:/project")
    require(
        not any(controls[key].isEnabled() for key in ("heuristic", "local_ai", "web_copy", "web_receive")),
        "AQR_SESSION_ROUTES_CLOSE_AFTER_SESSION_RETIRED",
    )
    row.close()
    app.processEvents()
    print("AQR_CORRECTION_SESSION_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
