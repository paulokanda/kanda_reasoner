"""Regression tests for Tab 3 single-location draft apply flow."""

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
SUPPORT = HELP / "manual_docstring_review_support.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_editor_imports_py_compile_for_safe_save() -> None:
    text = _read(EDITOR)

    assert "import py_compile" in text
    assert "py_compile.compile(str(path), doraise=True)" in text


def test_editor_has_single_location_apply_button() -> None:
    text = _read(EDITOR)

    assert 'QPushButton("Apply draft at location")' in text
    assert "self.apply_draft_button.clicked.connect(self.apply_current_docstring_at_location)" in text
    assert "def apply_current_docstring_at_location(self) -> None:" in text
    assert "Applied draft at current location. Use Save to write the module." in text


def test_apply_flow_normalizes_bare_docstring_text() -> None:
    text = _read(EDITOR)

    assert "if not text.startswith" in text
    assert " + text + " in text
    assert 'block_text.lstrip().startswith(("def ", "async def ", "class "))' in text
    assert 'indent += "    "' in text


def test_support_local_review_helpers_are_callable_by_name() -> None:
    text = _read(SUPPORT)

    assert "_manual_review_status_for_row(row)" in text
    assert "_manual__manual_review_status_for_row" not in text


if __name__ == "__main__":
    test_editor_imports_py_compile_for_safe_save()
    test_editor_has_single_location_apply_button()
    test_apply_flow_normalizes_bare_docstring_text()
    test_support_local_review_helpers_are_callable_by_name()
    print("T3R007 manual review apply draft flow tests passed.")
