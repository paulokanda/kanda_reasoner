# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/dependency_clusterer.py
"""Dependency-aware symbol clustering for large-file split planning."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from .models import ModuleAnalysisReport, PlannerSettings, RefactorSymbol, SCHEMA_VERSION

__all__ = [
    "DependencyCluster",
    "DependencyClusteringReport",
    "build_dependency_clusters",
]

_MULTI_SYMBOL_ROLE = "dependency_cluster_helper"


@dataclass(frozen=True)
class DependencyCluster:
    """One cohesive group of symbols that should move together."""

    cluster_id: str
    role: str
    symbols: list[str]
    estimated_lines: int
    dependency_edges: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready cluster record."""
        return asdict(self)


@dataclass(frozen=True)
class DependencyClusteringReport:
    """Dependency clustering evidence for a split plan."""

    schema_version: str
    target_file: str
    status: str
    clusters: list[DependencyCluster]
    risk_flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready clustering report."""
        return {
            "schema_version": self.schema_version,
            "target_file": self.target_file,
            "status": self.status,
            "clusters": [cluster.to_dict() for cluster in self.clusters],
            "risk_flags": list(self.risk_flags),
            "warnings": list(self.warnings),
            "blockers": list(self.blockers),
        }


def build_dependency_clusters(
    report: ModuleAnalysisReport,
    settings: PlannerSettings,
    movable_symbol_names: Iterable[str],
) -> DependencyClusteringReport:
    """Build dependency-aware clusters for movable top-level symbols."""
    movable = set(movable_symbol_names)
    symbols = [symbol for symbol in report.symbols if symbol.name in movable]
    if not symbols:
        return DependencyClusteringReport(
            schema_version=SCHEMA_VERSION,
            target_file=report.target_file,
            status="no_movable_symbols",
            clusters=[],
            warnings=["DEPENDENCY_CLUSTERING_NO_MOVABLE_SYMBOLS"],
        )
    symbol_by_name = {symbol.name: symbol for symbol in symbols}
    edges = _dependency_edges(symbol_by_name)
    components = _connected_components(symbol_by_name, edges)
    clusters = [
        _cluster_from_component(component, symbol_by_name, edges, settings)
        for component in components
    ]
    risks = sorted({risk for cluster in clusters for risk in cluster.risk_flags})
    warnings = sorted({warning for cluster in clusters for warning in cluster.warnings})
    blockers = sorted({blocker for cluster in clusters for blocker in cluster.blockers})
    if edges:
        warnings.append("DEPENDENCY_AWARE_CLUSTERING_USED")
    else:
        warnings.append("NO_INTERNAL_SYMBOL_DEPENDENCIES_DETECTED")
    return DependencyClusteringReport(
        schema_version=SCHEMA_VERSION,
        target_file=str(Path(report.target_file)),
        status="blocked" if blockers else "ready",
        clusters=clusters,
        risk_flags=sorted(set(risks)),
        warnings=sorted(set(warnings)),
        blockers=blockers,
    )


def _dependency_edges(symbol_by_name: dict[str, RefactorSymbol]) -> set[tuple[str, str]]:
    """Return undirected dependency edges between movable symbols."""
    names = set(symbol_by_name)
    edges: set[tuple[str, str]] = set()
    for symbol in symbol_by_name.values():
        candidates = set(symbol.references) | set(symbol.imports_used) | set(symbol.globals_used)
        for dependency in sorted(candidates & names):
            if dependency == symbol.name:
                continue
            edges.add(tuple(sorted((symbol.name, dependency))))
    return edges


def _connected_components(
    symbol_by_name: dict[str, RefactorSymbol],
    edges: set[tuple[str, str]],
) -> list[list[str]]:
    """Return dependency-connected components in source order."""
    adjacency = {name: set() for name in symbol_by_name}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    visited: set[str] = set()
    components: list[list[str]] = []
    ordered_names = sorted(symbol_by_name, key=lambda name: symbol_by_name[name].start_line)
    for name in ordered_names:
        if name in visited:
            continue
        stack = [name]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            stack.extend(sorted(adjacency[current] - visited))
        components.append(sorted(component, key=lambda item: symbol_by_name[item].start_line))
    return components


def _cluster_from_component(
    component: list[str],
    symbol_by_name: dict[str, RefactorSymbol],
    edges: set[tuple[str, str]],
    settings: PlannerSettings,
) -> DependencyCluster:
    """Return one cluster record from a dependency component."""
    symbols = [symbol_by_name[name] for name in component]
    estimated = 16 + sum(symbol.physical_lines + 2 for symbol in symbols)
    cluster_edges = [f"{left}->{right}" for left, right in sorted(edges) if left in component and right in component]
    role = _role_for_component(symbols, cluster_edges)
    risks = sorted({risk for symbol in symbols for risk in symbol.risk_flags})
    warnings: list[str] = []
    blockers: list[str] = []
    if cluster_edges:
        warnings.append("INTERNAL_DEPENDENCY_CLUSTER")
    if estimated > settings.ideal_physical_lines:
        warnings.append("DEPENDENCY_CLUSTER_OVER_IDEAL_SIZE")
    if estimated > settings.maximum_physical_lines:
        risks.append("DEPENDENCY_CLUSTER_TOO_LARGE")
        blockers.append(f"Dependency cluster {','.join(component)} exceeds maximum physical lines.")
    if any(symbol.globals_used for symbol in symbols):
        risks.append("GLOBAL_DEPENDENCY_CLUSTER")
        warnings.append("GLOBAL_DEPENDENCY_REQUIRES_REVIEW")
    return DependencyCluster(
        cluster_id=f"dependency:{'+'.join(component)}",
        role=role,
        symbols=list(component),
        estimated_lines=estimated,
        dependency_edges=cluster_edges,
        risk_flags=sorted(set(risks)),
        warnings=sorted(set(warnings)),
        blockers=sorted(set(blockers)),
    )


def _role_for_component(symbols: list[RefactorSymbol], edges: list[str]) -> str:
    """Return the helper role for a dependency component."""
    if len(symbols) > 1 or edges:
        return _MULTI_SYMBOL_ROLE
    symbol = symbols[0]
    if symbol.kind == "class":
        return "class_helper"
    if symbol.kind == "async_function":
        return "async_helper"
    return "function_helper"
