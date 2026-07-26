"""Validate Brick Wall Q10 single mutable-state ownership enforcement."""

from __future__ import annotations
__all__: list[str] = []
import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q10-single-mutable-state-owner-enforcement-v1"
BRICK_WALL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
BOX_CANON_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "04_box_architecture_and_boundaries/box_architecture_canon.md"
)
Q10_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q10_single_mutable_state_owner_v1.py"
)

CANON_FIELDS = (
    "### Law 5: State Belongs to One Box",
    "Every piece of mutable state must have exactly one owner box.",
    "Other boxes may request state through the public contract",
    "two boxes writing the same global variable",
    "registry storing runtime state from many boxes",
    "Every mutable state object must have one owner box.",
)

BRICK_FIELDS = (
    "### Single mutable-state owner (Q10)",
    "SINGLE MUTABLE-STATE OWNERSHIP RECORD",
    "mutable state required YES/NO",
    "States, once per mutable state:",
    "owner box | canonical storage/truth",
    "mutation owner/route",
    "shared-host feature caches",
    "Decision: COMPLETE/BLOCKED | proceed to Q11 YES/NO | may begin coding NO",
)

BRIDGE_FIELDS = (
    "## Single mutable-state owner gate (Q10)",
    "SINGLE MUTABLE-STATE OWNERSHIP RECORD",
    "Q10 single mutable-state ownership record complete: YES / NO",
    "Mutable-state ownership decision: COMPLETE / BLOCKED",
    "May proceed to Q11 MCard applicability gate: YES / NO",
)

RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "mutable_state_required",
    "no_state_evidence",
    "states",
    "all_states_classified_once",
    "duplicate_state_ids",
    "duplicate_owner_claims",
    "duplicate_storage_authorities",
    "hidden_mutable_globals",
    "registry_runtime_state",
    "shared_host_feature_caches",
    "cross_box_state_aliases",
    "direct_external_mutations",
    "persistence_owner_mismatches",
    "stale_async_mutation_risks",
    "state_tests",
    "boundary_tests",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q11",
    "may_begin_coding",
)

STATE_FIELDS = (
    "state_id",
    "description",
    "owner_box",
    "canonical_storage",
    "canonical_truth",
    "initializer",
    "mutation_owner_box",
    "mutation_route",
    "authorized_mutators",
    "external_request_routes",
    "read_route",
    "consumers",
    "lifetime",
    "persistence_owner",
    "persistence_contract",
    "reset_invalidation",
    "async_concurrency_guard",
    "tests",
    "blocked_direct_mutators",
    "owner_verified",
    "mutation_route_verified",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read_text(path))


def _parse_version(value: object) -> tuple[int, ...]:
    parts = str(value).strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise AssertionError(f"invalid numeric version: {value}")
    return tuple(int(part) for part in parts)


def _gate(name: str, passed: bool, detail: str = "") -> None:
    if not passed:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{name}: FAIL{suffix}")
    suffix = f" - {detail}" if detail else ""
    print(f"{name}: PASS{suffix}")


def _require_fragments(text: str, fragments: Sequence[str], label: str) -> None:
    for fragment in fragments:
        _gate(label, fragment in text, fragment)


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object, allow_empty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if not value:
        return allow_empty
    return all(_nonempty_text(item) for item in value)


