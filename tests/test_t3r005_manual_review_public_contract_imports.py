"""Static public-contract coverage for Tab 3 manual review helpers.

The architecture validator requires direct test-module import evidence for
public helper surfaces. The imports are kept in an unreachable block so this
focused test can run in headless environments without importing Qt widgets.
"""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_editor import (
        DocstringReviewEditorDialog,
    )
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_support import (
        backup_source_file,
        docstring_text_from_row,
        docstring_text_or_placeholder,
        format_review_row_context,
        format_tab1_findings_for_editor,
        format_tab1_snippets,
        manual_review_is_inside_project_root,
        manual_review_safe_int,
        project_root_for_window,
        refresh_tab1_findings_for_window,
    )


ROOT = Path(__file__).resolve().parents[1]
HELP_DIR = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
SUPPORT = HELP_DIR / "manual_docstring_review_support.py"
EDITOR = HELP_DIR / "manual_docstring_review_editor.py"


def _literal_all(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            return []
        out: list[str] = []
        for item in node.value.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                out.append(item.value)
        return out
    return []


def test_editor_public_surface_is_statically_tested() -> None:
    exports = _literal_all(EDITOR)

    assert "DocstringReviewEditorDialog" in exports


def test_support_public_surface_is_statically_tested() -> None:
    exports = set(_literal_all(SUPPORT))

    expected = {
        "backup_source_file",
        "docstring_text_from_row",
        "docstring_text_or_placeholder",
        "format_review_row_context",
        "format_tab1_findings_for_editor",
        "format_tab1_snippets",
        "manual_review_is_inside_project_root",
        "manual_review_safe_int",
        "project_root_for_window",
        "refresh_tab1_findings_for_window",
    }
    assert expected.issubset(exports)


def test_import_statements_remain_visible_to_static_analyzers() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_docstring_review_editor import" in text
    assert "manual_docstring_review_support import" in text
    assert "DocstringReviewEditorDialog" in text
    assert "manual_review_is_inside_project_root" in text


if __name__ == "__main__":
    test_editor_public_surface_is_statically_tested()
    test_support_public_surface_is_statically_tested()
    test_import_statements_remain_visible_to_static_analyzers()
    print("T3R005 manual review public contract import tests passed.")
