"""Validate AQR snapshot-lineage reset on real Qt text/progress widgets."""
from __future__ import annotations

import os
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit, QProgressBar, QWidget

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_aqr_snapshot_lifecycle import (
    retire_aqr_for_snapshot_replacement,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


class _Controller:
    def __init__(self) -> None:
        self.abandoned = False

    def abandon_current_generation(self) -> bool:
        self.abandoned = True
        return True


def main() -> int:
    app = QApplication.instance() or QApplication([])
    host = QWidget()
    host.show()
    progress = QPlainTextEdit(host)
    progress.setPlainText(
        "ADVANCED QUALITY REVIEW PROGRESS\n\n"
        "ENVIRONMENT_PREFLIGHT: PASS\n"
        "RUFF: FAILED\n"
        "API_REVIEW: STAGE_START:griffe_baseline\n"
        "IMPORT_GRAPH: WAITING"
    )
    bar = QProgressBar(host)
    bar.setValue(4)
    session = object()
    controller = _Controller()
    window = SimpleNamespace(
        _large_file_refactor_workbench_aqr_controller=controller,
        _large_file_refactor_workbench_aqr_progress_output=progress,
        _large_file_refactor_workbench_aqr_progress_bar=bar,
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_identity_hash="old-identity",
        _large_file_refactor_workbench_aqr_context=object(),
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="old diagnostic",
        _large_file_refactor_workbench_aqr_correction_session=session,
    )
    app.processEvents()
    retire_aqr_for_snapshot_replacement(window)
    app.processEvents()

    text = progress.toPlainText()
    require(controller.abandoned, "AQR_REAL_WIDGET_OLD_GENERATION_RETIRED")
    require(
        "RUFF: WAITING" in text
        and "API_REVIEW: WAITING" in text
        and "PERSISTENCE: WAITING" in text,
        "AQR_REAL_WIDGET_STALE_PROGRESS_REPLACED_BY_WAITING_STATE",
    )
    require(bar.value() == 0, "AQR_REAL_WIDGET_PROGRESS_BAR_RESET")
    require(
        window._large_file_refactor_workbench_aqr_correction_session is session,
        "AQR_REAL_WIDGET_CORRECTION_SESSION_PRESERVED",
    )
    host.close()
    app.processEvents()
    print("AQR_SNAPSHOT_LINEAGE_RETIREMENT_REAL_WIDGET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
