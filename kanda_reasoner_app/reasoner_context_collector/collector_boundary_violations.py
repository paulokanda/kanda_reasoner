"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "DISALLOWED_HANDOFFS",
    "HIGH_CROSS_BUCKET_THRESHOLD",
    "MIXED_ROLE_THRESHOLD",
    "build_boundary_violation_hotspots",
    "build_boundary_violation_index",
    "build_boundary_violation_summary",
]

from typing import Any


DISALLOWED_HANDOFFS = {
    ("controller", "domain"): "controller_to_domain",
}

MIXED_ROLE_THRESHOLD = 3
HIGH_CROSS_BUCKET_THRESHOLD = 5


def _safe_role(boundary_index: dict[str, dict[str, Any]], file_path: str) -> str:
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    return str(payload.get("boundary_role", "unclassified") or "unclassified")


def _safe_bucket(boundary_index: dict[str, dict[str, Any]], file_path: str) -> str:
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "general"
    return str(payload.get("bucket", "general") or "general")


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def build_boundary_violation_index(
    boundary_index: dict[str, dict[str, Any]],
    boundary_handoffs: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    violation_index: dict[str, list[dict[str, Any]]] = {}

    for handoff in boundary_handoffs:
        if not isinstance(handoff, dict):
            continue

        source_file = str(handoff.get("source_file", "") or "")
        target_file = str(handoff.get("target_file", "") or "")
        source_role = str(handoff.get("source_role", "") or "")
        target_role = str(handoff.get("target_role", "") or "")
        handoff_type = str(handoff.get("handoff_type", "") or "")
        cross_bucket = bool(handoff.get("cross_bucket", False))

        violation_type = DISALLOWED_HANDOFFS.get((source_role, target_role), "")
        if not violation_type:
            continue

        for file_path in [source_file, target_file]:
            if not file_path:
                continue
            violation_index.setdefault(file_path, []).append(
                {
                    "violation_type": violation_type,
                    "severity": "high",
                    "source_file": source_file,
                    "target_file": target_file,
                    "source_role": source_role,
                    "target_role": target_role,
                    "handoff_type": handoff_type,
                    "cross_bucket": cross_bucket,
                }
            )

    for file_path, payload in boundary_index.items():
        if not isinstance(payload, dict):
            continue

        role_flags = [
            bool(payload.get("ui_source", False)),
            bool(payload.get("ui_target", False)),
            _safe_role(boundary_index, file_path) == "controller",
            _safe_role(boundary_index, file_path) == "service",
            _safe_role(boundary_index, file_path) == "domain",
        ]
        active_role_count = sum(1 for flag in role_flags if flag)

        if active_role_count >= MIXED_ROLE_THRESHOLD:
            violation_index.setdefault(file_path, []).append(
                {
                    "violation_type": "mixed_boundary_role",
                    "severity": "medium",
                    "source_file": file_path,
                    "target_file": file_path,
                    "source_role": _safe_role(boundary_index, file_path),
                    "target_role": _safe_role(boundary_index, file_path),
                    "handoff_type": "self_mixed_role",
                    "cross_bucket": False,
                }
            )

        cross_bucket_count = _safe_int(payload.get("cross_bucket_handoff_count", 0))
        if cross_bucket_count >= HIGH_CROSS_BUCKET_THRESHOLD:
            violation_index.setdefault(file_path, []).append(
                {
                    "violation_type": "high_cross_bucket_traffic",
                    "severity": "medium",
                    "source_file": file_path,
                    "target_file": file_path,
                    "source_role": _safe_role(boundary_index, file_path),
                    "target_role": _safe_role(boundary_index, file_path),
                    "handoff_type": "cross_bucket_density",
                    "cross_bucket": True,
                }
            )

    return dict(sorted(violation_index.items()))


def build_boundary_violation_summary(
    boundary_violation_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    type_frequency: dict[str, int] = {}
    severity_frequency: dict[str, int] = {}
    rows: list[dict[str, Any]] = []

    for file_path, violations in boundary_violation_index.items():
        items = violations if isinstance(violations, list) else []
        local_types: list[str] = []
        high_count = 0
        medium_count = 0
        low_count = 0

        for violation in items:
            if not isinstance(violation, dict):
                continue

            violation_type = str(violation.get("violation_type", "") or "")
            severity = str(violation.get("severity", "") or "low")

            if violation_type:
                type_frequency[violation_type] = type_frequency.get(violation_type, 0) + 1
                local_types.append(violation_type)

            severity_frequency[severity] = severity_frequency.get(severity, 0) + 1

            if severity == "high":
                high_count += 1
            elif severity == "medium":
                medium_count += 1
            else:
                low_count += 1

        rows.append(
            {
                "file": file_path,
                "violation_count": len(items),
                "high_count": high_count,
                "medium_count": medium_count,
                "low_count": low_count,
                "violation_types": sorted(set(local_types)),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("high_count", 0)),
            -int(item.get("medium_count", 0)),
            -int(item.get("violation_count", 0)),
            item.get("file", ""),
        )
    )

    return {
        "file_count": len(boundary_violation_index),
        "violation_count": sum(len(v) for v in boundary_violation_index.values()),
        "type_frequency": dict(sorted(type_frequency.items())),
        "severity_frequency": dict(sorted(severity_frequency.items())),
        "files": rows,
    }


def build_boundary_violation_hotspots(
    boundary_violation_index: dict[str, list[dict[str, Any]]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, violations in boundary_violation_index.items():
        items = violations if isinstance(violations, list) else []

        high_count = 0
        medium_count = 0
        low_count = 0
        violation_types: list[str] = []

        for violation in items:
            if not isinstance(violation, dict):
                continue

            severity = str(violation.get("severity", "") or "low")
            violation_type = str(violation.get("violation_type", "") or "")

            if severity == "high":
                high_count += 1
            elif severity == "medium":
                medium_count += 1
            else:
                low_count += 1

            if violation_type:
                violation_types.append(violation_type)

        rows.append(
            {
                "file": file_path,
                "violation_count": len(items),
                "high_count": high_count,
                "medium_count": medium_count,
                "low_count": low_count,
                "violation_types": sorted(set(violation_types)),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("high_count", 0)),
            -int(item.get("medium_count", 0)),
            -int(item.get("violation_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
