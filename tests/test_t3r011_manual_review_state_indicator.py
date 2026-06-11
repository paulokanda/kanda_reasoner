"""Regression tests for Tab 3 manual review state indicator."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITOR = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_docstring_review_editor.py"
)


def _read() -> str:
    return EDITOR.read_text(encoding="utf-8")


def test_state_indicator_label_exists() -> None:
    text = _read()

    assert 'self.state_label = QLabel("State: unsaved/new")' in text
    assert "layout.addWidget(self.state_label)" in text
    assert "def _set_state_indicator(self, location: dict, restored: bool = False)" in text


def test_state_indicator_shows_restored_and_saved_messages() -> None:
    text = _read()

    assert '"State restored: " if restored else "State: "' in text
    assert 'bool(location.get("manual_review_state"))' in text
    assert "State saved." in text


def test_state_indicator_updates_after_apply_and_save() -> None:
    text = _read()

    assert "self._set_state_indicator(location)" in text
    assert "Applied draft at current location. State saved. Use Save to write the module." in text
    assert 'detail + "\\nState saved."' in text


def test_editor_remains_under_module_size_threshold() -> None:
    assert len(_read().splitlines()) < 500


if __name__ == "__main__":
    test_state_indicator_label_exists()
    test_state_indicator_shows_restored_and_saved_messages()
    test_state_indicator_updates_after_apply_and_save()
    test_editor_remains_under_module_size_threshold()
    print("T3R011 manual review state indicator tests passed.")
