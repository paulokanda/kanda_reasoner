# project-path: tools/validate_free_python_coding_ai_update1_validation_wrapper_v1r2.py
"""Validate the Update 1 native-stderr-safe delivery correction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import py_compile
import re
from typing import Any, Sequence

FEATURE_ID = (
    "free-python-coding-ai-catalog-and-config-update1-validation-correction-v1r2"
)
ORIGINAL_FEATURE_ID = "free-python-coding-ai-catalog-and-config-update1-v1"

REQUIRED_WRAPPER_TOKENS = (
    '$ErrorActionPreference = "Continue"',
    '$ExitCode = $LASTEXITCODE',
    '$ErrorActionPreference = $PreviousErrorActionPreference',
    'PSNativeCommandUseErrorActionPreference',
    'Invoke-KandaPythonCaptured',
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
        _require(target.is_file(), "REQUIRED UPDATE 1 SOURCE PRESENT: " + relative)
        _require(
            _sha256(target) == expected,
            "REQUIRED UPDATE 1 SOURCE HASH: " + relative,
        )
    print("ORIGINAL UPDATE 1 SOURCE FINGERPRINT: PASS")


def _validate_native_helper(package_root: Path) -> None:
    helper = package_root / "NATIVE_PROCESS.ps1"
    text = helper.read_text(encoding="utf-8")
    for token in REQUIRED_WRAPPER_TOKENS:
        _require(token in text, "NATIVE PROCESS TOKEN " + token)
    _require("finally" not in text.casefold(), "NATIVE PROCESS FINALLY ABSENT")
    _require(
        "return [pscustomobject]" in text,
        "NATIVE PROCESS STRUCTURED RESULT",
    )
    print("NATIVE STDERR EXIT-CODE AUTHORITY CONTRACT: PASS")


def _validate_validate_script(package_root: Path) -> None:
    path = package_root / "VALIDATE.ps1"
    text = path.read_text(encoding="utf-8")
    _require(
        '. (Join-Path $PSScriptRoot "NATIVE_PROCESS.ps1")' in text,
        "VALIDATE USES CANONICAL NATIVE HELPER",
    )
    _require(
        "NATIVE_STDERR_ZERO_EXIT_USES_EXIT_CODE_AUTHORITY: PASS" in text,
        "VALIDATE REQUIRES STDERR PROBE",
    )
    _require(
        "VALIDATION OK: $OriginalFeatureId" in text,
        "VALIDATE REQUIRES ORIGINAL FEATURE MARKER",
    )
    _require(
        "VALIDATION OK: $FeatureId" in text,
        "VALIDATE EMITS CORRECTION MARKER",
    )
    _require("Tee-Object" not in text, "VALIDATE TEE MARKER COUPLING ABSENT")
    unsafe = re.findall(r"&\s+\$PythonExe[^\r\n]*2>&1", text)
    _require(not unsafe, "VALIDATE UNSAFE DIRECT STDERR CAPTURE ABSENT")
    _require("finally" not in text.casefold(), "VALIDATE FINALLY ABSENT")
    print("VALIDATE WRAPPER NATIVE STDERR CORRECTION: PASS")


def _validate_freeze_script(package_root: Path) -> None:
    path = package_root / "PREPARE_FREEZE.ps1"
    text = path.read_text(encoding="utf-8")
    _require(
        '. (Join-Path $PSScriptRoot "NATIVE_PROCESS.ps1")' in text,
        "FREEZE USES CANONICAL NATIVE HELPER",
    )
    unsafe = re.findall(r"&\s+\$PythonExe[^\r\n]*2>&1", text)
    _require(not unsafe, "FREEZE UNSAFE DIRECT STDERR CAPTURE ABSENT")
    _require(
        "FREEZE_HINT_EVIDENCE_MERGE_OK:" in text,
        "FREEZE REQUIRES MERGE MARKER",
    )
    _require("finally" not in text.casefold(), "FREEZE FINALLY ABSENT")
    print("FREEZE WRAPPER NATIVE STDERR CORRECTION: PASS")


def _validate_probe(package_root: Path) -> None:
    path = package_root / "NATIVE_STDERR_PROBE.py"
    py_compile.compile(str(path), doraise=True)
    text = path.read_text(encoding="utf-8")
    _require("file=sys.stderr" in text, "NATIVE STDERR PROBE WRITES STDERR")
    _require("NATIVE_STDERR_PROBE_OK" in text, "NATIVE STDERR PROBE SUCCESS MARKER")


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
        _validate_native_helper(package_root)
        _validate_validate_script(package_root)
        _validate_freeze_script(package_root)
        _validate_probe(package_root)
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
