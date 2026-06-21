#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Focused cleanup tests for PA051G geometry and help contract repair."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime import (
    insert_missing_docstring_help_runtime as help_runtime,
)


MAIN_WINDOW = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window.py"
)
PA051B_TEST = PROJECT_ROOT / "tests" / "test_pa051b_tab3_size_clamp_two_thirds_screen.py"
PA052B_TEST = PROJECT_ROOT / "tests" / "test_pa052b_insert_missing_docstring_help_button_visibility.py"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_pa051b_regression_no_longer_requires_active_tab_resize_guard() -> None:
    """The PA051B regression should ensure Tab 3 does not own shell resize."""
    test_source = _read_text(PA051B_TEST)
    main_source = _read_text(MAIN_WINDOW)

    assert "_enforce_single_screen_tab_size" not in main_source
    assert "resize_window_to_screen_fraction_unlocked" not in main_source
    assert "does_not_resize_shell" in test_source


def test_pa052b_regression_no_longer_depends_on_exact_button_label() -> None:
    """The help button test should verify shell ownership, not a lower panel label."""
    test_source = _read_text(PA052B_TEST)

    assert "Help - Insert Missing Docstring" not in test_source
    assert "docstring_assistant.json" in test_source
    assert "open_help_document_for_legacy_catalog" in test_source


def test_help_runtime_has_direct_public_contract_import() -> None:
    """The help runtime should be directly imported and publicly protected."""
    exported = set(getattr(help_runtime, "__all__", ()))

    assert "get_insert_missing_docstring_help_text" in exported
    assert "open_insert_missing_docstring_help" in exported


if __name__ == "__main__":
    test_pa051b_regression_no_longer_requires_active_tab_resize_guard()
    test_pa052b_regression_no_longer_depends_on_exact_button_label()
    test_help_runtime_has_direct_public_contract_import()
    print("PA051G geometry and help contract cleanup tests passed.")
