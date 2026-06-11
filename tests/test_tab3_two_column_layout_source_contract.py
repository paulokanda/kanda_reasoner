"""Source contract tests for the Tab 3 two-column layout."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _source() -> str:
    """Return the Tab 3 layout runtime source."""
    return LAYOUT_RUNTIME.read_text(encoding="utf-8")


def _left_block(source: str) -> str:
    start = source.index("left_layout = QVBoxLayout(left_column)")
    end = source.index("right_column = QWidget()")
    return source[start:end]


def _right_block(source: str) -> str:
    start = source.index("right_layout = QVBoxLayout(right_column)")
    end = source.index("column_splitter = QSplitter()")
    return source[start:end]


def test_tab3_layout_uses_left_and_right_columns() -> None:
    """Tab 3 should arrange existing groups into left and right columns."""
    source = _source()

    assert "left_column = QWidget()" in source
    assert "right_column = QWidget()" in source
    assert "column_splitter = QSplitter()" in source
    assert "column_splitter.addWidget(left_column)" in source
    assert "column_splitter.addWidget(right_column)" in source


def test_tab3_left_column_keeps_project_options_local_ai_progress_output_and_report() -> None:
    """Left column should contain Project, options, Local AI, progress, Output, and Report."""
    source = _source()
    left_block = _left_block(source)

    assert "_build_project_group(window)" in left_block
    assert "_build_options_group(window)" in left_block
    assert "_build_ai_group(window)" in left_block
    assert "window._progress" in left_block
    assert "_build_output_panel(window)" in left_block
    assert "_build_report_group(window)" in left_block


def test_tab3_right_column_keeps_review_only() -> None:
    """The right column should contain Review after Output and Report move left."""
    source = _source()
    right_block = _right_block(source)

    assert "_build_review_panel(window)" in right_block
    assert "_build_report_group(window)" not in right_block
    assert "_build_output_panel(window)" not in right_block


def test_tab3_selected_mode_buttons_are_inside_handler_options() -> None:
    """The run and stop buttons should live in the handler-options group."""
    source = _source()

    assert "Missing Docstring Handler Options and Selected Mode" in source
    assert 'window._run_button = QPushButton("Run Selected Mode")' in source
    assert 'window._stop_button = QPushButton("Stop Running")' in source
    assert 'QGroupBox("Run Select Mode")' not in source


if __name__ == "__main__":
    test_tab3_layout_uses_left_and_right_columns()
    test_tab3_left_column_keeps_project_options_local_ai_progress_output_and_report()
    test_tab3_right_column_keeps_review_only()
    test_tab3_selected_mode_buttons_are_inside_handler_options()
    print("Tab 3 two-column layout source contract tests passed.")
