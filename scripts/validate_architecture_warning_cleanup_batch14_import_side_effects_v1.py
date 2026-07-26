"""Validate architecture warning cleanup batch 14."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "architecture-warning-cleanup-batch14-import-side-effects-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

SIDE_EFFECT_TARGETS = [
    "scripts/validate_complete_bridge_list_button_v1.py",
    "scripts/validate_error_memory_intake_refactor_completion_guard_v1.py",
    "scripts/validate_error_memory_intake_refactor_train_car_1_v1.py",
    "scripts/validate_file_retrieval_refactor_completion_guard_v1.py",
    "scripts/validate_file_retrieval_refactor_train_car_1_v1.py",
    "scripts/validate_freeze_hint_intake_contract_refactor_completion_guard_v1.py",
    "scripts/validate_freeze_hint_intake_contract_refactor_train_car_1_v1.py",
    "scripts/validate_prompt_router_reasoner_review_store_refactor_train_car_1_v1.py",
    "scripts/validate_routing_signal_scorer_contract_refactor_completion_guard_v1.py",
    "scripts/validate_routing_signal_scorer_contract_refactor_train_car_1_v1.py",
    "scripts/validate_source_tree_exporter_refactor_completion_guard_v1.py",
    "scripts/validate_source_tree_exporter_refactor_train_car_1_v1.py",
]

COMPILE_TARGETS = SIDE_EFFECT_TARGETS + [
    "scripts/validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1.py",
    "scripts/validate_architecture_warning_cleanup_batch14_import_side_effects_v1.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/complete_bridge_list_private_impl.py",
    "kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py",
]

ALLOWED_REMAINING_SIDE_EFFECTS = {
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py",
    "scripts/validate_sync_startup_kernel_refactor_train_car_7_v1.py",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def _is_sys_path_insert_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if not isinstance(func, ast.Attribute) or func.attr != "insert":
        return False
    value = func.value
    return (
        isinstance(value, ast.Attribute)
        and value.attr == "path"
        and isinstance(value.value, ast.Name)
        and value.value.id == "sys"
    )


def _statement_contains_sys_path_insert(statement: ast.stmt) -> bool:
    for node in ast.walk(statement):
        if _is_sys_path_insert_call(node):
            return True
    return False


def _assert_no_top_level_sys_path_insert(relative_path: str) -> None:
    tree = ast.parse(_text(relative_path), filename=relative_path)
    for statement in tree.body:
        if isinstance(statement, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
            continue
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        _assert(
            not _statement_contains_sys_path_insert(statement),
            "top-level sys.path.insert remains in " + relative_path,
        )


def _assert_py_compile() -> None:
    command = [sys.executable, "-m", "py_compile"] + COMPILE_TARGETS
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    _assert(result.returncode == 0, "py_compile failed:\n" + result.stdout)


def _assert_targeted_content() -> None:
    for relative_path in SIDE_EFFECT_TARGETS:
        _assert_no_top_level_sys_path_insert(relative_path)
        text = _text(relative_path)
        _assert(
            "def _ensure_project_root_on_path() -> None:" in text,
            "missing project-root path helper in " + relative_path,
        )

    batch13_text = _text("scripts/validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1.py")
    _assert('__all__ = ["main"]' in batch13_text, "batch13 validator is missing narrow __all__")

    bridge_text = _text("kanda_reasoner_app/reasoner_tools_shell/runner_help/complete_bridge_list_private_impl.py")
    _assert("from PySide6.QtWidgets import" not in bridge_text, "literal Qt import remains in bridge helper")
    _assert("importlib.import_module(\"PySide6.QtWidgets\")" in bridge_text, "lazy Qt import helper missing")

    mixin_text = _text("kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py")
    _assert(
        "load_pending_ai_assisted_error_lesson_intake_now as load_pending_ai_assisted_error_lesson_intake_now_impl" in mixin_text,
        "pending loader import alias missing",
    )
    _assert(
        "return load_pending_ai_assisted_error_lesson_intake_now_impl(self, project_root)" in mixin_text,
        "pending loader alias is not used by the wrapper method",
    )


def _architecture_output() -> str:
    command = [
        sys.executable,
        "kanda_reasoner_app/manage_architecture/manage_architecture.py",
        "--root",
        str(PROJECT_ROOT),
        "--validate",
    ]
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    _assert(result.returncode == 0, "architecture validation returned non-zero:\n" + result.stdout)
    return result.stdout


def _issue_paths(output: str, code: str) -> list[str]:
    prefix = "WARNING " + code
    paths: list[str] = []
    for line in output.splitlines():
        if not line.startswith(prefix):
            continue
        left = line.split("::", 1)[0]
        parts = left.split()
        if parts:
            paths.append(parts[-1].replace("\\", "/"))
    return paths


def _assert_architecture_warning_shape() -> None:
    output = _architecture_output()
    _assert("Errors: 0" in output, "architecture validation introduced errors")
    _assert("DUPLICATE_PUBLIC_SYMBOL" not in output, "duplicate public symbol regression detected")
    _assert("IMPORT_HEAVINESS_STARTUP" not in output, "Qt import heaviness warning remains")
    _assert("SYMBOL_SHADOWING" not in output, "symbol shadowing warning remains")
    _assert(
        "MISSING_PUBLIC_SURFACE_CONTROL scripts/validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1.py"
        not in output,
        "batch13 validator public surface warning remains",
    )

    remaining_side_effects = set(_issue_paths(output, "SIDE_EFFECT_ON_IMPORT"))
    _assert(
        remaining_side_effects <= ALLOWED_REMAINING_SIDE_EFFECTS,
        "unexpected side-effect-on-import warnings remain: " + repr(sorted(remaining_side_effects)),
    )


def main() -> int:
    _assert_py_compile()
    _assert_targeted_content()
    _assert_architecture_warning_shape()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
