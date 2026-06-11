# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Define shared GUI default constants.
# EXPORTS       : DEFAULT_WORKER_NAME, DEFAULT_PROJECT_ROOT, DEFAULT_BASE_URL, DEFAULT_MODEL
# DEPENDS ON    : pathlib
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Shared constants for the missing-docstrings GUI."""

from __future__ import annotations

from pathlib import Path

DEFAULT_WORKER_NAME = "insert_missing_docstrings.py"
DEFAULT_PROJECT_ROOT = str(Path.cwd())
DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "codellama:13b"

__all__ = [
    "DEFAULT_WORKER_NAME",
    "DEFAULT_PROJECT_ROOT",
    "DEFAULT_BASE_URL",
    "DEFAULT_MODEL",
]
