# project-path: kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts_scoring_private.py
"""Private scoring helpers for canonical conflict collection."""

from __future__ import annotations

__all__: list[str] = []

from typing import Any

from .collector_canonical_conflicts_helpers_private import (
    _basename_without_suffix,
    _normalize_path,
    _parent_path,
    _legacy_token_hits,
    _preference_token_hits,
    _safe_float,
    _safe_int,
    _safe_role,
    _transition_token_hits,
)


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
