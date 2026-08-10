"""Feedback-aware Heuristic candidate search and stage replay for Workbench recovery."""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
from types import SimpleNamespace
from typing import Any, Callable

from .ast_analysis import analyze_python_file
from .cst_real_preview_writer import build_and_write_real_preview
from .docstring_planner import build_docstring_proposals
from .models import PlannerSettings
from .planner_bounded_refinement import attach_docstring_proposals_to_plan
from .planner_workbench_handoff import export_latest_planner_workbench_handoff
from .real_preview_structural_validator import validate_real_preview_structure
from .split_planner import build_split_plan
from .workbench_completion_workflow import prepare_completion_evidence
from .workbench_dependency_readiness import build_workbench_dependency_readiness
from .workbench_plan_intake import build_workbench_plan_intake
from .workbench_plan_snapshot import build_workbench_plan_snapshot
from .workbench_preflight_backup_readiness import (
    build_and_write_preflight_backup_readiness,
)
from .workbench_project_support_paths import preview_runs_root
from .workbench_source_payload_builder import build_and_write_source_apply_payload
from .workbench_stage_correction_context import WorkbenchStageCorrectionContext

__all__ = [
    "HeuristicCorrectionSearchResult",
    "WorkbenchCorrectionReplayEvidence",
    "search_feedback_aware_heuristic_correction",
]

_STAGE_ORDER = (
    "PLAN_INTAKE",
    "DEPENDENCY_READINESS",
    "REAL_PREVIEW",
    "STRUCTURAL_VALIDATION",
    "PREFLIGHT_BACKUP",
    "SOURCE_PAYLOAD",
    "COMPLETION_EVIDENCE",
)

ProgressCallback = Callable[[str], None] | None


@dataclass(frozen=True)
class WorkbenchCorrectionReplayEvidence:
    """Non-mutating evidence replay for one candidate through the blocked target stage."""

    target_stage: str
    passed: bool
    reached_stage: str
    strategy: str
    settings_label: str
    snapshot: Any = None
    intake: Any = None
    dependency_readiness: Any = None
    real_preview: Any = None
    structural_validation: Any = None
    preflight_backup: Any = None
    source_payload: Any = None
    completion_evidence: Any = None
    blockers: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()


@dataclass(frozen=True)
class HeuristicCorrectionSearchResult:
    """Best passing feedback-aware candidate, or bounded diagnostics when none passes."""

    ok: bool
    message: str
    report: Any = None
    corrected_plan: Any = None
    proposals: tuple[Any, ...] = ()
    replay: WorkbenchCorrectionReplayEvidence | None = None
    strategy: str = ""
    settings_label: str = ""
    attempts: tuple[str, ...] = ()


