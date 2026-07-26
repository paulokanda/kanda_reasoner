"""Validate governed AQR blocked-stage correction recovery."""
from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

__all__ = []

FEATURE_ID = "advanced-quality-review-blocked-stage-correction-lane-v1"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (  # noqa: E402
    workbench_stage_correction_context as context_mod,
)


class Output:
    """Tiny QPlainTextEdit substitute for pure contract validation."""

    def __init__(self, text: str = "") -> None:
        self._text = text

    def toPlainText(self) -> str:
        return self._text


class EnumValue:
    """Tiny enum-like value used by duck-typed AQR contracts."""

    def __init__(self, value: str) -> None:
        self.value = value


class Controller:
    """Expose only the controller running projection used by the context layer."""

    def __init__(self, running: bool) -> None:
        self.running = running

    def state(self):
        return SimpleNamespace(running=self.running)


def _outcome(execution: str, decision: str):
    rules = (
        SimpleNamespace(
            rule_id="AQR_RUFF_NEW_REGRESSION",
            decision=EnumValue("BLOCKED"),
            rationale="New Ruff regression requires correction.",
        ),
        SimpleNamespace(
            rule_id="AQR_MYPY_TYPE_CONTRACT",
            decision=EnumValue("INDETERMINATE"),
            rationale="Type evidence did not complete authoritatively.",
        ),
    )
    return SimpleNamespace(
        run_record=SimpleNamespace(execution_status=EnumValue(execution)),
        cross_check_report=SimpleNamespace(
            quality_decision=EnumValue(decision),
            rule_results=rules,
        ),
    )


def _window(*, running: bool, outcome=None, terminal_status: str = ""):
    return SimpleNamespace(
        _large_file_refactor_workbench_aqr_controller=Controller(running),
        _large_file_refactor_workbench_advanced_quality_review=outcome,
        _large_file_refactor_workbench_aqr_terminal_status=terminal_status,
        _large_file_refactor_workbench_aqr_terminal_diagnostic="",
        _large_file_refactor_workbench_aqr_stage_states={
            "RUFF": "FAILED",
            "API_REVIEW": "FAILED",
            "IMPORT_GRAPH": "SUCCEEDED",
            "TYPE_REVIEW": "FAILED",
            "DEAD_CODE": "SUCCEEDED",
            "DELTA": "PASS",
            "CROSS_CHECK": "INDETERMINATE",
            "PERSISTENCE": "PASS",
        },
        _large_file_refactor_workbench_aqr_output=Output(
            "ADVANCED QUALITY REVIEW COMPLETE\n"
            "Execution status: FAILED\n"
            "Quality decision: INDETERMINATE"
        ),
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=None,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
        _large_file_refactor_workbench_intake_output=Output(),
        _large_file_refactor_workbench_dependency_output=Output(),
        _large_file_refactor_workbench_real_preview_output=Output(),
        _large_file_refactor_workbench_validation_output=Output(),
        _large_file_refactor_workbench_preflight_output=Output(),
        _large_file_refactor_workbench_source_payload_output=Output(),
        _large_file_refactor_workbench_completion_status_output=Output(),
        _large_file_refactor_workbench_plan_snapshot=None,
    )


