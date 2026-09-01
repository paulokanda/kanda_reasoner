"""Validate Brick Wall Q06 Tool/Project identity enforcement."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Mapping, Sequence
FEATURE_ID = "brick-wall-q06-tool-project-identity-enforcement-v1"
BRICK_WALL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
BOUNDARY_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)
BOUNDARY_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/project_tool_boundary_canon.meta.json"
)
NESTED_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_nested_support_root_v1.py"
)
WORKBENCH_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py"
)
Q06_VALIDATOR_REL = Path("tools/validate_brick_wall_q06_tool_project_identity_v1.py")
RECORD_FIELDS = (
    "Task classification:",
    "Operation class: TOOL_CHANGE / PROJECT_OPERATION / MIXED_GOVERNED / BLOCKED",
    "Session ID:",
    "Operation ID:",
    "Selection timestamp:",
    "Selection source:",
    "Tool project ID:",
    "Tool source root:",
    "Active Project ID:",
    "Active Project slug:",
    "Active Project root:",
    "Active Project source roots:",
    "Selected mutation root:",
    "Project root fingerprint or immutable identity:",
    "Same canonical resolved Tool/Project root: YES / NO / UNRESOLVED",
    "Self-hosting mode: YES / NO / UNRESOLVED",
    "Active Project Support root:",
    "Support-root identity and collision status:",
    "Transient workspace root:",
    "Transient namespace and cleanup owner:",
    "Requested source write targets:",
    "Tool write set:",
    "Project write set:",
    "External or cross-project paths:",
    "Cross-project access modes:",
    "Generated evidence authority: NON_AUTHORITATIVE / CANON_ASSIGNED / UNRESOLVED",
    "Generated evidence owner reference:",
    "Support security and retention profile:",
    "Identity invalidation conditions:",
    "Identity ambiguities:",
    "Identity decision: COMPLETE / BLOCKED",
    "May proceed to Q07 classification: YES / NO",
    "May begin coding: NO",
)
RETIRED_RECORD_FIELDS = (
    "Tool task or Project operation:",
    "Tool project slug:",
    "Same physical Tool/Project root:",
    "Human-selected active project evidence:",
    "Operation owner:",
    "Requested source write target:",
    "Source write target owner:",
    "Transient garbage root:",
    "Forbidden nested support root:",
    "Tool-owned reusable assets:",
    "Active-project-owned source or generated results:",
    "Project-specific durable support state:",
    "Cross-project paths involved:",
)
IMPLEMENTATION_FIELDS = (
    "Q06 Tool/Project identity record complete: YES / NO",
    "Tool/Project identity decision: COMPLETE / BLOCKED",
    "Tool task or Project operation:",
    "Tool source root:",
    "Active project root:",
    "Active project support root:",
    "Transient garbage root:",
    "Self-hosting logical separation preserved: YES / NO",
    "May proceed to Q07 classification: YES / NO",
)
ALLOWED_OPERATION_CLASSES = ("TOOL_CHANGE", "PROJECT_OPERATION", "MIXED_GOVERNED")
ALLOWED_ACCESS_MODES = ("READ", "COMPARE", "MIGRATION_SOURCE", "AUTHORIZED_WRITE")
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
def _text_sequence(value: object, *, allow_empty: bool = True) -> bool:
    if not isinstance(value, (list, tuple)):
        return False
    return (allow_empty or bool(value)) and all(_nonempty_text(item) for item in value)

def _norm(path: object) -> str:
    return str(path).replace("\\", "/").rstrip("/").casefold()

def _is_within(path: object, parent: object) -> bool:
    child = _norm(path)
    base = _norm(parent)
    return child == base or child.startswith(base + "/")

def _validate_identity_record(record: Mapping[str, object]) -> None:
    required = (
        "task_classification", "operation_class", "session_id", "operation_id",
        "selection_timestamp", "selection_source", "tool_project_id", "tool_source_root",
        "active_project_id", "active_project_slug", "active_project_root",
        "active_project_source_roots", "selected_mutation_root", "project_root_fingerprint",
        "same_canonical_root", "self_hosting_mode", "active_project_support_root",
        "support_root_identity_collision_status", "transient_workspace_root",
        "transient_namespace_cleanup_owner", "requested_source_write_targets",
        "tool_write_set", "project_write_set", "external_cross_project_paths",
        "cross_project_access_modes", "generated_evidence_authority",
        "generated_evidence_owner_reference", "support_security_retention_profile",
        "identity_invalidation_conditions", "identity_ambiguities", "identity_decision",
        "may_proceed_to_q07", "may_begin_coding",
    )
    missing = [key for key in required if key not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")
    text_fields = (
        "task_classification", "session_id", "operation_id", "selection_timestamp",
        "selection_source", "tool_project_id", "tool_source_root", "active_project_id",
        "active_project_slug", "active_project_root", "selected_mutation_root",
        "project_root_fingerprint", "active_project_support_root",
        "support_root_identity_collision_status", "transient_workspace_root",
        "transient_namespace_cleanup_owner", "generated_evidence_owner_reference",
        "support_security_retention_profile",
    )
    for key in text_fields:
        if not _nonempty_text(record[key]):
            raise AssertionError(f"{key} is empty")
    if record["operation_class"] not in ALLOWED_OPERATION_CLASSES:
        raise AssertionError("operation class is blocked or unknown")
    if record["same_canonical_root"] not in ("YES", "NO"):
        raise AssertionError("canonical root identity is unresolved")
    if record["self_hosting_mode"] not in ("YES", "NO"):
        raise AssertionError("self-hosting mode is unresolved")
    if record["generated_evidence_authority"] not in (
        "NON_AUTHORITATIVE", "CANON_ASSIGNED"
    ):
        raise AssertionError("generated evidence authority is unresolved")
    source_roots = record["active_project_source_roots"]
    requested = record["requested_source_write_targets"]
    tool_writes = record["tool_write_set"]
    project_writes = record["project_write_set"]
    external_paths = record["external_cross_project_paths"]
    access_modes = record["cross_project_access_modes"]
    invalidation = record["identity_invalidation_conditions"]
    for key, value, allow_empty in (
        ("active_project_source_roots", source_roots, False),
        ("requested_source_write_targets", requested, True),
        ("tool_write_set", tool_writes, True),
        ("project_write_set", project_writes, True),
        ("external_cross_project_paths", external_paths, True),
        ("cross_project_access_modes", access_modes, True),
        ("identity_invalidation_conditions", invalidation, False),
    ):
        if not _text_sequence(value, allow_empty=allow_empty):
            raise AssertionError(f"{key} is invalid")
    source_roots = tuple(str(item) for item in source_roots)
    if str(record["selected_mutation_root"]) not in source_roots:
        raise AssertionError("selected mutation root is not a declared Project source root")
    if not any(_is_within(root, record["active_project_root"]) for root in source_roots):
        raise AssertionError("Project source roots do not include the active Project root")
    roots_equal = _norm(record["tool_source_root"]) == _norm(record["active_project_root"])
    if (record["same_canonical_root"] == "YES") != roots_equal:
        raise AssertionError("canonical-root declaration does not match fixture roots")
    if roots_equal and record["self_hosting_mode"] != "YES":
        raise AssertionError("same canonical root requires self-hosting")
    if not roots_equal and record["self_hosting_mode"] != "NO":
        raise AssertionError("distinct canonical roots cannot use self-hosting mode")
    support_root = record["active_project_support_root"]
    transient_root = record["transient_workspace_root"]
    if any(_is_within(support_root, root) for root in source_roots):
        raise AssertionError("Project Support is nested inside Project source")
    durable_roots = (record["tool_source_root"], *source_roots, support_root)
    if any(_norm(transient_root) == _norm(root) for root in durable_roots):
        raise AssertionError("transient workspace claims a durable owner root")
    status = str(record["support_root_identity_collision_status"]).casefold()
    if "unresolved" in status or "collision_detected" in status:
        raise AssertionError("support-root identity or collision status is unresolved")
    if "handoff-only" in str(record["selection_source"]).casefold():
        raise AssertionError("handoff-only selection source is insufficient")
    requested_set = {_norm(item) for item in requested}
    classified_set = {_norm(item) for item in (*tool_writes, *project_writes)}
    if requested_set != classified_set:
        raise AssertionError("requested write targets are not fully owner-classified")
    if any(not _is_within(path, record["tool_source_root"]) for path in tool_writes):
        raise AssertionError("Tool write set escapes Tool source root")
    if any(not any(_is_within(path, root) for root in source_roots) for path in project_writes):
        raise AssertionError("Project write set escapes selected Project source roots")
    operation_class = record["operation_class"]
    if operation_class == "TOOL_CHANGE" and project_writes:
        raise AssertionError("Tool change contains Project source writes")
    if operation_class == "PROJECT_OPERATION" and tool_writes:
        raise AssertionError("Project operation contains Tool source writes")
    if operation_class == "MIXED_GOVERNED" and (not tool_writes or not project_writes):
        raise AssertionError("mixed governed operation lacks owner-pure write sets")
    if len(external_paths) != len(access_modes):
        raise AssertionError("cross-project paths and access modes are not paired")
    if any(mode not in ALLOWED_ACCESS_MODES for mode in access_modes):
        raise AssertionError("cross-project access mode is unsupported or unresolved")
    if record["generated_evidence_authority"] == "CANON_ASSIGNED" and not _nonempty_text(
        record["generated_evidence_owner_reference"]
    ):
        raise AssertionError("canon-assigned evidence lacks owner reference")
    if record["identity_ambiguities"] not in (None, "", [], ()):
        raise AssertionError("identity ambiguities remain unresolved")
    if record["identity_decision"] != "COMPLETE":
        raise AssertionError("identity decision is not COMPLETE")
    if record["may_proceed_to_q07"] != "YES":
        raise AssertionError("Q07 progression is not authorized")
    if record["may_begin_coding"] != "NO":
        raise AssertionError("Q06 record must not authorize coding")

def _valid_record() -> dict[str, object]:
    root = "E:/kanda_reasoner"
    return {
        "task_classification": "governed prompt-library Tool change",
        "operation_class": "TOOL_CHANGE",
        "session_id": "session-q06-001",
        "operation_id": "operation-q06-001",
        "selection_timestamp": "2026-08-25T00:00:00Z",
        "selection_source": "current typed human selection",
        "tool_project_id": "tool-kanda-reasoner",
        "tool_source_root": root,
        "active_project_id": "project-kanda-reasoner",
        "active_project_slug": "kanda_reasoner",
        "active_project_root": root,
        "active_project_source_roots": [root],
        "selected_mutation_root": root,
        "project_root_fingerprint": "fixture-fingerprint-kanda-reasoner",
        "same_canonical_root": "YES",
        "self_hosting_mode": "YES",
        "active_project_support_root": "E:/kanda_reasoner_show_project_to_AI",
        "support_root_identity_collision_status": "RESOLVED_NO_COLLISION",
        "transient_workspace_root": "E:/kanda_reasoner_delete_after_daily_work",
        "transient_namespace_cleanup_owner": "session-q06-001:Tool cleanup owner",
        "requested_source_write_targets": ["E:/kanda_reasoner/tools/q06_fixture.py"],
        "tool_write_set": ["E:/kanda_reasoner/tools/q06_fixture.py"],
        "project_write_set": [],
        "external_cross_project_paths": [],
        "cross_project_access_modes": [],
        "generated_evidence_authority": "NON_AUTHORITATIVE",
        "generated_evidence_owner_reference": "KPR-12-001",
        "support_security_retention_profile": "fixture: bounded non-sensitive retention",
        "identity_invalidation_conditions": ["selection change", "root identity change"],
        "identity_ambiguities": [],
        "identity_decision": "COMPLETE",
        "may_proceed_to_q07": "YES",
        "may_begin_coding": "NO",
    }

def _expect_rejection(name: str, record: Mapping[str, object]) -> None:
    try:
        _validate_identity_record(record)
    except AssertionError:
        print(f"Q06_NEGATIVE_{name}: PASS")
        return
    raise AssertionError(f"Q06_NEGATIVE_{name}: FAIL - record was accepted")

def _validate_record_semantics() -> None:
    record = _valid_record()
    _validate_identity_record(record)
    print("Q06_SELF_HOSTING_IDENTITY_ACCEPTED: PASS")
    external = deepcopy(record)
    external.update(
        {
            "operation_class": "PROJECT_OPERATION",
            "active_project_id": "project-client",
            "active_project_slug": "client_project",
            "active_project_root": "D:/client_project",
            "active_project_source_roots": ["D:/client_project"],
            "selected_mutation_root": "D:/client_project",
            "project_root_fingerprint": "fixture-fingerprint-client",
            "same_canonical_root": "NO",
            "self_hosting_mode": "NO",
            "active_project_support_root": "D:/client_project_show_project_to_AI",
            "transient_workspace_root": "D:/client_project_delete_after_daily_work",
            "requested_source_write_targets": ["D:/client_project/src/module.py"],
            "tool_write_set": [],
            "project_write_set": ["D:/client_project/src/module.py"],
        }
    )
    _validate_identity_record(external)
    print("Q06_EXTERNAL_PROJECT_IDENTITY_ACCEPTED: PASS")
    mixed = deepcopy(external)
    mixed.update(
        {
            "operation_class": "MIXED_GOVERNED",
            "requested_source_write_targets": [
                "E:/kanda_reasoner/tools/q06_fixture.py",
                "D:/client_project/src/module.py",
            ],
            "tool_write_set": ["E:/kanda_reasoner/tools/q06_fixture.py"],
            "project_write_set": ["D:/client_project/src/module.py"],
        }
    )
    _validate_identity_record(mixed)
    print("Q06_MIXED_GOVERNED_OWNER_PURE_WRITE_SETS: PASS")
    cross_read = deepcopy(external)
    cross_read["external_cross_project_paths"] = ["F:/comparison_project"]
    cross_read["cross_project_access_modes"] = ["COMPARE"]
    _validate_identity_record(cross_read)
    print("Q06_DECLARED_CROSS_PROJECT_COMPARE_ACCEPTED: PASS")
    cases: tuple[tuple[str, str, object], ...] = (
        ("MISSING_TOOL_ROOT", "tool_source_root", ""),
        ("MISSING_PROJECT_ID", "active_project_id", ""),
        ("SELF_HOSTING_UNDECLARED", "self_hosting_mode", "NO"),
        ("HANDOFF_ONLY_SELECTION", "selection_source", "handoff-only generated evidence"),
        ("UNRESOLVED_CANONICAL_ROOT", "same_canonical_root", "UNRESOLVED"),
        ("UNRESOLVED_SUPPORT_COLLISION", "support_root_identity_collision_status", "UNRESOLVED"),
        ("IDENTITY_AMBIGUITY", "identity_ambiguities", ["owner"]),
        ("BLOCKED_DECISION", "identity_decision", "BLOCKED"),
        ("Q06_AUTHORIZES_CODING", "may_begin_coding", "YES"),
    )
    for name, key, value in cases:
        candidate = deepcopy(record)
        candidate[key] = value
        _expect_rejection(name, candidate)
    wrong_owner = deepcopy(record)
    wrong_owner["project_write_set"] = ["D:/other_project/module.py"]
    wrong_owner["requested_source_write_targets"] = [
        "E:/kanda_reasoner/tools/q06_fixture.py", "D:/other_project/module.py"
    ]
    _expect_rejection("WRONG_PROJECT_WRITE_OWNER", wrong_owner)
    nested = deepcopy(record)
    nested["active_project_support_root"] = "E:/kanda_reasoner/support"
    _expect_rejection("NESTED_SUPPORT_ROOT", nested)
    transient = deepcopy(record)
    transient["transient_workspace_root"] = transient["active_project_support_root"]
    _expect_rejection("TRANSIENT_OWNS_SUPPORT", transient)
    undeclared_cross = deepcopy(external)
    undeclared_cross["external_cross_project_paths"] = ["F:/comparison_project"]
    undeclared_cross["cross_project_access_modes"] = []
    _expect_rejection("UNDECLARED_CROSS_PROJECT_ACCESS", undeclared_cross)

def _validate_sources(project_root: Path) -> None:
    paths = {
        "brick": project_root / BRICK_WALL_REL,
        "brick_meta": project_root / BRICK_META_REL,
        "bridge": project_root / BRIDGE_REL,
        "bridge_meta": project_root / BRIDGE_META_REL,
        "boundary": project_root / BOUNDARY_REL,
        "boundary_meta": project_root / BOUNDARY_META_REL,
        "nested_validator": project_root / NESTED_VALIDATOR_REL,
        "workbench_validator": project_root / WORKBENCH_VALIDATOR_REL,
        "q06_validator": project_root / Q06_VALIDATOR_REL,
    }
    for path in paths.values():
        _gate("Q06_REQUIRED_FILE", path.is_file(), str(path))
    brick = _read_text(paths["brick"])
    bridge = _read_text(paths["bridge"])
    boundary = _read_text(paths["boundary"])
    nested_validator = _read_text(paths["nested_validator"])
    workbench_validator = _read_text(paths["workbench_validator"])
    _require_fragments(
        boundary,
        ("TOOL/PROJECT IDENTITY RECORD", *RECORD_FIELDS),
        "Q06_CANONICAL_IDENTITY_RECORD",
    )
    for fragment in RETIRED_RECORD_FIELDS:
        _gate("Q06_RETIRED_IDENTITY_FIELD_ABSENT", fragment not in boundary, fragment)
    _require_fragments(
        brick,
        ("### Tool versus Project (Q06)", "TOOL/PROJECT IDENTITY RECORD", "May begin coding: NO"),
        "Q06_BRICK_WALL_ENFORCEMENT",
    )
    _require_fragments(
        bridge,
        ("## Tool/Project identity gate (Q06)", *IMPLEMENTATION_FIELDS),
        "Q06_ROUTER_BRIDGE_ENFORCEMENT",
    )
    _gate(
        "Q06_CURRENT_SELECTION_REQUIRED",
        "The selection record must be current and typed." in boundary
        and "Keyword presence in prose is not evidence." in boundary
        and "handoff-only or generated evidence is insufficient" in brick,
    )
    _gate(
        "Q06_SELF_HOSTING_LOGICAL_SEPARATION",
        "Root equality never collapses logical ownership." in boundary
        and "Root equality is allowed only for explicit self-hosting" in bridge,
    )
    _gate(
        "Q06_OWNER_PURE_WRITE_SET_CANON",
        "requires separate Tool and Project write sets" in boundary,
    )
    _gate(
        "Q06_DECLARED_CROSS_PROJECT_ACCESS_CANON",
        "External dependencies, comparison repositories" in boundary
        and "The hard prohibition is undeclared or unauthorized cross-project mutation" in boundary,
    )
    _gate(
        "Q06_FORWARD_COMPATIBLE_BOUNDARY_VALIDATORS",
        'metadata.get("version") == "1.4"' not in nested_validator
        and 'canon_meta.get("version") != "1.3"' not in workbench_validator,
    )
    metadata_requirements = (
        (paths["brick_meta"], (1, 6), "Brick Wall"),
        (paths["bridge_meta"], (2, 0), "router bridge"),
        (paths["boundary_meta"], (2, 5), "boundary canon"),
    )
    for path, minimum, label in metadata_requirements:
        metadata = _load_json(path)
        _gate("Q06_METADATA_VERSION", _parse_version(metadata.get("version")) >= minimum, label)
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        _gate("Q06_METADATA_ALIGNMENT", bool(source_stage) and source_stage == updated_for, label)
        description = str(metadata.get("description", ""))
        description_ok = "Q06" in description
        if label == "boundary canon":
            description_ok = (
                metadata.get("prompt_id") == "project_tool_boundary_canon"
                and "Tool-versus-selected-Project" in description
            )
        _gate("Q06_METADATA_DESCRIPTION", description_ok, label)
    for path in (
        paths["brick"], paths["bridge"], paths["boundary"], paths["nested_validator"],
        paths["workbench_validator"], paths["q06_validator"],
    ):
        line_count = len(_read_text(path).splitlines())
        _gate("Q06_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")
    _gate(
        "Q06_NO_PARALLEL_ENGINE_OR_SCHEMA",
        all(
            not str(path).startswith("kanda_reasoner_app/")
            for path in (
                BRICK_WALL_REL, BRICK_META_REL, BRIDGE_REL, BRIDGE_META_REL,
                BOUNDARY_REL, BOUNDARY_META_REL, NESTED_VALIDATOR_REL,
                WORKBENCH_VALIDATOR_REL, Q06_VALIDATOR_REL,
            )
        ),
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
    print("Q06 CURRENT CANON SCHEMA MODERNIZATION: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
