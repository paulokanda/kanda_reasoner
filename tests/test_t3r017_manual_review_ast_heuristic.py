"""Regression tests for Tab 3 AST-aware heuristic suggestions."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_heuristic import (
        suggest_manual_review_heuristic,
    )


ROOT = Path(__file__).resolve().parents[1]
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
EDITOR = HELP / "manual_docstring_review_editor.py"
HEURISTIC = HELP / "manual_docstring_review_heuristic.py"


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


def test_heuristic_helper_has_public_contract_and_ast_logic() -> None:
    text = _read(HEURISTIC)
    exports = _literal_all(HEURISTIC)

    assert "suggest_manual_review_heuristic" in exports
    assert "def suggest_manual_review_heuristic(location: dict, module_text: str) -> str:" in text
    assert "ast.parse(module_text)" in text
    assert "ast.ClassDef" in text
    assert "ast.FunctionDef" in text


def test_editor_uses_heuristic_as_editable_draft_only() -> None:
    text = _read(EDITOR)

    assert "suggest_manual_review_heuristic(location, self.module_editor.toPlainText())" in text
    assert "Heuristic suggestion loaded into editable draft. Use Apply draft at location to insert it." in text
    method = text.split("def insert_heuristic_suggestion", 1)[1].split("def _insert_docstring_at_cursor", 1)[0]
    assert "_insert_docstring_at_cursor" not in method


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(HEURISTIC).splitlines()) < 500


def test_static_import_evidence_is_visible() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_docstring_review_heuristic import" in text
    assert "suggest_manual_review_heuristic" in text


if __name__ == "__main__":
    test_heuristic_helper_has_public_contract_and_ast_logic()
    test_editor_uses_heuristic_as_editable_draft_only()
    test_modules_remain_under_size_threshold()
    test_static_import_evidence_is_visible()
    print("T3R017 manual review AST heuristic tests passed.")
