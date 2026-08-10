# project-path: kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "CANONICAL_PREFERENCE_HINTS",
    "LEGACY_TOKENS",
    "TRANSITION_TOKENS",
    "build_canonical_conflict_index",
    "build_canonical_conflict_summary",
    "build_legacy_shadow_hotspots",
]

from typing import Any
from .collector_canonical_conflicts_helpers_private import (
    _legacy_token_hits,
    _preference_token_hits,
    _safe_bucket,
    _safe_float,
    _safe_int,
    _safe_role,
    _transition_token_hits,
)
from .collector_canonical_conflicts_scoring_private import (
    _build_stem_groups,
    _canonical_score,
    _classify_conflict_status,
    _is_entry_candidate,
    _safe_centrality_score,
    _safe_git_recency_score,
    _safe_priority_rank,
    _safe_priority_score,
)


LEGACY_TOKENS = (
    "legacy",
    "deprecated",
    "backup",
    "old",
    "older",
    "archive",
    "archived",
    "obsolete",
    "tmp",
    "temp",
    "copy",
)

TRANSITION_TOKENS = (
    "migrate",
    "migration",
    "refactor",
    "rewrite",
    "transition",
    "bridge",
    "adapter",
    "compat",
    "compatibility",
)

CANONICAL_PREFERENCE_HINTS = (
    "core",
    "common",
    "kanda",
    "modules",
    "ui",
    "tabs",
    "controllers",
    "services",
)










































def build_canonical_conflict_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
    git_metadata_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a canonical conflict index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    git_metadata_index : dict[str, dict[str, Any]]
        The git metadata index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    stem_groups = _build_stem_groups(files_payload)
    output: dict[str, dict[str, Any]] = {}

    for stem, group_files in stem_groups.items():
        scored_files: list[tuple[str, float]] = []

        for file_path in group_files:
            score = _canonical_score(
                file_path,
                files_payload,
                boundary_index,
                file_priority_index,
                module_centrality_index,
                git_metadata_index,
            )
            scored_files.append((file_path, score))

        scored_files.sort(key=lambda item: (-item[1], item[0]))
        canonical_file = scored_files[0][0]
        canonical_score_value = scored_files[0][1]

        for file_path, score in scored_files:
            legacy_hits = _legacy_token_hits(file_path)
            transition_hits = _transition_token_hits(file_path)
            preference_hits = _preference_token_hits(file_path)
            priority_rank = _safe_priority_rank(file_path, file_priority_index)

            output[file_path] = {
                "file": file_path,
                "conflict_group": stem,
                "group_file_count": len(group_files),
                "group_files": list(group_files),
                "bucket": _safe_bucket(file_path, files_payload),
                "boundary_role": _safe_role(file_path, boundary_index),
                "canonical_score": score,
                "canonical_file": canonical_file,
                "is_canonical_candidate": file_path == canonical_file,
                "conflict_status": _classify_conflict_status(
                    file_path,
                    group_files,
                    canonical_file,
                ),
                "legacy_token_hits": legacy_hits,
                "transition_token_hits": transition_hits,
                "preference_token_hits": preference_hits,
                "priority_rank": priority_rank,
                "priority_score": _safe_priority_score(file_path, file_priority_index),
                "centrality_score": _safe_centrality_score(
                    file_path,
                    module_centrality_index,
                ),
                "git_recency_score": _safe_git_recency_score(
                    file_path,
                    git_metadata_index,
                ),
                "entry_candidate": _is_entry_candidate(file_path, files_payload),
                "shadow_severity": round(canonical_score_value - score, 3),
            }

    return dict(sorted(output.items()))


def build_canonical_conflict_summary(
    canonical_conflict_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a canonical conflict summary.
    
    Parameters
    ----------
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    status_frequency: dict[str, int] = {}
    group_to_files: dict[str, list[str]] = {}

    for file_path, payload in canonical_conflict_index.items():
        status = str(payload.get("conflict_status", "") or "unknown")
        group = str(payload.get("conflict_group", "") or "")

        status_frequency[status] = status_frequency.get(status, 0) + 1
        if group:
            group_to_files.setdefault(group, []).append(file_path)

        rows.append(
            {
                "file": file_path,
                "conflict_group": group,
                "group_file_count": _safe_int(payload.get("group_file_count", 0)),
                "conflict_status": status,
                "is_canonical_candidate": bool(
                    payload.get("is_canonical_candidate", False)
                ),
                "canonical_file": str(payload.get("canonical_file", "") or ""),
                "canonical_score": _safe_float(payload.get("canonical_score", 0.0)),
                "shadow_severity": _safe_float(payload.get("shadow_severity", 0.0)),
                "legacy_token_hits": list(payload.get("legacy_token_hits", [])),
                "transition_token_hits": list(payload.get("transition_token_hits", [])),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("shadow_severity", 0.0)),
            -_safe_int(item.get("group_file_count", 0)),
            item.get("file", ""),
        )
    )

    legacy_candidate_count = sum(
        1
        for row in rows
        if row.get("conflict_status") in ("legacy_shadow", "canonical_but_legacy_named")
    )
    shadow_conflict_count = sum(
        1 for row in rows if not bool(row.get("is_canonical_candidate", False))
    )

    return {
        "file_count": len(rows),
        "conflict_group_count": len(group_to_files),
        "legacy_candidate_count": legacy_candidate_count,
        "shadow_conflict_count": shadow_conflict_count,
        "status_frequency": dict(sorted(status_frequency.items())),
        "files": rows,
    }


def build_legacy_shadow_hotspots(
    canonical_conflict_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a legacy shadow hotspots.
    
    Parameters
    ----------
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in canonical_conflict_index.items():
        rows.append(
            {
                "file": file_path,
                "conflict_group": str(payload.get("conflict_group", "") or ""),
                "group_file_count": _safe_int(payload.get("group_file_count", 0)),
                "conflict_status": str(payload.get("conflict_status", "") or ""),
                "is_canonical_candidate": bool(
                    payload.get("is_canonical_candidate", False)
                ),
                "canonical_file": str(payload.get("canonical_file", "") or ""),
                "canonical_score": _safe_float(payload.get("canonical_score", 0.0)),
                "shadow_severity": _safe_float(payload.get("shadow_severity", 0.0)),
                "legacy_token_hits": list(payload.get("legacy_token_hits", [])),
                "transition_token_hits": list(payload.get("transition_token_hits", [])),
                "bucket": str(payload.get("bucket", "general") or "general"),
                "boundary_role": str(
                    payload.get("boundary_role", "unclassified") or "unclassified"
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("shadow_severity", 0.0)),
            -_safe_int(item.get("group_file_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
