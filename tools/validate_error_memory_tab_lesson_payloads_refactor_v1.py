# project-path: tools/validate_error_memory_tab_lesson_payloads_refactor_v1.py
"""Validate Error Memory Tab Lesson Payloads Refactor v1."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

FEATURE_ID = 'error-memory-tab-lesson-payloads-refactor-v1'


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
    helper = root / "kanda_reasoner_app/error_memory_gui/_lesson_payloads.py"
    text_payloads = root / "kanda_reasoner_app/error_memory_gui/_text_payloads.py"
    pending_sources = root / "kanda_reasoner_app/error_memory_gui/_pending_sources.py"
    test_file = root / "tests/test_error_memory_tab_lesson_payloads_public_contract.py"

    for path in (tab, helper, text_payloads, pending_sources, test_file):
        if not path.exists():
            return _fail(f"missing required file: {path.as_posix()}")

    tab_text = tab.read_text(encoding="utf-8")
    helper_text = helper.read_text(encoding="utf-8")
    test_text = test_file.read_text(encoding="utf-8")

    if "from kanda_reasoner_app.error_memory_gui._lesson_payloads import" not in tab_text:
        return _fail("error_memory_tab.py does not import _lesson_payloads")
    if "build_lesson_from_ai_form" in tab_text or "parse_error_lesson_ai_response" in tab_text:
        return _fail("Error Memory tab still owns AI lesson parse/build internals")
    if "def canonical_draft_lesson_from_partial" not in helper_text:
        return _fail("helper missing canonical_draft_lesson_from_partial")
    if "def lesson_from_formatted_text" not in helper_text:
        return _fail("helper missing lesson_from_formatted_text")
    if "def text_is_formatted_error_lesson_payload" not in helper_text:
        return _fail("helper missing text_is_formatted_error_lesson_payload")
    if "PySide6" in helper_text or "QWidget" in helper_text:
        return _fail("_lesson_payloads.py must stay non-GUI")
    if "error_memory_tab" in helper_text or "ErrorMemoryTab" in helper_text:
        return _fail("_lesson_payloads.py must not import upward into ErrorMemoryTab facade")
    if "from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab" not in test_text:
        return _fail("test must preserve ErrorMemoryTab public facade import")
    if "from kanda_reasoner_app.error_memory_gui._lesson_payloads import" not in test_text:
        return _fail("test must directly cover _lesson_payloads helper")

    mod = ast.parse(tab_text)
    class_node = next((node for node in mod.body if isinstance(node, ast.ClassDef) and node.name == "ErrorMemoryTab"), None)
    if class_node is None:
        return _fail("ErrorMemoryTab class not found")
    methods = {node.name for node in class_node.body if isinstance(node, ast.FunctionDef)}
    for method in ("_lesson_from_formatted_text", "_canonical_draft_lesson_from_partial", "_text_is_formatted_error_lesson_payload"):
        if method not in methods:
            return _fail(f"wrapper method missing after extraction: {method}")

    line_count = len(tab_text.splitlines())
    if line_count >= 1763:
        return _fail(f"error_memory_tab.py did not shrink from cluster 2 baseline: {line_count}")

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
