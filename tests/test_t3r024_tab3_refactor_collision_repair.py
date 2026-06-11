"""Regression tests for Tab 3 refactor collision repair."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"
ASK_RUNTIME = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
GUI_RUNTIME = ROOT / "reasoner_tools_gui" / "tab3_manual_review_runtime"


PUBLIC_FACADES = {
    "layout_builder.py": {"build_ui", "wire_events", "set_ai_controls_enabled"},
    "manual_docstring_review_editor.py": {"DocstringReviewEditorDialog"},
    "manual_docstring_review_batch.py": {"apply_approved_review_batch"},
    "manual_docstring_review_export.py": {"export_manual_review_summary"},
    "manual_docstring_review_ai.py": {"suggest_manual_review_docstring"},
    "manual_docstring_review_heuristic.py": {"suggest_manual_review_heuristic"},
    "manual_docstring_review_preview.py": {"build_approved_review_preview"},
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _literal_all(path: Path) -> list[str]:
    tree = ast.parse(_read(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        return ast.literal_eval(node.value)
    return []


def test_public_ownership_stays_on_original_facades() -> None:
    for file_name, expected in PUBLIC_FACADES.items():
        assert set(_literal_all(HELP / file_name)) == expected


def test_runtime_modules_do_not_export_duplicate_public_symbols() -> None:
    for folder in (ASK_RUNTIME, GUI_RUNTIME):
        for path in folder.glob("*.py"):
            if path.name == "__init__.py":
                continue
            assert "__all__" not in _read(path), path


def test_qt_heavy_implementation_moved_to_gui_package() -> None:
    assert "PySide6" in _read(GUI_RUNTIME / "editor_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "layout_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "report_panel_runtime.py")
    assert not (ASK_RUNTIME / "editor_runtime.py").exists()
    assert not (ASK_RUNTIME / "layout_runtime.py").exists()
    assert not (ASK_RUNTIME / "report_panel_runtime.py").exists()


def test_original_facades_are_thin_and_literal() -> None:
    for path in HELP.glob("manual_docstring_review_*.py"):
        if path.name in {"manual_docstring_review_boundary_note.py"}:
            continue
        text = _read(path)
        assert len(text.splitlines()) < 80, path
        assert "PySide6" not in text
        assert _literal_all(path), path


def test_repair_report_exists() -> None:
    report = (
        ROOT
        / "_project_reference"
        / "ACTIVE_PROJECT_ GOVERNANCE"
        / "TAB3_MANUAL_REVIEW_STRUCTURE_REFACTOR_REPAIR.md"
    )
    text = _read(report)
    assert "cross-box public symbol" in text
    assert "private/internal" in text


if __name__ == "__main__":
    test_public_ownership_stays_on_original_facades()
    test_runtime_modules_do_not_export_duplicate_public_symbols()
    test_qt_heavy_implementation_moved_to_gui_package()
    test_original_facades_are_thin_and_literal()
    test_repair_report_exists()
    print("T3R024 Tab 3 refactor collision repair tests passed.")
