"""Source-level tests for Tab 1 running indicator contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = ROOT / 'ask_' 'ai_project_reasoner' / "manage_architecture" / "manage_architecture_gui.py"
INDICATOR_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_architecture"
    / "ai_review"
    / "running_indicator.py"
)
INTEGRATION_PATH = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_architecture"
    / "ai_review"
    / "gui_integration.py"
)


def test_running_indicator_supports_heuristic_and_ai_states() -> None:
    """The animated indicator exposes both deterministic and AI states."""
    source = INDICATOR_PATH.read_text(encoding="utf-8")

    assert "class Tab1ActivityIndicator" in source
    assert "def start_heuristic" in source
    assert "def start_ai_review" in source
    assert "QProgressBar" in source
    assert "QTimer" in source
    assert "self._frame.setVisible(False)" in source
    assert "self._bar.setVisible(False)" in source
    assert "def _hide_after_finish" in source


def test_gui_starts_indicator_for_first_check_and_ai_review() -> None:
    """Tab 1 GUI starts the indicator for heuristic and AI work."""
    gui_source = GUI_PATH.read_text(encoding="utf-8")
    integration_source = INTEGRATION_PATH.read_text(encoding="utf-8")

    assert "indicator.start_heuristic(mode)" in gui_source
    assert "indicator.finish_success" in gui_source
    assert "indicator.finish_error" in gui_source
    assert "indicator.start_ai_review" in integration_source


if __name__ == "__main__":
    test_running_indicator_supports_heuristic_and_ai_states()
    test_gui_starts_indicator_for_first_check_and_ai_review()
    print("Tab 1 running indicator source contract tests passed.")
