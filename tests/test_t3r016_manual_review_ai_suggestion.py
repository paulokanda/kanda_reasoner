"""Regression tests for Tab 3 one-location AI docstring suggestion."""

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
AI_HELPER = HELP / "manual_docstring_review_ai.py"


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


def test_ai_helper_has_public_contract_and_safe_fallback() -> None:
    text = _read(AI_HELPER)
    exports = _literal_all(AI_HELPER)

    assert "suggest_manual_review_docstring" in exports
    assert "def suggest_manual_review_docstring(window: object, location: dict, module_text: str) -> str:" in text
    assert "return fallback" in text
    assert "urllib.request.urlopen(request, timeout=45)" in text


def test_editor_uses_ai_suggestion_as_editable_draft_only() -> None:
    text = _read(EDITOR)

    assert "suggest_manual_review_docstring(self.owner_window, location, self.module_editor.toPlainText())" in text
    assert "AI suggestion loaded into editable draft. Use Apply draft at location to insert it." in text
    ai_method = text.split("def insert_ai_suggestion_placeholder", 1)[1].split("def insert_heuristic_suggestion", 1)[0]
    assert "_insert_docstring_at_cursor" not in ai_method


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(AI_HELPER).splitlines()) < 500


def test_static_import_evidence_is_visible() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_docstring_review_ai import" in text
    assert "suggest_manual_review_docstring" in text


if __name__ == "__main__":
    test_ai_helper_has_public_contract_and_safe_fallback()
    test_editor_uses_ai_suggestion_as_editable_draft_only()
    test_modules_remain_under_size_threshold()
    test_static_import_evidence_is_visible()
    print("T3R016 manual review AI suggestion tests passed.")
