"""Tests for PA052 Insert Missing Docstring help button and help content."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import (
    insert_missing_docstring_help_runtime,
)


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_PATH = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime" / "layout_runtime.py"
HELP_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "insert_missing_docstring_help.md"
)


def test_help_button_is_created_and_wired() -> None:
    """Verify the Help button is created and connected from the layout."""
    source = LAYOUT_PATH.read_text(encoding="utf-8")

    assert "_insert_missing_docstring_help_button" in source
    assert 'QPushButton("Help")' in source
    assert "_insert_missing_docstring_help_slot(window)" in source
    assert ".insert_missing_docstring_help_runtime" in source
    assert "open_insert_missing_docstring_help(window)" in source


def test_help_text_covers_fields_buttons_and_workflows() -> None:
    """Verify the help file explains controls and complete workflows."""
    assert HELP_PATH.exists()
    text = insert_missing_docstring_help_runtime.get_insert_missing_docstring_help_text()

    required_phrases = [
        "Open the tab named Insert Missing Docstring",
        "Scan Files for Missing Docstrings",
        "Generate Draft",
        "Enable Local AI",
        "Base URL",
        "Model",
        "Minimum confidence",
        "AI draft style",
        "Concise",
        "Balanced",
        "Detailed",
        "Save Review Decision",
        "Generate Visible Drafts",
        "Generate All Drafts",
        "Undo Last Bulk Drafts",
        "Complete heuristic example",
        "Complete Local AI example for one selected row",
        "Complete Local AI bulk example",
        "Minimum confidence is a safety/acceptance setting",
    ]

    for phrase in required_phrases:
        assert phrase in text

    assert "Tab 3" not in text


def test_help_runtime_public_contracts_are_importable() -> None:
    """Verify the help runtime exposes the expected public callables."""
    assert callable(insert_missing_docstring_help_runtime.get_insert_missing_docstring_help_text)
    assert callable(insert_missing_docstring_help_runtime.open_insert_missing_docstring_help)


if __name__ == "__main__":
    test_help_button_is_created_and_wired()
    test_help_text_covers_fields_buttons_and_workflows()
    test_help_runtime_public_contracts_are_importable()
    print("PA052 Insert Missing Docstring help button tests passed.")
