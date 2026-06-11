#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for Insert Missing Docstring geometry ownership."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_geometry import (
    calculate_screen_fraction_size,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_WINDOW = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "main_window.py"
WINDOW_GEOMETRY = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_geometry.py"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_fraction_helper_still_supports_two_thirds_when_explicitly_requested() -> None:
    """The generic helper can still calculate 2/3 sizes for callers that ask for it."""
    width, height = calculate_screen_fraction_size(
        1920,
        1040,
        width_ratio=2.0 / 3.0,
        height_ratio=2.0 / 3.0,
        minimum_width=900,
        minimum_height=620,
    )

    assert width == int(1920 * (2.0 / 3.0))
    assert height == int(1040 * (2.0 / 3.0))


def test_insert_missing_docstring_tab_does_not_resize_shell_on_switch() -> None:
    """The tab switch should load content only, not resize the main shell."""
    source = _read_text(MAIN_WINDOW)

    assert "self.tabs.currentChanged.connect(self._on_tab_changed)" in source
    assert "_enforce_single_screen_tab_size" not in source
    assert "_apply_tab3_size_pressure_guard" not in source
    assert "_shrink_to_two_thirds_of_one_screen" not in source
    assert "resize_window_to_screen_fraction_unlocked" not in source


def test_window_geometry_keeps_generic_helpers_for_non_active_compatibility() -> None:
    """The helper module can keep generic geometry helpers without owning Tab 3 sizing."""
    source = _read_text(WINDOW_GEOMETRY)

    assert "calculate_screen_fraction_size" in source
    assert "resize_window_to_screen_fraction_unlocked" in source


if __name__ == "__main__":
    test_fraction_helper_still_supports_two_thirds_when_explicitly_requested()
    test_insert_missing_docstring_tab_does_not_resize_shell_on_switch()
    test_window_geometry_keeps_generic_helpers_for_non_active_compatibility()
    print("PA051B geometry regression tests passed.")
