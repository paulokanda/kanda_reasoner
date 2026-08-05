# project-path: tools/validate_manage_architecture_warning_policy_brick_wall_split_v1.py
"""Validate the Brick-Wall-preserving warning-policy module split."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
from pathlib import Path
import subprocess
import sys
from typing import Any

__all__ = ["main"]


FEATURE_ID = "manage-architecture-warning-policy-brick-wall-preserving-split-v1"

FACADE_REL = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_warning_policy_private_impl.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_warning_policy_extended_private_impl.py"
)
SOURCE_LOADER_REL = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_private_impl.py"
)
SELF_REL = Path(
    "tools/validate_manage_architecture_warning_policy_brick_wall_split_v1.py"
)

EXPECTED_SOURCE_HASHES = {
    FACADE_REL.as_posix(): (
        "319d62e0b32eddf622ead24b000d841365d5032a8e115f6d1e3c089353620d3f"
    ),
    HELPER_REL.as_posix(): (
        "06f5ff41d867a15bc7f56942bfc72b055729f3255d5cccdf135ec00458a48349"
    ),
}
EXPECTED_SOURCE_LOADER_HASH = (
    "fe476ac1bf74c7898a24adf85b680b55450a18f9c2316a87230c1004b35bb7d2"
)
EXPECTED_RECONSTRUCTED_SOURCE_HASH = (
    "b7f905d345979cb8c36edeb75ec41c07052834925a0a4d3d5112505ce07ce139"
)
EXPECTED_RECONSTRUCTED_LINES = 7268
EXPECTED_RECONSTRUCTED_BYTES = 265565

FACADE_POLICY_ORDER = (
    "_apply_canonical_test_protection_alias_policy",
    "_apply_test_protection_generated_private_policy",
    "_apply_stale_variant_compatibility_shim_policy",
    "_apply_generated_artifact_bundle_temp_manifest_policy",
    "_apply_generated_prompt_delivery_manifest_location_policy",
    "_apply_test_contract_cleanup_policy",
    "apply_manage_architecture_extended_warning_policies",
    "_apply_governed_validation_artifact_policy",
)

HELPER_POLICY_ORDER = (
    "_apply_governed_validator_classification_policy",
    "_apply_boundary_error_contract_marker_policy",
    "_apply_stale_variant_active_domain_terms_policy",
    "_apply_generated_prompt_delivery_duplicate_owner_policy",
    "_apply_mixed_responsibility_boundary_policy",
    "_apply_import_heaviness_gui_boundary_policy",
    "_apply_side_effect_governed_validation_policy",
)

BRICK_WALL_SOURCE_MARKERS = (
    "def detect_side_effect_on_import_issues(",
    "def detect_mixed_responsibility_file_issues(",
    "def detect_stale_variant_issues(",
    "def detect_deprecated_variant_reference_issues(",
    "def detect_test_protection_gap_issues(",
    "MODULE_TOO_LARGE",
    "TEST_PROTECTION_GAP",
    "STALE_VARIANT_SOURCE_OF_TRUTH",
    "MIXED_RESPONSIBILITY_FILE",
)


def fail(message: str) -> None:
    """Raise one deterministic validation failure."""
    raise AssertionError(message)


def sha256_file(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def read_text(root: Path, relative: Path) -> str:
    """Read one required UTF-8 source file."""
    path = root / relative
    if not path.is_file():
        fail("MISSING_REQUIRED_FILE: " + relative.as_posix())
    return path.read_text(encoding="utf-8-sig", errors="strict")


def function_node(tree: ast.Module, name: str) -> ast.FunctionDef:
    """Return one required top-level function."""
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(matches) != 1:
        fail("FUNCTION_COUNT_CHANGED: " + name + ":" + str(len(matches)))
    return matches[0]


def call_name(node: ast.AST) -> str:
    """Return the terminal name for one call expression."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def assigned_call_order(function: ast.FunctionDef) -> tuple[str, ...]:
    """Return the governed source-transform calls in execution order."""
    names: list[str] = []
    for statement in function.body:
        call: ast.Call | None = None
        if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Call):
            call = statement.value
        if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Call):
            call = statement.value
        if call is not None:
            names.append(call_name(call.func))
    return tuple(names)


def validate_source_identity(root: Path) -> None:
    """Require exact reviewed split bytes and unchanged source loader."""
    for relative_text, expected in EXPECTED_SOURCE_HASHES.items():
        relative = Path(relative_text)
        actual = sha256_file(root / relative)
        if actual != expected:
            fail(
                "SOURCE_IDENTITY_DRIFT: "
                + relative_text
                + ":"
                + actual
            )
    loader_hash = sha256_file(root / SOURCE_LOADER_REL)
    if loader_hash != EXPECTED_SOURCE_LOADER_HASH:
        fail("SOURCE_LOADER_OWNER_DRIFT: " + loader_hash)
    print("SOURCE_IDENTITY_GUARD: PASS")
    print("SOURCE_LOADER_OWNER_UNCHANGED: PASS")


