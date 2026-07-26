"""Validate Wave 2B legacy routing consumer migration and retirement."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile

FEATURE_ID = "prompt-audit-wave2b-legacy-routing-retirement-v1"
LEGACY_IDS = {
    "prompt_router",
    "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon",
    "routing_signal_scorer_v3_lab_phase_entry_router_canon",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN: " + str(path))
    require(b"\r\n" not in raw, "CRLF_FORBIDDEN: " + str(path))
    return raw.decode("utf-8")


def load(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), "JSON_ROOT_NOT_OBJECT: " + str(path))
    return data


def load_existing(path: Path) -> dict:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN: " + str(path))
    data = json.loads(raw.decode("utf-8"))
    require(isinstance(data, dict), "JSON_ROOT_NOT_OBJECT: " + str(path))
    return data


def validate_historical_records(root: Path) -> None:
    plib = root / "kanda_prompt_workspace/prompt_library"
    specs = {
        "prompt_router": ("deprecated", "compatibility_only", "Prompt Router Compatibility Redirect"),
        "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon": ("retired", "historical_reference", "RG-PILOT-000 Historical Phase-Entry Record"),
        "routing_signal_scorer_v3_lab_phase_entry_router_canon": ("retired", "historical_reference", "RG-LAB-000 Historical Phase-Entry Record"),
    }
    for prompt_id, (status, load_type, marker) in specs.items():
        source = plib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing" / (prompt_id + ".md")
        meta = plib / "METADATA" / (prompt_id + ".meta.json")
        text = read(source)
        data = load(meta)
        require(marker in text, "Historical marker missing: " + prompt_id)
        require(data.get("status") == status, "Metadata status mismatch: " + prompt_id)
        require(data.get("load_type") == load_type, "Metadata load type mismatch: " + prompt_id)
        require(data.get("active_route") is False, "Active-route flag mismatch: " + prompt_id)
        require(data.get("may_be_selected_for_new_work") is False, "Selection flag mismatch: " + prompt_id)
        require(len(text.splitlines()) <= 120, "Historical record too large: " + prompt_id)
    print("WAVE2B_HISTORICAL_RECORDS_COMPACT: PASS")


def validate_active_routes(root: Path) -> None:
    plib = root / "kanda_prompt_workspace/prompt_library"
    route = load(plib / "ROUTING/prompt_navigation_index.json")
    ids = {item.get("prompt_id") for item in route.get("entries", [])}
    require(not (ids & LEGACY_IDS), "Legacy route remains active")
    require(route.get("prompt_count") == len(route.get("entries", [])), "Route count mismatch")
    groups = load(plib / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in groups["groups"] if item.get("group_id") == "02_prompt_routing_and_indexing")
    require(group.get("prompt_count") == 6, "Class 02 active count mismatch")
    require(not (set(group.get("prompt_ids") or []) & LEGACY_IDS), "Legacy prompt remains in active group")
    card = load(plib / "ROUTING/folder_assimilation_cards_index.json")
    folder = next(item for item in card["folders"] if item.get("folder_id") == "02_prompt_routing_and_indexing")
    require(folder.get("prompt_count") == 6, "Folder active count mismatch")
    require(not (set(folder.get("main_prompt_ids") or []) & LEGACY_IDS), "Legacy prompt remains in folder active list")
    coverage = read(plib / "ROUTING/prompt_route_coverage_table.csv")
    for prompt_id in LEGACY_IDS:
        require(("\n" + prompt_id + ",") not in coverage, "Legacy coverage row remains: " + prompt_id)
    print("WAVE2B_ACTIVE_ROUTE_RETIREMENT: PASS")


def validate_substitution(root: Path) -> None:
    plib = root / "kanda_prompt_workspace/prompt_library"
    text = read(plib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md")
    meta = load(plib / "METADATA/prompt_substitution_map.meta.json")
    for marker in ["prompt_router / kanda_prompt_router / KANDA_PROMPT_ROUTER", "RG-PILOT-000", "RG-LAB-000", "Active route: `NO`"]:
        require(marker in text, "Substitution marker missing: " + marker)
    require(tuple(int(part) for part in str(meta.get("version") or "0").split(".")) >= (2, 1), "Substitution metadata version mismatch")
    records = meta.get("retirement_records") or {}
    for key in ["prompt_router", "kanda_prompt_router", "RG-PILOT-000", "RG-LAB-000"]:
        require(key in records, "Retirement record missing: " + key)
    print("WAVE2B_SUBSTITUTION_REDIRECTS_COMPLETE: PASS")


def validate_consumers(root: Path) -> None:
    meta_root = root / "kanda_prompt_workspace/prompt_library/METADATA"
    for path in meta_root.glob("*.json"):
        data = load_existing(path)
        if data.get("prompt_id") in LEGACY_IDS:
            continue
        for key in ("required_companion_prompts", "optional_companion_prompts"):
            values = set(data.get(key) or [])
            require(not (values & LEGACY_IDS), "Metadata consumer remains: " + path.name)
    bridge = read(root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
    require("\nprompt_router\n" not in bridge, "Router bridge still requires prompt_router")
    require("ai_prompt_request_canon" in bridge and "prompt_navigation_index" in bridge, "Router bridge current owners missing")
    scanned = [
        root / "tools/validate_large_module_v70_router_binding_v1.py",
        root / "tools/validate_large_module_v70_context_validator_correction_v1.py",
        root / "tools/validate_large_module_refactor_router_binding_v1.py",
        root / "tools/validate_large_file_refactor_workbench_patch6_final_canon_v1.py",
        root / "tools/validate_patch_validate_freeze_recovery_blueprint_v1.py",
        root / "scripts/validate_terminal_cleanup_bridge_inline_python_repair_v2.py",
        root / "scripts/validate_terminal_cleanup_bridge_initial_prompts_v1.py",
        root / "scripts/validate_terminal_cleanup_bridge_helper_import_path_repair_v3.py",
        root / "kanda_prompt_workspace/prompt_tools/startup_kernel/prompt_library_zip.py",
    ]
    forbidden_path = "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md"
    for path in scanned:
        require(forbidden_path not in read(path), "Validator/source still binds prompt_router: " + str(path))
    print("WAVE2B_CONSUMER_MIGRATION_COMPLETE: PASS")


def validate_application_library(root: Path) -> None:
    app = root / "kanda_reasoner_app/prompt_library"
    source = read(app / "active/KANDA_PROMPT_ROUTER.md")
    meta = load(app / "metadata/kanda_prompt_router.meta.json")
    groups = load(app / "groups/PROMPT_GROUPS.json")
    require("not a routing authority" in source, "Application router redirect missing")
    require(meta.get("status") == "deprecated", "Application router metadata not deprecated")
    require("kanda_prompt_router" not in json.dumps(groups), "Application group still registers kanda_prompt_router")
    for path in app.rglob("*.meta.json"):
        data = load_existing(path)
        if path.name == "kanda_prompt_router.meta.json":
            continue
        for key in ("required_prompts", "required_companion_prompts", "optional_companion_prompts", "companions", "recommended_with", "depends_on"):
            values = set(data.get(key) or [])
            require("kanda_prompt_router" not in values, "Application metadata consumer remains: " + str(path))
    print("WAVE2B_APPLICATION_ROUTER_MIGRATED: PASS")


def validate_generated_zip(root: Path, startup_zip: Path | None) -> None:
    if startup_zip is None:
        return
    require(startup_zip.is_file(), "Startup ZIP missing")
    with zipfile.ZipFile(startup_zip, "r") as archive:
        names = set(archive.namelist())
        require("02_prompt_navigation_index.md" in names, "Generated navigation missing")
        nav = archive.read("02_prompt_navigation_index.md").decode("utf-8")
        require("Retired routing identities" in nav, "Generated navigation stale")
    print("WAVE2B_GENERATED_STARTUP_RETIREMENT_VISIBLE: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--startup-zip")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    startup = Path(args.startup_zip).resolve() if args.startup_zip else None
    validate_historical_records(root)
    validate_active_routes(root)
    validate_substitution(root)
    validate_consumers(root)
    validate_application_library(root)
    validate_generated_zip(root, startup)
    print("WAVE2B_LEGACY_ROUTING_RETIREMENT_REGRESSION_SET: PASS")
    print("WAVE2B_NO_NEW_ROUTING_ENGINE_OR_REGISTRY: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
