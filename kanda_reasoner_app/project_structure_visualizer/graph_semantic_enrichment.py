# project-path: kanda_reasoner_app/project_structure_visualizer/graph_semantic_enrichment.py
"""Orchestrate semantic graph enrichment from existing KANDA evidence."""

from __future__ import annotations

from typing import Any

from .graph_protection_status import apply_protection_evidence
from .graph_semantic_edges import add_semantic_edges
from .graph_symbol_nodes import add_symbol_nodes

__all__ = ["enrich_graph_semantics"]


def enrich_graph_semantics(
    project_root: object,
    payload: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, int]:
    """Add bounded symbols, relationships, validators, and protection status."""
    symbol_index = add_symbol_nodes(payload, nodes, edges)
    statistics = {
        "class_count": int(symbol_index["class_count"]),
        "function_count": int(symbol_index["function_count"]),
        "available_class_count": int(symbol_index["available_class_count"]),
        "available_function_count": int(symbol_index["available_function_count"]),
    }
    statistics.update(add_semantic_edges(payload, edges, symbol_index))
    statistics.update(apply_protection_evidence(project_root, payload, nodes, edges))
    return statistics
