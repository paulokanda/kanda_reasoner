"""Validate Large Module AST target queue v1 patch."""
from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "large-module-ast-target-queue-v1"
ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
HELPER = ROOT / "kanda_reasoner_app/manage_architecture/large_module_target_queue.py"
TEST = ROOT / "tests/test_large_module_target_queue_public_contract.py"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def top_level_import_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def main() -> int:
    for path in (GUI, HELPER, TEST):
        assert_true(path.exists(), f"missing required file: {path}")
        py_compile.compile(str(path), doraise=True)

    helper_text = HELPER.read_text(encoding="utf-8")
    gui_text = GUI.read_text(encoding="utf-8")
    test_text = TEST.read_text(encoding="utf-8")

    assert_true("parse_module_too_large_findings" in helper_text, "helper does not parse MODULE_TOO_LARGE findings")
    assert_true("format_target_counter" in helper_text, "helper does not format target counter")
    assert_true("_prev_large_module_target_btn" in gui_text, "previous large-module target button missing")
    assert_true("_next_large_module_target_btn" in gui_text, "next large-module target button missing")
    assert_true("_refresh_large_module_targets_from_audit_results" in gui_text, "audit results do not refresh target queue")
    assert_true("mode == 'validate'" in gui_text, "target queue is not tied to Validate/Project Audit results")
    assert_true("Run Validate first" in gui_text, "inactive AST guidance missing")
    assert_true("line_count <= 500" in gui_text, "resolved module removal guard missing")
    assert_true("parse_module_too_large_findings" in test_text, "public contract test misses parser")

    helper_imports = top_level_import_modules(HELPER)
    forbidden = {"PySide6", "kanda_reasoner_app"}
    assert_true(not (helper_imports & forbidden), f"helper has forbidden top-level imports: {helper_imports & forbidden}")

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); import tests.test_large_module_target_queue_public_contract as t; t.test_parse_module_too_large_findings_sorts_descending_and_filters_resolved(); t.test_format_target_counter_reports_position_and_lines()",
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
