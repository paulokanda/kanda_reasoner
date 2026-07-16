"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "STATE_CREATE_HINTS",
    "STATE_REHYDRATE_HINTS",
    "STATE_RESET_HINTS",
    "STATE_UPDATE_HINTS",
    "build_state_lifecycle_hotspots",
    "build_state_lifecycle_index",
    "build_state_lifecycle_summary",
]

from typing import Any


STATE_CREATE_HINTS = {
    "__init__",
    "initialize",
    "init",
    "build",
    "setup",
    "create",
    "make",
    "construct",
}

STATE_UPDATE_HINTS = {
    "set",
    "update",
    "change",
    "modify",
    "toggle",
    "append",
    "insert",
    "assign",
    "write",
    "save",
}

STATE_RESET_HINTS = {
    "reset",
    "clear",
    "cleanup",
    "restore",
    "close",
    "hide",
    "remove",
    "unload",
}

STATE_REHYDRATE_HINTS = {
    "load",
    "reload",
    "restore",
    "rehydrate",
    "read",
    "open",
    "import",
}


def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _safe_lower(value: Any) -> str:
    return _safe_text(value).lower()


def _safe_bucket(file_path: str, files_payload: list[dict[str, Any]]) -> str:
    for record in files_payload:
        if _safe_text(record.get("path", "")) == file_path:
            bucket = _safe_lower(record.get("subsystem_bucket", ""))
            if bucket:
                return bucket
            break
    return "general"


