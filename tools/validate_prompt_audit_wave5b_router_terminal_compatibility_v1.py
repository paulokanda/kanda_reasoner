"""Validate Prompt Audit Wave 5B Router and terminal reconciliation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
import csv
import json
from pathlib import Path

FEATURE_ID = "prompt-audit-wave5b-router-terminal-compatibility-v1"
CLASS_ID = "05_patch_delivery_and_validation"
ACTIVE = {
    "router_bridge_user_detected_correction": ("KPR-05-006", "2.0", "routed"),
    "terminal_cleanup_contract": ("KPR-05-007", "2.0", "always_startup"),
}
TOMBSTONES = {
    "router_bridge_governed_implementation": "brick_wall_comprehensive_quality_gate",
    "router_bridge_patch_delivery_contract": "pre_output_contract_gates",
    "universal_delivery_protocol": "implementation_and_delivery_protocol",
}
CORE = {
    "patch_install_delivery_error_register",
    "bundle_gated_development_workflow",
    "implementation_and_delivery_protocol",
    "implementation_roadmap_builder",
    "patch_validate_freeze_error_memory_routine_blueprint",
}
EXPECTED_ACTIVE = CORE | set(ACTIVE)


def gate(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ": FAIL" + (" - " + detail if detail else ""))
    print(name + ": PASS" + (" - " + detail if detail else ""))


def read(path: Path) -> str:
    gate("WAVE5B_REQUIRED_FILE", path.is_file(), str(path))
    data = path.read_bytes()
    gate("WAVE5B_UTF8_NO_BOM", not data.startswith(b"\xef\xbb\xbf"), path.name)
    gate("WAVE5B_LF_ONLY", b"\r\n" not in data, path.name)
    return data.decode("utf-8")


def load(path: Path) -> dict:
    return json.loads(read(path))


def validate_prompts(root: Path) -> None:
    lib = root / "kanda_prompt_workspace/prompt_library"
    class_root = lib / "ACTIVE_PROMPTS" / CLASS_ID
    meta_root = lib / "METADATA"
    correction = read(class_root / "router_bridge_user_detected_correction.md")
    terminal = read(class_root / "terminal_cleanup_contract.md")
    for prompt_id, (code, version, load_type) in ACTIVE.items():
        text = correction if prompt_id.startswith("router") else terminal
        meta = load(meta_root / (prompt_id + ".meta.json"))
        gate("WAVE5B_ACTIVE_IDENTITY", f"prompt_id: {prompt_id}" in text, prompt_id)
        gate("WAVE5B_ACTIVE_CODE", f"prompt_code: {code}" in text and meta.get("prompt_code") == code, prompt_id)
        gate("WAVE5B_ACTIVE_VERSION", f"version: {version}" in text and meta.get("version") == version, prompt_id)
        gate("WAVE5B_ACTIVE_STATUS", "status: active" in text and meta.get("status") == "active", prompt_id)
        gate("WAVE5B_ACTIVE_LOAD", f"load_type: {load_type}" in text and meta.get("load_type") == load_type, prompt_id)
        gate("WAVE5B_ACTIVE_STAGE", meta.get("source_stage") == FEATURE_ID and meta.get("updated_for") == FEATURE_ID, prompt_id)
        gate("WAVE5B_ACTIVE_SIZE", len(text.splitlines()) <= 300, prompt_id)
    for marker in (
        "CORRECTION INCIDENT RECORD",
        "May begin correction coding: NO",
        "Direct owner dispatch",
        "Always classify Error Memory applicability",
        "cannot authorize implementation",
    ):
        gate("WAVE5B_CORRECTION_DISPATCH", marker in correction, marker)
    gate("WAVE5B_CORRECTION_NO_RETIRED_REQUIREMENT", all(name not in load(lib / "METADATA/router_bridge_user_detected_correction.meta.json").get("required_companion_prompts", []) for name in TOMBSTONES))
    for marker in (
        "Clean-prompt entry guard",
        "If `>>` is visible",
        "NONINTERACTIVE_AUTOMATION",
        "INSTALL_SUCCESS",
        "INSTALL_ERROR",
        "PHASE",
        "ERROR TYPE",
        "Read-Host \"Press Enter to clear terminal\"",
        "Start-Sleep -Seconds 2",
        "must not use `else` or `elseif`",
    ):
        gate("WAVE5B_TERMINAL_CONTRACT", marker in terminal, marker)


def validate_tombstones(root: Path) -> None:
    lib = root / "kanda_prompt_workspace/prompt_library"
    class_root = lib / "ACTIVE_PROMPTS" / CLASS_ID
    meta_root = lib / "METADATA"
    for prompt_id, replacement in TOMBSTONES.items():
        text = read(class_root / (prompt_id + ".md"))
        meta = load(meta_root / (prompt_id + ".meta.json"))
        gate("WAVE5B_TOMBSTONE_STATUS", "status: deprecated" in text and meta.get("status") == "deprecated", prompt_id)
        gate("WAVE5B_TOMBSTONE_NO_ROUTE", "active_route: false" in text and meta.get("active_route") is False and meta.get("load_type") == "never", prompt_id)
        gate("WAVE5B_TOMBSTONE_REPLACEMENT", replacement in text and meta.get("canonical_replacement") == replacement, prompt_id)
        gate("WAVE5B_TOMBSTONE_NONAUTHORITY", "cannot" in text.lower() or "Do not load or execute" in text, prompt_id)
        gate("WAVE5B_TOMBSTONE_SIZE", len(text.splitlines()) <= 500, prompt_id)


def validate_routing(root: Path) -> None:
    lib = root / "kanda_prompt_workspace/prompt_library"
    nav = load(lib / "ROUTING/prompt_navigation_index.json")
    entries = list(nav.get("entries", [])); by_id = {row.get("prompt_id"): row for row in entries}
    gate("WAVE5B_NAV_COUNT", nav.get("prompt_count") == len(entries))
    gate("WAVE5B_RETIRED_ROUTES_REMOVED", not (set(TOMBSTONES) & set(by_id)))
    for prompt_id, (code, _, load_type) in ACTIVE.items():
        row = by_id.get(prompt_id, {})
        gate("WAVE5B_ACTIVE_ROUTE", row.get("prompt_code") == code and row.get("load_type") == load_type and row.get("category") == CLASS_ID, prompt_id)
    groups = load(lib / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(row for row in groups.get("groups", []) if row.get("group_id") == CLASS_ID)
    gate("WAVE5B_DRAFT_GROUP", group.get("prompt_count") == len(group.get("prompt_ids", [])) and set(group.get("prompt_ids", [])) == EXPECTED_ACTIVE)
    machine = load(lib / "ROUTING/group_assimilation_index.json")
    group = next(row for row in machine.get("groups", []) if row.get("group_id") == CLASS_ID)
    gate("WAVE5B_MACHINE_GROUP", group.get("prompt_count") == len(group.get("main_prompts", [])) and {Path(x).stem for x in group.get("main_prompts", [])} == EXPECTED_ACTIVE)
    cards = load(lib / "ROUTING/folder_assimilation_cards_index.json")
    card = next(row for row in cards.get("folders", []) if row.get("folder_id") == CLASS_ID)
    gate("WAVE5B_FOLDER_CARD", card.get("prompt_count") == len(card.get("main_prompt_ids", [])) and set(card.get("main_prompt_ids", [])) == EXPECTED_ACTIVE)
    with (lib / "ROUTING/prompt_route_coverage_table.csv").open("r", encoding="utf-8", newline="") as handle:
        coverage = {row.get("prompt_id"): row for row in csv.DictReader(handle)}
    gate("WAVE5B_COVERAGE_NO_TOMBSTONE", not (set(TOMBSTONES) & set(coverage)))
    gate("WAVE5B_COVERAGE_ACTIVE", set(ACTIVE).issubset(coverage))
    active_dependency_text = "\n".join(
        str(row.get("companions", ""))
        for row in coverage.values()
    )
    gate(
        "WAVE5B_COVERAGE_NO_RETIRED_DEPENDENCY",
        not any(name in active_dependency_text for name in TOMBSTONES),
    )
    nav_dependency_text = json.dumps(entries, ensure_ascii=True, sort_keys=True)
    gate(
        "WAVE5B_NAV_NO_RETIRED_DEPENDENCY",
        not any(name in nav_dependency_text for name in TOMBSTONES),
    )
    human_navigation = read(lib / "ROUTING/PROMPT_NAVIGATION_INDEX.md")
    gate(
        "WAVE5B_HUMAN_NAV_NO_RETIRED_DEPENDENCY",
        not any(name in human_navigation for name in TOMBSTONES),
    )
    substitution = read(lib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md")
    gate("WAVE5B_SUBSTITUTION_RECORDS", "## Wave 5B Router and terminal compatibility records" in substitution and all(name in substitution for name in TOMBSTONES))


def validate_generic_template(root: Path) -> None:
    app = root / "kanda_reasoner_app/prompt_library"
    old = app / "active/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.0.md"
    draft = app / "drafts/PROJECT_AGNOSTIC_DELIVERY_PLANNING_TEMPLATE.md"
    meta = load(app / "metadata/0000_0_8_universal_delivery_protocol.meta.json")
    text = read(draft)
    gate("WAVE5B_GENERIC_ACTIVE_REMOVED", not old.exists())
    gate("WAVE5B_GENERIC_DRAFT_ONLY", meta.get("status") == "draft" and meta.get("load_type") == "manual_only" and meta.get("governance_linked") is False)
    gate("WAVE5B_GENERIC_NO_KANDA_AUTHORITY", "Never use this template to override KANDA Reasoner governance" in text)
    gate("WAVE5B_GENERIC_NO_DIRECT_EXTRACTION", "assume direct ZIP extraction is safe" in text)


def validate_startup_and_validators(root: Path) -> None:
    master = read(root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md")
    gate("WAVE5B_TERMINAL_STARTUP_BRIDGE", "KPR-05-007 terminal_cleanup_contract" in master and "if `>>` is visible" in master and "Noninteractive automation" in master)
    folder = read(root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/_FOLDER_ASSIMILATION.md")
    gate("WAVE5B_CLASS05_OWNER_RECONCILIATION", all(code in folder for code in ("KPR-05-001", "KPR-05-002", "KPR-05-003", "KPR-05-004", "KPR-05-005", "KPR-05-006", "KPR-05-007")))
    for rel in (
        "scripts/validate_bridge_error_memory_implementation_error_gate_v1.py",
        "tools/validate_terminal_cleanup_contract_startup_bridge_v1.py",
        "tools/validate_prompt_audit_wave5a_patch_lifecycle_core_v1.py",
        "tools/validate_prompt_audit_wave5b_router_terminal_compatibility_v1.py",
    ):
        path = root / rel; text = read(path); ast.parse(text, filename=rel)
        gate("WAVE5B_VALIDATOR_MAX_500", len(text.splitlines()) <= 500, rel)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--project-root", required=True)
    args = parser.parse_args(); root = Path(args.project_root).resolve()
    validate_prompts(root); validate_tombstones(root); validate_routing(root)
    validate_generic_template(root); validate_startup_and_validators(root)
    print("WAVE5B_ROUTER_TERMINAL_COMPATIBILITY_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
