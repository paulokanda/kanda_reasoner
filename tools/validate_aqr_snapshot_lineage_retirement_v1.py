"""Validate AQR lineage retirement and visible progress reset on snapshot replacement."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_aqr_snapshot_lifecycle import (
    retire_aqr_for_snapshot_replacement,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"
ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


class _Text:
    def __init__(self, text: str) -> None:
        self.text = text

    def setPlainText(self, text: str) -> None:
        self.text = text

    def toPlainText(self) -> str:
        return self.text


class _Bar:
    def __init__(self) -> None:
        self.value = 4

    def setValue(self, value: int) -> None:
        self.value = value


class _Controller:
    def __init__(self) -> None:
        self.abandoned = False

    def abandon_current_generation(self) -> bool:
        self.abandoned = True
        return True


def main() -> int:
    session = object()
    controller = _Controller()
    window = SimpleNamespace(
        _large_file_refactor_workbench_aqr_controller=controller,
        _large_file_refactor_workbench_aqr_progress_output=_Text(
            "ADVANCED QUALITY REVIEW PROGRESS\n\nRUFF: FAILED\nAPI_REVIEW: STAGE_START:griffe_baseline"
        ),
        _large_file_refactor_workbench_aqr_progress_bar=_Bar(),
        _large_file_refactor_workbench_aqr_stage_states={"RUFF": "FAILED"},
        _large_file_refactor_workbench_aqr_identity_hash="old-identity",
        _large_file_refactor_workbench_aqr_context=object(),
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="old failure",
        _large_file_refactor_workbench_aqr_correction_session=session,
    )
    retire_aqr_for_snapshot_replacement(window)
    require(controller.abandoned, "AQR_OLD_GENERATION_RETIRED_ON_SNAPSHOT_REPLACEMENT")
    progress = window._large_file_refactor_workbench_aqr_progress_output.toPlainText()
    require(
        "RUFF: WAITING" in progress and "API_REVIEW: WAITING" in progress,
        "AQR_VISIBLE_PROGRESS_RESET_TO_FRESH_WAITING_STATE",
    )
    require(
        window._large_file_refactor_workbench_aqr_progress_bar.value == 0,
        "AQR_PROGRESS_BAR_RESET_ON_SNAPSHOT_REPLACEMENT",
    )
    require(
        window._large_file_refactor_workbench_aqr_stage_states == {}
        and window._large_file_refactor_workbench_aqr_identity_hash == ""
        and window._large_file_refactor_workbench_aqr_terminal_status == "",
        "AQR_STALE_LINEAGE_EVIDENCE_CLEARED",
    )
    require(
        window._large_file_refactor_workbench_aqr_correction_session is session,
        "AQR_UNRESOLVED_CORRECTION_SESSION_PRESERVED",
    )

    controller_text = (PLANNER / "advanced_quality_review_qt_controller.py").read_text(encoding="utf-8")
    bridge_text = (PLANNER / "workbench_snapshot_bridge.py").read_text(encoding="utf-8")
    require(
        "def abandon_current_generation" in controller_text
        and 'job["accept_result"] = False' in controller_text
        and 'job["suppress_settled"] = True' in controller_text,
        "AQR_RETIRED_GENERATION_REJECTS_LATE_OUTPUT_AND_SETTLEMENT_CALLBACK",
    )
    require(
        "retire_aqr_for_snapshot_replacement(window)" in bridge_text,
        "WORKBENCH_SNAPSHOT_REPLACEMENT_RETIRES_AQR_BEFORE_DOWNSTREAM_RESET",
    )
    print("AQR_SNAPSHOT_LINEAGE_RETIREMENT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
