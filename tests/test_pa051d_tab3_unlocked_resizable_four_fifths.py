#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA051D regression tests updated for PA051G no Tab 3 resize ownership."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_geometry import (
    calculate_safe_startup_size,
    calculate_screen_fraction_size,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_WINDOW = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "main_window.py"
GEOMETRY = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_geometry.py"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_startup_four_fifths_target_remains_inside_one_monitor() -> None:
    width, height = calculate_safe_startup_size(1920, 1040)

    assert width == int(1920 * 0.80)
    assert height == int(1040 * 0.80)


def test_generic_fraction_helper_can_still_calculate_four_fifths() -> None:
    width, height = calculate_screen_fraction_size(
        1920,
        1040,
        width_ratio=0.80,
        height_ratio=0.80,
        minimum_width=1100,
        minimum_height=720,
    )

    assert width == int(1920 * 0.80)
    assert height == int(1040 * 0.80)


def test_main_window_does_not_lock_or_resize_on_tab3_switch() -> None:
    source = _read_text(MAIN_WINDOW)

    assert "def _finish_tab3_size_pressure_guard" not in source
    assert "timer.singleShot(1100, self._finish_tab3_size_pressure_guard)" not in source
    assert "self.setMaximumSize(16777215, 16777215)" not in source
    assert "resize_window_to_screen_fraction_unlocked" not in source


def test_unlocked_resize_helper_remains_available_but_not_active_in_shell() -> None:
    source = _read_text(GEOMETRY)

    assert "def resize_window_to_screen_fraction_unlocked" in source
    assert "window.isMaximized()" in source


if __name__ == "__main__":
    test_startup_four_fifths_target_remains_inside_one_monitor()
    test_generic_fraction_helper_can_still_calculate_four_fifths()
    test_main_window_does_not_lock_or_resize_on_tab3_switch()
    test_unlocked_resize_helper_remains_available_but_not_active_in_shell()
    print("PA051D Tab 3 unlocked resizable geometry tests passed.")
