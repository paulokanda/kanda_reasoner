# project-path: kanda_reasoner_app/project_structure_visualizer/graph_snapshot_primitives.py
"""Private deterministic primitives for Project Structure 3D snapshots."""

from __future__ import annotations

import math
from pathlib import PurePosixPath
from typing import Any

__all__: list[str] = []


def normalize_relative_path(value: object) -> str:
    """Return one safe normalized project-relative path or an empty string."""
    text = str(value or "").strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    pure = PurePosixPath(text)
    if not text or pure.is_absolute() or ".." in pure.parts:
        return ""
    return pure.as_posix()


def module_name_from_path(relative_path: str) -> str:
    """Convert one Python file path to its importable module form."""
    pure = PurePosixPath(relative_path)
    parts = list(pure.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def package_path(relative_path: str) -> str:
    """Return a stable visual package owner for one module path."""
    parts = list(PurePosixPath(relative_path).parts)
    if not parts:
        return "project_root"
    if parts[0] == "kanda_reasoner_app" and len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def category_for_path(relative_path: str) -> str:
    """Classify one module using a stable visual category meaning."""
    lowered = relative_path.lower()
    if lowered.startswith("tools/") or "validator" in lowered or "validation" in lowered:
        return "validation"
    if any(token in lowered for token in ("gui", "window", "widget", "tab", "shell")):
        return "gui"
    if any(token in lowered for token in ("reasoner", "ai_", "web_ai", "ollama")):
        return "ai"
    if any(
        token in lowered
        for token in (
            "collector",
            "context_bundle",
            "evidence",
            "retriever",
            "symbol_atlas",
            "handoff",
        )
    ):
        return "evidence"
    return "core"


def module_kind(relative_path: str) -> str:
    """Return the graph node kind for one source file."""
    name = PurePosixPath(relative_path).name.lower()
    parts = {part.lower() for part in PurePosixPath(relative_path).parts}
    if (
        (relative_path.startswith("tools/") and name.startswith("validate_"))
        or name.startswith("test_")
        or name.endswith("_test.py")
        or "tests" in parts
    ):
        return "validator"
    return "module"


def make_node(
    node_id: str,
    label: str,
    kind: str,
    category: str,
    position: tuple[float, float, float],
    *,
    relative_path: str = "",
    package: str = "",
    parent_id: str = "",
    summary: str = "",
    size_metric: int = 1,
    metadata: dict[str, Any] | None = None,
    external: bool = False,
) -> dict[str, Any]:
    """Create one complete graph node."""
    return {
        "id": node_id,
        "label": label,
        "kind": kind,
        "relative_path": relative_path,
        "qualified_name": label,
        "package": package,
        "parent_id": parent_id,
        "category": category,
        "size_metric": max(1, int(size_metric or 1)),
        "complexity_metric": 0,
        "incoming_count": 0,
        "outgoing_count": 0,
        "frozen": False,
        "protected": False,
        "external": bool(external),
        "risk_level": "none",
        "summary": summary,
        "position": [round(value, 3) for value in position],
        "metadata": dict(metadata or {}),
    }


def make_edge(
    edge_id: str,
    source: str,
    target: str,
    relationship: str,
    *,
    evidence: str,
    confidence: str = "confirmed",
) -> dict[str, Any]:
    """Create one complete graph relationship."""
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relationship": relationship,
        "directed": relationship != "contains",
        "weight": 1,
        "label": relationship.replace("_", " "),
        "evidence": evidence,
        "validation_status": "evidence_backed",
        "confidence": confidence,
        "metadata": {"source": evidence},
    }


def package_position(index: int, total: int) -> tuple[float, float, float]:
    """Place package centers on a deterministic three-dimensional ring."""
    angle = (2.0 * math.pi * index) / max(1, total)
    radius = 340.0 + 35.0 * (index % 3)
    return (
        radius * math.cos(angle),
        radius * math.sin(angle),
        110.0 * math.sin(angle * 2.0),
    )


def module_position(
    package_center: tuple[float, float, float],
    index: int,
    total: int,
) -> tuple[float, float, float]:
    """Place modules around their package center deterministically."""
    angle = (2.0 * math.pi * index) / max(1, total)
    ring = 55.0 + 18.0 * (index // 18)
    return (
        package_center[0] + ring * math.cos(angle),
        package_center[1] + ring * math.sin(angle),
        package_center[2] + ((index % 7) - 3) * 16.0,
    )


def semantic_child_position(
    parent_position: tuple[float, float, float],
    index: int,
    total: int,
    *,
    layer: int,
) -> tuple[float, float, float]:
    """Place semantic child nodes around one stable visual parent."""
    angle = (2.0 * math.pi * index) / max(1, total)
    radius = 24.0 + 15.0 * max(1, layer) + 8.0 * (index // 18)
    z_offset = ((index % 5) - 2) * (8.0 + 3.0 * max(1, layer))
    return (
        parent_position[0] + radius * math.cos(angle),
        parent_position[1] + radius * math.sin(angle),
        parent_position[2] + z_offset,
    )


def resolve_internal_target(
    target_text: str,
    module_to_node: dict[str, str],
) -> str:
    """Resolve an import target to the nearest internal module node."""
    candidate = str(target_text or "").strip().lstrip(".")
    while candidate:
        node_id = module_to_node.get(candidate)
        if node_id:
            return node_id
        if "." not in candidate:
            break
        candidate = candidate.rsplit(".", 1)[0]
    return ""


def external_name(target_text: str) -> str:
    """Return one stable top-level external dependency name."""
    text = str(target_text or "").strip().lstrip(".")
    return text.split(".", 1)[0] if text else ""


def apply_relationship_counts(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> None:
    """Populate incoming and outgoing relationship counts."""
    by_id = {node["id"]: node for node in nodes}
    for edge in edges:
        source = by_id.get(edge["source"])
        target = by_id.get(edge["target"])
        if source is not None:
            source["outgoing_count"] += 1
        if target is not None:
            target["incoming_count"] += 1
