# project-path: kanda_reasoner_app/reasoner_context_collector/collector_implementation_chronology.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "CANONICAL_HINTS",
    "LEGACY_HINTS",
    "TRANSITION_HINTS",
    "build_implementation_chronology_index",
    "build_implementation_chronology_summary",
    "build_migration_transition_hotspots",
]

from typing import Any
from .collector_implementation_chronology_helpers_private import (
    _safe_float,
    _safe_int,
    _path_tokens,
    _safe_bucket,
    _safe_boundary_role,
    _safe_git_score,
    _safe_priority_score,
    _safe_centrality_score,
    _safe_overlap_score,
    _safe_feature_count,
    _find_canonical_partner,
    _classify_chronology_status,
)


LEGACY_HINTS = {
    "legacy",
    "deprecated",
    "old",
    "older",
    "backup",
    "archive",
    "archived",
    "obsolete",
    "tmp",
    "temp",
    "copy",
}

TRANSITION_HINTS = {
    "migrate",
    "migration",
    "refactor",
    "rewrite",
    "bridge",
    "adapter",
    "compat",
    "transition",
}

CANONICAL_HINTS = {
    "core",
    "common",
    "modules",
    "ui",
    "controllers",
    "services",
    "tabs",
    "kanda",
}




























def build_implementation_chronology_index(
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    canonical_conflict_index: dict[str, dict[str, Any]],
    responsibility_overlap_index: dict[str, dict[str, Any]],
    feature_registry: dict[str, dict[str, Any]],
    git_metadata_index: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a implementation chronology index.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    responsibility_overlap_index : dict[str, dict[str, Any]]
        The responsibility overlap index value.
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    git_metadata_index : dict[str, dict[str, Any]]
        The git metadata index value.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    module_centrality_index : dict[str, dict[str, Any]]
        The module centrality index value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    output: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        file_path = str(file_record.get("path", "")).strip()
        if not file_path:
            continue

        tokens = _path_tokens(file_path)
        legacy_hits = sorted(token for token in tokens if token in LEGACY_HINTS)
        transition_hits = sorted(token for token in tokens if token in TRANSITION_HINTS)
        canonical_hits = sorted(token for token in tokens if token in CANONICAL_HINTS)

        canonical_payload = canonical_conflict_index.get(file_path, {})
        canonical_score = _safe_float(canonical_payload.get("canonical_score", 0.0))
        shadow_severity = _safe_float(canonical_payload.get("shadow_severity", 0.0))
        is_canonical_candidate = bool(
            canonical_payload.get("is_canonical_candidate", False)
        )

        git_score = _safe_git_score(file_path, git_metadata_index)
        priority_score = _safe_priority_score(file_path, file_priority_index)
        centrality_score = _safe_centrality_score(file_path, module_centrality_index)
        overlap_score = _safe_overlap_score(file_path, responsibility_overlap_index)
        feature_count = _safe_feature_count(file_path, feature_registry)

        chronology_score = (
            (canonical_score * 1.8)
            + (git_score * 0.4)
            + (priority_score * 1.2)
            + (centrality_score * 1.0)
            + (feature_count * 1.5)
            + (len(canonical_hits) * 1.5)
            - (len(legacy_hits) * 5.0)
            - (len(transition_hits) * 1.5)
            - (shadow_severity * 0.5)
            + (overlap_score * 0.5)
        )

        chronology_status = _classify_chronology_status(
            canonical_payload if isinstance(canonical_payload, dict) else {},
            legacy_hits,
            transition_hits,
            canonical_score,
        )

        output[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_record),
            "boundary_role": _safe_boundary_role(file_path, boundary_index),
            "chronology_status": chronology_status,
            "chronology_score": round(chronology_score, 3),
            "legacy_token_hits": legacy_hits,
            "transition_token_hits": transition_hits,
            "canonical_token_hits": canonical_hits,
            "canonical_file": _find_canonical_partner(
                file_path,
                canonical_conflict_index,
            ),
            "is_canonical_candidate": is_canonical_candidate,
            "git_score": round(git_score, 3),
            "priority_score": round(priority_score, 3),
            "centrality_score": round(centrality_score, 3),
            "feature_count": feature_count,
            "overlap_score": round(overlap_score, 3),
            "is_transition_candidate": bool(
                chronology_status in {"transition_shadow", "transition_candidate", "transition_current"}
            ),
            "is_current_candidate": bool(
                chronology_status in {"current_canonical", "transition_current", "active_candidate"}
            ),
        }

    return dict(sorted(output.items()))


def build_implementation_chronology_summary(
    implementation_chronology_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a implementation chronology summary.
    
    Parameters
    ----------
    implementation_chronology_index : dict[str, dict[str, Any]]
        The implementation chronology index value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    status_frequency: dict[str, int] = {}

    for file_path, payload in implementation_chronology_index.items():
        status = str(payload.get("chronology_status", "")).strip() or "unknown"
        status_frequency[status] = status_frequency.get(status, 0) + 1

        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general")),
                "boundary_role": str(payload.get("boundary_role", "unclassified")),
                "chronology_status": status,
                "chronology_score": _safe_float(payload.get("chronology_score", 0.0)),
                "feature_count": _safe_int(payload.get("feature_count", 0)),
                "is_transition_candidate": bool(
                    payload.get("is_transition_candidate", False)
                ),
                "is_current_candidate": bool(
                    payload.get("is_current_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -_safe_float(item.get("chronology_score", 0.0)),
            item.get("file", ""),
        )
    )

    transition_candidate_count = sum(
        1 for row in rows if bool(row.get("is_transition_candidate", False))
    )

    return {
        "file_count": len(rows),
        "transition_candidate_count": transition_candidate_count,
        "status_frequency": dict(sorted(status_frequency.items())),
        "files": rows,
    }


def build_migration_transition_hotspots(
    implementation_chronology_index: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a migration transition hotspots.
    
    Parameters
    ----------
    implementation_chronology_index : dict[str, dict[str, Any]]
        The implementation chronology index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in implementation_chronology_index.items():
        if not bool(payload.get("is_transition_candidate", False)) and str(
            payload.get("chronology_status", "")
        ) not in {"legacy_shadow", "legacy_candidate"}:
            continue

        rows.append(
            {
                "file": file_path,
                "bucket": str(payload.get("bucket", "general")),
                "boundary_role": str(payload.get("boundary_role", "unclassified")),
                "chronology_status": str(payload.get("chronology_status", "")),
                "chronology_score": _safe_float(payload.get("chronology_score", 0.0)),
                "canonical_file": str(payload.get("canonical_file", "")),
                "legacy_token_hits": list(payload.get("legacy_token_hits", [])),
                "transition_token_hits": list(payload.get("transition_token_hits", [])),
                "feature_count": _safe_int(payload.get("feature_count", 0)),
            }
        )

    rows.sort(
        key=lambda item: (
            item.get("chronology_status", "") not in {"transition_shadow", "transition_candidate", "transition_current"},
            -_safe_float(item.get("chronology_score", 0.0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
