# project-path: kanda_reasoner_app/reasoner_context_collector/collector_event_propagation.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


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


def _safe_role_for_file(
    file_path: str,
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    """Support safe role for file behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    return str(payload.get("boundary_role", "unclassified") or "unclassified")


def _safe_centrality_score(
    file_path: str,
    module_centrality_index: dict[str, dict[str, Any]],
) -> float:
    """Support safe centrality score behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    payload = module_centrality_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0

    for key in ("centrality_score", "score", "total_score"):
        value = payload.get(key)
        try:
            return float(value)
        except Exception:
            continue
    return 0.0


def _iter_qt_records(qt_signal_map: Any) -> list[dict[str, Any]]:
    """Support iter qt records behavior.
    
    Parameters
    ----------
    qt_signal_map : Any
        The qt signal map value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    if isinstance(qt_signal_map, list):
        return [item for item in qt_signal_map if isinstance(item, dict)]

    if isinstance(qt_signal_map, dict):
        output: list[dict[str, Any]] = []
        for value in qt_signal_map.values():
            if isinstance(value, list):
                output.extend(item for item in value if isinstance(item, dict))
        return output

    return []


def _resolve_target_file(
    target_symbol: str,
    symbol_index: dict[str, dict[str, Any]],
) -> str:
    """Support resolve target file behavior.
    
    Parameters
    ----------
    target_symbol : str
        The target symbol value.
    symbol_index : dict[str, dict[str, Any]]
        The symbol index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not target_symbol or target_symbol == "unknown":
        return ""

    direct = symbol_index.get(target_symbol, {})
    if isinstance(direct, dict) and direct.get("file"):
        return str(direct.get("file", "") or "")

    stripped = target_symbol
    if stripped.startswith("self."):
        stripped = stripped[5:]

    for symbol_name, payload in symbol_index.items():
        if not isinstance(payload, dict):
            continue
        if symbol_name == stripped or symbol_name.endswith("." + stripped):
            return str(payload.get("file", "") or "")

    return ""


def build_event_propagation_index(
    qt_signal_map: Any,
    ui_action_index: dict[str, dict[str, Any]],
    symbol_index: dict[str, dict[str, Any]],
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a event propagation index.
    
    Parameters
    ----------
    qt_signal_map : Any
        The qt signal map value.
    ui_action_index : dict[str, dict[str, Any]]
        The ui action index value.
    symbol_index : dict[str, dict[str, Any]]
        The symbol index value.
    files_payload : list[dict[str, Any]]
        The files payload value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}

    for record in files_payload:
        file_path = str(record.get("path", "") or "")
        if not file_path:
            continue

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket_for_file(file_path, files_payload),
            "boundary_role": _safe_role_for_file(file_path, boundary_index),
            "centrality_score": _safe_centrality_score(
                file_path,
                module_centrality_index,
            ),
            "signal_emit_count": 0,
            "resolved_signal_target_count": 0,
            "ui_action_reference_count": 0,
            "fanout_file_count": 0,
            "fanout_bucket_count": 0,
            "fanout_role_count": 0,
            "fanout_files": [],
            "fanout_buckets": [],
            "fanout_roles": [],
            "source_symbols": [],
            "signal_names": [],
            "target_symbols": [],
        }

    qt_records = _iter_qt_records(qt_signal_map)

    for record in qt_records:
        source_file = str(
            record.get("source_file", record.get("file", "")) or ""
        ).strip()
        if not source_file or source_file not in output:
            continue

        source_symbol = str(
            record.get("source_symbol", record.get("source", "")) or ""
        ).strip()
        signal_name = str(
            record.get("signal_name", record.get("signal", "")) or ""
        ).strip()
        target_symbol = str(record.get("target", "") or "").strip()

        item = output[source_file]
        item["signal_emit_count"] += 1

        if source_symbol and source_symbol not in item["source_symbols"]:
            item["source_symbols"].append(source_symbol)

        if signal_name and signal_name not in item["signal_names"]:
            item["signal_names"].append(signal_name)

        if target_symbol and target_symbol not in item["target_symbols"]:
            item["target_symbols"].append(target_symbol)

        target_file = _resolve_target_file(target_symbol, symbol_index)
        if target_file:
            item["resolved_signal_target_count"] += 1

            if target_file not in item["fanout_files"]:
                item["fanout_files"].append(target_file)

            target_bucket = _safe_bucket_for_file(target_file, files_payload)
            if target_bucket not in item["fanout_buckets"]:
                item["fanout_buckets"].append(target_bucket)

            target_role = _safe_role_for_file(target_file, boundary_index)
            if target_role not in item["fanout_roles"]:
                item["fanout_roles"].append(target_role)

    for action_key, payload in ui_action_index.items():
        if not isinstance(payload, dict):
            continue

        source_files = payload.get("source_files", [])
        target_files = payload.get("target_files", [])
        target_buckets = payload.get("target_buckets", [])

        for source_file in source_files:
            source_file_str = str(source_file or "")
            if not source_file_str or source_file_str not in output:
                continue

            item = output[source_file_str]
            item["ui_action_reference_count"] += 1

            for target_file in target_files:
                target_file_str = str(target_file or "")
                if target_file_str and target_file_str not in item["fanout_files"]:
                    item["fanout_files"].append(target_file_str)

            for target_bucket in target_buckets:
                bucket_str = str(target_bucket or "")
                if bucket_str and bucket_str not in item["fanout_buckets"]:
                    item["fanout_buckets"].append(bucket_str)

            for target_file in target_files:
                target_file_str = str(target_file or "")
                if not target_file_str:
                    continue
                target_role = _safe_role_for_file(target_file_str, boundary_index)
                if target_role not in item["fanout_roles"]:
                    item["fanout_roles"].append(target_role)

    for file_path, item in output.items():
        item["fanout_file_count"] = len(item["fanout_files"])
        item["fanout_bucket_count"] = len(item["fanout_buckets"])
        item["fanout_role_count"] = len(item["fanout_roles"])

        propagation_score = (
            (int(item["signal_emit_count"]) * 1.0)
            + (int(item["resolved_signal_target_count"]) * 2.0)
            + (int(item["ui_action_reference_count"]) * 2.0)
            + (int(item["fanout_file_count"]) * 2.0)
            + (int(item["fanout_bucket_count"]) * 3.0)
            + (int(item["fanout_role_count"]) * 2.0)
            + (float(item["centrality_score"]) * 0.5)
        )

        item["propagation_score"] = round(propagation_score, 3)
        item["is_event_hub_candidate"] = bool(
            int(item["signal_emit_count"]) >= 3
            or int(item["ui_action_reference_count"]) >= 3
            or int(item["fanout_bucket_count"]) >= 2
            or int(item["fanout_file_count"]) >= 4
        )

        item["source_symbols"] = sorted(item["source_symbols"])
        item["signal_names"] = sorted(item["signal_names"])
        item["target_symbols"] = sorted(item["target_symbols"])
        item["fanout_files"] = sorted(item["fanout_files"])
        item["fanout_buckets"] = sorted(item["fanout_buckets"])
        item["fanout_roles"] = sorted(item["fanout_roles"])

    return dict(sorted(output.items()))


