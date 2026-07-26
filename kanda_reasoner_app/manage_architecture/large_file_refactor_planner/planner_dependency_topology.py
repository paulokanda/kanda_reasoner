# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_dependency_topology.py
"""Projected dependency topology evidence for planned helper architectures."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable

from .dependency_clusterer import DependencyCluster
from .models import ModuleAnalysisReport, ProposedModule

__all__ = [
    "DependencyTopologyReport",
    "build_cluster_dependency_topology",
    "build_module_dependency_topology",
]

_FACADE_NODE = "public_facade"


@dataclass(frozen=True)
class DependencyTopologyReport:
    """Directed projected module topology derived from symbol references."""

    status: str
    nodes: list[str]
    edges: list[str]
    helper_edges: list[str]
    helper_topological_order: list[str]
    helper_cycles: list[list[str]] = field(default_factory=list)
    full_cycle_components: list[list[str]] = field(default_factory=list)
    facade_back_references: list[str] = field(default_factory=list)
    edge_evidence: dict[str, list[str]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready topology evidence."""
        return asdict(self)


def build_cluster_dependency_topology(
    report: ModuleAnalysisReport,
    clusters: list[DependencyCluster],
    facade_symbols: Iterable[str],
) -> DependencyTopologyReport:
    """Build topology using candidate cluster ids as helper nodes."""
    assignment = {name: _FACADE_NODE for name in facade_symbols}
    for cluster in clusters:
        for symbol in cluster.symbols:
            assignment[symbol] = cluster.cluster_id
    nodes = [_FACADE_NODE] + [cluster.cluster_id for cluster in clusters]
    return _build_topology(report, assignment, nodes)


def build_module_dependency_topology(
    report: ModuleAnalysisReport,
    modules: list[ProposedModule],
) -> DependencyTopologyReport:
    """Build topology using final proposed filenames as nodes."""
    assignment: dict[str, str] = {}
    nodes: list[str] = []
    for module in modules:
        nodes.append(module.filename)
        for symbol in module.symbols:
            assignment[symbol] = module.filename
    facade_name = next(
        (module.filename for module in modules if module.role == "public_facade"),
        _FACADE_NODE,
    )
    return _build_topology(report, assignment, nodes, facade_name=facade_name)


def _build_topology(
    report: ModuleAnalysisReport,
    assignment: dict[str, str],
    nodes: list[str],
    facade_name: str = _FACADE_NODE,
) -> DependencyTopologyReport:
    edge_evidence: dict[tuple[str, str], set[str]] = {}
    known_symbols = set(assignment)
    for symbol in report.symbols:
        source_node = assignment.get(symbol.name)
        if not source_node:
            continue
        dependencies = (
            set(symbol.references)
            | set(symbol.imports_used)
            | set(symbol.globals_used)
        )
        for dependency in sorted(dependencies & known_symbols):
            target_node = assignment.get(dependency)
            if not target_node or target_node == source_node:
                continue
            edge_evidence.setdefault((source_node, target_node), set()).add(
                symbol.name + "->" + dependency
            )

    edges = sorted(edge_evidence)
    helper_nodes = sorted(node for node in set(nodes) if node != facade_name)
    helper_edges = sorted(
        (left, right)
        for left, right in edges
        if left in helper_nodes and right in helper_nodes
    )
    helper_cycles = _cycle_components(helper_nodes, helper_edges)
    full_nodes = sorted(set(nodes) | {item for edge in edges for item in edge})
    full_cycles = _cycle_components(full_nodes, edges)
    facade_back_refs = sorted(
        (left, right)
        for left, right in edges
        if left in helper_nodes and right == facade_name
    )
    warnings: list[str] = []
    blockers: list[str] = []
    if facade_back_refs:
        warnings.append("FACADE_BACK_REFERENCE_RISK")
    if any(facade_name in component for component in full_cycles):
        warnings.append("FACADE_BOUNDARY_CYCLE_RISK")
    if helper_cycles:
        blockers.append("HELPER_DEPENDENCY_CYCLE")
    status = (
        "blocked" if blockers else
        "ready_with_warnings" if warnings else
        "ready"
    )
    return DependencyTopologyReport(
        status=status,
        nodes=sorted(set(nodes)),
        edges=[_edge_text(edge) for edge in edges],
        helper_edges=[_edge_text(edge) for edge in helper_edges],
        helper_topological_order=(
            [] if helper_cycles else _topological_order(helper_nodes, helper_edges)
        ),
        helper_cycles=helper_cycles,
        full_cycle_components=full_cycles,
        facade_back_references=[_edge_text(edge) for edge in facade_back_refs],
        edge_evidence={
            _edge_text(edge): sorted(values)
            for edge, values in sorted(edge_evidence.items())
        },
        warnings=warnings,
        blockers=blockers,
    )


def _cycle_components(
    nodes: list[str],
    edges: list[tuple[str, str]],
) -> list[list[str]]:
    """Return strongly connected components that represent directed cycles."""
    adjacency = {node: [] for node in nodes}
    for left, right in edges:
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, [])
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in sorted(adjacency.get(node, [])):
            if target not in indices:
                visit(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[target])
        if lowlinks[node] != indices[node]:
            return
        component: list[str] = []
        while stack:
            current = stack.pop()
            on_stack.remove(current)
            component.append(current)
            if current == node:
                break
        component.sort()
        if len(component) > 1:
            components.append(component)
        elif (component[0], component[0]) in edges:
            components.append(component)

    for node in sorted(adjacency):
        if node not in indices:
            visit(node)
    return sorted(components)


def _topological_order(
    nodes: list[str],
    edges: list[tuple[str, str]],
) -> list[str]:
    """Return deterministic Kahn topological order for an acyclic helper graph."""
    adjacency = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for left, right in edges:
        if right not in adjacency[left]:
            adjacency[left].add(right)
            indegree[right] = indegree.get(right, 0) + 1
    ready = sorted(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for target in sorted(adjacency.get(node, set())):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
                ready.sort()
    return order


def _edge_text(edge: tuple[str, str]) -> str:
    return edge[0] + " -> " + edge[1]
