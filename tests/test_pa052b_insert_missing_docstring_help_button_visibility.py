#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for Docstring Assistant shell help button visibility."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)
TOOL_SPECS = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "tool_specs.py"
)
LAZY_TABS = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "lazy_tabs.py"
)
RENDERED_HELP = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "help_docs"
    / "rendered"
    / "docstring_assistant.html"
)
LEGACY_FALLBACK = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_help"
    / "docstring_assistant.json"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_shell_help_button_is_created_from_docstring_tool_spec() -> None:
    """The visible Help action should be owned by the lazy-tab shell."""
    tool_specs = _read_text(TOOL_SPECS)
    lazy_tabs = _read_text(LAZY_TABS)

    assert 'step_title="Docstring Assistant"' in tool_specs
    assert 'help_catalog="docstring_assistant.json"' in tool_specs
    assert 'tab_id="docstring_assistant"' in tool_specs
    assert 'self.help_button = QPushButton("Help")' in lazy_tabs
    assert "open_help_document_for_legacy_catalog" in lazy_tabs


def test_embedded_layout_no_longer_creates_lower_help_button() -> None:
    """The Docstring Assistant work surface should not create a second Help button."""
    source = _read_text(LAYOUT_RUNTIME)
    old_lower_help_label = "Help - " + "Insert Missing Docstring"

    assert "_insert_missing_docstring_help_button" not in source
    assert "_insert_missing_docstring_help_slot" not in source
    assert old_lower_help_label not in source
    assert "open_insert_missing_docstring_help(window)" not in source


def test_rich_help_and_plain_fallback_exist() -> None:
    """The shell Help action should have rich HTML and a legacy JSON fallback."""
    rendered = _read_text(RENDERED_HELP)
    fallback = _read_text(LEGACY_FALLBACK)

    assert "<h1>Docstring Assistant</h1>" in rendered
    assert "../css/book_help.css" in rendered
    assert "docstring_assistant_opener_library.png" in rendered
    assert '"tab": "Docstring Assistant"' in fallback


if __name__ == "__main__":
    test_shell_help_button_is_created_from_docstring_tool_spec()
    test_embedded_layout_no_longer_creates_lower_help_button()
    test_rich_help_and_plain_fallback_exist()
    print("PA052B Docstring Assistant shell help visibility tests passed.")
