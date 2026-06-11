"""Source contract tests for Tab 2 AI review thread lifetime safety."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_workflows"
    / "ai_review"
    / "gui_integration.py"
)
WORKER_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_workflows"
    / "ai_review"
    / "qt_worker.py"
)


def test_result_handling_uses_gui_thread_receiver() -> None:
    """Worker results must not update Qt widgets through a raw lambda."""
    source = GUI_PATH.read_text(encoding="utf-8")

    assert "class _Tab2AIReviewResultReceiver(QObject):" in source
    assert "@Slot(object)" in source
    assert "worker.result_ready.connect(receiver.handle_result)" in source
    assert "lambda result: _handle_tab2_ai_review_result" not in source


def test_worker_has_finished_signal_for_orderly_thread_shutdown() -> None:
    """The worker exposes a completion signal used to quit the QThread."""
    gui_source = GUI_PATH.read_text(encoding="utf-8")
    worker_source = WORKER_PATH.read_text(encoding="utf-8")

    assert "finished = Signal()" in worker_source
    assert "self.finished.emit()" in worker_source
    assert "worker.finished.connect(thread.quit)" in gui_source
    assert "worker.finished.connect(worker.deleteLater)" in gui_source


def test_worker_logs_broad_exception_before_returning_error_result() -> None:
    """Broad worker failures must have an explicit error surface."""
    worker_source = WORKER_PATH.read_text(encoding="utf-8")

    assert '_LOGGER.exception("Tab 2 AI review worker failed")' in worker_source
    assert 'success=False' in worker_source
    assert 'error_message="Tab 2 AI review worker failed: " + str(exc)' in worker_source


if __name__ == "__main__":
    test_result_handling_uses_gui_thread_receiver()
    test_worker_has_finished_signal_for_orderly_thread_shutdown()
    test_worker_logs_broad_exception_before_returning_error_result()
    print("Tab 2 AI review thread lifetime contract tests passed.")
