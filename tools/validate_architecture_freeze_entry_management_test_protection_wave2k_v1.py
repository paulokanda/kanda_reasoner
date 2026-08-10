#!/usr/bin/env python3
# project-path: tools/validate_architecture_freeze_entry_management_test_protection_wave2k_v1.py
"""Validate focused test protection for frozen-entry mutation management."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-freeze-entry-management-test-protection-wave2k-v1"
TARGET_REL = Path(
    "kanda_reasoner_app/freeze_after_update/frozen_entry_management.py"
)
TEST_REL = Path("tests/test_frozen_entry_management_mutation_contract.py")
INHERITED_VALIDATOR_REL = Path(
    "tools/validate_freeze_list_frozen_manager_responsive_v1.py"
)
EXPECTED_TARGET_SHA256 = (
    "74b361e1a2355fd274c8613b9c8cc2797ea1f039946ec18fac2a4cf650968906"
)
EXPECTED_TEST_SHA256 = (
    "137f219b74cc6608292cf316c28533d4986a8afc7118a046511f5eb39427665c"
)
TARGET_MODULE = (
    "kanda_reasoner_app.freeze_after_update.frozen_entry_management"
)
EXPECTED_PUBLIC_SYMBOLS = (
    "activate_frozen_entries",
    "delete_last_deprecated_entry",
    "delete_selected_deprecated_entries",
    "inactivate_frozen_entries",
    "list_managed_frozen_entries",
    "undelete_last_frozen_entry",
)
REQUIRED_TEST_CALLS = set(EXPECTED_PUBLIC_SYMBOLS)


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def sha256_file(path: Path) -> str:
    """Return one file SHA-256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal_all(tree: ast.Module) -> tuple[str, ...]:
    """Return the literal module public surface."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            continue
        value = ast.literal_eval(node.value)
        require(
            isinstance(value, (list, tuple))
            and all(isinstance(item, str) for item in value),
            "FROZEN_ENTRY_MANAGEMENT_PUBLIC_SURFACE_NOT_LITERAL",
        )
        return tuple(value)
    raise RuntimeError("FROZEN_ENTRY_MANAGEMENT_PUBLIC_SURFACE_MISSING")


def imported_modules(tree: ast.Module) -> set[str]:
    """Return direct imported module names."""
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result


def called_names(tree: ast.Module) -> set[str]:
    """Return simple function names called by the test module."""
    result: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            result.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            result.add(node.func.attr)
    return result


def validate_static(root: Path) -> None:
    """Validate source immutability and the direct functional test contract."""
    target = root / TARGET_REL
    test = root / TEST_REL
    inherited = root / INHERITED_VALIDATOR_REL

    require(target.is_file(), "FROZEN_ENTRY_MANAGEMENT_SOURCE_MISSING")
    require(test.is_file(), "FROZEN_ENTRY_MANAGEMENT_TEST_MISSING")
    require(inherited.is_file(), "FROZEN_ENTRY_INHERITED_VALIDATOR_MISSING")
    require(
        sha256_file(target) == EXPECTED_TARGET_SHA256,
        "FROZEN_ENTRY_MANAGEMENT_SOURCE_HASH_DRIFT",
    )
    require(
        sha256_file(test) == EXPECTED_TEST_SHA256,
        "FROZEN_ENTRY_MANAGEMENT_TEST_HASH_DRIFT",
    )

    target_tree = ast.parse(
        target.read_text(encoding="utf-8-sig"),
        filename=str(target),
    )
    test_text = test.read_text(encoding="utf-8-sig")
    test_tree = ast.parse(test_text, filename=str(test))

    require(
        literal_all(target_tree) == EXPECTED_PUBLIC_SYMBOLS,
        "FROZEN_ENTRY_MANAGEMENT_PUBLIC_SURFACE_DRIFT",
    )
    require(
        TARGET_MODULE in imported_modules(test_tree),
        "FROZEN_ENTRY_MANAGEMENT_DIRECT_TEST_IMPORT_MISSING",
    )
    missing_calls = REQUIRED_TEST_CALLS - called_names(test_tree)
    require(
        not missing_calls,
        "FROZEN_ENTRY_MANAGEMENT_PUBLIC_OPERATION_UNTESTED:"
        + ",".join(sorted(missing_calls)),
    )

    for token in (
        "TemporaryDirectory",
        "build_paths",
        "assertRaisesRegex",
        "freeze_index",
        "deleted_entries",
        "outside the canonical entries folder",
        "Active frozen entries cannot be deleted",
    ):
        require(
            token in test_text,
            "FROZEN_ENTRY_MANAGEMENT_TEST_BOUNDARY_MARKER_MISSING:" + token,
        )

    require(
        "unittest.mock" not in test_text and "mock.patch" not in test_text,
        "FROZEN_ENTRY_MANAGEMENT_OWNER_MOCKED",
    )
    require(
        len(test_text.splitlines()) <= 260,
        "FROZEN_ENTRY_MANAGEMENT_TEST_SIZE_CONTRACT_DRIFT",
    )
    require(
        len(Path(__file__).read_text(encoding="utf-8-sig").splitlines()) <= 360,
        "WAVE2K_VALIDATOR_SIZE_CONTRACT_DRIFT",
    )

    print("FROZEN ENTRY MANAGEMENT SOURCE UNCHANGED: PASS")
    print("FROZEN ENTRY MANAGEMENT DIRECT TEST IMPORT: PASS")
    print("FROZEN ENTRY MANAGEMENT PUBLIC OPERATIONS COVERED: PASS")
    print("FROZEN ENTRY MANAGEMENT REAL MUTATION BOUNDARY: PASS")
    print("FROZEN ENTRY MANAGEMENT PATH ESCAPE GUARD TESTED: PASS")
    print("FROZEN ENTRY MANAGEMENT OWNER MOCKING: ABSENT")
    print("WAVE2K PYTHON AND SIZE CONTRACT: PASS")


def run_command(
    root: Path,
    command: list[str],
    markers: tuple[str, ...],
    code: str,
    *,
    timeout: int = 1800,
    extra_environment: dict[str, str] | None = None,
) -> str:
    """Run one command and require its exit code and markers."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra_environment:
        environment.update(extra_environment)
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, code + "_NONZERO_EXIT")
    for marker in markers:
        require(marker in output, code + "_MARKER_MISSING:" + marker)
    return output


