# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_plan_intake.py
"""Plan intake gates for Workbench-owned Planner snapshots."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
from typing import Any

from .models import FEATURE_ID, SCHEMA_VERSION, ModuleAnalysisReport, RefactorPlan
from .workbench_plan_snapshot import WorkbenchPlanSnapshot

__all__ = [
    "WORKBENCH_FEATURE_ID",
    "WorkbenchPlanIntakeResult",
    "build_workbench_plan_intake",
    "recheck_workbench_source_hash",
]

WORKBENCH_FEATURE_ID = "architecture-review-large-file-refactor-workbench-intake-v1"
_REFERENCE_ROOTS = {".project_reference", "_project_reference"}
_PROTECTED_PARTS = {
    "project_freeze_after_update",
    "project_freeze_ledger",
    "project_error_memory",
    "show_project_to_AI",
    "_show_project_to_AI",
    "large_file_refactor_preview",
}


@dataclass(frozen=True)
class WorkbenchPlanIntakeResult:
    """Validated Workbench ownership result for one immutable snapshot."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    target_file: str
    source_content_hash: str
    current_source_content_hash: str
    source_hash_fresh: bool
    planner_status: str
    planner_candidate_verified: bool
    snapshot_hash: str = ""
    planner_handoff_hash: str = ""
    snapshot_integrity_valid: bool = False
    workbench_snapshot_owned: bool = False
    ready_for_real_preview: bool = False
    source_mutation_enabled: bool = False
    real_preview_generation_enabled: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_workbench_plan_intake(
    *,
    snapshot: WorkbenchPlanSnapshot | None,
    active_project_root: str,
) -> WorkbenchPlanIntakeResult:
    """Validate immutable snapshot ownership before Workbench execution."""

    root = _resolve_root(active_project_root)
    integrity = bool(snapshot and snapshot.integrity_valid())
    plan, analysis, materialize_blockers = _materialize(snapshot)
    target = _target(plan)
    current_hash = _hash_file(target) if target and target.is_file() else ""
    candidate_verified = _candidate_contains(
        target,
        snapshot.candidate_paths if snapshot else (),
    )
    blockers = list(materialize_blockers)
    blockers.extend(
        _blockers(
            snapshot,
            plan,
            analysis,
            root,
            target,
            current_hash,
            candidate_verified,
            integrity,
        )
    )
    unique_blockers = sorted(set(blockers))
    ready = not unique_blockers
    correction_only_owned = _correction_only_ownership_allowed(
        snapshot, unique_blockers
    )
    snapshot_owned = bool(snapshot and (ready or correction_only_owned))
    warnings = _warnings()
    if correction_only_owned:
        warnings.append("PLANNER_PLAN_OWNED_FOR_CORRECTION_ONLY")
    return WorkbenchPlanIntakeResult(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_FEATURE_ID,
        status=(
            "plan_intake_ready"
            if ready
            else "plan_intake_correction_ready"
            if correction_only_owned
            else "blocked"
        ),
        active_project_root=str(root),
        target_file=str(target) if target else "",
        source_content_hash=snapshot.source_content_hash if snapshot else "",
        current_source_content_hash=current_hash,
        source_hash_fresh=bool(
            snapshot and current_hash == snapshot.source_content_hash
        ),
        planner_status=snapshot.planner_status if snapshot else "missing",
        planner_candidate_verified=candidate_verified,
        snapshot_hash=snapshot.snapshot_hash if snapshot else "",
        planner_handoff_hash=(
            snapshot.planner_handoff_hash if snapshot else ""
        ),
        snapshot_integrity_valid=integrity,
        workbench_snapshot_owned=snapshot_owned,
        ready_for_real_preview=ready,
        source_mutation_enabled=False,
        real_preview_generation_enabled=False,
        checked_rules=_checked_rules(),
        blockers=unique_blockers,
        warnings=sorted(set(warnings)),
    )


def recheck_workbench_source_hash(
    intake: WorkbenchPlanIntakeResult,
) -> WorkbenchPlanIntakeResult:
    """Refresh source freshness without any Planner access."""

    target = Path(intake.target_file).resolve() if intake.target_file else None
    current_hash = _hash_file(target) if target and target.is_file() else ""
    blockers = list(intake.blockers)
    if not target or not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    elif current_hash != intake.source_content_hash:
        blockers.append("STALE_SOURCE")
    else:
        blockers = [
            item for item in blockers
            if item not in {"STALE_SOURCE", "TARGET_FILE_MISSING"}
        ]
    unique_blockers = sorted(set(blockers))
    ready = (
        not unique_blockers
        and intake.planner_candidate_verified
        and intake.snapshot_integrity_valid
        and intake.workbench_snapshot_owned
    )
    correction_only_owned = (
        intake.workbench_snapshot_owned
        and _correction_only_blockers(unique_blockers)
        and intake.planner_candidate_verified
        and intake.snapshot_integrity_valid
        and current_hash == intake.source_content_hash
    )
    return WorkbenchPlanIntakeResult(
        schema_version=intake.schema_version,
        feature_id=intake.feature_id,
        status=(
            "plan_intake_ready"
            if ready
            else "plan_intake_correction_ready"
            if correction_only_owned
            else "blocked"
        ),
        active_project_root=intake.active_project_root,
        target_file=intake.target_file,
        source_content_hash=intake.source_content_hash,
        current_source_content_hash=current_hash,
        source_hash_fresh=current_hash == intake.source_content_hash,
        planner_status=intake.planner_status,
        planner_candidate_verified=intake.planner_candidate_verified,
        snapshot_hash=intake.snapshot_hash,
        planner_handoff_hash=intake.planner_handoff_hash,
        snapshot_integrity_valid=intake.snapshot_integrity_valid,
        workbench_snapshot_owned=intake.workbench_snapshot_owned,
        ready_for_real_preview=ready,
        source_mutation_enabled=False,
        real_preview_generation_enabled=False,
        checked_rules=list(intake.checked_rules),
        blockers=unique_blockers,
        warnings=list(intake.warnings),
    )



