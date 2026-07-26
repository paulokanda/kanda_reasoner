"""Validate Brick Wall Q14 immediate pre-write freshness enforcement."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import hashlib
import json
import ntpath
import re
import tempfile
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q14-immediate-pre-write-freshness-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
COMPANION_REL = PLIB / "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/governed_architecture_companion_handoff.md"
Q13_VALIDATOR_REL = Path("tools/validate_brick_wall_q13_explicit_write_authorization_v1.py")
Q14_VALIDATOR_REL = Path("tools/validate_brick_wall_q14_immediate_pre_write_freshness_v1.py")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_CLASSIFICATIONS = {"TOOL_OWNED_LOGIC", "ACTIVE_PROJECT_SOURCE"}
BRICK_MARKERS = (
    "### Immediate pre-write freshness (Q14)",
    "IMMEDIATE PRE-WRITE FRESHNESS RECORD",
    "check phase/timestamp",
    "current exact-disk SHA-256",
    "Preview required/ID/expected/current exact-byte fingerprint",
    "no intervening identity change",
    "stale evidence invalidated",
    "proceed to Q15 canonical path-authority YES/NO",
    "may begin coding NO",
    "may write source NO",
    "invalidates Q12-Q14",
)
BRIDGE_MARKERS = (
    "## Immediate pre-write freshness gate (Q14)",
    "Q14 immediate pre-write freshness record complete: YES / NO",
    "Freshness decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "Freshness checked immediately before write: YES / NO / N/A",
    "Current exact-disk target fingerprints match: YES / NO / N/A",
    "No intervening identity change: YES / NO / N/A",
    "May proceed to Q15 canonical path-authority gate: YES / NO",
    "## Immediate pre-write freshness bridge",
)
COMPANION_MARKERS = (
    "## 4. Evidence freshness and reset rules",
    "source file content or hash",
    "operation identity",
    "lifecycle generation",
    "transaction identity",
    "Q14 immediate freshness:",
    "MAY BEGIN CODING: YES / NO",
    "MAY WRITE SOURCE: YES / NO",
)
RECORD_FIELDS = (
    "freshness_basis", "primary_box", "writes_required", "no_write_evidence",
    "check_phase", "checked_at", "checked_immediately_before_write",
    "operation_id", "authorization_id", "feature_id", "tool_root",
    "active_project_root", "targets", "preview_required", "preview_id",
    "expected_preview_fingerprint", "current_preview_fingerprint",
    "expected_generation", "current_generation", "transaction_applicable",
    "expected_transaction_id", "current_transaction_id", "public_owner",
    "public_facade", "current_consumers", "authorization_current",
    "human_authorization_current", "no_intervening_identity_change",
    "stale_evidence_invalidated", "blockers", "tests", "decision",
    "may_proceed_to_precode_authorization", "may_begin_coding",
    "may_write_source",
)
TARGET_FIELDS = (
    "relative_path", "logical_owner", "classification", "expected_sha256",
    "current_disk_sha256", "exists", "file_type", "link_status",
    "canonical_source", "current_match",
)


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


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validate_target(target: Mapping[str, object]) -> None:
    _fields(target, TARGET_FIELDS)
    if not _safe_relative(target["relative_path"]):
        raise AssertionError("unsafe target path")
    if not _nonempty(target["logical_owner"]):
        raise AssertionError("target owner missing")
    if target["classification"] not in ALLOWED_CLASSIFICATIONS:
        raise AssertionError("target classification invalid")
    expected = target["expected_sha256"]
    current = target["current_disk_sha256"]
    if not isinstance(expected, str) or not HEX64.fullmatch(expected.lower()):
        raise AssertionError("expected target fingerprint invalid")
    if not isinstance(current, str) or not HEX64.fullmatch(current.lower()):
        raise AssertionError("current target fingerprint invalid")
    if expected.lower() != current.lower() or target["current_match"] is not True:
        raise AssertionError("target fingerprint is stale")
    if target["exists"] is not True or target["file_type"] != "FILE":
        raise AssertionError("target missing or not a file")
    if target["link_status"] != "NOT_LINK":
        raise AssertionError("target link status is unresolved")
    if target["canonical_source"] is not True:
        raise AssertionError("generated artifact used as canonical source")


def validate_record(record: Mapping[str, object]) -> None:
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["freshness_basis"]) or not _nonempty(record["primary_box"]):
        raise AssertionError("freshness basis or primary box missing")
    if not isinstance(record["writes_required"], bool):
        raise AssertionError("writes_required must be boolean")
    if _text_list(record["blockers"]):
        raise AssertionError("freshness blockers remain")
    if record["may_begin_coding"] is not False or record["may_write_source"] is not False:
        raise AssertionError("Q14 cannot directly authorize coding or writing")
    if record["writes_required"] is False:
        if not _text_list(record["no_write_evidence"]):
            raise AssertionError("not-applicable evidence missing")
        if record["targets"] not in ([], None):
            raise AssertionError("not-applicable record carries targets")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_precode_authorization"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        return
    if record["decision"] != "COMPLETE":
        raise AssertionError("required freshness decision is not COMPLETE")
    if record["may_proceed_to_precode_authorization"] is not True:
        raise AssertionError("Q15 progression missing")
    if record["check_phase"] != "IMMEDIATELY_BEFORE_WRITE":
        raise AssertionError("freshness check phase is not immediate")
    if not _nonempty(record["checked_at"]):
        raise AssertionError("freshness timestamp missing")
    if record["checked_immediately_before_write"] is not True:
        raise AssertionError("freshness was not checked immediately before write")
    for field in (
        "operation_id", "authorization_id", "feature_id", "tool_root",
        "active_project_root", "expected_generation", "current_generation",
        "public_owner", "public_facade",
    ):
        if not _nonempty(record[field]):
            raise AssertionError(f"empty freshness field: {field}")
    if not ntpath.isabs(str(record["tool_root"])) or not ntpath.isabs(str(record["active_project_root"])):
        raise AssertionError("Tool or Project root is not absolute")
    targets = record["targets"]
    if not isinstance(targets, list) or not targets:
        raise AssertionError("freshness target set missing")
    paths: list[str] = []
    for target in targets:
        if not isinstance(target, Mapping):
            raise AssertionError("target record is not a mapping")
        _validate_target(target)
        paths.append(str(target["relative_path"]))
    if len(set(paths)) != len(paths):
        raise AssertionError("duplicate target path")
    if record["preview_required"] is True:
        for field in ("preview_id", "expected_preview_fingerprint", "current_preview_fingerprint"):
            if not _nonempty(record[field]):
                raise AssertionError("required Preview evidence missing")
        expected = str(record["expected_preview_fingerprint"])
        current = str(record["current_preview_fingerprint"])
        if not HEX64.fullmatch(expected.lower()) or not HEX64.fullmatch(current.lower()) or expected.lower() != current.lower():
            raise AssertionError("Preview fingerprint is stale")
    elif record["preview_required"] is False:
        for field in ("preview_id", "expected_preview_fingerprint", "current_preview_fingerprint"):
            if record[field] not in (None, "", "N/A"):
                raise AssertionError("non-applicable Preview carries identity")
    else:
        raise AssertionError("Preview applicability must be boolean")
    if record["expected_generation"] != record["current_generation"]:
        raise AssertionError("lifecycle generation is stale")
    if record["transaction_applicable"] is True:
        if not _nonempty(record["expected_transaction_id"]) or record["expected_transaction_id"] != record["current_transaction_id"]:
            raise AssertionError("transaction identity is stale")
    elif record["transaction_applicable"] is False:
        if record["expected_transaction_id"] not in (None, "", "N/A") or record["current_transaction_id"] not in (None, "", "N/A"):
            raise AssertionError("non-applicable transaction carries identity")
    else:
        raise AssertionError("transaction applicability must be boolean")
    if not _text_list(record["current_consumers"]):
        raise AssertionError("current consumer evidence missing")
    for field in (
        "authorization_current", "human_authorization_current",
        "no_intervening_identity_change", "stale_evidence_invalidated",
    ):
        if record[field] is not True:
            raise AssertionError(f"freshness failed: {field}")
    if not _text_list(record["tests"]):
        raise AssertionError("freshness tests missing")


def _target(path: str = "tools/example.py", digest: str = "a" * 64) -> dict[str, object]:
    return {
        "relative_path": path,
        "logical_owner": "Prompt library governance",
        "classification": "TOOL_OWNED_LOGIC",
        "expected_sha256": digest,
        "current_disk_sha256": digest,
        "exists": True,
        "file_type": "FILE",
        "link_status": "NOT_LINK",
        "canonical_source": True,
        "current_match": True,
    }


def _valid_required() -> dict[str, object]:
    return {
        "freshness_basis": "Current exact source re-read after Q13 authorization",
        "primary_box": "Prompt library governance",
        "writes_required": True,
        "no_write_evidence": [],
        "check_phase": "IMMEDIATELY_BEFORE_WRITE",
        "checked_at": "2026-07-15T03:10:00Z",
        "checked_immediately_before_write": True,
        "operation_id": "q14-operation-001",
        "authorization_id": "q14-auth-001",
        "feature_id": FEATURE_ID,
        "tool_root": r"E:\kanda_reasoner",
        "active_project_root": r"E:\kanda_reasoner",
        "targets": [_target()],
        "preview_required": False,
        "preview_id": "N/A",
        "expected_preview_fingerprint": "N/A",
        "current_preview_fingerprint": "N/A",
        "expected_generation": "q14-generation-1",
        "current_generation": "q14-generation-1",
        "transaction_applicable": False,
        "expected_transaction_id": "N/A",
        "current_transaction_id": "N/A",
        "public_owner": "Brick Wall prompt owner",
        "public_facade": "router_bridge_governed_implementation",
        "current_consumers": ["prompt router", "startup prompt generator"],
        "authorization_current": True,
        "human_authorization_current": True,
        "no_intervening_identity_change": True,
        "stale_evidence_invalidated": True,
        "blockers": [],
        "tests": ["Q14 exact-byte and negative freshness matrix"],
        "decision": "COMPLETE",
        "may_proceed_to_precode_authorization": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def _valid_na() -> dict[str, object]:
    record = _valid_required()
    record.update(
        writes_required=False,
        no_write_evidence=["No governed write is requested"],
        targets=[],
        decision="NOT_APPLICABLE",
    )
    return record


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
    _require(brick, BRICK_MARKERS, "Q14_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q14_ROUTER_BRIDGE_CONTRACT")
    _require(companion, COMPANION_MARKERS, "Q14_EXISTING_FRESHNESS_OWNER_REUSED")
    _gate("Q14_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 4))
    _gate("Q14_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (2, 8))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q14_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q13 = _read(root / Q13_VALIDATOR_REL)
    _gate(
        "Q13_FORWARD_COMPATIBLE_METADATA",
        "Q13_METADATA_ALIGNMENT" in q13
        and "_nonempty(stage) and stage == updated" in q13,
    )
    for rel in (BRICK_REL, BRIDGE_REL, Q13_VALIDATOR_REL, Q14_VALIDATOR_REL):
        lines = len(_read(root / rel).splitlines())
        _gate("Q14_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def validate_semantics() -> None:
    validate_record(_valid_required())
    print("Q14_REQUIRED_WRITE_RECORD_ACCEPTED: PASS")
    validate_record(_valid_na())
    print("Q14_NOT_APPLICABLE_RECORD_ACCEPTED: PASS")
    cases = [
        ("Q14_NEGATIVE_WRONG_PHASE", lambda r: r.update(check_phase="EARLIER_PREFLIGHT")),
        ("Q14_NEGATIVE_NOT_IMMEDIATE", lambda r: r.update(checked_immediately_before_write=False)),
        ("Q14_NEGATIVE_EMPTY_TARGETS", lambda r: r.update(targets=[])),
        ("Q14_NEGATIVE_DUPLICATE_TARGET", lambda r: r.update(targets=[_target(), _target()])),
        ("Q14_NEGATIVE_ABSOLUTE_TARGET", lambda r: r.update(targets=[_target(r"E:\\bad.py")])),
        ("Q14_NEGATIVE_TRAVERSAL_TARGET", lambda r: r.update(targets=[_target(r"..\\bad.py")])),
        ("Q14_NEGATIVE_MISSING_TARGET", lambda r: r["targets"][0].update(exists=False)),
        ("Q14_NEGATIVE_NON_FILE_TARGET", lambda r: r["targets"][0].update(file_type="DIRECTORY")),
        ("Q14_NEGATIVE_LINK_TARGET", lambda r: r["targets"][0].update(link_status="SYMLINK")),
        ("Q14_NEGATIVE_GENERATED_AS_SOURCE", lambda r: r["targets"][0].update(canonical_source=False)),
        ("Q14_NEGATIVE_OWNER_MISSING", lambda r: r["targets"][0].update(logical_owner="")),
        ("Q14_NEGATIVE_CLASSIFICATION", lambda r: r["targets"][0].update(classification="GENERATED_EVIDENCE_OR_HANDOFF")),
        ("Q14_NEGATIVE_INVALID_EXPECTED_HASH", lambda r: r["targets"][0].update(expected_sha256="bad")),
        ("Q14_NEGATIVE_INVALID_CURRENT_HASH", lambda r: r["targets"][0].update(current_disk_sha256="bad")),
        ("Q14_NEGATIVE_SOURCE_HASH_MISMATCH", lambda r: r["targets"][0].update(current_disk_sha256="b" * 64)),
        ("Q14_NEGATIVE_REQUIRED_PREVIEW_MISSING", lambda r: r.update(preview_required=True, preview_id="", expected_preview_fingerprint="", current_preview_fingerprint="")),
        ("Q14_NEGATIVE_PREVIEW_HASH_MISMATCH", lambda r: r.update(preview_required=True, preview_id="preview-1", expected_preview_fingerprint="a" * 64, current_preview_fingerprint="b" * 64)),
        ("Q14_NEGATIVE_GENERATION_MISMATCH", lambda r: r.update(current_generation="q14-generation-2")),
        ("Q14_NEGATIVE_TRANSACTION_MISMATCH", lambda r: r.update(transaction_applicable=True, expected_transaction_id="tx-1", current_transaction_id="tx-2")),
        ("Q14_NEGATIVE_CONSUMERS_MISSING", lambda r: r.update(current_consumers=[])),
        ("Q14_NEGATIVE_AUTHORIZATION_STALE", lambda r: r.update(authorization_current=False)),
        ("Q14_NEGATIVE_HUMAN_AUTHORITY_STALE", lambda r: r.update(human_authorization_current=False)),
        ("Q14_NEGATIVE_INTERVENING_CHANGE", lambda r: r.update(no_intervening_identity_change=False)),
        ("Q14_NEGATIVE_STALE_EVIDENCE_NOT_INVALIDATED", lambda r: r.update(stale_evidence_invalidated=False)),
        ("Q14_NEGATIVE_BLOCKERS_REMAIN", lambda r: r.update(blockers=["source changed"])),
        ("Q14_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q14_NEGATIVE_SOURCE_WRITE_AUTHORIZATION", lambda r: r.update(may_write_source=True)),
        ("Q14_NEGATIVE_NO_FINAL_PROGRESSION", lambda r: r.update(may_proceed_to_precode_authorization=False)),
    ]
    for label, mutate in cases:
        _reject(label, mutate)
    invalid = _valid_na()
    invalid["no_write_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        print("Q14_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: PASS")
    else:
        raise AssertionError("Q14_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: FAIL")


def validate_exact_disk_bytes() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "fixture.txt"
        data = b"first\r\nsecond\r\n"
        path.write_bytes(data)
        exact_hash = _sha_bytes(path.read_bytes())
        normalized_hash = _sha_bytes(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8"))
        _gate("Q14_EXACT_DISK_BYTE_FINGERPRINT", exact_hash == _sha_bytes(data))
        _gate("Q14_TEXT_NORMALIZED_HASH_REJECTED", exact_hash != normalized_hash)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_source(root)
    validate_semantics()
    validate_exact_disk_bytes()
    print("Q14_CANONICAL_SOURCE_AND_PREVIEW_FRESHNESS: PASS")
    print("Q14_IMMEDIATE_PRE_WRITE_FRESHNESS_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
