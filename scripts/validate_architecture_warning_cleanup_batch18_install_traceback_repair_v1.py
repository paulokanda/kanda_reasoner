"""Validate Batch 18 install-traceback repair."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch18-install-traceback-repair-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

__all__ = ["main"]

REPAIR_SCRIPT = Path("scripts/repair_ai_response_patch_delivery_public_ownership_batch18_v1.py")
BATCH18_VALIDATOR = Path("scripts/validate_architecture_warning_cleanup_batch18_public_ownership_repair_v1.py")
FACADE_PATH = Path("scripts/validate_ai_response_patch_delivery.py")
HELPER_PATHS = (
    Path("scripts/validate_ai_response_patch_delivery_contract.py"),
    Path("scripts/validate_ai_response_patch_delivery_audit_runner.py"),
    Path("scripts/validate_ai_response_patch_delivery_text_helpers.py"),
)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when validation fails."""

    if not condition:
        raise AssertionError(message)


def _top_level_all(path: Path) -> object:
    """Return the literal top-level __all__ value from a Python file."""

    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
                return ast.literal_eval(node.value)
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__" and node.value is not None:
                return ast.literal_eval(node.value)
    return None


def _run(args: list[str], *, label: str) -> str:
    """Run a command and return combined output."""

    result = subprocess.run(
        args,
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, f"{label} failed with exit {result.returncode}: {output}")
    return output


def validate_py_compile() -> None:
    """Compile the repair and validation files."""

    targets = [REPAIR_SCRIPT, Path(__file__).relative_to(PROJECT_ROOT)]
    if (PROJECT_ROOT / BATCH18_VALIDATOR).exists():
        targets.append(BATCH18_VALIDATOR)
    targets.extend(path for path in (FACADE_PATH,) + HELPER_PATHS if (PROJECT_ROOT / path).exists())
    for rel_path in targets:
        _run([sys.executable, "-m", "py_compile", str(PROJECT_ROOT / rel_path)], label=f"py_compile {rel_path}")


def validate_repair_script_check_mode() -> None:
    """Run the repaired Batch 18 repair script in check mode."""

    output = _run([sys.executable, str(PROJECT_ROOT / REPAIR_SCRIPT), "--check"], label="repair --check")
    require("CHECK OK: architecture-warning-cleanup-batch18-public-ownership-repair-v1" in output, "missing CHECK OK marker")
    require("Traceback (most recent call last)" not in output, "repair --check emitted traceback")


def validate_public_ownership() -> None:
    """Assert facade/helper public ownership contract."""

    require(
        _top_level_all(PROJECT_ROOT / FACADE_PATH)
        == ["ResponseValidationError", "validate_response_text", "validate_zip_member_names"],
        "facade __all__ does not own expected symbols",
    )
    for rel_path in HELPER_PATHS:
        require(_top_level_all(PROJECT_ROOT / rel_path) == [], f"helper __all__ is not implementation-only: {rel_path}")


def validate_batch18_validator_if_present() -> None:
    """Run the original Batch 18 focused validator when present."""

    if not (PROJECT_ROOT / BATCH18_VALIDATOR).exists():
        return
    output = _run([sys.executable, str(PROJECT_ROOT / BATCH18_VALIDATOR)], label="Batch 18 focused validator")
    require("VALIDATION OK: architecture-warning-cleanup-batch18-public-ownership-repair-v1" in output, "missing Batch 18 validation marker")


def validate_architecture_errors_clear() -> None:
    """Run architecture validation and require duplicate-public-symbol errors are gone."""

    validator = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
    if not validator.exists():
        return
    output = _run([sys.executable, str(validator), "--root", str(PROJECT_ROOT), "--validate"], label="architecture validation")
    require("Errors: 0" in output, "architecture validation did not report Errors: 0")
    require("DUPLICATE_PUBLIC_SYMBOL" not in output, "duplicate public symbol marker remains")


def main() -> int:
    """Run focused validation."""

    print("Batch 18 traceback repair validation: py_compile", flush=True)
    validate_py_compile()
    print("Batch 18 traceback repair validation: repair check", flush=True)
    validate_repair_script_check_mode()
    print("Batch 18 traceback repair validation: public ownership", flush=True)
    validate_public_ownership()
    print("Batch 18 traceback repair validation: original validator", flush=True)
    validate_batch18_validator_if_present()
    print("Batch 18 traceback repair validation: architecture errors", flush=True)
    validate_architecture_errors_clear()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
