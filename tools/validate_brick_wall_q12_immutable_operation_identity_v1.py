"""Validate Brick Wall Q12 immutable operation identity enforcement."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import ntpath
import re
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q12-immutable-operation-identity-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = (
    PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = (
    PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
COMPANION_REL = (
    PLIB / "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/"
    "governed_architecture_companion_handoff.md"
)
Q11_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py"
)
Q12_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q12_immutable_operation_identity_v1.py"
)
BRICK_MARKERS = (
    "### Immutable operation identity (Q12)",
    "IMMUTABLE OPERATION IDENTITY RECORD",
    "operation required YES/NO",
    "Operation ID/type",
    "feature/patch identity",
    "source fingerprints",
    "lifecycle generation",
    "transaction applicable/ID",
    "Decision: COMPLETE/NOT_APPLICABLE/BLOCKED",
    "proceed to Q13 YES/NO",
    "may begin coding NO",
    "Any identity mismatch invalidates Q13 authority",
)
BRIDGE_MARKERS = (
    "## Immutable operation identity gate (Q12)",
    "Q12 immutable operation identity record complete: YES / NO",
    "Operation identity decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "Current operation ID:",
    "Current feature or patch identity:",
    "Current lifecycle generation:",
    "Current transaction ID or N/A:",
    "May proceed to Q13 write authorization gate: YES / NO",
    "## Immutable operation identity bridge",
    "IMMUTABLE OPERATION IDENTITY RECORD",
    "May implement: NO",
)
COMPANION_MARKERS = (
    "Every card identity must bind:",
    "current operation identity, when applicable",
    "current transaction identity, when applicable",
    "A result from an old Project root, old target, old source hash, old operation, old transaction, or old lifecycle generation must fail closed.",
    "Q12 operation identity:",
)
RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "operation_required",
    "no_operation_evidence",
    "operations",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q13",
    "may_begin_coding",
)
OPERATION_FIELDS = (
    "operation_id",
    "operation_type",
    "feature_id",
    "feature_identity_status",
    "tool_root",
    "active_project_root",
    "target_relative_paths",
    "source_fingerprints",
    "lifecycle_generation",
    "transaction_applicable",
    "transaction_id",
    "identity_owner",
    "immutable_fields",
    "identity_established_before_downstream_work",
    "target_containment_verified",
    "current_root_matches",
    "current_target_set_matches",
    "current_fingerprints_match",
    "current_generation_matches",
    "current_operation_id_matches",
    "current_transaction_matches",
    "stale_result_rejection",
    "mismatch_invalidates_authority",
    "self_hosting_logical_separation_preserved",
    "tests",
)
IMMUTABLE_FIELDS = {
    "tool_root",
    "active_project_root",
    "target_relative_paths",
    "source_fingerprints",
    "lifecycle_generation",
    "operation_id",
    "feature_id",
    "transaction_id",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{label}: FAIL{suffix}")
    print(f"{label}: PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def _windows_abs(value: object) -> bool:
    return _nonempty(value) and ntpath.isabs(str(value))


def _safe_relative(value: object) -> bool:
    if not _nonempty(value):
        return False
    normalized = str(value).replace("/", "\\")
    return not ntpath.isabs(normalized) and ".." not in normalized.split("\\")


def _require_fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _validate_operation(operation: Mapping[str, object]) -> None:
    _require_fields(operation, OPERATION_FIELDS)
    for field in (
        "operation_id",
        "operation_type",
        "feature_id",
        "identity_owner",
        "lifecycle_generation",
    ):
        if not _nonempty(operation[field]):
            raise AssertionError(f"empty operation field: {field}")
    if operation["feature_identity_status"] not in {
        "NEW_UNCONSUMED",
        "CURRENT_UNCONSUMED",
        "DISTINCT_REPAIR",
    }:
        raise AssertionError("invalid or consumed feature identity")
    if not _windows_abs(operation["tool_root"]):
        raise AssertionError("Tool root is not absolute")
    if not _windows_abs(operation["active_project_root"]):
        raise AssertionError("Active Project root is not absolute")
    targets = _text_list(operation["target_relative_paths"])
    if not targets or any(not _safe_relative(target) for target in targets):
        raise AssertionError("unsafe or empty target-relative paths")
    if len(set(targets)) != len(targets):
        raise AssertionError("duplicate target-relative path")
    fingerprints = operation["source_fingerprints"]
    if not isinstance(fingerprints, Mapping):
        raise AssertionError("source fingerprints must be a mapping")
    if set(fingerprints) != set(targets):
        raise AssertionError("target and fingerprint sets differ")
    for target, fingerprint in fingerprints.items():
        if not isinstance(target, str) or not isinstance(fingerprint, str):
            raise AssertionError("invalid fingerprint entry")
        if not HEX64.fullmatch(fingerprint.lower()):
            raise AssertionError("invalid source fingerprint")
    immutable = set(_text_list(operation["immutable_fields"]))
    if not IMMUTABLE_FIELDS.issubset(immutable):
        raise AssertionError("immutable identity field set incomplete")
    transaction_applicable = operation["transaction_applicable"]
    if not isinstance(transaction_applicable, bool):
        raise AssertionError("transaction applicability must be boolean")
    transaction_id = operation["transaction_id"]
    transaction_current = operation["current_transaction_matches"]
    if transaction_applicable:
        if not _nonempty(transaction_id) or transaction_current is not True:
            raise AssertionError("applicable transaction identity is incomplete")
    else:
        if transaction_id not in (None, "", "N/A"):
            raise AssertionError("non-applicable transaction has an ID")
        if transaction_current not in (None, True):
            raise AssertionError("non-applicable transaction has mismatch state")
    required_true = (
        "identity_established_before_downstream_work",
        "target_containment_verified",
        "current_root_matches",
        "current_target_set_matches",
        "current_fingerprints_match",
        "current_generation_matches",
        "current_operation_id_matches",
        "stale_result_rejection",
        "mismatch_invalidates_authority",
        "self_hosting_logical_separation_preserved",
    )
    for field in required_true:
        if operation[field] is not True:
            raise AssertionError(f"operation identity gate failed: {field}")
    if not _text_list(operation["tests"]):
        raise AssertionError("operation identity lacks focused tests")


def validate_record(record: Mapping[str, object]) -> None:
    _require_fields(record, RECORD_FIELDS)
    if not _nonempty(record["identity_basis"]):
        raise AssertionError("identity basis is empty")
    if not _nonempty(record["primary_box"]):
        raise AssertionError("primary box is empty")
    if not isinstance(record["operation_required"], bool):
        raise AssertionError("operation_required must be boolean")
    if _text_list(record["unresolved_fields"]):
        raise AssertionError("operation identity has unresolved fields")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q12 may not authorize coding")
    operations = record["operations"]
    if not isinstance(operations, list):
        raise AssertionError("operations must be a list")
    if record["operation_required"]:
        if _text_list(record["no_operation_evidence"]):
            raise AssertionError("required operation contains no-operation evidence")
        if not operations:
            raise AssertionError("required operation record is empty")
        ids: set[str] = set()
        for operation in operations:
            if not isinstance(operation, Mapping):
                raise AssertionError("operation entry must be a mapping")
            _validate_operation(operation)
            operation_id = str(operation["operation_id"])
            if operation_id in ids:
                raise AssertionError("duplicate operation ID")
            ids.add(operation_id)
        if record["decision"] != "COMPLETE":
            raise AssertionError("required operation decision must be COMPLETE")
        if record["may_proceed_to_q13"] is not True:
            raise AssertionError("complete Q12 must proceed to Q13")
    else:
        if not _text_list(record["no_operation_evidence"]):
            raise AssertionError("no-operation record lacks evidence")
        if operations:
            raise AssertionError("no-operation record contains operation state")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("no-operation decision must be NOT_APPLICABLE")
        if record["may_proceed_to_q13"] is not True:
            raise AssertionError("not-applicable Q12 must proceed to Q13")


def _valid_operation() -> dict[str, object]:
    targets = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md",
        "tools/validate_brick_wall_q12_immutable_operation_identity_v1.py",
    ]
    return {
        "operation_id": "q12-operation-20260715-001",
        "operation_type": "prompt-library governance repair",
        "feature_id": FEATURE_ID,
        "feature_identity_status": "NEW_UNCONSUMED",
        "tool_root": r"E:\kanda_reasoner",
        "active_project_root": r"E:\kanda_reasoner",
        "target_relative_paths": targets,
        "source_fingerprints": {target: "a" * 64 for target in targets},
        "lifecycle_generation": "q12-generation-1",
        "transaction_applicable": False,
        "transaction_id": "N/A",
        "identity_owner": "Brick Wall Q12 operation record",
        "immutable_fields": sorted(IMMUTABLE_FIELDS),
        "identity_established_before_downstream_work": True,
        "target_containment_verified": True,
        "current_root_matches": True,
        "current_target_set_matches": True,
        "current_fingerprints_match": True,
        "current_generation_matches": True,
        "current_operation_id_matches": True,
        "current_transaction_matches": None,
        "stale_result_rejection": True,
        "mismatch_invalidates_authority": True,
        "self_hosting_logical_separation_preserved": True,
        "tests": ["immutable identity positive and negative matrix"],
    }


def _valid_required() -> dict[str, object]:
    return {
        "identity_basis": "Current post-Q11 exact source and Q12 release identity",
        "primary_box": "Prompt library governance",
        "operation_required": True,
        "no_operation_evidence": [],
        "operations": [_valid_operation()],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q13": True,
        "may_begin_coding": False,
    }


def _valid_not_applicable() -> dict[str, object]:
    return {
        "identity_basis": "Current explanation-only task",
        "primary_box": "No source mutation",
        "operation_required": False,
        "no_operation_evidence": [
            "No governed source mutation, async handoff, patch, transaction, or freeze operation"
        ],
        "operations": [],
        "unresolved_fields": [],
        "decision": "NOT_APPLICABLE",
        "may_proceed_to_q13": True,
        "may_begin_coding": False,
    }


def _expect_rejected(label: str, mutate) -> None:
    record = _valid_required()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        print(f"{label}: PASS")
        return
    raise AssertionError(f"{label}: FAIL - invalid record accepted")


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    companion = _read(root / COMPANION_REL)
    brick_meta = _load_json(root / BRICK_META_REL)
    bridge_meta = _load_json(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q12_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q12_ROUTER_BRIDGE_CONTRACT")
    _require(companion, COMPANION_MARKERS, "Q12_EXISTING_IDENTITY_OWNER_REUSED")
    _gate("Q12_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 2))
    _gate("Q12_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (2, 6))
    for label, metadata in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = metadata.get("source_stage")
        updated = metadata.get("updated_for")
        _gate(
            "Q12_METADATA_ALIGNMENT",
            _nonempty(stage) and stage == updated,
            label,
        )
    q11 = _read(root / Q11_VALIDATOR_REL)
    _gate(
        "Q11_FORWARD_COMPATIBLE_METADATA_REPAIR",
        "_nonempty(stage) and stage == updated and stage == FEATURE_ID," not in q11
        and "_nonempty(stage) and stage == updated," in q11,
    )
    for relative in (BRICK_REL, BRIDGE_REL, Q11_VALIDATOR_REL, Q12_VALIDATOR_REL):
        lines = len(_read(root / relative).splitlines())
        _gate("Q12_MODULE_SIZE", lines <= 500, f"{relative}={lines}")


def validate_semantics() -> None:
    validate_record(_valid_required())
    print("Q12_REQUIRED_OPERATION_RECORD_ACCEPTED: PASS")
    validate_record(_valid_not_applicable())
    print("Q12_NOT_APPLICABLE_RECORD_ACCEPTED: PASS")
    cases = [
        ("Q12_NEGATIVE_EMPTY_OPERATION_SET", lambda r: r.update(operations=[])),
        ("Q12_NEGATIVE_DUPLICATE_OPERATION_ID", lambda r: r.update(operations=[_valid_operation(), _valid_operation()])),
        ("Q12_NEGATIVE_REUSED_CONSUMED_FEATURE_ID", lambda r: r["operations"][0].update(feature_identity_status="REUSED_CONSUMED")),
        ("Q12_NEGATIVE_RELATIVE_TOOL_ROOT", lambda r: r["operations"][0].update(tool_root="kanda_reasoner")),
        ("Q12_NEGATIVE_RELATIVE_PROJECT_ROOT", lambda r: r["operations"][0].update(active_project_root="project")),
        ("Q12_NEGATIVE_ABSOLUTE_TARGET", lambda r: r["operations"][0].update(target_relative_paths=[r"E:\bad.py"], source_fingerprints={r"E:\bad.py": "a" * 64})),
        ("Q12_NEGATIVE_TARGET_TRAVERSAL", lambda r: r["operations"][0].update(target_relative_paths=[r"..\bad.py"], source_fingerprints={r"..\bad.py": "a" * 64})),
        ("Q12_NEGATIVE_FINGERPRINT_SET_MISMATCH", lambda r: r["operations"][0].update(source_fingerprints={})),
        ("Q12_NEGATIVE_INVALID_FINGERPRINT", lambda r: r["operations"][0].update(source_fingerprints={target: "bad" for target in r["operations"][0]["target_relative_paths"]})),
        ("Q12_NEGATIVE_MISSING_IMMUTABLE_FIELD", lambda r: r["operations"][0].update(immutable_fields=["operation_id"])),
        ("Q12_NEGATIVE_TRANSACTION_ID_MISSING", lambda r: r["operations"][0].update(transaction_applicable=True, transaction_id="", current_transaction_matches=True)),
        ("Q12_NEGATIVE_UNEXPECTED_TRANSACTION_ID", lambda r: r["operations"][0].update(transaction_id="tx-1")),
        ("Q12_NEGATIVE_IDENTITY_ESTABLISHED_LATE", lambda r: r["operations"][0].update(identity_established_before_downstream_work=False)),
        ("Q12_NEGATIVE_TARGET_CONTAINMENT", lambda r: r["operations"][0].update(target_containment_verified=False)),
        ("Q12_NEGATIVE_ROOT_MISMATCH", lambda r: r["operations"][0].update(current_root_matches=False)),
        ("Q12_NEGATIVE_TARGET_SET_MISMATCH", lambda r: r["operations"][0].update(current_target_set_matches=False)),
        ("Q12_NEGATIVE_FINGERPRINT_MISMATCH", lambda r: r["operations"][0].update(current_fingerprints_match=False)),
        ("Q12_NEGATIVE_GENERATION_MISMATCH", lambda r: r["operations"][0].update(current_generation_matches=False)),
        ("Q12_NEGATIVE_OPERATION_ID_MISMATCH", lambda r: r["operations"][0].update(current_operation_id_matches=False)),
        ("Q12_NEGATIVE_STALE_RESULT_ACCEPTED", lambda r: r["operations"][0].update(stale_result_rejection=False)),
        ("Q12_NEGATIVE_MISMATCH_AUTHORITY_RETAINED", lambda r: r["operations"][0].update(mismatch_invalidates_authority=False)),
        ("Q12_NEGATIVE_SELF_HOSTING_COLLAPSE", lambda r: r["operations"][0].update(self_hosting_logical_separation_preserved=False)),
        ("Q12_NEGATIVE_UNRESOLVED_FIELD", lambda r: r.update(unresolved_fields=["transaction identity"])),
        ("Q12_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
    ]
    for label, mutate in cases:
        _expect_rejected(label, mutate)
    invalid_na = _valid_not_applicable()
    invalid_na["no_operation_evidence"] = []
    try:
        validate_record(invalid_na)
    except AssertionError:
        print("Q12_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: PASS")
    else:
        raise AssertionError("Q12_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: FAIL")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_source(root)
    validate_semantics()
    print("Q12_IMMUTABLE_OPERATION_IDENTITY_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
