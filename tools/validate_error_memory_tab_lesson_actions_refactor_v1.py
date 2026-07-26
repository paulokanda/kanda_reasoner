"""Validate Error Memory tab lesson action helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-lesson-actions-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_lesson_actions.py"
TEST = ROOT / "tests/test_error_memory_tab_lesson_actions_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._lesson_actions import (",
    "save_preview_lesson,",
    "set_selected_lesson_status,",
    "undo_lesson_action,",
    "def _save_preview_lesson(self) -> None:",
    "save_preview_lesson(self)",
    "def _set_selected_lesson_status(self, status: str) -> None:",
    "set_selected_lesson_status(self, status)",
    "def _undo_lesson_action(self) -> None:",
    "undo_lesson_action(self)",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def save_preview_lesson(tab: Any) -> None:",
    "def delete_selected_lesson(tab: Any) -> None:",
    "def lesson_from_preview_or_selection(tab: Any) -> dict[str, Any] | None:",
    "def save_draft_lesson_from_partial(tab: Any, lesson: dict[str, Any], *, source_text: str, success_prefix: str) -> Path | None:",
    "def set_selected_lesson_status(tab: Any, status: str) -> None:",
    "def supersede_selected_lesson(tab: Any) -> None:",
    "def undo_lesson_action(tab: Any) -> None:",
    "from PySide6.QtWidgets import QMessageBox",
    "from PySide6.QtWidgets import QInputDialog",
]

FORBIDDEN_OLD_TAB_SNIPPETS = [
    "text = self.received_preview_edit.toPlainText().strip()\n        if not text:\n            QMessageBox.warning(self, 'Error Memory', 'No lesson JSON is shown in Error Editor.')",
    "answer = QMessageBox.question(self, 'Delete Error Memory lesson'",
    "replacement_id, ok = QInputDialog.getText(self, 'Supersede lesson'",
    "if self._undo_deleted_lesson:\n            try:\n                path = save_lesson(self._current_project_root(), self._undo_deleted_lesson)",
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
                _fail("_lesson_actions.py has top-level PySide import: " + module)
            if "error_memory_tab" in module:
                _fail("_lesson_actions.py imports facade upward: " + module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("PySide6") or "error_memory_tab" in alias.name:
                    _fail("_lesson_actions.py has forbidden top-level import: " + alias.name)
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab" in source:
        _fail("_lesson_actions.py imports error_memory_tab")


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_lesson_actions.py missing snippet: " + snippet)
    for snippet in FORBIDDEN_OLD_TAB_SNIPPETS:
        if snippet in tab_text:
            _fail("error_memory_tab.py still owns old lesson action block: " + snippet[:80])
    _assert_no_top_level_gui_or_upward_imports(helper_text)
    if len(tab_text.splitlines()) >= 1508:
        _fail("error_memory_tab.py did not shrink below cluster 8 line count")
    if len(helper_text.splitlines()) > 500:
        _fail("_lesson_actions.py exceeds module-size law")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _lesson_actions

    expected_exports = {
        "delete_selected_lesson",
        "lesson_from_preview_or_selection",
        "save_draft_lesson_from_partial",
        "save_preview_lesson",
        "set_selected_lesson_status",
        "supersede_selected_lesson",
        "undo_lesson_action",
    }
    if set(_lesson_actions.__all__) != expected_exports:
        _fail("_lesson_actions.__all__ does not match expected exports")

    class FakeEdit:
        def __init__(self, text: str = "") -> None:
            self.text = text
        def toPlainText(self) -> str:
            return self.text
        def setPlainText(self, text: str) -> None:
            self.text = text

    class FakeTab:
        def __init__(self) -> None:
            self.received_preview_edit = FakeEdit('{"lesson_id":"preview-id"}')
            self.calls = 0
        def _selected_lesson_id_from_table(self) -> str:
            self.calls += 1
            return "selected-id"
        def _current_project_root(self) -> Path:
            return ROOT

    fake = FakeTab()
    if _lesson_actions.lesson_from_preview_or_selection(fake) != {"lesson_id": "preview-id"}:
        _fail("lesson_from_preview_or_selection did not prefer preview JSON")
    if fake.calls != 0:
        _fail("lesson_from_preview_or_selection unexpectedly touched table selection")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
