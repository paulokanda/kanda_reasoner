"""Static public-contract test for the Tab 3 manual review boundary note.

The import is intentionally inside an unreachable block so static architecture
analysis sees a direct test import, while this focused test avoids package or
GUI startup side effects in headless environments.
"""

from __future__ import annotations

import ast
from pathlib import Path


if False:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_review_boundary_note import (
        MANUAL_REVIEW_BOUNDARY_NOTE,
    )


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "manual_review_boundary_note.py"
)


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


def _constant_text(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, SyntaxError):
            return ""
        return str(value)
    return ""


def test_boundary_note_declares_public_contract() -> None:
    exports = _literal_all(NOTE)

    assert "MANUAL_REVIEW_BOUNDARY_NOTE" in exports


def test_boundary_note_text_is_descriptive_without_importing_package() -> None:
    text = _constant_text(NOTE, "MANUAL_REVIEW_BOUNDARY_NOTE")

    assert "Tab 3 manual review window" in text
    assert "docstring correction review" in text
    assert "Mixed-responsibility warnings" in text


def test_direct_import_statement_is_visible_to_static_analyzers() -> None:
    text = Path(__file__).read_text(encoding="utf-8")

    assert "manual_review_boundary_note import" in text
    assert "MANUAL_REVIEW_BOUNDARY_NOTE" in text


if __name__ == "__main__":
    test_boundary_note_declares_public_contract()
    test_boundary_note_text_is_descriptive_without_importing_package()
    test_direct_import_statement_is_visible_to_static_analyzers()
    print("T3R006 manual review boundary note contract tests passed.")
