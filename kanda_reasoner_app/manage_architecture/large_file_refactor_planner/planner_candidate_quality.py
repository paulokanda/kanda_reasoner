# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_candidate_quality.py
"""Responsibility and topology quality evidence for heuristic candidates."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .dependency_clusterer import DependencyCluster
from .models import ModuleAnalysisReport, PlannerSettings
from .planner_dependency_topology import build_cluster_dependency_topology
from .planner_responsibility_labels import label_cluster_responsibilities

__all__ = ["CandidateQualityEvidence", "evaluate_candidate_quality"]


@dataclass(frozen=True)
class CandidateQualityEvidence:
    """Explainable candidate quality beyond size and merge affinity."""

    responsibility_cohesion_score: float
    topology_score: float
    mixed_responsibility_penalty: float
    facade_back_reference_penalty: float
    mixed_responsibility_clusters: list[dict[str, object]] = field(default_factory=list)
    topology: dict[str, object] = field(default_factory=dict)
    responsibility_labels: dict[str, dict[str, object]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready quality evidence."""
        return asdict(self)


def evaluate_candidate_quality(
    report: ModuleAnalysisReport,
    settings: PlannerSettings,
    clusters: list[DependencyCluster],
    facade_symbols: set[str],
) -> CandidateQualityEvidence:
    """Score responsibility cohesion and projected topology deterministically."""
    labels = label_cluster_responsibilities(report, clusters)
    mixed_records: list[dict[str, object]] = []
    weighted_scores: list[tuple[int, float]] = []
    weighted_penalties: list[tuple[int, float]] = []
    for cluster in clusters:
        label = labels[cluster.cluster_id]
        secondary_count = len(label.secondary_responsibilities)
        size_pressure = min(1.0, cluster.estimated_lines / max(1, settings.maximum_physical_lines))
        secondary_penalty = min(0.55, 0.20 * secondary_count * (0.55 + 0.45 * size_pressure))
        cohesion = max(0.0, label.confidence_score * (1.0 - secondary_penalty))
        weighted_scores.append((cluster.estimated_lines, cohesion))
        weighted_penalties.append((cluster.estimated_lines, secondary_penalty))
        if secondary_count:
            mixed_records.append(
                {
                    "cluster_id": cluster.cluster_id,
                    "estimated_lines": cluster.estimated_lines,
                    "primary_responsibility": label.primary_responsibility,
                    "secondary_responsibilities": list(label.secondary_responsibilities),
                    "penalty": round(secondary_penalty, 6),
                }
            )

    topology = build_cluster_dependency_topology(report, clusters, facade_symbols)
    facade_penalty = min(0.35, 0.08 * len(topology.facade_back_references))
    helper_cycle_penalty = 1.0 if topology.helper_cycles else 0.0
    helper_edge_penalty = min(0.20, 0.03 * len(topology.helper_edges))
    topology_score = max(
        0.0,
        1.0 - facade_penalty - helper_edge_penalty - helper_cycle_penalty,
    )
    return CandidateQualityEvidence(
        responsibility_cohesion_score=round(_weighted_average(weighted_scores), 6),
        topology_score=round(topology_score, 6),
        mixed_responsibility_penalty=round(_weighted_average(weighted_penalties), 6),
        facade_back_reference_penalty=round(facade_penalty, 6),
        mixed_responsibility_clusters=mixed_records,
        topology=topology.to_dict(),
        responsibility_labels={
            cluster_id: label.to_dict()
            for cluster_id, label in labels.items()
        },
    )


def _weighted_average(values: list[tuple[int, float]]) -> float:
    if not values:
        return 1.0
    total_weight = sum(max(1, weight) for weight, _value in values)
    return sum(max(1, weight) * value for weight, value in values) / total_weight
