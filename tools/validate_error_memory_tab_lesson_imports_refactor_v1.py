# project-path: tools/validate_error_memory_tab_lesson_imports_refactor_v1.py
"""Validate Error Memory Tab Lesson Imports Refactor v1."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "error-memory-tab-lesson-imports-refactor-v1"


def _fail(message: str) -> int:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    
    Returns
    -------
    int
        The integer result.
    """
    
    print("VALIDATION ERROR:", message)
    return 1


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    root = Path.cwd()
    tab = root / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
    helper = root / "kanda_reasoner_app/error_memory_gui/_lesson_imports.py"
    text_payloads = root / "kanda_reasoner_app/error_memory_gui/_text_payloads.py"
    pending_sources = root / "kanda_reasoner_app/error_memory_gui/_pending_sources.py"
    lesson_payloads = root / "kanda_reasoner_app/error_memory_gui/_lesson_payloads.py"
    test_file = root / "tests/test_error_memory_tab_lesson_imports_public_contract.py"

    for path in (tab, helper, text_payloads, pending_sources, lesson_payloads, test_file):
        if not path.exists():
            return _fail(f"missing required file: {path.as_posix()}")

    tab_text = tab.read_text(encoding="utf-8")
    helper_text = helper.read_text(encoding="utf-8")
    test_text = test_file.read_text(encoding="utf-8")

    if "from kanda_reasoner_app.error_memory_gui._lesson_imports import" not in tab_text:
        return _fail("error_memory_tab.py does not import _lesson_imports")
    if "import zipfile" in tab_text:
        return _fail("error_memory_tab.py still owns ZIP import/scanning dependency")
    if "def formatted_text_from_manifested_lesson_zip" not in helper_text:
        return _fail("helper missing formatted_text_from_manifested_lesson_zip")
    if "def formatted_import_text_for_window" not in helper_text:
        return _fail("helper missing formatted_import_text_for_window")
    if "PySide6" in helper_text or "QWidget" in helper_text:
        return _fail("_lesson_imports.py must stay non-GUI")
    if "error_memory_tab" in helper_text or "ErrorMemoryTab" in helper_text:
        return _fail("_lesson_imports.py must not import upward into ErrorMemoryTab facade")
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab" not in test_text:
        return _fail("test must preserve ErrorMemoryTab public facade import")
    if "from kanda_reasoner_app.error_memory_gui._lesson_imports import" not in test_text:
        return _fail("test must directly cover _lesson_imports helper")

    mod = ast.parse(tab_text)
    class_node = next((node for node in mod.body if isinstance(node, ast.ClassDef) and node.name == "ErrorMemoryTab"), None)
    if class_node is None:
        return _fail("ErrorMemoryTab class not found")
    methods = {node.name for node in class_node.body if isinstance(node, ast.FunctionDef)}
    for method in ("_formatted_text_from_manifested_lesson_zip", "_formatted_import_text_for_window"):
        if method not in methods:
            return _fail(f"wrapper method missing after extraction: {method}")

    line_count = len(tab_text.splitlines())
    if line_count >= 1705:
        return _fail(f"error_memory_tab.py did not shrink from cluster 3 baseline: {line_count}")

    compile_result = subprocess.run([
        sys.executable,
        "-m",
        "py_compile",
        str(tab),
        str(helper),
        str(test_file),
    ], cwd=root)
    if compile_result.returncode != 0:
        return _fail("py_compile failed")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
