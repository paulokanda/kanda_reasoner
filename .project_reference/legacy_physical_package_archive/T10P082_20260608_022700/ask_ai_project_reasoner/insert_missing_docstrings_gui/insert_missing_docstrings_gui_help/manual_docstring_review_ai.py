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
