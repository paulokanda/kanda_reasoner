# project-path: kanda_reasoner_app/patch_governance/delivery_provenance_contract.py
"""Patch delivery provenance and receiver proof for installable KANDA ZIPs.

This module is a bounded companion to the canonical ZIP member validator.  It
validates root release metadata only; it never extracts archives, installs
payload files, chooses a Project, or grants write authority.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping, Sequence
import zipfile

__all__ = [
    "DELIVERY_MANIFEST_FILENAME",
    "PATCH_TRACE_FILENAME",
    "DeliveryProvenanceContractError",
    "DeliveryProvenanceReport",
    "validate_delivery_provenance_contract",
]

DELIVERY_MANIFEST_FILENAME = "KANDA_PATCH_DELIVERY_MANIFEST.json"
PATCH_TRACE_FILENAME = "KANDA_PATCH_TRACE.json"
INSTALL_MANIFEST_FILENAME = "INSTALL_MANIFEST.json"
FREEZE_HINT_FILENAME = "KANDA_FREEZE_HINT.json"
SCHEMA_VERSION = "2.0"
DELIVERY_KIND = "kanda_patch_delivery_manifest"
TRACE_KIND = "kanda_patch_trace"
HEX_64 = re.compile(r"^[0-9a-f]{64}$")

RECEIVER_CLASSIFICATIONS = {
    "SOURCE_PATCH",
    "FREEZE_HINT_INTAKE",
    "MANUAL_FREEZE_FORM_RECEIVER",
    "ERROR_MEMORY_AI_ASSISTED_INTAKE",
    "STORAGE_ONLY_MANUAL_HELPER",
}

DELIVERY_REQUIRED_FIELDS = (
    "schema_version",
    "kind",
    "feature_id",
    "patch_name",
    "zip_name",
    "zip_purpose",
    "zip_placement_path",
    "what_zip_is",
    "what_zip_is_not",
    "target_box",
    "files_changed",
    "allowed_write_paths",
    "forbidden_write_paths",
    "forbidden_boxes",
    "generated_vs_canonical_status",
    "install_commands",
    "validation_commands",
    "expected_validation_markers",
    "receiver_contract",
    "freeze_intake",
    "error_memory_intake",
    "post_validation_steps",
    "beginner_do_not_do",
)

TRACE_REQUIRED_FIELDS = (
    "schema_version",
    "kind",
    "feature_id",
    "patch_name",
    "router_bridge_used",
    "prompt_paths_loaded",
    "source_files_inspected",
    "source_baselines",
    "target_box",
    "forbidden_boxes",
    "allowed_write_paths",
    "forbidden_write_paths",
    "files_changed",
    "validation_commands",
    "validation_markers",
    "delivery_manifest_sha256",
    "install_manifest_sha256",
    "freeze_hint_sha256",
)


class DeliveryProvenanceContractError(ValueError):
    """Raised when release provenance or receiver proof is incomplete."""


@dataclass(frozen=True)
class DeliveryProvenanceReport:
    """Read-only summary of one validated patch provenance envelope."""

    feature_id: str
    patch_name: str
    zip_name: str
    receiver_classification: str
    files_changed: tuple[str, ...]
    delivery_manifest_sha256: str
    trace_sha256: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable copy of the report."""
        return {
            "feature_id": self.feature_id,
            "patch_name": self.patch_name,
            "zip_name": self.zip_name,
            "receiver_classification": self.receiver_classification,
            "files_changed": list(self.files_changed),
            "delivery_manifest_sha256": self.delivery_manifest_sha256,
            "trace_sha256": self.trace_sha256,
        }


