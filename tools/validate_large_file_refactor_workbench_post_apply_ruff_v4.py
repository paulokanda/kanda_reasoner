# project-path: tools/validate_large_file_refactor_workbench_post_apply_ruff_v4.py
"""Focused validation for Workbench touched-file post-apply Ruff checks."""

from __future__ import annotations

import argparse
import hashlib
from importlib import import_module
import json
from pathlib import Path
import py_compile
import sys
import zipfile

from validate_large_file_refactor_workbench_post_apply_ruff_v4_support import (
    validate_runtime,
)

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

_PACKAGE_PREFIX = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner."
_MODELS = import_module(_PACKAGE_PREFIX + "models")
_GUARDED = import_module(_PACKAGE_PREFIX + "workbench_guarded_source_apply")
_PAYLOAD = import_module(_PACKAGE_PREFIX + "workbench_source_payload_builder")
_POST_APPLY = import_module(_PACKAGE_PREFIX + "workbench_post_apply_validator")
_POST_APPLY_RUFF = import_module(
    _PACKAGE_PREFIX + "workbench_post_apply_ruff_validation"
)

SCHEMA_VERSION = _MODELS.SCHEMA_VERSION
GUARDED_SOURCE_APPLY_FEATURE_ID = _GUARDED.GUARDED_SOURCE_APPLY_FEATURE_ID
GuardedSourceApplyResult = _GUARDED.GuardedSourceApplyResult
SOURCE_PAYLOAD_READINESS_FEATURE_ID = _PAYLOAD.SOURCE_PAYLOAD_READINESS_FEATURE_ID
SourceApplyPayloadFile = _PAYLOAD.SourceApplyPayloadFile
SourceApplyPayloadReadinessResult = _PAYLOAD.SourceApplyPayloadReadinessResult
PostApplyValidationResult = _POST_APPLY.PostApplyValidationResult
WorkbenchPostApplyValidationResult = _POST_APPLY.WorkbenchPostApplyValidationResult
validate_and_write_post_apply = _POST_APPLY.validate_and_write_post_apply
validate_and_write_post_apply_ruff = _POST_APPLY_RUFF.validate_and_write_post_apply_ruff

FEATURE_ID = "architecture-review-workbench-post-apply-ruff-v4"
EXPECTED_PATCH_MEMBERS = {
    "KANDA_FREEZE_HINT.json",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_ruff_validation.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
    "tools/validate_large_file_refactor_workbench_post_apply_ruff_v4.py",
    "tools/validate_large_file_refactor_workbench_post_apply_ruff_v4_support.py",
}
TOUCHED = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_ruff_validation.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
    "tools/validate_large_file_refactor_workbench_post_apply_ruff_v4.py",
    "tools/validate_large_file_refactor_workbench_post_apply_ruff_v4_support.py",
)
FROZEN_SOURCE_HYGIENE = dict(
    (
        (
            "ruff.toml",
            "52172a11111cedc04a0942130358ecb65ffa34ee98be833ef6c50cbc01bc0746",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py",
            "6ecde4874c74888fd19314cf12eeda9556469db97ba0fc1ae818323e15533fcf",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_correction_apply.py",
            "8c5555a39d7ebce82d5a2871d13c3a5c14b6b75e6fd04996f381b57728102d79",
        ),
    )
)
PREDECESSOR_POST_APPLY_SHA256 = (
    "fad796f6bb60bcda4e0b64d21eed352c3f3a0162b1f98152ad27207b3ca87f7f"
)

FROZEN_PATCH5_OWNERS = {
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_completion_apply_bridge.py": (
        "fe50a11719380b0b9404a950bdc23d1e7ec355e6e834637d7db670d6e4e5455a"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_journaled_apply_executor.py": (
        "39d3306764e276f96b443371b19c5eec4db5f6bd405404d26870813f1c311a06"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_transaction_rollback.py": (
        "056dd7e2e0cb720b5db003d080e4ee2f8216375941a5cd94dabd7b7f67778897"
    ),
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_refactor_receipt.py": (
        "8aa19b143498b44b1b90ab1f078cedfae634b127eb6a8269b31bf7787496504c"
    ),
}


