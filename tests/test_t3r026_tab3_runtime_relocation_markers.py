"""Regression tests for Tab 3 runtime relocation markers."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ASK_RUNTIME = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime"
GUI_RUNTIME = ROOT / "reasoner_tools_gui" / "tab3_manual_review_runtime"


MARKERS = {
    "editor_runtime.py": "TAB3_EDITOR_RUNTIME_RELOCATED",
    "layout_runtime.py": "TAB3_LAYOUT_RUNTIME_RELOCATED",
    "report_panel_runtime.py": "TAB3_REPORT_PANEL_RUNTIME_RELOCATED",
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


def test_relocation_marker_files_have_unique_public_contracts() -> None:
    for file_name, symbol in MARKERS.items():
        path = ASK_RUNTIME / file_name
        assert path.is_file()
        assert _literal_all(path) == [symbol]
        text = _read(path)
        assert "PySide6" not in text
        assert "QPushButton" not in text
        assert "QDialog" not in text


def test_relocation_marker_symbols_are_directly_importable() -> None:
    from kanda_reasoner_app.tab3_manual_review_runtime.editor_runtime import (
        TAB3_EDITOR_RUNTIME_RELOCATED,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.layout_runtime import (
        TAB3_LAYOUT_RUNTIME_RELOCATED,
    )
    from kanda_reasoner_app.tab3_manual_review_runtime.report_panel_runtime import (
        TAB3_REPORT_PANEL_RUNTIME_RELOCATED,
    )

    assert TAB3_EDITOR_RUNTIME_RELOCATED == "reasoner_tools_gui.tab3_manual_review_runtime.editor_runtime"
    assert TAB3_LAYOUT_RUNTIME_RELOCATED == "reasoner_tools_gui.tab3_manual_review_runtime.layout_runtime"
    assert TAB3_REPORT_PANEL_RUNTIME_RELOCATED == "reasoner_tools_gui.tab3_manual_review_runtime.report_panel_runtime"


def test_gui_runtime_still_contains_real_implementation() -> None:
    assert "PySide6" in _read(GUI_RUNTIME / "editor_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "layout_runtime.py")
    assert "PySide6" in _read(GUI_RUNTIME / "report_panel_runtime.py")


if __name__ == "__main__":
    test_relocation_marker_files_have_unique_public_contracts()
    test_relocation_marker_symbols_are_directly_importable()
    test_gui_runtime_still_contains_real_implementation()
    print("T3R026 Tab 3 runtime relocation marker tests passed.")
