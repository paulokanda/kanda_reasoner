# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Provide a public boundary note for the Tab 3 manual review window.
# EXPORTS       : MANUAL_REVIEW_BOUNDARY_NOTE
# DEPENDS ON    : none
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Public boundary note for the Tab 3 manual review window."""

from __future__ import annotations

__all__ = ["MANUAL_REVIEW_BOUNDARY_NOTE"]

MANUAL_REVIEW_BOUNDARY_NOTE = (
    "The Tab 3 manual review window is a GUI boundary over docstring "
    "correction review. Mixed-responsibility warnings remain visible until "
    "a structural refactor or an explicit accepted-warning baseline task."
)
