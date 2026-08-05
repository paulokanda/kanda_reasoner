# project-path: kanda_reasoner_app/project_structure_visualizer/graph_cycle_detector.py
"""Detect import/call cycles in a built graph snapshot (Tarjan SCC)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

__all__ = ["annotate_cycles"]

_CYCLE_RELATIONSHIPS = {"imports", "calls"}


def _build_adjacency(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Return adjacency list restricted to cycle-relevant relationships."""
    node_ids = {node["id"] for node in nodes}
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge.get("relationship") not in _CYCLE_RELATIONSHIPS:
            continue
        source, target = edge.get("source"), edge.get("target")
        if source in node_ids and target in node_ids:
            adjacency[source].append(target)
    return adjacency


def _tarjan_scc(adjacency: dict[str, list[str]], node_ids: list[str]) -> list[list[str]]:
    """Return strongly connected components with more than one member."""
    index_counter = [0]
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low_links: dict[str, int] = {}
    result: list[list[str]] = []

    def strongconnect(node_id: str) -> None:
        indices[node_id] = index_counter[0]
        low_links[node_id] = index_counter[0]
        index_counter[0] += 1
        stack.append(node_id)
        on_stack.add(node_id)

        for neighbor in adjacency.get(node_id, []):
            if neighbor not in indices:
                strongconnect(neighbor)
                low_links[node_id] = min(low_links[node_id], low_links[neighbor])
            elif neighbor in on_stack:
                low_links[node_id] = min(low_links[node_id], indices[neighbor])

        if low_links[node_id] == indices[node_id]:
            component: list[str] = []
            while True:
                member = stack.pop()
                on_stack.discard(member)
                component.append(member)
                if member == node_id:
                    break
            if len(component) > 1:
                result.append(component)

    for node_id in node_ids:
        if node_id not in indices:
            strongconnect(node_id)

    return result


def annotate_cycles(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    """Mark cycle-participant nodes and return cycle statistics.

    Sets node["metadata"]["in_cycle"] = True for every node in a
    strongly-connected component of size > 1, and raises node["risk_level"]
    to at least "review" (existing schema field, currently unused/"none").
    Does not mutate edges. Call after apply_relationship_counts().
    """
    node_ids = [node["id"] for node in nodes]
    adjacency = _build_adjacency(nodes, edges)
    components = _tarjan_scc(adjacency, node_ids)

    cyclic_ids: set[str] = set()
    for component in components:
        cyclic_ids.update(component)

    by_id = {node["id"]: node for node in nodes}
    for node_id in cyclic_ids:
        node = by_id[node_id]
        node["metadata"]["in_cycle"] = True
        if node.get("risk_level") == "none":
            node["risk_level"] = "review"

    return {
        "cycle_count": len(components),
        "cyclic_node_count": len(cyclic_ids),
        "cycles": [sorted(component) for component in components],
    }