def main() -> int:
    """Run all focused validation gates."""
    args = _parse_args()
    root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    ruff = Path(args.ruff_executable).resolve()

    _validate_patch_members(patch_zip)
    print("PATCH_MEMBER_SCOPE_GOVERNED_POST_APPLY_EXTENSION: PASS")
    _validate_freeze_hint(patch_zip)
    print("FREEZE_HINT_CONTRACT: PASS")
    _validate_frozen_source_hygiene(root)
    print("FROZEN_PHASE2_PHASE3_SOURCE_HYGIENE_IDENTITY: PASS")
    _validate_source_extension(root)
    print("FROZEN_WORKBENCH_PUBLIC_CONTRACT_PRESERVED: PASS")
    _validate_patch5_owners(root)
    print("PATCH5_TRANSACTION_OWNERS_UNCHANGED: PASS")
    _validate_compile_and_size(root)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")
    _validate_ascii(root)
    print("ASCII_PYTHON_SOURCE: PASS")
    validate_runtime(root, ruff)
    print("POST_APPLY_RUFF_EXACT_VERSION: PASS")
    print("POST_APPLY_RUFF_VERSION_MISMATCH_BLOCKS: PASS")
    print("POST_APPLY_RUFF_TOUCHED_FILES_ONLY: PASS")
    print("POST_APPLY_RUFF_READ_ONLY: PASS")
    print("POST_APPLY_RUFF_EVIDENCE_ROOT_SHIELDED: PASS")
    print("POST_APPLY_RUFF_NO_PROJECT_CACHE: PASS")
    print("POST_APPLY_RUFF_LINT_BLOCKS: PASS")
    print("POST_APPLY_RUFF_FORMAT_BLOCKS: PASS")
    print("POST_APPLY_RUFF_OPTIONAL_POLICY_COMPATIBILITY: PASS")
    print("POST_APPLY_RUFF_EXECUTION_EVIDENCE_ACCURATE: PASS")
    print("WORKBENCH_POST_APPLY_INTEGRATION: PASS")
    print("ROLLBACK_MANIFEST_REMAINS_AVAILABLE_AFTER_RUFF_BLOCK: PASS")
    _run_ruff_on_touched(root, ruff)
    print("TOUCHED_MODULE_RUFF_LINT: PASS")
    print("TOUCHED_MODULE_RUFF_FORMAT_CHECK: PASS")
    print("PATCH_ZIP_CONTRACT: PASS")
    print("ZIP CONTRACT: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", required=True)
    return parser.parse_args()


def _validate_patch_members(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        names = set(archive.namelist())
    if names != EXPECTED_PATCH_MEMBERS:
        raise AssertionError("PATCH_MEMBER_SCOPE_CHANGED:" + "|".join(sorted(names)))


def _validate_freeze_hint(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        payload = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
    if payload.get("feature_id") != FEATURE_ID:
        raise AssertionError("FREEZE_HINT_FEATURE_ID_MISMATCH")
    if payload.get("root_freeze_hint") is not True:
        raise AssertionError("FREEZE_HINT_ROOT_FLAG_MISSING")


def _validate_frozen_source_hygiene(root: Path) -> None:
    for relative, expected in FROZEN_SOURCE_HYGIENE.items():
        if _sha256(root / relative) != expected:
            raise AssertionError("FROZEN_SOURCE_HYGIENE_CHANGED:" + relative)


def _validate_source_extension(root: Path) -> None:
    path = root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "workbench_post_apply_validator.py"
    )
    text = path.read_text(encoding="utf-8")
    if PREDECESSOR_POST_APPLY_SHA256 == _sha256(path):
        raise AssertionError("POST_APPLY_EXTENSION_NOT_INSTALLED")
    required = (
        "WorkbenchPostApplyValidationResult = PostApplyValidationResult",
        "validate_and_write_post_apply_ruff(",
        'status = "post_apply_validated" if not blockers else "blocked"',
    )
    for marker in required:
        if marker not in text:
            raise AssertionError("POST_APPLY_PUBLIC_CONTRACT_MISSING:" + marker)
    if PostApplyValidationResult is not WorkbenchPostApplyValidationResult:
        raise AssertionError("POST_APPLY_COMPATIBILITY_ALIAS_CHANGED")


def _validate_patch5_owners(root: Path) -> None:
    """Prove transaction, rollback, and receipt owners remain byte-identical."""
    for relative, expected in FROZEN_PATCH5_OWNERS.items():
        if _sha256(root / relative) != expected:
            raise AssertionError("PATCH5_TRANSACTION_OWNER_CHANGED:" + relative)


def _validate_compile_and_size(root: Path) -> None:
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count >= 500:
            raise AssertionError(f"MODULE_TOO_LARGE:{relative}:{line_count}")


def _validate_ascii(root: Path) -> None:
    for relative in TOUCHED:
        data = (root / relative).read_bytes()
        try:
            data.decode("ascii")
        except UnicodeDecodeError as exc:
            raise AssertionError("NON_ASCII_SOURCE:" + relative) from exc


def _run_ruff_on_touched(root: Path, ruff: Path) -> None:
    paths = [str(root / relative) for relative in TOUCHED]
    _run(
        [
            str(ruff),
            "check",
            "--no-cache",
            "--config",
            str(root / "ruff.toml"),
            *paths,
        ],
        root,
    )
    _run(
        [
            str(ruff),
            "format",
            "--check",
            "--no-cache",
            "--config",
            str(root / "ruff.toml"),
            *paths,
        ],
        root,
    )


def _run(argv: list[str], cwd: Path) -> None:
    import subprocess

    completed = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "COMMAND_FAILED:"
            + " ".join(argv)
            + "\n"
            + completed.stdout
            + completed.stderr
        )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
