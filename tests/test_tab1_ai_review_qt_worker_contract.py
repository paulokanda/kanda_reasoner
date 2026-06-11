"""Tests for Tab 1 advisory AI review Qt worker source contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_architecture"
    / "ai_review"
    / "qt_worker.py"
)


def test_qt_worker_exposes_result_signal_and_run_method() -> None:
    """Worker source exposes the expected Qt result signal and run method."""
    source = WORKER_PATH.read_text(encoding="utf-8")

    assert "class Tab1AIReviewWorker" in source
    assert "result_ready = Signal(object)" in source
    assert "def run(self)" in source
    assert "run_tab1_ai_review" in source


if __name__ == "__main__":
    test_qt_worker_exposes_result_signal_and_run_method()
    print("Tab 1 AI review Qt worker contract tests passed.")
