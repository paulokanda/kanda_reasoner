# project-path: tools/validate_patch_provenance_receiver_contract_v1.py
"""Focused validation for patch provenance and receiver contract release 5R2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any, Callable
import zipfile

from kanda_reasoner_app.patch_governance.validator import (
    PatchZipContractError,
    validate_patch_zip,
)
from kanda_reasoner_app.patch_governance.installer_template import (
    render_installer_template,
)

FEATURE_ID = "patch-provenance-receiver-contract-v1"
PATCH_NAME = "kanda_patch_provenance_receiver_contract_v1"
ZIP_NAME = PATCH_NAME + ".zip"

DELIVERY_NAME = "KANDA_PATCH_DELIVERY_MANIFEST.json"
TRACE_NAME = "KANDA_PATCH_TRACE.json"
INSTALL_NAME = "INSTALL_MANIFEST.json"
HINT_NAME = "KANDA_FREEZE_HINT.json"

SOURCE_FILES = (
    "kanda_reasoner_app/patch_governance/delivery_provenance_contract.py",
    "kanda_reasoner_app/patch_governance/models.py",
    "kanda_reasoner_app/patch_governance/validator.py",
    "kanda_reasoner_app/patch_governance/KANDA_PATCH_DELIVERY_MANIFEST.schema.json",
    "kanda_reasoner_app/patch_governance/KANDA_PATCH_TRACE.schema.json",
    "tools/validate_patch_provenance_receiver_contract_v1.py",
)

PROMPTS = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md",
)

FORBIDDEN_BOXES = (
    "Project selection registry",
    "Project operation authority",
    "Tool governance packaged resource",
    "Freeze writer",
    "Error Memory canonical stores",
)

FORBIDDEN_PATHS = (
    "Any external Project source root",
    "project_error_memory/",
    "tool_error_memory/",
    "project_freeze_after_update/frozen_features_memory/",
    "project_freeze_ledger/",
)

MARKERS = (
    "ZIP CONTRACT: PASS",
    "PATCH_PROVENANCE_REQUIRED: PASS",
    "PATCH_DELIVERY_MANIFEST_SCHEMA_ALIGNED: PASS",
    "PATCH_TRACE_SCHEMA_ALIGNED: PASS",
    "PATCH_IDENTITY_CROSSCHECK: PASS",
    "PATCH_CHANGED_FILE_SET_RECONCILED: PASS",
    "PATCH_SOURCE_BASELINE_PROVENANCE: PASS",
    "SOURCE_PATCH_RECEIVER_PROOF: PASS",
    "FREEZE_HINT_RECEIVER_PROOF: PASS",
    "PATCH_RECEIVER_AMBIGUITY_REJECTED: PASS",
    "PATCH_TRACE_TAMPER_REJECTED: PASS",
    "PATCH_LEGACY_COMPATIBILITY_PRESERVED: PASS",
    "TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS",
    f"VALIDATION OK: {FEATURE_ID}",
    "STATUS: IN_SYNC",
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _fixture_payload() -> dict[str, bytes]:
    payload_path = "kanda_reasoner_app/fixture_owner.py"
    payload_bytes = (
        '# project-path: kanda_reasoner_app/fixture_owner.py\n'
        '"""Fixture payload for patch provenance validation."""\n'
        'VALUE = "installed"\n'
    ).encode("utf-8")
    installed_hash = _sha256(payload_bytes)
    baseline_hash = "1" * 64

    install = {
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "patch_name": PATCH_NAME,
        "files": [
            {
                "path": payload_path,
                "operation": "replace",
                "baseline_sha256": baseline_hash,
                "installed_sha256": installed_hash,
                "size_bytes": len(payload_bytes),
            }
        ],
        "declared_payload_members": [],
        "error_memory_intake": [],
    }
    hint = {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "patch_name": PATCH_NAME,
        "feature_id": FEATURE_ID,
        "feature_title": "Patch Provenance and Receiver Contract",
        "primary_box": "kanda_reasoner_app/patch_governance/delivery_provenance_contract.py",
        "box_type": "Patch metadata provenance and receiver proof",
        "validated_files": [payload_path],
        "generated_files": ["project_validation_evidence/fixture.txt"],
        "protected_paths": ["project_freeze_after_update/frozen_features_memory/"],
        "do_not_regress_rules": ["Receiver proof remains fail closed."],
        "validation_evidence_summary": f"VALIDATION OK: {FEATURE_ID}\nSTATUS: IN_SYNC",
        "known_warnings": "Fixture only.",
        "planned_next_step": "Validate fixture.",
        "notes": "Fixture only.",
        "freeze_readiness": "pre_validation_hint",
        "requires_user_validation": True,
        "source_patch_zip": ZIP_NAME,
        "patch_provenance_required": True,
        "delivery_manifest_name": DELIVERY_NAME,
        "patch_trace_name": TRACE_NAME,
    }
    delivery = {
        "schema_version": "2.0",
        "kind": "kanda_patch_delivery_manifest",
        "feature_id": FEATURE_ID,
        "patch_name": PATCH_NAME,
        "zip_name": ZIP_NAME,
        "zip_purpose": "Validate source-patch provenance and receiver proof.",
        "zip_placement_path": "<project_drive>:/" + ZIP_NAME,
        "what_zip_is": "A bounded source patch fixture.",
        "what_zip_is_not": "It is not an automatic freeze or Error Memory write.",
        "target_box": "kanda_reasoner_app/patch_governance",
        "files_changed": [payload_path],
        "allowed_write_paths": [payload_path],
        "forbidden_write_paths": list(FORBIDDEN_PATHS),
        "forbidden_boxes": list(FORBIDDEN_BOXES),
        "generated_vs_canonical_status": "Payload is canonical fixture source; root JSON is release metadata.",
        "install_commands": ["Run INSTALL.ps1 -ProjectRoot <project_root>."],
        "validation_commands": ["Run VALIDATE.ps1 -ProjectRoot <project_root>."],
        "expected_validation_markers": list(MARKERS),
        "receiver_contract": {
            "classification": "SOURCE_PATCH",
            "actual_receiver_path_or_action": "INSTALL.ps1 applies INSTALL_MANIFEST.json payload to the explicitly selected self-hosting Project.",
            "installer_stages_to_receiver": True,
            "manual_paste_required": False,
            "storage_only_helper": False,
            "proof_artifacts": [INSTALL_NAME, "INSTALL.ps1"],
        },
        "freeze_intake": {
            "classification": "FREEZE_HINT_INTAKE",
            "actual_receiver_path_or_action": "PREPARE_FREEZE.ps1 stages the validated sidecar into the selected Project Support freeze_hint_intake root.",
            "installer_stages_to_receiver": False,
            "manual_paste_required": False,
            "storage_only_helper": False,
            "proof_artifacts": [HINT_NAME, "PREPARE_FREEZE.ps1"],
        },
        "error_memory_intake": {
            "status": "NOT_APPLICABLE",
            "reason": "The fixture does not correct a durable implementation error.",
        },
        "post_validation_steps": ["Prepare Freeze only after complete local validation."],
        "beginner_do_not_do": ["Do not treat root metadata as installed source."],
    }

    install_raw = _json_bytes(install)
    hint_raw = _json_bytes(hint)
    delivery_raw = _json_bytes(delivery)
    trace = {
        "schema_version": "2.0",
        "kind": "kanda_patch_trace",
        "feature_id": FEATURE_ID,
        "patch_name": PATCH_NAME,
        "router_bridge_used": "pre_output_contract_gates",
        "prompt_paths_loaded": list(PROMPTS),
        "source_files_inspected": [payload_path],
        "source_baselines": [
            {
                "path": payload_path,
                "operation": "replace",
                "baseline_sha256": baseline_hash,
                "installed_sha256": installed_hash,
            }
        ],
        "target_box": "kanda_reasoner_app/patch_governance",
        "forbidden_boxes": list(FORBIDDEN_BOXES),
        "allowed_write_paths": [payload_path],
        "forbidden_write_paths": list(FORBIDDEN_PATHS),
        "files_changed": [payload_path],
        "validation_commands": delivery["validation_commands"],
        "validation_markers": delivery["expected_validation_markers"],
        "delivery_manifest_sha256": _sha256(delivery_raw),
        "install_manifest_sha256": _sha256(install_raw),
        "freeze_hint_sha256": _sha256(hint_raw),
    }
    return {
        INSTALL_NAME: install_raw,
        HINT_NAME: hint_raw,
        DELIVERY_NAME: delivery_raw,
        TRACE_NAME: _json_bytes(trace),
        "INSTALL.ps1": render_installer_template(
            project_root_placeholder="<PROJECT_ROOT>",
            patch_name=PATCH_NAME,
            payload_folder="payload",
        ).encode("utf-8"),
        "VALIDATE.ps1": b"# fixture validator\n",
        "PREPARE_FREEZE.ps1": b"# fixture freeze preparation\n",
        "CHECK_PACKAGE.ps1": b"# fixture package check\n",
        "payload/" + payload_path: payload_bytes,
    }


def _write_zip(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)


def _mutate_json_member(
    members: dict[str, bytes],
    member: str,
    mutator: Callable[[dict[str, Any]], None],
    *,
    refresh_trace_hashes: bool,
) -> dict[str, bytes]:
    changed = dict(members)
    payload = json.loads(changed[member].decode("utf-8"))
    mutator(payload)
    changed[member] = _json_bytes(payload)
    if refresh_trace_hashes:
        trace = json.loads(changed[TRACE_NAME].decode("utf-8"))
        trace["delivery_manifest_sha256"] = _sha256(changed[DELIVERY_NAME])
        trace["install_manifest_sha256"] = _sha256(changed[INSTALL_NAME])
        trace["freeze_hint_sha256"] = _sha256(changed[HINT_NAME])
        changed[TRACE_NAME] = _json_bytes(trace)
    return changed


def _expect_rejected(path: Path, expected_fragment: str) -> None:
    try:
        validate_patch_zip(path)
    except PatchZipContractError as exc:
        if expected_fragment not in str(exc):
            raise AssertionError(f"Unexpected rejection: {exc}") from exc
        return
    raise AssertionError("Invalid patch provenance fixture was accepted")


def _validate_schema_files(project_root: Path) -> None:
    delivery_schema = json.loads(
        (project_root / "kanda_reasoner_app/patch_governance/KANDA_PATCH_DELIVERY_MANIFEST.schema.json").read_text(encoding="utf-8")
    )
    trace_schema = json.loads(
        (project_root / "kanda_reasoner_app/patch_governance/KANDA_PATCH_TRACE.schema.json").read_text(encoding="utf-8")
    )
    if set(delivery_schema.get("required", [])) != {
        "schema_version", "kind", "feature_id", "patch_name", "zip_name",
        "zip_purpose", "zip_placement_path", "what_zip_is", "what_zip_is_not",
        "target_box", "files_changed", "allowed_write_paths", "forbidden_write_paths",
        "forbidden_boxes", "generated_vs_canonical_status", "install_commands",
        "validation_commands", "expected_validation_markers", "receiver_contract",
        "freeze_intake", "error_memory_intake", "post_validation_steps",
        "beginner_do_not_do",
    }:
        raise AssertionError("Delivery schema required fields drifted")
    if "source_baselines" not in set(trace_schema.get("required", [])):
        raise AssertionError("Trace schema lacks source baseline provenance")
    print("PATCH_DELIVERY_MANIFEST_SCHEMA_ALIGNED: PASS")
    print("PATCH_TRACE_SCHEMA_ALIGNED: PASS")


def _validate_module_sizes(project_root: Path) -> None:
    python_files = [
        "kanda_reasoner_app/patch_governance/delivery_provenance_contract.py",
        "kanda_reasoner_app/patch_governance/models.py",
        "kanda_reasoner_app/patch_governance/validator.py",
        "tools/validate_patch_provenance_receiver_contract_v1.py",
    ]
    for relative in python_files:
        count = len((project_root / relative).read_text(encoding="utf-8").splitlines())
        if count < 101 or count > 499:
            raise AssertionError(f"MODULE_SIZE_INVALID: {relative}: {count}")
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    _validate_schema_files(project_root)
    _validate_module_sizes(project_root)

    with tempfile.TemporaryDirectory(prefix="kanda_patch_provenance_") as temp_text:
        temp = Path(temp_text)
        members = _fixture_payload()
        valid_zip = temp / ZIP_NAME
        _write_zip(valid_zip, members)
        report = validate_patch_zip(valid_zip)
        if report.get("patch_provenance_contract") is not True:
            raise AssertionError("Patch provenance contract was not reported")
        if report.get("receiver_classification") != "SOURCE_PATCH":
            raise AssertionError("Source patch receiver was not reported")
        print("ZIP CONTRACT: PASS")
        print("PATCH_PROVENANCE_REQUIRED: PASS")
        print("PATCH_IDENTITY_CROSSCHECK: PASS")
        print("PATCH_CHANGED_FILE_SET_RECONCILED: PASS")
        print("PATCH_SOURCE_BASELINE_PROVENANCE: PASS")
        print("SOURCE_PATCH_RECEIVER_PROOF: PASS")
        print("FREEZE_HINT_RECEIVER_PROOF: PASS")

        ambiguous = _mutate_json_member(
            members,
            DELIVERY_NAME,
            lambda payload: payload["receiver_contract"].update(
                {"classification": "STORAGE_ONLY_MANUAL_HELPER"}
            ),
            refresh_trace_hashes=True,
        )
        ambiguous_zip = temp / "ambiguous.zip"
        ambiguous[DELIVERY_NAME] = ambiguous[DELIVERY_NAME].replace(
            ZIP_NAME.encode("utf-8"), b"ambiguous.zip"
        )
        trace = json.loads(ambiguous[TRACE_NAME].decode("utf-8"))
        trace["delivery_manifest_sha256"] = _sha256(ambiguous[DELIVERY_NAME])
        ambiguous[TRACE_NAME] = _json_bytes(trace)
        hint = json.loads(ambiguous[HINT_NAME].decode("utf-8"))
        hint["source_patch_zip"] = "ambiguous.zip"
        hint["patch_name"] = "ambiguous"
        ambiguous[HINT_NAME] = _json_bytes(hint)
        install = json.loads(ambiguous[INSTALL_NAME].decode("utf-8"))
        install["patch_name"] = "ambiguous"
        ambiguous[INSTALL_NAME] = _json_bytes(install)
        delivery = json.loads(ambiguous[DELIVERY_NAME].decode("utf-8"))
        delivery["patch_name"] = "ambiguous"
        delivery["zip_name"] = "ambiguous.zip"
        ambiguous[DELIVERY_NAME] = _json_bytes(delivery)
        trace = json.loads(ambiguous[TRACE_NAME].decode("utf-8"))
        trace["patch_name"] = "ambiguous"
        trace["delivery_manifest_sha256"] = _sha256(ambiguous[DELIVERY_NAME])
        trace["install_manifest_sha256"] = _sha256(ambiguous[INSTALL_NAME])
        trace["freeze_hint_sha256"] = _sha256(ambiguous[HINT_NAME])
        ambiguous[TRACE_NAME] = _json_bytes(trace)
        _write_zip(ambiguous_zip, ambiguous)
        _expect_rejected(ambiguous_zip, "PATCH_RECEIVER_CLASSIFICATION_MISMATCH")
        print("PATCH_RECEIVER_AMBIGUITY_REJECTED: PASS")

        tampered = dict(members)
        delivery = json.loads(tampered[DELIVERY_NAME].decode("utf-8"))
        delivery["zip_purpose"] = "Tampered after trace creation."
        tampered[DELIVERY_NAME] = _json_bytes(delivery)
        tampered_zip = temp / ZIP_NAME
        _write_zip(tampered_zip, tampered)
        _expect_rejected(tampered_zip, "PATCH_TRACE_HASH_MISMATCH")
        print("PATCH_TRACE_TAMPER_REJECTED: PASS")

        legacy = dict(members)
        legacy.pop(DELIVERY_NAME)
        legacy.pop(TRACE_NAME)
        hint = json.loads(legacy[HINT_NAME].decode("utf-8"))
        hint.pop("patch_provenance_required")
        hint.pop("delivery_manifest_name")
        hint.pop("patch_trace_name")
        legacy[HINT_NAME] = _json_bytes(hint)
        legacy_zip = temp / "legacy.zip"
        hint["patch_name"] = "legacy"
        hint["source_patch_zip"] = "legacy.zip"
        legacy[HINT_NAME] = _json_bytes(hint)
        install = json.loads(legacy[INSTALL_NAME].decode("utf-8"))
        install["patch_name"] = "legacy"
        legacy[INSTALL_NAME] = _json_bytes(install)
        _write_zip(legacy_zip, legacy)
        legacy_report = validate_patch_zip(legacy_zip)
        if legacy_report.get("patch_provenance_contract") is not False:
            raise AssertionError("Legacy compatibility report is incorrect")
        print("PATCH_LEGACY_COMPATIBILITY_PRESERVED: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