def validate_line_law(root: Path) -> None:
    """Require all touched permanent Python files to remain 101-499 lines."""
    counts: dict[str, int] = {}
    for relative in (FACADE_REL, HELPER_REL, SELF_REL):
        text = read_text(root, relative)
        count = len(text.splitlines())
        counts[relative.as_posix()] = count
        if not 101 <= count <= 499:
            fail(
                "LINE_LAW_101_499_VIOLATION: "
                + relative.as_posix()
                + ":"
                + str(count)
            )
        if any(ord(character) > 127 for character in text):
            fail("NON_ASCII_SOURCE: " + relative.as_posix())
        ast.parse(text, filename=str(root / relative))
    if counts[FACADE_REL.as_posix()] >= 500:
        fail("MODULE_TOO_LARGE_REMAINS: " + repr(counts))
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("MODULE_TOO_LARGE_WARNING_POLICY_RESOLVED: PASS")


def validate_structure(root: Path) -> None:
    """Validate facade ownership, call order, and one-way dependency flow."""
    facade_text = read_text(root, FACADE_REL)
    helper_text = read_text(root, HELPER_REL)
    loader_text = read_text(root, SOURCE_LOADER_REL)
    facade_tree = ast.parse(facade_text, filename=str(root / FACADE_REL))
    helper_tree = ast.parse(helper_text, filename=str(root / HELPER_REL))

    facade_imports = [
        node
        for node in facade_tree.body
        if isinstance(node, ast.ImportFrom)
        and node.module == "source_loader_warning_policy_extended_private_impl"
    ]
    if len(facade_imports) != 1:
        fail("EXTENDED_HELPER_IMPORT_COUNT_CHANGED")
    imported_names = {
        alias.name
        for alias in facade_imports[0].names
    }
    if imported_names != {"apply_manage_architecture_extended_warning_policies"}:
        fail("EXTENDED_HELPER_IMPORT_SURFACE_DRIFT: " + repr(imported_names))

    helper_import_modules = {
        str(node.module or "")
        for node in helper_tree.body
        if isinstance(node, ast.ImportFrom)
    }
    forbidden_imports = {
        "source_loader_warning_policy_private_impl",
        "source_loader_private_impl",
        "manage_architecture",
    }
    if helper_import_modules.intersection(forbidden_imports):
        fail(
            "HELPER_TO_OWNER_BACK_REFERENCE: "
            + repr(sorted(helper_import_modules.intersection(forbidden_imports)))
        )

    facade_apply = function_node(
        facade_tree,
        "apply_manage_architecture_warning_policies",
    )
    helper_apply = function_node(
        helper_tree,
        "apply_manage_architecture_extended_warning_policies",
    )
    if assigned_call_order(facade_apply) != FACADE_POLICY_ORDER:
        fail(
            "FACADE_POLICY_ORDER_DRIFT: "
            + repr(assigned_call_order(facade_apply))
        )
    if assigned_call_order(helper_apply) != HELPER_POLICY_ORDER:
        fail(
            "HELPER_POLICY_ORDER_DRIFT: "
            + repr(assigned_call_order(helper_apply))
        )

    if "apply_manage_architecture_warning_policies" not in loader_text:
        fail("SOURCE_LOADER_DELEGATION_MISSING")
    if "source_loader_warning_policy_extended_private_impl" in loader_text:
        fail("SOURCE_LOADER_BYPASSES_FACADE")

    facade_all = [
        node
        for node in facade_tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        )
    ]
    helper_all = [
        node
        for node in helper_tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        )
    ]
    if len(facade_all) != 1 or len(helper_all) != 1:
        fail("PUBLIC_CONTRACT_ASSIGNMENT_COUNT_CHANGED")

    print("PUBLIC_FACADE_PRESERVATION: PASS")
    print("POLICY_EXECUTION_ORDER_PRESERVED: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("NO_HELPER_TO_FACADE_BACK_REFERENCE: PASS")


def validate_reconstructed_source(root: Path) -> None:
    """Require the complete generated architecture source to be byte-identical."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    importlib.invalidate_caches()
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture_help."
        "source_loader_private_impl"
    )
    source = module.load_manage_architecture_source()
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if digest != EXPECTED_RECONSTRUCTED_SOURCE_HASH:
        fail("RECONSTRUCTED_ARCHITECTURE_SOURCE_DRIFT: " + digest)
    if len(source.splitlines()) != EXPECTED_RECONSTRUCTED_LINES:
        fail(
            "RECONSTRUCTED_SOURCE_LINE_COUNT_DRIFT: "
            + str(len(source.splitlines()))
        )
    if len(source.encode("utf-8")) != EXPECTED_RECONSTRUCTED_BYTES:
        fail(
            "RECONSTRUCTED_SOURCE_BYTE_COUNT_DRIFT: "
            + str(len(source.encode("utf-8")))
        )
    for marker in BRICK_WALL_SOURCE_MARKERS:
        if marker not in source:
            fail("BRICK_WALL_SOURCE_MARKER_MISSING: " + marker)
    print("RECONSTRUCTED_ARCHITECTURE_SOURCE_BYTE_IDENTITY: PASS")
    print("BRICK_WALL_WARNING_LOGIC_IDENTITY: PASS")


def run_validator(
    root: Path,
    relative: Path,
    arguments: list[str],
    required_markers: tuple[str, ...],
    label: str,
) -> None:
    """Run one inherited validator and require its deterministic markers."""
    path = root / relative
    if not path.is_file():
        fail("INHERITED_VALIDATOR_MISSING: " + relative.as_posix())
    result = subprocess.run(
        [sys.executable, str(path), *arguments],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if output:
        print(output.rstrip())
    if result.returncode != 0:
        fail(label + "_EXIT_CODE: " + str(result.returncode))
    for marker in required_markers:
        if marker not in output:
            fail(label + "_MARKER_MISSING: " + marker)


def validate_inherited_regressions(root: Path) -> None:
    """Run the two directly affected historical warning-policy contracts."""
    run_validator(
        root,
        Path("tools/validate_cleanup_batch_11_test_internal_contract_policy_v1.py"),
        ["--project-root", str(root)],
        (
            "VALIDATION OK: cleanup-batch-11-test-internal-contract-policy-v1",
            "STATUS: IN_SYNC",
        ),
        "CLEANUP_BATCH11",
    )
    print("CLEANUP_BATCH11_WARNING_POLICY_REGRESSION: PASS")

    run_validator(
        root,
        Path(
            "tools/validate_stale_variant_governed_validation_artifact_policy_v1.py"
        ),
        ["--project-root", str(root)],
        (
            "GOVERNED_VALIDATION_ARTIFACT_EXCLUSION: PASS",
            "NON_GOVERNED_STALE_VARIANT_RETENTION: PASS",
            "DEPRECATED_REFERENCE_ACTIVE_OWNER_SCOPE: PASS",
            "VALIDATION OK: stale-variant-governed-validation-artifact-policy-v1",
            "STATUS: IN_SYNC",
        ),
        "STALE_VARIANT_GOVERNED_ARTIFACT",
    )
    print("STALE_VARIANT_WARNING_POLICY_REGRESSION: PASS")


def validate_fresh_architecture_scan(root: Path) -> None:
    """Scan the touched family with the current architecture engine."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    top_names = architecture.project_top_level_names(root)
    for relative in (FACADE_REL, HELPER_REL):
        module, warnings = architecture.scan_module(
            root,
            root / relative,
            top_names,
        )
        if module.line_count >= 500:
            fail(
                "FRESH_MODULE_LINE_COUNT_OVER_LIMIT: "
                + relative.as_posix()
                + ":"
                + str(module.line_count)
            )
        for warning in warnings:
            if warning.code == "MODULE_TOO_LARGE":
                fail(
                    "FRESH_MODULE_TOO_LARGE_WARNING_REMAINS: "
                    + relative.as_posix()
                )
    print("FRESH_WARNING_POLICY_FAMILY_SIZE_SCAN: PASS")


def validate_full_project_architecture_scan(root: Path) -> None:
    """Run the complete project architecture validation when requested."""
    validator = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    result = subprocess.run(
        [sys.executable, str(validator), "--root", str(root), "--validate"],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if result.returncode != 0:
        if output:
            print(output.rstrip())
        fail("FULL_ARCHITECTURE_SCAN_EXIT: " + str(result.returncode))
    if "Errors: 0" not in output:
        fail("FULL_ARCHITECTURE_SCAN_ERRORS_NOT_ZERO")
    forbidden = (
        "MODULE_TOO_LARGE             " + FACADE_REL.as_posix(),
        "MODULE_TOO_LARGE             " + HELPER_REL.as_posix(),
    )
    for marker in forbidden:
        if marker in output:
            fail("FULL_MODULE_TOO_LARGE_REMAINS: " + marker)
    print("FULL_PROJECT_ARCHITECTURE_SCAN_ERRORS_ZERO: PASS")


def validate_ast_family(root: Path) -> None:
    """Require fresh SAFE AST audit results for both runtime modules."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative in (FACADE_REL, HELPER_REL):
        result = run_large_module_split_audit(
            root,
            root / relative,
            classifier_mode="heuristic",
        )
        classification: dict[str, Any] = result.data[
            "refactor_safety_classification"
        ]
        if classification.get("label") != "SAFE REFACTORING":
            fail(
                "AST_SPLIT_NOT_SAFE: "
                + relative.as_posix()
                + ":"
                + repr(classification)
            )
        if classification.get("hard_blockers"):
            fail(
                "AST_SPLIT_HARD_BLOCKERS: "
                + relative.as_posix()
                + ":"
                + repr(classification.get("hard_blockers"))
            )
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def main() -> int:
    """Run all focused Brick-Wall-preserving split checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--full-project-scan", action="store_true")
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()

    validate_source_identity(root)
    validate_line_law(root)
    validate_structure(root)
    validate_reconstructed_source(root)
    validate_inherited_regressions(root)
    validate_fresh_architecture_scan(root)
    if args.full_project_scan:
        validate_full_project_architecture_scan(root)
    validate_ast_family(root)

    print("WARNING_POLICY_BRICK_WALL_PRESERVING_SPLIT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
