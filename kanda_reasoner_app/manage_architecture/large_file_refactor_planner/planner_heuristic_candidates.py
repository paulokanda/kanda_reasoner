# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_heuristic_candidates.py
"""Deterministic candidate generation and ranking for heuristic split planning."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace

from .dependency_clusterer import DependencyCluster
from .models import (
    MIN_HELPER_PHYSICAL_LINES,
    ModuleAnalysisReport,
    PlannerSettings,
    RefactorSymbol,
)
from .planner_candidate_quality import evaluate_candidate_quality
from .planner_git_cochange import GitCochangeEvidence
from .planner_symbol_affinity import ClusterAffinity, cluster_affinity

__all__ = [
    "HeuristicCandidate",
    "HeuristicCandidateSelection",
    "build_ranked_heuristic_candidates",
]


@dataclass(frozen=True)
class HeuristicCandidate:
    """One deterministic helper-clustering candidate and its score evidence."""

    candidate_id: str
    strategy: str
    clusters: list[DependencyCluster]
    status: str
    total_score: float
    size_score: float
    fragmentation_score: float
    affinity_score: float
    module_economy_score: float
    responsibility_cohesion_score: float
    topology_score: float
    mixed_responsibility_penalty: float
    facade_back_reference_penalty: float
    historical_cochange_score: float
    quality_evidence: dict[str, object] = field(default_factory=dict)
    merge_evidence: list[dict[str, object]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready candidate record."""
        data = asdict(self)
        data["clusters"] = [cluster.to_dict() for cluster in self.clusters]
        return data


