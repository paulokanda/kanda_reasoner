"""Validate the Class 07 Prompt Library foundation correction."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path
from typing import Any

FEATURE_ID = "prompt-library-class07-foundation-correction-v1"
PROMPT_ROOT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit"
)
METADATA_ROOT_REL = Path("kanda_prompt_workspace/prompt_library/METADATA")

PROMPT_SPECS = {
    "project_specific_prompt_generalization": {
        "version": "2.0",
        "load_type": "on_request",
        "code": "",
        "required": [
            "GENERALIZATION RECORD",
            "semantic loss",
            "PROJECT_OVERLAY",
            "NEW_PROMPT_CANDIDATE",
            "source-write authorization: `NO`",
        ],
    },
    "prompt_audit_canon": {
        "version": "2.0",
        "load_type": "on_request",
        "code": "",
        "required": [
            "One-primary-target rule",
            "Adaptive sequential batches",
            "The audit identifies",
            "formally closed",
            "not implementation authorization",
        ],
    },
    "prompt_canon_reconciliation_protocol": {
        "version": "2.0",
        "load_type": "on_request",
        "code": "",
        "required": [
            "Decision order",
            "CREATE_NEW_PROMPT",
            "one canonical semantic owner",
            "PROMPT CANON RECONCILIATION RECORD",
            "source-write authorization: `NO`",
        ],
    },
    "prompt_identity_code_registry_canon": {
        "version": "2.0",
        "load_type": "routed",
        "code": "KPR-07-002",
        "required": [
            "partially migrated",
            "KPR-07-001",
            "KPR-07-002",
            "Do not create a new central registry",
            "NO_CODE_REQUIRED",
        ],
    },
    "prompt_insertion_and_router_registration_protocol": {
        "version": "2.0",
        "load_type": "routed",
        "code": "KPR-07-001",
        "required": [
            "Required upstream decisions",
            "Immediate freshness gate",
            "Atomic implementation",
            "idempotent",
            "Loading this prompt does not authorize",
            "never `project_freeze_ledger`",
        ],
    },
}

EXACT_PROMPT_IDS = list(PROMPT_SPECS)


class ValidationError(RuntimeError):
    """Raised when the focused validation fails."""


def require(condition: bool, message: str) -> None:
    """Raise ValidationError when condition is false."""
    if not condition:
        raise ValidationError(message)


def read_text(path: Path) -> str:
    """Read UTF-8 text and reject BOM or CRLF drift."""
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF8_BOM_FORBIDDEN: {path}")
    require(b"\r\n" not in raw, f"CRLF_FORBIDDEN: {path}")
    return raw.decode("utf-8")


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON document."""
    return json.loads(read_text(path))


def parse_version(value: object) -> tuple[int, ...]:
    """Parse a dotted numeric version for forward-compatible checks."""
    require(isinstance(value, str) and bool(value.strip()), "VERSION_MISSING")
    parts = value.split(".")
    require(all(part.isdigit() for part in parts), f"VERSION_INVALID: {value}")
    return tuple(int(part) for part in parts)


