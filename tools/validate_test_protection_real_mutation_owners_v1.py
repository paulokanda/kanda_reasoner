"""Validate that test protection targets real mutation owners."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

__all__ = [
    "main",
]

FEATURE_ID = "test-protection-real-mutation-owners-v1"
EXPECTED_TEST_FILES = (
    "tests/test_project_mutation_and_journaled_transactions_v1.py",
    "tests/test_workbench_stage_and_state_boundaries_v1.py",
    "tests/test_analyzer_process_tree_boundary_v1.py",
    "tests/test_ruff_correction_mutation_boundary_v1.py",
)
VALIDATOR_PATH = "tools/validate_test_protection_real_mutation_owners_v1.py"
EXPECTED_PAYLOAD_FILES = (*EXPECTED_TEST_FILES, VALIDATOR_PATH)
BUNDLE_MANIFEST_PATH = (
    "workbench/_bundle_temp/"
    "BUNDLE_MANIFEST_test_protection_real_mutation_owners_v1.txt"
)
EXPECTED_ROOT_FILES = {
    "PACKAGE_MANIFEST.json",
    "KANDA_FREEZE_HINT.json",
    "INSTALL.ps1",
    "VALIDATE.ps1",
    "FREEZE.ps1",
    BUNDLE_MANIFEST_PATH,
}
TARGET_MODULES = {
    "kanda_reasoner_app.engineering_safety.project_mutation_lane",
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.analyzer_process_tree"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.main_workbench_stage_adapters"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.main_workbench_state_store"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.planner_bounded_refinement"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_completion_apply_bridge"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_journaled_apply_executor"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_refactor_transaction"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_source_mutation_primitives"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_stage_correction_service"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_transaction_rollback"
    ),
    (
        "kanda_reasoner_app.manage_architecture."
        "large_file_refactor_planner.workbench_transaction_store"
    ),
    "kanda_reasoner_app.source_hygiene.ruff_correction_apply",
    "kanda_reasoner_app.source_hygiene.ruff_correction_storage",
}
TARGET_PATHS = {
    module.replace(".", "/") + ".py" for module in TARGET_MODULES
}
HANDOFF_EXCLUSION_GAPS = {
    "kanda_reasoner_app/error_memory/store.py",
    (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "workbench_guarded_source_apply.py"
    ),
    (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "workbench_import_rewrite_rollback_executor.py"
    ),
    (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "workbench_rollback_executor.py"
    ),
    "kanda_reasoner_app/storage_policy/source_debris_quarantine_dry_run.py",
}
WARNING_PATTERN = re.compile(
    r"^WARNING\s+TEST_PROTECTION_GAP\s+(.+?)\s+::",
    re.MULTILINE,
)
ERROR_PATTERN = re.compile(r"^ERROR\s+", re.MULTILINE)
RAN_TESTS_PATTERN = re.compile(r"Ran\s+(\d+)\s+tests?")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_zip_name(name: str) -> bool:
    normalized = name.replace("\\", "/")
    parts = normalized.split("/")
    if not normalized or normalized.startswith("/"):
        return False
    if re.match(r"^[A-Za-z]:", normalized):
        return False
    return ".." not in parts


def _validate_zip_contract(patch_zip: Path) -> None:
    with zipfile.ZipFile(patch_zip) as archive:
        names = [name.replace("\\", "/") for name in archive.namelist()]
        _assert(all(_safe_zip_name(name) for name in names), "UNSAFE_ZIP_MEMBER")
        _assert(len(names) == len(set(names)), "DUPLICATE_ZIP_MEMBER")
        expected = EXPECTED_ROOT_FILES | {
            "payload/" + path for path in EXPECTED_PAYLOAD_FILES
        }
        _assert(set(names) == expected, "ZIP_MEMBER_SET_CHANGED")
        _assert(names.count("KANDA_FREEZE_HINT.json") == 1, "FREEZE_HINT_COUNT")
        _assert(
            not any(name.endswith("/KANDA_FREEZE_HINT.json") for name in names),
            "FREEZE_HINT_DUPLICATED_IN_PAYLOAD",
        )
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json"))
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "MANIFEST_FEATURE_ID")
        _assert(hint.get("feature_id") == FEATURE_ID, "HINT_FEATURE_ID")
        _assert(manifest.get("patch_name") == hint.get("patch_name"), "PATCH_IDENTITY")
        items = manifest.get("files")
        _assert(isinstance(items, list), "MANIFEST_FILES_NOT_LIST")
        by_path = {item.get("relative_path"): item for item in items}
        _assert(set(by_path) == set(EXPECTED_PAYLOAD_FILES), "MANIFEST_FILE_SET")
        for relative_path in EXPECTED_PAYLOAD_FILES:
            item = by_path[relative_path]
            data = archive.read("payload/" + relative_path)
            _assert(
                hashlib.sha256(data).hexdigest() == item.get("sha256"),
                "PAYLOAD_HASH_MISMATCH: " + relative_path,
            )
            _assert(item.get("new_file") is True, "NEW_FILE_FLAG: " + relative_path)
            _assert(
                item.get("accepted_existing_sha256") == [],
                "EXISTING_HASH_LIST: " + relative_path,
            )
        bundle_text = archive.read(BUNDLE_MANIFEST_PATH).decode("utf-8")
        _assert(FEATURE_ID in bundle_text, "BUNDLE_MANIFEST_FEATURE_ID")
    print("ZIP CONTRACT: PASS")


def _validate_source_files(project_root: Path) -> None:
    for relative_path in EXPECTED_PAYLOAD_FILES:
        path = project_root / relative_path
        _assert(path.is_file(), "INSTALLED_FILE_MISSING: " + relative_path)
        raw = path.read_bytes()
        _assert(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_BOM: " + relative_path)
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise AssertionError("NON_ASCII_SOURCE: " + relative_path) from exc
        ast.parse(text, filename=str(path))
        line_count = len(text.splitlines())
        _assert(line_count <= 500, "MODULE_OVER_500_LINES: " + relative_path)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")
    print("ASCII_SOURCE_ONLY: PASS")


def _direct_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    return imported


def _validate_direct_contract_imports(project_root: Path) -> None:
    imported: set[str] = set()
    for relative_path in EXPECTED_TEST_FILES:
        imported.update(_direct_imports(project_root / relative_path))
    missing = sorted(TARGET_MODULES - imported)
    _assert(not missing, "MISSING_DIRECT_IMPORTS: " + ", ".join(missing))
    print("DIRECT_PUBLIC_CONTRACT_IMPORTS: 14")


def _run_command(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd)
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        raise AssertionError("COMMAND_FAILED: " + " ".join(command))
    return result


def _run_real_boundary_tests(project_root: Path) -> None:
    total = 0
    for relative_path in EXPECTED_TEST_FILES:
        result = _run_command(
            [sys.executable, str(project_root / relative_path), "-v"],
            cwd=project_root,
            timeout=120,
        )
        match = RAN_TESTS_PATTERN.search(result.stdout)
        _assert(match is not None, "TEST_COUNT_NOT_FOUND: " + relative_path)
        total += int(match.group(1))
    _assert(total == 14, "REAL_TEST_COUNT_CHANGED: " + str(total))
    print("REAL_MUTATION_BOUNDARY_TESTS: 14")


def _run_architecture_validation(
    project_root: Path,
    *,
    require_zero_total_gaps: bool,
) -> None:
    script = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "manage_architecture.py"
    )
    result = _run_command(
        [sys.executable, str(script), "--root", str(project_root), "--validate"],
        cwd=project_root,
        timeout=300,
    )
    output = result.stdout
    warning_paths = set(WARNING_PATTERN.findall(output))
    target_remaining = sorted(TARGET_PATHS & warning_paths)
    _assert(
        not target_remaining,
        "TARGET_GAPS_REMAIN: " + ", ".join(target_remaining),
    )
    _assert(
        "Additional test-protection gaps suppressed after 80 findings" not in output,
        "SUPPRESSION_SUMMARY_REAPPEARED",
    )
    if require_zero_total_gaps:
        _assert(
            not warning_paths,
            "UNEXPECTED_LOCAL_TEST_GAPS: " + ", ".join(sorted(warning_paths)),
        )
    else:
        unexpected = warning_paths - HANDOFF_EXCLUSION_GAPS
        _assert(
            not unexpected,
            "UNEXPECTED_HANDOFF_TEST_GAPS: " + ", ".join(sorted(unexpected)),
        )
    error_count = len(ERROR_PATTERN.findall(output))
    _assert(error_count == 0, "ARCHITECTURE_ERRORS: " + str(error_count))
    print("TARGET_TEST_PROTECTION_GAPS: 0")
    print("TOTAL_TEST_PROTECTION_GAPS: " + str(len(warning_paths)))
    print("TEST_PROTECTION_GAP_SUPPRESSION_SUMMARY: ABSENT")
    print("ARCHITECTURE_ERROR_COUNT: 0")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--require-zero-total-test-gaps", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    _assert(project_root.is_dir(), "PROJECT_ROOT_MISSING")
    _assert(patch_zip.is_file(), "PATCH_ZIP_MISSING")
    _validate_zip_contract(patch_zip)
    _validate_source_files(project_root)
    _validate_direct_contract_imports(project_root)
    _run_real_boundary_tests(project_root)
    _run_architecture_validation(
        project_root,
        require_zero_total_gaps=args.require_zero_total_test_gaps,
    )
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION ERROR: " + str(exc))
        raise
