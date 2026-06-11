"""Regression tests for Insert Missing Docstring child width pressure."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAYOUT_PATH = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _source() -> str:
    return LAYOUT_PATH.read_text(encoding="utf-8")


def test_tab3_main_splitter_no_longer_forces_large_width() -> None:
    """The main Tab 3 splitter must not request two 1000-pixel columns."""
    source = _source()

    assert "column_splitter.setSizes([1000, 1000])" not in source
    assert "column_splitter.setSizes([1, 1])" in source
    assert "_relieve_horizontal_size_pressure(column_splitter" in source


def test_tab3_review_editors_wrap_and_release_width_pressure() -> None:
    """Before and after editors must not force long no-wrap width hints."""
    source = _source()

    assert "setLineWrapMode(QPlainTextEdit.NoWrap)" not in source
    assert "setLineWrapMode(QPlainTextEdit.WidgetWidth)" in source
    assert "_relieve_horizontal_size_pressure(window._review_original_snippet" in source
    assert "_relieve_horizontal_size_pressure(window._review_corrected_snippet" in source


def test_tab3_after_correction_actions_are_split_across_rows() -> None:
    """A single long correction row should not force the shell wider."""
    source = _source()

    assert "draft_action_row = QHBoxLayout()" in source
    assert "review_decision_row = QHBoxLayout()" in source
    assert "correction_row = QHBoxLayout()" not in source


if __name__ == "__main__":
    test_tab3_main_splitter_no_longer_forces_large_width()
    test_tab3_review_editors_wrap_and_release_width_pressure()
    test_tab3_after_correction_actions_are_split_across_rows()
    print("PA051H Tab 3 child width pressure repair tests passed.")
