"""Validate Batch 17 line-count and validator smoke coverage cleanup."""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch17-line-count-smoke-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

__all__ = ["main"]

LINE_COUNT_TARGETS = (
    Path("kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_command_runner.py"),
    Path("kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_environment_contract_detectors.py"),
    Path("kanda_reasoner_app/reasoner_context_collector/collector_scope.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/adviser_offline/promotion_gate/promotion_criteria_gate.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/generator_candidate_preparation_closure_shield.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_envelope_design.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_skeleton_design.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_commit_design.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/human_architectural_review_record_design.py"),
    Path("kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py"),
)

PY_COMPILE_TARGETS = LINE_COUNT_TARGETS + (
    Path("tests/test_architecture_warning_cleanup_batch17_validator_contracts.py"),
    Path("scripts/validate_architecture_warning_cleanup_batch17_line_count_smoke_v1.py"),
)

REQUIRED_TEST_IMPORTS = (
    "scripts.validate_architecture_warning_cleanup_batch15_remaining_side_effects_v1",
    "scripts.validate_architecture_warning_cleanup_batch16_test_protection_smoke_v1",
)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""

    if not condition:
        raise AssertionError(message)


def validate_py_compile() -> None:
    """Compile all Batch 17 touched Python files."""

    for rel_path in PY_COMPILE_TARGETS:
        path = PROJECT_ROOT / rel_path
        require(path.exists(), f"missing py_compile target: {rel_path}")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        require(
            result.returncode == 0,
            f"py_compile failed for {rel_path}: {result.stderr or result.stdout}",
        )


def validate_line_counts() -> None:
    """Verify behavior-neutral compaction brought selected modules to the bridge limit."""

    for rel_path in LINE_COUNT_TARGETS:
        path = PROJECT_ROOT / rel_path
        count = len(path.read_text(encoding="utf-8").splitlines())
        require(count <= 500, f"line count still above 500 for {rel_path}: {count}")


def validate_smoke_test_import_declarations() -> None:
    """Verify the new smoke test directly imports prior cleanup validators."""

    test_path = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch17_validator_contracts.py"
    tree = ast.parse(test_path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    for expected in REQUIRED_TEST_IMPORTS:
        require(expected in imports, f"missing validator smoke import: {expected}")


def validate_smoke_test_module() -> None:
    """Import and run the smoke test without broad pytest collection."""

    test_path = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch17_validator_contracts.py"
    spec = importlib.util.spec_from_file_location("batch17_validator_contracts", test_path)
    require(spec is not None and spec.loader is not None, "could not load Batch 17 smoke test spec")
    module = importlib.util.module_from_spec(spec)
    root_text = str(PROJECT_ROOT)
    inserted = False
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
        inserted = True
    try:
        spec.loader.exec_module(module)
        module.test_batch17_previous_cleanup_validators_expose_main_only()
    finally:
        if inserted:
            try:
                sys.path.remove(root_text)
            except ValueError:
                pass


def validate_architecture_no_errors() -> None:
    """Run architecture validation and require no errors."""

    validator = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
    if not validator.exists():
        return
    result = subprocess.run(
        [sys.executable, str(validator), "--root", str(PROJECT_ROOT), "--validate"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require("Errors: 0" in output, "architecture validation reported errors")
    for rel_path in LINE_COUNT_TARGETS:
        marker = f"MODULE_TOO_LARGE             {rel_path.as_posix()}"
        require(marker not in output, f"module-too-large warning remains for {rel_path}")


def main() -> int:
    """Run focused Batch 17 validation."""

    print("Batch 17 validation: py_compile", flush=True)
    validate_py_compile()
    print("Batch 17 validation: line counts", flush=True)
    validate_line_counts()
    print("Batch 17 validation: smoke import declarations", flush=True)
    validate_smoke_test_import_declarations()
    print("Batch 17 validation: smoke module", flush=True)
    validate_smoke_test_module()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
