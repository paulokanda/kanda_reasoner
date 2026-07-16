"""Support static evidence collection for Project Reasoner."""

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


def _safe_role_for_file(
    file_path: str,
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    return str(payload.get("boundary_role", "unclassified") or "unclassified")


def _safe_module_score(
    file_path: str,
    module_centrality_index: dict[str, dict[str, Any]],
) -> float:
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


def _resolve_target_file(
    to_call: str,
    symbol_index: dict[str, dict[str, Any]],
) -> str:
    payload = symbol_index.get(to_call, {})
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("file", "") or "")


def build_orchestration_index(
    files_payload: list[dict[str, Any]],
    call_edges: list[dict[str, Any]],
    symbol_index: dict[str, dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    orchestration_index: dict[str, dict[str, Any]] = {}

    for record in files_payload:
        file_path = str(record.get("path", "") or "")
        if not file_path:
            continue

        orchestration_index[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket_for_file(file_path, files_payload),
            "boundary_role": _safe_role_for_file(file_path, boundary_index),
            "centrality_score": _safe_module_score(file_path, module_centrality_index),
            "outbound_call_count": 0,
            "resolved_outbound_call_count": 0,
            "target_file_count": 0,
            "target_bucket_count": 0,
            "cross_bucket_target_count": 0,
            "target_files": [],
            "target_buckets": [],
            "target_roles": [],
            "entry_candidate": bool(record.get("entry_markers")),
        }

    for edge in call_edges:
        if not isinstance(edge, dict):
            continue

        source_file = str(edge.get("from_file", "") or "")
        to_call = str(edge.get("to_call", "") or "")
        if not source_file or source_file not in orchestration_index:
            continue

        item = orchestration_index[source_file]
        item["outbound_call_count"] += 1

        target_file = _resolve_target_file(to_call, symbol_index)
        if not target_file:
            continue

        item["resolved_outbound_call_count"] += 1

        if target_file not in item["target_files"]:
            item["target_files"].append(target_file)

        target_bucket = _safe_bucket_for_file(target_file, files_payload)
        if target_bucket not in item["target_buckets"]:
            item["target_buckets"].append(target_bucket)

        target_role = _safe_role_for_file(target_file, boundary_index)
        if target_role not in item["target_roles"]:
            item["target_roles"].append(target_role)

    for file_path, item in orchestration_index.items():
        source_bucket = str(item.get("bucket", "general") or "general")
        target_buckets = list(item.get("target_buckets", []))

        cross_bucket_target_count = 0
        for bucket in target_buckets:
            if bucket != source_bucket:
                cross_bucket_target_count += 1

        item["target_file_count"] = len(item.get("target_files", []))
        item["target_bucket_count"] = len(target_buckets)
        item["cross_bucket_target_count"] = cross_bucket_target_count

        outbound_call_count = int(item.get("outbound_call_count", 0))
        resolved_outbound_call_count = int(item.get("resolved_outbound_call_count", 0))
        target_file_count = int(item.get("target_file_count", 0))
        target_bucket_count = int(item.get("target_bucket_count", 0))
        centrality_score = float(item.get("centrality_score", 0.0))

        orchestration_score = (
            (outbound_call_count * 1.0)
            + (resolved_outbound_call_count * 1.5)
            + (target_file_count * 2.0)
            + (target_bucket_count * 3.0)
            + (cross_bucket_target_count * 4.0)
            + (centrality_score * 0.5)
            + (3.0 if item.get("entry_candidate") else 0.0)
        )

        item["orchestration_score"] = round(orchestration_score, 3)
        item["is_orchestration_candidate"] = bool(
            target_file_count >= 3 or target_bucket_count >= 2 or outbound_call_count >= 8
        )

    return dict(sorted(orchestration_index.items()))


def build_orchestration_summary(
    orchestration_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    bucket_frequency: dict[str, int] = {}
    role_frequency: dict[str, int] = {}
    rows: list[dict[str, Any]] = []

    for file_path, payload in orchestration_index.items():
        bucket = str(payload.get("bucket", "general") or "general")
        role = str(payload.get("boundary_role", "unclassified") or "unclassified")

        bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1
        role_frequency[role] = role_frequency.get(role, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": bucket,
                "boundary_role": role,
                "orchestration_score": float(payload.get("orchestration_score", 0.0)),
                "outbound_call_count": int(payload.get("outbound_call_count", 0)),
                "resolved_outbound_call_count": int(
                    payload.get("resolved_outbound_call_count", 0)
                ),
                "target_file_count": int(payload.get("target_file_count", 0)),
                "target_bucket_count": int(payload.get("target_bucket_count", 0)),
                "cross_bucket_target_count": int(
                    payload.get("cross_bucket_target_count", 0)
                ),
                "entry_candidate": bool(payload.get("entry_candidate", False)),
                "is_orchestration_candidate": bool(
                    payload.get("is_orchestration_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("orchestration_score", 0.0)),
            -int(item.get("cross_bucket_target_count", 0)),
            -int(item.get("target_bucket_count", 0)),
            item.get("file", ""),
        )
    )

    candidate_count = sum(
        1 for row in rows if bool(row.get("is_orchestration_candidate", False))
    )

    return {
        "file_count": len(rows),
        "candidate_count": candidate_count,
        "bucket_frequency": dict(sorted(bucket_frequency.items())),
        "role_frequency": dict(sorted(role_frequency.items())),
        "files": rows,
    }


def build_orchestration_hotspots(
    orchestration_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, payload in orchestration_index.items():
        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "orchestration_score": float(payload.get("orchestration_score", 0.0)),
                "outbound_call_count": int(payload.get("outbound_call_count", 0)),
                "resolved_outbound_call_count": int(
                    payload.get("resolved_outbound_call_count", 0)
                ),
                "target_file_count": int(payload.get("target_file_count", 0)),
                "target_bucket_count": int(payload.get("target_bucket_count", 0)),
                "cross_bucket_target_count": int(
                    payload.get("cross_bucket_target_count", 0)
                ),
                "entry_candidate": bool(payload.get("entry_candidate", False)),
                "is_orchestration_candidate": bool(
                    payload.get("is_orchestration_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("orchestration_score", 0.0)),
            -int(item.get("cross_bucket_target_count", 0)),
            -int(item.get("target_bucket_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]