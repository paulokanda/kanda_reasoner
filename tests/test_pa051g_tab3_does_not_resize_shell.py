#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA051G tests for removing Tab 3 ownership of main-window size."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_geometry import (
    calculate_safe_startup_size,
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


def test_tab_switch_does_not_connect_geometry_resize_handler() -> None:
    """Tab changes must not resize the top-level GUI shell."""
    source = _read_text(MAIN_WINDOW)

    assert "self.tabs.currentChanged.connect(self._on_tab_changed)" in source
    assert "self.tabs.currentChanged.connect(self._enforce_single_screen_tab_size)" not in source
    assert "def _enforce_single_screen_tab_size" not in source
    assert "def _apply_tab3_size_pressure_guard" not in source
    assert "def _finish_tab3_size_pressure_guard" not in source
    assert "def _shrink_to_two_thirds_of_one_screen" not in source


def test_main_window_no_longer_imports_tab_resize_helpers() -> None:
    """The main window should not import helpers used only for Tab 3 resizing."""
    source = _read_text(MAIN_WINDOW)

    assert "resize_window_for_primary_screen" in source
    assert "resize_window_to_screen_fraction_unlocked" not in source
    assert "set_widget_size_pressure_limit" not in source
    assert "release_widget_size_pressure_limit" not in source
    assert "self.setMaximumSize(16777215, 16777215)" not in source


def test_startup_defaults_to_four_fifths_of_one_monitor() -> None:
    """The startup size should be about 4/5 of one monitor by default."""
    width, height = calculate_safe_startup_size(1920, 1040)

    assert width == int(1920 * 0.80)
    assert height == int(1040 * 0.80)
    assert width < 1920
    assert height < 1040


def test_geometry_helpers_may_exist_but_are_not_shell_tab_owners() -> None:
    """Helper functions may remain for compatibility but must not be active in the shell."""
    main_source = _read_text(MAIN_WINDOW)
    geometry_source = _read_text(WINDOW_GEOMETRY)

    assert "def resize_window_to_screen_fraction_unlocked" in geometry_source
    assert "resize_window_to_screen_fraction_unlocked" not in main_source


if __name__ == "__main__":
    test_tab_switch_does_not_connect_geometry_resize_handler()
    test_main_window_no_longer_imports_tab_resize_helpers()
    test_startup_defaults_to_four_fifths_of_one_monitor()
    test_geometry_helpers_may_exist_but_are_not_shell_tab_owners()
    print("PA051G Tab 3 no shell-resize ownership tests passed.")
