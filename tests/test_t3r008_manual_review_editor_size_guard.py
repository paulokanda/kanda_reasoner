"""Regression test for Tab 3 manual review editor size guard."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITOR = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_docstring_review_editor.py"
)


def test_manual_review_editor_stays_under_module_size_threshold() -> None:
    line_count = len(EDITOR.read_text(encoding="utf-8").splitlines())

    assert line_count < 500


def test_manual_review_apply_and_safe_save_flow_are_preserved() -> None:
    text = EDITOR.read_text(encoding="utf-8")

    assert 'QPushButton("Apply draft at location")' in text
    assert "def apply_current_docstring_at_location(self) -> None:" in text
    assert "backup_source_file(" in text
    assert "py_compile.compile(str(path), doraise=True)" in text
    assert "path.write_text(text, encoding=\"utf-8\"" in text
    assert "path.write_text(original, encoding=\"utf-8\"" in text


if __name__ == "__main__":
    test_manual_review_editor_stays_under_module_size_threshold()
    test_manual_review_apply_and_safe_save_flow_are_preserved()
    print("T3R008 manual review editor size guard tests passed.")
