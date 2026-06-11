"""Source contract tests for Tab 3 Run Options inline Scope layout."""

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


def test_scope_controls_are_on_mode_row() -> None:
    """Scope controls should sit to the right of Mode in Run Options."""
    source = _source()

    mode_start = source.index("mode_row = QHBoxLayout()")
    mode_end = source.index("layout.addLayout(mode_row)", mode_start)
    mode_block = source[mode_start:mode_end]

    assert 'QLabel("Mode")' in mode_block
    assert "window._mode_combo" in mode_block
    assert 'QLabel("Scope")' in mode_block
    assert "window._scope_combo" in mode_block
    assert "window._target_path_edit" in mode_block
    assert "window._browse_target_button" in mode_block
    assert "window._clear_target_button" in mode_block

    assert mode_block.index('QLabel("Mode")') < mode_block.index("window._mode_combo")
    assert mode_block.index("window._mode_combo") < mode_block.index('QLabel("Scope")')
    assert mode_block.index('QLabel("Scope")') < mode_block.index("window._scope_combo")


def test_scope_controls_are_not_in_separate_scope_row() -> None:
    """The separate Scope row should not remain after the layout update."""
    source = _source()

    assert "scope_row = QHBoxLayout()" not in source
    assert "layout.addLayout(scope_row)" not in source


def test_existing_run_options_groups_remain() -> None:
    """The GUI-only change must keep the existing group and action titles."""
    source = _source()

    assert 'QGroupBox("Run Options")' in source
    assert 'QGroupBox("Run Select Mode")' in source
    assert 'QPushButton("Run selected mode")' in source
    assert 'QPushButton("Stop Running Selected Mode")' in source


if __name__ == "__main__":
    test_scope_controls_are_on_mode_row()
    test_scope_controls_are_not_in_separate_scope_row()
    test_existing_run_options_groups_remain()
    print("Tab 3 Run Options inline Scope layout tests passed.")
