"""Regression tests for Tab 3 approved-only preview."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_preview import (
        build_approved_review_preview,
    )


ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"
EDITOR = HELP / "manual_docstring_review_editor.py"
PREVIEW = HELP / "manual_docstring_review_preview.py"


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


def test_preview_helper_has_public_contract() -> None:
    text = _read(PREVIEW)
    exports = _literal_all(PREVIEW)
    assert "build_approved_review_preview" in exports
    assert "def build_approved_review_preview(locations: list[dict]) -> str:" in text
    assert 'approval_state", "")).strip().lower() == "approved"' in text
    assert "Approved-only preview: no approved locations." in text


def test_editor_has_preview_button_and_read_only_handler() -> None:
    text = _read(EDITOR)
    assert 'QPushButton("Preview approved only")' in text
    assert "self.preview_approved_button.clicked.connect(self.preview_approved_only)" in text
    assert "def preview_approved_only(self) -> None:" in text
    assert "self.context.setPlainText(build_approved_review_preview(self._locations))" in text


def test_preview_does_not_write_source_files() -> None:
    method = _read(EDITOR).split("def preview_approved_only", 1)[1].split("def apply_current_docstring_at_location", 1)[0]
    assert "write_text" not in method
    assert "py_compile" not in method
    assert "save_manual_review_state" not in method


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(PREVIEW).splitlines()) < 500


if __name__ == "__main__":
    test_preview_helper_has_public_contract()
    test_editor_has_preview_button_and_read_only_handler()
    test_preview_does_not_write_source_files()
    test_modules_remain_under_size_threshold()
    print("T3R019 manual review approved-only preview tests passed.")
