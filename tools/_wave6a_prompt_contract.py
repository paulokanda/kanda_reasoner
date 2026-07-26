"""Shared focused checks for Prompt Audit Wave 6A.

This is validator support only. It does not own prompt routing or runtime
architecture behavior.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

__all__ = ["validate_current_contract"]

PROMPT_BASE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening"
)
META_BASE = Path("kanda_prompt_workspace/prompt_library/METADATA")
ROUTING_BASE = Path("kanda_prompt_workspace/prompt_library/ROUTING")


def _read(root: Path, relative: Path | str) -> str:
    path = root / Path(relative)
    if not path.is_file():
        raise AssertionError("Missing required file: " + str(relative))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _json(root: Path, relative: Path | str) -> dict[str, Any]:
    loaded = json.loads(_read(root, relative))
    if not isinstance(loaded, dict):
        raise AssertionError("JSON root must be an object: " + str(relative))
    return loaded


def _require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def _contains(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _require(not missing, label + " missing: " + repr(missing))


def _version_tuple(value: object) -> tuple[int, ...]:
    parts = re.findall(r"\d+", str(value or ""))
    return tuple(int(part) for part in parts)


def _entry_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = data.get("entries", [])
    return {
        str(item.get("prompt_id")): item
        for item in entries
        if isinstance(item, dict) and item.get("prompt_id")
    }


def validate_sources(root: Path) -> None:
    architecture = _read(root, PROMPT_BASE / "architecture_hardening_triage_protocol.md")
    architecture_template = _read(root, PROMPT_BASE / "architecture_hardening_triage_template.md")
    large = _read(root, PROMPT_BASE / "large_module_refactor_protocol.md")
    large_template = _read(root, PROMPT_BASE / "large_module_refactor_template.md")

    _contains(
        architecture,
        (
            "Prompt code: `KPR-06-005`",
            "Version: 2.",
            "Hardening is not rewriting.",
            "HARD_FAILURE",
            "PROTECTION_GAP",
            "TRANSITIONAL_DEBT",
            "WARNING",
            "NOT_APPLICABLE",
            "current-owner discovery",
            "KPR-03-001",
            "KPR-04-001",
            "KPR-04-002",
            "KPR-04-006",
            "KPR-12-001",
            "May begin coding: YES / NO",
        ),
        "architecture protocol",
    )
    for forbidden in (
        "unified KANDA-style direct ZIP delivery",
        "official governance-only updates",
        "_bundle_temp\\BUNDLE_MANIFEST",
        "wait for user validation -> freeze",
    ):
        _require(forbidden not in architecture, "Architecture protocol retained delivery authority: " + forbidden)
    _require(len(architecture.splitlines()) <= 300, "Architecture protocol is not reduced")

    _contains(
        architecture_template,
        (
            "Prompt code: `KPR-06-006`",
            "Status: `draft_template`",
            "Load type: `explicit_on_request`",
            "does not authorize",
            "Brick Wall implementation authorization",
        ),
        "architecture template",
    )
    _require(len(architecture_template.splitlines()) <= 180, "Architecture template is too large")

    _contains(
        large,
        (
            "Prompt code: `KPR-06-007`",
            "Version: 9.",
            "Module-size and complexity law",
            "ideal size: 400 physical lines or fewer",
            "absolute hard maximum: 500 physical lines or fewer",
            "No universal minimum file size is imposed.",
            "never remove required",
            "candidate-island queue",
            "public import paths",
            "behavior equivalence",
            "KPR-06-001",
            "KPR-06-002",
            "KPR-06-003",
            "KPR-06-004",
            "KPR-06-005",
            "KPR-06-006",
            "KPR-06-007",
            "KPR-06-008",
            "Class 05 owners",
            "May begin coding: YES / NO",
        ),
        "large-module protocol",
    )
    for forbidden in (
        "strictly more than 100 physical lines",
        "101 through 499 physical lines inclusive",
        "Maximum per response: 4 ordered patch ZIPs.",
        "Patch-train delivery bundle",
        "freeze each inner patch separately",
    ):
        _require(forbidden not in large, "Large-module protocol retained obsolete doctrine: " + forbidden)
    _require("formatting compression" not in large.lower(), "Legacy Q36 forbidden phrase returned")
    _require(len(large.splitlines()) <= 400, "Large-module protocol is not reduced")

    _contains(
        large_template,
        (
            "Prompt code: `KPR-06-008`",
            "Version: 4.0.0",
            "Status: `draft_template`",
            "Aligned with: `KPR-06-007 large_module_refactor_protocol v9.0`",
            "Completing this record does not itself authorize implementation.",
        ),
        "large-module template",
    )
    _require(len(large_template.splitlines()) <= 180, "Large-module template is too large")


def validate_metadata(root: Path) -> None:
    expected = {
        "architecture_hardening_triage_protocol": ("KPR-06-005", "2.0.0", "active", "routed"),
        "architecture_hardening_triage_template": ("KPR-06-006", "2.0.0", "draft_template", "explicit_on_request"),
        "large_module_refactor_protocol": ("KPR-06-007", "9.0.0", "active", "routed"),
        "large_module_refactor_template": ("KPR-06-008", "4.0.0", "draft_template", "explicit_on_request"),
    }
    for prompt_id, (code, version, status, load_type) in expected.items():
        meta = _json(root, META_BASE / (prompt_id + ".meta.json"))
        _require(meta.get("prompt_id") == prompt_id, prompt_id + " metadata prompt_id drift")
        _require(meta.get("prompt_code") == code, prompt_id + " metadata code drift")
        _require(_version_tuple(meta.get("version")) >= _version_tuple(version), prompt_id + " metadata version drift")
        _require(meta.get("status") == status, prompt_id + " metadata status drift")
        _require(meta.get("load_type") == load_type, prompt_id + " metadata load type drift")
        _require(str(meta.get("source_stage") or "").startswith("prompt-audit-wave6"), prompt_id + " metadata provenance drift")
        _require(bool(meta.get("do_not_regress")), prompt_id + " metadata do_not_regress missing")

    large_meta = _json(root, META_BASE / "large_module_refactor_protocol.meta.json")
    _require("large_module_refactor_template" in set(large_meta.get("required_companion_prompts", [])), "Large protocol template companion missing")
    template_meta = _json(root, META_BASE / "large_module_refactor_template.meta.json")
    _require(template_meta.get("aligned_with") == "large_module_refactor_protocol_v9.0", "Large template alignment drift")
    for template_id in ("architecture_hardening_triage_template", "large_module_refactor_template"):
        meta = _json(root, META_BASE / (template_id + ".meta.json"))
        _require(meta.get("edit_policy") == "draft_only", template_id + " edit policy drift")
        _require(meta.get("promotion_policy") == "manual_only", template_id + " promotion policy drift")


def validate_routing(root: Path) -> None:
    navigation = _json(root, ROUTING_BASE / "prompt_navigation_index.json")
    entries = _entry_map(navigation)
    expected = {
        "architecture_hardening_triage_protocol": ("KPR-06-005", "active", "routed"),
        "architecture_hardening_triage_template": ("KPR-06-006", "draft_template", "explicit_on_request"),
        "large_module_refactor_protocol": ("KPR-06-007", "active", "routed"),
        "large_module_refactor_template": ("KPR-06-008", "draft_template", "explicit_on_request"),
    }
    for prompt_id, (code, status, load_type) in expected.items():
        entry = entries.get(prompt_id)
        _require(entry is not None, "Missing routing entry: " + prompt_id)
        _require(entry.get("prompt_code") == code, prompt_id + " routing code drift")
        if status != "active":
            _require(entry.get("status") == status, prompt_id + " routing status drift")
            _require(entry.get("load_type") == load_type, prompt_id + " routing load type drift")
        _require(bool(entry.get("when_to_load")), prompt_id + " when_to_load missing")
        _require(bool(entry.get("when_not_to_load")), prompt_id + " when_not_to_load missing")

    active_nav = _read(root, "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md")
    routing_md = _read(root, ROUTING_BASE / "PROMPT_NAVIGATION_INDEX.md")
    folder_card = _read(root, PROMPT_BASE / "_FOLDER_ASSIMILATION.md")
    for code in ("KPR-06-005", "KPR-06-006", "KPR-06-007", "KPR-06-008"):
        _require(code in active_nav, "Active navigation missing " + code)
        _require(code in routing_md, "Routing markdown missing " + code)
        _require(code in folder_card, "Folder card missing " + code)
    _require("draft-only records" in active_nav.lower(), "Active navigation does not classify templates")
    _require("Class 05 owns patch" in active_nav, "Active navigation does not delegate delivery")

    coverage_path = root / ROUTING_BASE / "prompt_route_coverage_table.csv"
    with coverage_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = {row["prompt_id"]: row for row in csv.DictReader(handle)}
    for prompt_id, (code, _, _) in expected.items():
        row = rows.get(prompt_id)
        _require(row is not None, "Coverage row missing: " + prompt_id)
        _require(code in row.get("aliases", ""), prompt_id + " coverage code missing")


def validate_duplicate_retirement(root: Path) -> None:
    retired = (
        "kanda_reasoner_app/prompt_library/active/0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL TEMPLATE v1.0.md",
        "kanda_reasoner_app/prompt_library/metadata/0000_5_5_large_module_refactor_protocol_template.meta.json",
        "kanda_reasoner_app/prompt_library/active/0000 8.1 PYARCHITECT ARCHITECTURE HARDENING TRIAGE PROTOCOL TEMPLATE v1.0.md",
        "kanda_reasoner_app/prompt_library/metadata/0000_8_1_architecture_hardening_triage_protocol_template.meta.json",
    )
    for relative in retired:
        _require(not (root / relative).exists(), "Retired application duplicate remains: " + relative)

    groups = _json(root, "kanda_reasoner_app/prompt_library/groups/PROMPT_GROUPS.json")
    encoded = json.dumps(groups, ensure_ascii=True)
    _require("0000_5_5_large_module_refactor_protocol_template" not in encoded, "Legacy large-module app route remains")
    _require("0000_8_1_architecture_hardening_triage_protocol_template" not in encoded, "Legacy architecture app route remains")

    profile = _json(root, "kanda_reasoner_app/prompt_library/profiles/PROJECT_PROMPT_STACK_PROFILE_TEMPLATE.json")
    profile_text = json.dumps(profile, ensure_ascii=True)
    _require("0000_5_5_large_module_refactor_protocol_template" not in profile_text, "Legacy large-module profile route remains")
    _require("0000_8_1_architecture_hardening_triage_protocol_template" not in profile_text, "Legacy architecture profile route remains")
    _require("large_module_refactor_protocol" in profile_text, "Canonical large-module profile route missing")
    _require("architecture_hardening_triage_protocol" in profile_text, "Canonical architecture profile route missing")


def validate_current_contract(project_root: Path) -> None:
    root = project_root.expanduser().resolve(strict=True)
    validate_sources(root)
    validate_metadata(root)
    validate_routing(root)
    validate_duplicate_retirement(root)
