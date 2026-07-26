# project-path: tools/validate_error_memory_pending_duplicate_warning_silent_v10.py
"""Focused validation for Error Memory pending duplicate warning silence v10."""
from __future__ import annotations

import ast
import py_compile
from pathlib import Path

FEATURE_ID = "error-memory-pending-duplicate-warning-silent-v10"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/error_memory_gui/_pending_loader.py",
    "tools/validate_error_memory_pending_duplicate_warning_silent_v10.py",
]
OLD_MESSAGE_PARTS = [
    "This AI-assisted Error Memory lesson was not loaded into the intake window",
    "Pending source kept for user control",
    "Error Memory intake already memorized",
]


def _read(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        raise AssertionError(f"Missing required file: {rel_path}")
    return path.read_text(encoding="utf-8")


def _line_count(rel_path: str) -> int:
    return len(_read(rel_path).splitlines())


def _compile_files() -> None:
    for rel_path in FILES:
        py_compile.compile(str(ROOT / rel_path), doraise=True)


def _assert_line_limits() -> None:
    for rel_path in FILES:
        count = _line_count(rel_path)
        if count > 500:
            raise AssertionError(f"{rel_path} has {count} lines; limit is 500")


def _function_node(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Missing function: {name}")


def _assert_duplicate_warning_silent() -> None:
    rel_path = "kanda_reasoner_app/error_memory_gui/_pending_loader.py"
    text = _read(rel_path)
    for old_text in OLD_MESSAGE_PARTS:
        if old_text in text:
            raise AssertionError(f"Old duplicate warning text still exists: {old_text}")
    if "tab._show_duplicate_pending_intake_warning" in text:
        raise AssertionError("Loader still calls duplicate warning hook during row load")

    tree = ast.parse(text, filename=rel_path)
    warning_fn = _function_node(tree, "show_duplicate_pending_intake_warning")
    if any(isinstance(node, ast.Call) for node in ast.walk(warning_fn)):
        raise AssertionError("Duplicate warning compatibility hook must not show dialogs or call helpers")
    if "del tab, lesson_id, pending_file" not in ast.get_source_segment(text, warning_fn):
        raise AssertionError("Duplicate warning hook must explicitly discard its arguments")

    loader_fn = _function_node(tree, "load_pending_intake_row_into_editor")
    loader_src = ast.get_source_segment(text, loader_fn) or ""
    if "del show_duplicate_warning" not in loader_src:
        raise AssertionError("Row loader must ignore old show_duplicate_warning flag")
    if "Memorize Error owns duplicate cleanup" not in loader_src:
        raise AssertionError("Row loader must document that Memorize Error owns duplicate cleanup")


def main() -> int:
    _compile_files()
    _assert_line_limits()
    _assert_duplicate_warning_silent()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
