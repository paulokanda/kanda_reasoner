# project-path: tools/validate_free_python_coding_ai_update3_validation_wrapper_v1r1.py
"""Validate the Update 3 PowerShell path-delivery correction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import py_compile
from typing import Any, Sequence

FEATURE_ID = (
    "free-python-coding-ai-governed-draft-handoffs-update3-"
    "validation-correction-v1r1"
)
ORIGINAL_FEATURE_ID = "free-python-coding-ai-governed-draft-handoffs-update3-v1"

POWERSHELL_FILES = (
    "RUN_INSTALL.ps1",
    "INSTALL.ps1",
    "RUN_VALIDATE.ps1",
    "VALIDATE.ps1",
    "PREPARE_FREEZE.ps1",
    "NATIVE_PROCESS.ps1",
)

REQUIRED_PATH_TOKENS = (
    '$ToolsRoot = Join-Path $ProjectPath "tools"',
    '$Update1Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update1_v1.py"',
    '$Update2Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update2_v1.py"',
    '$Update3Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update3_v1.py"',
    '$DeliveryValidator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update3_validation_wrapper_v1r1.py"',
    '$ScriptsRoot = Join-Path $ProjectPath "scripts"',
    '$ZipValidator = Join-Path $ScriptsRoot "validate_patch_zip.py"',
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _load_manifest(package_root: Path) -> dict[str, Any]:
    path = package_root / "INSTALL_MANIFEST.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("INSTALL_MANIFEST.json root must be an object.")
    return data


def _validate_required_existing(tool_root: Path, package_root: Path) -> None:
    manifest = _load_manifest(package_root)
    records = manifest.get("required_existing_files")
    if not isinstance(records, list) or not records:
        raise RuntimeError("required_existing_files must be a non-empty list.")
    for item in records:
        if not isinstance(item, dict):
            raise RuntimeError("Invalid required_existing_files record.")
        relative = str(item.get("path") or "").replace("\\", "/")
        expected = str(item.get("sha256") or "").lower()
        target = (tool_root / relative).resolve()
        target.relative_to(tool_root)
        _require(target.is_file(), "REQUIRED UPDATE 3 SOURCE PRESENT: " + relative)
        _require(
            _sha256(target) == expected,
            "REQUIRED UPDATE 3 SOURCE HASH: " + relative,
        )
    print("ORIGINAL UPDATE 3 SOURCE FINGERPRINT: PASS")


def _invalid_control_offsets(raw: bytes) -> list[int]:
    return [
        index
        for index, value in enumerate(raw)
        if value < 32 and value not in {9, 10, 13}
    ]


def _validate_control_character_gate(package_root: Path) -> None:
    for name in POWERSHELL_FILES:
        path = package_root / name
        _require(path.is_file(), "POWERSHELL SCRIPT PRESENT: " + name)
        offsets = _invalid_control_offsets(path.read_bytes())
        _require(not offsets, "POWERSHELL CONTROL CHARACTERS ABSENT: " + name)
    _require(
        bool(_invalid_control_offsets(b'tools\\x0balidate_example.py'.replace(b'\\x0b', bytes([11])))),
        "POWERSHELL CONTROL CHARACTER FIXTURE REJECTED",
    )
    print("POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS")


def _validate_component_paths(package_root: Path) -> None:
    path = package_root / "VALIDATE.ps1"
    text = path.read_text(encoding="utf-8")
    for token in REQUIRED_PATH_TOKENS:
        _require(token in text, "VALIDATOR PATH TOKEN " + token)
    lowered = text.casefold()
    _require("toolsvalidate_" not in lowered, "CONCATENATED TOOLSVALIDATE PATH ABSENT")
    _require('"tools\\validate_' not in lowered, "ESCAPE-SENSITIVE TOOLS PATH ABSENT")
    _require('"scripts\\validate_' not in lowered, "ESCAPE-SENSITIVE SCRIPTS PATH ABSENT")
    _require("\\x0b" not in repr(path.read_bytes()), "VERTICAL TAB BYTE ABSENT")
    print("VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS")


def _validate_native_helper(package_root: Path) -> None:
    path = package_root / "NATIVE_PROCESS.ps1"
    text = path.read_text(encoding="utf-8")
    for token in (
        '$ErrorActionPreference = "Continue"',
        '$ExitCode = $LASTEXITCODE',
        '$ErrorActionPreference = $PreviousErrorActionPreference',
        'PSNativeCommandUseErrorActionPreference',
        'Invoke-KandaPythonCaptured',
    ):
        _require(token in text, "NATIVE PROCESS TOKEN " + token)
    _require("finally" not in text.casefold(), "NATIVE PROCESS FINALLY ABSENT")
    print("NATIVE STDERR EXIT-CODE AUTHORITY CONTRACT: PASS")


def _validate_validate_script(package_root: Path) -> None:
    text = (package_root / "VALIDATE.ps1").read_text(encoding="utf-8")
    _require(
        "POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS" in text,
        "VALIDATE REQUIRES CONTROL CHARACTER MARKER",
    )
    _require(
        "VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS" in text,
        "VALIDATE REQUIRES PATH COMPONENT MARKER",
    )
    _require(
        "VALIDATION OK: $OriginalFeatureId" in text,
        "VALIDATE REQUIRES ORIGINAL UPDATE 3 MARKER",
    )
    _require(
        "VALIDATION OK: $FeatureId" in text,
        "VALIDATE EMITS CORRECTION MARKER",
    )
    _require("finally" not in text.casefold(), "VALIDATE FINALLY ABSENT")
    print("UPDATE 3 VALIDATION DELIVERY CORRECTION: PASS")


def _validate_freeze_script(package_root: Path) -> None:
    text = (package_root / "PREPARE_FREEZE.ps1").read_text(encoding="utf-8")
    _require(
        "FREEZE_HINT_EVIDENCE_MERGE_OK:" in text,
        "FREEZE REQUIRES MERGE MARKER",
    )
    _require(
        "POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS" in text,
        "FREEZE REQUIRES CONTROL CHARACTER EVIDENCE",
    )
    _require(
        "VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS" in text,
        "FREEZE REQUIRES PATH COMPONENT EVIDENCE",
    )
    _require("finally" not in text.casefold(), "FREEZE FINALLY ABSENT")
    print("UPDATE 3 FREEZE DELIVERY CORRECTION: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve()
    package_root = Path(args.package_root).expanduser().resolve()
    try:
        _require(tool_root.is_dir(), "VALIDATOR TOOL ROOT IMPORT PATH")
        _require(package_root.is_dir(), "VALIDATOR PACKAGE ROOT")
        _validate_required_existing(tool_root, package_root)
        _validate_control_character_gate(package_root)
        _validate_component_paths(package_root)
        _validate_native_helper(package_root)
        _validate_validate_script(package_root)
        _validate_freeze_script(package_root)
        py_compile.compile(str(Path(__file__)), doraise=True)
        _require(True, "CORRECTION VALIDATOR PYTHON COMPILE")
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
