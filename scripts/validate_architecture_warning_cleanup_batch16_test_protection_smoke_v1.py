"""Validate Batch 16 test-protection smoke coverage."""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch16-test-protection-smoke-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

__all__ = ["main"]

PY_COMPILE_TARGETS = (
    Path("tests/test_architecture_warning_cleanup_batch16_public_contract_coverage.py"),
    Path("scripts/validate_architecture_warning_cleanup_batch15_remaining_side_effects_v1.py"),
    Path("scripts/validate_architecture_warning_cleanup_batch16_test_protection_smoke_v1.py"),
)

REQUIRED_IMPORT_FRAGMENTS = (
    "startup_kernel.boot_text",
    "startup_kernel.constants",
    "startup_kernel.generic_helpers",
    "startup_kernel.source_resolution",
    "kanda_reasoner_app.error_memory_gui._clipboard_export",
    "kanda_reasoner_app.error_memory_gui._correction_guard",
    "kanda_reasoner_app.error_memory_gui._intake_actions_mixin",
    "kanda_reasoner_app.error_memory_gui._project_paths_mixin",
    "kanda_reasoner_app.freeze_after_update_gui._local_ai_formulary",
    "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help._run_execution",
    "kanda_reasoner_app.templates.green_sonar_monitor",
    "scripts.validate_bridge_error_memory_implementation_error_gate_v1",
    "tools.validate_router_bridge_module_size_law_v1",
)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""

    if not condition:
        raise AssertionError(message)


def validate_py_compile() -> None:
    """Compile all Batch 16 touched Python files."""

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


def validate_import_declarations() -> None:
    """Verify the smoke test declares the intended direct coverage imports."""

    test_path = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch16_public_contract_coverage.py"
    tree = ast.parse(test_path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    for fragment in REQUIRED_IMPORT_FRAGMENTS:
        require(
            any(name == fragment or name.startswith(fragment + ".") for name in imports),
            f"missing direct smoke import declaration for {fragment}",
        )


def validate_smoke_test_module() -> None:
    """Import and run the smoke test without invoking pytest collection."""

    test_path = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch16_public_contract_coverage.py"
    spec = importlib.util.spec_from_file_location("batch16_public_contract_coverage", test_path)
    require(spec is not None and spec.loader is not None, "could not load smoke test spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.test_batch16_runtime_safe_public_contracts_are_importable()
    module.test_batch16_static_only_contract_targets_are_declared()


def validate_batch15_public_surface_contract() -> None:
    """Verify the Batch 15 validator now exposes only its public entry point."""

    path = PROJECT_ROOT / "scripts/validate_architecture_warning_cleanup_batch15_remaining_side_effects_v1.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    require(
                        isinstance(node.value, ast.List)
                        and len(node.value.elts) == 1
                        and isinstance(node.value.elts[0], ast.Constant)
                        and node.value.elts[0].value == "main",
                        "Batch 15 validator __all__ is not narrow",
                    )
                    return
    raise AssertionError("Batch 15 validator __all__ is missing")


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
    marker = (
        "MISSING_PUBLIC_SURFACE_CONTROL "
        "scripts/validate_architecture_warning_cleanup_batch15_remaining_side_effects_v1.py"
    )
    require(marker not in output, "Batch 15 validator still lacks public-surface control")


def main() -> int:
    """Run focused Batch 16 validation."""

    validate_py_compile()
    validate_import_declarations()
    validate_smoke_test_module()
    validate_batch15_public_surface_contract()
    validate_architecture_no_errors()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
