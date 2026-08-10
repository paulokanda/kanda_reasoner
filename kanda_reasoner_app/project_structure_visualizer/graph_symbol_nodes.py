# project-path: kanda_reasoner_app/project_structure_visualizer/graph_symbol_nodes.py
"""Build bounded class and important-function nodes from complete JSON."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .graph_snapshot_primitives import (
    category_for_path,
    make_edge,
    make_node,
    normalize_relative_path,
    semantic_child_position,
)

__all__ = ["add_symbol_nodes"]

_MAX_CLASSES = 300
_MAX_FUNCTIONS = 360
_MAX_FUNCTIONS_PER_MODULE = 4
_IMPORTANT_PREFIXES = (
    "apply",
    "build",
    "collect",
    "create",
    "execute",
    "load",
    "main",
    "read",
    "resolve",
    "run",
    "save",
    "validate",
    "write",
)


def _safe_int(value: object) -> int:
    """Return one non-negative integer."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _safe_list(value: object) -> list[Any]:
    """Return one list without accepting strings as sequences."""
    return value if isinstance(value, list) else []


def _first_doc_line(record: dict[str, Any]) -> str:
    """Return the first supported documentation summary line."""
    summary = record.get("docstring_summary")
    if isinstance(summary, dict):
        text = str(summary.get("summary") or "").strip()
        if text:
            return text
    for line in str(record.get("docstring") or "").splitlines():
        if line.strip():
            return line.strip()
    return ""


def _symbol_record(
    raw: dict[str, Any],
    *,
    path: str,
    kind: str,
    parent_symbol: str = "",
) -> dict[str, Any] | None:
    """Normalize one complete-JSON class or function record."""
    name = str(raw.get("name") or "").strip()
    qualname = str(raw.get("qualname") or name).strip()
    if not name or not qualname:
        return None
    bases = [str(item).strip() for item in _safe_list(raw.get("bases")) if str(item).strip()]
    methods = [item for item in _safe_list(raw.get("methods")) if isinstance(item, dict)]
    return {
        "path": path,
        "name": name,
        "qualname": qualname,
        "kind": kind,
        "parent_symbol": str(raw.get("parent_symbol") or parent_symbol).strip(),
        "line": _safe_int(raw.get("lineno") or raw.get("line")),
        "line_end": _safe_int(raw.get("line_end") or raw.get("lineno")),
        "bases": bases,
        "methods": methods,
        "method_count": len(methods),
        "is_async": bool(raw.get("is_async")),
        "decorators": [
            str(item).strip()
            for item in _safe_list(raw.get("decorator_names"))
            if str(item).strip()
        ],
        "summary": _first_doc_line(raw),
    }


