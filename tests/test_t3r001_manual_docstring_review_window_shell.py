"""Regression tests for the Tab 3 manual docstring review window shell."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
LAYOUT = HELP / "layout_builder.py"
REPORT = HELP / "report_review_panel.py"
EDITOR = HELP / "manual_docstring_review_editor.py"
SUPPORT = HELP / "manual_docstring_review_support.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_layout_adds_manual_review_button() -> None:
    text = _read(LAYOUT)

    assert "Open Manual Docstring Review" in text
    assert "open_docstring_review_window(self)" in text
    assert "_docstring_review_editor_button" in text


def test_review_panel_exports_floating_editor_shell() -> None:
    report_text = _read(REPORT)
    editor_text = _read(EDITOR)

    assert "\"open_docstring_review_window\"" in report_text
    assert "class DocstringReviewEditorDialog(QDialog):" in editor_text
    assert "def show_corrected(self) -> None:" in editor_text
    assert "def show_still_missing(self) -> None:" in editor_text
    assert "def show_dubious(self) -> None:" in editor_text
    assert "def show_tab1_missing(self) -> None:" in editor_text


def test_review_window_has_manual_save_and_tab1_support() -> None:
    editor_text = _read(EDITOR)
    support_text = _read(SUPPORT)

    assert "save_current_review_state" in editor_text
    assert "py_compile.compile" in editor_text
    assert "refresh_tab1_audit_docstring_source(window, True)" in support_text
    assert "_read_source_snippet" in support_text


if __name__ == "__main__":
    test_layout_adds_manual_review_button()
    test_review_panel_exports_floating_editor_shell()
    test_review_window_has_manual_save_and_tab1_support()
    print("T3R001 manual docstring review window shell tests passed.")
