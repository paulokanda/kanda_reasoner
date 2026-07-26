"""Public contract tests for Error Memory tab lesson action extraction."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _lesson_actions

ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_lesson_actions.py"


def test_lesson_actions_helper_public_contract() -> None:
    expected = {
        "delete_selected_lesson",
        "lesson_from_preview_or_selection",
        "save_draft_lesson_from_partial",
        "save_preview_lesson",
        "set_selected_lesson_status",
        "supersede_selected_lesson",
        "undo_lesson_action",
    }
    assert set(_lesson_actions.__all__) == expected
    for name in expected:
        assert hasattr(_lesson_actions, name)


def test_lesson_actions_helper_does_not_import_facade_or_pyside_top_level() -> None:
    source = HELPER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            imported_modules.append(node.module or "")
    assert not any("error_memory_tab" in item for item in imported_modules)
    assert not any(item.startswith("PySide6") for item in imported_modules)


def test_error_memory_tab_keeps_public_facade_wrappers() -> None:
    text = TAB.read_text(encoding="utf-8")
    assert "from kanda_reasoner_app.error_memory_gui._lesson_actions import (" in text
    assert "def _save_preview_lesson(self) -> None:" in text
    assert "save_preview_lesson(self)" in text
    assert "def _set_selected_lesson_status(self, status: str) -> None:" in text
    assert "set_selected_lesson_status(self, status)" in text
    assert "def _undo_lesson_action(self) -> None:" in text
    assert "undo_lesson_action(self)" in text
    assert "def _lesson_from_preview_or_selection(self) -> dict[str, Any] | None:" in text


class _FakeEdit:
    def __init__(self, text: str = "") -> None:
        self._text = text
        self.written: list[str] = []

    def toPlainText(self) -> str:
        return self._text

    def setPlainText(self, text: str) -> None:
        self.written.append(text)
        self._text = text


class _FakeTab:
    def __init__(self) -> None:
        self.received_preview_edit = _FakeEdit(json.dumps({"lesson_id": "preview-id"}))
        self._root = Path("/tmp/project")
        self.selected_calls = 0

    def _selected_lesson_id_from_table(self) -> str:
        self.selected_calls += 1
        return "selected-id"

    def _current_project_root(self) -> Path:
        return self._root


def test_lesson_from_preview_prefers_valid_editor_json() -> None:
    tab = _FakeTab()
    assert _lesson_actions.lesson_from_preview_or_selection(tab) == {"lesson_id": "preview-id"}
    assert tab.selected_calls == 0


def test_lesson_from_selection_uses_store_when_preview_invalid(monkeypatch) -> None:
    tab = _FakeTab()
    tab.received_preview_edit = _FakeEdit("not json")
    monkeypatch.setattr(
        _lesson_actions,
        "list_lessons",
        lambda root, include_inactive=False: [
            {"lesson_id": "other"},
            {"lesson_id": "selected-id", "status": "draft"},
        ],
    )
    assert _lesson_actions.lesson_from_preview_or_selection(tab) == {"lesson_id": "selected-id", "status": "draft"}
    assert tab.selected_calls == 1
