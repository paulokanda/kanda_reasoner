"""Validate Prompt Audit Wave 4B Class 04 owner reconciliation."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import csv
import json
from pathlib import Path

FEATURE_ID = "prompt-audit-wave4b-box-architecture-boundaries-v1"
CLASS_ID = "04_box_architecture_and_boundaries"
ACTIVE = {
    "box_architecture_canon": ("KPR-04-001", "2.0"),
    "kanda_box_shielding_canon": ("KPR-04-002", "2.0"),
    "project_folder_organization_canon": ("KPR-04-003", "4.0"),
    "stateful_control_regression_canon": ("KPR-04-004", "2.0"),
    "boundary_first_repair_protocol": ("KPR-04-006", "2.0"),
}


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(f"{marker}: FAIL")
    print(f"{marker}: PASS")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def validate_prompts(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    class_root = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata = library / "METADATA"
    codes: list[str] = []
    for prompt_id, (code, version) in ACTIVE.items():
        prompt = read_text(class_root / f"{prompt_id}.md")
        meta = load_json(metadata / f"{prompt_id}.meta.json")
        require(
            f"prompt_id: {prompt_id}" in prompt
            and f"prompt_code: {code}" in prompt
            and f"version: {version}" in prompt
            and "status: active" in prompt
            and "source_write_authorization" not in prompt
            and len(prompt.splitlines()) <= 300,
            f"WAVE4B_ACTIVE_OWNER_{prompt_id.upper()}",
        )
        require(
            meta.get("prompt_id") == prompt_id
            and meta.get("prompt_code") == code
            and meta.get("version") == version
            and meta.get("status") == "active"
            and meta.get("load_type") == "routed"
            and meta.get("source_write_authorization") == "NO",
            f"WAVE4B_METADATA_{prompt_id.upper()}",
        )
        codes.append(code)
    require(len(codes) == len(set(codes)), "WAVE4B_CLASS04_CODE_UNIQUENESS")
    box = read_text(class_root / "box_architecture_canon.md")
    require(
        all(token in box for token in (
            "The active Project supplies its own implementation authorization and root/ownership model",
            "One primary responsibility owner per change",
            "atomic multi-owner contract migration",
            "BOX BOUNDARY AUDIT",
            "May begin coding from this audit: NO",
        )),
        "WAVE4B_BOX_ARCHITECTURE_SCOPE",
    )
    require(
        "Brick Wall is the final governed implementation-authority coordinator" not in box
        and "`project_tool_boundary_canon` owns Tool" not in box
        and "Project-agnostic operating rule" in box,
        "WAVE4B_BOX_ARCHITECTURE_AGNOSTIC_BOUNDARY",
    )
    boundary = read_text(class_root / "boundary_first_repair_protocol.md")
    require(
        all(token in boundary for token in (
            "Change correlation: PROVEN_CAUSAL / PLAUSIBLE / TEMPORAL_ONLY / UNKNOWN",
            "Disconfirming evidence:",
            "Boundary diagnosis status: OWNER_PROVEN / OWNER_PROVISIONAL / OWNER_UNRESOLVED",
            "May write source: NO",
        )),
        "WAVE4B_BOUNDARY_FIRST_SCOPE",
    )
    shield = read_text(class_root / "kanda_box_shielding_canon.md")
    require(
        all(token in shield for token in (
            "Shielding is risk-based, not milestone-automatic",
            "SHIELD APPLICABILITY DECISION",
            "Simpler existing-test strengthening sufficient",
            "May write snapshot/freeze state from this record: NO",
        )),
        "WAVE4B_SHIELDING_SCOPE",
    )
    folder = read_text(class_root / "project_folder_organization_canon.md")
    require(
        all(token in folder for token in (
            "consumes root identities from the active Project\'s declared root/ownership authority",
            "ARTIFACT PLACEMENT ASSESSMENT",
            "Generated / durable / transient status",
            "May write source from this assessment: NO",
        )),
        "WAVE4B_FOLDER_PLACEMENT_SCOPE",
    )
    control = read_text(class_root / "stateful_control_regression_canon.md")
    require(
        all(token in control for token in (
            "Stable ID schema and version",
            "Signals suppressed or event origin classified",
            "STALE_RESULT_REJECTED",
            "May write source: NO",
        )),
        "WAVE4B_STATEFUL_CONTROL_SCOPE",
    )


def validate_retirements(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    class_root = library / "ACTIVE_PROMPTS" / CLASS_ID
    require(
        not (class_root / "closed_box_delivery_canon.md").exists()
        and not (library / "METADATA" / "closed_box_delivery_canon.meta.json").exists(),
        "WAVE4B_CLOSED_BOX_OWNER_RETIRED",
    )
    companion = read_text(class_root / "governed_architecture_companion_handoff.md")
    meta = load_json(
        library / "METADATA" / "governed_architecture_companion_handoff.meta.json"
    )
    require(
        "status: deprecated" in companion
        and "load_type: never" in companion
        and len(companion.splitlines()) <= 80
        and meta.get("status") == "deprecated"
        and meta.get("active_route") is False,
        "WAVE4B_COMPILED_COMPANION_RETIRED",
    )


def validate_routing(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    nav = load_json(library / "ROUTING" / "prompt_navigation_index.json")
    class_entries = [
        entry for entry in nav.get("entries", [])
        if entry.get("category") == CLASS_ID
    ]
    require(
        {entry.get("prompt_id") for entry in class_entries} == set(ACTIVE)
        and nav.get("prompt_count") == len(nav.get("entries", [])),
        "WAVE4B_MACHINE_NAVIGATION_OWNER_SET",
    )
    groups = load_json(library / "ROUTING" / "group_assimilation_index.json")
    group = next(g for g in groups.get("groups", []) if g.get("group_id") == CLASS_ID)
    require(
        group.get("prompt_count") == 5
        and set(group.get("main_prompts", []))
        == {f"{prompt_id}.md" for prompt_id in ACTIVE},
        "WAVE4B_GROUP_OWNER_SET",
    )
    require(
        not any(
            route.get("task_intent") == "GOVERNED_ARCHITECTURE_COMPANION"
            for route in groups.get("task_routes", [])
        ),
        "WAVE4B_RETIRED_GROUP_ROUTE_REMOVED",
    )
    with (library / "ROUTING" / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    class_rows = [row for row in rows if row.get("category") == CLASS_ID]
    require(
        {row.get("prompt_id") for row in class_rows} == set(ACTIVE),
        "WAVE4B_ROUTE_COVERAGE_OWNER_SET",
    )
    substitution = read_text(
        library / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing"
        / "prompt_substitution_map.md"
    )
    require(
        "closed_box_delivery_canon" in substitution
        and "current canonical owner dispatch" in substitution,
        "WAVE4B_SUBSTITUTION_COVERAGE",
    )


def validate_bridges(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    startup = read_text(
        library / "ACTIVE_PROMPTS" / "01_session_start_and_navigation"
        / "start_of_day_master_stack.md"
    )
    require(
        "Class 04 Architecture Owner Dispatch Bridge" in startup
        and "Do not load the retired compiled architecture companion" in startup
        and "Load `governed_architecture_companion_handoff`" not in startup,
        "WAVE4B_STARTUP_DIRECT_OWNER_DISPATCH",
    )
    bridge = read_text(
        library / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation"
        / "router_bridge_governed_implementation.md"
    )
    require(
        "the retired architecture companion is never loaded" in bridge
        and len(bridge.splitlines()) <= 500,
        "WAVE4B_ROUTER_BRIDGE_DIRECT_OWNER_DISPATCH",
    )
    start_here = read_text(
        project_root / "kanda_prompt_workspace" / "prompt_tools"
        / "startup_kernel" / "start_here_lists.py"
    )
    require(
        "4. Class 04 Architecture Owner Dispatch" in start_here
        and "full governed_architecture_companion_handoff" not in start_here,
        "WAVE4B_START_HERE_DIRECT_OWNER_DISPATCH",
    )


def validate_negative_guards(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    texts = "\n".join(
        read_text(path)
        for path in (library / "ACTIVE_PROMPTS" / CLASS_ID).glob("*.md")
    )
    require(
        "If the user says \"go\"" not in texts
        and "full governed architecture companion" not in texts.lower()
        and "must be frozen after every milestone" not in texts.lower(),
        "WAVE4B_NEGATIVE_AUTHORITY_AND_MEGA_OWNER_GUARDS",
    )
    require(
        not any(
            token in texts
            for token in (
                "<PROJECT_ROOT>/project_analysis_evidence",
                "APP_MAINTENANCE_ROOT",
                "Routing Signal Scorer Shield Profile",
            )
        ),
        "WAVE4B_STALE_SPECIALIST_POLICY_REMOVED",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    validate_prompts(root)
    validate_retirements(root)
    validate_routing(root)
    validate_bridges(root)
    validate_negative_guards(root)
    print("WAVE4B_BOX_ARCHITECTURE_BOUNDARIES_REGRESSION_SET: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"WAVE4B_VALIDATION_ERROR: {type(exc).__name__}: {exc}")
        raise
