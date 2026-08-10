# project-path: kanda_reasoner_app/project_structure_visualizer/graph_structure_analysis.py
"""Annotate bounded structural findings on an existing graph snapshot."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter, defaultdict
from typing import Any

__all__ = ["analyze_graph_structure"]

_MODULE_KINDS = {"module", "validator"}
_LOW_CONFIDENCE = {"inferred", "unresolved"}
_MAX_REPORTED_ITEMS = 10
_MAX_REPORTED_COMPONENTS = 20
_MAX_REPORTED_COMPONENT_MEMBERS = 20
_REVIEW_MIN_IMPORT_FAN_IN = 2
_REVIEW_PERCENTILE = 0.90


def _metadata(record: dict[str, Any]) -> dict[str, Any]:
    """Return a mutable metadata mapping for one graph record."""
    value = record.get("metadata")
    if isinstance(value, dict):
        return value
    replacement: dict[str, Any] = {}
    record["metadata"] = replacement
    return replacement


def _module_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return module-like nodes in stable identifier order."""
    return sorted(
        (node for node in nodes if node.get("kind") in _MODULE_KINDS),
        key=lambda node: str(node.get("id") or ""),
    )


def _import_pairs(
    edges: list[dict[str, Any]],
    module_ids: set[str],
) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """Return all module imports and the internal module-only subset."""
    all_pairs: set[tuple[str, str]] = set()
    internal_pairs: set[tuple[str, str]] = set()
    for edge in edges:
        if edge.get("relationship") != "imports":
            continue
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        if source not in module_ids or not target:
            continue
        all_pairs.add((source, target))
        if target in module_ids:
            internal_pairs.add((source, target))
    return all_pairs, internal_pairs


def _tarjan_components(
    module_ids: list[str],
    internal_pairs: set[tuple[str, str]],
) -> list[list[str]]:
    """Return deterministic cyclic strongly connected components."""
    adjacency: dict[str, list[str]] = defaultdict(list)
    self_loops: set[str] = set()
    for source, target in sorted(internal_pairs):
        adjacency[source].append(target)
        if source == target:
            self_loops.add(source)

    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low_links: dict[str, int] = {}
    components: list[list[str]] = []

    def strong_connect(node_id: str) -> None:
        nonlocal index
        indices[node_id] = index
        low_links[node_id] = index
        index += 1
        stack.append(node_id)
        on_stack.add(node_id)

        for neighbor in adjacency.get(node_id, []):
            if neighbor not in indices:
                strong_connect(neighbor)
                low_links[node_id] = min(low_links[node_id], low_links[neighbor])
            elif neighbor in on_stack:
                low_links[node_id] = min(low_links[node_id], indices[neighbor])

        if low_links[node_id] != indices[node_id]:
            return
        component: list[str] = []
        while stack:
            member = stack.pop()
            on_stack.discard(member)
            component.append(member)
            if member == node_id:
                break
        component.sort()
        if len(component) > 1 or node_id in self_loops:
            components.append(component)

    for node_id in module_ids:
        if node_id not in indices:
            strong_connect(node_id)
    return sorted(components, key=lambda component: tuple(component))


def _fan_in_percentiles(fan_in: Counter[str]) -> dict[str, float]:
    """Return bounded rank percentiles for positive import fan-in values."""
    positive = sorted(value for value in fan_in.values() if value > 0)
    if not positive:
        return {node_id: 0.0 for node_id in fan_in}
    total = len(positive)
    return {
        node_id: (
            round(bisect_right(positive, value) / total, 4)
            if value > 0
            else 0.0
        )
        for node_id, value in fan_in.items()
    }


def _finding_record(node: dict[str, Any]) -> dict[str, Any]:
    """Return one compact, renderer-safe structural finding record."""
    metadata = _metadata(node)
    return {
        "id": str(node.get("id") or ""),
        "relative_path": str(node.get("relative_path") or ""),
        "import_fan_in": int(metadata.get("import_fan_in") or 0),
        "import_fan_out": int(metadata.get("import_fan_out") or 0),
        "import_fan_in_percentile": float(
            metadata.get("import_fan_in_percentile") or 0.0
        ),
        "visible_validation_link_count": int(
            metadata.get("visible_validation_link_count") or 0
        ),
        "visible_protection_link_count": int(
            metadata.get("visible_protection_link_count") or 0
        ),
    }


