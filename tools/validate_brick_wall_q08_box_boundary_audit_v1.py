"""Validate Brick Wall Q08 Box Boundary Audit enforcement."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q08-box-boundary-audit-enforcement-v1"
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
Q07_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q07_ownership_no_leak_classification_v1.py"
)
Q08_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q08_box_boundary_audit_v1.py"
)

CANON_FIELDS = (
    "Patch target:",
    "Primary box:",
    "Box type:",
    "Box size:",
    "Lifecycle state:",
    "Single responsibility:",
    "Owner paths:",
    "Files expected to change:",
    "Files outside owner paths:",
    "Reason for outside touch:",
    "Allowed supporting touch? YES / NO",
    "Public contract:",
    "Private internals:",
    "Inputs:",
    "Outputs:",
    "Dependencies:",
    "Optional dependencies:",
    "Forbidden dependencies:",
    "Communication route:",
    "State ownership:",
    "Fallback behavior:",
    "Disable/removal behavior:",
    "Risk of circular dependency:",
    "Risk of registry leakage:",
    "Risk of GUI/domain mixing:",
    "Risk of private reach-in:",
    "Focused tests:",
    "Boundary tests:",
    "Contamination tests:",
    "Manual validation needed:",
    "Freeze condition:",
)

BRICK_FIELDS = (
    "### Box Boundary Audit (Q08)",
    "BOX BOUNDARY AUDIT",
    "Q08 COMPLETION",
    "Coverage / one primary box / allowed outside touches: YES / NO",
    "Public-contract communication / state and evidence owners: YES / NO",
    "Decision: COMPLETE/BLOCKED | proceed to Q09 YES/NO | may begin coding NO",
)

BRIDGE_FIELDS = (
    "## Box Boundary Audit gate (Q08)",
    "Q08 COMPLETION",
    "Q08 Box Boundary Audit complete: YES / NO",
    "Box Boundary decision: COMPLETE / BLOCKED",
    "May proceed to Q09 public-contract gate: YES / NO",
)

REQUIRED_RECORD_FIELDS = (
    "patch_target",
    "primary_box",
    "box_type",
    "box_size",
    "lifecycle_state",
    "single_responsibility",
    "owner_paths",
    "files_expected_to_change",
    "files_outside_owner_paths",
    "reason_for_outside_touch",
    "allowed_supporting_touch",
    "public_contract",
    "private_internals",
    "inputs",
    "outputs",
    "dependencies",
    "optional_dependencies",
    "forbidden_dependencies",
    "communication_route",
    "state_ownership",
    "owns_mutable_state",
    "mutable_state_location",
    "mutation_authority",
    "fallback_behavior",
    "disable_removal_behavior",
    "risk_circular_dependency",
    "risk_registry_leakage",
    "risk_gui_domain_mixing",
    "risk_private_reach_in",
    "focused_tests",
    "boundary_tests",
    "contamination_tests",
    "manual_validation_needed",
    "generated_file_owner",
    "validation_owner",
    "freeze_condition",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q09",
    "may_begin_coding",
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


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_RECORD_FIELDS if field not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")

    scalar_fields = (
        "patch_target",
        "primary_box",
        "box_type",
        "box_size",
        "lifecycle_state",
        "single_responsibility",
        "reason_for_outside_touch",
        "public_contract",
        "communication_route",
        "state_ownership",
        "mutable_state_location",
        "mutation_authority",
        "fallback_behavior",
        "disable_removal_behavior",
        "risk_circular_dependency",
        "risk_registry_leakage",
        "risk_gui_domain_mixing",
        "risk_private_reach_in",
        "manual_validation_needed",
        "generated_file_owner",
        "validation_owner",
        "freeze_condition",
    )
    for field in scalar_fields:
        if not _nonempty_text(record[field]):
            raise AssertionError(f"empty field: {field}")
        if str(record[field]).strip().upper() in {"UNKNOWN", "UNRESOLVED"}:
            raise AssertionError(f"unresolved field: {field}")

    list_fields = (
        "owner_paths",
        "files_expected_to_change",
        "private_internals",
        "inputs",
        "outputs",
        "dependencies",
        "forbidden_dependencies",
        "focused_tests",
        "boundary_tests",
        "contamination_tests",
    )
    for field in list_fields:
        if not _text_list(record[field]):
            raise AssertionError(f"invalid list field: {field}")

    for field in ("files_outside_owner_paths", "optional_dependencies"):
        if not _text_list(record[field], allow_empty=True):
            raise AssertionError(f"invalid optional list field: {field}")

    primary = str(record["primary_box"]).strip()
    if "," in primary or "|" in primary or " and " in primary.lower():
        raise AssertionError("multiple primary boxes")

    outside = record["files_outside_owner_paths"]
    allowed = record["allowed_supporting_touch"] is True
    reason = str(record["reason_for_outside_touch"]).strip()
    if outside and (not allowed or reason.upper() in {"N/A", "NONE"}):
        raise AssertionError("outside touch is not declared and allowed")
    if not outside and allowed:
        raise AssertionError("supporting touch allowed without outside files")

    owns_state = record["owns_mutable_state"] is True
    state_location = str(record["mutable_state_location"]).strip().upper()
    mutation_authority = str(record["mutation_authority"]).strip().upper()
    if owns_state and (state_location in {"N/A", "NONE"} or mutation_authority in {"N/A", "NONE"}):
        raise AssertionError("mutable state owner is incomplete")
    if not owns_state and (state_location not in {"N/A", "NONE"} or mutation_authority not in {"N/A", "NONE"}):
        raise AssertionError("non-owner declares mutable state authority")

    unresolved = record["unresolved_fields"]
    if not isinstance(unresolved, list) or unresolved:
        raise AssertionError("unresolved fields remain")
    if str(record["decision"]).strip().upper() != "COMPLETE":
        raise AssertionError("decision is not COMPLETE")
    if record["may_proceed_to_q09"] is not True:
        raise AssertionError("Q09 progression is not authorized")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q08 must not authorize coding")


def _valid_record() -> dict[str, object]:
    return {
        "patch_target": "Brick Wall Q08 enforcement",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "box_type": "prompt-library governance",
        "box_size": "bounded five-file repair",
        "lifecycle_state": "active and source-inspected",
        "single_responsibility": "enforce canonical Box Boundary Audit",
        "owner_paths": ["kanda_prompt_workspace/prompt_library", "tools"],
        "files_expected_to_change": ["brick_wall_comprehensive_quality_gate.md"],
        "files_outside_owner_paths": [],
        "reason_for_outside_touch": "N/A",
        "allowed_supporting_touch": False,
        "public_contract": "canonical prompt and focused validator",
        "private_internals": ["prompt wording helpers"],
        "inputs": ["exact source", "Box Architecture canon"],
        "outputs": ["Q08 audit decision", "Q09 progression"],
        "dependencies": ["box_architecture_canon"],
        "optional_dependencies": [],
        "forbidden_dependencies": ["private runtime internals"],
        "communication_route": "public prompt contract",
        "state_ownership": "no runtime mutable state",
        "owns_mutable_state": False,
        "mutable_state_location": "N/A",
        "mutation_authority": "N/A",
        "fallback_behavior": "block when evidence is incomplete",
        "disable_removal_behavior": "remove Q08 route without runtime impact",
        "risk_circular_dependency": "low",
        "risk_registry_leakage": "low",
        "risk_gui_domain_mixing": "none",
        "risk_private_reach_in": "blocked",
        "focused_tests": ["Q08 source validator"],
        "boundary_tests": ["outside-touch rejection"],
        "contamination_tests": ["no parallel box schema"],
        "manual_validation_needed": "local validation and freeze review",
        "generated_file_owner": "active project support root",
        "validation_owner": "focused Q08 validator",
        "freeze_condition": "local markers plus human Confirm and Write",
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q09": True,
        "may_begin_coding": False,
    }


def _expect_rejection(name: str, record: Mapping[str, object]) -> None:
    try:
        validate_record(record)
    except AssertionError:
        print(f"Q08_NEGATIVE_{name}: PASS")
        return
    raise AssertionError(f"Q08_NEGATIVE_{name}: FAIL - record was accepted")


def _validate_record_matrix() -> None:
    record = _valid_record()
    validate_record(record)
    print("Q08_COMPLETE_AUDIT_ACCEPTED: PASS")

    cases: list[tuple[str, dict[str, object]]] = []
    missing_primary = deepcopy(record)
    missing_primary["primary_box"] = ""
    cases.append(("MISSING_PRIMARY_BOX", missing_primary))

    multiple_primary = deepcopy(record)
    multiple_primary["primary_box"] = "Box A and Box B"
    cases.append(("MULTIPLE_PRIMARY_BOXES", multiple_primary))

    outside_undeclared = deepcopy(record)
    outside_undeclared["files_outside_owner_paths"] = ["other_box/private.py"]
    cases.append(("UNDECLARED_OUTSIDE_TOUCH", outside_undeclared))

    missing_contract = deepcopy(record)
    missing_contract["public_contract"] = ""
    cases.append(("MISSING_PUBLIC_CONTRACT", missing_contract))

    unresolved_owner = deepcopy(record)
    unresolved_owner["validation_owner"] = "UNKNOWN"
    cases.append(("UNRESOLVED_OWNER", unresolved_owner))

    missing_tests = deepcopy(record)
    missing_tests["boundary_tests"] = []
    cases.append(("MISSING_BOUNDARY_TEST", missing_tests))

    wrong_state = deepcopy(record)
    wrong_state["owns_mutable_state"] = True
    cases.append(("MUTABLE_STATE_OWNER_INCOMPLETE", wrong_state))

    blocked = deepcopy(record)
    blocked["decision"] = "BLOCKED"
    cases.append(("BLOCKED_DECISION", blocked))

    coding = deepcopy(record)
    coding["may_begin_coding"] = True
    cases.append(("CODING_AUTHORIZED", coding))

    for name, candidate in cases:
        _expect_rejection(name, candidate)


def _validate_sources(project_root: Path) -> None:
    paths = {
        "brick": project_root / BRICK_WALL_REL,
        "brick_meta": project_root / BRICK_META_REL,
        "bridge": project_root / BRIDGE_REL,
        "bridge_meta": project_root / BRIDGE_META_REL,
        "box": project_root / BOX_CANON_REL,
        "q07_validator": project_root / Q07_VALIDATOR_REL,
        "q08_validator": project_root / Q08_VALIDATOR_REL,
    }
    for path in paths.values():
        _gate("Q08_REQUIRED_FILE", path.is_file(), str(path))

    brick = _read_text(paths["brick"])
    bridge = _read_text(paths["bridge"])
    box = _read_text(paths["box"])
    q07_validator = _read_text(paths["q07_validator"])

    _require_fragments(brick, BRICK_FIELDS, "Q08_BRICK_WALL_ENFORCEMENT")
    _require_fragments(bridge, BRIDGE_FIELDS, "Q08_ROUTER_BRIDGE_ENFORCEMENT")
    _require_fragments(box, ("## 13. Box Boundary Audit", *CANON_FIELDS), "Q08_CANONICAL_AUDIT_OWNER")

    _gate(
        "Q08_NO_COMPETING_BOX_SCHEMA",
        "do not create a competing box schema" in brick
        and "do not create a competing box schema" in bridge,
    )
    _gate(
        "Q08_Q07_FORWARD_COMPATIBLE",
        "bool(source_stage) and source_stage == updated_for" in q07_validator
        and '_parse_version(metadata.get("version")) >= minimum' in q07_validator,
    )

    metadata_requirements = (
        (paths["brick_meta"], (1, 8), "Brick Wall"),
        (paths["bridge_meta"], (2, 2), "router bridge"),
    )
    for path, minimum, label in metadata_requirements:
        metadata = _load_json(path)
        _gate("Q08_METADATA_VERSION", _parse_version(metadata.get("version")) >= minimum, label)
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        _gate("Q08_METADATA_ALIGNMENT", bool(source_stage) and source_stage == updated_for, label)
        _gate("Q08_METADATA_DESCRIPTION", "Q08" in str(metadata.get("description", "")), label)
        _gate(
            "Q08_METADATA_DO_NOT_REGRESS",
            any("Q08" in str(item) for item in metadata.get("do_not_regress", [])),
            label,
        )

    for path in (paths["brick"], paths["bridge"], paths["q07_validator"], paths["q08_validator"]):
        line_count = len(_read_text(path).splitlines())
        _gate("Q08_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")

    _gate("Q08_ONE_PRIMARY_BOX", "one primary box" in brick.lower() and "one primary box" in bridge.lower())
    _gate("Q08_Q09_PROGRESSION", "proceed to Q09" in brick and "May proceed to Q09" in bridge)
    _gate("Q08_CODING_REMAINS_BLOCKED", "may begin coding NO" in brick and "coding `NO`" in bridge)
    _gate("Q08_NO_NEW_ENGINE_OR_SCHEMA", "new engine" not in brick.lower() and "competing box schema" in brick)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    project_root = args.project_root.resolve()

    _validate_sources(project_root)
    _validate_record_matrix()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