def search_feedback_aware_heuristic_correction(
    *,
    plan: Any,
    context: WorkbenchStageCorrectionContext,
    progress_callback: ProgressCallback = None,
) -> HeuristicCorrectionSearchResult:
    """Search bounded deterministic variants and commit only a target-stage PASS candidate."""
    if plan is None or not context.target_file:
        return HeuristicCorrectionSearchResult(
            False,
            "Heuristic correction blocked: Workbench plan or target file is missing.",
        )
    _emit(progress_callback, "ANALYZE_PROJECT_SOURCE")
    try:
        report = analyze_python_file(context.target_file)
        base_settings = _settings_from_plan(plan)
    except Exception as exc:
        return HeuristicCorrectionSearchResult(False, "Heuristic analysis failed: " + str(exc))

    attempts: list[str] = []
    seen: set[str] = set()
    candidates = [("current_replay", "current", plan, tuple(getattr(plan, "docstring_proposals", ()) or ()))]

    for settings_label, settings in _settings_variants(base_settings, context):
        for strategy in _strategy_order(plan, context):
            _emit(progress_callback, "BUILD_CANDIDATE:" + settings_label + ":" + strategy)
            try:
                candidate_plan = build_split_plan(
                    report,
                    settings,
                    source_path=None,
                    preferred_strategy=strategy,
                )
                proposals = build_docstring_proposals(report, candidate_plan)
                candidate_plan = attach_docstring_proposals_to_plan(candidate_plan, proposals)
            except Exception as exc:
                attempts.append(f"{settings_label}/{strategy}:BUILD_FAILED:{exc}")
                continue
            candidates.append((settings_label, strategy, candidate_plan, tuple(proposals)))

    for settings_label, strategy, candidate_plan, proposals in candidates:
        fingerprint = _plan_fingerprint(candidate_plan)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        _emit(progress_callback, "REPLAY_TARGET_STAGE:" + strategy)
        replay = _replay_candidate(
            plan=candidate_plan,
            report=report,
            context=context,
            strategy=strategy,
            settings_label=settings_label,
            fingerprint=fingerprint,
        )
        attempts.append(_attempt_summary(replay))
        if replay.passed:
            return HeuristicCorrectionSearchResult(
                True,
                (
                    "Heuristic correction found a candidate that deterministically replays "
                    + context.stage
                    + " to PASS. The candidate may now replace Workbench ownership."
                ),
                report=report,
                corrected_plan=candidate_plan,
                proposals=tuple(proposals),
                replay=replay,
                strategy=strategy,
                settings_label=settings_label,
                attempts=tuple(attempts),
            )

    return HeuristicCorrectionSearchResult(
        False,
        (
            "Heuristic correction found no bounded deterministic candidate that makes "
            + context.stage
            + " PASS. The current blocked Workbench snapshot was preserved; use Local AI "
              "or Web AI correction with the exact blocker context. Attempts: "
            + " | ".join(attempts[-8:])
        ),
        report=report,
        attempts=tuple(attempts),
    )