def analyze_graph_structure(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    """Annotate import-only structure metrics and return bounded findings.

    The analysis consumes only the already-built, bounded graph snapshot. It does
    not scan source, claim whole-project completeness, or create a quality score.
    """
    modules = _module_nodes(nodes)
    module_ids = {str(node.get("id") or "") for node in modules}
    module_ids.discard("")
    all_imports, internal_imports = _import_pairs(edges, module_ids)

    fan_in: Counter[str] = Counter({node_id: 0 for node_id in module_ids})
    fan_out: Counter[str] = Counter({node_id: 0 for node_id in module_ids})
    for source, target in all_imports:
        fan_out[source] += 1
        if target in module_ids:
            fan_in[target] += 1

    visible_validation: Counter[str] = Counter()
    visible_protection: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()
    for edge in edges:
        confidence_counts[str(edge.get("confidence") or "unresolved")] += 1
        target = str(edge.get("target") or "")
        if target not in module_ids:
            continue
        relationship = edge.get("relationship")
        if relationship == "validates":
            visible_validation[target] += 1
        elif relationship == "protects":
            visible_protection[target] += 1

    percentiles = _fan_in_percentiles(fan_in)
    for node in modules:
        node_id = str(node.get("id") or "")
        metadata = _metadata(node)
        metadata["import_fan_in"] = int(fan_in[node_id])
        metadata["import_fan_out"] = int(fan_out[node_id])
        metadata["import_fan_in_percentile"] = float(percentiles[node_id])
        metadata["visible_validation_link_count"] = int(
            visible_validation[node_id]
        )
        metadata["visible_protection_link_count"] = int(
            visible_protection[node_id]
        )
        metadata["in_import_cycle"] = False
        metadata["import_cycle_component_id"] = ""

    components = _tarjan_components(sorted(module_ids), internal_imports)
    component_by_node: dict[str, str] = {}
    component_records: list[dict[str, Any]] = []
    for index, component in enumerate(components, start=1):
        component_id = f"import-cycle-{index:03d}"
        for node_id in component:
            component_by_node[node_id] = component_id
        component_records.append(
            {
                "component_id": component_id,
                "size": len(component),
                "members": component[:_MAX_REPORTED_COMPONENT_MEMBERS],
                "members_truncated": len(component) > _MAX_REPORTED_COMPONENT_MEMBERS,
            }
        )

    by_id = {str(node.get("id") or ""): node for node in modules}
    for node_id, component_id in component_by_node.items():
        metadata = _metadata(by_id[node_id])
        metadata["in_import_cycle"] = True
        metadata["import_cycle_component_id"] = component_id

    for edge in edges:
        if edge.get("relationship") != "imports":
            continue
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        source_component = component_by_node.get(source, "")
        target_component = component_by_node.get(target, "")
        metadata = _metadata(edge)
        metadata["in_import_cycle"] = bool(
            source_component and source_component == target_component
        )
        metadata["import_cycle_component_id"] = (
            source_component if metadata["in_import_cycle"] else ""
        )

    ranked_nodes = sorted(
        modules,
        key=lambda node: (
            -int(_metadata(node).get("import_fan_in") or 0),
            str(node.get("relative_path") or ""),
            str(node.get("id") or ""),
        ),
    )
    ranked_positive = [
        node
        for node in ranked_nodes
        if int(_metadata(node).get("import_fan_in") or 0) > 0
    ]
    review_candidates = [
        node
        for node in ranked_positive
        if int(_metadata(node).get("import_fan_in") or 0)
        >= _REVIEW_MIN_IMPORT_FAN_IN
        and float(_metadata(node).get("import_fan_in_percentile") or 0.0)
        >= _REVIEW_PERCENTILE
        and int(_metadata(node).get("visible_validation_link_count") or 0) == 0
    ]

    low_confidence_count = sum(
        confidence_counts.get(value, 0) for value in _LOW_CONFIDENCE
    )
    return {
        "analysis_version": "import-structure-v1",
        "scope": "rendered_snapshot_only",
        "whole_project_completeness_claimed": False,
        "quality_score": None,
        "cyclic_component_count": len(components),
        "cyclic_node_count": len(component_by_node),
        "cyclic_components": component_records[:_MAX_REPORTED_COMPONENTS],
        "cyclic_components_truncated": (
            len(component_records) > _MAX_REPORTED_COMPONENTS
        ),
        "top_import_fan_in_nodes": [
            _finding_record(node)
            for node in ranked_positive[:_MAX_REPORTED_ITEMS]
        ],
        "top_import_fan_in_truncated": len(ranked_positive) > _MAX_REPORTED_ITEMS,
        "high_import_fan_in_without_visible_validation": [
            _finding_record(node)
            for node in review_candidates[:_MAX_REPORTED_ITEMS]
        ],
        "review_candidates_truncated": (
            len(review_candidates) > _MAX_REPORTED_ITEMS
        ),
        "confidence_counts": {
            key: int(confidence_counts[key]) for key in sorted(confidence_counts)
        },
        "low_confidence_edge_count": int(low_confidence_count),
    }
