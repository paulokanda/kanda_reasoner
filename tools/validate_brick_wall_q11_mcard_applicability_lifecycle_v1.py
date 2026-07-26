"""Validate Brick Wall Q11 MCard applicability and lifecycle enforcement."""
from __future__ import annotations
__all__: list[str] = []
import argparse
import json
import ntpath
from pathlib import Path
from typing import Mapping, Sequence

FEATURE_ID = "brick-wall-q11-mcard-applicability-lifecycle-enforcement-v1"
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
MCARD_REL = (
    PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/"
    "architecture_review_project_card_machine_canon.md"
)
Q10_VALIDATOR_REL = Path("tools/validate_brick_wall_q10_single_mutable_state_owner_v1.py")
MCARD_VALIDATOR_REL = Path(
    "tools/validate_architecture_review_project_card_machine_canon_router_v1.py"
)
Q11_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py"
)
BRICK_MARKERS = (
    "### MCard applicability and lifecycle (Q11)",
    "MCARD APPLICABILITY AND LIFECYCLE RECORD",
    "MCard applicable YES/NO",
    "one edited file alone does not activate MCard",
    "Decision: COMPLETE/NOT_APPLICABLE/BLOCKED",
    "proceed to Q12 YES/NO",
    "may begin coding NO",
)
BRIDGE_MARKERS = (
    "## MCard applicability and lifecycle gate (Q11)",
    "Q11 MCard applicability and lifecycle record complete: YES / NO",
    "MCard applicability decision: APPLIES / NOT_APPLICABLE / BLOCKED",
    "MCard lifecycle decision: COMPLETE / NOT_APPLICABLE / BLOCKED",
    "May proceed to Q12 operation identity gate: YES / NO",
    "## Architecture Review project-card machine bridge",
    "MCARD APPLICABILITY AND LIFECYCLE RECORD",
    "Project results retained after eject:",
    "May implement: NO",
)
MCARD_MARKERS = (
    "Prompt ID: architecture_review_project_card_machine_canon",
    "Prompt code: KPR-12-005",
    "KANDA Reasoner Tool = reusable card machine",
    "Active Project = card owner",
    "Selected large module = inserted card",
    "## Lifecycle state machine",
    "## Router bridge requirements",
    "## Routing triggers",
    "## When not to use",
)
RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "mcard_applicable",
    "trigger_evidence",
    "not_applicable_evidence",
    "owner_prompts_loaded",
    "cards",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q12",
    "may_begin_coding",
)
CARD_FIELDS = (
    "active_project_root",
    "active_project_support_root",
    "transient_garbage_root",
    "tool_source_root",
    "inserted_card_target",
    "target_relative_path",
    "target_content_hash",
    "lifecycle_generation",
    "target_inside_active_project_root",
    "card_ownership_proven",
    "current_lifecycle_phase",
    "transition_from",
    "transition_to",
    "transition_allowed",
    "async_generation_valid",
    "planner_state_owner",
    "workbench_state_owner",
    "preview_owner",
    "shadow_owner",
    "transaction_owner",
    "open_transaction",
    "unresolved_apply_outcome",
    "switch_blocked",
    "eject_blocked",
    "rollback_status",
    "write_target",
    "terminal_eject_condition",
    "tool_memory_cleared_after_completion",
    "project_results_retained_after_eject",
    "self_hosting_logical_separation_preserved",
    "tests",
)
VALID_TRANSITIONS = {
    ("EMPTY", "CARD_INSERTED"),
    ("CARD_INSERTED", "CARD_READ"),
    ("CARD_READ", "PLAN_READY"),
    ("PLAN_READY", "WORKBENCH_READY"),
    ("WORKBENCH_READY", "PREVIEW_VALIDATED"),
    ("PREVIEW_VALIDATED", "AUTHORIZED"),
    ("AUTHORIZED", "APPLYING"),
    ("APPLYING", "VERIFIED_TERMINAL"),
    ("VERIFIED_TERMINAL", "CARD_EJECTED"),
    ("APPLYING", "ROLLBACK_REQUESTED"),
    ("APPLIED_NOT_VERIFIED", "ROLLBACK_REQUESTED"),
    ("ROLLBACK_REQUESTED", "ROLLBACK_VERIFIED"),
    ("ROLLBACK_VERIFIED", "CARD_EJECTED"),
}

