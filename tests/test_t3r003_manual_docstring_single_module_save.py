"""Regression tests for Tab 3 manual docstring single-module save shell."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
EDITOR = HELP / "manual_docstring_review_editor.py"
REPORT = HELP / "report_review_panel.py"
MANIFEST = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_review_panel_delegates_floating_editor_to_helper() -> None:
    text = _read(REPORT)

    assert "from .manual_docstring_review_editor import DocstringReviewEditorDialog" in text
    assert "class DocstringReviewEditorDialog" not in text
    assert "\"open_docstring_review_window\"" in text


def test_editor_can_save_one_loaded_module_safely() -> None:
    text = _read(EDITOR)

    assert "def save_current_review_state(self) -> None:" in text
    assert "py_compile.compile(str(path), doraise=True)" in text
    assert "backup_source_file(self.owner_window, path)" in text
    assert "path.write_text(original, encoding=\"utf-8\", newline=\"\\n\")" in text
    assert "Save blocked: path is outside selected project root." in text
    assert "manual_review_is_inside_project_root(self.owner_window, path)" in text


def test_suggestion_buttons_insert_at_module_cursor() -> None:
    text = _read(EDITOR)

    assert "def _insert_docstring_at_cursor(self, docstring: str) -> None:" in text
    assert "cursor.insertText(prepared + \"\\n\")" in text
    assert "self._insert_docstring_at_cursor(suggestion)" in text


def test_manifest_includes_manual_editor_helper_and_open_export() -> None:
    text = _read(MANIFEST)

    assert "manual_docstring_review_editor.py" in text
    assert "manual_docstring_review_support.py" in text
    assert "manual_review_is_inside_project_root" in text
    assert "manual_review_safe_int" in text
    assert "def is_inside_project_root(" not in text
    assert "def safe_int(" not in text
    assert "DocstringReviewEditorDialog" in text
    assert "open_docstring_review_window" in text


if __name__ == "__main__":
    test_review_panel_delegates_floating_editor_to_helper()
    test_editor_can_save_one_loaded_module_safely()
    test_suggestion_buttons_insert_at_module_cursor()
    test_manifest_includes_manual_editor_helper_and_open_export()
    print("T3R003 manual docstring single-module save tests passed.")
