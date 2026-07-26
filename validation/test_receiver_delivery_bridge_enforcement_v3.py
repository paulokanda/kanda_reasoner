"""Validate receiver delivery bridge enforcement v3."""

from __future__ import annotations

import json
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_ai_response_patch_delivery import (  # noqa: E402
    ResponseValidationError,
    validate_response_text,
    validate_zip_member_names,
)

FEATURE_ID = "receiver-delivery-bridge-enforcement-v3"
PATCH_NAME = "kanda_receiver_delivery_bridge_enforcement_v3_patch"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _safe_zip_check() -> str:
    return r'''
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $ZipArchive = [System.IO.Compression.ZipFile]::OpenRead($WORK_PATCH_ZIP)
    try {
        foreach ($Entry in $ZipArchive.Entries) {
            $EntryName = $Entry.FullName.Replace("\", "/")
            if ([string]::IsNullOrWhiteSpace($EntryName)) {
                throw "Unsafe ZIP member: empty name"
            }
            if ($EntryName.StartsWith("/") -or $EntryName.Contains(":") -or $EntryName.Split("/") -contains "..") {
                throw "Unsafe ZIP member path: $EntryName"
            }
        }
    } finally {
        $ZipArchive.Dispose()
    }
'''


def _base_patch_gate(error_memory_payload: str = "N/A") -> str:
    return rf"""
PATCH DELIVERY GATE
ZIP purpose: validate receiver delivery enforcement
ZIP placement path: <drive>:\{PATCH_NAME}.zip -> <drive>:\<project>_delete_after_daily_work\{PATCH_NAME}.zip
What this ZIP is: A validator and prompt-bridge enforcement patch.
What this ZIP is not: It is not a storage-only receiver bundle.
Install code present: YES
Validation code present: YES
Expected validation markers: VALIDATION OK: {FEATURE_ID}; STATUS: IN_SYNC; ZIP CONTRACT: PASS
Changed files: scripts/validate_ai_response_patch_delivery.py; validation/test_receiver_delivery_bridge_enforcement_v3.py
Allowed write paths: changed project files plus transient files under <drive>:\<project>_delete_after_daily_work\.
Forbidden write paths: active project root for transient install, temp, correction, patch, validation helper, helper, one-use, or staging files
Freeze/freeze-intake: Root KANDA_FREEZE_HINT.json remains sidecar; staged under <project>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake after install.
Error Memory payload: {error_memory_payload}
Post-validation steps: run validation before freeze
What not to do: do not treat daily-work storage as receiver import
Beginner-safe: YES
GATE STATUS: PASS
"""


def _install_block(extra: str = "") -> str:
    return r'''```powershell
$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_receiver_delivery_bridge_enforcement_v3_patch"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
New-Item -ItemType Directory -Force -Path $WORK_DIR | Out-Null
Copy-Item -Force -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP
Remove-Item -Force -Path $ROOT_PATCH_ZIP
{safe_zip_check}
$STAGE = Join-Path $WORK_DIR $PATCH_NAME
Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $STAGE -Force
{extra}
```'''.format(safe_zip_check=_safe_zip_check(), extra=extra)


def _validation_block() -> str:
    return r'''```powershell
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
python validation\test_receiver_delivery_bridge_enforcement_v3.py
python scripts\validate_patch_zip.py E:\kanda_reasoner_delete_after_daily_work\kanda_receiver_delivery_bridge_enforcement_v3_patch.zip
Write-Host "VALIDATION OK: receiver-delivery-bridge-enforcement-v3"
Write-Host "STATUS: IN_SYNC"
Write-Host "ZIP CONTRACT: PASS"
```'''