def _safe_boundary_role(
    file_path: str,
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    role = _safe_lower(payload.get("boundary_role", ""))
    return role or "unclassified"


def _safe_payload(
    mapping: dict[str, dict[str, Any]],
    file_path: str,
) -> dict[str, Any]:
    payload = mapping.get(file_path, {})
    if isinstance(payload, dict):
        return payload
    return {}


def _iter_symbols(file_record: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    for fn in file_record.get("functions", []):
        if isinstance(fn, dict):
            out.append(fn)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if isinstance(method, dict):
                out.append(method)

    return out


def _symbol_name(symbol: dict[str, Any]) -> str:
    return _safe_text(symbol.get("qualname", symbol.get("name", "")))


def _has_any_hint(text: str, hints: set[str]) -> bool:
    lowered = _safe_lower(text)
    return any(hint in lowered for hint in hints)


def _collect_symbol_lifecycle_counts(
    file_record: dict[str, Any],
) -> dict[str, Any]:
    create_count = 0
    update_count = 0
    reset_count = 0
    rehydrate_count = 0
    read_count = 0

    create_symbols: list[str] = []
    update_symbols: list[str] = []
    reset_symbols: list[str] = []
    rehydrate_symbols: list[str] = []

    for symbol in _iter_symbols(file_record):
        symbol_name = _symbol_name(symbol)
        assignments = symbol.get("assignments", [])
        attribute_reads = symbol.get("attribute_reads", [])
        calls = symbol.get("calls", [])

        has_assignments = isinstance(assignments, list) and len(assignments) > 0
        has_reads = isinstance(attribute_reads, list) and len(attribute_reads) > 0

        if has_assignments and _has_any_hint(symbol_name, STATE_CREATE_HINTS):
            create_count += 1
            create_symbols.append(symbol_name)

        if has_assignments and _has_any_hint(symbol_name, STATE_UPDATE_HINTS):
            update_count += 1
            update_symbols.append(symbol_name)

        if (
            has_assignments or has_reads
        ) and _has_any_hint(symbol_name, STATE_RESET_HINTS):
            reset_count += 1
            reset_symbols.append(symbol_name)

        if (
            has_reads or has_assignments
        ) and _has_any_hint(symbol_name, STATE_REHYDRATE_HINTS):
            rehydrate_count += 1
            rehydrate_symbols.append(symbol_name)

        if has_reads:
            read_count += len(attribute_reads)

        for call in calls if isinstance(calls, list) else []:
            if not isinstance(call, dict):
                continue
            call_name = _safe_text(call.get("call_name", ""))
            if _has_any_hint(call_name, STATE_REHYDRATE_HINTS):
                rehydrate_count += 1
                rehydrate_symbols.append(symbol_name)
            if _has_any_hint(call_name, STATE_RESET_HINTS):
                reset_count += 1
                reset_symbols.append(symbol_name)
            if _has_any_hint(call_name, STATE_UPDATE_HINTS):
                update_count += 1
                update_symbols.append(symbol_name)

    return {
        "create_count": create_count,
        "update_count": update_count,
        "reset_count": reset_count,
        "rehydrate_count": rehydrate_count,
        "read_count": read_count,
        "create_symbols": sorted(set(create_symbols))[:25],
        "update_symbols": sorted(set(update_symbols))[:25],
        "reset_symbols": sorted(set(reset_symbols))[:25],
        "rehydrate_symbols": sorted(set(rehydrate_symbols))[:25],
    }


def build_state_lifecycle_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    state_mutation_index: dict[str, dict[str, Any]],
    persistence_io_index: dict[str, dict[str, Any]],
    attribute_state_map: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        file_path = _safe_text(file_record.get("path", ""))
        if not file_path:
            continue

        mutation_payload = _safe_payload(state_mutation_index, file_path)
        persistence_payload = _safe_payload(persistence_io_index, file_path)
        lifecycle_counts = _collect_symbol_lifecycle_counts(file_record)

        attribute_payload = attribute_state_map.get(file_path, {})
        attribute_state_count = 0
        if isinstance(attribute_payload, dict):
            for value in attribute_payload.values():
                if isinstance(value, list):
                    attribute_state_count += len(value)

        state_like_target_count = int(mutation_payload.get("state_like_target_count", 0))
        assignment_count = int(mutation_payload.get("assignment_count", 0))
        persistence_write_count = int(persistence_payload.get("write_call_count", 0))
        persistence_read_count = int(persistence_payload.get("read_call_count", 0))

        lifecycle_score = (
            (lifecycle_counts["create_count"] * 2.0)
            + (lifecycle_counts["update_count"] * 1.5)
            + (lifecycle_counts["reset_count"] * 2.0)
            + (lifecycle_counts["rehydrate_count"] * 2.5)
            + (lifecycle_counts["read_count"] * 0.2)
            + (state_like_target_count * 2.5)
            + (assignment_count * 0.4)
            + (persistence_write_count * 2.0)
            + (persistence_read_count * 1.5)
            + (attribute_state_count * 0.5)
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_path, files_payload),
            "boundary_role": _safe_boundary_role(file_path, boundary_index),
            "create_count": lifecycle_counts["create_count"],
            "update_count": lifecycle_counts["update_count"],
            "reset_count": lifecycle_counts["reset_count"],
            "rehydrate_count": lifecycle_counts["rehydrate_count"],
            "read_count": lifecycle_counts["read_count"],
            "state_like_target_count": state_like_target_count,
            "assignment_count": assignment_count,
            "persistence_write_count": persistence_write_count,
            "persistence_read_count": persistence_read_count,
            "attribute_state_count": attribute_state_count,
            "create_symbols": lifecycle_counts["create_symbols"],
            "update_symbols": lifecycle_counts["update_symbols"],
            "reset_symbols": lifecycle_counts["reset_symbols"],
            "rehydrate_symbols": lifecycle_counts["rehydrate_symbols"],
            "lifecycle_score": round(lifecycle_score, 3),
            "is_state_reset_candidate": bool(
                lifecycle_counts["reset_count"] >= 1
                or any(lifecycle_counts["reset_symbols"])
            ),
            "is_state_rehydration_candidate": bool(
                lifecycle_counts["rehydrate_count"] >= 1
                or persistence_read_count >= 1
            ),
        }

    return dict(sorted(output.items()))


def build_state_lifecycle_summary(
    state_lifecycle_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    reset_candidate_count = 0
    rehydration_candidate_count = 0

    for file_path, payload in state_lifecycle_index.items():
        is_reset = bool(payload.get("is_state_reset_candidate", False))
        is_rehydrate = bool(payload.get("is_state_rehydration_candidate", False))

        if is_reset:
            reset_candidate_count += 1
        if is_rehydrate:
            rehydration_candidate_count += 1

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "boundary_role": _safe_text(payload.get("boundary_role", "unclassified")) or "unclassified",
                "create_count": int(payload.get("create_count", 0)),
                "update_count": int(payload.get("update_count", 0)),
                "reset_count": int(payload.get("reset_count", 0)),
                "rehydrate_count": int(payload.get("rehydrate_count", 0)),
                "lifecycle_score": float(payload.get("lifecycle_score", 0.0)),
                "is_state_reset_candidate": is_reset,
                "is_state_rehydration_candidate": is_rehydrate,
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("lifecycle_score", 0.0)),
            item.get("file", ""),
        )
    )

    return {
        "file_count": len(rows),
        "state_reset_candidate_count": reset_candidate_count,
        "state_rehydration_candidate_count": rehydration_candidate_count,
        "files": rows,
    }


def build_state_lifecycle_hotspots(
    state_lifecycle_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, payload in state_lifecycle_index.items():
        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "boundary_role": _safe_text(payload.get("boundary_role", "unclassified")) or "unclassified",
                "create_count": int(payload.get("create_count", 0)),
                "update_count": int(payload.get("update_count", 0)),
                "reset_count": int(payload.get("reset_count", 0)),
                "rehydrate_count": int(payload.get("rehydrate_count", 0)),
                "lifecycle_score": float(payload.get("lifecycle_score", 0.0)),
                "is_state_reset_candidate": bool(payload.get("is_state_reset_candidate", False)),
                "is_state_rehydration_candidate": bool(payload.get("is_state_rehydration_candidate", False)),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("lifecycle_score", 0.0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
