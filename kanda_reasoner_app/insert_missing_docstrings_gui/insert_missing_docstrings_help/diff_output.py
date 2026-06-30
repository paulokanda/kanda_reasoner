# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/diff_output.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Unified diff rendering for docstring previews
# EXPORTS       : diff_text
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Unified diff rendering for docstring previews."""

from __future__ import annotations

import difflib
from pathlib import Path

__all__ = [
    "diff_text",
]


def diff_text(current: str, desired: str, fromfile: str, tofile: str) -> str:
    """Handle diff text.
    
    Parameters
    ----------
    current : str
        TODO: describe current.
    desired : str
        TODO: describe desired.
    fromfile : str
        TODO: describe fromfile.
    tofile : str
        TODO: describe tofile.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            desired.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )
