"""Validate Error Memory tab correction/guard helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-correction-guard-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_correction_guard.py"
TEST = ROOT / "tests/test_error_memory_tab_correction_guard_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._correction_guard import (",
    "active_ready_missing_text,",
    "apply_heuristic_correction_to_error_editor,",
    "check_against_lessons,",
    "heuristic_correction_result_for_editor,",
    "operation_phase_for_guard,",
    "refresh_heuristic_correction_button_state,",
    "show_repeat_guard_report,",
    "def _active_ready_missing_text(self, lesson: dict[str, Any], *, limit: int=20) -> str:",
    "return active_ready_missing_text(lesson, limit=limit)",
    "def _heuristic_correction_result_for_editor(self):",
    "return heuristic_correction_result_for_editor(self)",
    "def _apply_heuristic_correction_to_error_editor(self) -> None:",
    "apply_heuristic_correction_to_error_editor(self)",
    "def _operation_phase_for_guard(self, raw_text: str) -> str:",
    "return operation_phase_for_guard(self, raw_text)",
    "def _check_against_lessons(self) -> None:",
    "check_against_lessons(self)",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def active_ready_missing_text(lesson: dict[str, Any], *, limit: int = 20) -> str:",
    "def heuristic_correction_result_for_editor(tab: Any):",
    "def refresh_heuristic_correction_button_state(tab: Any) -> None:",
    "def apply_heuristic_correction_to_error_editor(tab: Any) -> None:",
    "def operation_phase_for_guard(tab: Any, raw_text: str) -> str:",
    "def check_against_lessons(tab: Any) -> None:",
    "def show_repeat_guard_report(tab: Any, report: dict[str, Any]) -> None:",
    "analyze_error_against_lessons(",
    "classify_and_normalize_error_lesson_text(",
]

FORBIDDEN_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory.guard import analyze_error_against_lessons",
    "from kanda_reasoner_app.error_memory.heuristic_normalizer import classify_and_normalize_error_lesson_text",
    "from kanda_reasoner_app.error_memory.models import active_ready, active_ready_missing_reasons",
    "return classify_and_normalize_error_lesson_text(self.received_preview_edit.toPlainText(), project_slug=self._current_project_root().name)",
    "report = analyze_error_against_lessons(self._current_project_root(), raw_text, operation_phase=self._operation_phase_for_guard(raw_text), include_drafts=True, include_deprecated=False)",
    "dialog = QDialog(self)\n        dialog.setWindowTitle('Repeat Error Guard - advisory report')",
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
                _fail("_correction_guard.py has top-level PySide import: " + module)
            if "error_memory_tab" in module:
                _fail("_correction_guard.py imports facade upward: " + module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("PySide6") or "error_memory_tab" in alias.name:
                    _fail("_correction_guard.py has forbidden top-level import: " + alias.name)
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab" in source:
        _fail("_correction_guard.py imports error_memory_tab")


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_correction_guard.py missing snippet: " + snippet)
    for snippet in FORBIDDEN_TAB_SNIPPETS:
        if snippet in tab_text:
            _fail("error_memory_tab.py still owns old correction/guard block: " + snippet[:90])
    _assert_no_top_level_gui_or_upward_imports(helper_text)
    if len(tab_text.splitlines()) >= 1142:
        _fail("error_memory_tab.py did not shrink below cluster 11 line count")
    if len(helper_text.splitlines()) > 500:
        _fail("_correction_guard.py exceeds module-size law")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _correction_guard

    expected_exports = {
        "active_ready_missing_text",
        "apply_heuristic_correction_to_error_editor",
        "check_against_lessons",
        "heuristic_correction_result_for_editor",
        "operation_phase_for_guard",
        "refresh_heuristic_correction_button_state",
        "show_repeat_guard_report",
    }
    if set(_correction_guard.__all__) != expected_exports:
        _fail("_correction_guard.py __all__ mismatch")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
