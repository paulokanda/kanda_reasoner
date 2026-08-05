# project-path: kanda_reasoner_app/project_structure_visualizer/graph_structure_findings.py
"""Derive structural quality findings from a built graph snapshot."""

from __future__ import annotations

import statistics as stats
from typing import Any

__all__ = ["compute_structure_findings"]

_HOTSPOT_STD_DEV_THRESHOLD = 1.5
_LOW_CONFIDENCE = {"inferred", "unresolved"}


def _module_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return only module/validator nodes (skip project/package/external)."""
    return [n for n in nodes if n.get("kind") in {"module", "validator"}]


def _has_incoming_validation(node_id: str, edges: list[dict[str, Any]]) -> bool:
    """Return whether a node has an incoming 'validates' edge."""
    return any(
        edge.get("target") == node_id and edge.get("relationship") == "validates"
        for edge in edges
    )


def compute_structure_findings(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute non-visual structural findings for the statistics block.

    Read-only: does not mutate nodes/edges. Call after apply_relationship_counts()
    and annotate_cycles(). Intended to populate snapshot["statistics"]["structure_findings"].
    """
    modules = _module_nodes(nodes)
    if not modules:
        return {
            "high_fan_in_nodes": [],
            "untested_hotspots": [],
            "low_confidence_edge_count": 0,
            "fan_in_mean": 0.0,
            "fan_in_std_dev": 0.0,
        }

    fan_in_values = [int(n.get("incoming_count", 0)) for n in modules]
    fan_in_mean = stats.mean(fan_in_values)
    fan_in_std_dev = stats.pstdev(fan_in_values) if len(fan_in_values) > 1 else 0.0
    threshold = fan_in_mean + _HOTSPOT_STD_DEV_THRESHOLD * fan_in_std_dev

    high_fan_in_nodes = sorted(
        (
            {
                "id": n["id"],
                "relative_path": n.get("relative_path", ""),
                "incoming_count": int(n.get("incoming_count", 0)),
            }
            for n in modules
            if int(n.get("incoming_count", 0)) > threshold
        ),
        key=lambda item: item["incoming_count"],
        reverse=True,
    )

    untested_hotspots = [
        {
            "id": item["id"],
            "relative_path": item["relative_path"],
            "incoming_count": item["incoming_count"],
        }
        for item in high_fan_in_nodes
        if not _has_incoming_validation(item["id"], edges)
    ]

    low_confidence_edge_count = sum(
        1 for edge in edges if edge.get("confidence") in _LOW_CONFIDENCE
    )

    return {
        "high_fan_in_nodes": high_fan_in_nodes,
        "untested_hotspots": untested_hotspots,
        "low_confidence_edge_count": low_confidence_edge_count,
        "fan_in_mean": round(fan_in_mean, 2),
        "fan_in_std_dev": round(fan_in_std_dev, 2),
    }
