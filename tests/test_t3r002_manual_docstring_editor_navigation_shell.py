"""Regression tests for the Tab 3 manual docstring editor navigation shell."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PANEL = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_docstring_review_editor.py"
)
SUPPORT = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_docstring_review_support.py"
)


def _text() -> str:
    return REVIEW_PANEL.read_text(encoding="utf-8")


def test_manual_review_window_has_editor_navigation_controls() -> None:
    text = _text()

    assert "class DocstringReviewEditorDialog(QDialog):" in text
    assert 'QPushButton("Previous")' in text
    assert 'QPushButton("Next")' in text
    assert 'QPushButton("Undo")' in text
    assert 'QPushButton("Cancel")' in text
    assert 'QPushButton("Save")' in text
    assert 'QPushButton("Exit")' in text


def test_manual_review_window_loads_modules_and_navigates_locations() -> None:
    text = _text()

    assert "self.module_editor = QPlainTextEdit()" in text
    assert "def _load_module_for_location(" in text
    assert "def _move_module_cursor_to_line(" in text
    assert "def show_previous_location(" in text
    assert "def show_next_location(" in text
    assert "self.module_editor.centerCursor()" in text


def test_manual_review_window_has_suggestion_buttons_without_source_write() -> None:
    text = _text()

    assert 'QPushButton("AI suggest docstring")' in text
    assert 'QPushButton("Heuristic suggest docstring")' in text
    assert "def insert_ai_suggestion_placeholder(" in text
    assert "def insert_heuristic_suggestion(" in text
    assert "py_compile.compile" in text


def test_manual_review_window_loads_tab1_locations() -> None:
    text = _text()
    support = SUPPORT.read_text(encoding="utf-8")

    assert 'QPushButton("Get docstrings missing from Tab1")' in text
    assert "def show_tab1_missing(" in text
    assert "refresh_tab1_findings_for_window" in text
    assert '"source": "tab1_audit"' in text
    assert "refresh_tab1_audit_docstring_source" in support


if __name__ == "__main__":
    test_manual_review_window_has_editor_navigation_controls()
    test_manual_review_window_loads_modules_and_navigates_locations()
    test_manual_review_window_has_suggestion_buttons_without_source_write()
    test_manual_review_window_loads_tab1_locations()
    print("T3R002 manual docstring editor navigation shell tests passed.")
