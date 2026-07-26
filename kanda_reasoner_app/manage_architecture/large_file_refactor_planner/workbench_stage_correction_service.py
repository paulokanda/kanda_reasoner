"""Governed correction services for blocked Workbench stages."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .ast_analysis import analyze_python_file
from .planner_bounded_refinement import attach_docstring_proposals_to_plan
from .docstring_planner import build_docstring_proposals
from .models import PlannerSettings
from .split_planner import build_split_plan
from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    get_last_generated_native_bundle,
    select_planner_version,
    store_heuristic_version,
    store_local_ai_version,
)
from .planner_web_ai_exchange import build_comprehensive_web_ai_planning_prompt
from .planner_web_ai_import_artifact import build_web_ai_import_contract
from .workbench_plan_intake import WorkbenchPlanIntakeResult
from .workbench_local_ai_correction_models import (
    LocalAIWorkbenchCorrectionCandidate,
)
from .workbench_local_ai_correction_runtime import (
    build_bounded_local_ai_workbench_correction_candidate,
)
from .workbench_heuristic_feedback_search import (
    WorkbenchCorrectionReplayEvidence,
    search_feedback_aware_heuristic_correction,
)
from .workbench_snapshot_bridge import (
    load_latest_snapshot_into_workbench,
    materialize_workbench_owned_plan,
)
from .workbench_stage_correction_context import WorkbenchStageCorrectionContext
from .workbench_aqr_correction_session import note_aqr_correction_candidate
from .workbench_correction_candidate_guard import plans_materially_different

# Frozen v1 service route remains transitively owned by feedback search -> build_split_plan(

__all__ = [
    "HeuristicWorkbenchCorrectionCandidate",
    "WorkbenchCorrectionResult",
    "apply_heuristic_workbench_correction",
    "apply_local_ai_workbench_correction",
    "build_heuristic_workbench_correction_candidate",
    "build_local_ai_workbench_correction_candidate",
    "build_web_ai_workbench_correction_prompt",
]


@dataclass(frozen=True)
class WorkbenchCorrectionResult:
    """One correction attempt that still requires deterministic stage rerun."""

    ok: bool
    route: str
    message: str
    intake: WorkbenchPlanIntakeResult | None = None
    replay: WorkbenchCorrectionReplayEvidence | None = None
    model_name: str = ""


@dataclass(frozen=True)
class HeuristicWorkbenchCorrectionCandidate:
    """Deterministic bounded Heuristic candidate produced off the Qt GUI thread."""

    ok: bool
    message: str
    report: Any = None
    corrected_plan: Any = None
    proposals: tuple[Any, ...] = ()
    replay: WorkbenchCorrectionReplayEvidence | None = None
    strategy: str = ""
    settings_label: str = ""
    attempts: tuple[str, ...] = ()
    history_mode: str = "ast_static_only_no_git_requery"


def build_heuristic_workbench_correction_candidate(
    *,
    plan: Any,
    context: WorkbenchStageCorrectionContext,
    progress_callback: Callable[[str], None] | None = None,
) -> HeuristicWorkbenchCorrectionCandidate:
    """Search feedback-aware variants and return one bounded correction candidate."""
    if context.stage == "ADVANCED_QUALITY_REVIEW":
        return _build_aqr_heuristic_candidate(
            plan=plan,
            context=context,
            progress_callback=progress_callback,
        )
    search = search_feedback_aware_heuristic_correction(
        plan=plan,
        context=context,
        progress_callback=progress_callback,
    )
    return HeuristicWorkbenchCorrectionCandidate(
        ok=search.ok,
        message=search.message,
        report=search.report,
        corrected_plan=search.corrected_plan,
        proposals=search.proposals,
        replay=search.replay,
        strategy=search.strategy,
        settings_label=search.settings_label,
        attempts=search.attempts,
        history_mode="ast_static_only_no_git_requery",
    )


def apply_heuristic_workbench_correction(
    window: object,
    context: WorkbenchStageCorrectionContext,
    candidate: HeuristicWorkbenchCorrectionCandidate,
) -> WorkbenchCorrectionResult:
    """Commit a safe correction candidate and require deterministic downstream rerun."""
    if context.stage == "ADVANCED_QUALITY_REVIEW":
        return _apply_aqr_heuristic_candidate(window, context, candidate)
    if (
        not candidate.ok
        or candidate.corrected_plan is None
        or candidate.replay is None
        or not candidate.replay.passed
    ):
        return WorkbenchCorrectionResult(
            False,
            "heuristic",
            candidate.message,
        )
    window._large_file_refactor_last_analysis = candidate.report
    store_heuristic_version(
        window,
        candidate.corrected_plan,
        list(candidate.proposals),
    )
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    intake, load_message = load_latest_snapshot_into_workbench(
        window,
        context.active_project_root,
    )
    if intake is None or not bool(getattr(intake, "ready_for_real_preview", False)):
        return WorkbenchCorrectionResult(
            False,
            "heuristic",
            "Passing Heuristic candidate existed, but Workbench ownership reload was blocked. "
            + load_message,
        )
    _apply_replay_state(window, candidate.replay, intake)
    return WorkbenchCorrectionResult(
        True,
        "heuristic",
        _correction_pass_message(context, candidate, load_message),
        intake=intake,
        replay=candidate.replay,
    )


def _apply_replay_state(
    window: object,
    replay: WorkbenchCorrectionReplayEvidence,
    intake: WorkbenchPlanIntakeResult,
) -> None:
    """Restore only evidence produced by the passing sequential replay."""
    window._large_file_refactor_workbench_intake = intake
    mapping = {
        "_large_file_refactor_workbench_dependency_readiness": replay.dependency_readiness,
        "_large_file_refactor_workbench_real_preview": replay.real_preview,
        "_large_file_refactor_workbench_structural_validation": replay.structural_validation,
        "_large_file_refactor_workbench_preflight_backup": replay.preflight_backup,
        "_large_file_refactor_workbench_source_payload": replay.source_payload,
        "_large_file_refactor_workbench_completion_evidence": replay.completion_evidence,
    }
    for attr_name, value in mapping.items():
        setattr(window, attr_name, value)
    window._large_file_refactor_workbench_state = _state_for_reached_stage(replay.reached_stage)


def _state_for_reached_stage(stage: str) -> str:
    return {
        "PLAN_INTAKE": "READY_FOR_REAL_PREVIEW",
        "DEPENDENCY_READINESS": "DEPENDENCY_READY",
        "REAL_PREVIEW": "REAL_PREVIEW_READY",
        "STRUCTURAL_VALIDATION": "STRUCTURAL_PREVIEW_VALIDATED",
        "PREFLIGHT_BACKUP": "PREFLIGHT_BACKUP_READY",
        "SOURCE_PAYLOAD": "SOURCE_APPLY_PAYLOAD_READY",
        "COMPLETION_EVIDENCE": "COMPLETION_EVIDENCE_READY",
    }.get(stage, "BLOCKED")


def _correction_pass_message(
    context: WorkbenchStageCorrectionContext,
    candidate: HeuristicWorkbenchCorrectionCandidate,
    load_message: str,
) -> str:
    lines = [
        "HEURISTIC CORRECTION TARGET STAGE PASS",
        "Blocked stage corrected: " + context.stage,
        "Selected strategy: " + (candidate.strategy or "<current replay>"),
        "Settings variant: " + (candidate.settings_label or "<current>"),
        "Sequential replay reached: " + candidate.replay.reached_stage,
        "The corrected snapshot replaced Workbench ownership only after target-stage PASS evidence existed.",
        "The next governed phase is now projected from real replay evidence; no button was force-enabled.",
    ]
    if load_message:
        lines.append("Detail: " + load_message)
    return "\n".join(lines)


def build_local_ai_workbench_correction_candidate(
    *,
    plan: Any,
    proposals: list[Any],
    context: WorkbenchStageCorrectionContext,
) -> LocalAIWorkbenchCorrectionCandidate:
    """Compatibility entry point for the bounded single-track Local AI runtime."""
    return build_bounded_local_ai_workbench_correction_candidate(
        plan=plan,
        proposals=proposals,
        context=context,
    )


def apply_local_ai_workbench_correction(
    window: object,
    context: WorkbenchStageCorrectionContext,
    candidate: LocalAIWorkbenchCorrectionCandidate,
) -> WorkbenchCorrectionResult:
    """Apply a validated Local AI Planner candidate on the GUI thread and reload Workbench ownership."""
    if not candidate.ok or candidate.corrected_plan is None:
        return WorkbenchCorrectionResult(
            False,
            "local_ai",
            candidate.message,
            model_name=candidate.model_name,
        )
    current_plan = materialize_workbench_owned_plan(window)
    if (
        int(candidate.corrections_applied or 0) <= 0
        or not plans_materially_different(current_plan, candidate.corrected_plan)
    ):
        return WorkbenchCorrectionResult(
            False,
            "local_ai",
            "Local AI correction was rejected as a no-op. The current AQR blocker remains active and Heuristic, Local AI, and Web AI routes remain reusable.",
            model_name=candidate.model_name,
        )
    window._large_file_refactor_last_analysis = candidate.report
    store_local_ai_version(
        window,
        candidate.corrected_plan,
        list(candidate.proposals),
    )
    select_planner_version(window, PLANNER_VERSION_LOCAL_AI)
    intake, load_message = load_latest_snapshot_into_workbench(
        window,
        context.active_project_root,
    )
    if intake is None:
        return WorkbenchCorrectionResult(
            False,
            "local_ai",
            "Local AI returned a candidate but Workbench reload was blocked. " + load_message,
            model_name=candidate.model_name,
        )
    if context.stage == "ADVANCED_QUALITY_REVIEW":
        note_aqr_correction_candidate(window, "local_ai")
    return WorkbenchCorrectionResult(
        True,
        "local_ai",
        _correction_loaded_message(
            route="Local AI",
            context=context,
            plan_status=str(getattr(candidate.corrected_plan, "status", "")),
            extra=(
                "review_status=" + candidate.review_status
                + "; corrections_applied=" + str(candidate.corrections_applied)
                + ("; " + load_message if load_message else "")
            ),
        ),
        intake=intake,
        model_name=candidate.model_name,
    )


def build_web_ai_workbench_correction_prompt(
    window: object,
    context: WorkbenchStageCorrectionContext,
) -> str:
    """Build the existing governed Web AI exchange with exact Workbench failure context."""
    report = getattr(window, "_large_file_refactor_last_analysis", None)
    bundle = get_last_generated_native_bundle(window)
    if report is None or bundle is None:
        raise ValueError(
            "Web AI correction requires a native Heuristic or Local AI plan and analysis evidence."
        )
    correction_context = context.to_dict()
    correction_context["instruction"] = context.prompt_text()
    blocked_plan = materialize_workbench_owned_plan(window)
    to_dict = getattr(blocked_plan, "to_dict", None)
    if callable(to_dict):
        correction_context["blocked_workbench_plan"] = to_dict()
    return build_comprehensive_web_ai_planning_prompt(
        report,
        blocked_plan,
        list(getattr(blocked_plan, "docstring_proposals", ()) or bundle.docstring_proposals),
        local_ai_summary={
            "status": "workbench_blocker_correction_requested",
            "workbench_failure_context": correction_context,
        },
        import_contract=build_web_ai_import_contract(context.active_project_root),
        base_version_name=str(getattr(window, "_large_file_refactor_selected_version", "") or bundle.version_name),
    )


def _settings_from_plan(plan: Any) -> PlannerSettings:
    values = dict(getattr(plan, "settings", {}) or {})
    allowed = {
        "ideal_physical_lines",
        "maximum_physical_lines",
        "minimum_helper_physical_lines",
        "preserve_public_facade",
        "generate_missing_docstrings",
        "rewrite_project_imports",
        "import_migration_preview",
        "use_local_llm",
        "preview_only",
        "create_patch_only_after_validation",
    }
    return PlannerSettings(**{key: value for key, value in values.items() if key in allowed})


def _correction_loaded_message(
    *,
    route: str,
    context: WorkbenchStageCorrectionContext,
    plan_status: str,
    extra: str,
) -> str:
    parts = [
        route + " correction candidate loaded into Workbench ownership.",
        "Blocked stage: " + context.stage,
        "Observed status: " + context.status,
        "Plan status after correction: " + (plan_status or "<missing>"),
        "Sequential downstream evidence was invalidated intentionally.",
        "Run Dependency and Scope Readiness again, then advance one PASS at a time.",
        "The next phase remains disabled until deterministic evidence proves readiness.",
    ]
    if extra:
        parts.append("Detail: " + extra)
    return "\n".join(parts)

def _build_aqr_heuristic_candidate(
    *,
    plan: Any,
    context: WorkbenchStageCorrectionContext,
    progress_callback: Callable[[str], None] | None,
) -> HeuristicWorkbenchCorrectionCandidate:
    """Build one deterministic AQR-informed plan candidate without claiming AQR PASS."""
    if plan is None or not context.target_file:
        return HeuristicWorkbenchCorrectionCandidate(
            False,
            "AQR Heuristic correction blocked: Workbench plan or target file is missing.",
        )
    try:
        if progress_callback is not None:
            progress_callback("AQR_FEEDBACK_ANALYZE_SOURCE")
        report = analyze_python_file(context.target_file)
        settings = _settings_from_plan(plan)
        strategy = _aqr_strategy(context, plan)
        corrected_plan = build_split_plan(
            report,
            settings,
            source_path=None,
            preferred_strategy=strategy,
        )
        if str(getattr(corrected_plan, "status", "")) == "blocked":
            details = "; ".join(getattr(corrected_plan, "validation_blockers", ()) or ())
            return HeuristicWorkbenchCorrectionCandidate(
                False, "AQR Heuristic candidate remained blocked: " + (details or "UNKNOWN_PLAN_BLOCKER")
            )
        proposals = build_docstring_proposals(report, corrected_plan)
        corrected_plan = attach_docstring_proposals_to_plan(corrected_plan, proposals)
    except Exception as exc:
        return HeuristicWorkbenchCorrectionCandidate(
            False,
            "AQR Heuristic correction failed without opening any gate: " + str(exc),
        )
    if not plans_materially_different(plan, corrected_plan):
        return HeuristicWorkbenchCorrectionCandidate(
            False,
            "AQR Heuristic correction produced no material plan change. The current blocker remains active and all correction routes remain reusable.",
            report=report,
            corrected_plan=corrected_plan,
            proposals=tuple(proposals),
            replay=None,
            strategy=strategy,
            settings_label="aqr_feedback_bounded",
            attempts=("AQR_CONTEXT_APPLIED_NO_MATERIAL_CHANGE",),
        )
    return HeuristicWorkbenchCorrectionCandidate(
        True,
        "AQR-informed materially changed deterministic candidate built. AQR PASS is not claimed; full sequential rerun remains mandatory.",
        report=report,
        corrected_plan=corrected_plan,
        proposals=tuple(proposals),
        replay=None,
        strategy=strategy,
        settings_label="aqr_feedback_bounded",
        attempts=("AQR_CONTEXT_APPLIED",),
    )


def _apply_aqr_heuristic_candidate(
    window: object,
    context: WorkbenchStageCorrectionContext,
    candidate: HeuristicWorkbenchCorrectionCandidate,
) -> WorkbenchCorrectionResult:
    """Load one AQR-informed plan generation while keeping every downstream gate closed."""
    if not candidate.ok or candidate.corrected_plan is None:
        return WorkbenchCorrectionResult(False, "heuristic", candidate.message)
    window._large_file_refactor_last_analysis = candidate.report
    store_heuristic_version(
        window,
        candidate.corrected_plan,
        list(candidate.proposals),
    )
    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    intake, load_message = load_latest_snapshot_into_workbench(
        window,
        context.active_project_root,
    )
    if intake is None or not bool(getattr(intake, "ready_for_real_preview", False)):
        return WorkbenchCorrectionResult(
            False,
            "heuristic",
            "AQR-informed candidate existed, but Workbench reload was blocked. "
            + load_message,
        )
    note_aqr_correction_candidate(window, "heuristic")
    return WorkbenchCorrectionResult(
        True,
        "heuristic",
        "\n".join(
            [
                "AQR HEURISTIC CORRECTION CANDIDATE LOADED",
                "Observed blocked stage: ADVANCED_QUALITY_REVIEW",
                "Selected strategy: " + candidate.strategy,
                "No AQR PASS was synthesized or prevalidated.",
                "Downstream evidence was invalidated intentionally.",
                "Rerun Dependency Readiness, Real Preview, Structural Validation, and Advanced Quality Review in order.",
            ]
        ),
        intake=intake,
    )


def _aqr_strategy(
    context: WorkbenchStageCorrectionContext,
    plan: Any,
) -> str:
    failed_stages = {
        item.split(":", 2)[1]
        for item in context.blockers
        if item.startswith("AQR_STAGE:") and item.count(":") >= 2
    }
    blocking_rules = {
        item.split(":", 2)[1]
        for item in context.blockers
        if item.startswith("AQR_RULE:") and item.count(":") >= 2
    }
    if (
        "IMPORT_GRAPH" in failed_stages
        or "AQR_GRIMP_TOPOLOGY_DELTA" in blocking_rules
    ):
        return "dependency_dominant"
    if (
        "API_REVIEW" in failed_stages
        or "AQR_GRIFFE_PUBLIC_CONTRACT" in blocking_rules
    ):
        return "responsibility_dominant"
    return "balanced"