@dataclass(frozen=True)
class HeuristicCandidateSelection:
    """Ranked deterministic candidates and the selected architecture."""

    selected_candidate_id: str
    selected_strategy: str
    candidates: list[HeuristicCandidate]

    @property
    def selected_clusters(self) -> list[DependencyCluster]:
        """Return clusters from the selected candidate."""
        for candidate in self.candidates:
            if candidate.candidate_id == self.selected_candidate_id:
                return list(candidate.clusters)
        return []

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready selection evidence."""
        return {
            "selected_candidate_id": self.selected_candidate_id,
            "selected_strategy": self.selected_strategy,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }


def build_ranked_heuristic_candidates(
    report: ModuleAnalysisReport,
    settings: PlannerSettings,
    base_clusters: list[DependencyCluster],
    git_history: GitCochangeEvidence | None = None,
) -> HeuristicCandidateSelection:
    """Generate, score, and select deterministic architecture candidates."""
    symbol_by_name = {symbol.name: symbol for symbol in report.symbols}
    strategies = (
        ("dependency_dominant", 0.55),
        ("balanced", 0.30),
        ("responsibility_dominant", 0.20),
    )
    candidates = [
        _build_candidate(
            report,
            settings,
            base_clusters,
            symbol_by_name,
            strategy,
            threshold,
            git_history,
        )
        for strategy, threshold in strategies
    ]
    strategy_priority = {
        "balanced": 3,
        "responsibility_dominant": 2,
        "dependency_dominant": 1,
    }
    ranked = sorted(
        candidates,
        key=lambda item: (
            item.status == "valid",
            item.total_score,
            strategy_priority.get(item.strategy, 0),
            -len(item.clusters),
        ),
        reverse=True,
    )
    selected = ranked[0]
    return HeuristicCandidateSelection(
        selected_candidate_id=selected.candidate_id,
        selected_strategy=selected.strategy,
        candidates=ranked,
    )


def _build_candidate(
    report: ModuleAnalysisReport,
    settings: PlannerSettings,
    base_clusters: list[DependencyCluster],
    symbol_by_name: dict[str, RefactorSymbol],
    strategy: str,
    threshold: float,
    git_history: GitCochangeEvidence | None,
) -> HeuristicCandidate:
    """Build one candidate by repairing tiny clusters through bounded merges."""
    clusters = [_copy_cluster(cluster) for cluster in base_clusters]
    merge_evidence: list[dict[str, object]] = []
    while _tiny_clusters(clusters, settings):
        proposal = _best_tiny_merge(
            report,
            settings,
            clusters,
            symbol_by_name,
            strategy,
            threshold,
            git_history,
        )
        if proposal is None:
            break
        left_index, right_index, affinity = proposal
        left = clusters[left_index]
        right = clusters[right_index]
        merged = _merge_clusters(left, right, symbol_by_name)
        evidence = affinity.to_dict()
        evidence.update(
            {
                "strategy": strategy,
                "source_clusters": [left.cluster_id, right.cluster_id],
                "result_cluster": merged.cluster_id,
                "result_estimated_lines": merged.estimated_lines,
            }
        )
        merge_evidence.append(evidence)
        clusters = [
            cluster
            for index, cluster in enumerate(clusters)
            if index not in {left_index, right_index}
        ]
        clusters.append(merged)
        clusters.sort(key=lambda item: _cluster_start(item, symbol_by_name))

    blockers = _candidate_blockers(clusters, settings)
    status = "valid" if not blockers else "blocked"
    size_score = _size_score(clusters, settings)
    fragmentation_score = _fragmentation_score(clusters, settings)
    affinity_score = _merge_affinity_score(merge_evidence)
    module_economy_score = _module_economy_score(len(clusters), len(base_clusters))
    historical_cochange_score = _historical_merge_score(merge_evidence)
    facade_symbols = set(report.public_api_symbols)
    facade_symbols.update(
        symbol.name
        for symbol in report.symbols
        if set(symbol.risk_flags) & {"GLOBAL_STATE", "DECORATOR_RISK", "NESTED_SYMBOL_CLUSTER"}
    )
    quality = evaluate_candidate_quality(
        report,
        settings,
        clusters,
        facade_symbols,
    )
    blockers.extend(str(item) for item in quality.topology.get("blockers", []))
    blockers = sorted(set(blockers))
    status = "valid" if not blockers else "blocked"
    base_total = (
        0.22 * size_score
        + 0.18 * fragmentation_score
        + 0.15 * affinity_score
        + 0.10 * module_economy_score
        + 0.20 * quality.responsibility_cohesion_score
        + 0.15 * quality.topology_score
        - 0.15 * quality.mixed_responsibility_penalty
    )
    history_active = bool(git_history is not None and git_history.available)
    total = (
        0.95 * base_total + 0.05 * historical_cochange_score
        if history_active
        else base_total
    )
    return HeuristicCandidate(
        candidate_id=f"heuristic:{strategy}",
        strategy=strategy,
        clusters=clusters,
        status=status,
        total_score=round(total, 6),
        size_score=round(size_score, 6),
        fragmentation_score=round(fragmentation_score, 6),
        affinity_score=round(affinity_score, 6),
        module_economy_score=round(module_economy_score, 6),
        responsibility_cohesion_score=quality.responsibility_cohesion_score,
        topology_score=quality.topology_score,
        mixed_responsibility_penalty=quality.mixed_responsibility_penalty,
        facade_back_reference_penalty=quality.facade_back_reference_penalty,
        historical_cochange_score=round(historical_cochange_score, 6),
        quality_evidence=quality.to_dict(),
        merge_evidence=merge_evidence,
        blockers=blockers,
    )


def _best_tiny_merge(
    report: ModuleAnalysisReport,
    settings: PlannerSettings,
    clusters: list[DependencyCluster],
    symbol_by_name: dict[str, RefactorSymbol],
    strategy: str,
    threshold: float,
    git_history: GitCochangeEvidence | None,
) -> tuple[int, int, ClusterAffinity] | None:
    """Return the best admissible merge involving at least one tiny cluster."""
    minimum = max(
        MIN_HELPER_PHYSICAL_LINES,
        settings.minimum_helper_physical_lines,
    )
    proposals: list[tuple[float, int, int, ClusterAffinity]] = []
    for left_index, left in enumerate(clusters):
        for right_index in range(left_index + 1, len(clusters)):
            right = clusters[right_index]
            if left.estimated_lines >= minimum and right.estimated_lines >= minimum:
                continue
            merged_lines = _merged_estimated_lines(left, right, symbol_by_name)
            if merged_lines > settings.maximum_physical_lines:
                continue
            affinity = cluster_affinity(report, left, right, git_history)
            effective_score = _strategy_score(strategy, affinity)
            if effective_score < threshold:
                continue
            proposals.append((effective_score, left_index, right_index, affinity))
    if not proposals:
        return None
    proposals.sort(
        key=lambda item: (
            item[0],
            item[3].structural_score,
            item[3].semantic_score,
            item[3].historical_cochange_score,
            item[3].source_proximity_score,
            -item[1],
            -item[2],
        ),
        reverse=True,
    )
    _score, left_index, right_index, affinity = proposals[0]
    return left_index, right_index, affinity


def _strategy_score(strategy: str, affinity: ClusterAffinity) -> float:
    """Return strategy-specific score using the same explainable evidence."""
    if affinity.history_available:
        if strategy == "dependency_dominant":
            return (
                0.55 * affinity.structural_score
                + 0.15 * affinity.semantic_score
                + 0.10 * affinity.source_proximity_score
                + 0.05 * affinity.role_compatibility_score
                + 0.15 * affinity.historical_cochange_score
            )
        if strategy == "responsibility_dominant":
            return (
                0.45 * affinity.semantic_score
                + 0.20 * affinity.structural_score
                + 0.15 * affinity.source_proximity_score
                + 0.05 * affinity.role_compatibility_score
                + 0.15 * affinity.historical_cochange_score
            )
    if strategy == "dependency_dominant":
        return 0.65 * affinity.structural_score + 0.20 * affinity.semantic_score + 0.15 * affinity.source_proximity_score
    if strategy == "responsibility_dominant":
        return 0.50 * affinity.semantic_score + 0.25 * affinity.structural_score + 0.20 * affinity.source_proximity_score + 0.05 * affinity.role_compatibility_score
    return affinity.total_score


def _merge_clusters(
    left: DependencyCluster,
    right: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> DependencyCluster:
    """Return one merged cluster while preserving all atomic symbols."""
    symbols = sorted(
        set(left.symbols) | set(right.symbols),
        key=lambda name: symbol_by_name[name].start_line,
    )
    estimated = 16 + sum(symbol_by_name[name].physical_lines + 2 for name in symbols)
    return DependencyCluster(
        cluster_id="affinity:" + "+".join(symbols),
        role="dependency_cluster_helper" if len(symbols) > 1 else left.role,
        symbols=symbols,
        estimated_lines=estimated,
        dependency_edges=sorted(set(left.dependency_edges) | set(right.dependency_edges)),
        risk_flags=sorted(set(left.risk_flags) | set(right.risk_flags)),
        warnings=sorted(set(left.warnings) | set(right.warnings) | {"MULTI_SIGNAL_AFFINITY_MERGE"}),
        blockers=sorted(set(left.blockers) | set(right.blockers)),
    )


def _copy_cluster(cluster: DependencyCluster) -> DependencyCluster:
    """Return a detached cluster value for candidate isolation."""
    return replace(
        cluster,
        symbols=list(cluster.symbols),
        dependency_edges=list(cluster.dependency_edges),
        risk_flags=list(cluster.risk_flags),
        warnings=list(cluster.warnings),
        blockers=list(cluster.blockers),
    )


def _merged_estimated_lines(
    left: DependencyCluster,
    right: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> int:
    """Estimate merged physical lines without double-counting module overhead."""
    names = set(left.symbols) | set(right.symbols)
    return 16 + sum(symbol_by_name[name].physical_lines + 2 for name in names)


def _tiny_clusters(
    clusters: list[DependencyCluster],
    settings: PlannerSettings,
) -> list[DependencyCluster]:
    """Return helper clusters below the effective minimum size."""
    minimum = max(
        MIN_HELPER_PHYSICAL_LINES,
        settings.minimum_helper_physical_lines,
    )
    return [cluster for cluster in clusters if cluster.estimated_lines < minimum]


def _candidate_blockers(
    clusters: list[DependencyCluster],
    settings: PlannerSettings,
) -> list[str]:
    """Return size blockers for one helper candidate architecture."""
    blockers: list[str] = []
    minimum = max(
        MIN_HELPER_PHYSICAL_LINES,
        settings.minimum_helper_physical_lines,
    )
    for cluster in clusters:
        if cluster.estimated_lines < minimum:
            blockers.append(f"Cluster {cluster.cluster_id} remains below minimum helper size.")
        if cluster.estimated_lines > settings.maximum_physical_lines:
            blockers.append(f"Cluster {cluster.cluster_id} exceeds maximum helper size.")
        blockers.extend(cluster.blockers)
    return sorted(set(blockers))


def _size_score(clusters: list[DependencyCluster], settings: PlannerSettings) -> float:
    """Return average closeness to the ideal size for admissible helpers."""
    if not clusters:
        return 1.0
    values: list[float] = []
    for cluster in clusters:
        lines = cluster.estimated_lines
        if lines <= 0 or lines > settings.maximum_physical_lines:
            values.append(0.0)
        elif lines <= settings.ideal_physical_lines:
            values.append(min(1.0, lines / settings.ideal_physical_lines))
        else:
            span = max(1, settings.maximum_physical_lines - settings.ideal_physical_lines)
            values.append(max(0.0, 1.0 - (lines - settings.ideal_physical_lines) / span))
    return sum(values) / len(values)


def _fragmentation_score(clusters: list[DependencyCluster], settings: PlannerSettings) -> float:
    """Return one when no tiny helpers remain, falling with fragmentation."""
    if not clusters:
        return 1.0
    tiny_count = len(_tiny_clusters(clusters, settings))
    return 1.0 - tiny_count / len(clusters)


def _merge_affinity_score(merge_evidence: list[dict[str, object]]) -> float:
    """Return average accepted merge affinity, neutral for no-merge candidates."""
    if not merge_evidence:
        return 0.5
    return sum(float(item["total_score"]) for item in merge_evidence) / len(merge_evidence)


def _historical_merge_score(merge_evidence: list[dict[str, object]]) -> float:
    """Return average usable historical affinity, neutral when no merge has history."""
    values = [
        float(item.get("historical_cochange_score", 0.0))
        for item in merge_evidence
        if bool(item.get("history_available", False))
    ]
    if not values:
        return 0.5
    return sum(values) / len(values)


def _module_economy_score(current_count: int, base_count: int) -> float:
    """Return bounded evidence that unnecessary fragmentation was reduced."""
    if base_count <= 1:
        return 1.0
    reduction = max(0, base_count - current_count)
    return min(1.0, 0.5 + 0.5 * reduction / (base_count - 1))


def _cluster_start(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> int:
    """Return source-order key for a cluster."""
    starts = [symbol_by_name[name].start_line for name in cluster.symbols if name in symbol_by_name]
    return min(starts) if starts else 0
