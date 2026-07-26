# project-path: tools/validate_workbench_blocked_stage_correction_lane_v1.py
"""Validate fail-closed Workbench progression and blocker correction routes."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

FEATURE_ID = "architecture-review-workbench-blocked-stage-correction-lane-v1"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PKG / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load " + filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Output:
    def __init__(self, text: str = "") -> None:
        self.text = text

    def toPlainText(self) -> str:
        return self.text


def run_validation() -> None:
    progression = _load("kanda_progression_focused", "workbench_gui_progression.py")
    context_mod = _load("kanda_correction_context_focused", "workbench_stage_correction_context.py")
    _validate_preview_to_validate_gate(progression)
    _validate_blocked_context(context_mod)
    _validate_ready_stage_has_no_correction(context_mod)
    _validate_gui_routes()
    _validate_service_routes()
    _validate_fail_closed_source_contract()
    _validate_legacy_guidance()
    _validate_sizes()
    print("REAL_PREVIEW_READY_ENABLES_VALIDATE_REAL_PREVIEW: PASS")
    print("BLOCKED_STAGE_EXPOSES_CORRECTION_CONTEXT: PASS")
    print("CORRECTION_PROMPT_INCLUDES_ERROR_CONTEXT_AND_PASS_GOAL: PASS")
    print("READY_STAGE_HIDES_CORRECTION_ROUTES: PASS")
    print("HEURISTIC_CORRECTION_REBUILDS_AND_RELOADS_PLAN: PASS")
    print("LOCAL_AI_RECEIVES_EXACT_BLOCKER_CONTEXT: PASS")
    print("WEB_AI_CORRECTION_PACKAGE_CONTAINS_WORKBENCH_FAILURE_CONTEXT: PASS")
    print("WEB_AI_RECEIVE_RELOADS_ACCEPTED_VERSION: PASS")
    print("CORRECTION_ROUTES_DO_NOT_FORCE_ENABLE_NEXT_STAGE: PASS")
    print("LEGACY_APPLY_ROLLBACK_EXPLAINED_AS_NON_SEQUENTIAL: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("WORKBENCH_BLOCKED_STAGE_CORRECTION_LANE: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _validate_preview_to_validate_gate(progression) -> None:
    preview = SimpleNamespace(
        status="real_preview_written",
        files=(SimpleNamespace(relative_path="helper.py"),),
        written_files=("preview/helper.py", "preview/REAL_PREVIEW_MANIFEST.json"),
        blockers=(),
    )
    state = progression.build_workbench_gui_progression(preview=preview)
    assert state.structural_validation_enabled
    blocked = SimpleNamespace(
        status="blocked",
        files=(),
        written_files=(),
        blockers=("MOVED_SYMBOL_BODY_MISMATCH:f",),
    )
    blocked_state = progression.build_workbench_gui_progression(preview=blocked)
    assert not blocked_state.structural_validation_enabled


def _base_window(structural) -> SimpleNamespace:
    return SimpleNamespace(
        _large_file_refactor_workbench_intake=None,
        _large_file_refactor_workbench_dependency_readiness=None,
        _large_file_refactor_workbench_real_preview=None,
        _large_file_refactor_workbench_structural_validation=structural,
        _large_file_refactor_workbench_preflight_backup=None,
        _large_file_refactor_workbench_source_payload=None,
        _large_file_refactor_workbench_completion_evidence=None,
        _large_file_refactor_workbench_intake_output=Output(),
        _large_file_refactor_workbench_dependency_output=Output(),
        _large_file_refactor_workbench_real_preview_output=Output(),
        _large_file_refactor_workbench_validation_output=Output(
            "Status: blocked\nBlockers:\n- MOVED_SYMBOL_BODY_MISMATCH:f"
        ),
        _large_file_refactor_workbench_preflight_output=Output(),
        _large_file_refactor_workbench_source_payload_output=Output(),
        _large_file_refactor_workbench_completion_status_output=Output(),
        _large_file_refactor_workbench_plan_snapshot=None,
    )


def _validate_blocked_context(context_mod) -> None:
    structural = SimpleNamespace(
        status="blocked",
        blockers=("MOVED_SYMBOL_BODY_MISMATCH:f",),
        warnings=("STRUCTURAL_VALIDATION_ONLY",),
    )
    window = _base_window(structural)
    context = context_mod.build_stage_correction_context(
        window,
        "STRUCTURAL_VALIDATION",
        "E:/active_project",
    )
    assert context_mod.stage_correction_needed(
        window,
        "STRUCTURAL_VALIDATION",
        "E:/active_project",
    )
    assert "MOVED_SYMBOL_BODY_MISMATCH:f" in context.blockers
    prompt = context.prompt_text()
    assert "OBSERVED FAILURE CONTEXT" in prompt
    assert "Do not force-enable the next phase" in prompt
    assert "Advanced Quality Review" in prompt
    assert "MOVED_SYMBOL_BODY_MISMATCH:f" in prompt


def _validate_ready_stage_has_no_correction(context_mod) -> None:
    structural = SimpleNamespace(
        status="passed_with_warnings",
        blockers=(),
        warnings=("BEHAVIOR_VALIDATION_NOT_RUN",),
    )
    window = _base_window(structural)
    assert not context_mod.stage_correction_needed(
        window,
        "STRUCTURAL_VALIDATION",
        "E:/active_project",
    )


def _validate_gui_routes() -> None:
    gui = (PKG / "workbench_gui.py").read_text(encoding="utf-8")
    completion = (PKG / "workbench_completion_gui.py").read_text(encoding="utf-8")
    lane = (PKG / "workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    for stage in (
        "PLAN_INTAKE",
        "DEPENDENCY_READINESS",
        "REAL_PREVIEW",
        "STRUCTURAL_VALIDATION",
        "PREFLIGHT_BACKUP",
        "SOURCE_PAYLOAD",
    ):
        assert f'build_workbench_stage_correction_row(window, "{stage}"' in gui
    aqr_gui = (PKG / "advanced_quality_review_gui.py").read_text(encoding="utf-8")
    assert '"ADVANCED_QUALITY_REVIEW"' in aqr_gui
    assert "build_workbench_stage_correction_row(" in aqr_gui
    assert 'build_workbench_stage_correction_row(window, "COMPLETION_EVIDENCE"' in completion
    for label in (
        "Heuristic Correction",
        "Local AI Correction",
        "Copy Web AI Correction Package",
        "Receive Web AI Correction",
    ):
        assert label in lane
    assert "threading.Thread(" not in lane
    assert "start_local_ai_correction(" in lane
    assert "Cancel Local AI Wait" in lane
    controller = (PKG / "workbench_local_ai_correction_qt_controller.py").read_text(encoding="utf-8")
    assert "QThread()" in controller
    assert "_LOCAL_AI_TIMEOUT_MS = 120_000" in controller


def _validate_service_routes() -> None:
    service = (PKG / "workbench_stage_correction_service.py").read_text(encoding="utf-8")
    local_runtime = (PKG / "workbench_local_ai_correction_runtime.py").read_text(encoding="utf-8")
    required = (
        "build_split_plan(",
        "store_heuristic_version(",
        "load_latest_snapshot_into_workbench(",
        'correction_context["blocked_workbench_plan"]',
        '"workbench_failure_context": correction_context',
    )
    for marker in required:
        assert marker in service, marker
    for marker in (
        "analyze_python_file(context.target_file)",
        "strategy_instruction=context.prompt_text()",
        "force_exploration=True",
        "max_rounds=2",
        "include_naming_review=False",
        "include_final_audit=False",
    ):
        assert marker in local_runtime, marker
    lane = (PKG / "workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    assert "open_receive_planning_from_web_ai(" in lane
    assert "load_latest_snapshot_into_workbench(" in lane


def _validate_fail_closed_source_contract() -> None:
    service = (PKG / "workbench_stage_correction_service.py").read_text(encoding="utf-8")
    lane = (PKG / "workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    context = (PKG / "workbench_stage_correction_context.py").read_text(encoding="utf-8")
    assert "setEnabled(True)" not in service
    assert "setEnabled(True)" not in lane
    assert "Do not force-enable the next phase" in context
    assert "deterministic rerun" in lane
    assert "Downstream evidence was invalidated" in lane


def _validate_legacy_guidance() -> None:
    gui = (PKG / "workbench_gui.py").read_text(encoding="utf-8")
    assert 'QPushButton("Legacy Apply Source Changes (Disabled)")' not in gui
    assert 'QPushButton("Rollback Last Apply")' not in gui
    assert "Exact apply token:" not in gui
    assert "Next governed stage: Completion Review and Refactor Authorization." in gui
    assert "Legacy direct apply and rollback controls are not part of this workflow." in gui


def _validate_sizes() -> None:
    names = (
        "workbench_gui.py",
        "workbench_completion_gui.py",
        "workbench_stage_correction_context.py",
        "workbench_stage_correction_service.py",
        "workbench_stage_correction_gui.py",
    )
    for name in names:
        lines = len((PKG / name).read_text(encoding="utf-8").splitlines())
        assert lines <= 500, f"SIZE_POLICY:{name}:{lines}"


if __name__ == "__main__":
    run_validation()