def validate_functional_test(root: Path) -> None:
    """Execute the new test against real temporary filesystem state."""
    run_command(
        root,
        [sys.executable, str(root / TEST_REL)],
        (
            "Ran 2 tests",
            "OK",
        ),
        "FROZEN_ENTRY_MANAGEMENT_FUNCTIONAL_TEST",
        timeout=120,
    )
    print("FROZEN ENTRY MANAGEMENT FUNCTIONAL TEST SUITE: PASS")


def validate_inherited_contract(root: Path) -> None:
    """Run inherited validation with bytecode outside the source tree."""
    with tempfile.TemporaryDirectory(
        prefix="kanda_wave2k_pycache_"
    ) as pycache_root:
        run_command(
            root,
            [
                sys.executable,
                str(root / INHERITED_VALIDATOR_REL),
                "--root",
                str(root),
                "--skip-real-qt",
            ],
            (
                "LIST_FROZEN_BACKEND_BEHAVIOR_PRESERVED: PASS",
                "LIST_FROZEN_DEPRECATED_STARTUP_EXCLUSION: PASS",
                "LIST_FROZEN_REVERSIBLE_DELETE_UNDELETE: PASS",
                "VALIDATION OK: freeze-list-frozen-manager-responsive-v1",
                "STATUS: IN_SYNC",
            ),
            "FROZEN_ENTRY_MANAGEMENT_INHERITED_VALIDATION",
            extra_environment={
                "PYTHONPYCACHEPREFIX": pycache_root,
            },
        )
    print("FROZEN ENTRY MANAGEMENT INHERITED BYTECODE REDIRECT: PASS")
    print("FROZEN ENTRY MANAGEMENT INHERITED BACKEND CONTRACT: PASS")


def validate_architecture(root: Path) -> None:
    """Require only the three Project Web AI test gaps to remain."""
    output = run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "kanda_reasoner_app"
                / "manage_architecture"
                / "manage_architecture.py"
            ),
            "--root",
            str(root),
            "--validate",
        ],
        ("ARCHITECTURE VALIDATION SUMMARY",),
        "ARCHITECTURE_VALIDATION",
    )
    require("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    require(
        "Total issues: 3 | Errors: 0 | Warnings: 3 | Other: 0" in output,
        "WAVE2K_ARCHITECTURE_COUNT_UNEXPECTED",
    )
    require(
        "TEST_PROTECTION_GAP: 3 (errors=0, warnings=3)" in output,
        "WAVE2K_TEST_GAP_COUNT_UNEXPECTED",
    )
    require(
        "MISPLACED_TEST" not in output,
        "WAVE2K_MISPLACED_TEST_WARNING_REMAINS",
    )
    require(
        "TEST_PROTECTION_GAP          " + TARGET_REL.as_posix() not in output,
        "WAVE2K_FROZEN_ENTRY_TEST_GAP_REMAINS",
    )
    for remaining in (
        "project_web_ai_apply_receipts.py",
        "project_web_ai_shadow.py",
        "project_web_ai_write_storage.py",
    ):
        require(
            remaining in output,
            "WAVE2K_EXPECTED_REMAINING_GAP_MISSING:" + remaining,
        )

    print("WAVE2K FROZEN ENTRY TEST PROTECTION GAP ABSENT: PASS")
    print("WAVE2K TEST LOCATION CANONICAL: PASS")
    print("WAVE2K REMAINING TEST GAPS ISOLATED TO PROJECT WEB AI: PASS")
    print("WAVE2K FREEZE MANAGEMENT TEST PROTECTION FAMILY CLOSED: PASS")


def main() -> int:
    """Run Wave 2K validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_static(root)
    validate_functional_test(root)
    validate_inherited_contract(root)
    if not args.static_only:
        validate_architecture(root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
