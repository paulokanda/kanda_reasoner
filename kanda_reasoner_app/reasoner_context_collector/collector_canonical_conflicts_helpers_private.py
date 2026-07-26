# project-path: kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts_helpers_private.py
"""Private helpers for canonical conflict collection."""

from __future__ import annotations

__all__: list[str] = []

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
