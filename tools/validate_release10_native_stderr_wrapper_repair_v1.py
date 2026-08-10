"""Validate Release 10 native stderr wrapper repair contracts."""
from __future__ import annotations

import argparse
from pathlib import Path

FEATURE_ID = "release10-native-stderr-wrapper-repair-v1"
UNSAFE_FRAGMENTS = (
    '& python @Arguments 2>&1 | ForEach-Object',
    '$Output = & python @Arguments 2>&1\n    $Code = $LASTEXITCODE',
)
REQUIRED_CAPTURE_FRAGMENTS = (
    'function Invoke-PythonCaptured',
    '$PreviousErrorActionPreference = $ErrorActionPreference',
    '$ErrorActionPreference = "Continue"',
    '$Code = $LASTEXITCODE',
    '$ErrorActionPreference = $PreviousErrorActionPreference',
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-root", required=True)
    return parser.parse_args()


def _read_text(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise AssertionError("UTF8_BOM_FORBIDDEN:" + path.name)
    return data.decode("utf-8")


def _assert_capture_contract(path: Path, *, require_probe: bool) -> None:
    text = _read_text(path)
    for fragment in REQUIRED_CAPTURE_FRAGMENTS:
        if fragment not in text:
            raise AssertionError(path.name + " missing safe capture fragment: " + fragment)
    for fragment in UNSAFE_FRAGMENTS:
        if fragment in text:
            raise AssertionError(path.name + " contains unsafe capture fragment: " + fragment)
    helper_start = text.index("function Invoke-PythonCaptured")
    continue_index = text.index('$ErrorActionPreference = "Continue"', helper_start)
    code_index = text.index("$Code = $LASTEXITCODE", continue_index)
    restore_index = text.index(
        "$ErrorActionPreference = $PreviousErrorActionPreference",
        code_index,
    )
    if not helper_start < continue_index < code_index < restore_index:
        raise AssertionError(path.name + " safe capture order is invalid")
    if require_probe:
        probe = 'tools/validate_native_stderr_exitcode_classification_v1.py'
        if probe not in text:
            raise AssertionError("VALIDATE.ps1 missing benign native stderr probe")
        marker = "NATIVE_STDERR_EXITCODE_CLASSIFICATION: PASS"
        if marker not in text:
            raise AssertionError("VALIDATE.ps1 missing required benign stderr marker gate")


def main() -> None:
    args = _parse_args()
    patch_root = Path(args.patch_root).expanduser().resolve(strict=True)
    validate_path = patch_root / "VALIDATE.ps1"
    freeze_path = patch_root / "FREEZE.ps1"
    if not validate_path.is_file():
        raise FileNotFoundError("VALIDATE.ps1 not found under patch root")
    if not freeze_path.is_file():
        raise FileNotFoundError("FREEZE.ps1 not found under patch root")

    _assert_capture_contract(validate_path, require_probe=True)
    print("RELEASE10_VALIDATE_NATIVE_STDERR_CAPTURE_SAFE: PASS")

    _assert_capture_contract(freeze_path, require_probe=False)
    print("RELEASE10_FREEZE_NATIVE_STDERR_CAPTURE_SAFE: PASS")

    lesson_root = patch_root / "payload" / "error_memory_receive_blocks"
    lesson_files = sorted(lesson_root.glob("KANDA_ERROR_LESSON_JSON_*.txt"))
    if len(lesson_files) != 1:
        raise AssertionError("Expected exactly one packaged Error Memory lesson block")
    raw_files = sorted(lesson_root.glob("RAW_ERROR_EVIDENCE_*.txt"))
    if len(raw_files) != 1:
        raise AssertionError("Expected exactly one packaged raw error evidence file")
    print("RELEASE10_ERROR_MEMORY_RECEIVER_PAYLOAD_PRESENT: PASS")

    install_text = _read_text(patch_root / "INSTALL.ps1")
    required_install = (
        "pending_ai_assisted_error_lesson_intake",
        "error_memory_receive_blocks",
        "KANDA_ERROR_LESSON_JSON_release10-known-native-stderr-wrapper-regression-v1.txt",
    )
    for fragment in required_install:
        if fragment not in install_text:
            raise AssertionError("INSTALL.ps1 missing Error Memory staging fragment: " + fragment)
    print("RELEASE10_ERROR_MEMORY_DYNAMIC_STAGING_CONTRACT: PASS")

    print("RELEASE10_NATIVE_STDERR_WRAPPER_REPAIR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