def parse_front_matter(text: str) -> dict[str, str]:
    """Parse the flat scalar fields used by focused prompt front matter."""
    lines = text.splitlines()
    require(lines and lines[0] == "---", "FRONT_MATTER_START_MISSING")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError("FRONT_MATTER_END_MISSING") from exc

    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def validate_prompt_and_metadata(project_root: Path) -> None:
    """Validate all five canonical Class 07 stage owners."""
    prompt_root = project_root / PROMPT_ROOT_REL
    metadata_root = project_root / METADATA_ROOT_REL

    seen_codes: set[str] = set()
    for prompt_id, spec in PROMPT_SPECS.items():
        prompt_path = prompt_root / f"{prompt_id}.md"
        metadata_path = metadata_root / f"{prompt_id}.meta.json"
        require(prompt_path.is_file(), f"PROMPT_MISSING: {prompt_path}")
        require(metadata_path.is_file(), f"METADATA_MISSING: {metadata_path}")

        source = read_text(prompt_path)
        metadata = load_json(metadata_path)
        require(isinstance(metadata, dict), f"METADATA_NOT_OBJECT: {metadata_path}")
        front = parse_front_matter(source)

        line_count = len(source.splitlines())
        require(line_count <= 500, f"MODULE_SIZE_MAX_EXCEEDED: {prompt_path} {line_count}")
        require("E:\\kanda_reasoner" not in source, f"HARDCODED_ROOT: {prompt_path}")

        require(front.get("prompt_id") == prompt_id, f"SOURCE_PROMPT_ID_MISMATCH: {prompt_id}")
        require(front.get("version") == spec["version"], f"SOURCE_VERSION_MISMATCH: {prompt_id}")
        require(front.get("status") == "active", f"SOURCE_STATUS_MISMATCH: {prompt_id}")
        require(front.get("load_type") == spec["load_type"], f"SOURCE_LOAD_TYPE_MISMATCH: {prompt_id}")
        require(front.get("owner_box") == "07_prompt_authoring_and_audit", f"SOURCE_OWNER_MISMATCH: {prompt_id}")

        expected_code = spec["code"]
        require(front.get("prompt_code", "") == expected_code, f"SOURCE_CODE_MISMATCH: {prompt_id}")
        if expected_code:
            require(expected_code not in seen_codes, f"DUPLICATE_CODE: {expected_code}")
            seen_codes.add(expected_code)

        require(metadata.get("prompt_id") == prompt_id, f"METADATA_PROMPT_ID_MISMATCH: {prompt_id}")
        require(metadata.get("version") == spec["version"], f"METADATA_VERSION_MISMATCH: {prompt_id}")
        require(metadata.get("status") == "active", f"METADATA_STATUS_MISMATCH: {prompt_id}")
        require(metadata.get("load_type") == spec["load_type"], f"METADATA_LOAD_TYPE_MISMATCH: {prompt_id}")
        require(metadata.get("owner_box") == "07_prompt_authoring_and_audit", f"METADATA_OWNER_MISMATCH: {prompt_id}")
        require(metadata.get("prompt_code", "") == expected_code, f"METADATA_CODE_MISMATCH: {prompt_id}")
        require(metadata.get("source_stage") == FEATURE_ID, f"METADATA_SOURCE_STAGE_MISMATCH: {prompt_id}")
        require(bool(metadata.get("updated_for")), f"METADATA_UPDATED_FOR_MISSING: {prompt_id}")
        require(bool(metadata.get("canonical_path")), f"METADATA_CANONICAL_PATH_MISSING: {prompt_id}")

        for marker in spec["required"]:
            require(marker in source, f"REQUIRED_MARKER_MISSING: {prompt_id}: {marker}")

    require(seen_codes == {"KPR-07-001", "KPR-07-002"}, "CLASS07_CODE_SET_MISMATCH")
    print("CLASS07_PROMPT_METADATA_ALIGNMENT: PASS")
    print("CLASS07_MODULE_SIZE_AND_ENCODING: PASS")
    print("CLASS07_CODE_RESERVATIONS: PASS")


def validate_stage_boundaries(project_root: Path) -> None:
    """Validate the five stage owners do not collapse into one mega-owner."""
    root = project_root / PROMPT_ROOT_REL
    audit = read_text(root / "prompt_audit_canon.md")
    reconcile = read_text(root / "prompt_canon_reconciliation_protocol.md")
    generalize = read_text(root / "project_specific_prompt_generalization.md")
    identity = read_text(root / "prompt_identity_code_registry_canon.md")
    insertion = read_text(root / "prompt_insertion_and_router_registration_protocol.md")

    require("must not modify" in audit.lower(), "AUDIT_READ_ONLY_RULE_MISSING")
    require("does not perform source mutation" in reconcile.lower(), "RECONCILIATION_READ_ONLY_RULE_MISSING")
    require("does not authorize Prompt Library writes" in generalize, "GENERALIZATION_NON_AUTH_MISSING")
    require("does not audit semantic duplication" in identity, "IDENTITY_DELEGATION_MISSING")
    require("consumes upstream decisions" in insertion, "INSERTION_UPSTREAM_BOUNDARY_MISSING")
    require("Class 02 owns routing architecture" in insertion, "INSERTION_ROUTING_DELEGATION_MISSING")
    require("current Class 05" in insertion, "INSERTION_DELIVERY_DELEGATION_MISSING")
    require("current freeze owners" in insertion, "INSERTION_FREEZE_DELEGATION_MISSING")

    print("CLASS07_ONE_OWNER_PER_STAGE: PASS")
    print("CLASS07_NO_MEGA_PROTOCOL_OWNERSHIP: PASS")