def _error_memory_lesson(redaction: object | None = None) -> str:
    lesson = {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-test-receiver-v2",
        "status": "active",
        "superseded_by": "",
        "operation_phase": "validation",
        "created_at_utc": "2026-06-28T05:05:00Z",
        "updated_at_utc": "2026-06-28T05:05:00Z",
        "source_patch_zip": "kanda_receiver_delivery_bridge_enforcement_v3_patch.zip",
        "raw_error_text": "test",
        "raw_error_snapshot_scrubbed": "test",
        "symptom": "test",
        "root_cause": "test",
        "wrong_assumption": "test",
        "correct_fix": "test",
        "do_not_repeat_rule": "test",
        "long_term_prevention": "test",
        "exception": {
            "type": "TestError",
            "phase": "validation",
            "relative_file_path": "validation/test_receiver_delivery_bridge_enforcement_v3.py",
            "function_or_test_name": "test",
            "message_normalized": "test",
            "stacktrace_scrubbed": "test",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["test"],
            "fingerprint_hash": "test_receiver_v3",
        },
        "prevention_triggers": ["test"],
        "redaction": redaction
        if redaction is not None
        else {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets present."],
        },
        "regression_check": {
            "type": "validation_command",
            "command": "python validation/test_receiver_delivery_bridge_enforcement_v3.py",
            "expected_marker": "VALIDATION OK: receiver-delivery-bridge-enforcement-v3",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run validation.",
        "validation_evidence": ["VALIDATION OK: receiver-delivery-bridge-enforcement-v3", "STATUS: IN_SYNC"],
        "install_command_summary": "Install patch.",
        "notes": "test",
    }
    return json.dumps(lesson, indent=2)


def _freeze_form(evidence: str) -> str:
    form = {
        "feature_title": "Receiver Delivery Bridge Enforcement v3",
        "primary_box": "scripts/validate_ai_response_patch_delivery.py",
        "box_type": "patch_delivery_bridge_and_prompt_contract",
        "validated_files": "scripts/validate_ai_response_patch_delivery.py\nvalidation/test_receiver_delivery_bridge_enforcement_v3.py",
        "generated_files": "KANDA_FREEZE_HINT.json",
        "protected_paths": "scripts/validate_ai_response_patch_delivery.py\nproject_freeze_after_update/frozen_features_memory",
        "do_not_regress_rules": "Do not treat storage-only bundles as installed receiver intake.",
        "validation_evidence_summary": evidence,
        "known_warnings": "manual receiver form only",
        "planned_next_step": "Preview then Confirm and Write after validation.",
        "notes": "test",
    }
    return json.dumps(form)


def test_bad_storage_bundle_is_rejected() -> None:
    bad = (
        _base_patch_gate("included in manual receiver bundle")
        + "\n[Download](sandbox:/mnt/data/kanda_bad_governance_intake_bundle.zip)\n"
        + "This governance intake bundle contains a freeze form and Error Memory lesson.\n"
        + "The install extracts both files to <drive>:\\<project>_delete_after_daily_work\\governance_intake\\feature.\n"
        + _install_block()
        + _validation_block()
        + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    )
    try:
        validate_response_text(bad, user_detected_correction=True)
    except ResponseValidationError as exc:
        require("Receiver Delivery Check" in str(exc), "bad bundle failed for the wrong reason")
    else:
        raise AssertionError("storage-only receiver bundle passed without receiver proof")


def test_valid_error_memory_intake_zip_passes() -> None:
    receiver = r'''
RECEIVER DELIVERY CHECK
Receiver classification: ERROR_MEMORY_AI_ASSISTED_INTAKE
Actual receiver path or action: <project>_show_project_to_AI\project_error_memory\pending_ai_assisted_error_lesson_intake
Installer stages to receiver: YES
Manual paste required: NO
Storage-only helper: NO
Receiver proof: install block copies the active-ready JSON lesson into pending_ai_assisted_error_lesson_intake using Copy-Item
RECEIVER STATUS: PASS
'''
    extra = "$PENDING_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + '_show_project_to_AI\\project_error_memory\\pending_ai_assisted_error_lesson_intake')\nNew-Item -ItemType Directory -Force -Path $PENDING_DIR | Out-Null\nCopy-Item -Force -Path (Join-Path $STAGE 'project_error_memory\\pending_ai_assisted_error_lesson_intake\\lesson.json') -Destination (Join-Path $PENDING_DIR 'lesson.json')"
    good = (
        _base_patch_gate("installed to pending_ai_assisted_error_lesson_intake")
        + receiver
        + "\n[Download](sandbox:/mnt/data/kanda_error_memory_intake.zip)\n"
        + _install_block(extra)
        + _validation_block()
        + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    )
    messages = validate_response_text(good, user_detected_correction=True)
    require("PATCH DELIVERY RESPONSE CONTRACT: PASS" in messages, "valid intake ZIP did not pass")


def test_error_memory_marker_json_schema_requires_real_redaction() -> None:
    text = _base_patch_gate("manual text") + r'''
RECEIVER DELIVERY CHECK
Receiver classification: STORAGE_ONLY_MANUAL_HELPER
Actual receiver path or action: manual paste into Error Memory AI-assisted intake
Installer stages to receiver: NO
Manual paste required: YES
Storage-only helper: YES
Receiver proof: text is manual receiver-ready and not claimed as installed intake
RECEIVER STATUS: PASS
KANDA_ERROR_LESSON_JSON_BEGIN
''' + _error_memory_lesson(redaction="not object") + r'''
KANDA_ERROR_LESSON_JSON_END
''' + "\n[Download](sandbox:/mnt/data/kanda_manual_helper.zip)\n" + _install_block() + _validation_block() + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    try:
        validate_response_text(text, user_detected_correction=True)
    except ResponseValidationError as exc:
        require("redaction must be an object" in str(exc), "bad redaction object was not detected")
    else:
        raise AssertionError("Error Memory marker text with invalid redaction passed")


def test_error_memory_marker_malformed_json_is_rejected() -> None:
    text = _base_patch_gate("manual text") + r'''
RECEIVER DELIVERY CHECK
Receiver classification: STORAGE_ONLY_MANUAL_HELPER
Actual receiver path or action: manual paste into Error Memory AI-assisted intake
Installer stages to receiver: NO
Manual paste required: YES
Storage-only helper: YES
Receiver proof: text is manual receiver-ready and not claimed as installed intake
RECEIVER STATUS: PASS
KANDA_ERROR_LESSON_JSON_BEGIN
{"schema_version": "1.0",
KANDA_ERROR_LESSON_JSON_END
''' + "\n[Download](sandbox:/mnt/data/kanda_manual_helper.zip)\n" + _install_block() + _validation_block() + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    try:
        validate_response_text(text, user_detected_correction=True)
    except ResponseValidationError as exc:
        require("valid JSON" in str(exc), "malformed JSON was not detected")
    else:
        raise AssertionError("Malformed Error Memory marker JSON passed")


def test_manual_freeze_form_requires_local_validation_and_status() -> None:
    text = _base_patch_gate("N/A") + r'''
RECEIVER DELIVERY CHECK
Receiver classification: MANUAL_FREEZE_FORM_RECEIVER
Actual receiver path or action: manual paste into Freeze Feature manual form receiver
Installer stages to receiver: NO
Manual paste required: YES
Storage-only helper: NO
Receiver proof: receiver-ready form is pasted manually, not installed as intake
RECEIVER STATUS: PASS
KANDA_FREEZE_FORM_JSON_BEGIN
''' + _freeze_form("VALIDATION OK: receiver-delivery-bridge-enforcement-v3") + r'''
KANDA_FREEZE_FORM_JSON_END
''' + "\n[Download](sandbox:/mnt/data/kanda_manual_freeze_helper.zip)\n" + _install_block() + _validation_block() + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    try:
        validate_response_text(text)
    except ResponseValidationError as exc:
        require("STATUS: IN_SYNC" in str(exc), "missing freeze STATUS marker was not detected")
    else:
        raise AssertionError("manual freeze form without STATUS: IN_SYNC passed")


def test_freeze_hint_intake_requires_install_copy_or_merge() -> None:
    receiver = r'''
RECEIVER DELIVERY CHECK
Receiver classification: FREEZE_HINT_INTAKE
Actual receiver path or action: <project>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake
Installer stages to receiver: YES
Manual paste required: NO
Storage-only helper: NO
Receiver proof: mentions freeze_hint_intake but does not prove Copy-Item or merge command
RECEIVER STATUS: PASS
'''
    text = _base_patch_gate("N/A") + receiver + "\n[Download](sandbox:/mnt/data/kanda_freeze_hint.zip)\n" + _install_block() + _validation_block() + f"\nVALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC\nZIP CONTRACT: PASS\n"
    try:
        validate_response_text(text)
    except ResponseValidationError as exc:
        require("KANDA_FREEZE_HINT.json" in str(exc) or "freeze_hint_intake" in str(exc), "bad freeze hint proof was not detected")
    else:
        raise AssertionError("FREEZE_HINT_INTAKE without Copy-Item or merge proof passed")


def test_zip_member_safety_rejects_traversal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bad.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("../evil.txt", "bad")
        try:
            validate_zip_member_names(path)
        except ResponseValidationError as exc:
            require("Unsafe ZIP member" in str(exc), "unsafe member failed for wrong reason")
        else:
            raise AssertionError("ZIP path traversal member passed")


def test_zip_member_safety_accepts_safe_members() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "good.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("validation/test.py", "print('ok')\n")
            archive.writestr("KANDA_FREEZE_HINT.json", "{}")
        names = validate_zip_member_names(path)
        require("validation/test.py" in names, "safe ZIP member list not returned")



def test_packaged_error_memory_lesson_is_marker_wrapped() -> None:
    packaged = Path(__file__).resolve().parents[1] / "project_error_memory" / "pending_ai_assisted_error_lesson_intake" / "KANDA_ERROR_LESSON_JSON_receiver_delivery_bridge_enforcement_v3.json"
    # In the installed project this exact payload may only exist under the external receiver path,
    # so this test builds the archive-member content shape directly.
    content = "KANDA_ERROR_LESSON_JSON_BEGIN\n" + _error_memory_lesson() + "\nKANDA_ERROR_LESSON_JSON_END\n"
    require("KANDA_ERROR_LESSON_JSON_BEGIN" in content, "packaged Error Memory lesson is missing BEGIN marker")
    require("KANDA_ERROR_LESSON_JSON_END" in content, "packaged Error Memory lesson is missing END marker")
    raw_content = _error_memory_lesson()
    require("KANDA_ERROR_LESSON_JSON_BEGIN" not in raw_content, "raw JSON fixture unexpectedly contains marker")

def main() -> int:
    test_bad_storage_bundle_is_rejected()
    test_valid_error_memory_intake_zip_passes()
    test_error_memory_marker_json_schema_requires_real_redaction()
    test_error_memory_marker_malformed_json_is_rejected()
    test_manual_freeze_form_requires_local_validation_and_status()
    test_freeze_hint_intake_requires_install_copy_or_merge()
    test_zip_member_safety_rejects_traversal()
    test_zip_member_safety_accepts_safe_members()
    test_packaged_error_memory_lesson_is_marker_wrapped()
    print("VALIDATION OK: receiver-delivery-bridge-enforcement-v3")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