def _replay_candidate(
    *,
    plan: Any,
    report: Any,
    context: WorkbenchStageCorrectionContext,
    strategy: str,
    settings_label: str,
    fingerprint: str,
) -> WorkbenchCorrectionReplayEvidence:
    """Replay deterministic no-source-mutation phases through the original blocked stage."""
    target_stage = context.stage
    diagnostics: list[str] = []
    try:
        holder = SimpleNamespace(
            _large_file_refactor_last_plan=plan,
            _large_file_refactor_last_analysis=report,
            _large_file_refactor_planner_candidates=[SimpleNamespace(path=context.target_file)],
        )
        handoff = export_latest_planner_workbench_handoff(holder)
        snapshot = build_workbench_plan_snapshot(handoff)
        intake = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=context.active_project_root,
        )
    except Exception as exc:
        return _blocked_replay(target_stage, "PLAN_INTAKE", strategy, settings_label, [str(exc)])

    if not _stage_passed("PLAN_INTAKE", intake):
        return _replay_result(target_stage, "PLAN_INTAKE", strategy, settings_label, snapshot=snapshot, intake=intake)
    if target_stage == "PLAN_INTAKE":
        return _replay_result(target_stage, "PLAN_INTAKE", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake)

    dependency = build_workbench_dependency_readiness(intake)
    if not _stage_passed("DEPENDENCY_READINESS", dependency):
        return _replay_result(target_stage, "DEPENDENCY_READINESS", strategy, settings_label, snapshot=snapshot, intake=intake, dependency_readiness=dependency)
    if target_stage == "DEPENDENCY_READINESS":
        return _replay_result(target_stage, "DEPENDENCY_READINESS", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake, dependency_readiness=dependency)

    preview_root = preview_runs_root(context.active_project_root) / (
        "heuristic_correction_" + fingerprint[:16]
    )
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=dependency,
        active_project_root=context.active_project_root,
        preview_root=str(preview_root),
    )
    if not _stage_passed("REAL_PREVIEW", preview):
        return _replay_result(target_stage, "REAL_PREVIEW", strategy, settings_label, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview)
    if target_stage == "REAL_PREVIEW":
        return _replay_result(target_stage, "REAL_PREVIEW", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview)

    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=context.active_project_root,
    )
    if not _stage_passed("STRUCTURAL_VALIDATION", structural):
        return _replay_result(target_stage, "STRUCTURAL_VALIDATION", strategy, settings_label, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural)
    if target_stage == "STRUCTURAL_VALIDATION":
        return _replay_result(target_stage, "STRUCTURAL_VALIDATION", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural)

    preflight = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=context.active_project_root,
    )
    if not _stage_passed("PREFLIGHT_BACKUP", preflight):
        return _replay_result(target_stage, "PREFLIGHT_BACKUP", strategy, settings_label, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural, preflight_backup=preflight)
    if target_stage == "PREFLIGHT_BACKUP":
        return _replay_result(target_stage, "PREFLIGHT_BACKUP", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural, preflight_backup=preflight)

    payload = build_and_write_source_apply_payload(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        preflight_backup=preflight,
        active_project_root=context.active_project_root,
    )
    if not _stage_passed("SOURCE_PAYLOAD", payload):
        return _replay_result(target_stage, "SOURCE_PAYLOAD", strategy, settings_label, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural, preflight_backup=preflight, source_payload=payload)
    if target_stage == "SOURCE_PAYLOAD":
        return _replay_result(target_stage, "SOURCE_PAYLOAD", strategy, settings_label, passed=True, snapshot=snapshot, intake=intake, dependency_readiness=dependency, real_preview=preview, structural_validation=structural, preflight_backup=preflight, source_payload=payload)

    if target_stage == "COMPLETION_EVIDENCE":
        try:
            completion = prepare_completion_evidence(
                snapshot=snapshot,
                preview=preview,
                preflight=preflight,
                source_payload=payload,
                active_project_root=context.active_project_root,
            )
        except Exception as exc:
            diagnostics.append(str(exc))
            completion = None
        return _replay_result(
            target_stage,
            "COMPLETION_EVIDENCE" if completion is not None else "SOURCE_PAYLOAD",
            strategy,
            settings_label,
            passed=completion is not None,
            snapshot=snapshot,
            intake=intake,
            dependency_readiness=dependency,
            real_preview=preview,
            structural_validation=structural,
            preflight_backup=preflight,
            source_payload=payload,
            completion_evidence=completion,
            diagnostics=tuple(diagnostics),
        )

    return _blocked_replay(target_stage, "UNSUPPORTED", strategy, settings_label, ["UNSUPPORTED_TARGET_STAGE"])


