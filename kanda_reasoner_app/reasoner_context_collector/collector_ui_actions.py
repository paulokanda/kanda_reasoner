"""Support static evidence collection for Project Reasoner."""

# developer_tools/kanda_reasoner_app/reasoner_context_collector/collector_ui_actions.py

from __future__ import annotations

from typing import Any


def _safe_bucket_for_file(
    file_path: str,
    files_payload: list[dict[str, Any]],
) -> str:
    for record in files_payload:
        if str(record.get("path", "")) == file_path:
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"


def _normalize_signal_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}

    return {
        "source_file": str(record.get("source_file", "") or record.get("file", "") or ""),
        "source_symbol": str(record.get("source_symbol", "") or ""),
        "widget": str(record.get("widget", "") or ""),
        "signal": str(record.get("signal", "") or record.get("signal_name", "") or ""),
        "signal_name": str(record.get("signal_name", "") or record.get("signal", "") or ""),
        "handler": str(record.get("handler", "") or record.get("target", "") or ""),
        "target": str(record.get("target", "") or record.get("handler", "") or ""),
        "target_kind": str(record.get("target_kind", "") or ""),
        "line": record.get("line"),
    }


def _extract_class_name_from_source_symbol(source_symbol: str) -> str:
    if not source_symbol:
        return ""

    parts = source_symbol.split(".")
    if len(parts) >= 2:
        return parts[0]
    return ""


def _expand_candidate_targets(
    raw_target: str,
    source_symbol: str,
) -> list[str]:
    target = str(raw_target or "").strip()
    if not target or target == "unknown":
        return []

    candidates: list[str] = [target]

    if target.startswith("self."):
        class_name = _extract_class_name_from_source_symbol(source_symbol)
        method_name = target[len("self.") :].strip()
        if class_name and method_name:
            candidates.insert(0, f"{class_name}.{method_name}")

    return list(dict.fromkeys(candidates))


def _resolve_handler_target(
    raw_target: str,
    source_symbol: str,
    symbol_index: dict[str, Any],
) -> dict[str, Any]:
    for candidate in _expand_candidate_targets(raw_target, source_symbol):
        payload = symbol_index.get(candidate, {})
        if isinstance(payload, dict) and payload:
            return {
                "symbol": candidate,
                "raw_target": raw_target,
                "file": str(payload.get("file", "") or ""),
                "line": payload.get("line"),
                "kind": str(payload.get("kind", "") or ""),
                "resolved": True,
            }

    return {
        "symbol": str(raw_target or ""),
        "raw_target": str(raw_target or ""),
        "file": "",
        "line": None,
        "kind": "",
        "resolved": False,
    }


