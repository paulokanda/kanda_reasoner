"""Regression tests for Tab 3 final warning repair."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ASK_RUNTIME = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
GUI_RUNTIME = ROOT / "reasoner_tools_gui" / "tab3_manual_review_runtime"
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"


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


def test_ask_runtime_relocation_markers_are_explicit_and_tested() -> None:
    from kanda_reasoner_app.tab3_manual_review_runtime.editor_runtime import (
        TAB3_EDITOR_RUNTIME_RELOCATED,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime import (
        TAB3_LAYOUT_RUNTIME_RELOCATED,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime import (
        TAB3_REPORT_PANEL_RUNTIME_RELOCATED,
    )

    assert TAB3_EDITOR_RUNTIME_RELOCATED.endswith("editor_runtime")
    assert TAB3_LAYOUT_RUNTIME_RELOCATED.endswith("layout_runtime")
    assert TAB3_REPORT_PANEL_RUNTIME_RELOCATED.endswith("report_panel_runtime")


def test_gui_runtime_owns_qt_heavy_modules() -> None:
    assert "PySide6" in _read(GUI_RUNTIME / "editor_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "layout_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "report_panel_runtime.py")


def test_review_support_no_longer_contains_gui_domain_token() -> None:
    text = _read(ASK_RUNTIME / "review_support.py").lower()

    assert "pyside6" not in text
    assert "qpushbutton" not in text
    assert "qdialog" not in text
    assert "insert_missing_docstrings_gui" not in text
    assert "gui" not in text


def test_public_facade_ownership_is_still_preserved() -> None:
    assert "DocstringReviewEditorDialog" in _literal_all(HELP / "manual_docstring_review_editor.py")
    assert "apply_approved_review_batch" in _literal_all(HELP / "manual_docstring_review_batch.py")
    assert "build_ui" in _literal_all(HELP / "layout_builder.py")


def test_repair_report_exists() -> None:
    report = (
        ROOT
        / "_project_reference"
        / "ACTIVE_PROJECT_ GOVERNANCE"
        / "TAB3_MANUAL_REVIEW_FINAL_WARNING_REPAIR.md"
    )
    text = _read(report)
    assert "dead shim" in text
    assert "mixed-responsibility" in text


if __name__ == "__main__":
    test_ask_runtime_relocation_markers_are_explicit_and_tested()
    test_gui_runtime_owns_qt_heavy_modules()
    test_review_support_no_longer_contains_gui_domain_token()
    test_public_facade_ownership_is_still_preserved()
    test_repair_report_exists()
    print("T3R025 Tab 3 final warning repair tests passed.")
