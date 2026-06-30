# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/manual_docstring_review_ai.py
"""Compatibility facade for manual review AI suggestions."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.ai_suggestion import (
    generate_manual_review_docstring,
)

__all__ = [
    "suggest_manual_review_docstring",
]


def suggest_manual_review_docstring(window: object, location: dict, module_text: str) -> str:
    """Return one docstring suggestion through the Tab 3 runtime boundary."""
    return generate_manual_review_docstring(window, location, module_text)
