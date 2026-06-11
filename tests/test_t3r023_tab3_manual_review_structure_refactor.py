"""Regression tests for Tab 3 manual review structural refactor."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"
ASK_RUNTIME = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
GUI_RUNTIME = ROOT / "reasoner_tools_gui" / "tab3_manual_review_runtime"

FACADE_FILES = [
    "layout_builder.py",
    "manual_docstring_review_batch.py",
    "manual_docstring_review_editor.py",
    "manual_docstring_review_export.py",
    "manual_docstring_review_support.py",
    "report_review_panel.py",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _literal_all(path: Path) -> list[str]:
    tree = ast.parse(_read(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except Exception:
            return []
        return value if isinstance(value, list) else []
    return []


def test_runtime_package_contains_moved_implementations() -> None:
    ask_expected = {
        "review_support.py",
        "export_summary.py",
        "batch_apply.py",
        "ai_suggestion.py",
        "heuristic_suggestion.py",
        "preview_summary.py",
    }
    gui_expected = {
        "layout_runtime.py",
        "report_panel_runtime.py",
        "editor_runtime.py",
    }
    assert not [name for name in ask_expected if not (ASK_RUNTIME / name).is_file()]
    assert not [name for name in gui_expected if not (GUI_RUNTIME / name).is_file()]


def test_original_warned_paths_are_thin_facades_without_pyside_imports() -> None:
    for name in FACADE_FILES:
        text = _read(HELP / name)
        assert "PySide6" not in text
        assert "QPushButton" not in text
        assert "QDialog" not in text
        assert len(text.splitlines()) < 80, name


def test_public_symbols_are_preserved_by_facades() -> None:
    assert "build_ui" in _literal_all(HELP / "layout_builder.py")
    assert "DocstringReviewEditorDialog" in _literal_all(HELP / "manual_docstring_review_editor.py")
    assert "apply_approved_review_batch" in _literal_all(HELP / "manual_docstring_review_batch.py")
    assert "export_manual_review_summary" in _literal_all(HELP / "manual_docstring_review_export.py")


def test_runtime_feature_surface_is_preserved() -> None:
    editor = _read(GUI_RUNTIME / "editor_runtime.py")
    batch = _read(ASK_RUNTIME / "batch_apply.py")
    assert 'QPushButton("Apply approved batch")' in editor
    assert 'QPushButton("Preview approved only")' in editor
    assert "def apply_approved_review_batch(" in batch
    assert "py_compile.compile(str(path), doraise=True)" in batch


def test_refactor_status_report_exists() -> None:
    report = (
        ROOT
        / "_project_reference"
        / "ACTIVE_PROJECT_ GOVERNANCE"
        / "TAB3_MANUAL_REVIEW_STRUCTURE_REFACTOR.md"
    )
    text = _read(report)
    assert "thin facades" in text
    assert "tab3_manual_review_runtime" in text


if __name__ == "__main__":
    test_runtime_package_contains_moved_implementations()
    test_original_warned_paths_are_thin_facades_without_pyside_imports()
    test_public_symbols_are_preserved_by_facades()
    test_runtime_feature_surface_is_preserved()
    test_refactor_status_report_exists()
    print("T3R023 Tab 3 manual review structural refactor tests passed.")
