# project-path: kanda_reasoner_app/reasoner_context_collector/collector_boundaries.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "CONTROLLER_KEYWORDS",
    "DOMAIN_KEYWORDS",
    "SERVICE_KEYWORDS",
    "build_boundary_handoffs",
    "build_boundary_index",
    "build_boundary_summary",
]

from typing import Any


CONTROLLER_KEYWORDS = (
    "window",
    "dialog",
    "controller",
    "manager",
    "handler",
    "toolbar",
    "widget",
    "view",
    "screen",
    "tab",
)

SERVICE_KEYWORDS = (
    "service",
    "builder",
    "loader",
    "exporter",
    "importer",
    "writer",
    "reader",
    "resolver",
    "provider",
    "runner",
    "engine",
    "processor",
)

DOMAIN_KEYWORDS = (
    "model",
    "domain",
    "entity",
    "schema",
    "state",
    "config",
    "record",
    "signal",
    "analysis",
)


def _normalize_text(value: Any) -> str:
    """Support normalize text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(value or "").strip().lower()


def _safe_bucket_for_file(
    file_path: str,
    files_payload: list[dict[str, Any]],
) -> str:
    """Support safe bucket for file behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for record in files_payload:
        if str(record.get("path", "")) == file_path:
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"


def _safe_module_centrality(
    file_path: str,
    module_centrality_index: dict[str, Any],
) -> float:
    """Support safe module centrality behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    module_centrality_index : dict[str, Any]
        The module centrality index value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    payload = module_centrality_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0
    score = payload.get("centrality_score", 0.0)
    try:
        return float(score)
    except (TypeError, ValueError):
        return 0.0


def _guess_boundary_role(record: dict[str, Any]) -> str:
    """Support guess boundary role behavior.
    
    Parameters
    ----------
    record : dict[str, Any]
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    path_text = _normalize_text(record.get("path", ""))
    module_name = _normalize_text(record.get("module_name", ""))
    primary_role = _normalize_text(record.get("primary_role", ""))
    semantic_roles = record.get("semantic_roles", [])
    semantic_text = " ".join(_normalize_text(item) for item in semantic_roles)

    joined = " ".join([path_text, module_name, primary_role, semantic_text])

    if any(keyword in joined for keyword in CONTROLLER_KEYWORDS):
        return "controller"

    if any(keyword in joined for keyword in SERVICE_KEYWORDS):
        return "service"

    if any(keyword in joined for keyword in DOMAIN_KEYWORDS):
        return "domain"

    if "ui_qt" in path_text:
        return "controller"

    if "runtime" in path_text or "loader" in path_text or "builder" in path_text:
        return "service"

    if "config" in path_text or "state" in path_text or "schema" in path_text:
        return "domain"

    return "unclassified"


