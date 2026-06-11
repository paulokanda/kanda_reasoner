"""PA051 tests for screen-aware GUI startup sizing."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_geometry import (
    calculate_safe_startup_size,
)


def test_large_preferred_size_is_clamped_to_single_1080p_monitor() -> None:
    width, height = calculate_safe_startup_size(1920, 1040)

    assert width <= 1920
    assert height <= 1040
    assert width < 1900
    assert height < 1100


def test_startup_size_never_exceeds_small_screen() -> None:
    width, height = calculate_safe_startup_size(1366, 728)

    assert width <= 1366
    assert height <= 728


def test_main_window_uses_screen_aware_helper_instead_of_fixed_resize() -> None:
    source_path = Path(
        'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/main_window.py'
    )
    source = source_path.read_text(encoding="utf-8")

    assert "resize_window_for_primary_screen" in source
    assert "self.resize(1900, 1100)" not in source


if __name__ == "__main__":
    test_large_preferred_size_is_clamped_to_single_1080p_monitor()
    test_startup_size_never_exceeds_small_screen()
    test_main_window_uses_screen_aware_helper_instead_of_fixed_resize()
    print("PA051 GUI startup size tests passed.")
