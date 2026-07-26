"""Validate Error Memory tab clipboard/export helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-clipboard-export-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_clipboard_export.py"
TEST = ROOT / "tests/test_error_memory_tab_clipboard_export_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._clipboard_export import (",
    "copy_complete_error_memory_json_to_clipboard,",
    "copy_error_draft_to_clipboard,",
    "export_for_ai,",
    "def _copy_complete_error_memory_json_to_clipboard(self, text: str) -> None:",
    "copy_complete_error_memory_json_to_clipboard(text)",
    "def _show_action_done(self, title: str, message: str, detail_text: str='') -> None:",
    "show_action_done(self, title, message, detail_text)",
    "def _copy_error_draft_to_clipboard(self) -> None:",
    "copy_error_draft_to_clipboard(self)",
    "def _export_for_ai(self) -> None:",
    "export_for_ai(self)",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def copy_complete_error_memory_json_to_clipboard(text: str) -> None:",
    "def copy_path_to_clipboard(tab: Any, path: Path, label: str) -> None:",
    "def copy_error_lesson_intake_blueprint_to_clipboard(tab: Any) -> None:",
    "def show_active_ready_failure_copy_window(tab: Any, *, source_label: str, lesson: dict[str, Any]) -> None:",
    "def copy_ai_assisted_intake_error_draft_to_clipboard(tab: Any) -> None:",
    "def copy_error_draft_to_clipboard(tab: Any) -> None:",
    "def export_for_ai(tab: Any) -> None:",
    "write_complete_error_memory_ai_clipboard_export(root, include_inactive=True)",
    "QTimer.singleShot(1000",
]

FORBIDDEN_OLD_TAB_SNIPPETS = [
    "clipboard = QApplication.clipboard()\n        clipboard.clear(mode=QClipboard.Mode.Clipboard)",
    "clipboard_text = self._error_lesson_intake_blueprint_clipboard_text(context_text=context_text)\n            QApplication.clipboard().setText",
    "result = write_complete_error_memory_ai_clipboard_export(root, include_inactive=True)",
    "QTimer.singleShot(1000, lambda text=clipboard_text: self._copy_complete_error_memory_json_to_clipboard(text))",
]


def _fail(message: str) -> None:
    raise SystemExit("VALIDATION FAIL: " + message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail("missing file: " + str(path))
    return path.read_text(encoding="utf-8")


def _assert_no_top_level_gui_or_upward_imports(source: str) -> None:
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("PySide6"):
                _fail("_clipboard_export.py has top-level PySide import: " + module)
            if "error_memory_tab" in module:
                _fail("_clipboard_export.py imports facade upward: " + module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("PySide6") or "error_memory_tab" in alias.name:
                    _fail("_clipboard_export.py has forbidden top-level import: " + alias.name)
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab" in source:
        _fail("_clipboard_export.py imports error_memory_tab")


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_clipboard_export.py missing snippet: " + snippet)
    for snippet in FORBIDDEN_OLD_TAB_SNIPPETS:
        if snippet in tab_text:
            _fail("error_memory_tab.py still owns old clipboard/export block: " + snippet[:80])
    _assert_no_top_level_gui_or_upward_imports(helper_text)
    if "from PySide6.QtGui import QClipboard" in tab_text:
        _fail("error_memory_tab.py still imports QClipboard")
    if "from PySide6.QtWidgets import QApplication" in tab_text:
        _fail("error_memory_tab.py still imports QApplication")
    if "from kanda_reasoner_app.error_memory.exporter import" in tab_text:
        _fail("error_memory_tab.py still imports exporter functions")
    if len(tab_text.splitlines()) >= 1266:
        _fail("error_memory_tab.py did not shrink below cluster 10 line count")
    if len(helper_text.splitlines()) > 500:
        _fail("_clipboard_export.py exceeds module-size law")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _clipboard_export

    expected_exports = {
        "copy_ai_assisted_intake_error_draft_to_clipboard",
        "copy_complete_error_memory_json_to_clipboard",
        "copy_error_draft_to_clipboard",
        "copy_error_lesson_intake_blueprint_to_clipboard",
        "copy_path_to_clipboard",
        "export_for_ai",
        "show_action_done",
        "show_active_ready_failure_copy_window",
    }
    if set(_clipboard_export.__all__) != expected_exports:
        _fail("_clipboard_export.__all__ does not match expected exports")

    class FakeClipboard:
        def __init__(self) -> None:
            self.value = ""
        def clear(self, *, mode=None) -> None:
            self.value = ""
        def setText(self, text: str, *, mode=None) -> None:
            self.value = text
        def text(self, *, mode=None) -> str:
            return self.value

    class FakeApplication:
        clipboard_obj = FakeClipboard()
        @staticmethod
        def clipboard() -> FakeClipboard:
            return FakeApplication.clipboard_obj
        @staticmethod
        def processEvents() -> None:
            return None

    _clipboard_export._application = lambda: FakeApplication
    _clipboard_export._clipboard_mode = lambda: object()
    payload = '{"lessons": []}\n'
    _clipboard_export.copy_complete_error_memory_json_to_clipboard(payload)
    if FakeApplication.clipboard_obj.value != payload:
        _fail("clipboard export helper did not copy JSON payload")
    try:
        _clipboard_export.copy_complete_error_memory_json_to_clipboard("E:/kanda/second_prompt_files")
    except ValueError:
        pass
    else:
        _fail("clipboard export helper accepted path-like payload")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
