# project-path: kanda_reasoner_app/project_structure_visualizer/graph_layout_state.py
"""Semantic zones and Project Support-owned position caching for the graph."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    PROJECT_STRUCTURE_3D_STATE_DIR,
    ensure_show_project_lifecycle_manifest,
)
from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
    project_support_root_blockers,
    resolve_project_tool_boundary_identity,
)

from .graph_schema import validate_graph_snapshot

__all__ = ["stabilize_project_graph_layout"]

_CACHE_DIR = PROJECT_STRUCTURE_3D_STATE_DIR
_CACHE_FILE = "layout_positions_v1.json"
_MAX_CACHE_NODES = 10_000
_ZONE_CENTERS: dict[str, tuple[float, float, float]] = {
    "core": (0.0, 0.0, 0.0),
    "gui": (360.0, -235.0, 55.0),
    "ai": (-360.0, -235.0, 85.0),
    "validation": (360.0, 260.0, -45.0),
    "evidence": (-360.0, 260.0, -25.0),
    "external": (0.0, 0.0, 230.0),
}
_ZONE_LABELS = {
    "core": "Core",
    "gui": "GUI",
    "ai": "AI / Reasoner",
    "validation": "Validation",
    "evidence": "Evidence",
    "external": "External",
}


def _numeric_position(value: object) -> list[float] | None:
    """Return one bounded three-number position or ``None``."""
    if not isinstance(value, list) or len(value) != 3:
        return None
    if not all(isinstance(item, (int, float)) for item in value):
        return None
    result = [round(float(item), 3) for item in value]
    if any(abs(item) > 100_000 for item in result):
        return None
    return result


def _apply_semantic_zones(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return a copy positioned into deterministic responsibility zones."""
    result = deepcopy(snapshot)
    nodes = list(result.get("nodes", []))
    grouped: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        category = str(node.get("category") or "core")
        if category not in _ZONE_CENTERS:
            category = "core"
        node["metadata"] = dict(node.get("metadata", {}))
        node["metadata"]["semantic_zone"] = category
        if node.get("kind") not in {"project", "external"}:
            grouped.setdefault(category, []).append(node)

    for category, members in grouped.items():
        positions = [
            _numeric_position(node.get("position")) or [0.0, 0.0, 0.0]
            for node in members
        ]
        count = max(1, len(positions))
        centroid = [
            sum(position[index] for position in positions) / count
            for index in range(3)
        ]
        target = _ZONE_CENTERS[category]
        for node, position in zip(members, positions):
            scale = 0.62 if node.get("kind") == "package" else 0.54
            node["position"] = [
                round(target[index] + (position[index] - centroid[index]) * scale, 3)
                for index in range(3)
            ]

    for node in nodes:
        if node.get("kind") == "project":
            node["position"] = [0.0, 0.0, 0.0]
        elif node.get("kind") == "external":
            original = _numeric_position(node.get("position")) or [0.0, 0.0, 0.0]
            node["position"] = [original[0], original[1], 230.0]

    result["nodes"] = nodes
    layout = dict(result.get("layout", {}))
    layout.update(
        {
            "engine": "deterministic_semantic_zone_layout_v1d",
            "stable": True,
            "coordinates_are_authoritative": False,
            "semantic_zones": [
                {
                    "id": category,
                    "label": _ZONE_LABELS[category],
                    "center": list(center),
                }
                for category, center in _ZONE_CENTERS.items()
            ],
        }
    )
    result["layout"] = layout
    return result


def _cache_path(project_root: Path) -> tuple[Path, str, str]:
    """Return the canonical cache path and stable Project identity fields."""
    identity = resolve_project_tool_boundary_identity(project_root)
    support_root = canonical_project_support_root(project_root)
    blockers = project_support_root_blockers(project_root, support_root)
    if blockers:
        raise RuntimeError("Unsafe Project Support layout owner: " + ",".join(blockers))
    path = support_root / _CACHE_DIR / _CACHE_FILE
    return path, identity.active_project_id, identity.active_project_root_fingerprint


def _read_cached_positions(
    path: Path,
    project_id: str,
    root_fingerprint: str,
) -> dict[str, list[float]]:
    """Read only positions belonging to the current canonical Project."""
    if not path.is_file():
        return {}
    loaded = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    if not isinstance(loaded, dict) or loaded.get("schema_version") != "1.0":
        return {}
    if loaded.get("project_id") != project_id:
        return {}
    if loaded.get("project_root_fingerprint") != root_fingerprint:
        return {}
    raw_positions = loaded.get("positions")
    if not isinstance(raw_positions, dict):
        return {}
    result: dict[str, list[float]] = {}
    for node_id in sorted(raw_positions)[:_MAX_CACHE_NODES]:
        position = _numeric_position(raw_positions.get(node_id))
        if position is not None:
            result[str(node_id)] = position
    return result


def _write_cached_positions(
    path: Path,
    project_slug: str,
    project_id: str,
    root_fingerprint: str,
    nodes: list[dict[str, Any]],
) -> bool:
    """Atomically persist presentation-only node positions when changed."""
    positions: dict[str, list[float]] = {}
    for node in nodes[:_MAX_CACHE_NODES]:
        node_id = str(node.get("id") or "").strip()
        position = _numeric_position(node.get("position"))
        if node_id and position is not None:
            positions[node_id] = position
    document = {
        "schema_version": "1.0",
        "owner": "project_support.project_structure_3d",
        "authority": "presentation_cache_only",
        "project_slug": project_slug,
        "project_id": project_id,
        "project_root_fingerprint": root_fingerprint,
        "layout_version": "semantic_zone_layout_v1d",
        "positions": positions,
    }
    text = json.dumps(document, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    if path.is_file():
        try:
            if path.read_text(encoding="utf-8", errors="strict") == text:
                return False
        except OSError:
            pass
    ensure_show_project_lifecycle_manifest(path.parent.parent)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    try:
        temporary.write_text(text, encoding="utf-8", errors="strict", newline="\n")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return True


def stabilize_project_graph_layout(
    snapshot: dict[str, Any],
    project_root: Path | str,
    *,
    persist: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply zones, reuse cached positions, and optionally persist the result."""
    root = Path(project_root).expanduser().resolve()
    result = _apply_semantic_zones(snapshot)
    cache_status: dict[str, Any] = {
        "owner": "project_support.project_structure_3d",
        "path_hint": f"{_CACHE_DIR}/{_CACHE_FILE}",
        "authority": "presentation_cache_only",
        "status": "disabled",
        "applied_count": 0,
        "written": False,
    }
    if bool(result.get("statistics", {}).get("fixture")):
        result["layout"]["position_cache"] = cache_status
        validate_graph_snapshot(result)
        return result, cache_status

    try:
        path, project_id, fingerprint = _cache_path(root)
        cached = _read_cached_positions(path, project_id, fingerprint)
        by_id = {str(node.get("id")): node for node in result.get("nodes", [])}
        applied = 0
        for node_id, position in cached.items():
            node = by_id.get(node_id)
            if node is not None:
                node["position"] = position
                applied += 1
        cache_status.update(
            {
                "status": "loaded" if cached else "created",
                "applied_count": applied,
            }
        )
        if persist:
            cache_status["written"] = _write_cached_positions(
                path,
                root.name,
                project_id,
                fingerprint,
                list(result.get("nodes", [])),
            )
    except (OSError, RuntimeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        cache_status.update(
            {
                "status": "unavailable",
                "error": str(exc)[:240],
            }
        )

    result["layout"]["position_cache"] = cache_status
    validate_graph_snapshot(result)
    return result, cache_status