def _fail(code: str, detail: str) -> None:
    raise DeliveryProvenanceContractError(f"{code}: {detail}")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_root_json(
    archive: zipfile.ZipFile,
    filename: str,
    *,
    required: bool,
) -> tuple[dict[str, Any] | None, bytes | None]:
    names = {info.orig_filename for info in archive.infolist() if not info.is_dir()}
    if filename not in names:
        if required:
            _fail("PATCH_PROVENANCE_ROOT_MEMBER_MISSING", filename)
        return None, None
    raw = archive.read(filename)
    try:
        loaded = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail("PATCH_PROVENANCE_JSON_INVALID", f"{filename}: {exc}")
    if not isinstance(loaded, dict):
        _fail("PATCH_PROVENANCE_JSON_ROOT_INVALID", filename)
    return dict(loaded), raw


def _nonempty_text(value: Any, *, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        _fail("PATCH_PROVENANCE_FIELD_EMPTY", field)
    return text


def _string_list(value: Any, *, field: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        _fail("PATCH_PROVENANCE_LIST_INVALID", field)
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        text = _nonempty_text(item, field=f"{field}[{index}]")
        normalized = text.replace("\\", "/")
        if normalized in seen:
            _fail("PATCH_PROVENANCE_LIST_DUPLICATE", f"{field}: {normalized}")
        seen.add(normalized)
        result.append(normalized)
    if not result and not allow_empty:
        _fail("PATCH_PROVENANCE_LIST_EMPTY", field)
    return result


def _require_fields(payload: Mapping[str, Any], fields: Sequence[str], *, owner: str) -> None:
    missing = [field for field in fields if field not in payload]
    if missing:
        _fail("PATCH_PROVENANCE_FIELDS_MISSING", f"{owner}: {', '.join(missing)}")


def _validate_relative_project_paths(paths: Sequence[str], *, field: str) -> None:
    for path in paths:
        pure = PurePosixPath(path)
        if pure.is_absolute() or not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
            _fail("PATCH_PROVENANCE_PROJECT_PATH_INVALID", f"{field}: {path}")
        if re.match(r"^[A-Za-z]:", path) or path.startswith("//"):
            _fail("PATCH_PROVENANCE_PROJECT_PATH_INVALID", f"{field}: {path}")


def _validate_receiver_contract(
    contract: Any,
    *,
    owner: str,
    expected_classification: str,
    expected_installer_stages: bool,
    expected_manual_paste: bool,
    expected_storage_only: bool,
    archive_names: set[str],
) -> dict[str, Any]:
    if not isinstance(contract, Mapping):
        _fail("PATCH_RECEIVER_CONTRACT_INVALID", owner)
    classification = _nonempty_text(contract.get("classification"), field=f"{owner}.classification")
    if classification not in RECEIVER_CLASSIFICATIONS:
        _fail("PATCH_RECEIVER_CLASSIFICATION_INVALID", f"{owner}: {classification}")
    if classification != expected_classification:
        _fail(
            "PATCH_RECEIVER_CLASSIFICATION_MISMATCH",
            f"{owner}: expected {expected_classification}, got {classification}",
        )
    _nonempty_text(
        contract.get("actual_receiver_path_or_action"),
        field=f"{owner}.actual_receiver_path_or_action",
    )
    booleans = {
        "installer_stages_to_receiver": expected_installer_stages,
        "manual_paste_required": expected_manual_paste,
        "storage_only_helper": expected_storage_only,
    }
    for field, expected in booleans.items():
        value = contract.get(field)
        if not isinstance(value, bool) or value is not expected:
            _fail("PATCH_RECEIVER_BOOLEAN_MISMATCH", f"{owner}.{field}")
    proof = _string_list(contract.get("proof_artifacts"), field=f"{owner}.proof_artifacts")
    missing = [item for item in proof if item not in archive_names]
    if missing:
        _fail("PATCH_RECEIVER_PROOF_ARTIFACT_MISSING", f"{owner}: {', '.join(missing)}")
    return dict(contract)


def _validate_freeze_intake_contract(
    value: Any,
    *,
    archive_names: set[str],
    hint_present: bool,
) -> None:
    if not isinstance(value, Mapping):
        _fail("PATCH_FREEZE_INTAKE_CONTRACT_INVALID", "freeze_intake")
    status = str(value.get("status") or "").strip()
    if not hint_present:
        if status != "NOT_APPLICABLE":
            _fail(
                "PATCH_FREEZE_INTAKE_STATUS_INVALID",
                "Freeze Hint absent; freeze_intake.status must be NOT_APPLICABLE",
            )
        _nonempty_text(value.get("reason"), field="freeze_intake.reason")
        return
    if status and status != "ACTIVE_READY":
        _fail("PATCH_FREEZE_INTAKE_STATUS_INVALID", status)
    _validate_receiver_contract(
        value,
        owner="freeze_intake",
        expected_classification="FREEZE_HINT_INTAKE",
        expected_installer_stages=False,
        expected_manual_paste=False,
        expected_storage_only=False,
        archive_names=archive_names,
    )


def _validate_error_memory_contract(value: Any, *, archive_names: set[str]) -> None:
    if not isinstance(value, Mapping):
        _fail("PATCH_ERROR_MEMORY_CONTRACT_INVALID", "error_memory_intake")
    status = _nonempty_text(value.get("status"), field="error_memory_intake.status")
    if status == "NOT_APPLICABLE":
        _nonempty_text(value.get("reason"), field="error_memory_intake.reason")
        return
    if status != "ACTIVE_READY":
        _fail("PATCH_ERROR_MEMORY_STATUS_INVALID", status)
    _validate_receiver_contract(
        value.get("receiver_contract"),
        owner="error_memory_intake.receiver_contract",
        expected_classification="ERROR_MEMORY_AI_ASSISTED_INTAKE",
        expected_installer_stages=True,
        expected_manual_paste=False,
        expected_storage_only=False,
        archive_names=archive_names,
    )


def _install_file_records(install_manifest: Mapping[str, Any]) -> list[dict[str, str]]:
    files = install_manifest.get("files")
    if not isinstance(files, list) or not files:
        _fail("PATCH_INSTALL_MANIFEST_FILES_INVALID", "files")
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(files):
        if not isinstance(item, Mapping):
            _fail("PATCH_INSTALL_MANIFEST_FILE_INVALID", f"files[{index}]")
        path = _nonempty_text(item.get("path"), field=f"files[{index}].path").replace("\\", "/")
        if path in seen:
            _fail("PATCH_INSTALL_MANIFEST_FILE_DUPLICATE", path)
        seen.add(path)
        operation = _nonempty_text(item.get("operation"), field=f"files[{index}].operation")
        baseline = str(item.get("baseline_sha256") or "").strip().lower()
        installed = _nonempty_text(
            item.get("installed_sha256"),
            field=f"files[{index}].installed_sha256",
        ).lower()
        if operation not in {"add", "replace", "delete"}:
            _fail("PATCH_INSTALL_OPERATION_INVALID", f"{path}: {operation}")
        if operation == "add" and baseline:
            _fail("PATCH_INSTALL_BASELINE_INVALID", f"new file has baseline: {path}")
        if operation in {"replace", "delete"} and not HEX_64.fullmatch(baseline):
            _fail("PATCH_INSTALL_BASELINE_INVALID", path)
        if not HEX_64.fullmatch(installed):
            _fail("PATCH_INSTALL_INSTALLED_HASH_INVALID", path)
        result.append(
            {
                "path": path,
                "operation": operation,
                "baseline_sha256": baseline,
                "installed_sha256": installed,
            }
        )
    _validate_relative_project_paths([item["path"] for item in result], field="install_manifest.files")
    return result


def _trace_baselines(trace: Mapping[str, Any]) -> list[dict[str, str]]:
    raw = trace.get("source_baselines")
    if not isinstance(raw, list) or not raw:
        _fail("PATCH_TRACE_BASELINES_INVALID", "source_baselines")
    result: list[dict[str, str]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            _fail("PATCH_TRACE_BASELINE_INVALID", f"source_baselines[{index}]")
        result.append(
            {
                "path": _nonempty_text(item.get("path"), field=f"source_baselines[{index}].path").replace("\\", "/"),
                "operation": _nonempty_text(item.get("operation"), field=f"source_baselines[{index}].operation"),
                "baseline_sha256": str(item.get("baseline_sha256") or "").strip().lower(),
                "installed_sha256": _nonempty_text(
                    item.get("installed_sha256"),
                    field=f"source_baselines[{index}].installed_sha256",
                ).lower(),
            }
        )
    return result


def _require_equal(left: Any, right: Any, *, code: str, detail: str) -> None:
    if left != right:
        _fail(code, detail)


def validate_delivery_provenance_contract(
    archive: zipfile.ZipFile,
    *,
    actual_zip_name: str,
    freeze_hint: Mapping[str, Any] | None,
    required: bool,
) -> DeliveryProvenanceReport | None:
    """Validate patch provenance and receiver proof inside an already-open ZIP."""
    archive_names = {info.orig_filename for info in archive.infolist() if not info.is_dir()}
    present = DELIVERY_MANIFEST_FILENAME in archive_names or PATCH_TRACE_FILENAME in archive_names
    if not required and not present:
        return None

    delivery, delivery_raw = _load_root_json(archive, DELIVERY_MANIFEST_FILENAME, required=True)
    trace, trace_raw = _load_root_json(archive, PATCH_TRACE_FILENAME, required=True)
    install, install_raw = _load_root_json(archive, INSTALL_MANIFEST_FILENAME, required=True)
    hint, hint_raw = _load_root_json(archive, FREEZE_HINT_FILENAME, required=False)
    assert delivery is not None and delivery_raw is not None
    assert trace is not None and trace_raw is not None
    assert install is not None and install_raw is not None

    _require_fields(delivery, DELIVERY_REQUIRED_FIELDS, owner=DELIVERY_MANIFEST_FILENAME)
    _require_fields(trace, TRACE_REQUIRED_FIELDS, owner=PATCH_TRACE_FILENAME)
    _require_equal(delivery.get("schema_version"), SCHEMA_VERSION, code="PATCH_DELIVERY_SCHEMA_INVALID", detail="schema_version")
    _require_equal(delivery.get("kind"), DELIVERY_KIND, code="PATCH_DELIVERY_KIND_INVALID", detail="kind")
    _require_equal(trace.get("schema_version"), SCHEMA_VERSION, code="PATCH_TRACE_SCHEMA_INVALID", detail="schema_version")
    _require_equal(trace.get("kind"), TRACE_KIND, code="PATCH_TRACE_KIND_INVALID", detail="kind")

    feature_id = _nonempty_text(delivery.get("feature_id"), field="feature_id")
    patch_name = _nonempty_text(delivery.get("patch_name"), field="patch_name")
    zip_name = _nonempty_text(delivery.get("zip_name"), field="zip_name")
    identities = {
        "actual_zip_name": actual_zip_name,
        "delivery.zip_name": zip_name,
        "delivery.patch_name": patch_name,
        "trace.patch_name": trace.get("patch_name"),
        "install.patch_name": install.get("patch_name"),
        "delivery.feature_id": feature_id,
        "trace.feature_id": trace.get("feature_id"),
        "install.feature_id": install.get("feature_id"),
    }
    if hint is not None:
        identities["hint.patch_name"] = hint.get("patch_name")
        identities["hint.feature_id"] = hint.get("feature_id")
    _require_equal(zip_name, actual_zip_name, code="PATCH_ZIP_IDENTITY_MISMATCH", detail=str(identities))
    _require_equal(patch_name, PurePosixPath(actual_zip_name).stem, code="PATCH_NAME_IDENTITY_MISMATCH", detail=str(identities))
    for owner in (trace, install):
        _require_equal(owner.get("feature_id"), feature_id, code="PATCH_FEATURE_ID_MISMATCH", detail=str(identities))
        _require_equal(owner.get("patch_name"), patch_name, code="PATCH_NAME_IDENTITY_MISMATCH", detail=str(identities))
    if hint is not None:
        _require_equal(hint.get("feature_id"), feature_id, code="PATCH_FEATURE_ID_MISMATCH", detail=str(identities))
        _require_equal(hint.get("patch_name"), patch_name, code="PATCH_NAME_IDENTITY_MISMATCH", detail=str(identities))
        if freeze_hint is not None:
            _require_equal(dict(freeze_hint), hint, code="PATCH_FREEZE_HINT_OBJECT_MISMATCH", detail="validator hint differs from archive")
        _require_equal(hint.get("source_patch_zip"), actual_zip_name, code="PATCH_SOURCE_ZIP_MISMATCH", detail="freeze hint")
        if hint.get("patch_provenance_required") is not True:
            _fail("PATCH_PROVENANCE_FLAG_MISSING", "KANDA_FREEZE_HINT.json")
        _require_equal(hint.get("delivery_manifest_name"), DELIVERY_MANIFEST_FILENAME, code="PATCH_PROVENANCE_FILENAME_MISMATCH", detail="delivery manifest")
        _require_equal(hint.get("patch_trace_name"), PATCH_TRACE_FILENAME, code="PATCH_PROVENANCE_FILENAME_MISMATCH", detail="patch trace")

    install_records = _install_file_records(install)
    install_paths = [item["path"] for item in install_records]
    delivery_files = _string_list(delivery.get("files_changed"), field="files_changed")
    allowed_paths = _string_list(delivery.get("allowed_write_paths"), field="allowed_write_paths")
    trace_files = _string_list(trace.get("files_changed"), field="trace.files_changed")
    trace_allowed = _string_list(trace.get("allowed_write_paths"), field="trace.allowed_write_paths")
    _validate_relative_project_paths(delivery_files, field="files_changed")
    _require_equal(delivery_files, install_paths, code="PATCH_CHANGED_FILES_MISMATCH", detail="delivery <> install")
    _require_equal(allowed_paths, install_paths, code="PATCH_ALLOWED_WRITE_PATHS_MISMATCH", detail="delivery <> install")
    _require_equal(trace_files, install_paths, code="PATCH_TRACE_FILES_MISMATCH", detail="trace <> install")
    _require_equal(trace_allowed, install_paths, code="PATCH_TRACE_ALLOWED_PATHS_MISMATCH", detail="trace <> install")
    _require_equal(_trace_baselines(trace), install_records, code="PATCH_SOURCE_BASELINE_PROVENANCE_MISMATCH", detail="trace <> install")

    target_box = _nonempty_text(delivery.get("target_box"), field="target_box")
    _require_equal(trace.get("target_box"), target_box, code="PATCH_TARGET_BOX_MISMATCH", detail="trace <> delivery")
    forbidden_boxes = _string_list(delivery.get("forbidden_boxes"), field="forbidden_boxes")
    forbidden_paths = _string_list(delivery.get("forbidden_write_paths"), field="forbidden_write_paths")
    _require_equal(_string_list(trace.get("forbidden_boxes"), field="trace.forbidden_boxes"), forbidden_boxes, code="PATCH_FORBIDDEN_BOXES_MISMATCH", detail="trace <> delivery")
    _require_equal(_string_list(trace.get("forbidden_write_paths"), field="trace.forbidden_write_paths"), forbidden_paths, code="PATCH_FORBIDDEN_PATHS_MISMATCH", detail="trace <> delivery")

    for field in (
        "zip_purpose",
        "zip_placement_path",
        "what_zip_is",
        "what_zip_is_not",
        "generated_vs_canonical_status",
    ):
        _nonempty_text(delivery.get(field), field=field)
    install_commands = _string_list(delivery.get("install_commands"), field="install_commands")
    validation_commands = _string_list(delivery.get("validation_commands"), field="validation_commands")
    markers = _string_list(delivery.get("expected_validation_markers"), field="expected_validation_markers")
    _string_list(delivery.get("post_validation_steps"), field="post_validation_steps")
    _string_list(delivery.get("beginner_do_not_do"), field="beginner_do_not_do")
    required_markers = {
        "ZIP CONTRACT: PASS",
        f"VALIDATION OK: {feature_id}",
        "STATUS: IN_SYNC",
    }
    if not required_markers.issubset(set(markers)):
        _fail("PATCH_VALIDATION_MARKERS_INCOMPLETE", ", ".join(sorted(required_markers - set(markers))))
    _require_equal(_string_list(trace.get("validation_commands"), field="trace.validation_commands"), validation_commands, code="PATCH_VALIDATION_COMMANDS_MISMATCH", detail="trace <> delivery")
    _require_equal(_string_list(trace.get("validation_markers"), field="trace.validation_markers"), markers, code="PATCH_VALIDATION_MARKERS_MISMATCH", detail="trace <> delivery")
    if not install_commands:
        _fail("PATCH_INSTALL_COMMANDS_EMPTY", "install_commands")

    receiver = _validate_receiver_contract(
        delivery.get("receiver_contract"),
        owner="receiver_contract",
        expected_classification="SOURCE_PATCH",
        expected_installer_stages=True,
        expected_manual_paste=False,
        expected_storage_only=False,
        archive_names=archive_names,
    )
    _validate_freeze_intake_contract(
        delivery.get("freeze_intake"),
        archive_names=archive_names,
        hint_present=hint is not None,
    )
    _validate_error_memory_contract(delivery.get("error_memory_intake"), archive_names=archive_names)

    _require_equal(trace.get("router_bridge_used"), "pre_output_contract_gates", code="PATCH_ROUTER_BRIDGE_MISMATCH", detail="router_bridge_used")
    prompts = _string_list(trace.get("prompt_paths_loaded"), field="prompt_paths_loaded")
    if not any(item.endswith("pre_output_contract_gates.md") for item in prompts):
        _fail("PATCH_PRE_OUTPUT_OWNER_NOT_TRACED", "prompt_paths_loaded")
    inspected = _string_list(trace.get("source_files_inspected"), field="source_files_inspected")
    replacement_paths = {item["path"] for item in install_records if item["operation"] != "add"}
    if not replacement_paths.issubset(set(inspected)):
        _fail("PATCH_REPLACED_SOURCE_NOT_INSPECTED", ", ".join(sorted(replacement_paths - set(inspected))))

    expected_hashes = {
        "delivery_manifest_sha256": _sha256_bytes(delivery_raw),
        "install_manifest_sha256": _sha256_bytes(install_raw),
    }
    for field, expected in expected_hashes.items():
        actual = str(trace.get(field) or "").strip().lower()
        if not HEX_64.fullmatch(actual) or actual != expected:
            _fail("PATCH_TRACE_HASH_MISMATCH", field)
    freeze_hash = str(trace.get("freeze_hint_sha256") or "").strip().lower()
    if hint_raw is None:
        if freeze_hash not in {"", "not_applicable"}:
            _fail("PATCH_TRACE_HASH_MISMATCH", "freeze_hint_sha256")
    else:
        expected_freeze_hash = _sha256_bytes(hint_raw)
        if not HEX_64.fullmatch(freeze_hash) or freeze_hash != expected_freeze_hash:
            _fail("PATCH_TRACE_HASH_MISMATCH", "freeze_hint_sha256")

    return DeliveryProvenanceReport(
        feature_id=feature_id,
        patch_name=patch_name,
        zip_name=zip_name,
        receiver_classification=str(receiver["classification"]),
        files_changed=tuple(install_paths),
        delivery_manifest_sha256=expected_hashes["delivery_manifest_sha256"],
        trace_sha256=_sha256_bytes(trace_raw),
    )
