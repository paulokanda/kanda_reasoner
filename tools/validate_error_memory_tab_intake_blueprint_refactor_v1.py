"""Validate Error Memory tab intake blueprint helper extraction."""
from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-intake-blueprint-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_intake_blueprint.py"
TEST = ROOT / "tests/test_error_memory_tab_intake_blueprint_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._intake_blueprint import (",
    "error_lesson_intake_blueprint_clipboard_text(",
    "error_memory_prompt_template_dir(self._current_project_root(), module_file=__file__)",
    "read_error_memory_intake_template_file(",
    "def _error_lesson_intake_blueprint_clipboard_text(self, *, context_text: str = \"\") -> str:",
    "def _copy_error_lesson_intake_blueprint_to_clipboard(self) -> None:",
    "def _show_active_ready_failure_copy_window(self, *, source_label: str, lesson: dict[str, Any]) -> None:",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def error_memory_prompt_template_dir(project_root: Path, *, module_file: str) -> Path:",
    "def read_error_memory_intake_template_file(project_root: Path, filename: str, *, module_file: str) -> str:",
    "def error_lesson_intake_blueprint_clipboard_text(",
    "ERROR MEMORY AI INTAKE REQUEST",
    "Do not invent validation evidence.",
    "ERROR OR DRAFT CONTEXT TO CONVERT:",
]


def _fail(message: str) -> None:
    raise SystemExit("VALIDATION FAIL: " + message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail("missing file: " + str(path))
    return path.read_text(encoding="utf-8")


def _assert_no_upward_or_gui_imports(source: str) -> None:
    forbidden = ["PySide", "QtCore", "QtGui", "QtWidgets", "error_memory_tab", "ErrorMemoryTab"]
    for token in forbidden:
        if token in source:
            _fail("_intake_blueprint.py contains forbidden dependency token: " + token)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = ""
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            for alias in getattr(node, "names", []):
                module = module + " " + alias.name
            if "PySide" in module or "error_memory_tab" in module:
                _fail("_intake_blueprint.py imports forbidden module: " + module)


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_intake_blueprint.py missing snippet: " + snippet)
    _assert_no_upward_or_gui_imports(helper_text)
    if "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons" in tab_text and "relative = Path" in tab_text:
        _fail("error_memory_tab.py still owns old template-dir implementation block")
    if len(tab_text.splitlines()) >= 1657:
        _fail("error_memory_tab.py did not shrink below cluster 4 line count")
    compile_result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(TAB), str(HELPER), str(TEST)],
        cwd=str(ROOT),
    )
    if compile_result.returncode != 0:
        _fail("py_compile failed")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
