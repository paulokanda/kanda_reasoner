"""Validate Brick Wall Q07 ownership and NO-LEAK classification."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q07-ownership-no-leak-classification-enforcement-v1"
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
Q06_VALIDATOR_REL = Path("tools/validate_brick_wall_q06_tool_project_identity_v1.py")
Q07_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q07_ownership_no_leak_classification_v1.py"
)

ALLOWED_CLASSIFICATIONS = set(
    "tool-owned logic|active-project source|project-specific support state|"
    "generated evidence or handoff artifact|transient garbage artifact|"
    "external box dependency|out-of-scope file".split("|")
)

RECORD_FIELDS = (
    "Identity basis | primary task owner | active box:",
    "Touched-item classifications, once per item:",
    "Item/path | classification | logical owner | owner root | authority role | ",
    "allowed action | contract/bridge | leak risk | blocked write",
    "Completeness: exactly once YES/NO; unclassified items; duplicate classifications",
    "Source/lifetime: canonical-vs-generated YES/NO; durable-vs-transient YES/NO",
    "Boundary findings: public routes; private reach-ins; wrong-root; cross-project;",
    "cross-box; mutable-state; generated-as-source; Preview/daily-work; Shadow/durable",
    "Evidence placement: validation; freeze; Error Memory; prompt/canon",
    "Leak risks | blocked writes | unresolved classifications:",
    "Decision: COMPLETE/BLOCKED | proceed to Q08 YES/NO | may begin coding NO",
)

IMPLEMENTATION_GATE_FIELDS = (
    "Q07 ownership and NO-LEAK record complete: YES / NO",
    "Ownership/NO-LEAK decision: COMPLETE / BLOCKED",
    "May proceed to Q08 Box Boundary Audit: YES / NO",
)

REGRESSION_VALIDATORS = {
    Path("tools/validate_project_tool_boundary_nested_support_root_v1.py"):
        "FORBIDDEN_NESTED_PROJECT_SUPPORT_ROOT_CANON",
    Path("tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py"):
        "ROUTER_BRIDGE_WORKBENCH_OWNERSHIP_GATE",
    Path("tools/validate_real_widget_observability_transient_fixture_v1.py"):
        "CONTROLLED_VALIDATION_FIXTURES_UNDER_TRANSIENT_GARBAGE_ROOT",
    Path("tools/validate_reasoner_symbol_atlas_main_helper_mapper_source_ready_refactor_v1.py"):
        "PREVIEW_ONLY_METADATA_REMOVED_FROM_CANONICAL_SOURCE",
    Path("tools/validate_routing_signal_scorer_similarity_runtime_source_ready_refactor_v1.py"):
        "PREVIEW_ONLY_METADATA_REMOVED_FROM_CANONICAL_SOURCE",
}


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


def _is_empty(value: object) -> bool:
    return value in (None, "", [], (), {})


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_text_sequence(value: object) -> bool:
    return isinstance(value, (list, tuple)) and bool(value) and all(
        _nonempty_text(item) for item in value
    )


def _validate_item(item: Mapping[str, object]) -> None:
    fields = (
        "item_or_path",
        "classification",
        "logical_owner",
        "owner_root",
        "authority_role",
        "allowed_action",
        "public_contract_or_approved_bridge",
        "leak_risk",
        "blocked_write",
    )
    missing = [field for field in fields if field not in item]
    if missing:
        raise AssertionError(f"item missing fields: {', '.join(missing)}")
    for field in fields:
        if not _nonempty_text(item[field]):
            raise AssertionError(f"item field is empty: {field}")
    if item["classification"] not in ALLOWED_CLASSIFICATIONS:
        raise AssertionError("unknown canonical classification")


def _validate_record(record: Mapping[str, object]) -> None:
    required = (
        "current_tool_project_identity_basis",
        "primary_task_owner",
        "active_box",
        "touched_items",
        "all_touched_items_classified_exactly_once",
        "unclassified_items",
        "duplicate_classifications",
        "canonical_source_vs_generated_complete",
        "durable_vs_transient_complete",
        "public_contract_routes",
        "private_reach_ins",
        "wrong_root_risks",
        "cross_project_risks",
        "cross_box_risks",
        "mutable_state_leakage",
        "generated_artifact_as_source_risks",
        "preview_to_daily_work_risks",
        "shadow_to_durable_authority_risks",
        "validation_evidence_placement",
        "freeze_evidence_placement",
        "error_memory_evidence_placement",
        "prompt_canon_source_placement",
        "leak_risks",
        "blocked_writes",
        "unresolved_classifications",
        "classification_decision",
        "may_proceed_to_q08",
        "may_begin_coding",
    )
    missing = [field for field in required if field not in record]
    if missing:
        raise AssertionError(f"record missing fields: {', '.join(missing)}")

    for field in (
        "current_tool_project_identity_basis",
        "primary_task_owner",
        "active_box",
        "validation_evidence_placement",
        "freeze_evidence_placement",
        "error_memory_evidence_placement",
        "prompt_canon_source_placement",
    ):
        if not _nonempty_text(record[field]):
            raise AssertionError(f"record field is empty: {field}")

    items = record["touched_items"]
    if not isinstance(items, (list, tuple)) or not items:
        raise AssertionError("touched-item classifications are missing")
    paths: list[str] = []
    for raw_item in items:
        if not isinstance(raw_item, Mapping):
            raise AssertionError("touched item is not a mapping")
        _validate_item(raw_item)
        paths.append(str(raw_item["item_or_path"]).casefold())
    if len(paths) != len(set(paths)):
        raise AssertionError("one touched item has multiple classifications")

    if record["all_touched_items_classified_exactly_once"] != "YES":
        raise AssertionError("exactly-once classification is not proven")
    for field in (
        "unclassified_items",
        "duplicate_classifications",
        "private_reach_ins",
        "wrong_root_risks",
        "cross_project_risks",
        "cross_box_risks",
        "mutable_state_leakage",
        "generated_artifact_as_source_risks",
        "preview_to_daily_work_risks",
        "shadow_to_durable_authority_risks",
        "unresolved_classifications",
    ):
        if not _is_empty(record[field]):
            raise AssertionError(f"blocking Q07 evidence remains: {field}")

    if record["canonical_source_vs_generated_complete"] != "YES":
        raise AssertionError("canonical/generated classification is incomplete")
    if record["durable_vs_transient_complete"] != "YES":
        raise AssertionError("durable/transient classification is incomplete")
    if not _nonempty_text_sequence(record["public_contract_routes"]):
        raise AssertionError("public-contract routes are missing")
    if not _nonempty_text_sequence(record["leak_risks"]):
        raise AssertionError("leak-risk assessment is missing")
    if not _nonempty_text_sequence(record["blocked_writes"]):
        raise AssertionError("blocked writes are missing")
    if record["classification_decision"] != "COMPLETE":
        raise AssertionError("Q07 decision is not COMPLETE")
    if record["may_proceed_to_q08"] != "YES":
        raise AssertionError("Q08 progression is not authorized")
    if record["may_begin_coding"] != "NO":
        raise AssertionError("Q07 must not authorize coding")


def _valid_record() -> dict[str, object]:
    return {
        "current_tool_project_identity_basis": "Q06 COMPLETE",
        "primary_task_owner": "prompt library governance box",
        "active_box": "kanda_prompt_workspace/prompt_library",
        "touched_items": [
            {
                "item_or_path": "owner.md",
                "classification": "tool-owned logic",
                "logical_owner": "prompt library",
                "owner_root": "<tool_source_root>",
                "authority_role": "canonical source",
                "allowed_action": "modify through governed prompt workflow",
                "public_contract_or_approved_bridge": "router bridge",
                "leak_risk": "generated copy could be mistaken for source",
                "blocked_write": "generated startup ZIP contents",
            },
            {
                "item_or_path": "validation.txt",
                "classification": "generated evidence or handoff artifact",
                "logical_owner": "active project support",
                "owner_root": "<active_project_support_root>",
                "authority_role": "durable validation evidence",
                "allowed_action": "write after validation",
                "public_contract_or_approved_bridge": "durable evidence route",
                "leak_risk": "daily-work-only evidence",
                "blocked_write": "<transient_garbage_root> as sole durable copy",
            },
        ],
        "all_touched_items_classified_exactly_once": "YES",
        "unclassified_items": [],
        "duplicate_classifications": [],
        "canonical_source_vs_generated_complete": "YES",
        "durable_vs_transient_complete": "YES",
        "public_contract_routes": ["prompt source -> router bridge"],
        "private_reach_ins": [],
        "wrong_root_risks": [],
        "cross_project_risks": [],
        "cross_box_risks": [],
        "mutable_state_leakage": [],
        "generated_artifact_as_source_risks": [],
        "preview_to_daily_work_risks": [],
        "shadow_to_durable_authority_risks": [],
        "validation_evidence_placement": "<active_project_support_root>",
        "freeze_evidence_placement": "<active_project_support_root>",
        "error_memory_evidence_placement": "<active_project_support_root>",
        "prompt_canon_source_placement": "canonical prompt-library source",
        "leak_risks": ["wrong-root and generated-source confusion assessed"],
        "blocked_writes": ["generated artifacts as canonical source"],
        "unresolved_classifications": [],
        "classification_decision": "COMPLETE",
        "may_proceed_to_q08": "YES",
        "may_begin_coding": "NO",
    }


def _expect_rejection(name: str, record: Mapping[str, object]) -> None:
    try:
        _validate_record(record)
    except AssertionError:
        print(f"Q07_NEGATIVE_{name}: PASS")
        return
    raise AssertionError(f"Q07_NEGATIVE_{name}: FAIL - record was accepted")


def _validate_record_semantics() -> None:
    record = _valid_record()
    _validate_record(record)
    print("Q07_COMPLETE_CLASSIFICATION_ACCEPTED: PASS")

    cases: tuple[tuple[str, str, object], ...] = (
        ("UNCLASSIFIED_ITEM", "unclassified_items", ["missing.py"]),
        ("DUPLICATE_CLASSIFICATION", "duplicate_classifications", ["owner.md"]),
        ("GENERATED_CLASSIFICATION_INCOMPLETE", "canonical_source_vs_generated_complete", "NO"),
        ("DURABLE_TRANSIENT_INCOMPLETE", "durable_vs_transient_complete", "NO"),
        ("PRIVATE_REACH_IN", "private_reach_ins", ["other_box._private"]),
        ("WRONG_ROOT", "wrong_root_risks", ["support under source"]),
        ("CROSS_PROJECT", "cross_project_risks", ["Project B target"]),
        ("CROSS_BOX", "cross_box_risks", ["undeclared box touch"]),
        ("MUTABLE_STATE_LEAK", "mutable_state_leakage", ["shared global"]),
        ("GENERATED_AS_SOURCE", "generated_artifact_as_source_risks", ["startup ZIP"]),
        ("PREVIEW_DAILY_WORK", "preview_to_daily_work_risks", ["durable Preview"]),
        ("SHADOW_DURABLE", "shadow_to_durable_authority_risks", ["Shadow promoted"]),
        ("UNRESOLVED", "unresolved_classifications", ["owner"]),
        ("BLOCKED_DECISION", "classification_decision", "BLOCKED"),
        ("Q08_NOT_AUTHORIZED", "may_proceed_to_q08", "NO"),
        ("CODING_AUTHORIZED", "may_begin_coding", "YES"),
        ("MISSING_BLOCKED_WRITES", "blocked_writes", []),
    )
    for name, field, value in cases:
        candidate = deepcopy(record)
        candidate[field] = value
        _expect_rejection(name, candidate)

    duplicate_item = deepcopy(record)
    duplicate_item["touched_items"].append(deepcopy(duplicate_item["touched_items"][0]))
    _expect_rejection("SAME_ITEM_TWICE", duplicate_item)

    unknown_class = deepcopy(record)
    unknown_class["touched_items"][0]["classification"] = "tool source alias"
    _expect_rejection("UNKNOWN_CLASSIFICATION", unknown_class)

    missing_field = deepcopy(record)
    del missing_field["touched_items"][0]["owner_root"]
    _expect_rejection("MISSING_ITEM_FIELD", missing_field)


def _validate_sources(project_root: Path) -> None:
    paths = {
        "brick": project_root / BRICK_WALL_REL,
        "brick_meta": project_root / BRICK_META_REL,
        "bridge": project_root / BRIDGE_REL,
        "bridge_meta": project_root / BRIDGE_META_REL,
        "box": project_root / BOX_CANON_REL,
        "q06_validator": project_root / Q06_VALIDATOR_REL,
        "q07_validator": project_root / Q07_VALIDATOR_REL,
    }
    for path in paths.values():
        _gate("Q07_REQUIRED_FILE", path.is_file(), str(path))

    brick = _read_text(paths["brick"])
    bridge = _read_text(paths["bridge"])
    box = _read_text(paths["box"])
    q06_validator = _read_text(paths["q06_validator"])

    _require_fragments(
        brick,
        (
            "### Ownership and NO-LEAK classification (Q07)",
            "OWNERSHIP AND NO-LEAK CLASSIFICATION RECORD",
            *RECORD_FIELDS,
        ),
        "Q07_BRICK_WALL_RECORD",
    )
    _require_fragments(
        bridge,
        (
            "## Ownership and NO-LEAK classification gate (Q07)",
            "OWNERSHIP AND NO-LEAK CLASSIFICATION RECORD",
            *IMPLEMENTATION_GATE_FIELDS,
        ),
        "Q07_ROUTER_BRIDGE_ENFORCEMENT",
    )
    _require_fragments(
        box,
        (
            "NO_LEAK_LOGIC_V1",
            "NO-LEAK CHECK",
            "tool-owned logic",
            "active-project source",
            "project-specific support state",
            "generated evidence or handoff artifact",
            "transient garbage artifact",
            "external box dependency",
            "out-of-scope file",
        ),
        "Q07_CANONICAL_CLASSIFICATION_OWNER",
    )
    _gate(
        "Q07_NO_PARALLEL_AUTHORITY",
        "a parallel classifier" in brick
        and "parallel owner" in bridge
        and "NO-LEAK authority" in brick,
    )
    _gate(
        "Q07_Q06_FORWARD_COMPATIBLE",
        "source_stage == FEATURE_ID" not in q06_validator
        and "source_stage == updated_for" in q06_validator,
    )

    metadata_requirements = (
        (paths["brick_meta"], (1, 7), "Brick Wall"),
        (paths["bridge_meta"], (2, 1), "router bridge"),
    )
    for path, minimum, label in metadata_requirements:
        metadata = _load_json(path)
        _gate(
            "Q07_METADATA_VERSION",
            _parse_version(metadata.get("version")) >= minimum,
            label,
        )
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        _gate(
            "Q07_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
        _gate(
            "Q07_METADATA_DESCRIPTION",
            "Q07" in str(metadata.get("description", "")),
            label,
        )

    for path in (
        paths["brick"],
        paths["bridge"],
        paths["q06_validator"],
        paths["q07_validator"],
    ):
        line_count = len(_read_text(path).splitlines())
        _gate("Q07_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")

    for relative_path, marker in REGRESSION_VALIDATORS.items():
        path = project_root / relative_path
        _gate("Q07_REGRESSION_VALIDATOR_PRESENT", path.is_file(), str(relative_path))
        _gate(
            "Q07_REGRESSION_MARKER_PRESENT",
            marker in _read_text(path),
            marker,
        )

    declared_touches = {
        BRICK_WALL_REL,
        BRICK_META_REL,
        BRIDGE_REL,
        BRIDGE_META_REL,
        Q07_VALIDATOR_REL,
    }
    _gate(
        "Q07_ONE_PRIMARY_BOX",
        all(
            path.as_posix().startswith("kanda_prompt_workspace/prompt_library/")
            or path.as_posix().startswith("tools/")
            for path in declared_touches
        ),
    )
    _gate(
        "Q07_NO_NEW_ENGINE_OR_SCHEMA",
        all(not str(path).startswith("kanda_reasoner_app/") for path in declared_touches),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="KANDA Reasoner project root.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    project_root = args.project_root.resolve()
    _validate_sources(project_root)
    _validate_record_semantics()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
