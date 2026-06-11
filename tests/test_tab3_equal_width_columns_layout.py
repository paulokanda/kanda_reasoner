"""Contracts for equal-width Tab 3 column layout."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _source() -> str:
    return LAYOUT_RUNTIME.read_text(encoding="utf-8")


def test_tab3_main_columns_have_equal_splitter_stretch() -> None:
    """The two main Tab 3 columns should start with equal splitter weight."""
    source = _source()
    assert "column_splitter.setStretchFactor(0, 1)" in source
    assert "column_splitter.setStretchFactor(1, 1)" in source
    assert "column_splitter.setSizes([1000, 1000])" in source
    assert "column_splitter.setChildrenCollapsible(False)" in source


def test_tab3_output_and_report_remain_below_left_progress_area() -> None:
    """Output and Report remain under the progress bar in the left column."""
    source = _source()
    progress_index = source.index("left_layout.addWidget(window._progress)")
    output_index = source.index("left_layout.addWidget(_build_output_panel(window), 1)")
    report_index = source.index("left_layout.addWidget(_build_report_group(window))")
    review_index = source.index("right_layout.addWidget(_build_review_panel(window), 1)")
    assert progress_index < output_index < report_index
    assert review_index > report_index


if __name__ == "__main__":
    test_tab3_main_columns_have_equal_splitter_stretch()
    test_tab3_output_and_report_remain_below_left_progress_area()
    print("Tab 3 equal-width columns layout tests passed.")
