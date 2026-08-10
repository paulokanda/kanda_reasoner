# project-path: kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_help/normalization.py
"""Normalization helpers for collector_runtime_scenarios."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def _safe_text(value: Any) -> str:
    """Support safe text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(value or "").strip()

def _safe_lower(value: Any) -> str:
    """Support safe lower behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _safe_text(value).lower()

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

def _read_json(path: Path) -> dict[str, Any]:
    """Support read json behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return {}

def _normalize_path_text(value: Any) -> str:
    """Support normalize path text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _safe_text(value).replace("\\", "/")
