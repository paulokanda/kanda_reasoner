"""Validate Error Memory tab memorize-flow helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-memorize-flow-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_memorize_flow.py"
TEST = ROOT / "tests/test_error_memory_tab_memorize_flow_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._memorize_flow import (",
    "candidate_text_for_memorize,",
    "memorize_error_from_text_window,",
    "def _candidate_text_for_memorize(self) -> tuple[str, str]:",
    "return candidate_text_for_memorize(self)",
    "def _save_active_ready_lesson(self, lesson: dict[str, Any], success_prefix: str) -> Path | None:",
    "return save_active_ready_lesson(self, lesson, success_prefix)",
    "def _clear_ai_assisted_intake_after_memorize(self, lesson: dict[str, Any]) -> None:",
    "clear_ai_assisted_intake_after_memorize(self, lesson)",
    "def _memorize_error_from_text_window(self) -> None:",
    "memorize_error_from_text_window(self)",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def candidate_text_for_memorize(tab: Any) -> tuple[str, str]:",
    "def save_active_ready_lesson(tab: Any, lesson: dict[str, Any], success_prefix: str) -> Path | None:",
    "def consume_loaded_pending_intake_file_if_matches(tab: Any, lesson: dict[str, Any], *, allow_lesson_id_change: bool = False) -> bool:",
    "def select_saved_active_lesson_row(tab: Any, lesson_id: str) -> bool:",
    "def clear_ai_assisted_intake_after_memorize(tab: Any, lesson: dict[str, Any]) -> None:",
    "def memorize_error_from_text_window(tab: Any) -> None:",
    "from PySide6.QtWidgets import QMessageBox",
    "from PySide6.QtCore import Qt",
]

FORBIDDEN_OLD_TAB_SNIPPETS = [
    "editor_text = self.received_preview_edit.toPlainText().strip()\n        if self._text_has_formatted_lesson_payload(editor_text):",
    "lesson['status'] = 'active'\n        if not active_ready(lesson):",
    "marker = str(self._loaded_pending_intake_file or '').strip()\n        if not marker:",
    "for row in range(self.lessons_table.rowCount()):\n            if self._row_kind_for_row(row) != 'lesson':",
    "text, source_label = self._candidate_text_for_memorize()\n        if not text:",
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
                _fail("_memorize_flow.py has top-level PySide import: " + module)
            if "error_memory_tab" in module:
                _fail("_memorize_flow.py imports facade upward: " + module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("PySide6") or "error_memory_tab" in alias.name:
                    _fail("_memorize_flow.py has forbidden top-level import: " + alias.name)
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab" in source:
        _fail("_memorize_flow.py imports error_memory_tab")


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_memorize_flow.py missing snippet: " + snippet)
    for snippet in FORBIDDEN_OLD_TAB_SNIPPETS:
        if snippet in tab_text:
            _fail("error_memory_tab.py still owns old memorize-flow block: " + snippet[:80])
    _assert_no_top_level_gui_or_upward_imports(helper_text)
    if len(tab_text.splitlines()) >= 1362:
        _fail("error_memory_tab.py did not shrink below cluster 9 line count")
    if len(helper_text.splitlines()) > 500:
        _fail("_memorize_flow.py exceeds module-size law")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _memorize_flow

    expected_exports = {
        "candidate_text_for_memorize",
        "clear_ai_assisted_intake_after_memorize",
        "consume_loaded_pending_intake_file_if_matches",
        "memorize_error_from_text_window",
        "save_active_ready_lesson",
        "select_saved_active_lesson_row",
    }
    if set(_memorize_flow.__all__) != expected_exports:
        _fail("_memorize_flow.__all__ does not match expected exports")

    class FakeEdit:
        def __init__(self, text: str = "") -> None:
            self.text = text
            self.cleared = False
        def toPlainText(self) -> str:
            return self.text
        def clear(self) -> None:
            self.cleared = True
            self.text = ""
        def setPlainText(self, text: str) -> None:
            self.text = text

    class FakeTab:
        def __init__(self) -> None:
            self.received_preview_edit = FakeEdit("formatted editor")
            self.raw_error_edit = FakeEdit("formatted raw")
        def _text_has_formatted_lesson_payload(self, text: str) -> bool:
            return text.startswith("formatted")

    fake = FakeTab()
    if _memorize_flow.candidate_text_for_memorize(fake) != ("formatted editor", "Error Editor"):
        _fail("candidate_text_for_memorize did not prefer editor text")
    fake.received_preview_edit = FakeEdit("plain editor")
    if _memorize_flow.candidate_text_for_memorize(fake) != ("formatted raw", "AI-assisted error lesson intake"):
        _fail("candidate_text_for_memorize did not fall back to raw intake text")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