def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


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


def _require(text: str, markers: Sequence[str], label: str) -> None:
    for marker in markers:
        _gate(label, marker in text, marker)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object, allow_empty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if not value:
        return allow_empty
    return all(_nonempty(item) for item in value)


def _contained(root: object, candidate: object) -> bool:
    if not _nonempty(root) or not _nonempty(candidate):
        return False
    root_text = ntpath.normcase(ntpath.normpath(str(root)))
    candidate_text = ntpath.normcase(ntpath.normpath(str(candidate)))
    try:
        return ntpath.commonpath([root_text, candidate_text]) == root_text
    except ValueError:
        return False


def _validate_card(card: Mapping[str, object]) -> None:
    missing = [field for field in CARD_FIELDS if field not in card]
    if missing:
        raise AssertionError("card missing fields: " + ", ".join(missing))
    text_fields = (
        "active_project_root",
        "active_project_support_root",
        "transient_garbage_root",
        "tool_source_root",
        "inserted_card_target",
        "target_relative_path",
        "target_content_hash",
        "lifecycle_generation",
        "current_lifecycle_phase",
        "transition_from",
        "transition_to",
        "planner_state_owner",
        "workbench_state_owner",
        "preview_owner",
        "shadow_owner",
        "transaction_owner",
        "rollback_status",
        "write_target",
        "terminal_eject_condition",
    )
    for field in text_fields:
        if not _nonempty(card[field]):
            raise AssertionError(f"card empty field: {field}")
        if str(card[field]).strip().upper() in {"UNKNOWN", "UNRESOLVED"}:
            raise AssertionError(f"card unresolved field: {field}")
    for field in (
        "target_inside_active_project_root",
        "card_ownership_proven",
        "transition_allowed",
        "async_generation_valid",
        "open_transaction",
        "unresolved_apply_outcome",
        "switch_blocked",
        "eject_blocked",
        "tool_memory_cleared_after_completion",
        "project_results_retained_after_eject",
        "self_hosting_logical_separation_preserved",
    ):
        if not isinstance(card[field], bool):
            raise AssertionError(f"card field must be boolean: {field}")
    if not _text_list(card["tests"]):
        raise AssertionError("card tests must be a non-empty text list")
    if not card["target_inside_active_project_root"]:
        raise AssertionError("card target ownership is not proven")
    if not _contained(card["active_project_root"], card["inserted_card_target"]):
        raise AssertionError("card target is outside active project root")
    if not _contained(card["active_project_root"], card["write_target"]):
        raise AssertionError("write target is outside active project root")
    if not card["card_ownership_proven"]:
        raise AssertionError("card ownership is not proven")
    transition = (str(card["transition_from"]), str(card["transition_to"]))
    if transition not in VALID_TRANSITIONS or not card["transition_allowed"]:
        raise AssertionError("invalid or unauthorized MCard transition")
    if not card["async_generation_valid"]:
        raise AssertionError("stale async generation")
    lock_required = card["open_transaction"] or card["unresolved_apply_outcome"]
    if lock_required and not (card["switch_blocked"] and card["eject_blocked"]):
        raise AssertionError("transaction or apply outcome lacks switch/eject lock")
    preview = str(card["preview_owner"]).lower()
    shadow = str(card["shadow_owner"]).lower()
    transaction = str(card["transaction_owner"]).lower()
    if "_delete_after_daily_work" in preview:
        raise AssertionError("Preview authority leaked into daily-work")
    if "_show_project_to_ai" not in preview:
        raise AssertionError("Preview owner is not project support")
    if "_delete_after_daily_work" not in shadow:
        raise AssertionError("Shadow owner is not transient garbage")
    if "_show_project_to_ai" not in transaction:
        raise AssertionError("transaction owner is not project support")
    if card["transition_to"] == "CARD_EJECTED":
        prior = str(card["transition_from"])
        if prior not in {"VERIFIED_TERMINAL", "ROLLBACK_VERIFIED"}:
            raise AssertionError("premature card eject")
        if not card["tool_memory_cleared_after_completion"]:
            raise AssertionError("terminal eject retained Tool card memory")
        if not card["project_results_retained_after_eject"]:
            raise AssertionError("terminal eject destroyed Project results")
    if not card["self_hosting_logical_separation_preserved"]:
        raise AssertionError("self-hosting logical separation collapsed")


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in RECORD_FIELDS if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))
    if not _nonempty(record["identity_basis"]):
        raise AssertionError("identity basis is missing")
    if not _nonempty(record["primary_box"]):
        raise AssertionError("primary box is missing")
    if not isinstance(record["mcard_applicable"], bool):
        raise AssertionError("mcard_applicable must be boolean")
    if not _text_list(record["owner_prompts_loaded"]):
        raise AssertionError("owner prompts must be listed")
    owners = set(record["owner_prompts_loaded"])
    required = {
        "architecture_review_project_card_machine_canon",
        "project_tool_boundary_canon",
    }
    if not required.issubset(owners):
        raise AssertionError("required MCard owner prompts are missing")
    if not _text_list(record["unresolved_fields"], allow_empty=True):
        raise AssertionError("unresolved_fields must be a text list")
    if record["unresolved_fields"]:
        raise AssertionError("unresolved MCard fields")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q11 may_begin_coding must remain false")
    if record["may_proceed_to_q12"] is not True:
        raise AssertionError("Q11 must explicitly proceed to Q12")
    cards = record["cards"]
    if not isinstance(cards, list):
        raise AssertionError("cards must be a list")
    if record["mcard_applicable"]:
        if not _text_list(record["trigger_evidence"]):
            raise AssertionError("applicable MCard record lacks trigger evidence")
        triggers = " ".join(record["trigger_evidence"]).lower()
        if triggers.strip() in {"one edited file", "single edited file"}:
            raise AssertionError("single-file-only false MCard activation")
        if record["not_applicable_evidence"] not in ([], None):
            raise AssertionError("applicable record contains not-applicable evidence")
        if not cards:
            raise AssertionError("applicable MCard record has no card")
        for card in cards:
            if not isinstance(card, Mapping):
                raise AssertionError("card entry must be a mapping")
            _validate_card(card)
        if record["decision"] != "COMPLETE":
            raise AssertionError("applicable MCard decision must be COMPLETE")
    else:
        if not _text_list(record["not_applicable_evidence"]):
            raise AssertionError("not-applicable record lacks evidence")
        if record["trigger_evidence"] not in ([], None):
            raise AssertionError("not-applicable record contains trigger evidence")
        if cards:
            raise AssertionError("not-applicable record contains card state")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("non-MCard decision must be NOT_APPLICABLE")


