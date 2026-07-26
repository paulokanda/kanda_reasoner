# project-path: kanda_reasoner_app/project_structure_visualizer/graph_protection_status.py
"""Apply read-only test and Freeze protection evidence to graph nodes."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

from kanda_reasoner_app.freeze_after_update.freeze_state import build_freezes

from .graph_snapshot_primitives import make_edge, normalize_relative_path

__all__ = ["apply_protection_evidence"]

_MAX_VALIDATION_EDGES = 600
_MAX_PROTECTION_EDGES = 300


def _safe_list(value: object) -> list[Any]:
    """Return one list without accepting strings as sequences."""
    return value if isinstance(value, list) else []


def _module_nodes(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return module and validator nodes by project-relative path."""
    return {
        str(node.get("relative_path")): node
        for node in nodes
        if node.get("kind") in {"module", "validator"}
        and str(node.get("relative_path"))
    }


def _test_links(payload: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Return source/test/confidence triples from current or legacy evidence."""
    links: list[tuple[str, str, str]] = []
    current = payload.get("web_ai_test_protection_index")
    if isinstance(current, dict):
        for source_key in sorted(current):
            record = current.get(source_key)
            if not isinstance(record, dict):
                continue
            source = normalize_relative_path(record.get("source_file") or source_key)
            for item in _safe_list(record.get("linked_tests")):
                if isinstance(item, dict):
                    test_path = normalize_relative_path(item.get("test_file"))
                    confidence = str(item.get("confidence") or "derived")
                else:
                    test_path = normalize_relative_path(item)
                    confidence = "derived"
                if source and test_path:
                    links.append((source, test_path, confidence))
        if links:
            return links
    for record in _safe_list(payload.get("test_links")):
        if not isinstance(record, dict):
            continue
        source = normalize_relative_path(record.get("source_file"))
        for item in _safe_list(record.get("linked_tests")):
            test_path = normalize_relative_path(
                item.get("test_file") if isinstance(item, dict) else item
            )
            if source and test_path:
                links.append((source, test_path, "derived"))
    return links


def _apply_test_protection(
    payload: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, int]:
    """Mark test-protected modules and add validator relationships."""
    modules = _module_nodes(nodes)
    seen: set[tuple[str, str]] = set()
    validated_nodes: set[str] = set()
    edge_count = 0
    for source_path, test_path, confidence in _test_links(payload):
        source = modules.get(source_path)
        test = modules.get(test_path)
        if source is None or test is None:
            continue
        key = (str(test["id"]), str(source["id"]))
        if key in seen:
            continue
        seen.add(key)
        source["protected"] = True
        source_metadata = source.get("metadata")
        if isinstance(source_metadata, dict):
            source_metadata["test_protected"] = True
            linked = source_metadata.setdefault("linked_tests", [])
            if isinstance(linked, list) and test_path not in linked:
                linked.append(test_path)
        test["kind"] = "validator"
        edges.append(
            make_edge(
                "validates:" + key[0] + ":" + key[1],
                key[0],
                key[1],
                "validates",
                evidence="web_ai_test_protection_index: " + confidence,
                confidence="derived",
            )
        )
        validated_nodes.add(key[1])
        edge_count += 1
        if edge_count >= _MAX_VALIDATION_EDGES:
            break
    return {
        "validation_edge_count": edge_count,
        "test_protected_node_count": len(validated_nodes),
    }


def _normalize_protected_path(value: object) -> str:
    """Return one source-relevant protected path or an empty string."""
    text = normalize_relative_path(value)
    if not text:
        return ""
    lowered = text.lower()
    if lowered.startswith("project_freeze_after_update/"):
        return ""
    if lowered.startswith("frozen_features_memory/"):
        return ""
    return text.rstrip("/")


def _path_is_protected(relative_path: str, protected_path: str) -> bool:
    """Return whether one node path is owned by a protected file/folder."""
    node = PurePosixPath(relative_path)
    protected = PurePosixPath(protected_path)
    if node == protected:
        return True
    return len(node.parts) > len(protected.parts) and node.parts[: len(protected.parts)] == protected.parts


def _apply_freeze_protection(
    project_root: object,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, int]:
    """Read existing Freeze entries and mark matching source nodes."""
    try:
        freezes = build_freezes(project_root)
    except (OSError, ValueError, TypeError):
        freezes = []
    active: list[tuple[str, str]] = []
    for freeze in freezes:
        if not isinstance(freeze, dict) or freeze.get("superseded_by"):
            continue
        freeze_id = str(freeze.get("freeze_id") or "").strip()
        for raw_path in _safe_list(freeze.get("protected_paths")):
            protected_path = _normalize_protected_path(raw_path)
            if freeze_id and protected_path:
                active.append((freeze_id, protected_path))
    project_id = next(
        (str(node["id"]) for node in nodes if node.get("kind") == "project"),
        "",
    )
    frozen_nodes: set[str] = set()
    edge_count = 0
    for node in nodes:
        relative_path = str(node.get("relative_path") or "")
        if not relative_path:
            continue
        matching = sorted(
            {
                freeze_id
                for freeze_id, protected_path in active
                if _path_is_protected(relative_path, protected_path)
            }
        )
        if not matching:
            continue
        node["frozen"] = True
        node["protected"] = True
        metadata = node.get("metadata")
        if isinstance(metadata, dict):
            metadata["freeze_ids"] = matching
        frozen_nodes.add(str(node["id"]))
        if project_id and edge_count < _MAX_PROTECTION_EDGES:
            edges.append(
                make_edge(
                    "protects:" + project_id + ":" + str(node["id"]),
                    project_id,
                    str(node["id"]),
                    "protects",
                    evidence="freeze_after_update.frozen_features_memory",
                    confidence="confirmed",
                )
            )
            edge_count += 1
    return {
        "protection_edge_count": edge_count,
        "frozen_node_count": len(frozen_nodes),
        "freeze_entry_count": len(freezes),
    }


def apply_protection_evidence(
    project_root: object,
    payload: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, int]:
    """Apply read-only test and Freeze protection evidence."""
    result = _apply_test_protection(payload, nodes, edges)
    result.update(_apply_freeze_protection(project_root, nodes, edges))
    return result
