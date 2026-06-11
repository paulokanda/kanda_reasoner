"""Contract tests for the Tab 3 handler-options selected-mode layout."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_run_options_group_is_renamed_to_handler_options() -> None:
    """The options group has the new user-facing title."""
    text = _read('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py')
    assert "Missing Docstring Handler Options and Selected Mode" in text
    assert 'QGroupBox("Run Options")' not in text


def test_run_and_stop_buttons_live_next_to_workers() -> None:
    """Run/stop controls are inside the handler-options group."""
    text = _read('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py')
    start = text.index("def _build_options_group")
    end = text.index("def _build_ai_group")
    block = text[start:end]
    assert 'workers_row.addWidget(QLabel("Workers"))' in block
    assert "workers_row.addWidget(window._workers_spin)" in block
    assert 'window._run_button = QPushButton("Run Selected Mode")' in block
    assert 'window._stop_button = QPushButton("Stop Running")' in block
    assert "workers_row.addWidget(window._run_button)" in block
    assert "workers_row.addWidget(window._stop_button)" in block


def test_separate_run_select_mode_group_is_removed() -> None:
    """The old standalone Run Select Mode group is not built anymore."""
    text = _read('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py')
    assert "def _build_action_row" not in text
    assert 'QGroupBox("Run Select Mode")' not in text
    assert "right_layout.addWidget(_build_action_row(window))" not in text


if __name__ == "__main__":
    test_run_options_group_is_renamed_to_handler_options()
    test_run_and_stop_buttons_live_next_to_workers()
    test_separate_run_select_mode_group_is_removed()
    print("Tab 3 handler-options selected-mode layout tests passed.")