def _correction_only_ownership_allowed(
    snapshot: WorkbenchPlanSnapshot | None,
    blockers: list[str],
) -> bool:
    """Allow ownership only for a safely bounded blocked-plan correction lane."""

    return bool(snapshot and _correction_only_blockers(blockers))


def _correction_only_blockers(blockers: list[str]) -> bool:
    """Return whether PLANNER_PLAN_BLOCKED is the sole intake blocker."""

    return set(blockers) == {"PLANNER_PLAN_BLOCKED"}

def _materialize(
    snapshot: WorkbenchPlanSnapshot | None,
) -> tuple[RefactorPlan | None, ModuleAnalysisReport | None, list[str]]:
    if snapshot is None:
        return None, None, ["WORKBENCH_PLAN_SNAPSHOT_MISSING"]
    if not snapshot.integrity_valid():
        return None, None, ["WORKBENCH_SNAPSHOT_HASH_MISMATCH"]
    try:
        return snapshot.materialize_plan(), snapshot.materialize_analysis(), []
    except (TypeError, ValueError, KeyError):
        return None, None, ["WORKBENCH_SNAPSHOT_MATERIALIZATION_FAILED"]


def _blockers(
    snapshot: WorkbenchPlanSnapshot | None,
    plan: RefactorPlan | None,
    analysis: ModuleAnalysisReport | None,
    root: Path,
    target: Path | None,
    current_hash: str,
    candidate_verified: bool,
    integrity: bool,
) -> list[str]:
    blockers: list[str] = []
    if snapshot is None:
        blockers.append("WORKBENCH_PLAN_SNAPSHOT_MISSING")
    elif not integrity:
        blockers.append("WORKBENCH_SNAPSHOT_HASH_MISMATCH")
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    if analysis is None:
        blockers.append("PLANNER_ANALYSIS_MISSING")
    if plan is not None and plan.status == "blocked":
        blockers.append("PLANNER_PLAN_BLOCKED")
    if not target:
        blockers.append("TARGET_FILE_MISSING")
        return blockers
    blockers.extend(_path_blockers(root, target))
    if not candidate_verified:
        blockers.append("TARGET_NOT_IN_WARNING_MODULE_TOO_LARGE_QUEUE")
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    elif snapshot is not None and current_hash != snapshot.source_content_hash:
        blockers.append("STALE_SOURCE")
    if plan is not None and plan.feature_id != FEATURE_ID:
        blockers.append("UNSUPPORTED_PLANNER_FEATURE_ID")
    if analysis is not None and plan is not None:
        if analysis.source_content_hash != plan.source_content_hash:
            blockers.append("ANALYSIS_PLAN_HASH_MISMATCH")
    return blockers


def _path_blockers(root: Path, target: Path) -> list[str]:
    blockers: list[str] = []
    if not _is_relative_to(target, root):
        blockers.append("TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT")
    lowered = {part.lower() for part in target.parts}
    if lowered & _REFERENCE_ROOTS:
        blockers.append("TARGET_INSIDE_REFERENCE_ROOT")
    for part in _PROTECTED_PARTS:
        if part.lower() in lowered:
            blockers.append("TARGET_INSIDE_PROTECTED_OUTPUT_ROOT")
    if target.suffix != ".py":
        blockers.append("TARGET_NOT_PYTHON_SOURCE")
    return blockers


def _warnings() -> list[str]:
    return [
        "WORKBENCH_OWNS_IMMUTABLE_PLAN_SNAPSHOT",
        "NO_DOWNSTREAM_PLANNER_PRIVATE_STATE_READ",
        "SOURCE_MUTATION_DISABLED_DURING_INTAKE",
        "PLANNER_WARNING_QUEUE_VERIFIED_ONLY_AT_EXPLICIT_LOAD_BOUNDARY",
        "SHIELDING_LOGIC_BLOCKS_CROSS_MODULE_CONTAMINATION",
    ]


def _checked_rules() -> list[str]:
    return [
        "public_planner_handoff_required",
        "handoff_hash_must_validate",
        "workbench_snapshot_hash_must_validate",
        "planner_analysis_required",
        "target_must_be_in_loaded_warning_candidate_snapshot",
        "selected_source_hash_must_be_fresh",
        "target_inside_active_project_root",
        "reference_roots_blocked",
        "generated_and_support_roots_blocked",
        "python_source_only",
        "workbench_owns_downstream_plan_snapshot",
        "no_automatic_planner_reload_from_workbench_actions",
        "shielding_logic_active",
    ]


def _target(plan: RefactorPlan | None) -> Path | None:
    if plan is None or not plan.target_file:
        return None
    try:
        return Path(plan.target_file).resolve()
    except OSError:
        return None


def _candidate_contains(
    target: Path | None,
    candidate_paths: tuple[str, ...],
) -> bool:
    if target is None:
        return False
    target_text = str(target.resolve())
    return any(
        raw and str(Path(raw).resolve()) == target_text
        for raw in candidate_paths
    )


def _hash_file(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _resolve_root(active_project_root: str) -> Path:
    text = str(active_project_root or "").strip()
    return Path(text).resolve() if text else Path.cwd().resolve()


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
