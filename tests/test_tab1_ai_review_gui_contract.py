"""Source-level tests for Tab 1 advisory AI review GUI wiring."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = ROOT / 'ask_' 'ai_project_reasoner' / "manage_architecture" / "manage_architecture_gui.py"
INTEGRATION_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_architecture"
    / "ai_review"
    / "gui_integration.py"
)


def test_gui_exposes_ai_review_button_without_replacing_first_check() -> None:
    """Tab 1 GUI keeps existing run controls and adds AI review control."""
    gui_source = GUI_PATH.read_text(encoding="utf-8")
    integration_source = INTEGRATION_PATH.read_text(encoding="utf-8")

    assert "install_tab1_ai_review_controls" in gui_source
    assert "AI Review First Check" in integration_source
    assert "Run Selected Mode" in gui_source
    assert "Read-only AI review" in integration_source


def test_gui_ai_review_uses_worker_thread() -> None:
    """AI review is wired through a worker thread instead of direct UI call."""
    integration_source = INTEGRATION_PATH.read_text(encoding="utf-8")

    assert "window._ai_review_thread = QThread(window)" in integration_source
    assert "Tab1AIReviewWorker" in integration_source
    assert "result_ready.connect" in integration_source


if __name__ == "__main__":
    test_gui_exposes_ai_review_button_without_replacing_first_check()
    test_gui_ai_review_uses_worker_thread()
    print("Tab 1 AI review GUI contract tests passed.")
