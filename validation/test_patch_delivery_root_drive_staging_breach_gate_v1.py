# project-path: validation/test_patch_delivery_root_drive_staging_breach_gate_v1.py
"""Validate root-drive-to-daily-work staging breach enforcement."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_ai_response_patch_delivery_contract import ResponseValidationError
from scripts.validate_ai_response_patch_delivery_staging_gate import (
    validate_root_drive_staging_install_block,
)

FEATURE_ID = "patch-delivery-root-drive-staging-breach-enforcement-v1"
PROMPT_PATH = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md"
WRAPPER_PATH = PROJECT_ROOT / "scripts" / "validate_ai_response_patch_delivery.py"
AUDIT_PATH = PROJECT_ROOT / "scripts" / "validate_ai_response_patch_delivery_audit_runner.py"
HELPER_PATH = PROJECT_ROOT / "scripts" / "validate_ai_response_patch_delivery_staging_gate.py"


def _good_block() -> str:
    return '''
$PROJECT_ROOT = "E:\\kanda_reasoner"
$PATCH_NAME = "demo.zip"
$PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
$PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\\")
$DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
$STAGED_PATCH_ZIP = Join-Path $DAILY_ROOT $PATCH_NAME
$EXTRACT_ROOT = Join-Path $DAILY_ROOT "demo_extract"
if (-not (Test-Path $DAILY_ROOT)) { New-Item -ItemType Directory -Path $DAILY_ROOT -Force | Out-Null }
if (Test-Path $ROOT_PATCH_ZIP) {
    Copy-Item -Path $ROOT_PATCH_ZIP -Destination $STAGED_PATCH_ZIP -Force
    if (-not (Test-Path $STAGED_PATCH_ZIP)) { throw "Patch ZIP staging failed" }
    Remove-Item -Path $ROOT_PATCH_ZIP -Force
}
if (-not (Test-Path $STAGED_PATCH_ZIP)) { throw "zip is not in root of drive:\\ where project is" }
Expand-Archive -Path $STAGED_PATCH_ZIP -DestinationPath $EXTRACT_ROOT -Force
'''


def _expect_fail(block: str, fragment: str) -> None:
    try:
        validate_root_drive_staging_install_block(block)
    except ResponseValidationError as exc:
        if fragment.lower() not in str(exc).lower():
            raise AssertionError(f"Expected {fragment!r} in {exc!s}") from exc
        return
    raise AssertionError("Expected staging gate failure")


def test_accepts_root_drive_copy_delete_then_staged_extract() -> None:
    validate_root_drive_staging_install_block(_good_block())


def test_rejects_extract_from_root_drive_zip() -> None:
    bad = _good_block().replace("Expand-Archive -Path $STAGED_PATCH_ZIP", "Expand-Archive -Path $ROOT_PATCH_ZIP")
    _expect_fail(bad, "must not extract from the drive-root ZIP")


def test_rejects_copy_without_root_delete() -> None:
    bad = _good_block().replace("    Remove-Item -Path $ROOT_PATCH_ZIP -Force\n", "")
    _expect_fail(bad, "delete the temporary drive-root ZIP copy")


def test_rejects_missing_exact_bridge_error() -> None:
    bad = _good_block().replace("zip is not in root of drive:\\ where project is", "Patch not found")
    _expect_fail(bad, "exact bridge error")


def test_prompt_declares_breach_conditions() -> None:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    required = [
        "After successful staging, delete the temporary downloaded ZIP copy from the drive root",
        "Install and extract only from the ZIP path inside the delete-after-daily-work staging folder",
        "Hard breach conditions for the installer staging rule:",
        "BREACH if the install block extracts from `<drive>:\\PATCH_NAME.zip` or `$ROOT_PATCH_ZIP`.",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError("Prompt is missing bridge staging text: " + ", ".join(missing))


def test_response_validator_wires_staging_gate() -> None:
    wrapper = WRAPPER_PATH.read_text(encoding="utf-8")
    audit = AUDIT_PATH.read_text(encoding="utf-8")
    helper = HELPER_PATH.read_text(encoding="utf-8")
    required = [
        "Root-drive staging breach gate must validate deletion of root ZIP copy",
        "validate_root_drive_staging_install_block(block)",
        "Install block must not extract from the drive-root ZIP",
        "zip is not in root of drive:\\\\ where project is",
    ]
    combined = "\n".join([wrapper, audit, helper])
    missing = [item for item in required if item not in combined]
    if missing:
        raise AssertionError("Response validator is missing staging gate wiring: " + ", ".join(missing))


def test_touched_python_modules_compile_and_line_count() -> None:
    files = [
        WRAPPER_PATH,
        AUDIT_PATH,
        HELPER_PATH,
        Path(__file__),
        PROJECT_ROOT / "tools" / "validate_patch_delivery_root_drive_staging_breach_gate_v1.py",
    ]
    for path in files:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        line_count = len(source.splitlines())
        if line_count > 500:
            raise AssertionError(f"Module exceeds 500 physical lines: {path} ({line_count})")


def main() -> int:
    tests = [
        test_accepts_root_drive_copy_delete_then_staged_extract,
        test_rejects_extract_from_root_drive_zip,
        test_rejects_copy_without_root_delete,
        test_rejects_missing_exact_bridge_error,
        test_prompt_declares_breach_conditions,
        test_response_validator_wires_staging_gate,
        test_touched_python_modules_compile_and_line_count,
    ]
    for test in tests:
        test()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
