"""Regression tests for Tab 3 manual review state summary counts."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_support import (
        manual_review_state_summary_text,
    )


ROOT = Path(__file__).resolve().parents[1]
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
EDITOR = HELP / "manual_docstring_review_editor.py"
SUPPORT = HELP / "manual_docstring_review_support.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _literal_all(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            return []
        return [
            item.value
            for item in node.value.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        ]
    return []


def test_editor_has_summary_count_label() -> None:
    text = _read(EDITOR)

    assert "self.counts_label = QLabel(" in text
    assert "Review counts: total=0 corrected=0 still_missing=0 dubious=0 unsaved/new=0" in text
    assert "def _update_review_counts(self) -> None:" in text
    assert "manual_review_state_summary_text(self._locations)" in text


def test_editor_refreshes_counts_after_state_changes() -> None:
    text = _read(EDITOR)

    assert text.count("self._update_review_counts()") >= 4


def test_support_exposes_summary_count_helper() -> None:
    text = _read(SUPPORT)
    exports = _literal_all(SUPPORT)

    assert "manual_review_state_summary_text" in exports
    assert "def manual_review_state_summary_text(locations: list[dict]) -> str:" in text
    assert '"corrected": 0' in text
    assert '"still_missing": 0' in text
    assert '"dubious": 0' in text
    assert '"unsaved/new": 0' in text


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(SUPPORT).splitlines()) < 500


if __name__ == "__main__":
    test_editor_has_summary_count_label()
    test_editor_refreshes_counts_after_state_changes()
    test_support_exposes_summary_count_helper()
    test_modules_remain_under_size_threshold()
    print("T3R014 manual review state summary count tests passed.")
