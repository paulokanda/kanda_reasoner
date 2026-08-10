"""Regression tests for Tab 3 manual review state filters."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    pass


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


def test_editor_has_review_state_filter_buttons() -> None:
    text = _read(EDITOR)

    assert 'QPushButton("All")' in text
    assert 'QPushButton("Corrected")' in text
    assert 'QPushButton("Still missing")' in text
    assert 'QPushButton("Dubious")' in text
    assert 'QPushButton("Unsaved/new")' in text
    assert "def set_review_state_filter(self, state_filter: str)" in text


def test_editor_navigation_uses_filtered_index_helper() -> None:
    text = _read(EDITOR)

    assert "next_filtered_location_index(self._locations, self._location_index, -1, self._state_filter)" in text
    assert "next_filtered_location_index(self._locations, self._location_index, 1, self._state_filter)" in text
    assert '" | Filter: " + self._state_filter' in text


def test_support_exposes_filter_helpers() -> None:
    text = _read(SUPPORT)
    exports = _literal_all(SUPPORT)

    assert "next_filtered_location_index" in exports
    assert "review_location_matches_state_filter" in exports
    assert "def next_filtered_location_index(" in text
    assert "def review_location_matches_state_filter(" in text
    assert 'normalized == "unsaved/new"' in text


def test_editor_remains_under_module_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500


if __name__ == "__main__":
    test_editor_has_review_state_filter_buttons()
    test_editor_navigation_uses_filtered_index_helper()
    test_support_exposes_filter_helpers()
    test_editor_remains_under_module_size_threshold()
    print("T3R013 manual review state filter tests passed.")
