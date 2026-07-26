"""Public contract tests for Error Memory tab memorize-flow extraction."""
from __future__ import annotations

import ast
from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _memorize_flow

ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_memorize_flow.py"


class _FakeEdit:
    def __init__(self, text: str = "") -> None:
        self._text = text
        self.cleared = False
        self.written: list[str] = []

    def toPlainText(self) -> str:
        return self._text

    def setPlainText(self, text: str) -> None:
        self._text = text
        self.written.append(text)

    def clear(self) -> None:
        self._text = ""
        self.cleared = True


class _FakeItem:
    def __init__(self, value: str) -> None:
        self.value = value

    def data(self, role: object) -> str:
        return self.value

    def text(self) -> str:
        return self.value


class _FakeTable:
    def __init__(self) -> None:
        self.selected: list[int] = []
        self.scrolled: list[_FakeItem] = []
        self.items = {1: _FakeItem("lesson-target")}

    def rowCount(self) -> int:
        return 3

    def item(self, row: int, column: int) -> _FakeItem | None:
        if column != 4:
            return None
        return self.items.get(row)

    def selectRow(self, row: int) -> None:
        self.selected.append(row)

    def scrollToItem(self, item: _FakeItem) -> None:
        self.scrolled.append(item)


class _FakeTab:
    def __init__(self) -> None:
        self.received_preview_edit = _FakeEdit("editor text")
        self.raw_error_edit = _FakeEdit("raw text")
        self.lessons_table = _FakeTable()
        self._selected_lesson_id = ""
        self._loaded_pending_intake_file = ""
        self._loaded_pending_intake_lesson_id = ""
        self._dismissed_pending_intake_files: set[str] = set()
        self._dismissed_pending_intake_lesson_ids: set[str] = set()
        self._last_received_lesson = None
        self.reloads = 0

    def _text_has_formatted_lesson_payload(self, text: str) -> bool:
        return text.startswith("formatted")

    def _row_kind_for_row(self, row: int) -> str:
        return "lesson" if row == 1 else "pending_edit"

    def _reload_table(self) -> None:
        self.reloads += 1

    def _consume_loaded_pending_intake_file_if_matches(self, lesson: dict, *, allow_lesson_id_change: bool = False) -> bool:
        return _memorize_flow.consume_loaded_pending_intake_file_if_matches(self, lesson, allow_lesson_id_change=allow_lesson_id_change)

    def _select_saved_active_lesson_row(self, lesson_id: str) -> bool:
        return _memorize_flow.select_saved_active_lesson_row(self, lesson_id)


def test_memorize_flow_helper_public_contract() -> None:
    expected = {
        "candidate_text_for_memorize",
        "clear_ai_assisted_intake_after_memorize",
        "consume_loaded_pending_intake_file_if_matches",
        "memorize_error_from_text_window",
        "save_active_ready_lesson",
        "select_saved_active_lesson_row",
    }
    assert set(_memorize_flow.__all__) == expected
    for name in expected:
        assert hasattr(_memorize_flow, name)


def test_memorize_flow_helper_does_not_import_facade_or_pyside_top_level() -> None:
    tree = ast.parse(HELPER.read_text(encoding="utf-8"))
    imported_modules: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            imported_modules.append(node.module or "")
    assert not any("error_memory_tab" in item for item in imported_modules)
    assert not any(item.startswith("PySide6") for item in imported_modules)


def test_error_memory_tab_keeps_public_facade_wrappers() -> None:
    text = TAB.read_text(encoding="utf-8")
    assert "from kanda_reasoner_app.error_memory_gui._memorize_flow import (" in text
    assert "def _candidate_text_for_memorize(self) -> tuple[str, str]:" in text
    assert "return candidate_text_for_memorize(self)" in text
    assert "def _memorize_error_from_text_window(self) -> None:" in text
    assert "memorize_error_from_text_window(self)" in text
    assert "def _clear_ai_assisted_intake_after_memorize(self, lesson: dict[str, Any]) -> None:" in text


def test_candidate_text_prefers_error_editor_then_raw_intake() -> None:
    tab = _FakeTab()
    tab.received_preview_edit = _FakeEdit("formatted editor")
    assert _memorize_flow.candidate_text_for_memorize(tab) == ("formatted editor", "Error Editor")
    tab.received_preview_edit = _FakeEdit("plain editor")
    tab.raw_error_edit = _FakeEdit("formatted raw")
    assert _memorize_flow.candidate_text_for_memorize(tab) == ("formatted raw", "AI-assisted error lesson intake")
    tab.raw_error_edit = _FakeEdit("plain raw")
    assert _memorize_flow.candidate_text_for_memorize(tab) == ("", "")


def test_select_saved_active_lesson_row_uses_lesson_rows(monkeypatch) -> None:
    tab = _FakeTab()
    monkeypatch.setattr(_memorize_flow, "_qt_user_role", lambda: 256)
    assert _memorize_flow.select_saved_active_lesson_row(tab, "lesson-target") is True
    assert tab._selected_lesson_id == "lesson-target"
    assert tab.lessons_table.selected == [1]


def test_clear_ai_assisted_intake_after_memorize_clears_and_selects(monkeypatch) -> None:
    tab = _FakeTab()
    monkeypatch.setattr(_memorize_flow, "_qt_user_role", lambda: 256)
    _memorize_flow.clear_ai_assisted_intake_after_memorize(tab, {"lesson_id": "lesson-target"})
    assert tab.raw_error_edit.cleared is True
    assert tab._selected_lesson_id == "lesson-target"
    assert tab.reloads == 1
    assert tab.lessons_table.selected == [1]