def _collect_records(
    payload: dict[str, Any],
    module_paths: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Collect class and function records already present in complete JSON."""
    classes: list[dict[str, Any]] = []
    functions: list[dict[str, Any]] = []
    for file_record in _safe_list(payload.get("files")):
        if not isinstance(file_record, dict):
            continue
        path = normalize_relative_path(file_record.get("path"))
        if path not in module_paths:
            continue
        for raw_class in _safe_list(file_record.get("classes")):
            if not isinstance(raw_class, dict):
                continue
            class_record = _symbol_record(raw_class, path=path, kind="class")
            if class_record is None:
                continue
            classes.append(class_record)
            parent = class_record["qualname"]
            for raw_method in class_record["methods"]:
                method = _symbol_record(
                    raw_method,
                    path=path,
                    kind="function",
                    parent_symbol=parent,
                )
                if method is not None:
                    functions.append(method)
        for raw_function in _safe_list(file_record.get("functions")):
            if not isinstance(raw_function, dict):
                continue
            function = _symbol_record(raw_function, path=path, kind="function")
            if function is not None:
                functions.append(function)
    classes.sort(key=lambda item: (item["path"], item["qualname"]))
    functions.sort(key=lambda item: (item["path"], item["qualname"]))
    return classes, functions


def _call_frequencies(payload: dict[str, Any]) -> tuple[Counter[tuple[str, str]], Counter[str]]:
    """Return outgoing and approximate incoming call frequencies."""
    outgoing: Counter[tuple[str, str]] = Counter()
    incoming: Counter[str] = Counter()
    for edge in _safe_list(payload.get("call_edges")):
        if not isinstance(edge, dict):
            continue
        path = normalize_relative_path(edge.get("from_file"))
        source = str(edge.get("from_symbol") or "").strip()
        target = str(edge.get("to_call") or "").strip()
        if path and source:
            for variant in {source, source.split(".")[-1]}:
                outgoing[(path, variant)] += 1
        if target:
            for variant in {target, target.split(".")[-1]}:
                incoming[variant] += 1
    return outgoing, incoming


def _function_score(
    record: dict[str, Any],
    outgoing: Counter[tuple[str, str]],
    incoming: Counter[str],
) -> int:
    """Score one function for bounded semantic visualization."""
    name = record["name"]
    qualname = record["qualname"]
    call_out = max(outgoing[(record["path"], qualname)], outgoing[(record["path"], name)])
    call_in = max(incoming[qualname], incoming[name])
    score = min(call_out, 20) * 2 + min(call_in, 20) * 3
    if not record["parent_symbol"]:
        score += 4
    if not name.startswith("_"):
        score += 3
    if name == "main":
        score += 12
    if name.lower().startswith(_IMPORTANT_PREFIXES):
        score += 4
    if record["summary"]:
        score += 1
    if name.startswith("__") and name.endswith("__"):
        score -= 12
    elif name.startswith("_"):
        score -= 2
    record["call_out"] = call_out
    record["call_in"] = call_in
    record["score"] = score
    return score


def _select_functions(
    functions: list[dict[str, Any]],
    outgoing: Counter[tuple[str, str]],
    incoming: Counter[str],
) -> list[dict[str, Any]]:
    """Select a deterministic bounded set of important functions."""
    ranked = sorted(
        functions,
        key=lambda item: (
            -_function_score(item, outgoing, incoming),
            item["path"],
            item["qualname"],
        ),
    )
    selected: list[dict[str, Any]] = []
    per_module: Counter[str] = Counter()
    for record in ranked:
        if len(selected) >= _MAX_FUNCTIONS:
            break
        if per_module[record["path"]] >= _MAX_FUNCTIONS_PER_MODULE:
            continue
        if int(record.get("score") or 0) < 4:
            continue
        selected.append(record)
        per_module[record["path"]] += 1
    return sorted(selected, key=lambda item: (item["path"], item["qualname"]))


def _node_by_path(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return visual module nodes by safe relative path."""
    return {
        str(node.get("relative_path")): node
        for node in nodes
        if node.get("kind") in {"module", "validator"}
        and str(node.get("relative_path"))
    }


def _append_class_nodes(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    classes: list[dict[str, Any]],
    modules: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Append bounded class nodes and return lookup indexes."""
    selected = classes[:_MAX_CLASSES]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in selected:
        grouped[record["path"]].append(record)
    by_file_name: dict[tuple[str, str], str] = {}
    by_name: dict[str, list[str]] = defaultdict(list)
    records_by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(grouped):
        module = modules.get(path)
        if module is None:
            continue
        records = grouped[path]
        for index, record in enumerate(records):
            node_id = "class:" + path + ":" + record["qualname"]
            position = semantic_child_position(
                tuple(module["position"]),
                index,
                len(records),
                layer=1,
            )
            node = make_node(
                node_id,
                record["name"],
                "class",
                category_for_path(path),
                position,
                relative_path=path,
                package=str(module.get("package") or ""),
                parent_id=str(module["id"]),
                summary=record["summary"] or "Class from canonical complete JSON evidence.",
                size_metric=max(1, record["method_count"]),
                metadata={
                    "source": "files.classes",
                    "line": record["line"],
                    "line_count": max(1, record["line_end"] - record["line"] + 1),
                    "symbol_count": record["method_count"],
                    "bases": record["bases"],
                    "method_count": record["method_count"],
                    "fixture": False,
                },
            )
            node["qualified_name"] = record["qualname"]
            node["complexity_metric"] = max(0, record["line_end"] - record["line"] + 1)
            nodes.append(node)
            edges.append(
                make_edge(
                    "contains:" + module["id"] + ":" + node_id,
                    str(module["id"]),
                    node_id,
                    "contains",
                    evidence="files.classes",
                )
            )
            for key in {record["name"], record["qualname"]}:
                by_file_name[(path, key)] = node_id
                by_name[key].append(node_id)
                by_name[key.split(".")[-1]].append(node_id)
            records_by_id[node_id] = record
    return {
        "by_file_name": by_file_name,
        "by_name": dict(by_name),
        "records_by_id": records_by_id,
    }


def _append_function_nodes(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    functions: list[dict[str, Any]],
    modules: dict[str, dict[str, Any]],
    class_index: dict[str, Any],
) -> dict[str, Any]:
    """Append important-function nodes and return lookup indexes."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in functions:
        grouped[record["path"]].append(record)
    nodes_by_id = {str(node["id"]): node for node in nodes}
    by_file_name: dict[tuple[str, str], str] = {}
    by_name: dict[str, list[str]] = defaultdict(list)
    records_by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(grouped):
        module = modules.get(path)
        if module is None:
            continue
        records = grouped[path]
        for index, record in enumerate(records):
            parent_id = class_index["by_file_name"].get(
                (path, record["parent_symbol"]),
                str(module["id"]),
            )
            parent = nodes_by_id.get(parent_id, module)
            node_id = "function:" + path + ":" + record["qualname"]
            position = semantic_child_position(
                tuple(parent["position"]),
                index,
                len(records),
                layer=2 if parent_id != module["id"] else 1,
            )
            node = make_node(
                node_id,
                record["name"],
                "function",
                category_for_path(path),
                position,
                relative_path=path,
                package=str(module.get("package") or ""),
                parent_id=parent_id,
                summary=record["summary"] or "Important function from canonical complete JSON evidence.",
                size_metric=max(1, record["call_in"] + record["call_out"]),
                metadata={
                    "source": "files.functions",
                    "line": record["line"],
                    "line_count": max(1, record["line_end"] - record["line"] + 1),
                    "symbol_count": 1,
                    "parent_symbol": record["parent_symbol"],
                    "is_async": record["is_async"],
                    "decorators": record["decorators"],
                    "call_in": record["call_in"],
                    "call_out": record["call_out"],
                    "selection_score": record["score"],
                    "fixture": False,
                },
            )
            node["qualified_name"] = record["qualname"]
            node["complexity_metric"] = max(0, record["line_end"] - record["line"] + 1)
            nodes.append(node)
            nodes_by_id[node_id] = node
            edges.append(
                make_edge(
                    "contains:" + parent_id + ":" + node_id,
                    parent_id,
                    node_id,
                    "contains",
                    evidence="files.functions",
                )
            )
            for key in {record["name"], record["qualname"]}:
                by_file_name[(path, key)] = node_id
                by_name[key].append(node_id)
                by_name[key.split(".")[-1]].append(node_id)
            records_by_id[node_id] = record
    return {
        "by_file_name": by_file_name,
        "by_name": dict(by_name),
        "records_by_id": records_by_id,
    }


def add_symbol_nodes(
    payload: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    """Append bounded class/function nodes and return semantic indexes."""
    modules = _node_by_path(nodes)
    classes, functions = _collect_records(payload, set(modules))
    outgoing, incoming = _call_frequencies(payload)
    selected_functions = _select_functions(functions, outgoing, incoming)
    class_index = _append_class_nodes(nodes, edges, classes, modules)
    function_index = _append_function_nodes(
        nodes,
        edges,
        selected_functions,
        modules,
        class_index,
    )
    return {
        "modules": modules,
        "classes": class_index,
        "functions": function_index,
        "class_count": len(class_index["records_by_id"]),
        "function_count": len(function_index["records_by_id"]),
        "available_class_count": len(classes),
        "available_function_count": len(functions),
    }
