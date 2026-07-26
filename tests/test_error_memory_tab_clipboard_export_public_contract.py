"""Public contract tests for Error Memory tab clipboard/export extraction."""
from __future__ import annotations

import ast
from pathlib import Path

from kanda_reasoner_app.error_memory_gui import _clipboard_export

ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_clipboard_export.py"


class _FakeClipboard:
    def __init__(self) -> None:
        self.value = ""
        self.cleared = False

    def clear(self, *, mode: object = None) -> None:
        self.cleared = True
        self.value = ""

    def setText(self, text: str, *, mode: object = None) -> None:
        self.value = text

    def text(self, *, mode: object = None) -> str:
        return self.value


class _FakeApplication:
    clipboard_obj = _FakeClipboard()
    events = 0

    @staticmethod
    def clipboard() -> _FakeClipboard:
        return _FakeApplication.clipboard_obj

    @staticmethod
    def processEvents() -> None:
        _FakeApplication.events += 1


class _FakeEdit:
    def __init__(self, text: str = "") -> None:
        self.text = text

    def toPlainText(self) -> str:
        return self.text


class _FakeTab:
    def __init__(self) -> None:
        self.raw_error_edit = _FakeEdit("raw evidence")
        self.received_preview_edit = _FakeEdit("editor evidence")
        self.action_calls: list[tuple[str, str, str]] = []

    def _error_lesson_intake_blueprint_clipboard_text(self, *, context_text: str = "") -> str:
        return "BLUEPRINT\n" + context_text

    def _show_action_done(self, title: str, message: str, detail_text: str = "") -> None:
        self.action_calls.append((title, message, detail_text))


def test_clipboard_export_helper_public_contract() -> None:
    expected = {
        "copy_ai_assisted_intake_error_draft_to_clipboard",
        "copy_complete_error_memory_json_to_clipboard",
        "copy_error_draft_to_clipboard",
        "copy_error_lesson_intake_blueprint_to_clipboard",
        "copy_path_to_clipboard",
        "export_for_ai",
        "show_action_done",
        "show_active_ready_failure_copy_window",
    }
    assert set(_clipboard_export.__all__) == expected
    for name in expected:
        assert hasattr(_clipboard_export, name)


def test_clipboard_export_helper_does_not_import_facade_or_pyside_top_level() -> None:
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
    assert "from kanda_reasoner_app.error_memory_gui._clipboard_export import (" in text
    assert "def _copy_complete_error_memory_json_to_clipboard(self, text: str) -> None:" in text
    assert "copy_complete_error_memory_json_to_clipboard(text)" in text
    assert "def _copy_error_draft_to_clipboard(self) -> None:" in text
    assert "copy_error_draft_to_clipboard(self)" in text
    assert "def _export_for_ai(self) -> None:" in text
    assert "export_for_ai(self)" in text


def test_complete_error_memory_json_clipboard_rejects_non_json(monkeypatch) -> None:
    monkeypatch.setattr(_clipboard_export, "_application", lambda: _FakeApplication)
    monkeypatch.setattr(_clipboard_export, "_clipboard_mode", lambda: object())
    try:
        _clipboard_export.copy_complete_error_memory_json_to_clipboard("E:/project/second_prompt_files")
    except ValueError as exc:
        assert "did not produce JSON" in str(exc) or "looks like a path" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_complete_error_memory_json_clipboard_copies_json(monkeypatch) -> None:
    _FakeApplication.clipboard_obj = _FakeClipboard()
    _FakeApplication.events = 0
    monkeypatch.setattr(_clipboard_export, "_application", lambda: _FakeApplication)
    monkeypatch.setattr(_clipboard_export, "_clipboard_mode", lambda: object())
    payload = '{"lessons": []}\n'
    _clipboard_export.copy_complete_error_memory_json_to_clipboard(payload)
    assert _FakeApplication.clipboard_obj.value == payload
    assert _FakeApplication.clipboard_obj.cleared is True
    assert _FakeApplication.events >= 1


def test_copy_error_drafts_include_source_window_context(monkeypatch) -> None:
    _FakeApplication.clipboard_obj = _FakeClipboard()
    monkeypatch.setattr(_clipboard_export, "_application", lambda: _FakeApplication)
    monkeypatch.setattr(_clipboard_export, "_clipboard_mode", lambda: object())
    tab = _FakeTab()
    _clipboard_export.copy_ai_assisted_intake_error_draft_to_clipboard(tab)
    assert "SOURCE WINDOW: AI-assisted error lesson intake" in _FakeApplication.clipboard_obj.value
    assert tab.action_calls
    _clipboard_export.copy_error_draft_to_clipboard(tab)
    assert "SOURCE WINDOW: Error Editor" in _FakeApplication.clipboard_obj.value
