"""Regression test for Tab 3 manual review editor module docstring."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITOR = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_docstring_review_editor.py"
)


def test_manual_review_editor_has_module_docstring() -> None:
    tree = ast.parse(EDITOR.read_text(encoding="utf-8"))

    assert ast.get_docstring(tree)


def test_manual_review_editor_stays_under_module_size_threshold() -> None:
    line_count = len(EDITOR.read_text(encoding="utf-8").splitlines())

    assert line_count < 500


def test_manual_review_state_indicator_is_preserved() -> None:
    text = EDITOR.read_text(encoding="utf-8")

    assert 'self.state_label = QLabel("State: unsaved/new")' in text
    assert "def _set_state_indicator(self, location: dict, restored: bool = False)" in text


if __name__ == "__main__":
    test_manual_review_editor_has_module_docstring()
    test_manual_review_editor_stays_under_module_size_threshold()
    test_manual_review_state_indicator_is_preserved()
    print("T3R012 manual review editor module docstring tests passed.")
