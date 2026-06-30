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

from pathlib import PurePosixPath
from typing import Any


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


def _safe_int(value: Any) -> int:
    """Support safe int behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    try:
        return int(value)
    except Exception:
        return 0


def _safe_float(value: Any) -> float:
    """Support safe float behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    try:
        return float(value)
    except Exception:
        return 0.0


def _normalize_path(file_path: str) -> str:
    """Support normalize path behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(file_path or "").replace("\\", "/").strip()


def _basename_without_suffix(file_path: str) -> str:
    """Support basename without suffix behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = PurePosixPath(_normalize_path(file_path))
    return path.stem.lower()


def _parent_path(file_path: str) -> str:
    """Support parent path behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    str
        The string result.
    """
    
    path = PurePosixPath(_normalize_path(file_path))
    return str(path.parent).lower()


def _path_tokens(file_path: str) -> list[str]:
    """Support path tokens behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    normalized = _normalize_path(file_path).lower()
    raw_tokens = normalized.replace("-", "_").replace(".", "_").split("/")
    tokens: list[str] = []
    for token in raw_tokens:
        tokens.extend([part for part in token.split("_") if part])
    return tokens


def _legacy_token_hits(file_path: str) -> list[str]:
    """Support legacy token hits behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tokens = _path_tokens(file_path)
    return sorted({token for token in tokens if token in LEGACY_TOKENS})


def _transition_token_hits(file_path: str) -> list[str]:
    """Support transition token hits behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tokens = _path_tokens(file_path)
    return sorted({token for token in tokens if token in TRANSITION_TOKENS})


def _preference_token_hits(file_path: str) -> list[str]:
    """Support preference token hits behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tokens = _path_tokens(file_path)
    return sorted({token for token in tokens if token in CANONICAL_PREFERENCE_HINTS})


def _safe_bucket(file_path: str, files_payload: list[dict[str, Any]]) -> str:
    """Support safe bucket behavior.
    
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
        if _normalize_path(str(record.get("path", ""))) == _normalize_path(file_path):
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"


def _safe_role(file_path: str, boundary_index: dict[str, dict[str, Any]]) -> str:
    """Support safe role behavior.
    
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


def _safe_priority_rank(
    file_path: str,
    file_priority_index: dict[str, dict[str, Any]],
) -> int:
    """Support safe priority rank behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    payload = file_priority_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 999999
    for key in ("priority_rank", "rank", "position"):
        if key in payload:
            return _safe_int(payload.get(key))
    return 999999


def _safe_priority_score(
    file_path: str,
    file_priority_index: dict[str, dict[str, Any]],
) -> float:
    """Support safe priority score behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    file_priority_index : dict[str, dict[str, Any]]
        The file priority index value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    payload = file_priority_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0
    for key in ("priority_score", "score", "total_score"):
        if key in payload:
            return _safe_float(payload.get(key))
    return 0.0


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
        if key in payload:
            return _safe_float(payload.get(key))
    return 0.0


def _safe_git_recency_score(
    file_path: str,
    git_metadata_index: dict[str, dict[str, Any]],
) -> float:
    """Support safe git recency score behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    git_metadata_index : dict[str, dict[str, Any]]
        The git metadata index value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    payload = git_metadata_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0

    candidate_keys = (
        "commit_count",
        "recent_commit_count",
        "author_count",
    )
    score = 0.0
    for key in candidate_keys:
        score += _safe_float(payload.get(key, 0))
    return score


def _is_entry_candidate(file_path: str, files_payload: list[dict[str, Any]]) -> bool:
    """Support is entry candidate behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for record in files_payload:
        if _normalize_path(str(record.get("path", ""))) == _normalize_path(file_path):
            return bool(record.get("entry_markers"))
    return False


def _build_stem_groups(files_payload: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Support build stem groups behavior.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    groups: dict[str, list[str]] = {}
    for record in files_payload:
        file_path = _normalize_path(str(record.get("path", "")))
        if not file_path:
            continue
        stem = _basename_without_suffix(file_path)
        groups.setdefault(stem, []).append(file_path)

    return {
        stem: sorted(paths)
        for stem, paths in groups.items()
        if len(paths) >= 2
    }


def _build_directory_name_groups(
    files_payload: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Support build directory name groups behavior.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    groups: dict[str, list[str]] = {}
    for record in files_payload:
        file_path = _normalize_path(str(record.get("path", "")))
        if not file_path:
            continue
        key = _parent_path(file_path) + "::" + _basename_without_suffix(file_path)
        groups.setdefault(key, []).append(file_path)

    return {
        key: sorted(paths)
        for key, paths in groups.items()
        if len(paths) >= 2
    }


def _canonical_score(
    file_path: str,
    files_payload: list[dict[str, Any]],
    boundary_index: dict[str, dict[str, Any]],
    file_priority_index: dict[str, dict[str, Any]],
    module_centrality_index: dict[str, dict[str, Any]],
    git_metadata_index: dict[str, dict[str, Any]],
) -> float:
    """Support canonical score behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
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
    float
        The floating-point result.
    """
    
    legacy_hits = _legacy_token_hits(file_path)
    transition_hits = _transition_token_hits(file_path)
    preference_hits = _preference_token_hits(file_path)
    priority_score = _safe_priority_score(file_path, file_priority_index)
    centrality_score = _safe_centrality_score(file_path, module_centrality_index)
    git_score = _safe_git_recency_score(file_path, git_metadata_index)
    entry_bonus = 5.0 if _is_entry_candidate(file_path, files_payload) else 0.0

    role = _safe_role(file_path, boundary_index)
    role_bonus = 0.0
    if role == "controller":
        role_bonus = 1.5
    elif role == "service":
        role_bonus = 1.0
    elif role == "domain":
        role_bonus = 0.75

    score = 0.0
    score += priority_score * 1.5
    score += centrality_score * 1.25
    score += git_score * 0.25
    score += len(preference_hits) * 2.0
    score += role_bonus
    score += entry_bonus
    score -= len(legacy_hits) * 6.0
    score -= len(transition_hits) * 2.0
    return round(score, 3)


def _classify_conflict_status(
    file_path: str,
    group_files: list[str],
    canonical_file: str,
) -> str:
    """Support classify conflict status behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    group_files : list[str]
        The group files value.
    canonical_file : str
        The canonical file value.
    
    Returns
    -------
    str
        The string result.
    """
    
    legacy_hits = _legacy_token_hits(file_path)
    transition_hits = _transition_token_hits(file_path)

    if file_path == canonical_file:
        if legacy_hits:
            return "canonical_but_legacy_named"
        if transition_hits:
            return "canonical_transition_candidate"
        return "canonical"

    if legacy_hits:
        return "legacy_shadow"
    if transition_hits:
        return "transition_shadow"
    return "shadow_conflict"


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
