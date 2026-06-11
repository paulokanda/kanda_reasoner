"""Regression tests for the strict two-part Tab 3 review layout."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_FILE = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime" / "layout_runtime.py"


def test_review_tab_has_only_two_visible_group_titles() -> None:
    """The review tab should expose only before and after visual sections."""
    source = LAYOUT_FILE.read_text(encoding="utf-8")
    assert 'QGroupBox("Before Correction")' in source
    assert 'QGroupBox("After Correction")' in source
    assert 'QLabel("Code snippet without missing docstring")' not in source
    assert 'QLabel("Same snippet with corrected docstring")' not in source
    assert 'QLabel("Selected row status and details")' not in source


def test_review_details_is_kept_for_logic_but_hidden_from_layout() -> None:
    """Existing detail-update logic should keep a hidden sink, not a visible third panel."""
    source = LAYOUT_FILE.read_text(encoding="utf-8")
    assert "window._review_details = QPlainTextEdit()" in source
    assert "window._review_details.hide()" in source
    assert "after_layout.addWidget(window._review_details" not in source


def test_review_splitter_contains_only_before_and_after_groups() -> None:
    """The review splitter should contain only the two main correction columns."""
    source = LAYOUT_FILE.read_text(encoding="utf-8")
    assert "review_splitter.addWidget(before_group)" in source
    assert "review_splitter.addWidget(after_group)" in source
    assert source.count("review_splitter.addWidget(") == 2


if __name__ == "__main__":
    test_review_tab_has_only_two_visible_group_titles()
    test_review_details_is_kept_for_logic_but_hidden_from_layout()
    test_review_splitter_contains_only_before_and_after_groups()
    print("PA031C Tab 3 strict two-part review layout tests passed.")
