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


def _safe_centrality_score(
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


def _iter_symbol_records(file_record: dict[str, Any]) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []

    for fn in file_record.get("functions", []):
        if isinstance(fn, dict):
            symbols.append(fn)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if isinstance(method, dict):
                symbols.append(method)

    return symbols


def build_state_mutation_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        file_path = str(file_record.get("path", "") or "")
        if not file_path:
            continue

        assignment_count = 0
        attribute_read_count = 0
        unique_assignment_targets: set[str] = set()
        self_assignment_targets: set[str] = set()
        state_like_targets: set[str] = set()
        symbol_names: list[str] = []

        for symbol in _iter_symbol_records(file_record):
            qualname = str(
                symbol.get("qualname", symbol.get("name", "")) or ""
            )
            if qualname:
                symbol_names.append(qualname)

            for assignment in symbol.get("assignments", []):
                if not isinstance(assignment, dict):
                    continue

                assignment_count += 1
                target = str(assignment.get("target", "") or "").strip()
                if not target:
                    continue

                unique_assignment_targets.add(target)

                if target.startswith("self."):
                    self_assignment_targets.add(target)

                lowered = target.lower()
                if (
                    lowered.startswith("self.")
                    or "state" in lowered
                    or "cache" in lowered
                    or "config" in lowered
                    or "current_" in lowered
                    or lowered.endswith("_state")
                    or lowered.endswith("_cache")
                    or lowered.endswith("_config")
                ):
                    state_like_targets.add(target)

            for attribute in symbol.get("attribute_reads", []):
                if isinstance(attribute, dict):
                    attribute_read_count += 1

        unique_target_count = len(unique_assignment_targets)
        self_target_count = len(self_assignment_targets)
        state_like_target_count = len(state_like_targets)
        centrality_score = _safe_centrality_score(file_path, module_centrality_index)

        mutation_score = (
            (assignment_count * 1.0)
            + (unique_target_count * 1.5)
            + (self_target_count * 2.0)
            + (state_like_target_count * 3.0)
            + (attribute_read_count * 0.25)
            + (centrality_score * 0.5)
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket_for_file(file_path, files_payload),
            "boundary_role": _safe_role_for_file(file_path, boundary_index),
            "centrality_score": centrality_score,
            "symbol_count": len(symbol_names),
            "symbols": sorted(symbol_names),
            "assignment_count": assignment_count,
            "attribute_read_count": attribute_read_count,
            "unique_assignment_target_count": unique_target_count,
            "self_assignment_target_count": self_target_count,
            "state_like_target_count": state_like_target_count,
            "top_assignment_targets": sorted(unique_assignment_targets)[:25],
            "top_self_assignment_targets": sorted(self_assignment_targets)[:25],
            "top_state_like_targets": sorted(state_like_targets)[:25],
            "mutation_score": round(mutation_score, 3),
            "is_state_owner_candidate": bool(
                state_like_target_count >= 3
                or self_target_count >= 4
                or assignment_count >= 10
            ),
        }

    return dict(sorted(output.items()))


def build_state_mutation_summary(
    state_mutation_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    bucket_frequency: dict[str, int] = {}
    role_frequency: dict[str, int] = {}

    for file_path, payload in state_mutation_index.items():
        bucket = str(payload.get("bucket", "general") or "general")
        role = str(payload.get("boundary_role", "unclassified") or "unclassified")

        bucket_frequency[bucket] = bucket_frequency.get(bucket, 0) + 1
        role_frequency[role] = role_frequency.get(role, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": bucket,
                "boundary_role": role,
                "assignment_count": int(payload.get("assignment_count", 0)),
                "attribute_read_count": int(payload.get("attribute_read_count", 0)),
                "unique_assignment_target_count": int(
                    payload.get("unique_assignment_target_count", 0)
                ),
                "self_assignment_target_count": int(
                    payload.get("self_assignment_target_count", 0)
                ),
                "state_like_target_count": int(
                    payload.get("state_like_target_count", 0)
                ),
                "mutation_score": float(payload.get("mutation_score", 0.0)),
                "is_state_owner_candidate": bool(
                    payload.get("is_state_owner_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("mutation_score", 0.0)),
            -int(item.get("state_like_target_count", 0)),
            -int(item.get("assignment_count", 0)),
            item.get("file", ""),
        )
    )

    candidate_count = sum(
        1 for row in rows if bool(row.get("is_state_owner_candidate", False))
    )

    return {
        "file_count": len(rows),
        "state_owner_candidate_count": candidate_count,
        "bucket_frequency": dict(sorted(bucket_frequency.items())),
        "role_frequency": dict(sorted(role_frequency.items())),
        "files": rows,
    }


def build_state_mutation_hotspots(
    state_mutation_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for file_path, payload in state_mutation_index.items():
        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
                "assignment_count": int(payload.get("assignment_count", 0)),
                "attribute_read_count": int(payload.get("attribute_read_count", 0)),
                "unique_assignment_target_count": int(
                    payload.get("unique_assignment_target_count", 0)
                ),
                "self_assignment_target_count": int(
                    payload.get("self_assignment_target_count", 0)
                ),
                "state_like_target_count": int(
                    payload.get("state_like_target_count", 0)
                ),
                "mutation_score": float(payload.get("mutation_score", 0.0)),
                "is_state_owner_candidate": bool(
                    payload.get("is_state_owner_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item.get("mutation_score", 0.0)),
            -int(item.get("state_like_target_count", 0)),
            -int(item.get("assignment_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]