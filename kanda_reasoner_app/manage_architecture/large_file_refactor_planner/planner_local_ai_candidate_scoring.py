# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_candidate_scoring.py
"""Deterministic scoring for validated Local AI architecture candidates."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .dependency_clusterer import DependencyCluster
from .models import MIN_HELPER_PHYSICAL_LINES, ModuleAnalysisReport, PlannerSettings, RefactorPlan
from .planner_candidate_quality import evaluate_candidate_quality

__all__ = ["LocalAICandidateScore", "score_local_ai_candidate"]


@dataclass(frozen=True)
class LocalAICandidateScore:
    """Explainable deterministic quality score for one Local AI candidate."""

    candidate_id: str
    strategy: str
    status: str
    total_score: float
    size_score: float
    module_economy_score: float
    change_cost_score: float
    responsibility_cohesion_score: float
    topology_score: float
    mixed_responsibility_penalty: float
    facade_back_reference_penalty: float
    helper_count: int
    corrections_applied: int
    blockers: list[str] = field(default_factory=list)
    quality_evidence: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready tournament score evidence."""
        return asdict(self)


def score_local_ai_candidate(
    report: ModuleAnalysisReport,
    plan: RefactorPlan,
    *,
    candidate_id: str,
    strategy: str,
    baseline_helper_count: int,
    corrections_applied: int,
) -> LocalAICandidateScore:
    """Score one deterministically revalidated candidate architecture."""
    settings = _settings_from_plan(plan)
    helpers = [module for module in plan.proposed_modules if module.role != "public_facade"]
    clusters = [
        DependencyCluster(
            cluster_id=module.filename,
            role=module.role,
            symbols=list(module.symbols),
            estimated_lines=module.estimated_lines,
            risk_flags=list(module.risk_flags),
        )
        for module in helpers
    ]
    facade_symbols = set(report.public_api_symbols)
    facade_symbols.update(
        symbol.name
        for symbol in report.symbols
        if set(symbol.risk_flags) & {"GLOBAL_STATE", "DECORATOR_RISK", "NESTED_SYMBOL_CLUSTER"}
    )
    quality = evaluate_candidate_quality(report, settings, clusters, facade_symbols)
    blockers = list(plan.validation_blockers)
    blockers.extend(str(item) for item in quality.topology.get("blockers", []))
    blockers = sorted(set(blockers))
    status = "valid" if plan.status == "planned" and not blockers else "blocked"
    size_score = _size_score(plan, settings)
    economy = _module_economy_score(len(helpers), baseline_helper_count)
    change_cost = 1.0 / (1.0 + max(0, corrections_applied))
    total = (
        0.20 * size_score
        + 0.10 * economy
        + 0.10 * change_cost
        + 0.30 * quality.responsibility_cohesion_score
        + 0.30 * quality.topology_score
        - 0.15 * quality.mixed_responsibility_penalty
    )
    return LocalAICandidateScore(
        candidate_id=candidate_id,
        strategy=strategy,
        status=status,
        total_score=round(total, 6),
        size_score=round(size_score, 6),
        module_economy_score=round(economy, 6),
        change_cost_score=round(change_cost, 6),
        responsibility_cohesion_score=quality.responsibility_cohesion_score,
        topology_score=quality.topology_score,
        mixed_responsibility_penalty=quality.mixed_responsibility_penalty,
        facade_back_reference_penalty=quality.facade_back_reference_penalty,
        helper_count=len(helpers),
        corrections_applied=max(0, corrections_applied),
        blockers=blockers,
        quality_evidence=quality.to_dict(),
    )


def _settings_from_plan(plan: RefactorPlan) -> PlannerSettings:
    allowed = set(PlannerSettings.__dataclass_fields__)
    values = {key: value for key, value in plan.settings.items() if key in allowed}
    return PlannerSettings(**values)


def _size_score(plan: RefactorPlan, settings: PlannerSettings) -> float:
    helpers = [module for module in plan.proposed_modules if module.role != "public_facade"]
    if not helpers:
        return 1.0
    minimum = max(MIN_HELPER_PHYSICAL_LINES, settings.minimum_helper_physical_lines)
    values: list[float] = []
    for module in helpers:
        lines = module.estimated_lines
        if lines < minimum or lines > settings.maximum_physical_lines:
            values.append(0.0)
        elif lines <= settings.ideal_physical_lines:
            values.append(min(1.0, lines / max(1, settings.ideal_physical_lines)))
        else:
            span = max(1, settings.maximum_physical_lines - settings.ideal_physical_lines)
            values.append(max(0.0, 1.0 - (lines - settings.ideal_physical_lines) / span))
    return sum(values) / len(values)


def _module_economy_score(current_count: int, baseline_count: int) -> float:
    if baseline_count <= 1:
        return 1.0 if current_count <= baseline_count else 0.5
    delta = baseline_count - current_count
    return max(0.0, min(1.0, 0.5 + 0.5 * delta / (baseline_count - 1)))
