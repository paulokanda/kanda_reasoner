# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_specific_delta_strategies.py
"""Analyzer-specific delta strategies for Advanced Quality Review."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable

from .advanced_quality_evidence_models import NormalizedFinding

__all__ = [
    "ANALYZER_SPECIFIC_DELTA_FEATURE_ID",
    "GraphTopologyDelta",
    "GraphTopologyDeltaState",
    "MypyFindingDelta",
    "MypyRelocationState",
    "VultureCandidateDelta",
    "VultureCandidateDeltaState",
    "build_graph_topology_deltas",
    "build_mypy_relocation_deltas",
    "build_vulture_candidate_deltas",
]

ANALYZER_SPECIFIC_DELTA_FEATURE_ID = (
    "advanced-quality-review-grimp-mypy-vulture-fitness-adapters-v1"
)


class GraphTopologyDeltaState(str, Enum):
    """Describe baseline-to-Preview topology set movement."""

    NEW_EDGE = "NEW_EDGE"
    REMOVED_EDGE = "REMOVED_EDGE"
    PERSISTENT_EDGE = "PERSISTENT_EDGE"
    NEW_CYCLE_BREAKER = "NEW_CYCLE_BREAKER"
    RESOLVED_CYCLE_BREAKER = "RESOLVED_CYCLE_BREAKER"
    PERSISTENT_CYCLE_BREAKER = "PERSISTENT_CYCLE_BREAKER"


@dataclass(frozen=True)
class GraphTopologyDelta:
    """Record one deterministic graph topology set delta."""

    state: GraphTopologyDeltaState
    importer: str
    imported: str

    def to_dict(self) -> dict[str, str]:
        """Return stable JSON-ready topology delta evidence."""
        payload = asdict(self)
        payload["state"] = self.state.value
        return payload


class MypyRelocationState(str, Enum):
    """Describe conservative mypy baseline-to-Preview finding movement."""

    EXACT_MATCH = "EXACT_MATCH"
    RELOCATED_MATCH = "RELOCATED_MATCH"
    AMBIGUOUS_MATCH = "AMBIGUOUS_MATCH"
    NEW_FINDING = "NEW_FINDING"
    RESOLVED_FINDING = "RESOLVED_FINDING"


@dataclass(frozen=True)
class MypyFindingDelta:
    """Record one mypy finding delta with conservative relocation evidence."""

    state: MypyRelocationState
    finding: NormalizedFinding
    candidate_semantic_keys: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready mypy delta evidence."""
        return {
            "state": self.state.value,
            "finding": self.finding.to_dict(),
            "semantic_key": self.finding.semantic_key,
            "candidate_semantic_keys": list(self.candidate_semantic_keys),
        }


class VultureCandidateDeltaState(str, Enum):
    """Describe baseline-to-Preview dead-code candidate movement."""

    NEW_CANDIDATE = "NEW_CANDIDATE"
    RESOLVED_CANDIDATE = "RESOLVED_CANDIDATE"
    PERSISTENT_CANDIDATE = "PERSISTENT_CANDIDATE"


