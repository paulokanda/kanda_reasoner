"""Validate Batch 15 remaining import-side-effect cleanup."""

from __future__ import annotations

import ast
import importlib
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch15-remaining-side-effects-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

__all__ = ["main"]

SIDE_EFFECT_TARGETS = (
    Path("kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py"),
    Path("scripts/validate_sync_startup_kernel_refactor_train_car_7_v1.py"),
)

PY_COMPILE_TARGETS = (
    Path("kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py"),
    Path("scripts/validate_sync_startup_kernel_refactor_train_car_7_v1.py"),
    Path("tests/test_architecture_warning_cleanup_batch15_public_contracts.py"),
)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""

    if not condition:
        raise AssertionError(message)


def _is_sys_path_insert_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "insert"
        and isinstance(func.value, ast.Attribute)
        and func.value.attr == "path"
        and isinstance(func.value.value, ast.Name)
        and func.value.value.id == "sys"
    )


def _has_top_level_sys_path_insert(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Expr) and _is_sys_path_insert_call(node.value):
            return True
        if isinstance(node, ast.If):
            for child in ast.walk(node):
                if _is_sys_path_insert_call(child):
                    return True
    return False


def validate_no_top_level_sys_path_insert() -> None:
    """Validate that patched modules no longer mutate sys.path at import scan level."""

    for rel_path in SIDE_EFFECT_TARGETS:
        path = PROJECT_ROOT / rel_path
        require(path.exists(), f"missing side-effect target: {rel_path}")
        require(
            not _has_top_level_sys_path_insert(path),
            f"top-level sys.path.insert remains in {rel_path}",
        )


def validate_py_compile() -> None:
    """Compile all Batch 15 touched Python files."""

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


def validate_smoke_test_module() -> None:
    """Import and run the non-GUI public contract smoke test."""

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    module = importlib.import_module(
        "tests.test_architecture_warning_cleanup_batch15_public_contracts"
    )
    module.test_batch15_non_gui_public_contracts_are_importable()


def validate_architecture_no_new_errors() -> None:
    """Run architecture validation and verify the two target side-effect warnings are absent."""

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
    for rel_path in SIDE_EFFECT_TARGETS:
        marker = f"SIDE_EFFECT_ON_IMPORT        {rel_path.as_posix()}"
        require(marker not in output, f"target side-effect warning remains: {rel_path}")


def main() -> int:
    """Run focused Batch 15 validation."""

    validate_no_top_level_sys_path_insert()
    validate_py_compile()
    validate_smoke_test_module()
    validate_architecture_no_new_errors()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
