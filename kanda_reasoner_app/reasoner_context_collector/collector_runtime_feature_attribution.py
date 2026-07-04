"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

__all__ = [
    'build_runtime_feature_attribution_hotspots',
    'build_runtime_feature_attribution_index',
    'build_runtime_feature_attribution_summary',
]



def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _safe_lower(value: Any) -> str:
    return _safe_text(value).lower()


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _normalize_path(value: Any) -> str:
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text


def _tokenize_text(value: Any) -> list[str]:
    text = _safe_lower(value)
    cleaned = []
    current = []

    for ch in text:
        if ch.isalnum():
            current.append(ch)
        else:
            if current:
                cleaned.append("".join(current))
                current = []

    if current:
        cleaned.append("".join(current))

    return cleaned


def _file_to_feature_map(
    feature_registry: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}

    for feature_name, payload in feature_registry.items():
        if not isinstance(payload, dict):
            continue

        for item in payload.get("files", []):
            if not isinstance(item, dict):
                continue

            file_path = _normalize_path(item.get("file", ""))
            if not file_path:
                continue

            if file_path not in mapping:
                mapping[file_path] = []

            if feature_name not in mapping[file_path]:
                mapping[file_path].append(feature_name)

    for file_path in mapping:
        mapping[file_path] = sorted(mapping[file_path])

    return dict(sorted(mapping.items()))


def _feature_name_tokens(feature_registry: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}

    for feature_name in feature_registry.keys():
        name = _safe_text(feature_name)
        if not name:
            continue
        out[name] = set(_tokenize_text(name))

    return dict(sorted(out.items()))


