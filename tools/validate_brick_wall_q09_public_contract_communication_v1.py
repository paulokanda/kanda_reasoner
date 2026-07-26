"""Validate Brick Wall Q09 public-contract communication enforcement."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q09-public-contract-communication-enforcement-v1"
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
Q09_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q09_public_contract_communication_v1.py"
)

CANON_FIELDS = (
    "### Law 2: Public Contract, Private Internals",
    "Other boxes may only use the public contract.",
    "Private internals must not be imported or modified by other boxes.",
    "### Law 3: No Private Reach-In",
    "No box may import or call another box's private file",
    "### Law 4: Explicit Communication",
    "Boxes must communicate only through approved routes:",
    "Test the public contract only.",
    "If the test cannot use the public contract, the contract is incomplete.",
)

BRICK_FIELDS = (
    "### Public-contract-only communication (Q09)",
    "PUBLIC-CONTRACT COMMUNICATION RECORD",
    "communication required YES/NO",
    "Routes, once per caller-callee/package boundary:",
    "unique public owner YES/NO",
    "package-root export verified YES/NO/N/A",
    "required subset preserved YES/NO",
    "private reexports in __all__",
    "Decision: COMPLETE/BLOCKED | proceed to Q10 YES/NO | may begin coding NO",
)

BRIDGE_FIELDS = (
    "## Public-contract-only communication gate (Q09)",
    "PUBLIC-CONTRACT COMMUNICATION RECORD",
    "Q09 public-contract communication record complete: YES / NO",
    "Public-contract communication decision: COMPLETE / BLOCKED",
    "May proceed to Q10 mutable-state ownership gate: YES / NO",
)

RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "communication_required",
    "no_route_evidence",
    "routes",
    "unique_public_owner",
    "explicit_exports_verified",
    "package_root_exports_verified",
    "duplicate_public_owners",
    "required_consumer_subset_preserved",
    "current_consumers_validated",
    "star_import_ambiguity",
    "private_reach_ins",
    "private_symbols_in_public_all",
    "direct_private_state_mutations",
    "hidden_mutable_globals",
    "accidental_package_root_ownership",
    "contract_tests",
    "boundary_tests",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q10",
    "may_begin_coding",
)

ROUTE_FIELDS = (
    "caller_box",
    "callee_box",
    "public_owner",
    "public_facade",
    "contract_symbol",
    "import_or_call_path",
    "approved_route",
    "consumer_evidence",
    "signature_behavior",
    "state_access",
    "optional_dependency",
    "fallback_behavior",
    "removal_behavior",
    "tests",
    "blocked_private_route",
    "package_root_import",
    "package_root_export_verified",
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


def _private_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    parts = [part for part in normalized.replace(".", "/").split("/") if part]
    return any(part.startswith("_") for part in parts)


def validate_route(route: Mapping[str, object]) -> None:
    missing = [field for field in ROUTE_FIELDS if field not in route]
    if missing:
        raise AssertionError(f"route missing fields: {', '.join(missing)}")

    text_fields = (
        "caller_box",
        "callee_box",
        "public_owner",
        "public_facade",
        "contract_symbol",
        "import_or_call_path",
        "approved_route",
        "consumer_evidence",
        "signature_behavior",
        "state_access",
        "removal_behavior",
        "blocked_private_route",
    )
    for field in text_fields:
        if not _nonempty_text(route[field]):
            raise AssertionError(f"route empty field: {field}")
        if str(route[field]).strip().upper() in {"UNKNOWN", "UNRESOLVED"}:
            raise AssertionError(f"route unresolved field: {field}")

    if not _text_list(route["tests"]):
        raise AssertionError("route tests must be a non-empty text list")

    import_path = str(route["import_or_call_path"])
    if _private_path(import_path):
        raise AssertionError("private import or call path")

    if not isinstance(route["optional_dependency"], bool):
        raise AssertionError("optional_dependency must be boolean")
    if not isinstance(route["package_root_import"], bool):
        raise AssertionError("package_root_import must be boolean")
    if not isinstance(route["package_root_export_verified"], bool):
        raise AssertionError("package_root_export_verified must be boolean")

    if route["optional_dependency"] and not _nonempty_text(route["fallback_behavior"]):
        raise AssertionError("optional dependency requires fallback behavior")
    if not route["optional_dependency"] and not isinstance(
        route["fallback_behavior"], str
    ):
        raise AssertionError("fallback_behavior must be text")
    if route["package_root_import"] and not route["package_root_export_verified"]:
        raise AssertionError("package-root import lacks verified explicit export")


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in RECORD_FIELDS if field not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")

    for field in ("identity_basis", "primary_box"):
        if not _nonempty_text(record[field]):
            raise AssertionError(f"empty field: {field}")

    for field in (
        "communication_required",
        "unique_public_owner",
        "explicit_exports_verified",
        "package_root_exports_verified",
        "required_consumer_subset_preserved",
        "current_consumers_validated",
        "star_import_ambiguity",
        "may_proceed_to_q10",
        "may_begin_coding",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError(f"{field} must be boolean")

    list_fields = (
        "duplicate_public_owners",
        "private_reach_ins",
        "private_symbols_in_public_all",
        "direct_private_state_mutations",
        "hidden_mutable_globals",
        "accidental_package_root_ownership",
        "contract_tests",
        "boundary_tests",
        "unresolved_fields",
    )
    for field in list_fields:
        if not _text_list(record[field], allow_empty=True):
            raise AssertionError(f"{field} must be a text list")

    if not record["contract_tests"] or not record["boundary_tests"]:
        raise AssertionError("contract and boundary tests are required")

    routes = record["routes"]
    if not isinstance(routes, list):
        raise AssertionError("routes must be a list")
    if record["communication_required"]:
        if not routes:
            raise AssertionError("communication-required record needs routes")
        for route in routes:
            if not isinstance(route, Mapping):
                raise AssertionError("route must be a mapping")
            validate_route(route)
    else:
        if routes:
            raise AssertionError("no-route record must not contain routes")
        if not _nonempty_text(record["no_route_evidence"]):
            raise AssertionError("no-route record needs evidence")

    blocking_lists = (
        "duplicate_public_owners",
        "private_reach_ins",
        "private_symbols_in_public_all",
        "direct_private_state_mutations",
        "hidden_mutable_globals",
        "accidental_package_root_ownership",
        "unresolved_fields",
    )
    for field in blocking_lists:
        if record[field]:
            raise AssertionError(f"blocking findings present: {field}")

    if not record["unique_public_owner"]:
        raise AssertionError("unique public owner is not verified")
    if not record["explicit_exports_verified"]:
        raise AssertionError("explicit exports are not verified")
    if not record["package_root_exports_verified"]:
        raise AssertionError("package-root export classification is unresolved")
    if not record["required_consumer_subset_preserved"]:
        raise AssertionError("required consumer subset is not preserved")
    if not record["current_consumers_validated"]:
        raise AssertionError("current consumers are not validated")
    if record["star_import_ambiguity"]:
        raise AssertionError("star-import ambiguity is unresolved")
    if str(record["decision"]).strip().upper() != "COMPLETE":
        raise AssertionError("decision must be COMPLETE")
    if not record["may_proceed_to_q10"]:
        raise AssertionError("Q10 progression must be YES")
    if record["may_begin_coding"]:
        raise AssertionError("Q09 must keep coding blocked")


def _complete_route() -> dict[str, object]:
    return {
        "caller_box": "Prompt governance",
        "callee_box": "Box architecture",
        "public_owner": "box_architecture_canon",
        "public_facade": "box_architecture_canon.md",
        "contract_symbol": "Laws 2-4",
        "import_or_call_path": "box_architecture_canon public contract",
        "approved_route": "routed prompt contract",
        "consumer_evidence": "Brick Wall and router references verified",
        "signature_behavior": "Canonical law text remains authoritative",
        "state_access": "read-only contract consumption",
        "optional_dependency": False,
        "fallback_behavior": "",
        "removal_behavior": "Q09 remains blocked if owner is unavailable",
        "tests": ["Q09 semantic record validation"],
        "blocked_private_route": "No private helper or internal state access",
        "package_root_import": False,
        "package_root_export_verified": True,
    }


def _complete_record() -> dict[str, object]:
    return {
        "identity_basis": "current post-Q08 exact source",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "communication_required": True,
        "no_route_evidence": "",
        "routes": [_complete_route()],
        "unique_public_owner": True,
        "explicit_exports_verified": True,
        "package_root_exports_verified": True,
        "duplicate_public_owners": [],
        "required_consumer_subset_preserved": True,
        "current_consumers_validated": True,
        "star_import_ambiguity": False,
        "private_reach_ins": [],
        "private_symbols_in_public_all": [],
        "direct_private_state_mutations": [],
        "hidden_mutable_globals": [],
        "accidental_package_root_ownership": [],
        "contract_tests": ["Canonical facade and owner verification"],
        "boundary_tests": ["Private reach-in rejection"],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q10": True,
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

    _require_fragments(canon_text, CANON_FIELDS, "Q09_CANONICAL_OWNER")
    _require_fragments(brick_text, BRICK_FIELDS, "Q09_BRICK_WALL_CONTRACT")
    _require_fragments(bridge_text, BRIDGE_FIELDS, "Q09_ROUTER_BRIDGE")

    _gate("Q09_BRICK_VERSION", _parse_version(brick_meta["version"]) >= (1, 9))
    _gate("Q09_BRIDGE_VERSION", _parse_version(bridge_meta["version"]) >= (2, 3))
    for label, metadata in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = metadata.get("source_stage")
        updated = metadata.get("updated_for")
        _gate(
            "Q09_METADATA_ALIGNMENT",
            _nonempty_text(stage) and stage == updated,
            label,
        )

    _gate("Q09_BRICK_MODULE_SIZE", len(brick_text.splitlines()) <= 500)
    _gate("Q09_BRIDGE_MODULE_SIZE", len(bridge_text.splitlines()) <= 500)
    validator_lines = len(_read_text(project_root / Q09_VALIDATOR_REL).splitlines())
    _gate("Q09_VALIDATOR_MODULE_SIZE", validator_lines <= 500)


def validate_semantics() -> None:
    validate_record(_complete_record())
    print("Q09_COMPLETE_RECORD_ACCEPTED: PASS")

    no_route = deepcopy(_complete_record())
    no_route["communication_required"] = False
    no_route["no_route_evidence"] = "No cross-box or package communication"
    no_route["routes"] = []
    validate_record(no_route)
    print("Q09_EVIDENCE_BACKED_NO_ROUTE_ACCEPTED: PASS")

    _expect_rejected(
        "Q09_NEGATIVE_MISSING_ROUTE",
        lambda r: r.update(routes=[]),
    )
    _expect_rejected(
        "Q09_NEGATIVE_PRIVATE_REACH_IN",
        lambda r: r["routes"][0].update(import_or_call_path="box._private"),
    )
    _expect_rejected(
        "Q09_NEGATIVE_PACKAGE_ROOT_ASSUMPTION",
        lambda r: r["routes"][0].update(
            package_root_import=True,
            package_root_export_verified=False,
        ),
    )
    _expect_rejected(
        "Q09_NEGATIVE_DUPLICATE_PUBLIC_OWNER",
        lambda r: r.update(duplicate_public_owners=["helper and facade"]),
    )
    _expect_rejected(
        "Q09_NEGATIVE_PRIVATE_ALL_REEXPORT",
        lambda r: r.update(private_symbols_in_public_all=["_internal"]),
    )
    _expect_rejected(
        "Q09_NEGATIVE_CONSUMER_SUBSET",
        lambda r: r.update(required_consumer_subset_preserved=False),
    )
    _expect_rejected(
        "Q09_NEGATIVE_CURRENT_CONSUMERS",
        lambda r: r.update(current_consumers_validated=False),
    )
    _expect_rejected(
        "Q09_NEGATIVE_STAR_IMPORT_AMBIGUITY",
        lambda r: r.update(star_import_ambiguity=True),
    )
    _expect_rejected(
        "Q09_NEGATIVE_PRIVATE_STATE_MUTATION",
        lambda r: r.update(direct_private_state_mutations=["other._state"]),
    )
    _expect_rejected(
        "Q09_NEGATIVE_OPTIONAL_FALLBACK",
        lambda r: r["routes"][0].update(
            optional_dependency=True,
            fallback_behavior="",
        ),
    )
    _expect_rejected(
        "Q09_NEGATIVE_UNRESOLVED_FIELD",
        lambda r: r.update(unresolved_fields=["facade owner"]),
    )
    _expect_rejected(
        "Q09_NEGATIVE_BLOCKED_DECISION",
        lambda r: r.update(decision="BLOCKED"),
    )
    _expect_rejected(
        "Q09_NEGATIVE_Q10_PROGRESSION",
        lambda r: r.update(may_proceed_to_q10=False),
    )
    _expect_rejected(
        "Q09_NEGATIVE_CODING_AUTHORIZATION",
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
