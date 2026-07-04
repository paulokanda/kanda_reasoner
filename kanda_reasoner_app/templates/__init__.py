# project-path: kanda_reasoner_app/templates/__init__.py
"""Shared reusable GUI and source templates."""

from __future__ import annotations

from .inner_tabs_template import (
    INNER_TAB_ACTIVE_STYLE,
    INNER_TAB_HEIGHT,
    INNER_TAB_INACTIVE_STYLE,
    INNER_TAB_STYLE_FRAGMENT,
    InnerTabSpec,
    apply_inner_tab_state,
    build_inner_tab_row,
    configure_inner_tab_button,
    select_inner_tab,
    wire_inner_tab_buttons,
)

__all__ = [
    "INNER_TAB_ACTIVE_STYLE",
    "INNER_TAB_HEIGHT",
    "INNER_TAB_INACTIVE_STYLE",
    "INNER_TAB_STYLE_FRAGMENT",
    "InnerTabSpec",
    "apply_inner_tab_state",
    "build_inner_tab_row",
    "configure_inner_tab_button",
    "select_inner_tab",
    "wire_inner_tab_buttons",
]