def validate_indexes(project_root: Path) -> None:
    """Validate folder, group, and routing inventories."""
    library = project_root / "kanda_prompt_workspace/prompt_library"

    groups = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in groups["groups"] if item.get("group_id") == "07_prompt_authoring_and_audit")
    require(group.get("prompt_ids") == EXACT_PROMPT_IDS, "PROMPT_GROUP_DRAFT_CLASS07_MISMATCH")

    route_groups = load_json(library / "ROUTING/group_assimilation_index.json")
    route_group = next(item for item in route_groups["groups"] if item.get("group_id") == "07_prompt_authoring_and_audit")
    require(route_group.get("prompt_count") == 5, "GROUP_ROUTE_PROMPT_COUNT_MISMATCH")
    require(route_group.get("main_prompts") == [f"{item}.md" for item in EXACT_PROMPT_IDS], "GROUP_ROUTE_MAIN_PROMPTS_MISMATCH")
    require(route_group.get("phase_1_folder_card_status") == "active_current", "GROUP_ROUTE_FOLDER_CARD_STATUS_MISMATCH")

    cards = load_json(library / "ROUTING/folder_assimilation_cards_index.json")
    card = next(item for item in cards["folders"] if item.get("folder_id") == "07_prompt_authoring_and_audit")
    require(card.get("prompt_count") == 5, "FOLDER_CARD_PROMPT_COUNT_MISMATCH")
    require(card.get("main_prompt_ids") == EXACT_PROMPT_IDS, "FOLDER_CARD_PROMPT_IDS_MISMATCH")

    card_source = read_text(project_root / PROMPT_ROOT_REL / "_FOLDER_ASSIMILATION.md")
    for prompt_id in EXACT_PROMPT_IDS:
        require(prompt_id in card_source, f"FOLDER_CARD_PROMPT_MISSING: {prompt_id}")

    card_metadata = load_json(
        library / "METADATA/folder_assimilation_07_prompt_authoring_and_audit.meta.json"
    )
    require(card_metadata.get("version") == "2.0", "FOLDER_CARD_METADATA_VERSION_MISMATCH")
    require(card_metadata.get("source_stage") == FEATURE_ID, "FOLDER_CARD_METADATA_STAGE_MISMATCH")

    navigation = read_text(
        library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
    )
    require("KPR-07-001 = prompt_insertion_and_router_registration_protocol" in navigation, "NAV_KPR_07001_MISSING")
    require("KPR-07-002 = prompt_identity_code_registry_canon" in navigation, "NAV_KPR_07002_MISSING")
    require("directly addressable" in navigation, "NAV_PARTIAL_MIGRATION_RULE_MISSING")
    navigation_metadata = load_json(library / "METADATA/prompt_navigation_index.meta.json")
    require(
        parse_version(navigation_metadata.get("version")) >= parse_version("2.1"),
        "NAV_METADATA_VERSION_MISMATCH",
    )
    navigation_stage = navigation_metadata.get("source_stage")
    navigation_updated_for = navigation_metadata.get("updated_for")
    require(bool(navigation_stage), "NAV_METADATA_STAGE_MISSING")
    require(bool(navigation_updated_for), "NAV_METADATA_UPDATED_FOR_MISSING")
    require(
        navigation_stage == navigation_updated_for,
        "NAV_METADATA_PROVENANCE_MISMATCH",
    )

    print("CLASS07_GROUP_AND_FOLDER_INVENTORIES: PASS")
    print("CLASS07_ROUTING_IDENTITY_VISIBILITY: PASS")


def validate_negative_controls() -> None:
    """Prove selected semantic guards fail when their contract is removed."""
    try:
        require(False, "negative control")
    except ValidationError:
        pass
    else:
        raise ValidationError("NEGATIVE_CONTROL_REQUIRE_FAILED")

    sample = "Loading this prompt does not authorize a mutation."
    require("does not authorize" in sample, "NEGATIVE_CONTROL_BASELINE")
    mutated = sample.replace("does not authorize", "authorizes")
    caught = False
    try:
        require("does not authorize" in mutated, "NEGATIVE_CONTROL_NON_AUTH")
    except ValidationError:
        caught = True
    require(caught, "NEGATIVE_CONTROL_MUTANT_SURVIVED")

    print("CLASS07_NEGATIVE_GUARD_CONTROLS: PASS")


def main() -> int:
    """Run focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve()

    try:
        validate_prompt_and_metadata(project_root)
        validate_stage_boundaries(project_root)
        validate_indexes(project_root)
        validate_negative_controls()
    except (ValidationError, KeyError, StopIteration, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"CLASS07 VALIDATION ERROR: {exc}")
        return 1

    print("CLASS07_FOUNDATION_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
