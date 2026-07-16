# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Persist standalone GUI preferences and safe value coercion.
# EXPORTS       : PREFS_FILENAME, safe_bool, safe_int, safe_text, prefs_path, load_prefs, save_prefs
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Preference helpers for the missing-docstrings GUI."""

from __future__ import annotations

import logging

import json
from pathlib import Path
from typing import Any

PREFS_FILENAME = ".missing_docstrings_gui_prefs.json"

__all__ = [
    "PREFS_FILENAME",
    "safe_bool",
    "safe_int",
    "safe_text",
    "prefs_path",
    "load_prefs",
    "save_prefs",
]


def safe_bool(value: object, default: bool) -> bool:
    """Return a boolean preference or a fallback value."""
    if isinstance(value, bool):
        return value
    return default


def safe_int(value: object, default: int, minimum: int, maximum: int) -> int:
    """Return an integer preference constrained to an inclusive range."""
    try:
        number = int(value)
    except Exception:
        return default
    return max(minimum, min(maximum, number))


def safe_text(value: object, default: str = "") -> str:
    """Return a stripped string preference or a fallback value."""
    text = str(value or "").strip()
    return text if text else default


def prefs_path(module_file: str | Path) -> Path:
    """Return the preference file beside the GUI module."""
    return Path(module_file).resolve().parent / PREFS_FILENAME


def load_prefs(path: Path) -> dict[str, Any]:
    """Load persisted GUI preferences from disk."""
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        logging.exception("Boundary failure in load_prefs")
        pass
    return {}


def save_prefs(path: Path, payload: dict[str, Any]) -> None:
    """Persist GUI preferences to disk, ignoring storage failures."""
    try:
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except Exception:
        pass
