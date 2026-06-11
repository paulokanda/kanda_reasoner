"""Regression tests for Tab 3 refresh-after-save classification."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_support import (
        classify_location_after_tab1_refresh,
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


def test_support_exposes_refresh_after_save_helper() -> None:
    text = _read(SUPPORT)
    exports = _literal_all(SUPPORT)

    assert "classify_location_after_tab1_refresh" in exports
    assert "def classify_location_after_tab1_refresh(window: object, location: dict)" in text
    assert "def _finding_matches_manual_location(" in text
    assert '"still_missing"' in text
    assert '"corrected"' in text


def test_editor_calls_refresh_after_successful_save() -> None:
    text = _read(EDITOR)

    assert "classify_location_after_tab1_refresh" in text
    assert "status, detail = classify_location_after_tab1_refresh(self.owner_window, location)" in text
    assert 'location["classification"] = status' in text
    assert "self.context.append(detail)" in text


def test_editor_remains_under_module_size_threshold() -> None:
    line_count = len(_read(EDITOR).splitlines())

    assert line_count < 500


def test_static_import_evidence_is_visible() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_docstring_review_support import" in text
    assert "classify_location_after_tab1_refresh" in text


if __name__ == "__main__":
    test_support_exposes_refresh_after_save_helper()
    test_editor_calls_refresh_after_successful_save()
    test_editor_remains_under_module_size_threshold()
    test_static_import_evidence_is_visible()
    print("T3R009 manual review refresh-after-save tests passed.")
