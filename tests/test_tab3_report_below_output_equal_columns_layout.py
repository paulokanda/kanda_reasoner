"""Contract tests for placing Tab 3 Report below Output."""

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
    """Return the source section that builds the left column."""
    start = source.index("left_layout = QVBoxLayout(left_column)")
    end = source.index("right_column = QWidget()")
    return source[start:end]


def _right_block(source: str) -> str:
    """Return the source section that builds the right column."""
    start = source.index("right_layout = QVBoxLayout(right_column)")
    end = source.index("column_splitter = QSplitter()")
    return source[start:end]


def test_report_is_in_left_column_below_output() -> None:
    """Report should sit below Output in the left column."""
    source = _source()
    left_block = _left_block(source)

    output_line = "left_layout.addWidget(_build_output_panel(window), 1)"
    report_line = "left_layout.addWidget(_build_report_group(window))"
    assert output_line in left_block
    assert report_line in left_block
    assert left_block.index(output_line) < left_block.index(report_line)


def test_right_column_keeps_review_without_report_or_output() -> None:
    """Right column should keep Review only after moving Report left."""
    source = _source()
    right_block = _right_block(source)

    assert "right_layout.addWidget(_build_review_panel(window), 1)" in right_block
    assert "_build_report_group(window)" not in right_block
    assert "_build_output_panel(window)" not in right_block


def test_column_splitter_keeps_equal_sizing_contract() -> None:
    """Main columns should retain symmetric sizing behavior."""
    source = _source()
    assert "column_splitter.setStretchFactor(0, 1)" in source
    assert "column_splitter.setStretchFactor(1, 1)" in source
    assert "column_splitter.setSizes([1000, 1000])" in source
    assert "column_splitter.setChildrenCollapsible(False)" in source


if __name__ == "__main__":
    test_report_is_in_left_column_below_output()
    test_right_column_keeps_review_without_report_or_output()
    test_column_splitter_keeps_equal_sizing_contract()
    print("Tab 3 Report below Output equal columns layout tests passed.")