def _settings_variants(base: PlannerSettings, context: WorkbenchStageCorrectionContext) -> list[tuple[str, PlannerSettings]]:
    """Return bounded hard-policy-preserving variants influenced by blocker context."""
    variants = [("original_settings", replace(base, use_local_llm=False))]
    ideals = [320, 260]
    if any("TOO_LARGE" in item for item in context.blockers):
        ideals = [260, 320]
    for ideal in ideals:
        bounded = max(180, min(int(ideal), int(base.maximum_physical_lines) - 20))
        variants.append((f"ideal_{bounded}", replace(base, ideal_physical_lines=bounded, use_local_llm=False)))
    unique: list[tuple[str, PlannerSettings]] = []
    seen: set[str] = set()
    for label, settings in variants:
        key = json.dumps(settings.to_dict(), sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append((label, settings))
    return unique


def _strategy_order(plan: Any, context: WorkbenchStageCorrectionContext) -> tuple[str, ...]:
    """Order deterministic strategies from blocker semantics and avoid blind same-plan replay."""
    current = str(
        ((getattr(plan, "import_migration", {}) or {}).get("heuristic_candidate_selection", {}) or {}).get(
            "selected_strategy", ""
        )
    )
    blockers = " ".join(context.blockers).upper()
    if "CYCLE" in blockers or "DEPENDENCY" in blockers or "IMPORT" in blockers:
        preferred = ["dependency_dominant", "balanced", "responsibility_dominant"]
    elif "FACADE" in blockers or "SYMBOL" in blockers or "RESPONSIBILITY" in blockers:
        preferred = ["responsibility_dominant", "balanced", "dependency_dominant"]
    else:
        preferred = ["balanced", "responsibility_dominant", "dependency_dominant"]
    return tuple([item for item in preferred if item != current] + ([current] if current in preferred else []))


def _settings_from_plan(plan: Any) -> PlannerSettings:
    values = dict(getattr(plan, "settings", {}) or {})
    allowed = {field for field in PlannerSettings.__dataclass_fields__}
    values = {key: value for key, value in values.items() if key in allowed}
    values["use_local_llm"] = False
    return PlannerSettings(**values)


def _stage_passed(stage: str, result: Any) -> bool:
    status = str(getattr(result, "status", "") or "")
    if stage == "PLAN_INTAKE":
        return bool(status == "plan_intake_ready" and getattr(result, "ready_for_real_preview", False))
    if stage == "DEPENDENCY_READINESS":
        return bool(status == "dependency_readiness_ready" and getattr(result, "ready_for_real_preview_writer", False))
    if stage == "REAL_PREVIEW":
        return bool(status == "real_preview_written" and getattr(result, "files", None) and not getattr(result, "blockers", ()))
    if stage == "STRUCTURAL_VALIDATION":
        return bool(status.startswith("passed") and getattr(result, "structural_status", "") != "STRUCTURAL_FAIL" and not getattr(result, "blockers", ()))
    if stage == "PREFLIGHT_BACKUP":
        return status == "preflight_backup_ready"
    if stage == "SOURCE_PAYLOAD":
        return status == "source_apply_payload_ready"
    if stage == "COMPLETION_EVIDENCE":
        return result is not None
    return False


def _replay_result(target_stage: str, reached_stage: str, strategy: str, settings_label: str, *, passed: bool = False, diagnostics: tuple[str, ...] = (), **kwargs: Any) -> WorkbenchCorrectionReplayEvidence:
    result = kwargs.get(_stage_field(reached_stage))
    blockers = tuple(str(item) for item in (getattr(result, "blockers", ()) or ()))
    return WorkbenchCorrectionReplayEvidence(
        target_stage=target_stage,
        passed=passed,
        reached_stage=reached_stage,
        strategy=strategy,
        settings_label=settings_label,
        blockers=blockers,
        diagnostics=diagnostics,
        **kwargs,
    )


def _blocked_replay(target_stage: str, reached_stage: str, strategy: str, settings_label: str, blockers: list[str]) -> WorkbenchCorrectionReplayEvidence:
    return WorkbenchCorrectionReplayEvidence(
        target_stage=target_stage,
        passed=False,
        reached_stage=reached_stage,
        strategy=strategy,
        settings_label=settings_label,
        blockers=tuple(blockers),
    )


def _stage_field(stage: str) -> str:
    return {
        "PLAN_INTAKE": "intake",
        "DEPENDENCY_READINESS": "dependency_readiness",
        "REAL_PREVIEW": "real_preview",
        "STRUCTURAL_VALIDATION": "structural_validation",
        "PREFLIGHT_BACKUP": "preflight_backup",
        "SOURCE_PAYLOAD": "source_payload",
        "COMPLETION_EVIDENCE": "completion_evidence",
    }.get(stage, "intake")


def _attempt_summary(replay: WorkbenchCorrectionReplayEvidence) -> str:
    return (
        replay.settings_label
        + "/"
        + replay.strategy
        + ":reached="
        + replay.reached_stage
        + ":target_pass="
        + ("yes" if replay.passed else "no")
        + (":blockers=" + ",".join(replay.blockers[:3]) if replay.blockers else "")
    )


def _plan_fingerprint(plan: Any) -> str:
    to_dict = getattr(plan, "to_dict", None)
    payload = to_dict() if callable(to_dict) else {"repr": repr(plan)}
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _emit(callback: ProgressCallback, phase: str) -> None:
    if callback is not None:
        callback(str(phase))
