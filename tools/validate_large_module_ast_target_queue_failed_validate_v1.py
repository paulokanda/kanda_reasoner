"""Validate Large Module AST Target Queue Failed Validate Population v1."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "large-module-ast-target-queue-failed-validate-v1"
ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
HELPER = ROOT / "kanda_reasoner_app/manage_architecture/large_module_target_queue.py"
TEST = ROOT / "tests/test_large_module_ast_target_queue_failed_validate_public_contract.py"


def fail(message: str) -> None:
    print(f"VALIDATION ERROR: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def get_method_body_text(source: str, method_name: str) -> str:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            return ast.get_source_segment(source, node) or ""
    fail(f"method not found: {method_name}")
    return ""


def assert_contains(text: str, snippet: str, label: str) -> None:
    if snippet not in text:
        fail(f"missing {label}")


def main() -> None:
    for path in (GUI, HELPER, TEST):
        if not path.exists():
            fail(f"missing file: {path.relative_to(ROOT)}")
        py_compile.compile(str(path), doraise=True)

    gui = read(GUI)
    handler = get_method_body_text(gui, "_handle_worker_error")
    assert_contains(handler, "if mode == 'validate':", "validate guard in error handler")
    assert_contains(handler, "self._refresh_large_module_targets_from_audit_results()", "failed validate queue refresh")
    assert_contains(handler, "Finished validate with issues; loaded", "status message for failed validate queue population")

    reset = get_method_body_text(gui, "_reset_large_module_target_state_for_new_project_audit_run")
    assert_contains(reset, "self._large_module_targets = []", "run-start queue reset remains intact")
    assert_contains(reset, "self._last_large_module_split_handoff = ''", "run-start handoff reset remains intact")

    helper = read(HELPER)
    assert_contains(helper, "parse_module_too_large_findings", "target parser helper remains available")
    assert_contains(helper, "MODULE_TOO_LARGE", "target parser still keys on MODULE_TOO_LARGE findings")

    test = read(TEST)
    assert_contains(test, "exit_code=1", "failed validate fixture")
    assert_contains(test, "parse_module_too_large_findings", "parser contract test")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
