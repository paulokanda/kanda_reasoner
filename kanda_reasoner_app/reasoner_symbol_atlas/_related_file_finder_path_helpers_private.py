# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_related_file_finder_path_helpers_private.py
"""Path and de-duplication helpers for related file finder support."""

from __future__ import annotations

from pathlib import Path as _Path

from .schemas import normalize_project_atlas_text as _normalize_project_atlas_text

__all__: list[str] = []


def _contains_any(value: str, search_terms: tuple[str, ...]) -> bool:
    """Support contains any behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    search_terms : tuple[str, ...]
        The search terms value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = value.lower().replace("\\", "/")
    for term in search_terms:
        cleaned = term.lower().replace("\\", "/")
        if cleaned and cleaned in lowered:
            return True
    return False


def _normalize_path(value: str) -> str:
    """Support normalize path behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = _normalize_project_atlas_text(value)
    return text.replace("\\", "/")


def _relative_path(project_root: _Path, file_path: _Path) -> str:
    """Support relative path behavior.
    
    Parameters
    ----------
    project_root : _Path
        The project root path.
    file_path : _Path
        The file path.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return str(file_path.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(file_path)


def _unique_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    """Support unique paths behavior.
    
    Parameters
    ----------
    paths : tuple[str, ...]
        The file or folder paths.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    seen: set[str] = set()
    for path in paths:
        cleaned = _normalize_path(path)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        values.append(cleaned)
    return tuple(values)


def _limited_unique_paths(paths: tuple[str, ...], max_items: int) -> tuple[str, ...]:
    """Support limited unique paths behavior.
    
    Parameters
    ----------
    paths : tuple[str, ...]
        The file or folder paths.
    max_items : int
        The max items value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    unique = _unique_paths(paths)
    if max_items <= 0:
        return unique
    return unique[:max_items]


def _unique_strings(values: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Support unique strings behavior.
    
    Parameters
    ----------
    values : list[str] | tuple[str, ...]
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = _normalize_project_atlas_text(value)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(cleaned)
    return tuple(result)
