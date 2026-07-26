# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_readiness.py
"""Workbench dependency-readiness gate before real LibCST preview writing."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION
from .symbol_dependency_builder import SymbolDependencyReport, build_symbol_dependency_report
from .workbench_plan_intake import WORKBENCH_FEATURE_ID, WorkbenchPlanIntakeResult

__all__ = [
    "WorkbenchDependencyReadinessResult",
    "build_workbench_dependency_readiness",
]


@dataclass(frozen=True)
class WorkbenchDependencyReadinessResult:
    """Read-only readiness report before real code movement."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    dependency_report: SymbolDependencyReport | None = None
    ready_for_real_preview_writer: bool = False
    source_mutation_enabled: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready readiness dictionary."""
        data = asdict(self)
        if self.dependency_report is not None:
            data["dependency_report"] = self.dependency_report.to_dict()
        return data


def build_workbench_dependency_readiness(
    intake: WorkbenchPlanIntakeResult | None,
) -> WorkbenchDependencyReadinessResult:
    """Build a read-only dependency readiness report from a valid intake."""
    if intake is None:
        return _blocked("", "", ["WORKBENCH_INTAKE_MISSING"])
    blockers = _intake_blockers(intake)
    if blockers:
        return _blocked(intake.target_file, intake.source_content_hash, blockers)
    report = build_symbol_dependency_report(Path(intake.target_file))
    blockers = list(report.blockers)
    warnings = list(report.warnings)
    ready = not blockers
    return WorkbenchDependencyReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_FEATURE_ID,
        status="dependency_readiness_ready" if ready else "blocked",
        target_file=intake.target_file,
        source_content_hash=intake.source_content_hash,
        dependency_report=report,
        ready_for_real_preview_writer=ready,
        source_mutation_enabled=False,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings + _stable_warnings())),
    )


def _blocked(
    target_file: str,
    source_hash: str,
    blockers: list[str],
) -> WorkbenchDependencyReadinessResult:
    """Return a blocked readiness result."""
    return WorkbenchDependencyReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_FEATURE_ID,
        status="blocked",
        target_file=target_file,
        source_content_hash=source_hash,
        dependency_report=None,
        ready_for_real_preview_writer=False,
        source_mutation_enabled=False,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_stable_warnings(),
    )


def _intake_blockers(intake: WorkbenchPlanIntakeResult) -> list[str]:
    """Return blockers inherited from the Workbench intake gate."""
    blockers = list(intake.blockers)
    if not intake.ready_for_real_preview:
        blockers.append("INTAKE_NOT_READY_FOR_DEPENDENCY_ANALYSIS")
    if not intake.source_hash_fresh:
        blockers.append("STALE_SOURCE")
    if not intake.planner_candidate_verified:
        blockers.append("TARGET_NOT_IN_WARNING_MODULE_TOO_LARGE_QUEUE")
    return sorted(set(blockers))


def _checked_rules() -> list[str]:
    """Return rule labels checked by dependency readiness."""
    return [
        "valid_workbench_intake_required",
        "source_hash_fresh_before_dependency_analysis",
        "ast_symbol_dependency_graph_built_read_only",
        "global_mutation_and_nonlocal_risks_block_real_preview",
        "decorator_type_hint_and_dynamic_namespace_risks_reported",
        "source_mutation_disabled",
        "shielding_logic_active",
    ]


def _stable_warnings() -> list[str]:
    """Return stable warnings for this read-only train."""
    return [
        "DEPENDENCY_READINESS_ONLY_NO_CST_MOVEMENT",
        "REAL_PREVIEW_WRITER_REQUIRES_SEPARATE_PREVIEW_ONLY_GATE",
        "SOURCE_MUTATION_DISABLED",
    ]
