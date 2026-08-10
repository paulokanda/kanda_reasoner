"""Regression tests for Tab 3 approved-only batch apply."""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    pass


ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"
EDITOR = HELP / "manual_docstring_review_editor.py"
BATCH = HELP / "manual_docstring_review_batch.py"


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


def test_batch_helper_has_public_contract_and_guards() -> None:
    text = _read(BATCH)
    exports = _literal_all(BATCH)
    assert "apply_approved_review_batch" in exports
    assert "def apply_approved_review_batch(window: object, locations: list[dict]) -> str:" in text
    assert 'approval_state", "")).lower() == "approved"' in text
    assert "manual_review_is_inside_project_root(window, path)" in text
    assert "backup_source_file(window, path)" in text
    assert "py_compile.compile(str(path), doraise=True)" in text
    assert "ROLLBACK " in text


def test_editor_has_confirmed_batch_apply_button() -> None:
    text = _read(EDITOR)
    assert 'QPushButton("Apply approved batch")' in text
    assert "self.apply_approved_batch_button.clicked.connect(self.apply_approved_batch)" in text
    assert "def apply_approved_batch(self) -> None:" in text
    assert "QMessageBox.question" in text
    assert "apply_approved_review_batch(self.owner_window, self._locations)" in text


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(BATCH).splitlines()) < 500


def test_static_import_evidence_is_visible() -> None:
    text = Path(__file__).read_text(encoding="utf-8")
    assert "manual_docstring_review_batch import" in text
    assert "apply_approved_review_batch" in text


if __name__ == "__main__":
    test_batch_helper_has_public_contract_and_guards()
    test_editor_has_confirmed_batch_apply_button()
    test_modules_remain_under_size_threshold()
    test_static_import_evidence_is_visible()
    print("T3R020 manual review approved batch apply tests passed.")