def _file_to_bucket_map(files_payload: list[dict[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}

    for record in files_payload:
        file_path = _normalize_path(record.get("path", ""))
        if not file_path:
            continue

        bucket = (
            _safe_lower(record.get("subsystem_bucket", ""))
            or _safe_lower(record.get("bucket", ""))
            or _safe_lower(record.get("primary_role", ""))
            or "general"
        )
        out[file_path] = bucket

    return dict(sorted(out.items()))


def _file_to_boundary_role_map(
    boundary_index: dict[str, dict[str, Any]],
) -> dict[str, str]:
    out: dict[str, str] = {}

    for file_path, payload in boundary_index.items():
        if not isinstance(payload, dict):
            continue
        out[_normalize_path(file_path)] = _safe_lower(payload.get("boundary_role", "")) or "unclassified"

    return dict(sorted(out.items()))


def _file_to_current_status_map(
    implementation_chronology_index: dict[str, dict[str, Any]],
) -> dict[str, str]:
    out: dict[str, str] = {}

    for file_path, payload in implementation_chronology_index.items():
        if not isinstance(payload, dict):
            continue
        out[_normalize_path(file_path)] = _safe_text(payload.get("chronology_status", "")) or "unknown"

    return dict(sorted(out.items()))


def _path_prefix_feature_match(
    source_file: str,
    file_feature_map: dict[str, list[str]],
) -> list[str]:
    src = _normalize_path(source_file)
    if not src:
        return []

    src_parts = PurePosixPath(src).parts
    best_len = -1
    best_features: list[str] = []

    for file_path, features in file_feature_map.items():
        candidate = _normalize_path(file_path)
        candidate_parts = PurePosixPath(candidate).parts

        common_len = 0
        for left, right in zip(src_parts, candidate_parts):
            if left != right:
                break
            common_len += 1

        if common_len >= 2 and common_len > best_len and features:
            best_len = common_len
            best_features = list(features)

    return sorted(best_features)


def _symbol_feature_match(
    source_symbol: str,
    event_type: str,
    message: str,
    feature_registry: dict[str, dict[str, Any]],
    feature_name_token_map: dict[str, set[str]],
) -> list[str]:
    symbol_tokens = set(_tokenize_text(source_symbol))
    event_tokens = set(_tokenize_text(event_type))
    message_tokens = set(_tokenize_text(message))
    combined_tokens = symbol_tokens | event_tokens | message_tokens

    if not combined_tokens:
        return []

    matches: list[tuple[int, str]] = []

    for feature_name in feature_registry.keys():
        feature_tokens = feature_name_token_map.get(feature_name, set())
        if not feature_tokens:
            continue

        overlap = combined_tokens & feature_tokens
        if overlap:
            matches.append((len(overlap), feature_name))

    matches.sort(key=lambda item: (-item[0], item[1]))
    return [name for _score, name in matches[:5]]


def _resolve_event_features(
    *,
    source_file: str,
    source_symbol: str,
    event_type: str,
    message: str,
    file_feature_map: dict[str, list[str]],
    feature_registry: dict[str, dict[str, Any]],
    feature_name_token_map: dict[str, set[str]],
) -> tuple[list[str], str]:
    normalized_source_file = _normalize_path(source_file)

    exact = file_feature_map.get(normalized_source_file, [])
    if exact:
        return sorted(exact), "exact_file"

    prefix = _path_prefix_feature_match(normalized_source_file, file_feature_map)
    if prefix:
        return sorted(prefix), "path_prefix"

    symbol_based = _symbol_feature_match(
        source_symbol=source_symbol,
        event_type=event_type,
        message=message,
        feature_registry=feature_registry,
        feature_name_token_map=feature_name_token_map,
    )
    if symbol_based:
        return sorted(symbol_based), "symbol_fallback"

    return [], "none"


def build_runtime_feature_attribution_index(
    runtime_scenario_index: dict[str, dict[str, Any]],
    feature_registry: dict[str, dict[str, Any]],
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    implementation_chronology_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    file_feature_map = _file_to_feature_map(feature_registry)
    feature_name_token_map = _feature_name_tokens(feature_registry)
    file_bucket_map = _file_to_bucket_map(files_payload)
    file_role_map = _file_to_boundary_role_map(boundary_index)
    file_status_map = _file_to_current_status_map(implementation_chronology_index)

    output: dict[str, dict[str, Any]] = {}

    for session_id, payload in runtime_scenario_index.items():
        if not isinstance(payload, dict):
            continue

        scenario_name = _safe_text(payload.get("scenario_name", ""))
        events = payload.get("events", [])
        if not isinstance(events, list):
            events = []

        touched_features: dict[str, int] = {}
        touched_buckets: dict[str, int] = {}
        touched_roles: dict[str, int] = {}
        touched_statuses: dict[str, int] = {}
        attribution_modes: dict[str, int] = {}
        attributed_events: list[dict[str, Any]] = []

        for event in events:
            if not isinstance(event, dict):
                continue

            source_file = _normalize_path(event.get("source_file", ""))
            source_symbol = _safe_text(event.get("source_symbol", ""))
            event_type = _safe_text(event.get("event_type", ""))
            message = _safe_text(event.get("message", ""))

            features, attribution_mode = _resolve_event_features(
                source_file=source_file,
                source_symbol=source_symbol,
                event_type=event_type,
                message=message,
                file_feature_map=file_feature_map,
                feature_registry=feature_registry,
                feature_name_token_map=feature_name_token_map,
            )

            bucket = file_bucket_map.get(source_file, "general")
            boundary_role = file_role_map.get(source_file, "unclassified")
            chronology_status = file_status_map.get(source_file, "unknown")

            for feature_name in features:
                touched_features[feature_name] = touched_features.get(feature_name, 0) + 1

            touched_buckets[bucket] = touched_buckets.get(bucket, 0) + 1
            touched_roles[boundary_role] = touched_roles.get(boundary_role, 0) + 1
            touched_statuses[chronology_status] = touched_statuses.get(chronology_status, 0) + 1
            attribution_modes[attribution_mode] = attribution_modes.get(attribution_mode, 0) + 1

            attributed_events.append(
                {
                    "seq": _safe_int(event.get("seq", 0)),
                    "event_type": event_type,
                    "source_file": source_file,
                    "source_symbol": source_symbol,
                    "message": message,
                    "features": list(features),
                    "feature_attribution_mode": attribution_mode,
                    "bucket": bucket,
                    "boundary_role": boundary_role,
                    "chronology_status": chronology_status,
                }
            )

        feature_hit_count = sum(touched_features.values())
        scenario_score = (
            (feature_hit_count * 1.5)
            + (len(touched_features) * 2.5)
            + (len(touched_buckets) * 1.5)
            + (len(touched_roles) * 1.0)
            + (_safe_int(attribution_modes.get("exact_file", 0)) * 0.5)
            + (_safe_int(attribution_modes.get("path_prefix", 0)) * 0.3)
            + (_safe_int(attribution_modes.get("symbol_fallback", 0)) * 0.2)
        )

        output[session_id] = {
            "session_id": session_id,
            "scenario_name": scenario_name,
            "feature_hit_count": feature_hit_count,
            "touched_features": dict(sorted(touched_features.items())),
            "touched_buckets": dict(sorted(touched_buckets.items())),
            "touched_boundary_roles": dict(sorted(touched_roles.items())),
            "touched_chronology_statuses": dict(sorted(touched_statuses.items())),
            "feature_attribution_modes": dict(sorted(attribution_modes.items())),
            "touched_feature_count": len(touched_features),
            "touched_bucket_count": len(touched_buckets),
            "scenario_score": round(scenario_score, 3),
            "attributed_events": attributed_events,
        }

    return dict(sorted(output.items()))


def build_runtime_feature_attribution_summary(
    runtime_feature_attribution_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    all_features: set[str] = set()
    all_buckets: set[str] = set()
    total_feature_hits = 0
    total_modes: dict[str, int] = {}

    for session_id, payload in runtime_feature_attribution_index.items():
        if not isinstance(payload, dict):
            continue

        touched_features = payload.get("touched_features", {})
        touched_buckets = payload.get("touched_buckets", {})
        attribution_modes = payload.get("feature_attribution_modes", {})

        if isinstance(touched_features, dict):
            for key, value in touched_features.items():
                all_features.add(_safe_text(key))
                total_feature_hits += _safe_int(value)

        if isinstance(touched_buckets, dict):
            for key in touched_buckets.keys():
                all_buckets.add(_safe_text(key))

        if isinstance(attribution_modes, dict):
            for key, value in attribution_modes.items():
                mode = _safe_text(key)
                total_modes[mode] = total_modes.get(mode, 0) + _safe_int(value)

        rows.append(
            {
                "session_id": session_id,
                "scenario_name": _safe_text(payload.get("scenario_name", "")),
                "feature_hit_count": _safe_int(payload.get("feature_hit_count", 0)),
                "touched_feature_count": _safe_int(payload.get("touched_feature_count", 0)),
                "touched_bucket_count": _safe_int(payload.get("touched_bucket_count", 0)),
                "scenario_score": _safe_float(payload.get("scenario_score", 0.0)),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("scenario_score", 0.0)),
            item.get("session_id", ""),
        )
    )

    return {
        "scenario_count": len(rows),
        "runtime_feature_hit_count": total_feature_hits,
        "runtime_touched_feature_count": len(all_features),
        "runtime_touched_bucket_count": len(all_buckets),
        "feature_attribution_modes": dict(sorted(total_modes.items())),
        "scenarios": rows,
    }


def build_runtime_feature_attribution_hotspots(
    runtime_feature_attribution_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for session_id, payload in runtime_feature_attribution_index.items():
        if not isinstance(payload, dict):
            continue

        rows.append(
            {
                "session_id": session_id,
                "scenario_name": _safe_text(payload.get("scenario_name", "")),
                "feature_hit_count": _safe_int(payload.get("feature_hit_count", 0)),
                "touched_feature_count": _safe_int(payload.get("touched_feature_count", 0)),
                "touched_bucket_count": _safe_int(payload.get("touched_bucket_count", 0)),
                "touched_features": list(payload.get("touched_features", {}).keys())[:15],
                "touched_buckets": list(payload.get("touched_buckets", {}).keys())[:15],
                "feature_attribution_modes": dict(payload.get("feature_attribution_modes", {})),
                "scenario_score": _safe_float(payload.get("scenario_score", 0.0)),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("scenario_score", 0.0)),
            item.get("session_id", ""),
        )
    )

    limit = max(0, _safe_int(limit))
    return rows[:limit]