def run_validation() -> None:
    _validate_registry_and_terminal_context()
    _validate_running_review_does_not_open_lane()
    _validate_gui_row_and_preflight_projection()
    _validate_aqr_correction_service_contract()
    _validate_snapshot_invalidation_contract()
    _validate_size_policy()

    print("AQR_CORRECTION_STAGE_REGISTERED: PASS")
    print("AQR_RUNNING_STATE_KEEPS_CORRECTION_ROUTES_CLOSED: PASS")
    print("AQR_TERMINAL_BLOCKED_EVIDENCE_OPENS_CORRECTION_ROUTES: PASS")
    print("AQR_CORRECTION_CONTEXT_INCLUDES_EXECUTION_DECISION_RULES: PASS")
    print("AQR_CORRECTION_PROMPT_INCLUDES_EXACT_FAILURE_CONTEXT_AND_PASS_GOAL: PASS")
    print("AQR_HEURISTIC_CORRECTION_DOES_NOT_SYNTHESIZE_PASS: PASS")
    print("AQR_LOCAL_AI_AND_WEB_AI_RECEIVE_EXACT_BLOCKER_CONTEXT: PASS")
    print("AQR_CORRECTION_RELOAD_INVALIDATES_DOWNSTREAM_AQR_EVIDENCE: PASS")
    print("AQR_PREFLIGHT_TEXT_TRACKS_RUNNING_BLOCKED_READY_STATE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("AQR_BLOCKED_STAGE_CORRECTION_LANE: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _validate_registry_and_terminal_context() -> None:
    assert "ADVANCED_QUALITY_REVIEW" in context_mod.WORKBENCH_CORRECTABLE_STAGES
    window = _window(running=False, outcome=_outcome("FAILED", "INDETERMINATE"))
    assert context_mod.stage_correction_needed(
        window,
        "ADVANCED_QUALITY_REVIEW",
        "E:/active_project",
    )
    context = context_mod.build_stage_correction_context(
        window,
        "ADVANCED_QUALITY_REVIEW",
        "E:/active_project",
    )
    assert context.status == "FAILED"
    assert "AQR_EXECUTION_STATUS:FAILED" in context.blockers
    assert "AQR_QUALITY_DECISION:INDETERMINATE" in context.blockers
    assert any(item.startswith("AQR_RULE:AQR_RUFF_NEW_REGRESSION:BLOCKED") for item in context.blockers)
    prompt = context.prompt_text()
    assert "ADVANCED_QUALITY_REVIEW" in prompt
    assert "Preflight Backup Readiness" in prompt
    assert "AQR_EXECUTION_STATUS:FAILED" in prompt
    assert "Do not force-enable the next phase" in prompt


def _validate_running_review_does_not_open_lane() -> None:
    window = _window(running=True, outcome=None)
    assert not context_mod.stage_correction_needed(
        window,
        "ADVANCED_QUALITY_REVIEW",
        "E:/active_project",
    )


def _validate_gui_row_and_preflight_projection() -> None:
    gui = (PKG / "advanced_quality_review_gui.py").read_text(encoding="utf-8")
    lane = (PKG / "workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    assert '"ADVANCED_QUALITY_REVIEW"' in gui
    assert "build_workbench_stage_correction_row(" in gui
    assert '"ADVANCED_QUALITY_REVIEW": "_large_file_refactor_workbench_aqr_output"' in lane
    for marker in (
        "AQR_RUNNING",
        "AQR_READY",
        "AQR_BLOCKED",
        "AQR_FAILED",
    ):
        assert marker in gui


def _validate_aqr_correction_service_contract() -> None:
    service = (PKG / "workbench_stage_correction_service.py").read_text(encoding="utf-8")
    local_runtime = (PKG / "workbench_local_ai_correction_runtime.py").read_text(encoding="utf-8")
    required = (
        'context.stage == "ADVANCED_QUALITY_REVIEW"',
        "_build_aqr_heuristic_candidate(",
        "_apply_aqr_heuristic_candidate(",
        "No AQR PASS was synthesized or prevalidated.",
        "Rerun Dependency Readiness, Real Preview, Structural Validation, and Advanced Quality Review in order.",
        'correction_context["blocked_workbench_plan"]',
        '"workbench_failure_context": correction_context',
    )
    for marker in required:
        assert marker in service, marker
    assert "strategy_instruction=context.prompt_text()" in local_runtime
    assert "setEnabled(True)" not in service
    assert "setEnabled(True)" not in local_runtime


def _validate_snapshot_invalidation_contract() -> None:
    bridge = (PKG / "workbench_snapshot_bridge.py").read_text(encoding="utf-8")
    for marker in (
        '"_large_file_refactor_workbench_advanced_quality_review"',
        "_large_file_refactor_workbench_aqr_identity_hash = \"\"",
        "_large_file_refactor_workbench_aqr_stage_states = {}",
        "_large_file_refactor_workbench_aqr_terminal_status = \"\"",
    ):
        assert marker in bridge, marker


def _validate_size_policy() -> None:
    names = (
        "advanced_quality_review_gui.py",
        "workbench_stage_correction_context.py",
        "workbench_stage_correction_gui.py",
        "workbench_stage_correction_service.py",
        "workbench_snapshot_bridge.py",
    )
    for name in names:
        lines = len((PKG / name).read_text(encoding="utf-8").splitlines())
        assert lines <= 500, f"SIZE_POLICY:{name}:{lines}"


if __name__ == "__main__":
    run_validation()
