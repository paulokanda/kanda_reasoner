# project-path: tools/validate_error_memory_clean_buttons_sync_v8.py
"""Focused validation for Error Memory Clean buttons clearing both work windows."""
from __future__ import annotations

import ast
import py_compile
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES = [
    Path("kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py"),
    Path("kanda_reasoner_app/error_memory_gui/_table_draft_mixin.py"),
    Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py"),
]
MAX_LINES = 500


def _source(rel_path: Path) -> str:
    path = PROJECT_ROOT / rel_path
    if not path.exists():
        raise AssertionError(f"Missing file: {rel_path}")
    return path.read_text(encoding="utf-8")


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Missing function: {name}")


def _called_attr_names(fn: ast.FunctionDef) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            callee = node.func
            if isinstance(callee, ast.Attribute):
                names.add(callee.attr)
            elif isinstance(callee, ast.Name):
                names.add(callee.id)
    return names


def validate_files_compile_and_line_counts() -> None:
    for rel_path in FILES:
        path = PROJECT_ROOT / rel_path
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_LINES:
            raise AssertionError(f"{rel_path} has {line_count} lines; max {MAX_LINES}")


def validate_clean_helper_logic() -> None:
    intake_src = _source(FILES[0])
    tree = ast.parse(intake_src)
    helper = _function(tree, "_clean_both_work_windows_from_clean_button")
    helper_calls = _called_attr_names(helper)
    required_helper_calls = {
        "_dismiss_loaded_pending_intake_file_for_session",
        "clear",
        "_refresh_heuristic_correction_button_state",
    }
    missing = sorted(required_helper_calls - helper_calls)
    if missing:
        raise AssertionError(f"Clean helper missing calls: {missing}")

    helper_text = ast.get_source_segment(intake_src, helper) or ""
    required_text = [
        "self.raw_error_edit.clear()",
        "self.received_preview_edit.clear()",
        "self._last_received_lesson = None",
        "self._selected_lesson_id = ''",
    ]
    for needle in required_text:
        if needle not in helper_text:
            raise AssertionError(f"Clean helper missing exact behavior: {needle}")

    intake_clean = _function(tree, "_clean_intake_window")
    if "_clean_both_work_windows_from_clean_button" not in _called_attr_names(intake_clean):
        raise AssertionError("Intake Clean button does not call shared clean-both helper")


def validate_editor_clean_uses_same_helper() -> None:
    table_src = _source(FILES[1])
    tree = ast.parse(table_src)
    editor_clean = _function(tree, "_clean_error_editor")
    if "_clean_both_work_windows_from_clean_button" not in _called_attr_names(editor_clean):
        raise AssertionError("Error Editor Clean button does not call shared clean-both helper")
    editor_text = ast.get_source_segment(table_src, editor_clean) or ""
    forbidden = "self.received_preview_edit.clear()\n        self._last_received_lesson = None"
    if forbidden in editor_text:
        raise AssertionError("Error Editor Clean still uses old one-window clear body")


def validate_tooltips_are_not_stale() -> None:
    tab_src = _source(FILES[2])
    if "Clear the AI-assisted intake window only" in tab_src:
        raise AssertionError("Intake Clean tooltip still says it clears only one window")
    if "Clear only the Error Editor window" in tab_src:
        raise AssertionError("Editor Clean tooltip still says it clears only one window")
    if "Clear both AI-assisted intake and Error Editor" not in tab_src:
        raise AssertionError("Intake Clean tooltip does not mention both windows")
    if "Clear both Error Editor and AI-assisted intake" not in tab_src:
        raise AssertionError("Editor Clean tooltip does not mention both windows")


def main() -> None:
    validate_files_compile_and_line_counts()
    validate_clean_helper_logic()
    validate_editor_clean_uses_same_helper()
    validate_tooltips_are_not_stale()
    print("VALIDATION OK: error-memory-clean-buttons-sync-v8")


if __name__ == "__main__":
    main()
