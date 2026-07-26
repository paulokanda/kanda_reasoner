# project-path: kanda_reasoner_app/project_structure_visualizer/graph_semantic_edges.py
"""Add bounded inheritance and call relationships from complete JSON."""

from __future__ import annotations

from typing import Any

from .graph_snapshot_primitives import make_edge, normalize_relative_path

__all__ = ["add_semantic_edges"]

_MAX_CALL_EDGES = 1600
_MAX_INHERITANCE_EDGES = 400


def _safe_list(value: object) -> list[Any]:
    """Return one list without treating strings as sequences."""
    return value if isinstance(value, list) else []


def _name_variants(value: object) -> list[str]:
    """Return stable symbol-name variants from one call or base expression."""
    text = str(value or "").strip()
    if not text:
        return []
    text = text.split("(", 1)[0].strip()
    text = text.split("[", 1)[0].strip()
    variants = [text]
    if text.startswith("self.") or text.startswith("cls."):
        variants.append(text.split(".", 1)[1])
    if "." in text:
        variants.append(text.split(".")[-1])
    result: list[str] = []
    for item in variants:
        if item and item not in result:
            result.append(item)
    return result


def _unique_global(index: dict[str, Any], variants: list[str]) -> str:
    """Resolve only an unambiguous global symbol target."""
    for variant in variants:
        matches = list(dict.fromkeys(index.get("by_name", {}).get(variant, [])))
        if len(matches) == 1:
            return matches[0]
    return ""


def _same_file(index: dict[str, Any], path: str, variants: list[str]) -> str:
    """Resolve one symbol target within the originating file."""
    lookup = index.get("by_file_name", {})
    for variant in variants:
        node_id = lookup.get((path, variant))
        if node_id:
            return str(node_id)
    return ""


def _resolve_symbol(
    path: str,
    value: object,
    primary_index: dict[str, Any],
    secondary_index: dict[str, Any] | None = None,
) -> str:
    """Resolve one semantic target with same-file precedence."""
    variants = _name_variants(value)
    if not variants:
        return ""
    node_id = _same_file(primary_index, path, variants)
    if node_id:
        return node_id
    if secondary_index is not None:
        node_id = _same_file(secondary_index, path, variants)
        if node_id:
            return node_id
    node_id = _unique_global(primary_index, variants)
    if node_id:
        return node_id
    if secondary_index is not None:
        return _unique_global(secondary_index, variants)
    return ""


def _add_inheritance_edges(
    edges: list[dict[str, Any]],
    symbol_index: dict[str, Any],
) -> int:
    """Add internal inheritance edges for selected class nodes."""
    class_index = symbol_index["classes"]
    seen: set[tuple[str, str]] = set()
    count = 0
    for source_id, record in sorted(class_index["records_by_id"].items()):
        for base in record.get("bases", []):
            target_id = _resolve_symbol(
                record["path"],
                base,
                class_index,
            )
            key = (source_id, target_id)
            if not target_id or source_id == target_id or key in seen:
                continue
            seen.add(key)
            edges.append(
                make_edge(
                    "inherits:" + source_id + ":" + target_id,
                    source_id,
                    target_id,
                    "inherits",
                    evidence="files.classes.bases: " + str(base),
                    confidence="derived",
                )
            )
            count += 1
            if count >= _MAX_INHERITANCE_EDGES:
                return count
    return count


def _add_call_edges(
    payload: dict[str, Any],
    edges: list[dict[str, Any]],
    symbol_index: dict[str, Any],
) -> int:
    """Add deduplicated calls between selected functions and classes."""
    functions = symbol_index["functions"]
    classes = symbol_index["classes"]
    seen: set[tuple[str, str]] = set()
    count = 0
    for raw_edge in _safe_list(payload.get("call_edges")):
        if not isinstance(raw_edge, dict):
            continue
        path = normalize_relative_path(raw_edge.get("from_file"))
        source_id = _resolve_symbol(
            path,
            raw_edge.get("from_symbol"),
            functions,
        )
        target_id = _resolve_symbol(
            path,
            raw_edge.get("to_call"),
            functions,
            classes,
        )
        key = (source_id, target_id)
        if not source_id or not target_id or source_id == target_id or key in seen:
            continue
        seen.add(key)
        line = str(raw_edge.get("line") or "").strip()
        evidence = "call_edges"
        if line:
            evidence += ": line " + line
        edges.append(
            make_edge(
                "calls:" + source_id + ":" + target_id,
                source_id,
                target_id,
                "calls",
                evidence=evidence,
                confidence="derived",
            )
        )
        count += 1
        if count >= _MAX_CALL_EDGES:
            break
    return count


def add_semantic_edges(
    payload: dict[str, Any],
    edges: list[dict[str, Any]],
    symbol_index: dict[str, Any],
) -> dict[str, int]:
    """Add bounded inheritance and call relationships."""
    inheritance_count = _add_inheritance_edges(edges, symbol_index)
    call_count = _add_call_edges(payload, edges, symbol_index)
    return {
        "call_edge_count": call_count,
        "inheritance_edge_count": inheritance_count,
    }