def build_event_propagation_summary(
    event_propagation_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a event propagation summary.
    
    Parameters
    ----------
    event_propagation_index : dict[str, dict[str, Any]]
        The event propagation index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    bucket_frequency: dict[str, int] = {}
    role_frequency: dict[str, int] = {}

    for file_path, payload in event_propagation_index.items():
        bucket = str(payload.get("bucket", "general") or "general")
        role = str(payload.get("boundary_role", "unclassified") or "unclassified")

        bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1
        role_frequency[role] = role_frequency.get(role, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": bucket,
                "boundary_role": role,
                "signal_emit_count": int(payload.get("signal_emit_count", 0)),
                "resolved_signal_target_count": int(
                    payload.get("resolved_signal_target_count", 0)
                ),
                "ui_action_reference_count": int(
                    payload.get("ui_action_reference_count", 0)
                ),
                "fanout_file_count": int(payload.get("fanout_file_count", 0)),
                "fanout_bucket_count": int(payload.get("fanout_bucket_count", 0)),
                "fanout_role_count": int(payload.get("fanout_role_count", 0)),
                "propagation_score": float(payload.get("propagation_score", 0.0)),
                "is_event_hub_candidate": bool(
                    payload.get("is_event_hub_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("propagation_score", 0.0)),
            -int(item.get("fanout_bucket_count", 0)),
            -int(item.get("fanout_file_count", 0)),
            item.get("file", ""),
        )
    )

    event_hub_candidate_count = sum(
        1 for row in rows if bool(row.get("is_event_hub_candidate", False))
    )

    return {
        "file_count": len(rows),
        "event_hub_candidate_count": event_hub_candidate_count,
        "bucket_frequency": dict(sorted(bucket_frequency.items())),
        "role_frequency": dict(sorted(role_frequency.items())),
        "files": rows,
    }


def build_event_propagation_hotspots(
    event_propagation_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a event propagation hotspots.
    
    Parameters
    ----------
    event_propagation_index : dict[str, dict[str, Any]]
        The event propagation index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in event_propagation_index.items():
        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "signal_emit_count": int(payload.get("signal_emit_count", 0)),
                "resolved_signal_target_count": int(
                    payload.get("resolved_signal_target_count", 0)
                ),
                "ui_action_reference_count": int(
                    payload.get("ui_action_reference_count", 0)
                ),
                "fanout_file_count": int(payload.get("fanout_file_count", 0)),
                "fanout_bucket_count": int(payload.get("fanout_bucket_count", 0)),
                "fanout_role_count": int(payload.get("fanout_role_count", 0)),
                "propagation_score": float(payload.get("propagation_score", 0.0)),
                "is_event_hub_candidate": bool(
                    payload.get("is_event_hub_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("propagation_score", 0.0)),
            -int(item.get("fanout_bucket_count", 0)),
            -int(item.get("fanout_file_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
