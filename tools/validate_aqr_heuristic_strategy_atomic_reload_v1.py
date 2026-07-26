"""Validate AQR heuristic strategy selection and atomic Workbench reload."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
from types import SimpleNamespace

__all__ = [
    "main",
]

FEATURE_ID = "advanced-quality-review-blocked-stage-correction-lane-v1"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (  # noqa: E402
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.docstring_planner import (  # noqa: E402
    build_docstring_proposals,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (  # noqa: E402
    attach_docstring_proposals_to_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (  # noqa: E402
    PLANNER_VERSION_HEURISTIC,
    initialize_planner_version_state,
    select_planner_version,
    store_heuristic_version,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (  # noqa: E402
    build_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_snapshot_bridge import (  # noqa: E402
    load_latest_snapshot_into_workbench,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_context import (  # noqa: E402
    WorkbenchStageCorrectionContext,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_service import (  # noqa: E402
    build_heuristic_workbench_correction_candidate,
)


class Output:
    """Minimal text output used by the snapshot reset contract."""

    def __init__(self, text: str = "") -> None:
        self.text = text

    def setPlainText(self, text: str) -> None:
        self.text = text

    def toPlainText(self) -> str:
        return self.text


class CheckBox:
    """Minimal checkbox contract for reset paths."""

    def __init__(self) -> None:
        self.checked = True
        self.enabled = True

    def setChecked(self, value: bool) -> None:
        self.checked = value

    def setEnabled(self, value: bool) -> None:
        self.enabled = value


class Button:
    """Minimal button contract for reset paths."""

    def __init__(self) -> None:
        self.enabled = True

    def setEnabled(self, value: bool) -> None:
        self.enabled = value


class Edit:
    """Minimal line-edit contract for reset paths."""

    def __init__(self) -> None:
        self.value = "token"

    def clear(self) -> None:
        self.value = ""


def main() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    report = analyze_python_file(str(target))
    original_plan = build_split_plan(report, source_path=None, preferred_strategy="balanced")
    proposals = build_docstring_proposals(report, original_plan)
    original_plan = attach_docstring_proposals_to_plan(original_plan, proposals)

    context = _aqr_context(str(ROOT), str(target))
    candidate = build_heuristic_workbench_correction_candidate(
        plan=original_plan,
        context=context,
    )
    assert candidate.ok, candidate.message
    assert candidate.strategy == "responsibility_dominant", candidate.strategy
    assert candidate.corrected_plan is not None
    assert candidate.corrected_plan.status != "blocked"
    assert not candidate.corrected_plan.validation_blockers

    dependency_plan = replace(
        original_plan,
        status="blocked",
        validation_blockers=[
            "Synthetic invalid candidate for atomic reload regression: below minimum helper size"
        ],
    )
    assert dependency_plan.status == "blocked"
    assert any("below minimum helper size" in item for item in dependency_plan.validation_blockers)

    window = _window(report, original_plan, proposals, target)
    intake, message = load_latest_snapshot_into_workbench(window, str(ROOT))
    assert intake is not None and intake.ready_for_real_preview, message
    window._large_file_refactor_workbench_intake = intake
    original_snapshot = window._large_file_refactor_workbench_plan_snapshot
    sentinel = SimpleNamespace(status="dependency_readiness_ready")
    window._large_file_refactor_workbench_dependency_readiness = sentinel
    window._large_file_refactor_workbench_dependency_output.setPlainText("CURRENT_DEPENDENCY_EVIDENCE")

    invalid_plan = dependency_plan
    store_heuristic_version(window, invalid_plan, [])
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    rejected, reject_message = load_latest_snapshot_into_workbench(window, str(ROOT))
    assert rejected is not None and not rejected.ready_for_real_preview
    assert "PLANNER_PLAN_BLOCKED" in reject_message
    assert window._large_file_refactor_workbench_plan_snapshot is original_snapshot
    assert window._large_file_refactor_workbench_dependency_readiness is sentinel
    assert window._large_file_refactor_workbench_dependency_output.toPlainText() == "CURRENT_DEPENDENCY_EVIDENCE"

    store_heuristic_version(window, candidate.corrected_plan, list(candidate.proposals))
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    accepted, accept_message = load_latest_snapshot_into_workbench(window, str(ROOT))
    assert accepted is not None and accepted.ready_for_real_preview, accept_message
    assert window._large_file_refactor_workbench_plan_snapshot is not original_snapshot
    assert window._large_file_refactor_workbench_dependency_readiness is None
    assert "Snapshot changed" in window._large_file_refactor_workbench_dependency_output.toPlainText()

    print("AQR_SUCCEEDED_STAGE_TEXT_IGNORED_FOR_FAILURE_STRATEGY: PASS")
    print("AQR_FAILED_API_REVIEW_SELECTS_RESPONSIBILITY_STRATEGY: PASS")
    print("AQR_HEURISTIC_CANDIDATE_REMAINS_PLANNED: PASS")
    print("AQR_INVALID_CANDIDATE_RELOAD_PRESERVES_CURRENT_WORKBENCH_STATE: PASS")
    print("AQR_VALID_CANDIDATE_RELOAD_ATOMICALLY_INVALIDATES_DOWNSTREAM: PASS")
    print("AQR_HEURISTIC_STRATEGY_AND_ATOMIC_RELOAD_REPAIR: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _aqr_context(root: str, target: str) -> WorkbenchStageCorrectionContext:
    return WorkbenchStageCorrectionContext(
        stage="ADVANCED_QUALITY_REVIEW",
        next_phase_goal="Preflight Backup Readiness",
        active_project_root=root,
        target_file=target,
        status="FAILED",
        blockers=(
            "AQR_STAGE:RUFF:FAILED",
            "AQR_STAGE:API_REVIEW:FAILED",
            "AQR_STAGE:TYPE_REVIEW:FAILED",
            "AQR_EXECUTION_STATUS:FAILED",
            "AQR_QUALITY_DECISION:INDETERMINATE",
        ),
        warnings=(),
        stage_output=(
            "ENVIRONMENT_PREFLIGHT: PASS\n"
            "RUFF: FAILED\n"
            "API_REVIEW: FAILED\n"
            "IMPORT_GRAPH: SUCCEEDED\n"
            "TYPE_REVIEW: FAILED\n"
            "DEAD_CODE: SUCCEEDED\n"
            "DELTA: PASS\n"
            "CROSS_CHECK: INDETERMINATE\n"
            "PERSISTENCE: PASS"
        ),
        evidence_chain=(("ADVANCED_QUALITY_REVIEW", "FAILED"),),
        correction_objective="Correct AQR failures without bypassing validation.",
    )


def _window(report, plan, proposals, target: Path):
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    window._large_file_refactor_last_analysis = report
    window._large_file_refactor_planner_candidates = [SimpleNamespace(path=str(target))]
    store_heuristic_version(window, plan, proposals)
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    for name in (
        "_large_file_refactor_workbench_dependency_output",
        "_large_file_refactor_workbench_real_preview_output",
        "_large_file_refactor_workbench_validation_output",
        "_large_file_refactor_workbench_aqr_output",
        "_large_file_refactor_workbench_preflight_output",
        "_large_file_refactor_workbench_source_payload_output",
        "_large_file_refactor_workbench_apply_output",
        "_large_file_refactor_workbench_rollback_output",
    ):
        setattr(window, name, Output())
    for name in (
        "_large_file_refactor_workbench_semantic_review_check",
        "_large_file_refactor_workbench_warning_ack_check",
        "_large_file_refactor_workbench_transaction_confirm_check",
    ):
        setattr(window, name, CheckBox())
    for name in (
        "_large_file_refactor_workbench_transaction_prepare_button",
        "_large_file_refactor_workbench_refactor_large_module_button",
        "_large_file_refactor_workbench_transaction_rollback_button",
    ):
        setattr(window, name, Button())
    window._large_file_refactor_workbench_apply_token_edit = Edit()
    window._large_file_refactor_workbench_rollback_token_edit = Edit()
    return window


if __name__ == "__main__":
    main()