def build_boundary_index(
    files_payload: list[dict[str, Any]],
    ui_action_index: dict[str, Any],
    module_centrality_index: dict[str, Any],
    call_edges: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a boundary index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    ui_action_index : dict[str, Any]
        The ui action index value.
    module_centrality_index : dict[str, Any]
        The module centrality index value.
    call_edges : list[dict[str, Any]]
        The call edges value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    ui_source_files: set[str] = set()
    ui_target_files: set[str] = set()

    for payload in ui_action_index.values():
        if not isinstance(payload, dict):
            continue

        for file_path in payload.get("source_files", []):
            if file_path:
                ui_source_files.add(str(file_path))

        for file_path in payload.get("target_files", []):
            if file_path:
                ui_target_files.add(str(file_path))

    outbound_call_counts: dict[str, int] = {}
    inbound_call_counts: dict[str, int] = {}

    for edge in call_edges:
        if not isinstance(edge, dict):
            continue

        from_file = str(edge.get("from_file", "") or "")
        to_call = str(edge.get("to_call", "") or "")

        if from_file:
            outbound_call_counts[from_file] = outbound_call_counts.get(from_file, 0) + 1

        if to_call:
            inbound_call_counts[to_call] = inbound_call_counts.get(to_call, 0) + 1

    output: dict[str, dict[str, Any]] = {}

    for record in files_payload:
        file_path = str(record.get("path", "") or "")
        if not file_path:
            continue

        boundary_role = _guess_boundary_role(record)
        bucket = _safe_bucket_for_file(file_path, files_payload)
        centrality_score = _safe_module_centrality(file_path, module_centrality_index)

        methods_count = 0
        for cls in record.get("classes", []):
            if isinstance(cls, dict):
                methods_count += len(cls.get("methods", []))

        function_count = len(record.get("functions", []))
        class_count = len(record.get("classes", []))
        symbol_count = function_count + class_count + methods_count

        output[file_path] = {
            "file": file_path,
            "module_name": str(record.get("module_name", "") or ""),
            "boundary_role": boundary_role,
            "bucket": bucket,
            "primary_role": str(record.get("primary_role", "") or ""),
            "secondary_roles": record.get("secondary_roles", []),
            "semantic_roles": record.get("semantic_roles", []),
            "centrality_score": centrality_score,
            "function_count": function_count,
            "class_count": class_count,
            "method_count": methods_count,
            "symbol_count": symbol_count,
            "ui_source": file_path in ui_source_files,
            "ui_target": file_path in ui_target_files,
            "outbound_call_count": outbound_call_counts.get(file_path, 0),
            "entry_candidate": bool(record.get("entry_markers", [])),
        }

    return dict(sorted(output.items()))


def build_boundary_summary(
    boundary_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a boundary summary.
    
    Parameters
    ----------
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    role_counts = {
        "controller": 0,
        "service": 0,
        "domain": 0,
        "unclassified": 0,
    }

    ui_source_count = 0
    ui_target_count = 0

    bucket_frequency: dict[str, int] = {}

    for payload in boundary_index.values():
        if not isinstance(payload, dict):
            continue

        role = str(payload.get("boundary_role", "unclassified") or "unclassified")
        if role not in role_counts:
            role = "unclassified"
        role_counts[role] += 1

        if bool(payload.get("ui_source")):
            ui_source_count += 1

        if bool(payload.get("ui_target")):
            ui_target_count += 1

        bucket = str(payload.get("bucket", "") or "general")
        bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1

    sorted_buckets = sorted(
        bucket_frequency.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return {
        "file_count": len(boundary_index),
        "controller_file_count": role_counts["controller"],
        "service_file_count": role_counts["service"],
        "domain_file_count": role_counts["domain"],
        "unclassified_file_count": role_counts["unclassified"],
        "ui_source_file_count": ui_source_count,
        "ui_target_file_count": ui_target_count,
        "bucket_frequency": dict(sorted_buckets),
    }


def build_boundary_handoffs(
    boundary_index: dict[str, dict[str, Any]],
    call_edges: list[dict[str, Any]],
    symbol_index: dict[str, Any],
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Build a boundary handoffs.
    
    Parameters
    ----------
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    call_edges : list[dict[str, Any]]
        The call edges value.
    symbol_index : dict[str, Any]
        The symbol index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    handoffs: list[dict[str, Any]] = []

    for edge in call_edges:
        if not isinstance(edge, dict):
            continue

        from_file = str(edge.get("from_file", "") or "")
        from_symbol = str(edge.get("from_symbol", "") or "")
        to_call = str(edge.get("to_call", "") or "")
        line = edge.get("line")

        if not from_file or not to_call:
            continue

        source_boundary = boundary_index.get(from_file, {})
        if not isinstance(source_boundary, dict):
            source_boundary = {}

        target_symbol_payload = symbol_index.get(to_call, {})
        if not isinstance(target_symbol_payload, dict):
            target_symbol_payload = {}

        target_file = str(target_symbol_payload.get("file", "") or "")
        if not target_file:
            continue

        target_boundary = boundary_index.get(target_file, {})
        if not isinstance(target_boundary, dict):
            target_boundary = {}

        source_role = str(source_boundary.get("boundary_role", "") or "")
        target_role = str(target_boundary.get("boundary_role", "") or "")

        if not source_role or not target_role:
            continue

        if from_file == target_file and source_role == target_role:
            continue

        if source_role == target_role:
            continue

        handoffs.append(
            {
                "from_file": from_file,
                "from_symbol": from_symbol,
                "from_role": source_role,
                "to_file": target_file,
                "to_symbol": to_call,
                "to_role": target_role,
                "line": line,
                "handoff_type": f"{source_role}_to_{target_role}",
                "cross_file": from_file != target_file,
            }
        )

    handoffs.sort(
        key=lambda item: (
            0 if item.get("cross_file") else 1,
            item.get("handoff_type", ""),
            item.get("from_file", ""),
            item.get("to_file", ""),
            item.get("to_symbol", ""),
        )
    )

    return handoffs[:limit]
