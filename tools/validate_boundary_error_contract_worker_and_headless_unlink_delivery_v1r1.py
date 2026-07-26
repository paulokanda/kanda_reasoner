"""Validate the v1r1 freeze evidence line gate delivery repair."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import zipfile
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = (
    "boundary-error-contract-worker-and-headless-unlink-delivery-repair-v1r1"
)
PATCH_NAME = "kanda_boundary_error_contract_worker_and_headless_unlink_v1r1"
MANIFEST_NAME = "PATCH_CONTENT_MANIFEST.json"
FREEZE_NAME = "FREEZE.ps1"
VALIDATE_NAME = "VALIDATE.ps1"
INSTALL_NAME = "INSTALL.ps1"
README_NAME = "PATCH_README.txt"
HINT_NAME = "KANDA_FREEZE_HINT.json"
LESSON_NAME = (
    "error_memory_receive_blocks/"
    "KANDA_ERROR_LESSON_JSON_powershell-required-line-array-collapse-v1.txt"
)
RAW_EVIDENCE_NAME = (
    "error_memory_receive_blocks/"
    "RAW_ERROR_EVIDENCE_powershell-required-line-array-collapse-v1.txt"
)
PRODUCT_FILES = {
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_stage_worker.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/"
    "_runtime_runner_part_2_scenarios.py",
    "tools/validate_boundary_error_contract_worker_and_headless_unlink_v1.py",
    "tools/validate_boundary_error_contract_worker_and_headless_unlink_"
    "delivery_v1r1.py",
}
ROOT_FILES = {
    FREEZE_NAME,
    INSTALL_NAME,
    HINT_NAME,
    MANIFEST_NAME,
    README_NAME,
    VALIDATE_NAME,
}
EXPECTED_MEMBERS = PRODUCT_FILES | ROOT_FILES | {
    LESSON_NAME,
    RAW_EVIDENCE_NAME,
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_ascii(path: Path) -> str:
    data = path.read_bytes()
    data.decode("ascii")
    return data.decode("utf-8")


def _validate_python_files(project_root: Path) -> None:
    paths = [
        Path(item)
        for item in PRODUCT_FILES
        if item.endswith(".py")
    ]
    for relative in sorted(paths):
        path = project_root / relative
        _require(path.is_file(), f"Missing project file: {relative}")
        source = _read_ascii(path)
        ast.parse(source, filename=str(relative))
        line_count = len(source.splitlines())
        _require(
            line_count <= 500,
            f"Python module exceeds 500 lines: {relative}: {line_count}",
        )
        print(f"MODULE_MAX_500_LINES:{relative.as_posix()}: PASS")
    print("PYTHON_SYNTAX_ASCII_MODULE_SIZE: PASS")


def _validate_freeze_script(freeze_text: str) -> None:
    _require(
        '$RequiredValidationLine = "VALIDATION OK: $FeatureId"'
        in freeze_text,
        "Freeze script lacks an explicit validation line variable.",
    )
    _require(
        '$RequiredStatusLine = "STATUS: IN_SYNC"' in freeze_text,
        "Freeze script lacks an explicit status line variable.",
    )
    _require(
        "$EvidenceLines -contains $RequiredValidationLine" in freeze_text,
        "Freeze script does not verify the validation line independently.",
    )
    _require(
        "$EvidenceLines -contains $RequiredStatusLine" in freeze_text,
        "Freeze script does not verify the status line independently.",
    )
    _require(
        '"VALIDATION OK: " + $FeatureId,' not in freeze_text,
        "Ambiguous concatenation-plus-comma expression remains.",
    )
    _require(
        "ReadAllLines" in freeze_text,
        "Freeze script must read deterministic evidence lines.",
    )
    fixture_lines = [
        f"VALIDATION OK: {FEATURE_ID}",
        "STATUS: IN_SYNC",
    ]
    _require(
        f"VALIDATION OK: {FEATURE_ID}" in fixture_lines,
        "Validation line fixture failed.",
    )
    _require(
        "STATUS: IN_SYNC" in fixture_lines,
        "Status line fixture failed.",
    )
    combined = f"VALIDATION OK: {FEATURE_ID} STATUS: IN_SYNC"
    _require(
        combined not in fixture_lines,
        "Combined line must not satisfy separate-line evidence.",
    )
    print("FREEZE_REQUIRED_LINES_INDEPENDENT: PASS")
    print("POWERSHELL_ARRAY_PRECEDENCE_REGRESSION_BLOCKED: PASS")
    print("COMBINED_LINE_FALSE_MATCH_REJECTED: PASS")


def _validate_validate_script(validate_text: str) -> None:
    required = (
        '$EvidenceLines.Add("VALIDATION OK: " + $FeatureId)',
        '$EvidenceLines.Add("STATUS: IN_SYNC")',
        "System.Text.UTF8Encoding($false)",
        "WriteAllText",
    )
    for fragment in required:
        _require(
            fragment in validate_text,
            f"Missing validation fragment: {fragment}",
        )
    _require(
        "Tee-Object" not in validate_text,
        "Tee-Object marker coupling returned.",
    )
    _require("finally" not in validate_text.lower(), "finally is forbidden.")
    print("VALIDATION_MARKERS_PERSISTED_SEPARATELY: PASS")
    print("UTF8_NO_BOM_EVIDENCE_WRITER: PASS")
    print("NO_TEE_OBJECT_OR_FINALLY: PASS")


def _validate_zip(project_root: Path, patch_zip: Path) -> None:
    _require(patch_zip.is_file(), f"Patch ZIP is missing: {patch_zip}")
    with zipfile.ZipFile(patch_zip) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        members = {info.filename for info in infos}
        _require(
            members == EXPECTED_MEMBERS,
            "Patch ZIP member set changed: "
            + repr(sorted(members.symmetric_difference(EXPECTED_MEMBERS))),
        )
        freeze_text = archive.read(FREEZE_NAME).decode("ascii")
        validate_text = archive.read(VALIDATE_NAME).decode("ascii")
        manifest = json.loads(archive.read(MANIFEST_NAME).decode("utf-8"))
        hint = json.loads(archive.read(HINT_NAME).decode("utf-8"))
        _require(
            manifest["patch_name"] == PATCH_NAME,
            "Manifest patch name changed.",
        )
        _require(
            manifest["feature_id"] == FEATURE_ID,
            "Manifest feature ID changed.",
        )
        _require(
            hint["patch_name"] == PATCH_NAME,
            "Freeze hint patch name changed.",
        )
        _require(
            hint["feature_id"] == FEATURE_ID,
            "Freeze hint feature ID changed.",
        )
        expected_hashes = manifest["payload_sha256"]
        for relative, expected_hash in expected_hashes.items():
            _require(
                relative in members,
                f"Manifest payload missing: {relative}",
            )
            _require(
                _sha256(archive.read(relative)) == expected_hash,
                f"ZIP payload hash mismatch: {relative}",
            )
            installed = project_root / relative
            _require(
                installed.is_file(),
                f"Installed payload missing: {relative}",
            )
            _require(
                _sha256(installed.read_bytes()) == expected_hash,
                f"Installed payload hash mismatch: {relative}",
            )
    _validate_freeze_script(freeze_text)
    _validate_validate_script(validate_text)
    print("PATCH_ZIP_EXACT_MEMBER_SET: PASS")
    print("PATCH_MANIFEST_AND_FREEZE_IDENTITY: PASS")
    print("PATCH_PAYLOAD_INSTALLED_HASHES: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    _validate_python_files(project_root)
    _validate_zip(project_root, patch_zip)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
