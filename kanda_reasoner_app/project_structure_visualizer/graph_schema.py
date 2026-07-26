# project-path: kanda_reasoner_app/project_structure_visualizer/graph_schema.py
"""Immutable graph snapshot validation for Project Structure 3D."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any

__all__ = ["graph_snapshot_json", "validate_graph_snapshot"]

_REQUIRED_TOP_LEVEL = {
    "schema_version",
    "project_identity",
    "source_provenance",
    "nodes",
    "edges",
    "clusters",
    "legend",
    "layout",
    "statistics",
}
_REQUIRED_NODE_KEYS = {
    "id",
    "label",
    "kind",
    "relative_path",
    "category",
    "summary",
    "position",
    "metadata",
}
_REQUIRED_EDGE_KEYS = {
    "id",
    "source",
    "target",
    "relationship",
    "directed",
    "confidence",
    "metadata",
}
_ALLOWED_NODE_KINDS = {
    "project",
    "package",
    "module",
    "class",
    "function",
    "validator",
    "external",
}
_ALLOWED_RELATIONSHIPS = {
    "contains",
    "imports",
    "calls",
    "inherits",
    "validates",
    "invokes",
    "protects",
    "depends_on",
}
_ALLOWED_CONFIDENCE = {
    "confirmed",
    "derived",
    "inferred",
    "documentation_only",
    "unresolved",
}


def _require_mapping(value: object, field_name: str) -> Mapping[str, Any]:
    """Return one mapping or raise a clear schema error."""
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def _require_sequence(value: object, field_name: str) -> Sequence[Any]:
    """Return one non-string sequence or raise a clear schema error."""
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field_name} must be an array")
    return value


def _validate_relative_path(value: object, node_id: str) -> None:
    """Reject absolute, drive-qualified, and traversal paths."""
    path_text = str(value or "")
    if not path_text:
        return
    windows_path = PureWindowsPath(path_text)
    posix_path = PurePosixPath(path_text.replace("\\", "/"))
    if windows_path.is_absolute() or windows_path.drive:
        raise ValueError(f"node {node_id} exposes an absolute path")
    if posix_path.is_absolute() or ".." in posix_path.parts:
        raise ValueError(f"node {node_id} contains an unsafe relative path")


def validate_graph_snapshot(snapshot: Mapping[str, Any]) -> None:
    """Validate one renderer-ready immutable graph snapshot."""
    missing = sorted(_REQUIRED_TOP_LEVEL - set(snapshot))
    if missing:
        raise ValueError("graph snapshot missing: " + ", ".join(missing))
    if str(snapshot.get("schema_version")) != "1.0":
        raise ValueError("unsupported graph schema version")

    project_identity = _require_mapping(
        snapshot.get("project_identity"),
        "project_identity",
    )
    if not str(project_identity.get("slug", "")).strip():
        raise ValueError("project_identity.slug is required")

    nodes = _require_sequence(snapshot.get("nodes"), "nodes")
    edges = _require_sequence(snapshot.get("edges"), "edges")
    node_ids: set[str] = set()
    edge_ids: set[str] = set()

    for index, raw_node in enumerate(nodes):
        node = _require_mapping(raw_node, f"nodes[{index}]")
        node_missing = sorted(_REQUIRED_NODE_KEYS - set(node))
        if node_missing:
            raise ValueError(
                f"nodes[{index}] missing: " + ", ".join(node_missing)
            )
        node_id = str(node.get("id", "")).strip()
        if not node_id or node_id in node_ids:
            raise ValueError(f"duplicate or empty node ID: {node_id!r}")
        node_ids.add(node_id)
        if node.get("kind") not in _ALLOWED_NODE_KINDS:
            raise ValueError(f"node {node_id} has an invalid kind")
        _validate_relative_path(node.get("relative_path"), node_id)
        position = _require_sequence(node.get("position"), f"{node_id}.position")
        if len(position) != 3 or not all(
            isinstance(value, (int, float)) for value in position
        ):
            raise ValueError(f"node {node_id} requires numeric x, y, z")
        _require_mapping(node.get("metadata"), f"{node_id}.metadata")

    for index, raw_edge in enumerate(edges):
        edge = _require_mapping(raw_edge, f"edges[{index}]")
        edge_missing = sorted(_REQUIRED_EDGE_KEYS - set(edge))
        if edge_missing:
            raise ValueError(
                f"edges[{index}] missing: " + ", ".join(edge_missing)
            )
        edge_id = str(edge.get("id", "")).strip()
        if not edge_id or edge_id in edge_ids:
            raise ValueError(f"duplicate or empty edge ID: {edge_id!r}")
        edge_ids.add(edge_id)
        source = str(edge.get("source", ""))
        target = str(edge.get("target", ""))
        if source not in node_ids or target not in node_ids:
            raise ValueError(f"edge {edge_id} references a missing endpoint")
        if edge.get("relationship") not in _ALLOWED_RELATIONSHIPS:
            raise ValueError(f"edge {edge_id} has an invalid relationship")
        if edge.get("confidence") not in _ALLOWED_CONFIDENCE:
            raise ValueError(f"edge {edge_id} has invalid confidence")
        _require_mapping(edge.get("metadata"), f"{edge_id}.metadata")


def graph_snapshot_json(snapshot: Mapping[str, Any]) -> str:
    """Serialize a validated graph snapshot for safe script embedding."""
    validate_graph_snapshot(snapshot)
    payload = json.dumps(
        snapshot,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return payload.replace("</", "<\\/")
