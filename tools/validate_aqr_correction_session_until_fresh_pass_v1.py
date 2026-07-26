"""Validate Stage 5 correction session persistence until fresh AQR PASS."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_aqr_correction_session import (
    clear_aqr_correction_session,
    current_aqr_correction_session,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_correction_candidate_guard import (
    plans_materially_different,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import (
    build_workbench_gui_progression,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_context import (
    stage_correction_needed,
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
        self._text = text

    def toPlainText(self) -> str:
        return self._text


class _Plan:
    def __init__(self, value: str) -> None:
        self.value = value

    def to_dict(self) -> dict[str, str]:
        return {"value": self.value}


def _blocked_window() -> SimpleNamespace:
    return SimpleNamespace(
        _large_file_refactor_workbench_advanced_quality_review=None,
        _large_file_refactor_workbench_aqr_terminal_status="FAILED",
        _large_file_refactor_workbench_aqr_terminal_diagnostic="",
        _large_file_refactor_workbench_aqr_stage_states={
            "RUFF": "FAILED",
            "API_REVIEW": "FAILED",
            "IMPORT_GRAPH": "SUCCEEDED",
            "TYPE_REVIEW": "FAILED",
        },
        _large_file_refactor_workbench_aqr_output=_Text("ADVANCED QUALITY REVIEW COMPLETE"),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
        _large_file_refactor_workbench_aqr_identity_hash="aqr-failed-identity",
        _large_file_refactor_workbench_plan_snapshot=None,
    )


def main() -> int:
    window = _blocked_window()
    require(
        stage_correction_needed(window, "ADVANCED_QUALITY_REVIEW", "E:/project"),
        "AQR_TERMINAL_FAILURE_OPENS_CORRECTION_SESSION",
    )
    require(
        current_aqr_correction_session(window) is not None,
        "AQR_CORRECTION_SESSION_RETAINED_FROM_TERMINAL_FAILURE",
    )

    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_output = _Text(
        "Snapshot changed. Run a fresh Advanced Quality Review after Structural Validation passes."
    )
    require(
        stage_correction_needed(window, "ADVANCED_QUALITY_REVIEW", "E:/project"),
        "AQR_CORRECTION_ROUTES_REMAIN_AVAILABLE_AFTER_CANDIDATE_GENERATION",
    )

    require(
        not plans_materially_different(_Plan("same"), _Plan("same")),
        "CORRECTION_IDENTICAL_PLAN_DETECTED_AS_NOOP",
    )
    require(
        plans_materially_different(_Plan("before"), _Plan("after")),
        "CORRECTION_MATERIAL_PLAN_CHANGE_DETECTED",
    )

    runtime_text = (PLANNER / "workbench_local_ai_correction_runtime.py").read_text(encoding="utf-8")
    service_text = (PLANNER / "workbench_stage_correction_service.py").read_text(encoding="utf-8")
    gui_text = (PLANNER / "workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    aqr_gui_text = (PLANNER / "advanced_quality_review_gui.py").read_text(encoding="utf-8")

    require(
        "action_count <= 0 or not plans_materially_different(plan, result.plan)" in runtime_text,
        "LOCAL_AI_ZERO_CHANGE_OR_IDENTICAL_PLAN_REJECTED",
    )
    require(
        "int(candidate.corrections_applied or 0) <= 0" in service_text,
        "LOCAL_AI_NOOP_DEFENSE_IN_DEPTH",
    )
    require(
        "AQR Heuristic correction produced no material plan change" in service_text,
        "HEURISTIC_AQR_NOOP_REJECTED",
    )
    require(
        "Imported Web AI correction was rejected as a no-op" in gui_text,
        "WEB_AI_AQR_NOOP_REJECTED",
    )
    require(
        'note_aqr_correction_candidate(window, "local_ai")' in service_text
        and 'note_aqr_correction_candidate(window, "heuristic")' in service_text
        and 'note_aqr_correction_candidate(window, "web_ai")' in gui_text,
        "AQR_CORRECTION_SESSION_PERSISTS_ACROSS_ROUTE_GENERATIONS",
    )
    require(
        "clear_aqr_correction_session(window)" in aqr_gui_text,
        "FRESH_AQR_PASS_RETIRES_CORRECTION_SESSION",
    )

    progression_before_pass = build_workbench_gui_progression(
        intake=SimpleNamespace(
            status="plan_intake_ready",
            ready_for_real_preview=True,
            source_hash_fresh=True,
        )
    )
    require(
        not progression_before_pass.preflight_enabled,
        "PREFLIGHT_REMAINS_CLOSED_WITH_UNRESOLVED_AQR",
    )

    pass_outcome = SimpleNamespace(
        cross_check_report=SimpleNamespace(
            quality_decision=SimpleNamespace(value="PASS"),
        ),
        run_record=SimpleNamespace(
            execution_status=SimpleNamespace(value="SUCCEEDED"),
        ),
    )
    progression_after_pass = build_workbench_gui_progression(
        advanced_quality_review=pass_outcome,
    )
    require(
        progression_after_pass.preflight_enabled,
        "PREFLIGHT_OPENS_ONLY_FROM_FRESH_AQR_PASS",
    )

    clear_aqr_correction_session(window)
    require(
        not stage_correction_needed(window, "ADVANCED_QUALITY_REVIEW", "E:/project"),
        "AQR_CORRECTION_SESSION_RETIRES_AFTER_PASS_CONTRACT",
    )

    print("AQR_CORRECTION_SESSION_UNTIL_FRESH_PASS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
