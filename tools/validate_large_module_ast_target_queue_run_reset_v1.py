"""Validate Large Module AST target queue run-reset v1 patch."""
from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "large-module-ast-target-queue-run-reset-v1"
ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
TEST = ROOT / "tests/test_large_module_ast_target_queue_run_reset_public_contract.py"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def get_method_body_text(source: str, method_name: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    fail(f"missing method: {method_name}")
    return ""


def main() -> int:
    for path in (GUI, TEST):
        assert_true(path.exists(), f"missing required file: {path}")
        py_compile.compile(str(path), doraise=True)

    gui_text = GUI.read_text(encoding="utf-8")
    test_text = TEST.read_text(encoding="utf-8")

    assert_true("def _reset_large_module_target_state_for_new_project_audit_run" in gui_text, "reset method missing")
    assert_true("self._reset_large_module_target_state_for_new_project_audit_run(mode)" in gui_text, "run_mode does not reset AST target queue")
    assert_true("Validate running - AST target queue will refresh from new results" in gui_text, "validate-running placeholder missing")
    assert_true("Run Validate to populate oversized module targets" in gui_text, "non-validate reset placeholder missing")
    assert_true("_last_large_module_split_handoff = ''" in gui_text, "handoff reset missing")

    run_body = get_method_body_text(gui_text, "run_mode")
    reset_pos = run_body.find("_reset_large_module_target_state_for_new_project_audit_run")
    clear_pos = run_body.find("self._output.clear()")
    assert_true(reset_pos != -1, "run_mode reset call missing")
    assert_true(clear_pos != -1, "run_mode output clear missing")
    assert_true(reset_pos < clear_pos, "AST target reset must happen before Project Audit output is cleared/replaced")

    reset_body = get_method_body_text(gui_text, "_reset_large_module_target_state_for_new_project_audit_run")
    for fragment in (
        "self._large_module_targets = []",
        "self._large_module_target_index = -1",
        "self._large_module_target_source = 'pending' if mode == 'validate' else 'none'",
        "self._last_large_module_split_handoff = ''",
        "self._sync_large_module_target_controls()",
    ):
        assert_true(fragment in reset_body, f"reset method missing fragment: {fragment}")

    assert_true("test_run_mode_resets_ast_queue_before_replacing_audit_results" in test_text, "public contract test missing reset check")

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); import tests.test_large_module_ast_target_queue_run_reset_public_contract as t; t.test_run_mode_resets_ast_queue_before_replacing_audit_results()",
        ],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert_true(result.returncode == 0, result.stdout)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
