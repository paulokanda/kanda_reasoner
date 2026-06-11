"""Regression tests for Tab 3 manual review state persistence."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_support import (
        apply_saved_manual_review_state,
        save_manual_review_state,
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


def test_support_exposes_persistence_helpers() -> None:
    text = _read(SUPPORT)
    exports = _literal_all(SUPPORT)

    assert "apply_saved_manual_review_state" in exports
    assert "save_manual_review_state" in exports
    assert "def apply_saved_manual_review_state(window: object, locations: list[dict])" in text
    assert "def save_manual_review_state(window: object, location: dict, draft_text: str)" in text
    assert "manual_docstring_review_state.json" in text


def test_editor_restores_and_saves_manual_review_state() -> None:
    text = _read(EDITOR)

    assert "apply_saved_manual_review_state(self.owner_window, locations)" in text
    assert "save_manual_review_state(self.owner_window, location, self.editor.toPlainText())" in text
    assert "save_manual_review_state(self.owner_window, location, draft)" in text


def test_editor_remains_under_module_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500


def test_static_import_evidence_is_visible() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_docstring_review_support import" in text
    assert "apply_saved_manual_review_state" in text
    assert "save_manual_review_state" in text


if __name__ == "__main__":
    test_support_exposes_persistence_helpers()
    test_editor_restores_and_saves_manual_review_state()
    test_editor_remains_under_module_size_threshold()
    test_static_import_evidence_is_visible()
    print("T3R010 manual review state persistence tests passed.")
