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
BOUNDARY_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)
BOUNDARY_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "project_tool_boundary_canon.meta.json"
)
NESTED_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_nested_support_root_v1.py"
)
WORKBENCH_VALIDATOR_REL = Path(
    "tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py"
)
Q06_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q06_tool_project_identity_v1.py"
)

RECORD_FIELDS = (
    "Task classification:",
    "Tool task or Project operation: TOOL_CHANGE / PROJECT_OPERATION / MIXED_GOVERNED / BLOCKED",
    "Tool project slug:",
    "Tool source root:",
    "Active project slug:",
    "Active project root:",
    "Same physical Tool/Project root: YES / NO",
    "Self-hosting mode: YES / NO",
    "Human-selected active project evidence:",
    "Operation owner: TOOL / ACTIVE_PROJECT / MIXED_GOVERNED / UNRESOLVED",
    "Requested source write target:",
    "Source write target owner: TOOL / ACTIVE_PROJECT / NONE / UNRESOLVED",
    "Active project support root:",
    "Transient garbage root:",
    "Forbidden nested support root:",
    "Tool-owned reusable assets:",
    "Active-project-owned source or generated results:",
    "Project-specific durable support state:",
    "Generated evidence authority:",
    "Cross-project paths involved:",
    "Identity ambiguities:",
    "Identity decision: COMPLETE / BLOCKED",
    "May proceed to Q07 classification: YES / NO",
    "May begin coding: NO",
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


def _nonempty_sequence(value: object) -> bool:
    return isinstance(value, (list, tuple)) and bool(value) and all(
        _nonempty_text(item) for item in value
    )


def _is_nested(path: str, parent: str) -> bool:
    normalized_path = path.replace("\\", "/").rstrip("/").casefold()
    normalized_parent = parent.replace("\\", "/").rstrip("/").casefold()
    return normalized_path.startswith(normalized_parent + "/")


def _validate_identity_record(record: Mapping[str, object]) -> None:
    required = (
        "task_classification",
        "operation_type",
        "tool_project_slug",
        "tool_source_root",
        "active_project_slug",
        "active_project_root",
        "same_physical_root",
        "self_hosting_mode",
        "active_project_evidence",
        "operation_owner",
        "source_write_target",
        "source_write_target_owner",
        "active_project_support_root",
        "transient_garbage_root",
        "forbidden_nested_support_root",
        "tool_owned_assets",
        "active_project_owned_results",
        "project_durable_support",
        "generated_evidence_authority",
        "cross_project_paths",
        "identity_ambiguities",
        "identity_decision",
        "may_proceed_to_q07",
        "may_begin_coding",
    )
    missing = [key for key in required if key not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")

    for key in (
        "task_classification",
        "tool_project_slug",
        "tool_source_root",
        "active_project_slug",
        "active_project_root",
        "active_project_evidence",
        "active_project_support_root",
        "transient_garbage_root",
        "forbidden_nested_support_root",
        "generated_evidence_authority",
    ):
        if not _nonempty_text(record[key]):
            raise AssertionError(f"{key} is empty")

    if record["operation_type"] not in (
        "TOOL_CHANGE",
        "PROJECT_OPERATION",
        "MIXED_GOVERNED",
    ):
        raise AssertionError("operation type is blocked or unknown")
    if record["operation_owner"] not in (
        "TOOL",
        "ACTIVE_PROJECT",
        "MIXED_GOVERNED",
    ):
        raise AssertionError("operation owner is unresolved")
    if record["source_write_target_owner"] not in (
        "TOOL",
        "ACTIVE_PROJECT",
        "NONE",
    ):
        raise AssertionError("source write target owner is unresolved")

    tool_root = str(record["tool_source_root"])
    project_root = str(record["active_project_root"])
    support_root = str(record["active_project_support_root"])
    transient_root = str(record["transient_garbage_root"])
    nested_root = str(record["forbidden_nested_support_root"])
    same_root = tool_root.replace("\\", "/").casefold() == project_root.replace(
        "\\", "/"
    ).casefold()
    if (record["same_physical_root"] == "YES") != same_root:
        raise AssertionError("same-root declaration does not match roots")
    if same_root and record["self_hosting_mode"] != "YES":
        raise AssertionError("same physical root requires self-hosting")
    if not same_root and record["self_hosting_mode"] == "YES":
        raise AssertionError("self-hosting does not match distinct roots")

    if support_root.casefold() in (tool_root.casefold(), project_root.casefold()):
        raise AssertionError("support root collapsed into source root")
    if _is_nested(support_root, project_root):
        raise AssertionError("support root is nested inside project source")
    if nested_root.casefold() == support_root.casefold():
        raise AssertionError("forbidden nested root equals canonical support root")
    if not _is_nested(nested_root, project_root):
        raise AssertionError("forbidden nested support root classification is invalid")
    if transient_root.casefold() in (
        tool_root.casefold(),
        project_root.casefold(),
        support_root.casefold(),
    ):
        raise AssertionError("transient root claims a durable owner root")

    evidence = str(record["active_project_evidence"]).casefold()
    if "handoff-only" in evidence or "generated-only" in evidence:
        raise AssertionError("current project selection is not proven")
    if "current" not in evidence and "human" not in evidence:
        raise AssertionError("active project evidence lacks current selection")

    for key in (
        "tool_owned_assets",
        "active_project_owned_results",
        "project_durable_support",
    ):
        if not _nonempty_sequence(record[key]):
            raise AssertionError(f"{key} is empty")

    operation_owner = record["operation_owner"]
    write_owner = record["source_write_target_owner"]
    if operation_owner == "TOOL" and write_owner not in ("TOOL", "NONE"):
        raise AssertionError("Tool operation writes project source")
    if operation_owner == "ACTIVE_PROJECT" and write_owner not in (
        "ACTIVE_PROJECT",
        "NONE",
    ):
        raise AssertionError("Project operation writes Tool source")
    if record["source_write_target_owner"] != "NONE" and not _nonempty_text(
        record["source_write_target"]
    ):
        raise AssertionError("source write target is empty")

    authority = str(record["generated_evidence_authority"]).casefold()
    if "non-authoritative" not in authority and "canon assigns" not in authority:
        raise AssertionError("generated evidence authority is unsafe")
    if record["cross_project_paths"] not in (None, "", [], ()):
        raise AssertionError("cross-project paths remain involved")
    if record["identity_ambiguities"] not in (None, "", [], ()):
        raise AssertionError("identity ambiguities remain unresolved")
    if record["identity_decision"] != "COMPLETE":
        raise AssertionError("identity decision is not COMPLETE")
    if record["may_proceed_to_q07"] != "YES":
        raise AssertionError("Q07 progression is not authorized")
    if record["may_begin_coding"] != "NO":
        raise AssertionError("Q06 record must not authorize coding")


def _valid_record() -> dict[str, object]:
    return {
        "task_classification": "governed prompt-library Tool change",
        "operation_type": "TOOL_CHANGE",
        "tool_project_slug": "kanda_reasoner",
        "tool_source_root": "E:/kanda_reasoner",
        "active_project_slug": "kanda_reasoner",
        "active_project_root": "E:/kanda_reasoner",
        "same_physical_root": "YES",
        "self_hosting_mode": "YES",
        "active_project_evidence": "current human selection and PROJECT READY",
        "operation_owner": "TOOL",
        "source_write_target": "E:/kanda_reasoner/kanda_prompt_workspace",
        "source_write_target_owner": "TOOL",
        "active_project_support_root": "E:/kanda_reasoner_show_project_to_AI",
        "transient_garbage_root": "E:/kanda_reasoner_delete_after_daily_work",
        "forbidden_nested_support_root": (
            "E:/kanda_reasoner/kanda_reasoner_show_project_to_AI"
        ),
        "tool_owned_assets": ["prompt-library canon", "validators"],
        "active_project_owned_results": ["selected project source and outputs"],
        "project_durable_support": ["validation evidence", "freeze memory"],
        "generated_evidence_authority": (
            "non-authoritative unless a current canon assigns authority"
        ),
        "cross_project_paths": [],
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
            "operation_type": "PROJECT_OPERATION",
            "active_project_slug": "client_project",
            "active_project_root": "D:/client_project",
            "same_physical_root": "NO",
            "self_hosting_mode": "NO",
            "operation_owner": "ACTIVE_PROJECT",
            "source_write_target": "D:/client_project/src/module.py",
            "source_write_target_owner": "ACTIVE_PROJECT",
            "active_project_support_root": "D:/client_project_show_project_to_AI",
            "transient_garbage_root": "D:/client_project_delete_after_daily_work",
            "forbidden_nested_support_root": (
                "D:/client_project/client_project_show_project_to_AI"
            ),
        }
    )
    _validate_identity_record(external)
    print("Q06_EXTERNAL_PROJECT_IDENTITY_ACCEPTED: PASS")

    cases: tuple[tuple[str, str, object], ...] = (
        ("MISSING_TOOL_ROOT", "tool_source_root", ""),
        ("MISSING_PROJECT_ROOT", "active_project_root", ""),
        ("SELF_HOSTING_UNDECLARED", "self_hosting_mode", "NO"),
        ("HANDOFF_ONLY_SELECTION", "active_project_evidence", "handoff-only"),
        ("UNRESOLVED_OWNER", "operation_owner", "UNRESOLVED"),
        ("WRONG_WRITE_OWNER", "source_write_target_owner", "ACTIVE_PROJECT"),
        ("CROSS_PROJECT_PATH", "cross_project_paths", ["D:/other_project"]),
        ("IDENTITY_AMBIGUITY", "identity_ambiguities", ["owner"]),
        ("BLOCKED_DECISION", "identity_decision", "BLOCKED"),
        ("Q06_AUTHORIZES_CODING", "may_begin_coding", "YES"),
    )
    for name, key, value in cases:
        candidate = deepcopy(record)
        candidate[key] = value
        _expect_rejection(name, candidate)

    nested = deepcopy(record)
    nested["active_project_support_root"] = (
        "E:/kanda_reasoner/kanda_reasoner_show_project_to_AI"
    )
    _expect_rejection("NESTED_SUPPORT_ROOT", nested)

    transient = deepcopy(record)
    transient["transient_garbage_root"] = transient["active_project_support_root"]
    _expect_rejection("TRANSIENT_OWNS_SUPPORT", transient)


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
    _require_fragments(
        brick,
        (
            "### Tool versus Project (Q06)",
            "TOOL/PROJECT IDENTITY RECORD",
            "May begin coding: NO",
        ),
        "Q06_BRICK_WALL_ENFORCEMENT",
    )
    _require_fragments(
        bridge,
        ("## Tool/Project identity gate (Q06)", *IMPLEMENTATION_FIELDS),
        "Q06_ROUTER_BRIDGE_ENFORCEMENT",
    )
    _gate(
        "Q06_CURRENT_SELECTION_REQUIRED",
        "Handoff-only or generated evidence is insufficient." in boundary
        and "handoff-only or generated evidence is insufficient" in brick,
    )
    _gate(
        "Q06_SELF_HOSTING_LOGICAL_SEPARATION",
        "Physical root equality is valid only for explicit self-hosting" in boundary
        and "Root equality is allowed only for explicit self-hosting" in bridge,
    )
    _gate(
        "Q06_FORWARD_COMPATIBLE_BOUNDARY_VALIDATORS",
        'metadata.get("version") == "1.4"' not in nested_validator
        and 'canon_meta.get("version") != "1.3"' not in workbench_validator,
    )

    metadata_requirements = (
        (paths["brick_meta"], (1, 6), "Brick Wall"),
        (paths["bridge_meta"], (2, 0), "router bridge"),
        (paths["boundary_meta"], (1, 5), "boundary canon"),
    )
    for path, minimum, label in metadata_requirements:
        metadata = _load_json(path)
        _gate("Q06_METADATA_VERSION", _parse_version(metadata.get("version")) >= minimum, label)
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        _gate(
            "Q06_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
        _gate(
            "Q06_METADATA_DESCRIPTION",
            "Q06" in str(metadata.get("description", "")),
            label,
        )

    for path in (
        paths["brick"],
        paths["bridge"],
        paths["boundary"],
        paths["nested_validator"],
        paths["workbench_validator"],
        paths["q06_validator"],
    ):
        line_count = len(_read_text(path).splitlines())
        _gate("Q06_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")

    _gate(
        "Q06_NO_PARALLEL_ENGINE_OR_SCHEMA",
        all(
            not str(path).startswith("kanda_reasoner_app/")
            for path in (
                BRICK_WALL_REL,
                BRICK_META_REL,
                BRIDGE_REL,
                BRIDGE_META_REL,
                BOUNDARY_REL,
                BOUNDARY_META_REL,
                NESTED_VALIDATOR_REL,
                WORKBENCH_VALIDATOR_REL,
                Q06_VALIDATOR_REL,
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
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
