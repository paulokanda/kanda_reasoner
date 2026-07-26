# project-path: tools/validate_error_memory_window_sync_after_resolution_v1.py
"""Validate Error Memory intake/editor synchronization after resolution actions."""
from __future__ import annotations

import ast
import py_compile
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "kanda_reasoner_app/error_memory_gui/_window_sync.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_actions.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
]

LOAD_SURFACES = [
    "kanda_reasoner_app/error_memory_gui/_receive_import.py",
    "kanda_reasoner_app/error_memory_gui/_pending_loader.py",
    "kanda_reasoner_app/error_memory_gui/_table_view.py",
]

MAX_LINES = 500
SUCCESS_MARKER = "VALIDATION OK: error-memory-window-sync-after-resolution-v1"


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _line_count(relative_path: str) -> int:
    return len(_read(relative_path).splitlines())


def _function_source(relative_path: str, function_name: str) -> str:
    text = _read(relative_path)
    tree = ast.parse(text)
    lines = text.splitlines()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return "\n".join(lines[node.lineno - 1: node.end_lineno])
    raise AssertionError(f"Missing function {function_name} in {relative_path}")


def _validate_compile_and_line_counts() -> None:
    for relative_path in TARGETS + LOAD_SURFACES:
        absolute_path = PROJECT_ROOT / relative_path
        py_compile.compile(str(absolute_path), doraise=True)
        count = _line_count(relative_path)
        _assert(count <= MAX_LINES, f"{relative_path} has {count} lines")


def _validate_clear_helper() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/_window_sync.py")
    for fragment in (
        "def clear_error_memory_work_windows",
        "raw_error_edit",
        "received_preview_edit",
        "clearSelection",
        "_last_received_lesson = None",
        "_selected_lesson_id = \"\"",
        "_loaded_pending_intake_file = \"\"",
        "_loaded_pending_intake_lesson_id = \"\"",
        "_refresh_heuristic_correction_button_state",
    ):
        _assert(fragment in text, f"clear helper missing fragment: {fragment}")


def _validate_resolution_actions_clear_both_windows() -> None:
    lesson_actions = "kanda_reasoner_app/error_memory_gui/_lesson_actions.py"
    memorize_flow = "kanda_reasoner_app/error_memory_gui/_memorize_flow.py"
    required_functions = [
        (lesson_actions, "save_preview_lesson"),
        (lesson_actions, "save_draft_lesson_from_partial"),
        (lesson_actions, "set_selected_lesson_status"),
        (lesson_actions, "supersede_selected_lesson"),
        (memorize_flow, "save_active_ready_lesson"),
        (memorize_flow, "clear_ai_assisted_intake_after_memorize"),
    ]
    for relative_path, function_name in required_functions:
        source = _function_source(relative_path, function_name)
        _assert(
            "clear_error_memory_work_windows(tab" in source,
            f"{function_name} does not clear both work windows",
        )


def _validate_pending_consumption_on_success() -> None:
    pairs = [
        ("kanda_reasoner_app/error_memory_gui/_lesson_actions.py", "save_preview_lesson"),
        ("kanda_reasoner_app/error_memory_gui/_lesson_actions.py", "save_draft_lesson_from_partial"),
        ("kanda_reasoner_app/error_memory_gui/_lesson_actions.py", "set_selected_lesson_status"),
        ("kanda_reasoner_app/error_memory_gui/_lesson_actions.py", "supersede_selected_lesson"),
        ("kanda_reasoner_app/error_memory_gui/_memorize_flow.py", "save_active_ready_lesson"),
    ]
    for relative_path, function_name in pairs:
        source = _function_source(relative_path, function_name)
        _assert(
            "_consume_loaded_pending_intake_file_if_matches" in source,
            f"{function_name} does not consume pending intake after save",
        )


def _validate_load_paths_still_populate_both_windows() -> None:
    receive = _function_source(
        "kanda_reasoner_app/error_memory_gui/_receive_import.py",
        "load_formatted_lesson_into_tab",
    )
    _assert("raw_error_edit.setPlainText" in receive, "receive/import no longer fills intake")
    _assert("received_preview_edit.setPlainText" in receive, "receive/import no longer fills editor")

    pending = _function_source(
        "kanda_reasoner_app/error_memory_gui/_pending_loader.py",
        "load_pending_intake_row_into_editor",
    )
    _assert("_set_ai_assisted_intake_and_error_editor_from_pending_text" in pending, "pending formatted load does not sync windows")
    _assert("raw_error_edit.setPlainText" in pending, "pending raw load does not fill intake")
    _assert("received_preview_edit.setPlainText" in pending, "pending raw load does not fill editor")

    table = _function_source(
        "kanda_reasoner_app/error_memory_gui/_table_view.py",
        "load_selected_lesson_into_preview",
    )
    _assert("raw_error_edit.setPlainText" in table, "saved lesson selection does not fill intake")
    _assert("received_preview_edit.setPlainText" in table, "saved lesson selection does not fill editor")


def main() -> int:
    _validate_compile_and_line_counts()
    _validate_clear_helper()
    _validate_resolution_actions_clear_both_windows()
    _validate_pending_consumption_on_success()
    _validate_load_paths_still_populate_both_windows()
    print(SUCCESS_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
