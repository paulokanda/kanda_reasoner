"""Contract tests for Tab 3 Output height fill behavior."""

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


def test_output_uses_remaining_left_column_height() -> None:
    """Output should absorb extra left-column height instead of blank stretch."""
    left_block = _left_block(_source())
    assert "left_layout.addWidget(_build_output_panel(window), 1)" in left_block
    assert "left_layout.addWidget(_build_report_group(window))" in left_block
    assert "left_layout.addStretch" not in left_block


def test_report_remains_below_output_after_height_change() -> None:
    """Report should remain below Output after increasing Output height."""
    left_block = _left_block(_source())
    output_line = "left_layout.addWidget(_build_output_panel(window), 1)"
    report_line = "left_layout.addWidget(_build_report_group(window))"
    assert left_block.index(output_line) < left_block.index(report_line)


def test_equal_column_width_contract_is_preserved() -> None:
    """Increasing Output height must not change equal-width columns."""
    source = _source()
    assert "column_splitter.setStretchFactor(0, 1)" in source
    assert "column_splitter.setStretchFactor(1, 1)" in source
    assert "column_splitter.setSizes([1000, 1000])" in source
    assert "column_splitter.setChildrenCollapsible(False)" in source


if __name__ == "__main__":
    test_output_uses_remaining_left_column_height()
    test_report_remains_below_output_after_height_change()
    test_equal_column_width_contract_is_preserved()
    print("Tab 3 Output height fill layout tests passed.")
