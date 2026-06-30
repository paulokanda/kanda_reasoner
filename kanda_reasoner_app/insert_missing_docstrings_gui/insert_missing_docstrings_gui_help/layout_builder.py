# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/layout_builder.py
"""Compatibility facade for Tab 3 review layout."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "build_ui",
    "wire_events",
    "set_ai_controls_enabled",
]


def _layout_runtime() -> Any:
    """Load the Tab 3 review layout runtime lazily."""
    module_name = "kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime"
    return import_module(module_name)


def build_ui(*args: Any, **kwargs: Any) -> Any:
    """Build the Tab 3 review layout through the runtime boundary."""
    return _layout_runtime()._build_ui(*args, **kwargs)


def wire_events(*args: Any, **kwargs: Any) -> Any:
    """Wire Tab 3 review events through the runtime boundary."""
    return _layout_runtime()._wire_events(*args, **kwargs)


def set_ai_controls_enabled(*args: Any, **kwargs: Any) -> Any:
    """Set Tab 3 AI-control state through the runtime boundary."""
    return _layout_runtime()._set_ai_controls_enabled(*args, **kwargs)
