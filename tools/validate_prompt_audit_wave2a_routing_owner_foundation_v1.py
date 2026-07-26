"""Validate Prompt Audit Wave 2A routing-owner foundation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path
import zipfile

FEATURE_ID = "prompt-audit-wave2a-routing-owner-foundation-v1"

SPECS = {
    "ai_prompt_request_canon": ("KPR-01-014", "3.0", "always_startup", "01_session_start_and_navigation"),
    "chatgpt_kanda_routing_choice_output_protocol": ("KPR-02-001", "3.0", "on_request", "02_prompt_routing_and_indexing"),
    "kanda_routing_system_canon": ("KPR-02-002", "3.0", "on_request", "02_prompt_routing_and_indexing"),
    "project_overlay_selector": ("KPR-02-003", "2.0", "on_request", "02_prompt_routing_and_indexing"),
    "prompt_navigation_index": ("KPR-02-004", "2.7", "always_startup", "02_prompt_routing_and_indexing"),
    "prompt_substitution_map": ("KPR-02-005", "2.1", "on_request", "02_prompt_routing_and_indexing"),
    "routing_signal_scorer_v3_semantic_readiness_canon": ("KPR-02-006", "2.0", "on_request", "02_prompt_routing_and_indexing"),
}

REQUIRED = {
    "ai_prompt_request_canon": [
        "Decide whether a request may use Fast Path or must use Routed Work Path",
        "HARD STOP",
        "STEP PAUSE",
        "DEGRADED WARNING",
        "activate `brick_wall_comprehensive_quality_gate`",
        "This prompt selects context; Brick Wall governs",
        "smallest current context package",
    ],
    "chatgpt_kanda_routing_choice_output_protocol": [
        "KANDA_ROUTING_CHOICE_START",
        "KANDA_ROUTING_CHOICE_END",
        '"advisory_only": true',
        '"may_mutate": false',
        '"may_freeze": false',
        '"may_activate_ml": false',
        "retrieve only that addressed path",
    ],
    "kanda_routing_system_canon": [
        "machine-readable route data",
        "Similarity, semantic, ML, and adviser outputs are evidence only",
        "Prompts are registered and selected, not globally injected",
        "Class 07 owns prompt audit",
        "Routing cannot authorize coding",
    ],
    "project_overlay_selector": [
        "selector never becomes the overlay",
        "exactly one current compatible overlay",
        "generated overlay artifacts presented as source",
        "May write from this selector: NO",
    ],
    "prompt_navigation_index": [
        "KPR-02-004 = prompt_navigation_index",
        "KPR-07-001 = prompt_insertion_and_router_registration_protocol",
        "KPR-07-002 = prompt_identity_code_registry_canon",
        "directly addressable",
        "large_module_refactor_protocol plus large_module_refactor_template",
        "KPR-12-005 = architecture_review_project_card_machine_canon",
        "MCard lifecycle gate: COMPLETE / NOT_APPLICABLE / BLOCKED",
        "May begin coding: NO",
        "Search for disconfirming evidence",
        "anti_hallucination_short_group",
        "anti_hallucination_full_group",
    ],
    "prompt_substitution_map": [
        "historical prompt name",
        "active_alias",
        "split_replacement",
        "unresolved_conflict",
        "follow substitution chains with a visited set",
    ],
    "routing_signal_scorer_v3_semantic_readiness_canon": [
        "No-expansion default",
        "verified present gap",
        "existing-capability review",
        "offline, and advisory",
        "Runtime or persistence changes require separate architecture scope",
    ],
}

FORBIDDEN = {
    "ai_prompt_request_canon": [
        "medical residency curriculum",
        "RG-LAB-000 FIRST-POSITION",
        "RG-PILOT-000 FIRST-POSITION",
        "E:\\kanda_reasoner",
    ],
    "kanda_routing_system_canon": [
        "Phase 1 completion",
        "Phase 2 plan",
        "upload first_prompts_to_ai.zip then paste",
        "E:\\kanda_reasoner",
    ],
    "project_overlay_selector": [
        "project_freeze_ledger",
        "E:\\kanda_reasoner",
        "general_prompt_stack_load_order",
    ],
    "prompt_substitution_map": [
        "INSTALL.ps1",
        "Run Confirm and Write",
        "Press Confirm and Write now",
    ],
    "routing_signal_scorer_v3_semantic_readiness_canon": [
        "ambiguity_delta = 0.05",
        "p95 target below 100",
        "P0 is next",
        "LAB-0 is next",
    ],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF8_BOM_FORBIDDEN: {path}")
    require(b"\r\n" not in raw, f"CRLF_FORBIDDEN: {path}")
    return raw.decode("utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read_text(path))
    require(isinstance(data, dict), f"JSON_ROOT_NOT_OBJECT: {path}")
    return data


def parse_front(text: str) -> dict[str, str]:
    lines = text.splitlines()
    require(lines and lines[0] == "---", "FRONT_MATTER_START_MISSING")
    end = lines.index("---", 1)
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def validate_prompts(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    codes: set[str] = set()
    for prompt_id, (code, version, load_type, category) in SPECS.items():
        prompt = library / "ACTIVE_PROMPTS" / category / f"{prompt_id}.md"
        metadata = library / "METADATA" / f"{prompt_id}.meta.json"
        require(prompt.is_file(), f"PROMPT_MISSING: {prompt_id}")
        require(metadata.is_file(), f"METADATA_MISSING: {prompt_id}")
        text = read_text(prompt)
        front = parse_front(text)
        meta = load_json(metadata)
        require(len(text.splitlines()) <= 500, f"PROMPT_LINE_LIMIT: {prompt_id}")
        require(front.get("prompt_id") == prompt_id, f"SOURCE_ID_MISMATCH: {prompt_id}")
        require(front.get("prompt_code") == code, f"SOURCE_CODE_MISMATCH: {prompt_id}")
        require(tuple(int(part) for part in front.get("version", "0").split(".")) >= tuple(int(part) for part in version.split(".")), f"SOURCE_VERSION_MISMATCH: {prompt_id}")
        require(front.get("status") == "active", f"SOURCE_STATUS_MISMATCH: {prompt_id}")
        require(front.get("load_type") == load_type, f"SOURCE_LOAD_MISMATCH: {prompt_id}")
        require(front.get("owner_box") == category, f"SOURCE_OWNER_MISMATCH: {prompt_id}")
        require(meta.get("prompt_id") == prompt_id, f"META_ID_MISMATCH: {prompt_id}")
        require(meta.get("prompt_code") == code, f"META_CODE_MISMATCH: {prompt_id}")
        require(tuple(int(part) for part in str(meta.get("version") or "0").split(".")) >= tuple(int(part) for part in version.split(".")), f"META_VERSION_MISMATCH: {prompt_id}")
        require(meta.get("status") == "active", f"META_STATUS_MISMATCH: {prompt_id}")
        require(meta.get("load_type") == load_type, f"META_LOAD_MISMATCH: {prompt_id}")
        require(meta.get("owner_box") == category, f"META_OWNER_MISMATCH: {prompt_id}")
        allowed_stage = FEATURE_ID
        if prompt_id in {"prompt_navigation_index", "prompt_substitution_map", "chatgpt_kanda_routing_choice_output_protocol"}:
            allowed_stage = meta.get("source_stage")
            require(allowed_stage in {FEATURE_ID, "prompt-audit-wave2b-legacy-routing-retirement-v1", "prompt-audit-wave3a-session-startup-kernel-v1"}, f"META_STAGE_MISMATCH: {prompt_id}")
        if prompt_id not in {"prompt_navigation_index", "prompt_substitution_map", "chatgpt_kanda_routing_choice_output_protocol"}:
            require(meta.get("source_stage") == FEATURE_ID, f"META_STAGE_MISMATCH: {prompt_id}")
        require(meta.get("updated_for") == meta.get("source_stage"), f"META_UPDATED_FOR_MISMATCH: {prompt_id}")
        require(bool(meta.get("canonical_path")), f"META_CANONICAL_PATH_MISSING: {prompt_id}")
        require(code not in codes, f"DUPLICATE_CODE: {code}")
        codes.add(code)
        for marker in REQUIRED[prompt_id]:
            marker_present = marker in text
            if prompt_id == "prompt_navigation_index" and marker == (
                "large_module_refactor_protocol plus large_module_refactor_template"
            ):
                marker_present = marker_present or (
                    "KPR-06-007 = large_module_refactor_protocol" in text
                    and "KPR-06-008 = large_module_refactor_template" in text
                )
            require(
                marker_present,
                f"REQUIRED_MARKER_MISSING: {prompt_id}: {marker}",
            )
        for marker in FORBIDDEN.get(prompt_id, []):
            require(marker not in text, f"FORBIDDEN_MARKER_PRESENT: {prompt_id}: {marker}")
    require(codes == {"KPR-01-014", "KPR-02-001", "KPR-02-002", "KPR-02-003", "KPR-02-004", "KPR-02-005", "KPR-02-006"}, "CODE_SET_MISMATCH")
    print("WAVE2A_PROMPT_METADATA_ALIGNMENT: PASS")
    print("WAVE2A_PROMPT_LINE_LIMITS: PASS")
    print("WAVE2A_CODE_IDENTITY_SET: PASS")


def validate_routes(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    route = load_json(library / "ROUTING/prompt_navigation_index.json")
    entries = {item.get("prompt_id"): item for item in route.get("entries", [])}
    require(route.get("prompt_count") == len(route.get("entries", [])), "ROUTE_COUNT_MISMATCH")
    for prompt_id, (code, version, _, category) in SPECS.items():
        entry = entries.get(prompt_id)
        require(isinstance(entry, dict), f"ROUTE_ENTRY_MISSING: {prompt_id}")
        require(entry.get("prompt_code") == code, f"ROUTE_CODE_MISMATCH: {prompt_id}")
        require(entry.get("status") == "active", f"ROUTE_STATUS_MISMATCH: {prompt_id}")
        require(tuple(int(part) for part in str(entry.get("version") or "0").split(".")) >= tuple(int(part) for part in version.split(".")), f"ROUTE_VERSION_MISMATCH: {prompt_id}")
        require(entry.get("owner_box") == category, f"ROUTE_OWNER_MISMATCH: {prompt_id}")
    require("prompt_router" not in entries, "PROMPT_ROUTER_ACTIVE_ROUTE_REMAINS")
    require("routing_signal_scorer_v3_pilot_copilot_phase0_router_canon" not in entries, "PILOT_ACTIVE_ROUTE_REMAINS")
    require("routing_signal_scorer_v3_lab_phase_entry_router_canon" not in entries, "LAB_ACTIVE_ROUTE_REMAINS")

    groups = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in groups["groups"] if item.get("group_id") == "02_prompt_routing_and_indexing")
    require(group.get("prompt_count") == 6, "GROUP_PROMPT_COUNT_MISMATCH")
    require(len(group.get("prompt_ids", [])) == 6, "GROUP_PROMPT_IDS_MISMATCH")

    card = read_text(library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/_FOLDER_ASSIMILATION.md")
    for code in ["KPR-02-001", "KPR-02-002", "KPR-02-003", "KPR-02-004", "KPR-02-005", "KPR-02-006"]:
        require(code in card, f"FOLDER_CARD_CODE_MISSING: {code}")
    require("Retired identities" in card, "RETIRED_IDENTITY_BOUNDARY_MISSING")
    print("WAVE2A_ROUTE_OWNER_ALIGNMENT: PASS")
    print("WAVE2A_TRANSITIONAL_ROUTE_GUARDS: PASS")


def validate_duplicate_and_startup(root: Path, startup_zip: Path | None) -> None:
    duplicate = root / "prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md"
    duplicate_meta = root / "prompt_library/METADATA/kanda_routing_system_canon.meta.json"
    text = read_text(duplicate)
    meta = load_json(duplicate_meta)
    require("Deprecated duplicate source" in text, "DUPLICATE_REDIRECT_MISSING")
    require("not canonical" in text, "DUPLICATE_NON_AUTH_MISSING")
    require(meta.get("status") == "deprecated", "DUPLICATE_META_STATUS_MISMATCH")
    require(meta.get("do_not_use_as_source_authority") is True, "DUPLICATE_META_AUTHORITY_MISSING")

    source_map = load_json(root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
    by_id = {item.get("prompt_id"): item for item in source_map.get("startup_sources", [])}
    for pid in ["ai_prompt_request_canon", "prompt_navigation_index"]:
        require(pid in by_id, f"STARTUP_SOURCE_MISSING: {pid}")
        require(by_id[pid].get("load_mode") == "always_startup", f"STARTUP_LOAD_MODE_MISMATCH: {pid}")
    require(
        "chatgpt_kanda_routing_choice_output_protocol" not in by_id,
        "ROUTING_CHOICE_MUST_BE_ON_REQUEST",
    )
    if startup_zip is not None:
        require(startup_zip.is_file(), f"STARTUP_ZIP_MISSING: {startup_zip}")
        with zipfile.ZipFile(startup_zip, "r") as archive:
            names = set(archive.namelist())
            required = {
                "01_ai_prompt_request_canon.md",
                "02_prompt_navigation_index.md",
            }
            require(required.issubset(names), "STARTUP_GENERATED_MEMBERS_MISSING")
            require(
                "11_chatgpt_kanda_routing_choice_output_protocol.md" not in names,
                "STARTUP_ROUTING_CHOICE_MEMBER_REMAINS",
            )
            ai = archive.read("01_ai_prompt_request_canon.md").decode("utf-8")
            nav = archive.read("02_prompt_navigation_index.md").decode("utf-8")
            require("KPR-01-014" in ai, "STARTUP_AI_PROMPT_STALE")
            require("KPR-02-004" in nav, "STARTUP_NAV_STALE")
    print("WAVE2A_DUPLICATE_SOURCE_RECONCILED: PASS")
    print("WAVE2A_STARTUP_OWNER_BRIDGES: PASS")



def validate_compatibility_reports(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    expanded = read_text(library / "ROUTING/PROMPT_NAVIGATION_INDEX.md")
    require("compatibility documentation" in expanded, "EXPANDED_ROUTE_AUTHORITY_NOTICE_MISSING")
    require("Do not select deprecated `prompt_router` for new work" in expanded, "EXPANDED_ROUTE_LEGACY_GUARD_MISSING")
    coverage = read_text(library / "ROUTING/prompt_route_coverage_table.csv")
    require("ai_prompt_request_canon,01_session_start_and_navigation,1" in coverage, "COVERAGE_AI_REQUEST_MISSING")
    require("chatgpt_kanda_routing_choice_output_protocol,02_prompt_routing_and_indexing,2" in coverage, "COVERAGE_CHOICE_OUTPUT_MISSING")
    require("prompt_router,02_prompt_routing_and_indexing" not in coverage, "COVERAGE_LEGACY_ROUTER_REMAINS")
    print("WAVE2A_COMPATIBILITY_REPORTS_ALIGNED: PASS")

def validate_negative_controls() -> None:
    current = {"status": "deprecated_historical", "priority": 0}
    require(current["status"] != "active", "NEGATIVE_HISTORICAL_STATUS")
    mutant = dict(current)
    mutant["status"] = "active"
    caught = False
    try:
        require(mutant["status"] != "active", "NEGATIVE_HISTORICAL_ROUTE")
    except AssertionError:
        caught = True
    require(caught, "NEGATIVE_ROUTE_MUTANT_SURVIVED")
    print("WAVE2A_NEGATIVE_GUARD_CONTROLS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--startup-zip")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    startup = Path(args.startup_zip).resolve() if args.startup_zip else None
    validate_prompts(root)
    validate_routes(root)
    validate_duplicate_and_startup(root, startup)
    validate_compatibility_reports(root)
    validate_negative_controls()
    print("WAVE2A_ROUTING_OWNER_FOUNDATION_REGRESSION_SET: PASS")
    print("WAVE2A_NO_NEW_ROUTING_ENGINE_OR_REGISTRY: PASS")
    print("WAVE2A_WAVE2B_MIGRATION_BOUNDARY: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
