#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for Insert Missing Docstring help button visibility."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)
HELP_RUNTIME = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "insert_missing_docstring_help_runtime.py"
)
HELP_FILE = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "insert_missing_docstring_help.md"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_help_button_is_connected_to_help_runtime() -> None:
    """The layout should connect a visible help action to the help runtime."""
    source = _read_text(LAYOUT_RUNTIME)

    assert "Help" in source
    assert "open_insert_missing_docstring_help" in source


def test_help_runtime_and_help_file_exist() -> None:
    """The visible Help action should have a runtime module and help content."""
    runtime_source = _read_text(HELP_RUNTIME)
    help_text = _read_text(HELP_FILE)

    assert "open_insert_missing_docstring_help" in runtime_source
    assert "get_insert_missing_docstring_help_text" in runtime_source
    assert "Insert Missing Docstring" in help_text
    assert "Generate Draft" in help_text


if __name__ == "__main__":
    test_help_button_is_connected_to_help_runtime()
    test_help_runtime_and_help_file_exist()
    print("PA052B help button visibility regression tests passed.")
