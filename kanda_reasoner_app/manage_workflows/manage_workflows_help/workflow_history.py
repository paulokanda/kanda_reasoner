# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_history.py
"""Own remembered project-root history behavior."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .workflow_constants import (
    HISTORY_FILE,
    HISTORY_MAX_ROOTS,
)

__all__ = [
    "clear_history",
    "get_history_roots",
    "print_history",
    "record_root",
]

def _load_history() -> dict[str, Any]:
    """Load the history file, returning a clean structure on any failure."""
    if not HISTORY_FILE.exists():
        return {"roots": []}
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"roots": []}
        data.setdefault("roots", [])
        return data
    except Exception:
        return {"roots": []}

def _save_history(history: dict[str, Any]) -> None:
    """Persist history to disk, silently ignoring write errors."""
    try:
        HISTORY_FILE.write_text(
            json.dumps(history, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except Exception:
        pass

def record_root(root: Path) -> None:
    """Push *root* to the front of the history list (deduplicated, max 10)."""
    history = _load_history()
    root_str = str(root)
    roots: list[str] = [r for r in history["roots"] if r != root_str]
    roots.insert(0, root_str)
    history["roots"] = roots[:HISTORY_MAX_ROOTS]
    _save_history(history)

def get_history_roots() -> list[str]:
    """Return the history roots.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return _load_history()["roots"]

def clear_history() -> None:
    """Support clear history behavior.
    """
    
    _save_history({"roots": []})
    print(f"History cleared ({HISTORY_FILE})")

def print_history() -> None:
    """Support print history behavior.
    """
    
    roots = get_history_roots()
    if not roots:
        print("No history recorded yet.")
        return
    print("Recent project roots:")
    for i, r in enumerate(roots, 1):
        print(f"  {i:2}. {r}")
