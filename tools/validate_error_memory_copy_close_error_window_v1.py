# project-path: tools/validate_error_memory_copy_close_error_window_v1.py
"""Validate Error Memory AI correction copy-and-close error window patch."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path

FEATURE_ID = "error-memory-copy-close-error-window-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOUCHED_FILES = [
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py",
    "tools/validate_error_memory_copy_close_error_window_v1.py",
]


def _read(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _physical_line_count(relative_path: str) -> int:
    """Return the physical line count for a project file."""
    return len(_read(relative_path).splitlines())


def _compile_touched_files() -> None:
    """Compile touched Python files without importing Qt or project modules."""
    for relative_path in TOUCHED_FILES:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def _assert_line_counts() -> None:
    """Assert every touched module stays under the 500-line hard gate."""
    oversized = [
        relative_path
        for relative_path in TOUCHED_FILES
        if _physical_line_count(relative_path) > 500
    ]
    if oversized:
        joined = ", ".join(oversized)
        raise AssertionError("Touched module exceeds 500 physical lines: " + joined)


def _function_source(module_text: str, function_name: str) -> str:
    """Return source text for one top-level function."""
    module = ast.parse(module_text)
    lines = module_text.splitlines()
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return "\n".join(lines[node.lineno - 1: node.end_lineno])
    raise AssertionError("Function not found: " + function_name)


def _assert_ai_correction_error_uses_copy_close() -> None:
    """Assert local AI correction failures use the reusable copy-close window."""
    module_text = _read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    function_text = _function_source(module_text, "_show_copyable_error")
    required_fragments = [
        "show_error_copy_close_window",
        "Error Memory AI correction failed",
        "detail_text=raw_response",
        'button_text="Copy and Close"',
    ]
    missing = [fragment for fragment in required_fragments if fragment not in function_text]
    if missing:
        raise AssertionError("Missing copy-close fragment(s): " + ", ".join(missing))
    forbidden_fragments = [
        "QMessageBox(parent)",
        "setDetailedText",
        ".exec()",
    ]
    present = [fragment for fragment in forbidden_fragments if fragment in function_text]
    if present:
        raise AssertionError("Native message box fragment still present: " + ", ".join(present))


def _assert_error_template_contract() -> None:
    """Assert the reusable template exposes Copy and Close behavior."""
    template_text = _read("kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py")
    required_fragments = [
        "ErrorCopyCloseFloatingWindow",
        "show_error_copy_close_window",
        "CopyMessageFloatingWindow",
        'button_text: str = "Copy and Close"',
        "clipboard_text=clipboard_text",
        "detail_text=detail_text",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in template_text]
    if missing:
        raise AssertionError("Missing template fragment(s): " + ", ".join(missing))


def main() -> int:
    """Run focused validation."""
    _compile_touched_files()
    _assert_line_counts()
    _assert_ai_correction_error_uses_copy_close()
    _assert_error_template_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
