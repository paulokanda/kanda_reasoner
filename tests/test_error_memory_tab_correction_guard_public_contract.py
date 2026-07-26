"""Public-contract checks for ErrorMemoryTab correction/guard extraction."""
from __future__ import annotations

import ast
from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _correction_guard

ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_correction_guard.py"


class _FakeResult:
    def __init__(self, *, can_apply: bool, level: int, lesson: dict | None, reason: str) -> None:
        self.can_apply = can_apply
        self.level = level
        self.lesson = lesson
        self.reason = reason


class _FakeEdit:
    def __init__(self, text: str = "") -> None:
        self.text = text

    def toPlainText(self) -> str:
        return self.text


class _FakeTab:
    def __init__(self) -> None:
        self.received_preview_edit = _FakeEdit('{"operation_phase":"install"}')
        self.raw_error_edit = _FakeEdit('')


def test_correction_guard_helper_public_contract() -> None:
    expected = {
        "active_ready_missing_text",
        "apply_heuristic_correction_to_error_editor",
        "check_against_lessons",
        "heuristic_correction_result_for_editor",
        "operation_phase_for_guard",
        "refresh_heuristic_correction_button_state",
        "show_repeat_guard_report",
    }
    assert set(_correction_guard.__all__) == expected
    for name in expected:
        assert hasattr(_correction_guard, name)


def test_correction_guard_helper_does_not_import_facade_or_pyside_top_level() -> None:
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
    assert "from kanda_reasoner_app.error_memory_gui._correction_guard import (" in text
    assert "def _active_ready_missing_text(self, lesson: dict[str, Any], *, limit: int=20) -> str:" in text
    assert "return active_ready_missing_text(lesson, limit=limit)" in text
    assert "def _refresh_heuristic_correction_button_state(self) -> None:" in text
    assert "refresh_heuristic_correction_button_state(self)" in text
    assert "def _operation_phase_for_guard(self, raw_text: str) -> str:" in text
    assert "return operation_phase_for_guard(self, raw_text)" in text
    assert "def _check_against_lessons(self) -> None:" in text
    assert "check_against_lessons(self)" in text


def test_operation_phase_for_guard_prefers_editor_json() -> None:
    assert _correction_guard.operation_phase_for_guard(_FakeTab(), "freeze traceback") == "install"


def test_operation_phase_for_guard_uses_text_fallbacks() -> None:
    tab = _FakeTab()
    tab.received_preview_edit = _FakeEdit('not json')
    assert _correction_guard.operation_phase_for_guard(tab, "validation failed") == "validation"
    assert _correction_guard.operation_phase_for_guard(tab, "freeze entry") == "freeze_write"
    assert _correction_guard.operation_phase_for_guard(tab, "traceback") == "runtime"