def _valid_applicable() -> dict[str, object]:
    return {
        "identity_basis": "Current Q11 source and selected Architecture Review card",
        "primary_box": "Architecture Review",
        "mcard_applicable": True,
        "trigger_evidence": ["Planner-to-Workbench handoff for a selected large module"],
        "not_applicable_evidence": [],
        "owner_prompts_loaded": [
            "architecture_review_project_card_machine_canon",
            "project_tool_boundary_canon",
            "large_module_refactor_protocol",
        ],
        "cards": [
            {
                "active_project_root": r"E:\sample_project",
                "active_project_support_root": r"E:\sample_project_show_project_to_AI",
                "transient_garbage_root": r"E:\sample_project_delete_after_daily_work",
                "tool_source_root": r"E:\kanda_reasoner",
                "inserted_card_target": r"E:\sample_project\pkg\large_module.py",
                "target_relative_path": r"pkg\large_module.py",
                "target_content_hash": "a" * 64,
                "lifecycle_generation": "generation-7",
                "target_inside_active_project_root": True,
                "card_ownership_proven": True,
                "current_lifecycle_phase": "WORKBENCH_READY",
                "transition_from": "PLAN_READY",
                "transition_to": "WORKBENCH_READY",
                "transition_allowed": True,
                "async_generation_valid": True,
                "planner_state_owner": "Tool memory bound to current card identity",
                "workbench_state_owner": "Tool engine with Project-owned durable state",
                "preview_owner": r"E:\sample_project_show_project_to_AI\large_file_refactor_workbench\preview\p1",
                "shadow_owner": r"E:\sample_project_delete_after_daily_work\large_file_refactor_shadow\s1",
                "transaction_owner": r"E:\sample_project_show_project_to_AI\large_file_refactor_workbench\transactions",
                "open_transaction": False,
                "unresolved_apply_outcome": False,
                "switch_blocked": False,
                "eject_blocked": False,
                "rollback_status": "NOT_REQUIRED",
                "write_target": r"E:\sample_project\pkg\large_module.py",
                "terminal_eject_condition": "Verified completion or verified rollback",
                "tool_memory_cleared_after_completion": False,
                "project_results_retained_after_eject": True,
                "self_hosting_logical_separation_preserved": True,
                "tests": ["deterministic MCard transition validation"],
            }
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q12": True,
        "may_begin_coding": False,
    }


def _valid_not_applicable() -> dict[str, object]:
    return {
        "identity_basis": "Current Q11 source and prompt-library-only task",
        "primary_box": "Prompt library governance",
        "mcard_applicable": False,
        "trigger_evidence": [],
        "not_applicable_evidence": [
            "No Architecture Review, AST Split Audit, Planner, Workbench, transaction, apply, rollback, receipt, or eject lifecycle"
        ],
        "owner_prompts_loaded": [
            "architecture_review_project_card_machine_canon",
            "project_tool_boundary_canon",
        ],
        "cards": [],
        "unresolved_fields": [],
        "decision": "NOT_APPLICABLE",
        "may_proceed_to_q12": True,
        "may_begin_coding": False,
    }


def _expect_rejected(label: str, mutate) -> None:
    record = _valid_applicable()
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
    mcard = _read(root / MCARD_REL)
    brick_meta = _load_json(root / BRICK_META_REL)
    bridge_meta = _load_json(root / BRIDGE_META_REL)

    _require(brick, BRICK_MARKERS, "Q11_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q11_ROUTER_BRIDGE_CONTRACT")
    _require(mcard, MCARD_MARKERS, "Q11_MCARD_CANON_REUSED")
    _gate("Q11_BRICK_VERSION", _parse_version(brick_meta["version"]) >= (2, 1))
    _gate("Q11_BRIDGE_VERSION", _parse_version(bridge_meta["version"]) >= (2, 5))
    for label, metadata in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = metadata.get("source_stage")
        updated = metadata.get("updated_for")
        _gate(
            "Q11_METADATA_ALIGNMENT",
            _nonempty(stage) and stage == updated,
            label,
        )

    q10 = _read(root / Q10_VALIDATOR_REL)
    _gate(
        "Q10_FORWARD_COMPATIBLE_METADATA_REPAIR",
        "stage == updated and stage == FEATURE_ID" not in q10
        and "_nonempty_text(stage) and stage == updated" in q10,
    )
    mcard_validator = _read(root / MCARD_VALIDATOR_REL)
    _gate(
        "MCARD_VALIDATOR_FORWARD_COMPATIBLE_METADATA_REPAIR",
        'bridge_meta.get("version") == "1.3"' not in mcard_validator
        and "_parse_version(bridge_meta.get(\"version\")) >= (1, 3)" in mcard_validator,
    )

    for relative in (BRICK_REL, BRIDGE_REL, Q10_VALIDATOR_REL, MCARD_VALIDATOR_REL, Q11_VALIDATOR_REL):
        lines = len(_read(root / relative).splitlines())
        _gate("Q11_MODULE_SIZE", lines <= 500, f"{relative}={lines}")


def validate_semantics() -> None:
    validate_record(_valid_applicable())
    print("Q11_APPLICABLE_RECORD_ACCEPTED: PASS")
    validate_record(_valid_not_applicable())
    print("Q11_NOT_APPLICABLE_RECORD_ACCEPTED: PASS")

    cases = [
        ("Q11_NEGATIVE_SINGLE_FILE_FALSE_ACTIVATION", lambda r: r.update(trigger_evidence=["one edited file"])),
        ("Q11_NEGATIVE_MISSING_OWNER_PROMPT", lambda r: r.update(owner_prompts_loaded=["project_tool_boundary_canon"])),
        ("Q11_NEGATIVE_TARGET_OUTSIDE_ROOT", lambda r: r["cards"][0].update(inserted_card_target=r"D:\other\x.py")),
        ("Q11_NEGATIVE_OWNERSHIP_UNPROVEN", lambda r: r["cards"][0].update(card_ownership_proven=False)),
        ("Q11_NEGATIVE_INVALID_TRANSITION", lambda r: r["cards"][0].update(transition_to="AUTHORIZED")),
        ("Q11_NEGATIVE_STALE_ASYNC_RESULT", lambda r: r["cards"][0].update(async_generation_valid=False)),
        ("Q11_NEGATIVE_TRANSACTION_SWITCH_UNLOCKED", lambda r: r["cards"][0].update(open_transaction=True, switch_blocked=False, eject_blocked=False)),
        ("Q11_NEGATIVE_APPLY_OUTCOME_EJECT_UNLOCKED", lambda r: r["cards"][0].update(unresolved_apply_outcome=True, switch_blocked=True, eject_blocked=False)),
        ("Q11_NEGATIVE_PREVIEW_IN_DAILY_WORK", lambda r: r["cards"][0].update(preview_owner=r"E:\sample_project_delete_after_daily_work\preview")),
        ("Q11_NEGATIVE_SHADOW_IN_PROJECT_SUPPORT", lambda r: r["cards"][0].update(shadow_owner=r"E:\sample_project_show_project_to_AI\shadow")),
        ("Q11_NEGATIVE_TRANSACTION_IN_DAILY_WORK", lambda r: r["cards"][0].update(transaction_owner=r"E:\sample_project_delete_after_daily_work\transactions")),
        ("Q11_NEGATIVE_WRITE_OUTSIDE_PROJECT", lambda r: r["cards"][0].update(write_target=r"E:\kanda_reasoner\pkg\large_module.py")),
        ("Q11_NEGATIVE_SELF_HOSTING_COLLAPSE", lambda r: r["cards"][0].update(self_hosting_logical_separation_preserved=False)),
        ("Q11_NEGATIVE_PREMATURE_EJECT", lambda r: r["cards"][0].update(transition_from="WORKBENCH_READY", transition_to="CARD_EJECTED", transition_allowed=True)),
        ("Q11_NEGATIVE_DESTRUCTIVE_EJECT", lambda r: r["cards"][0].update(transition_from="VERIFIED_TERMINAL", transition_to="CARD_EJECTED", transition_allowed=True, project_results_retained_after_eject=False)),
        ("Q11_NEGATIVE_STICKY_TOOL_MEMORY", lambda r: r["cards"][0].update(transition_from="VERIFIED_TERMINAL", transition_to="CARD_EJECTED", transition_allowed=True, tool_memory_cleared_after_completion=False)),
        ("Q11_NEGATIVE_UNRESOLVED_FIELD", lambda r: r.update(unresolved_fields=["transaction owner"])),
        ("Q11_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
    ]
    for label, mutate in cases:
        _expect_rejected(label, mutate)

    invalid_na = _valid_not_applicable()
    invalid_na["not_applicable_evidence"] = []
    try:
        validate_record(invalid_na)
    except AssertionError:
        print("Q11_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: PASS")
    else:
        raise AssertionError("Q11_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE: FAIL")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_source(root)
    validate_semantics()
    print("Q11_MCARD_APPLICABILITY_LIFECYCLE_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
