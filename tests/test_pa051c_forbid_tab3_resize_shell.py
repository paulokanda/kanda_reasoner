#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA051C regression tests updated for PA051G no-resize ownership."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_WINDOW = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "main_window.py"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_tab3_no_longer_uses_size_pressure_guard() -> None:
    """The old pressure guard should not be active after PA051G."""
    source = _read_text(MAIN_WINDOW)

    assert "self.tabs.currentChanged.connect(self._enforce_single_screen_tab_size)" not in source
    assert "set_widget_size_pressure_limit" not in source
    assert "release_widget_size_pressure_limit" not in source
    assert "QSizePolicy.Ignored" not in source


def test_tab3_switch_still_uses_normal_tab_load_handler() -> None:
    """Removing geometry ownership must not remove normal tab loading."""
    source = _read_text(MAIN_WINDOW)

    assert "self.tabs.currentChanged.connect(self._on_tab_changed)" in source


if __name__ == "__main__":
    test_tab3_no_longer_uses_size_pressure_guard()
    test_tab3_switch_still_uses_normal_tab_load_handler()
    print("PA051C Tab 3 resize prevention regression tests passed.")