def build_ui_action_index(
    qt_signal_map: Any,
    symbol_index: dict[str, Any],
    files_payload: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    action_index: dict[str, dict[str, Any]] = {}

    if isinstance(qt_signal_map, dict):
        normalized_records: list[dict[str, Any]] = []
        for raw_records in qt_signal_map.values():
            if isinstance(raw_records, list):
                normalized_records.extend(raw_records)
    elif isinstance(qt_signal_map, list):
        normalized_records = qt_signal_map
    else:
        normalized_records = []

    for raw_record in normalized_records:
        record = _normalize_signal_record(raw_record)

        source_file = record.get("source_file", "")
        source_symbol = record.get("source_symbol", "")
        signal_name = record.get("signal_name", "") or record.get("signal", "")
        target = record.get("target", "") or record.get("handler", "")

        if not signal_name and not target:
            continue

        action_key = f"{source_symbol}::{signal_name}::{target}".strip(":")
        if not action_key:
            continue

        resolved_target = _resolve_handler_target(target, source_symbol, symbol_index)
        target_file = resolved_target.get("file", "")
        target_bucket = (
            _safe_bucket_for_file(target_file, files_payload)
            if target_file
            else ""
        )
        source_bucket = _safe_bucket_for_file(source_file, files_payload) if source_file else "general"

        if action_key not in action_index:
            action_index[action_key] = {
                "action_key": action_key,
                "source_symbol": source_symbol,
                "widget": record.get("widget", ""),
                "signal": signal_name,
                "signal_name": signal_name,
                "handler": target,
                "target": target,
                "source_files": [],
                "source_buckets": [],
                "target_symbols": [],
                "target_files": [],
                "target_buckets": [],
                "records": [],
                "resolved_target": False,
            }

        item = action_index[action_key]

        if source_file and source_file not in item["source_files"]:
            item["source_files"].append(source_file)

        if source_bucket and source_bucket not in item["source_buckets"]:
            item["source_buckets"].append(source_bucket)

        resolved_symbol = str(resolved_target.get("symbol", "") or "")
        if resolved_symbol and resolved_symbol not in item["target_symbols"]:
            item["target_symbols"].append(resolved_symbol)

        if target_file and target_file not in item["target_files"]:
            item["target_files"].append(target_file)

        if target_bucket and target_bucket not in item["target_buckets"]:
            item["target_buckets"].append(target_bucket)

        if bool(resolved_target.get("resolved")):
            item["resolved_target"] = True

        item["records"].append(
            {
                "source_file": source_file,
                "source_symbol": source_symbol,
                "source_bucket": source_bucket,
                "widget": record.get("widget", ""),
                "signal_name": signal_name,
                "handler": target,
                "resolved_symbol": resolved_symbol,
                "resolved_target": bool(resolved_target.get("resolved")),
                "target_file": target_file,
                "target_line": resolved_target.get("line"),
                "target_kind": resolved_target.get("kind", ""),
                "target_bucket": target_bucket,
                "line": record.get("line"),
            }
        )

    return dict(sorted(action_index.items()))


def build_ui_action_summary(
    ui_action_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    for action_key, payload in ui_action_index.items():
        rows.append(
            {
                "action_key": action_key,
                "source_symbol": str(payload.get("source_symbol", "")),
                "signal_name": str(payload.get("signal_name", "") or payload.get("signal", "")),
                "target": str(payload.get("target", "") or payload.get("handler", "")),
                "source_file_count": len(payload.get("source_files", [])),
                "source_bucket_count": len(payload.get("source_buckets", [])),
                "target_symbol_count": len(payload.get("target_symbols", [])),
                "target_file_count": len(payload.get("target_files", [])),
                "target_bucket_count": len(payload.get("target_buckets", [])),
                "source_buckets": sorted(payload.get("source_buckets", [])),
                "target_buckets": sorted(payload.get("target_buckets", [])),
                "resolved_target": bool(payload.get("resolved_target", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            not bool(item.get("resolved_target", False)),
            -int(item.get("target_bucket_count", 0)),
            -int(item.get("target_file_count", 0)),
            item.get("action_key", ""),
        )
    )

    resolved_action_count = sum(1 for row in rows if row.get("resolved_target"))

    return {
        "action_count": len(rows),
        "resolved_action_count": resolved_action_count,
        "actions": rows,
    }


def build_ui_action_hotspots(
    ui_action_index: dict[str, dict[str, Any]],
    limit: int = 20,
) -> list[dict[str, Any]]:
    hotspots: list[dict[str, Any]] = []

    for action_key, payload in ui_action_index.items():
        hotspots.append(
            {
                "action_key": action_key,
                "source_symbol": str(payload.get("source_symbol", "")),
                "signal_name": str(payload.get("signal_name", "") or payload.get("signal", "")),
                "target": str(payload.get("target", "") or payload.get("handler", "")),
                "resolved_target": bool(payload.get("resolved_target", False)),
                "target_file_count": len(payload.get("target_files", [])),
                "target_bucket_count": len(payload.get("target_buckets", [])),
                "target_buckets": sorted(payload.get("target_buckets", [])),
            }
        )

    hotspots.sort(
        key=lambda item: (
            not bool(item.get("resolved_target", False)),
            -int(item.get("target_bucket_count", 0)),
            -int(item.get("target_file_count", 0)),
            item.get("action_key", ""),
        )
    )

    return hotspots[:limit]