@dataclass(frozen=True)
class VultureCandidateDelta:
    """Record one advisory dead-code candidate delta."""

    state: VultureCandidateDeltaState
    finding: NormalizedFinding

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready advisory delta evidence."""
        return {
            "state": self.state.value,
            "finding": self.finding.to_dict(),
            "semantic_key": self.finding.semantic_key,
        }


def build_graph_topology_deltas(
    baseline_edges: Iterable[tuple[str, str]],
    preview_edges: Iterable[tuple[str, str]],
    *,
    baseline_cycle_breakers: Iterable[tuple[str, str]] = (),
    preview_cycle_breakers: Iterable[tuple[str, str]] = (),
) -> tuple[GraphTopologyDelta, ...]:
    """Build graph set deltas without compressing topology into one score."""
    deltas: list[GraphTopologyDelta] = []
    deltas.extend(
        _edge_set_deltas(
            set(_normalized_edges(baseline_edges)),
            set(_normalized_edges(preview_edges)),
            new_state=GraphTopologyDeltaState.NEW_EDGE,
            removed_state=GraphTopologyDeltaState.REMOVED_EDGE,
            persistent_state=GraphTopologyDeltaState.PERSISTENT_EDGE,
        )
    )
    deltas.extend(
        _edge_set_deltas(
            set(_normalized_edges(baseline_cycle_breakers)),
            set(_normalized_edges(preview_cycle_breakers)),
            new_state=GraphTopologyDeltaState.NEW_CYCLE_BREAKER,
            removed_state=GraphTopologyDeltaState.RESOLVED_CYCLE_BREAKER,
            persistent_state=GraphTopologyDeltaState.PERSISTENT_CYCLE_BREAKER,
        )
    )
    return tuple(
        sorted(
            deltas,
            key=lambda item: (item.state.value, item.importer, item.imported),
        )
    )


def build_mypy_relocation_deltas(
    baseline_findings: Iterable[NormalizedFinding],
    preview_findings: Iterable[NormalizedFinding],
) -> tuple[MypyFindingDelta, ...]:
    """Build conservative exact, relocated, ambiguous, new, and resolved states."""
    baseline = tuple(baseline_findings)
    preview = tuple(preview_findings)
    baseline_by_key = {item.semantic_key: item for item in baseline}
    preview_by_key = {item.semantic_key: item for item in preview}
    deltas: list[MypyFindingDelta] = []
    exact_keys = set(baseline_by_key) & set(preview_by_key)
    for key in sorted(exact_keys):
        deltas.append(
            MypyFindingDelta(
                state=MypyRelocationState.EXACT_MATCH,
                finding=preview_by_key[key],
                candidate_semantic_keys=(key,),
            )
        )

    unmatched_baseline = [
        item for item in baseline if item.semantic_key not in exact_keys
    ]
    unmatched_preview = [
        item for item in preview if item.semantic_key not in exact_keys
    ]
    baseline_groups = _group_by_relocation_key(unmatched_baseline)
    matched_baseline_keys: set[str] = set()

    for finding in sorted(unmatched_preview, key=lambda item: item.semantic_key):
        candidates = baseline_groups.get(_mypy_relocation_key(finding), ())
        candidate_keys = tuple(sorted(item.semantic_key for item in candidates))
        if len(candidates) == 1:
            matched_baseline_keys.add(candidates[0].semantic_key)
            state = MypyRelocationState.RELOCATED_MATCH
        elif len(candidates) > 1:
            state = MypyRelocationState.AMBIGUOUS_MATCH
        else:
            state = MypyRelocationState.NEW_FINDING
        deltas.append(
            MypyFindingDelta(
                state=state,
                finding=finding,
                candidate_semantic_keys=candidate_keys,
            )
        )

    for finding in sorted(unmatched_baseline, key=lambda item: item.semantic_key):
        if finding.semantic_key in matched_baseline_keys:
            continue
        if _mypy_relocation_key(finding) in {
            _mypy_relocation_key(item)
            for item in unmatched_preview
            if len(baseline_groups.get(_mypy_relocation_key(item), ())) > 1
        }:
            continue
        deltas.append(
            MypyFindingDelta(
                state=MypyRelocationState.RESOLVED_FINDING,
                finding=finding,
            )
        )

    return tuple(
        sorted(
            deltas,
            key=lambda item: (item.state.value, item.finding.semantic_key),
        )
    )


def build_vulture_candidate_deltas(
    baseline_findings: Iterable[NormalizedFinding],
    preview_findings: Iterable[NormalizedFinding],
) -> tuple[VultureCandidateDelta, ...]:
    """Build advisory dead-code deltas using stable symbol/scope candidate identity."""
    baseline_map = {item.semantic_key: item for item in baseline_findings}
    preview_map = {item.semantic_key: item for item in preview_findings}
    deltas: list[VultureCandidateDelta] = []
    for key in sorted(set(baseline_map) | set(preview_map)):
        if key in baseline_map and key in preview_map:
            state = VultureCandidateDeltaState.PERSISTENT_CANDIDATE
            finding = preview_map[key]
        elif key in preview_map:
            state = VultureCandidateDeltaState.NEW_CANDIDATE
            finding = preview_map[key]
        else:
            state = VultureCandidateDeltaState.RESOLVED_CANDIDATE
            finding = baseline_map[key]
        deltas.append(VultureCandidateDelta(state=state, finding=finding))
    return tuple(deltas)


def _edge_set_deltas(
    baseline: set[tuple[str, str]],
    preview: set[tuple[str, str]],
    *,
    new_state: GraphTopologyDeltaState,
    removed_state: GraphTopologyDeltaState,
    persistent_state: GraphTopologyDeltaState,
) -> list[GraphTopologyDelta]:
    """Return deterministic set deltas for import edges or cycle breakers."""
    result: list[GraphTopologyDelta] = []
    for edge in sorted(baseline | preview):
        if edge in baseline and edge in preview:
            state = persistent_state
        elif edge in preview:
            state = new_state
        else:
            state = removed_state
        result.append(GraphTopologyDelta(state, edge[0], edge[1]))
    return result


def _normalized_edges(
    edges: Iterable[tuple[str, str]],
) -> tuple[tuple[str, str], ...]:
    """Validate and normalize one iterable of directed module edges."""
    normalized: list[tuple[str, str]] = []
    for importer, imported in edges:
        left = str(importer or "").strip()
        right = str(imported or "").strip()
        if not left or not right:
            raise ValueError("GRAPH_EDGE_MODULE_EMPTY")
        normalized.append((left, right))
    return tuple(normalized)


def _group_by_relocation_key(
    findings: Iterable[NormalizedFinding],
) -> dict[tuple[str, str, str], tuple[NormalizedFinding, ...]]:
    """Group mypy findings by conservative path-independent relocation identity."""
    groups: dict[tuple[str, str, str], list[NormalizedFinding]] = {}
    for finding in findings:
        groups.setdefault(_mypy_relocation_key(finding), []).append(finding)
    return {
        key: tuple(sorted(items, key=lambda item: item.semantic_key))
        for key, items in groups.items()
    }


def _mypy_relocation_key(finding: NormalizedFinding) -> tuple[str, str, str]:
    """Return conservative relocation identity without source path or line metadata."""
    return (
        finding.rule_id,
        finding.symbol_identity,
        finding.normalized_message_signature,
    )
