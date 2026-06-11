"""Focused contract tests for Tab 3 stop-running selected mode."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_layout_adds_stop_button_next_to_run_button() -> None:
    """The run and stop controls are still present after layout consolidation."""
    text = _read('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py')
    assert 'window._run_button = QPushButton("Run Selected Mode")' in text
    assert 'window._stop_button = QPushButton("Stop Running")' in text
    assert "workers_row.addWidget(window._run_button)" in text
    assert "workers_row.addWidget(window._stop_button)" in text
    assert "_stop_running_selected_mode_slot" in text
    assert "module.stop_running_selected_mode(window)" in text


if __name__ == "__main__":
    test_layout_adds_stop_button_next_to_run_button()
    print("Tab 3 stop running selected mode contract tests passed.")