def validate_state(state: Mapping[str, object]) -> None:
    missing = [field for field in STATE_FIELDS if field not in state]
    if missing:
        raise AssertionError(f"state missing fields: {', '.join(missing)}")

    text_fields = (
        "state_id",
        "description",
        "owner_box",
        "canonical_storage",
        "canonical_truth",
        "initializer",
        "mutation_owner_box",
        "mutation_route",
        "read_route",
        "lifetime",
        "persistence_owner",
        "reset_invalidation",
        "async_concurrency_guard",
    )
    for field in text_fields:
        if not _nonempty_text(state[field]):
            raise AssertionError(f"state empty field: {field}")
        if str(state[field]).strip().upper() in {"UNKNOWN", "UNRESOLVED"}:
            raise AssertionError(f"state unresolved field: {field}")

    for field in (
        "authorized_mutators",
        "consumers",
        "tests",
        "blocked_direct_mutators",
    ):
        if not _text_list(state[field]):
            raise AssertionError(f"state {field} must be a non-empty text list")

    if not _text_list(state["external_request_routes"], allow_empty=True):
        raise AssertionError("external_request_routes must be a text list")
    if not isinstance(state["persistence_contract"], str):
        raise AssertionError("persistence_contract must be text")
    if not isinstance(state["owner_verified"], bool):
        raise AssertionError("owner_verified must be boolean")
    if not isinstance(state["mutation_route_verified"], bool):
        raise AssertionError("mutation_route_verified must be boolean")

    if state["mutation_owner_box"] != state["owner_box"]:
        raise AssertionError("mutation owner differs from state owner")
    if not state["owner_verified"]:
        raise AssertionError("state owner is not verified")
    if not state["mutation_route_verified"]:
        raise AssertionError("mutation route is not verified")

    persistence_owner = str(state["persistence_owner"]).strip()
    owner_box = str(state["owner_box"]).strip()
    if persistence_owner not in {owner_box, "N/A"}:
        if not _nonempty_text(state["persistence_contract"]):
            raise AssertionError("external persistence owner requires public contract")


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in RECORD_FIELDS if field not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")

    for field in ("identity_basis", "primary_box"):
        if not _nonempty_text(record[field]):
            raise AssertionError(f"empty field: {field}")

    for field in (
        "mutable_state_required",
        "all_states_classified_once",
        "may_proceed_to_q11",
        "may_begin_coding",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError(f"{field} must be boolean")

    list_fields = (
        "duplicate_state_ids",
        "duplicate_owner_claims",
        "duplicate_storage_authorities",
        "hidden_mutable_globals",
        "registry_runtime_state",
        "shared_host_feature_caches",
        "cross_box_state_aliases",
        "direct_external_mutations",
        "persistence_owner_mismatches",
        "stale_async_mutation_risks",
        "state_tests",
        "boundary_tests",
        "unresolved_fields",
    )
    for field in list_fields:
        if not _text_list(record[field], allow_empty=True):
            raise AssertionError(f"{field} must be a text list")

    if not record["state_tests"] or not record["boundary_tests"]:
        raise AssertionError("state and boundary tests are required")

    states = record["states"]
    if not isinstance(states, list):
        raise AssertionError("states must be a list")

    if record["mutable_state_required"]:
        if not states:
            raise AssertionError("mutable-state record needs state rows")
        state_ids: list[str] = []
        for state in states:
            if not isinstance(state, Mapping):
                raise AssertionError("state row must be a mapping")
            validate_state(state)
            state_ids.append(str(state["state_id"]).strip())
        if len(state_ids) != len(set(state_ids)):
            raise AssertionError("state IDs must be unique")
    else:
        if states:
            raise AssertionError("no-state record must not contain state rows")
        if not _nonempty_text(record["no_state_evidence"]):
            raise AssertionError("no-state record requires evidence")

    if not record["all_states_classified_once"]:
        raise AssertionError("all states are not classified exactly once")

    blocking_lists = (
        "duplicate_state_ids",
        "duplicate_owner_claims",
        "duplicate_storage_authorities",
        "hidden_mutable_globals",
        "registry_runtime_state",
        "shared_host_feature_caches",
        "cross_box_state_aliases",
        "direct_external_mutations",
        "persistence_owner_mismatches",
        "stale_async_mutation_risks",
        "unresolved_fields",
    )
    for field in blocking_lists:
        if record[field]:
            raise AssertionError(f"blocking findings present: {field}")

    if str(record["decision"]).strip().upper() != "COMPLETE":
        raise AssertionError("decision must be COMPLETE")
    if not record["may_proceed_to_q11"]:
        raise AssertionError("Q11 progression must be YES")
    if record["may_begin_coding"]:
        raise AssertionError("Q10 must keep coding blocked")


def _complete_state() -> dict[str, object]:
    return {
        "state_id": "brick_wall_status",
        "description": "Current evidence-backed Q01-Q40 status",
        "owner_box": "Context Routing and Governance Layer",
        "canonical_storage": "current response state",
        "canonical_truth": "current exact source and evidence",
        "initializer": "Brick Wall invocation",
        "mutation_owner_box": "Context Routing and Governance Layer",
        "mutation_route": "Brick Wall evidence update",
        "authorized_mutators": ["brick_wall_comprehensive_quality_gate"],
        "external_request_routes": ["router bridge routed invocation"],
        "read_route": "Brick Wall status response",
        "consumers": ["user", "governed implementation router"],
        "lifetime": "current governed task and evidence generation",
        "persistence_owner": "N/A",
        "persistence_contract": "",
        "reset_invalidation": "reset on source, handoff, validation, or freeze change",
        "async_concurrency_guard": "no async mutation; evidence freshness required",
        "tests": ["Q10 semantic ownership validation"],
        "blocked_direct_mutators": ["other boxes and generated artifacts"],
        "owner_verified": True,
        "mutation_route_verified": True,
    }


def _complete_record() -> dict[str, object]:
    return {
        "identity_basis": "current post-Q09 exact source",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "mutable_state_required": True,
        "no_state_evidence": "",
        "states": [_complete_state()],
        "all_states_classified_once": True,
        "duplicate_state_ids": [],
        "duplicate_owner_claims": [],
        "duplicate_storage_authorities": [],
        "hidden_mutable_globals": [],
        "registry_runtime_state": [],
        "shared_host_feature_caches": [],
        "cross_box_state_aliases": [],
        "direct_external_mutations": [],
        "persistence_owner_mismatches": [],
        "stale_async_mutation_risks": [],
        "state_tests": ["single owner and mutation route"],
        "boundary_tests": ["cross-box direct mutation rejection"],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q11": True,
        "may_begin_coding": False,
    }


def _expect_rejected(name: str, mutate) -> None:
    record = deepcopy(_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        print(f"{name}: PASS")
        return
    raise AssertionError(f"{name}: FAIL - invalid record accepted")


def validate_source(project_root: Path) -> None:
    brick_text = _read_text(project_root / BRICK_WALL_REL)
    bridge_text = _read_text(project_root / BRIDGE_REL)
    canon_text = _read_text(project_root / BOX_CANON_REL)
    brick_meta = _load_json(project_root / BRICK_META_REL)
    bridge_meta = _load_json(project_root / BRIDGE_META_REL)

    _require_fragments(canon_text, CANON_FIELDS, "Q10_CANONICAL_OWNER")
    _require_fragments(brick_text, BRICK_FIELDS, "Q10_BRICK_WALL_CONTRACT")
    _require_fragments(bridge_text, BRIDGE_FIELDS, "Q10_ROUTER_BRIDGE")

    _gate("Q10_BRICK_VERSION", _parse_version(brick_meta["version"]) >= (2, 0))
    _gate("Q10_BRIDGE_VERSION", _parse_version(bridge_meta["version"]) >= (2, 4))
    for label, metadata in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = metadata.get("source_stage")
        updated = metadata.get("updated_for")
        _gate(
            "Q10_METADATA_ALIGNMENT",
            _nonempty_text(stage) and stage == updated,
            label,
        )

    _gate("Q10_BRICK_MODULE_SIZE", len(brick_text.splitlines()) <= 500)
    _gate("Q10_BRIDGE_MODULE_SIZE", len(bridge_text.splitlines()) <= 500)
    validator_lines = len(_read_text(project_root / Q10_VALIDATOR_REL).splitlines())
    _gate("Q10_VALIDATOR_MODULE_SIZE", validator_lines <= 500)


def validate_semantics() -> None:
    validate_record(_complete_record())
    print("Q10_COMPLETE_RECORD_ACCEPTED: PASS")

    no_state = deepcopy(_complete_record())
    no_state["mutable_state_required"] = False
    no_state["no_state_evidence"] = "No mutable runtime or persisted state is introduced"
    no_state["states"] = []
    validate_record(no_state)
    print("Q10_EVIDENCE_BACKED_NO_STATE_ACCEPTED: PASS")

    _expect_rejected(
        "Q10_NEGATIVE_MISSING_STATE_ROW",
        lambda r: r.update(states=[]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_DUPLICATE_STATE_ID",
        lambda r: r["states"].append(deepcopy(r["states"][0])),
    )
    _expect_rejected(
        "Q10_NEGATIVE_MUTATION_OWNER_MISMATCH",
        lambda r: r["states"][0].update(mutation_owner_box="Other box"),
    )
    _expect_rejected(
        "Q10_NEGATIVE_UNVERIFIED_OWNER",
        lambda r: r["states"][0].update(owner_verified=False),
    )
    _expect_rejected(
        "Q10_NEGATIVE_UNVERIFIED_MUTATION_ROUTE",
        lambda r: r["states"][0].update(mutation_route_verified=False),
    )
    _expect_rejected(
        "Q10_NEGATIVE_EXTERNAL_PERSISTENCE_WITHOUT_CONTRACT",
        lambda r: r["states"][0].update(
            persistence_owner="Settings box",
            persistence_contract="",
        ),
    )
    _expect_rejected(
        "Q10_NEGATIVE_DUPLICATE_OWNER_CLAIM",
        lambda r: r.update(duplicate_owner_claims=["Box A and Box B"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_DUPLICATE_STORAGE_AUTHORITY",
        lambda r: r.update(duplicate_storage_authorities=["two stores"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_HIDDEN_GLOBAL",
        lambda r: r.update(hidden_mutable_globals=["module_cache"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_REGISTRY_RUNTIME_STATE",
        lambda r: r.update(registry_runtime_state=["live widget pointer"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_SHARED_HOST_CACHE",
        lambda r: r.update(shared_host_feature_caches=["planner settings cache"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_CROSS_BOX_ALIAS",
        lambda r: r.update(cross_box_state_aliases=["shared mutable dict"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_DIRECT_EXTERNAL_MUTATION",
        lambda r: r.update(direct_external_mutations=["other_box._state"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_PERSISTENCE_OWNER_MISMATCH",
        lambda r: r.update(persistence_owner_mismatches=["fake settings owner"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_STALE_ASYNC_WRITE",
        lambda r: r.update(stale_async_mutation_risks=["old generation result"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_UNRESOLVED_FIELD",
        lambda r: r.update(unresolved_fields=["state owner"]),
    )
    _expect_rejected(
        "Q10_NEGATIVE_BLOCKED_DECISION",
        lambda r: r.update(decision="BLOCKED"),
    )
    _expect_rejected(
        "Q10_NEGATIVE_Q11_PROGRESSION",
        lambda r: r.update(may_proceed_to_q11=False),
    )
    _expect_rejected(
        "Q10_NEGATIVE_CODING_AUTHORIZATION",
        lambda r: r.update(may_begin_coding=True),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    validate_source(project_root)
    validate_semantics()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
