"""Contract tests for keeping Tab 3 Output below Local AI."""

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


def test_output_panel_is_in_left_column_below_progress() -> None:
    """Output should be under the progress bar in the left column."""
    source = _source()
    left_start = source.index("left_layout = QVBoxLayout(left_column)")
    left_end = source.index("right_column = QWidget()")
    left_block = source[left_start:left_end]

    assert "left_layout.addWidget(_build_ai_group(window))" in left_block
    assert "left_layout.addWidget(window._progress)" in left_block
    assert "left_layout.addWidget(_build_output_panel(window), 1)" in left_block

    progress_index = left_block.index("left_layout.addWidget(window._progress)")
    output_index = left_block.index("left_layout.addWidget(_build_output_panel(window), 1)")
    assert progress_index < output_index


def test_output_panel_is_not_in_right_column() -> None:
    """Output should not remain in the right column."""
    source = _source()
    right_start = source.index("right_layout = QVBoxLayout(right_column)")
    right_end = source.index("column_splitter = QSplitter()")
    right_block = source[right_start:right_end]

    assert "right_layout.addWidget(_build_review_panel(window), 1)" in right_block
    assert "_build_report_group(window)" not in right_block
    assert "_build_output_panel(window)" not in right_block


if __name__ == "__main__":
    test_output_panel_is_in_left_column_below_progress()
    test_output_panel_is_not_in_right_column()
    print("Tab 3 Output below Local AI layout tests passed.")
