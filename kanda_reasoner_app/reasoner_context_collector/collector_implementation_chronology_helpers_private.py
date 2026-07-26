# project-path: kanda_reasoner_app/reasoner_context_collector/collector_implementation_chronology_helpers_private.py
"""Private helpers for implementation chronology collection."""

from __future__ import annotations

__all__: list[str] = []

from typing import Any


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

def _normalize_path(path: str) -> str:
    """Support normalize path behavior.
    
    Parameters
    ----------
    path : str
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(path or "").replace("\\", "/").strip().lower()

def _path_tokens(path: str) -> set[str]:
    """Support path tokens behavior.
    
    Parameters
    ----------
    path : str
        The file or folder path.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    normalized = _normalize_path(path)
    cleaned = normalized.replace("-", "_").replace(".", "_").replace("/", "_")
    return {token for token in cleaned.split("_") if token}

def _safe_bucket(file_record: dict[str, Any]) -> str:
    """Support safe bucket behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    bucket = str(file_record.get("subsystem_bucket", "")).strip().lower()
    return bucket or "general"

def _safe_boundary_role(
    file_path: str,
    boundary_index: dict[str, dict[str, Any]],
) -> str:
    """Support safe boundary role behavior.
    
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
    role = str(payload.get("boundary_role", "")).strip().lower()
    return role or "unclassified"

def _safe_git_score(
    file_path: str,
    git_metadata_index: dict[str, dict[str, Any]],
) -> float:
    """Support safe git score behavior.
    
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

    score = 0.0
    for key in ("commit_count", "recent_commit_count", "author_count"):
        score += _safe_float(payload.get(key, 0))
    return score

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

def _safe_overlap_score(
    file_path: str,
    responsibility_overlap_index: dict[str, dict[str, Any]],
) -> float:
    """Support safe overlap score behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    responsibility_overlap_index : dict[str, dict[str, Any]]
        The responsibility overlap index value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    payload = responsibility_overlap_index.get(file_path, {})
    if not isinstance(payload, dict):
        return 0.0
    return _safe_float(payload.get("max_overlap_score", 0.0))

def _safe_feature_count(
    file_path: str,
    feature_registry: dict[str, dict[str, Any]],
) -> int:
    """Support safe feature count behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    feature_registry : dict[str, dict[str, Any]]
        The feature registry value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    count = 0
    for payload in feature_registry.values():
        if not isinstance(payload, dict):
            continue
        for item in payload.get("files", []):
            if isinstance(item, dict) and str(item.get("file", "")).strip() == file_path:
                count += 1
    return count

def _find_canonical_partner(
    file_path: str,
    canonical_conflict_index: dict[str, dict[str, Any]],
) -> str:
    """Support find canonical partner behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    canonical_conflict_index : dict[str, dict[str, Any]]
        The canonical conflict index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = canonical_conflict_index.get(file_path, {})
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("canonical_file", "")).strip()

def _classify_chronology_status(
    canonical_conflict_payload: dict[str, Any],
    legacy_hits: list[str],
    transition_hits: list[str],
    canonical_score: float,
) -> str:
    """Support classify chronology status behavior.
    
    Parameters
    ----------
    canonical_conflict_payload : dict[str, Any]
        The canonical conflict payload value.
    legacy_hits : list[str]
        The legacy hits value.
    transition_hits : list[str]
        The transition hits value.
    canonical_score : float
        The canonical score value.
    
    Returns
    -------
    str
        The string result.
    """
    
    conflict_status = str(canonical_conflict_payload.get("conflict_status", "")).strip()

    if conflict_status == "canonical":
        return "current_canonical"

    if conflict_status == "canonical_but_legacy_named":
        return "legacy_named_current"

    if conflict_status == "canonical_transition_candidate":
        return "transition_current"

    if conflict_status == "legacy_shadow":
        return "legacy_shadow"

    if conflict_status == "transition_shadow":
        return "transition_shadow"

    if transition_hits and canonical_score > 0:
        return "transition_candidate"

    if legacy_hits:
        return "legacy_candidate"

    return "active_candidate"
