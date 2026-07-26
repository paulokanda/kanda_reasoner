# project-path: kanda_reasoner_app/project_structure_visualizer/graph_view_filters.py
"""Read-only graph profile filtering for Project Structure 3D."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .graph_schema import validate_graph_snapshot

__all__ = ["filter_graph_snapshot"]

_SEMANTIC_RELATIONSHIPS = {"calls", "inherits", "validates", "protects"}


def filter_graph_snapshot(
    snapshot: dict[str, Any],
    *,
    mode: str,
    show_imports: bool,
    show_external: bool,
    show_symbols: bool = True,
    show_semantic: bool = True,
) -> dict[str, Any]:
    """Return one validated filtered copy without mutating source evidence."""
    normalized_mode = str(mode or "structure").strip().lower()
    if normalized_mode not in {"architecture", "structure"}:
        normalized_mode = "structure"

    result = deepcopy(snapshot)
    nodes = result.get("nodes", [])
    if normalized_mode == "architecture":
        allowed_kinds = {"project", "package", "external"}
    else:
        allowed_kinds = {
            "project",
            "package",
            "module",
            "validator",
            "external",
        }
        if show_symbols:
            allowed_kinds.update({"class", "function"})
    filtered_nodes = [
        node
        for node in nodes
        if node.get("kind") in allowed_kinds
        and (show_external or not bool(node.get("external")))
    ]
    node_ids = {str(node.get("id")) for node in filtered_nodes}
    filtered_edges = []
    for edge in result.get("edges", []):
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            continue
        relationship = str(edge.get("relationship") or "")
        if relationship == "imports" and not show_imports:
            continue
        if relationship in _SEMANTIC_RELATIONSHIPS and not show_semantic:
            continue
        filtered_edges.append(edge)

    for node in filtered_nodes:
        node["incoming_count"] = 0
        node["outgoing_count"] = 0
    by_id = {node["id"]: node for node in filtered_nodes}
    for edge in filtered_edges:
        by_id[edge["source"]]["outgoing_count"] += 1
        by_id[edge["target"]]["incoming_count"] += 1

    result["nodes"] = filtered_nodes
    result["edges"] = filtered_edges
    statistics = dict(result.get("statistics", {}))
    statistics.update(
        {
            "node_count": len(filtered_nodes),
            "edge_count": len(filtered_edges),
            "view_mode": normalized_mode,
            "imports_visible": bool(show_imports),
            "external_visible": bool(show_external),
            "symbols_visible": bool(show_symbols),
            "semantic_visible": bool(show_semantic),
        }
    )
    result["statistics"] = statistics
    result["layout"] = dict(result.get("layout", {}))
    result["layout"]["view_mode"] = normalized_mode
    validate_graph_snapshot(result)
    return result
