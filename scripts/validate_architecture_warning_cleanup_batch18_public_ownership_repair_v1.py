"""Validate Batch 18 public ownership repair."""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch18-public-ownership-repair-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

__all__ = ["main"]

REPAIR_SCRIPT = Path("scripts/repair_ai_response_patch_delivery_public_ownership_batch18_v1.py")
SMOKE_TEST = Path("tests/test_architecture_warning_cleanup_batch18_public_ownership_repair.py")
HELPER_PATHS = (
    Path("scripts/validate_ai_response_patch_delivery_contract.py"),
    Path("scripts/validate_ai_response_patch_delivery_audit_runner.py"),
    Path("scripts/validate_ai_response_patch_delivery_text_helpers.py"),
)
FACADE_PATH = Path("scripts/validate_ai_response_patch_delivery.py")
PY_COMPILE_TARGETS = (REPAIR_SCRIPT, SMOKE_TEST)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when validation fails."""

    if not condition:
        raise AssertionError(message)


def _top_level_all(path: Path) -> object:
    """Return the literal top-level __all__ value from a Python file."""

    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
                return ast.literal_eval(node.value)
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__" and node.value is not None:
                return ast.literal_eval(node.value)
    return None


def validate_py_compile() -> None:
    """Compile Batch 18 files and local patch-delivery modules when present."""

    targets = list(PY_COMPILE_TARGETS)
    targets.extend([path for path in (FACADE_PATH,) + HELPER_PATHS if (PROJECT_ROOT / path).exists()])
    for rel_path in targets:
        path = PROJECT_ROOT / rel_path
        require(path.exists(), f"missing py_compile target: {rel_path}")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        require(result.returncode == 0, f"py_compile failed for {rel_path}: {result.stderr or result.stdout}")


def validate_repair_script_check_mode_when_targets_exist() -> None:
    """Run repair script --check when the target helper files exist locally."""

    if not all((PROJECT_ROOT / path).exists() for path in (FACADE_PATH,) + HELPER_PATHS):
        return
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / REPAIR_SCRIPT), "--check"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"repair --check failed: {result.stderr or result.stdout}")
    require(f"CHECK OK: {FEATURE_ID}" in (result.stdout + result.stderr), "missing repair check marker")


def validate_public_ownership_when_targets_exist() -> None:
    """Assert facade owns public symbols and helper modules are implementation-only."""

    if not all((PROJECT_ROOT / path).exists() for path in (FACADE_PATH,) + HELPER_PATHS):
        return
    require(
        _top_level_all(PROJECT_ROOT / FACADE_PATH)
        == ["ResponseValidationError", "validate_response_text", "validate_zip_member_names"],
        "facade __all__ does not own expected symbols",
    )
    for rel_path in HELPER_PATHS:
        require(_top_level_all(PROJECT_ROOT / rel_path) == [], f"helper __all__ is not implementation-only: {rel_path}")


def validate_smoke_test_import_declarations() -> None:
    """Verify the Batch 18 test imports public contracts directly."""

    test_path = PROJECT_ROOT / SMOKE_TEST
    tree = ast.parse(test_path.read_text(encoding="utf-8"))
    source = test_path.read_text(encoding="utf-8")
    required_fragments = (
        "scripts.validate_ai_response_patch_delivery",
        "scripts.validate_ai_response_patch_delivery_contract",
        "scripts.validate_ai_response_patch_delivery_audit_runner",
        "scripts.validate_ai_response_patch_delivery_text_helpers",
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_core_mixin",
        "scripts.validate_architecture_warning_cleanup_batch17_line_count_smoke_v1",
    )
    require(isinstance(tree, ast.Module), "test file did not parse as module")
    for fragment in required_fragments:
        require(fragment in source, f"missing smoke coverage fragment: {fragment}")


def validate_smoke_test_module_when_targets_exist() -> None:
    """Run the direct smoke test when all target files are present locally."""

    if not all((PROJECT_ROOT / path).exists() for path in (FACADE_PATH,) + HELPER_PATHS):
        return
    test_path = PROJECT_ROOT / SMOKE_TEST
    spec = importlib.util.spec_from_file_location("batch18_public_ownership_repair", test_path)
    require(spec is not None and spec.loader is not None, "could not load Batch 18 smoke test")
    module = importlib.util.module_from_spec(spec)
    root_text = str(PROJECT_ROOT)
    inserted = False
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
        inserted = True
    try:
        spec.loader.exec_module(module)
        module.test_batch18_patch_delivery_facade_owns_public_validator_symbols()
        module.test_batch18_patch_delivery_helpers_are_implementation_only()
        module.test_batch18_new_retriever_mixins_keep_public_class_contracts()
        module.test_batch18_batch17_validator_has_direct_smoke_coverage()
    finally:
        if inserted:
            try:
                sys.path.remove(root_text)
            except ValueError:
                pass


def validate_architecture_no_errors_when_available() -> None:
    """Run architecture validation and require no errors when the validator exists."""

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
    require("DUPLICATE_PUBLIC_SYMBOL" not in output, "duplicate public symbol marker remains")
    for symbol in ("ResponseValidationError", "validate_response_text", "validate_zip_member_names"):
        require(symbol not in output or "DUPLICATE_PUBLIC_SYMBOL" not in output, f"duplicate output remains for {symbol}")


def main() -> int:
    """Run focused Batch 18 validation."""

    print("Batch 18 validation: py_compile", flush=True)
    validate_py_compile()
    print("Batch 18 validation: repair check", flush=True)
    validate_repair_script_check_mode_when_targets_exist()
    print("Batch 18 validation: ownership", flush=True)
    validate_public_ownership_when_targets_exist()
    print("Batch 18 validation: smoke declarations", flush=True)
    validate_smoke_test_import_declarations()
    print("Batch 18 validation: smoke module", flush=True)
    validate_smoke_test_module_when_targets_exist()
    print("Batch 18 validation: architecture errors", flush=True)
    validate_architecture_no_errors_when_available()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
