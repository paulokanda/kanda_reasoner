"""Validate Brick Wall Q13 explicit write authorization enforcement."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import ntpath
import re
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q13-explicit-write-authorization-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
COMPANION_REL = PLIB / "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/governed_architecture_companion_handoff.md"
Q12_VALIDATOR_REL = Path("tools/validate_brick_wall_q12_immutable_operation_identity_v1.py")
Q13_VALIDATOR_REL = Path("tools/validate_brick_wall_q13_explicit_write_authorization_v1.py")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
BRICK_MARKERS = (
    "### Explicit write authorization (Q13)",
    "EXPLICIT WRITE AUTHORIZATION RECORD",
    "writes required YES/NO",
    "Authorization ID",
    "allowed relative paths",
    "authorized write route",
    "approved Preview required/ID/fingerprint",
    "expected source fingerprints",
    "human authorization required/current",
    "Decision: COMPLETE/NOT_APPLICABLE/BLOCKED",
    "proceed to Q14 YES/NO",
    "may begin coding NO",
    "may write source NO",
    "boolean alone never grants mutation authority",
)
BRIDGE_MARKERS = (
    "## Explicit write authorization gate (Q13)",
    "Q13 explicit write authorization record complete: YES / NO",
    "Write authorization decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "Current authorization ID or N/A:",
    "Allowed write paths or N/A:",
    "Approved Preview identity or N/A:",
    "Human authorization current: YES / NO / N/A",
    "May proceed to Q14 immediate freshness gate: YES / NO",
    "May write source: NO",
    "## Explicit write authorization bridge",
    "EXPLICIT WRITE AUTHORIZATION RECORD",
)
COMPANION_MARKERS = (
    "Final coding authorization belongs to Brick Wall",
    "MAY BEGIN CODING: YES / NO",
    "MAY WRITE SOURCE: YES / NO",
    "Q13 write authorization:",
    "Do not implement until Brick Wall concludes:",
)
RECORD_FIELDS = (
    "authorization_basis", "primary_box", "writes_required",
    "no_write_evidence", "authorizations", "unresolved_fields", "decision",
    "may_proceed_to_q14", "may_begin_coding", "may_write_source",
)
AUTH_FIELDS = (
    "authorization_id", "operation_id", "feature_id", "active_project_root",
    "allowed_relative_paths", "authorized_write_route",
    "approved_preview_required", "approved_preview_id",
    "approved_preview_fingerprint", "expected_source_fingerprints",
    "lifecycle_generation", "transaction_applicable", "transaction_id",
    "authorization_owner", "authorization_evidence",
    "human_authorization_required", "human_authorization_current",
    "scope_bounded", "current_operation_matches", "current_project_matches",
    "current_path_set_matches", "current_preview_matches",
    "current_source_fingerprints_match", "current_generation_matches",
    "current_transaction_matches", "invalidation_conditions",
    "authorization_not_expired", "blocked_paths", "tests",
)
REQUIRED_INVALIDATION = {
    "operation_change", "project_change", "path_change", "preview_change",
    "source_fingerprint_change", "generation_change", "transaction_change",
    "human_authorization_withdrawn",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(f"{label}: FAIL" + (f" - {detail}" if detail else ""))
    print(f"{label}: PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [item for item in markers if item not in text]
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


def _safe_relative(value: object) -> bool:
    if not _nonempty(value):
        return False
    normalized = str(value).replace("/", "\\")
    return not ntpath.isabs(normalized) and ".." not in normalized.split("\\")


def _fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _validate_authorization(auth: Mapping[str, object]) -> None:
    _fields(auth, AUTH_FIELDS)
    for field in (
        "authorization_id", "operation_id", "feature_id",
        "active_project_root", "authorized_write_route",
        "lifecycle_generation", "authorization_owner",
    ):
        if not _nonempty(auth[field]):
            raise AssertionError(f"empty authorization field: {field}")
    if not ntpath.isabs(str(auth["active_project_root"])):
        raise AssertionError("Active Project root is not absolute")
    paths = _text_list(auth["allowed_relative_paths"])
    if not paths or any(not _safe_relative(path) for path in paths):
        raise AssertionError("unsafe or empty allowed paths")
    if len(set(paths)) != len(paths):
        raise AssertionError("duplicate allowed path")
    fingerprints = auth["expected_source_fingerprints"]
    if not isinstance(fingerprints, Mapping) or set(fingerprints) != set(paths):
        raise AssertionError("allowed path and fingerprint sets differ")
    if any(not isinstance(value, str) or not HEX64.fullmatch(value.lower()) for value in fingerprints.values()):
        raise AssertionError("invalid source fingerprint")
    if auth["approved_preview_required"] is True:
        if not _nonempty(auth["approved_preview_id"]):
            raise AssertionError("required Preview ID missing")
        preview_hash = auth["approved_preview_fingerprint"]
        if not isinstance(preview_hash, str) or not HEX64.fullmatch(preview_hash.lower()):
            raise AssertionError("required Preview fingerprint missing")
        if auth["current_preview_matches"] is not True:
            raise AssertionError("Preview is not current")
    elif auth["approved_preview_required"] is False:
        if auth["approved_preview_id"] not in (None, "", "N/A"):
            raise AssertionError("non-applicable Preview has identity")
        if auth["approved_preview_fingerprint"] not in (None, "", "N/A"):
            raise AssertionError("non-applicable Preview has fingerprint")
        if auth["current_preview_matches"] not in (None, True):
            raise AssertionError("non-applicable Preview has mismatch")
    else:
        raise AssertionError("Preview applicability must be boolean")
    if auth["transaction_applicable"] is True:
        if not _nonempty(auth["transaction_id"]):
            raise AssertionError("transaction ID missing")
        if auth["current_transaction_matches"] is not True:
            raise AssertionError("transaction is not current")
    elif auth["transaction_applicable"] is False:
        if auth["transaction_id"] not in (None, "", "N/A"):
            raise AssertionError("non-applicable transaction has ID")
        if auth["current_transaction_matches"] not in (None, True):
            raise AssertionError("non-applicable transaction has mismatch")
    else:
        raise AssertionError("transaction applicability must be boolean")
    evidence = _text_list(auth["authorization_evidence"])
    if len(evidence) < 2:
        raise AssertionError("authorization evidence is too weak")
    weak = {"path exists", "helper returned true", "boolean true", "manifest true"}
    if all(item.lower() in weak for item in evidence):
        raise AssertionError("path, helper, manifest, or boolean-only authority")
    if auth["human_authorization_required"] is not True:
        raise AssertionError("governed write must require human authorization")
    required_true = (
        "human_authorization_current", "scope_bounded",
        "current_operation_matches", "current_project_matches",
        "current_path_set_matches", "current_source_fingerprints_match",
        "current_generation_matches", "authorization_not_expired",
    )
    for field in required_true:
        if auth[field] is not True:
            raise AssertionError(f"write authorization failed: {field}")
    invalidation = set(_text_list(auth["invalidation_conditions"]))
    if not REQUIRED_INVALIDATION.issubset(invalidation):
        raise AssertionError("authorization invalidation set incomplete")
    blocked = _text_list(auth["blocked_paths"])
    if not blocked or any(path in blocked for path in paths):
        raise AssertionError("blocked path set is missing or contradictory")
    if not _text_list(auth["tests"]):
        raise AssertionError("write authorization lacks tests")


def validate_record(record: Mapping[str, object]) -> None:
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["authorization_basis"]):
        raise AssertionError("authorization basis is empty")
    if not _nonempty(record["primary_box"]):
        raise AssertionError("primary box is empty")
    if not isinstance(record["writes_required"], bool):
        raise AssertionError("writes_required must be boolean")
    if _text_list(record["unresolved_fields"]):
        raise AssertionError("write authorization has unresolved fields")
    if record["may_begin_coding"] is not False or record["may_write_source"] is not False:
        raise AssertionError("Q13 may not authorize coding or source writing")
    authorizations = record["authorizations"]
    if not isinstance(authorizations, list):
        raise AssertionError("authorizations must be a list")
    if record["writes_required"]:
        if _text_list(record["no_write_evidence"]):
            raise AssertionError("write-required record contains no-write evidence")
        if not authorizations:
            raise AssertionError("write-required authorization set is empty")
        ids: set[str] = set()
        operations: set[str] = set()
        for auth in authorizations:
            if not isinstance(auth, Mapping):
                raise AssertionError("authorization entry must be a mapping")
            _validate_authorization(auth)
            auth_id = str(auth["authorization_id"])
            operation_id = str(auth["operation_id"])
            if auth_id in ids:
                raise AssertionError("duplicate authorization ID")
            if operation_id in operations:
                raise AssertionError("multiple mutable authorities for one operation")
            ids.add(auth_id)
            operations.add(operation_id)
        if record["decision"] != "COMPLETE" or record["may_proceed_to_q14"] is not True:
            raise AssertionError("complete Q13 must proceed to Q14")
    else:
        if not _text_list(record["no_write_evidence"]):
            raise AssertionError("no-write record lacks evidence")
        if authorizations:
            raise AssertionError("no-write record contains authorization state")
        if record["decision"] != "NOT_APPLICABLE" or record["may_proceed_to_q14"] is not True:
            raise AssertionError("not-applicable Q13 must proceed to Q14")


def _valid_auth() -> dict[str, object]:
    paths = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md",
        "tools/validate_brick_wall_q13_explicit_write_authorization_v1.py",
    ]
    return {
        "authorization_id": "q13-auth-20260715-001",
        "operation_id": "q13-operation-20260715-001",
        "feature_id": FEATURE_ID,
        "active_project_root": r"E:\kanda_reasoner",
        "allowed_relative_paths": paths,
        "authorized_write_route": "governed baseline-hash installer",
        "approved_preview_required": False,
        "approved_preview_id": "N/A",
        "approved_preview_fingerprint": "N/A",
        "expected_source_fingerprints": {path: "a" * 64 for path in paths},
        "lifecycle_generation": "q13-generation-1",
        "transaction_applicable": False,
        "transaction_id": "N/A",
        "authorization_owner": "Brick Wall current Q13 decision",
        "authorization_evidence": [
            "User explicitly requested continuation of the Q13 implementation",
            "Q12 immutable operation identity is complete and current",
        ],
        "human_authorization_required": True,
        "human_authorization_current": True,
        "scope_bounded": True,
        "current_operation_matches": True,
        "current_project_matches": True,
        "current_path_set_matches": True,
        "current_preview_matches": None,
        "current_source_fingerprints_match": True,
        "current_generation_matches": True,
        "current_transaction_matches": None,
        "invalidation_conditions": sorted(REQUIRED_INVALIDATION),
        "authorization_not_expired": True,
        "blocked_paths": [
            "kanda_reasoner_app",
            "project_freeze_after_update/frozen_features_memory",
        ],
        "tests": ["Q13 positive and negative write-authorization matrix"],
    }


def _valid_required() -> dict[str, object]:
    return {
        "authorization_basis": "Current Q12 identity and explicit user continuation",
        "primary_box": "Prompt library governance",
        "writes_required": True,
        "no_write_evidence": [],
        "authorizations": [_valid_auth()],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q14": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def _valid_na() -> dict[str, object]:
    return {
        "authorization_basis": "Current explanation-only task",
        "primary_box": "No source mutation",
        "writes_required": False,
        "no_write_evidence": ["No governed mutation or patch delivery is requested"],
        "authorizations": [],
        "unresolved_fields": [],
        "decision": "NOT_APPLICABLE",
        "may_proceed_to_q14": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def _reject(label: str, mutate) -> None:
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
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q13_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q13_ROUTER_BRIDGE_CONTRACT")
    _require(companion, COMPANION_MARKERS, "Q13_EXISTING_AUTHORIZATION_OWNER_REUSED")
    _gate("Q13_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 3))
    _gate("Q13_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (2, 7))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q13_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q12 = _read(root / Q12_VALIDATOR_REL)
    _gate(
        "Q12_FORWARD_COMPATIBLE_METADATA_PRESERVED",
        "Q12_METADATA_ALIGNMENT" in q12
        and "_nonempty(stage) and stage == updated," in q12,
    )
    for rel in (BRICK_REL, BRIDGE_REL, Q12_VALIDATOR_REL, Q13_VALIDATOR_REL):
        lines = len(_read(root / rel).splitlines())
        _gate("Q13_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def validate_semantics() -> None:
    validate_record(_valid_required())
    print("Q13_REQUIRED_WRITE_RECORD_ACCEPTED: PASS")
    validate_record(_valid_na())
    print("Q13_NOT_APPLICABLE_RECORD_ACCEPTED: PASS")
    cases = [
        ("Q13_NEGATIVE_EMPTY_AUTHORIZATION_SET", lambda r: r.update(authorizations=[])),
        ("Q13_NEGATIVE_DUPLICATE_AUTHORIZATION_ID", lambda r: r.update(authorizations=[_valid_auth(), _valid_auth()])),
        ("Q13_NEGATIVE_PATH_ONLY_AUTHORITY", lambda r: r["authorizations"][0].update(authorization_evidence=["path exists", "boolean true"])),
        ("Q13_NEGATIVE_RELATIVE_PROJECT_ROOT", lambda r: r["authorizations"][0].update(active_project_root="project")),
        ("Q13_NEGATIVE_ABSOLUTE_ALLOWED_PATH", lambda r: r["authorizations"][0].update(allowed_relative_paths=[r"E:\bad.py"], expected_source_fingerprints={r"E:\bad.py": "a" * 64})),
        ("Q13_NEGATIVE_PATH_TRAVERSAL", lambda r: r["authorizations"][0].update(allowed_relative_paths=[r"..\bad.py"], expected_source_fingerprints={r"..\bad.py": "a" * 64})),
        ("Q13_NEGATIVE_FINGERPRINT_SET_MISMATCH", lambda r: r["authorizations"][0].update(expected_source_fingerprints={})),
        ("Q13_NEGATIVE_INVALID_FINGERPRINT", lambda r: r["authorizations"][0].update(expected_source_fingerprints={path: "bad" for path in r["authorizations"][0]["allowed_relative_paths"]})),
        ("Q13_NEGATIVE_REQUIRED_PREVIEW_MISSING", lambda r: r["authorizations"][0].update(approved_preview_required=True, approved_preview_id="", approved_preview_fingerprint="", current_preview_matches=True)),
        ("Q13_NEGATIVE_STALE_PREVIEW", lambda r: r["authorizations"][0].update(approved_preview_required=True, approved_preview_id="preview-1", approved_preview_fingerprint="b" * 64, current_preview_matches=False)),
        ("Q13_NEGATIVE_TRANSACTION_ID_MISSING", lambda r: r["authorizations"][0].update(transaction_applicable=True, transaction_id="", current_transaction_matches=True)),
        ("Q13_NEGATIVE_HUMAN_AUTHORIZATION_MISSING", lambda r: r["authorizations"][0].update(human_authorization_current=False)),
        ("Q13_NEGATIVE_UNBOUNDED_SCOPE", lambda r: r["authorizations"][0].update(scope_bounded=False)),
        ("Q13_NEGATIVE_OPERATION_MISMATCH", lambda r: r["authorizations"][0].update(current_operation_matches=False)),
        ("Q13_NEGATIVE_PROJECT_MISMATCH", lambda r: r["authorizations"][0].update(current_project_matches=False)),
        ("Q13_NEGATIVE_PATH_SET_MISMATCH", lambda r: r["authorizations"][0].update(current_path_set_matches=False)),
        ("Q13_NEGATIVE_SOURCE_MISMATCH", lambda r: r["authorizations"][0].update(current_source_fingerprints_match=False)),
        ("Q13_NEGATIVE_GENERATION_MISMATCH", lambda r: r["authorizations"][0].update(current_generation_matches=False)),
        ("Q13_NEGATIVE_EXPIRED_AUTHORIZATION", lambda r: r["authorizations"][0].update(authorization_not_expired=False)),
        ("Q13_NEGATIVE_INCOMPLETE_INVALIDATION", lambda r: r["authorizations"][0].update(invalidation_conditions=["operation_change"])),
        ("Q13_NEGATIVE_BLOCKED_PATH_CONTRADICTION", lambda r: r["authorizations"][0].update(blocked_paths=r["authorizations"][0]["allowed_relative_paths"])),
        ("Q13_NEGATIVE_UNRESOLVED_FIELD", lambda r: r.update(unresolved_fields=["Preview authority"])),
        ("Q13_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q13_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
    ]
    for label, mutate in cases:
        _reject(label, mutate)
    invalid = _valid_na()
    invalid["no_write_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        print("Q13_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: PASS")
    else:
        raise AssertionError("Q13_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: FAIL")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_source(root)
    validate_semantics()
    print("Q13_EXPLICIT_WRITE_AUTHORIZATION_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
