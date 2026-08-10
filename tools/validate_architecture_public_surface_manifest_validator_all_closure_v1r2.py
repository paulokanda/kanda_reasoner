# project-path: tools/validate_architecture_public_surface_manifest_validator_all_closure_v1r2.py
"""Validate helper-manifest alignment and explicit validator CLI surfaces."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

__all__ = ["main"]

FEATURE_ID = "architecture-public-surface-manifest-validator-all-closure-v1r2"

MANIFEST_REL = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help.json"
)
EXTENDED_HELPER_REL = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_warning_policy_extended_private_impl.py"
)

VALIDATOR_RELS = (
    Path("tools/validate_manage_architecture_warning_policy_brick_wall_split_v1.py"),
    Path("tools/validate_project_intelligence_symbol_indexer_cohesive_split_v1.py"),
    Path(
        "tools/validate_prompt_audit_wave10a_final_productization_"
        "generalized_canons_closure_v1.py"
    ),
    Path(
        "tools/validate_prompt_audit_wave9a_python_specialist_"
        "stack_reconciliation_v1.py"
    ),
)

SELF_REL = Path(
    "tools/validate_architecture_public_surface_manifest_validator_all_closure_v1r2.py"
)

EXPECTED_HASHES = {
    MANIFEST_REL.as_posix(): (
        "0b8fb74c176120c74e6de3ce7fbfde2201392fc40edd8801ab62c97b5ec980cb"
    ),
    VALIDATOR_RELS[0].as_posix(): (
        "58d51b4deb2804e7b2fba635f10728e45fb8f7231f274b4ad1347e148c259178"
    ),
    VALIDATOR_RELS[1].as_posix(): (
        "b8731b2b41a9c48e93f5e77ab52bf2fffc4e9a08e94a2d7fd8e87b33b1a6ee7d"
    ),
    VALIDATOR_RELS[2].as_posix(): (
        "1e133ecacb220817b3f55b2ae7155cec56d0fd67351795d9b332ffc4069abff8"
    ),
    VALIDATOR_RELS[3].as_posix(): (
        "69d73d64c81dec549a770592aeab1633314b3f8e08f97d9e65711f108c0db5b0"
    ),
}

EXPECTED_NON_ALL_SOURCE_HASHES = {
    VALIDATOR_RELS[0].as_posix(): (
        "09d9be5b1079dd818b0a3a3afe8a120238746d5dbeb2afd8304db0145e8fe809"
    ),
    VALIDATOR_RELS[1].as_posix(): (
        "be77e1204a2ebf2ac1ee100193cdd1db6ca07a4a8fd252d58ad64caf444ad187"
    ),
    VALIDATOR_RELS[2].as_posix(): (
        "d5a8dd7131e7eac35698c9b38fce3750a761a259b100b8c5f0d2962fe38ea568"
    ),
    VALIDATOR_RELS[3].as_posix(): (
        "212cf38731c0be2d30c30a96303b0d705e9f6cb249002a1223ba4a921ca5bb49"
    ),
}

TARGET_WARNING_FRAGMENTS = (
    "HELPER_MANIFEST_CONTRACT     " + MANIFEST_REL.as_posix(),
    "MISSING_PUBLIC_SURFACE_CONTROL " + VALIDATOR_RELS[0].as_posix(),
    "MISSING_PUBLIC_SURFACE_CONTROL " + VALIDATOR_RELS[1].as_posix(),
    "MISSING_PUBLIC_SURFACE_CONTROL " + VALIDATOR_RELS[2].as_posix(),
    "MISSING_PUBLIC_SURFACE_CONTROL " + VALIDATOR_RELS[3].as_posix(),
)


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def top_level_all(tree: ast.Module) -> tuple[str, ...] | None:
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (TypeError, ValueError, SyntaxError) as exc:
            fail("INVALID_TOP_LEVEL_ALL: " + repr(exc))
        if not isinstance(value, (list, tuple)):
            fail("TOP_LEVEL_ALL_NOT_SEQUENCE")
        return tuple(str(item) for item in value)
    return None


def source_hash_without_canonical_all(source: str) -> str:
    marker = '\n__all__ = ["main"]\n\n'
    if source.count(marker) != 1:
        fail("CANONICAL_MAIN_ALL_BLOCK_COUNT: " + str(source.count(marker)))
    predecessor_source = source.replace(marker, "", 1)
    return hashlib.sha256(predecessor_source.encode("utf-8")).hexdigest()


def validate_source_identity(root: Path) -> None:
    for relative_text, expected in EXPECTED_HASHES.items():
        actual = sha256_file(root / relative_text)
        if actual != expected:
            fail("SOURCE_IDENTITY_DRIFT: " + relative_text + ":" + actual)
    print("SOURCE_IDENTITY_GUARD: PASS")


def validate_manifest_alignment(root: Path) -> None:
    manifest = json.loads(read_text(root / MANIFEST_REL))
    helpers = manifest.get("helpers")
    if not isinstance(helpers, list):
        fail("HELPER_MANIFEST_HELPERS_NOT_LIST")
    target_module = (
        "kanda_reasoner_app.manage_architecture.manage_architecture_help."
        "source_loader_warning_policy_extended_private_impl"
    )
    target_path = (
        "manage_architecture_help/"
        "source_loader_warning_policy_extended_private_impl.py"
    )
    expected_export = "apply_manage_architecture_extended_warning_policies"
    matches = [
        item
        for item in helpers
        if isinstance(item, dict)
        and item.get("module") == target_module
        and item.get("path") == target_path
    ]
    if len(matches) != 1:
        fail("EXTENDED_WARNING_POLICY_MANIFEST_ENTRY_COUNT: " + str(len(matches)))
    if matches[0].get("exports") != [expected_export]:
        fail("EXTENDED_WARNING_POLICY_MANIFEST_EXPORT_DRIFT")
    helper_tree = ast.parse(read_text(root / EXTENDED_HELPER_REL))
    helper_all = top_level_all(helper_tree)
    if helper_all != (expected_export,):
        fail("EXTENDED_WARNING_POLICY_HELPER_ALL_DRIFT: " + repr(helper_all))
    print("HELPER_MANIFEST_EXTENDED_WARNING_POLICY_ALIGNMENT: PASS")
    print("HELPER_MANIFEST_CONTRACT_WARNING_RESOLVED: PASS")


def validate_validator_surfaces(root: Path) -> None:
    for relative in VALIDATOR_RELS:
        source = read_text(root / relative)
        tree = ast.parse(source, filename=str(root / relative))
        declared = top_level_all(tree)
        if declared != ("main",):
            fail("VALIDATOR_CANONICAL_ALL_DRIFT: " + relative.as_posix() + ":" + repr(declared))
        functions = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if "main" not in functions:
            fail("VALIDATOR_MAIN_MISSING: " + relative.as_posix())
        source_hash = source_hash_without_canonical_all(source)
        expected = EXPECTED_NON_ALL_SOURCE_HASHES[relative.as_posix()]
        if source_hash != expected:
            fail(
                "VALIDATOR_NON_ALL_SOURCE_DRIFT: "
                + relative.as_posix()
                + ":"
                + source_hash
            )
    print("VALIDATOR_MAIN_ONLY_PUBLIC_SURFACES: PASS")
    print("VALIDATOR_NON_ALL_SOURCE_IDENTITY: PASS")
    print("MISSING_PUBLIC_SURFACE_CONTROL_WARNINGS_RESOLVED: PASS")


def run_command(root: Path, relative: Path, extra: list[str], label: str) -> None:
    result = subprocess.run(
        [sys.executable, str(root / relative), *extra],
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
        fail(label + "_EXIT: " + str(result.returncode))
    if "STATUS: IN_SYNC" not in output:
        fail(label + "_STATUS_MARKER_MISSING")
    print(label + ": PASS")


def validate_inherited_validators(root: Path) -> None:
    run_command(
        root,
        VALIDATOR_RELS[0],
        ["--project-root", str(root)],
        "WARNING_POLICY_BRICK_WALL_VALIDATOR_REGRESSION",
    )
    run_command(
        root,
        VALIDATOR_RELS[1],
        ["--project-root", str(root)],
        "SYMBOL_INDEXER_VALIDATOR_REGRESSION",
    )
    run_command(
        root,
        VALIDATOR_RELS[2],
        ["--project-root", str(root)],
        "PROMPT_AUDIT_WAVE10A_VALIDATOR_REGRESSION",
    )
    run_command(
        root,
        VALIDATOR_RELS[3],
        ["--project-root", str(root)],
        "PROMPT_AUDIT_WAVE9A_VALIDATOR_REGRESSION",
    )


def validate_full_architecture_scan(root: Path) -> None:
    scanner = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    result = subprocess.run(
        [sys.executable, str(scanner), "--root", str(root), "--validate"],
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
    for fragment in TARGET_WARNING_FRAGMENTS:
        if fragment in output:
            fail("TARGET_WARNING_REMAINS: " + fragment)
    print("FULL_PROJECT_ARCHITECTURE_SCAN_ERRORS_ZERO: PASS")
    print("TARGET_PUBLIC_SURFACE_WARNING_SET_ABSENT: PASS")


def validate_self_surface(root: Path) -> None:
    source = read_text(root / SELF_REL)
    tree = ast.parse(source)
    if top_level_all(tree) != ("main",):
        fail("FOCUSED_VALIDATOR_ALL_DRIFT")
    count = len(source.splitlines())
    if not 101 <= count <= 499:
        fail("FOCUSED_VALIDATOR_LINE_LAW: " + str(count))
    print("FOCUSED_VALIDATOR_PUBLIC_SURFACE: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--full-project-scan", action="store_true")
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()

    validate_source_identity(root)
    validate_manifest_alignment(root)
    validate_validator_surfaces(root)
    validate_self_surface(root)
    validate_inherited_validators(root)
    if args.full_project_scan:
        validate_full_architecture_scan(root)

    print("ARCHITECTURE_PUBLIC_SURFACE_MANIFEST_VALIDATOR_ALL_CLOSURE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
