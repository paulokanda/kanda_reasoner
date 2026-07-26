"""Validate Prompt Audit Wave 6C Web-AI exchange boundaries."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
from pathlib import Path

__all__ = ["main"]
from typing import Any

FEATURE_ID = "prompt-audit-wave6c-web-ai-exchange-boundaries-v1"
CLASS_ID = "06_refactor_and_architecture_hardening"
PROMPTS = {
    "web_ai_large_module_refactor_exchange_protocol": "KPR-06-001",
    "web_ai_planning_response_bundle_blueprint": "KPR-06-002",
    "web_ai_ast_split_risk_repair_protocol": "KPR-06-003",
}


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker + ": FAIL")
    print(marker + ": PASS")


def read_text(path: Path) -> str:
    require(path.is_file(), "MISSING_" + path.as_posix())
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN_" + path.name)
    require(b"\r\n" not in raw, "CRLF_FORBIDDEN_" + path.name)
    return raw.decode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read_text(path))
    require(isinstance(value, dict), "JSON_OBJECT_" + path.name)
    return value


def validate_prompts(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    active = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata = library / "METADATA"

    p1 = read_text(active / "web_ai_large_module_refactor_exchange_protocol.md")
    p2 = read_text(active / "web_ai_planning_response_bundle_blueprint.md")
    p3 = read_text(active / "web_ai_ast_split_risk_repair_protocol.md")

    for prompt_id, code in PROMPTS.items():
        text = {**{
            "web_ai_large_module_refactor_exchange_protocol": p1,
            "web_ai_planning_response_bundle_blueprint": p2,
            "web_ai_ast_split_risk_repair_protocol": p3,
        }}[prompt_id]
        require(f"Prompt code: `{code}`" in text, "WAVE6C_PROMPT_CODE_" + code.replace("-", "_"))
        require("Version: 2.0.0" in text, "WAVE6C_PROMPT_VERSION_" + code.replace("-", "_"))
        require("Status: `active`" in text and "Load type: `routed`" in text, "WAVE6C_PROMPT_LIFECYCLE_" + code.replace("-", "_"))
        require(len(text.splitlines()) <= 260, "WAVE6C_PROMPT_REDUCED_" + code.replace("-", "_"))

        meta = load_json(metadata / (prompt_id + ".meta.json"))
        require(
            meta.get("prompt_id") == prompt_id
            and meta.get("prompt_code") == code
            and meta.get("version") == "2.0.0"
            and meta.get("status") == "active"
            and meta.get("load_type") == "routed"
            and meta.get("source_stage") == FEATURE_ID,
            "WAVE6C_METADATA_" + code.replace("-", "_"),
        )
        companions = list(meta.get("required_companion_prompts", []))
        require(len(companions) == len(set(companions)), "WAVE6C_COMPANION_DEDUP_" + code.replace("-", "_"))

    for marker in (
        "planning reasoning and bounded action selection only",
        "KPR-06-002",
        "KPR-06-003",
        "source_content_hash",
        "base_plan_hash",
        "KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN",
        "Panel 4: Proposed split plan",
        "Preview Freeze Entry",
        "Confirm and Write",
    ):
        require(marker in p1, "WAVE6C_KPR06001_BOUNDARY")
    for forbidden in (
        "owns the reusable operational blueprint for ZIP",
        "owns install",
        "write canonical freeze memory directly",
    ):
        require(forbidden.lower() not in p1.lower(), "WAVE6C_KPR06001_NO_DUPLICATE_AUTHORITY")

    for marker in (
        "payload and bundle profile",
        "pending_imported_web_ai_plan.txt",
        "Regex.Matches",
        "Regex.Escape",
        "BUNDLE_REQUIRED_FILES: PASS",
        "KANDA_FREEZE_HINT_KIND_CONTRACT: PASS",
        "Preview Freeze Entry",
        "Confirm and Write",
    ):
        require(marker in p2, "WAVE6C_KPR06002_PROFILE")
    require("not architecture authority" in p2.lower() or "not architecture reasoning" in p2.lower(), "WAVE6C_KPR06002_NO_REASONING_AUTHORITY")

    for marker in (
        "target-specific AST repair reasoning",
        "SOURCE_SHA256",
        "SOURCE_BYTE_LENGTH",
        "SOURCE_TEXT_ENDS_WITH_NEWLINE",
        "RISK REFACTORING",
        "SAFE REFACTORING",
        "fresh rerun",
        "single AST Split Audit",
        "400 physical lines or fewer",
        "500 physical lines or fewer",
        "universal minimum: none",
    ):
        require(marker in p3, "WAVE6C_KPR06003_CURRENT_CONTRACT")
    for forbidden in (
        "101-499",
        "strictly within 101",
    ):
        require(forbidden not in p3, "WAVE6C_KPR06003_NO_UNIVERSAL_FLOOR")

    print("WAVE6C_WEB_AI_OWNER_BOUNDARIES: PASS")
    print("WAVE6C_CURRENT_MODULE_SIZE_DELEGATION: PASS")


def validate_routing(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    routing = library / "ROUTING"

    nav = load_json(routing / "prompt_navigation_index.json")
    entries = list(nav.get("entries", []))
    ids = {str(item.get("prompt_id")) for item in entries if isinstance(item, dict)}
    require(nav.get("prompt_count") == len(entries), "WAVE6C_NAV_COUNT")
    require(set(PROMPTS) <= ids, "WAVE6C_MACHINE_NAV_REGISTERED")
    for prompt_id, code in PROMPTS.items():
        record = next(item for item in entries if item.get("prompt_id") == prompt_id)
        require(record.get("prompt_code") == code, "WAVE6C_NAV_CODE_" + code.replace("-", "_"))
        require(record.get("category") == CLASS_ID, "WAVE6C_NAV_BOX_" + code.replace("-", "_"))

    with (routing / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    coverage = {row.get("prompt_id"): row for row in rows}
    require(set(PROMPTS) <= set(coverage), "WAVE6C_COVERAGE_REGISTERED")
    for prompt_id, code in PROMPTS.items():
        row = coverage[prompt_id]
        require(code in str(row.get("aliases")), "WAVE6C_COVERAGE_CODE_" + code.replace("-", "_"))
        require("freeze" in str(row.get("when_not_to_load")).lower(), "WAVE6C_COVERAGE_FREEZE_BOUNDARY_" + code.replace("-", "_"))

    group = load_json(routing / "group_assimilation_index.json")
    class_group = next(item for item in group.get("groups", []) if item.get("group_id") == CLASS_ID)
    stems = {Path(name).stem for name in class_group.get("main_prompts", [])}
    require(class_group.get("prompt_count") == len(stems) == 8, "WAVE6C_GROUP_COUNT")
    require(set(PROMPTS) <= stems, "WAVE6C_GROUP_SPECIALISTS_REGISTERED")

    folder = load_json(routing / "folder_assimilation_cards_index.json")
    card = next(item for item in folder.get("folders", []) if item.get("folder_id") == CLASS_ID)
    require(card.get("prompt_count") == 4, "WAVE6C_CORE_FOLDER_CARD_UNCHANGED")
    require(not (set(PROMPTS) & set(card.get("main_prompt_ids", []))), "WAVE6C_SPECIALISTS_NOT_CORE_OWNERS")

    human_nav = read_text(routing / "PROMPT_NAVIGATION_INDEX.md")
    require(all(prompt_id in human_nav for prompt_id in PROMPTS), "WAVE6C_HUMAN_NAV_REGISTERED")
    print("WAVE6C_WEB_AI_ROUTING_COMPLETENESS: PASS")


def validate_dynamic_consumers(root: Path) -> None:
    planner_gui = read_text(
        root
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py"
    )
    ast_gui = read_text(
        root / "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py"
    )
    ast.parse(planner_gui)
    ast.parse(ast_gui)

    for marker in (
        "web_ai_large_module_refactor_exchange_protocol.md",
        "web_ai_planning_response_bundle_blueprint.md",
        "QApplication.clipboard().setText",
    ):
        require(marker in planner_gui, "WAVE6C_PLANNER_DYNAMIC_CONSUMER")
    for marker in (
        "web_ai_ast_split_risk_repair_protocol.md",
        "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN",
        "SOURCE_BYTE_LENGTH",
        "SOURCE_TEXT_ENDS_WITH_NEWLINE",
    ):
        require(marker in ast_gui, "WAVE6C_AST_DYNAMIC_CONSUMER")

    print("WAVE6C_DYNAMIC_PROMPT_CONSUMERS: PASS")


def validate_records(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    substitution = read_text(
        library
        / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md"
    )
    version_match = re.search(r"^version:\s*(\d+(?:\.\d+)?)", substitution, re.MULTILINE)
    require(version_match is not None and float(version_match.group(1)) >= 7.0, "WAVE6C_SUBSTITUTION_VERSION")
    require("## Wave 6C Web-AI exchange boundary records" in substitution, "WAVE6C_SUBSTITUTION_RECORD")
    require(all(code in substitution for code in PROMPTS.values()), "WAVE6C_SUBSTITUTION_CODES")

    folder = read_text(
        library
        / "ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md"
    )
    require("## Wave 6C Web-AI specialist boundary" in folder, "WAVE6C_FOLDER_BOUNDARY_RECORD")
    print("WAVE6C_LIFECYCLE_RECORDS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    validate_prompts(root)
    validate_routing(root)
    validate_dynamic_consumers(root)
    validate_records(root)

    print("WAVE6C_WEB_AI_EXCHANGE_BOUNDARIES_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
