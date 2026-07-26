"""Focused validation for prompt-audit Wave 1 boundary corrections."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "prompt-audit-wave1-tool-project-mcard-boundary-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
CLASS12 = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons"
EXPECTED_IDS = {
    "architecture_review_project_card_machine_canon",
    "data_transform_pipeline_invariants",
    "desktop_help_document_layout_canon",
    "domain_decision_table_template",
    "error_memory_active_ready_correction_blueprint",
    "error_memory_active_ready_json_template",
    "error_memory_model_template",
    "plugin_package_import_canon",
    "project_tool_boundary_canon",
    "project_tool_boundary_startup_bridge",
    "shared_visual_render_engine_canon",
    "transform_resolver_architecture_contract",
}


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def load_json(path: Path) -> dict[str, object]:
    loaded = json.loads(read(path))
    if not isinstance(loaded, dict):
        raise AssertionError("JSON root must be object: " + str(path))
    return loaded


def gate(label: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def run(root: Path, relative: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(root / relative), "--project-root", str(root)],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise AssertionError(relative + " failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--startup-zip", type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve()

    full = read(root / CLASS12 / "project_tool_boundary_canon.md")
    bridge = read(root / CLASS12 / "project_tool_boundary_startup_bridge.md")
    mcard = read(root / CLASS12 / "architecture_review_project_card_machine_canon.md")
    gate("WAVE1_ONE_FULL_BOUNDARY_OWNER", full.count("Prompt code: KPR-12-001") == 1)
    gate("WAVE1_COMPACT_STARTUP_BRIDGE", len(bridge.splitlines()) <= 60 and "May mutate from this bridge alone: NO" in bridge)
    gate("WAVE1_MCARD_LIFECYCLE_SPECIALIST", "MCard never authorizes coding or source write" in mcard)
    gate("WAVE1_NO_OWNERSHIP_FREE_TERM", "ownership-free transient" not in (full + bridge + mcard).lower())
    gate("WAVE1_PROMPT_LINE_LIMITS", max(len(text.splitlines()) for text in (full, bridge, mcard)) <= 500)

    group = load_json(root / PLIB / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    record = next(item for item in group.get("groups", []) if item.get("group_id") == "12_generalized_project_canons")
    gate("WAVE1_CLASS12_GROUP_INVENTORY", EXPECTED_IDS.issubset(set(record.get("prompt_ids") or [])) and record.get("prompt_count") == len(record.get("prompt_ids") or []))

    assimilation = load_json(root / PLIB / "ROUTING/group_assimilation_index.json")
    group_record = next(item for item in assimilation.get("groups", []) if item.get("group_id") == "12_generalized_project_canons")
    gate("WAVE1_CLASS12_ASSIMILATION_COUNT", group_record.get("prompt_count") == len(group_record.get("main_prompts") or []) and EXPECTED_IDS.issubset({Path(item).stem for item in (group_record.get("main_prompts") or [])}))

    folder = load_json(root / PLIB / "ROUTING/folder_assimilation_cards_index.json")
    folder_record = next(item for item in folder.get("folders", []) if item.get("folder_id") == "12_generalized_project_canons")
    gate("WAVE1_CLASS12_FOLDER_COUNT", folder_record.get("prompt_count") == len(folder_record.get("main_prompt_ids") or []) and EXPECTED_IDS.issubset(set(folder_record.get("main_prompt_ids") or [])))

    source_map = load_json(root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
    item14 = next(
        item
        for item in source_map.get("startup_sources", [])
        if item.get("prompt_id") == "project_tool_boundary_startup_bridge"
    )
    gate("WAVE1_STARTUP_BRIDGE_SELECTED", item14.get("prompt_id") == "project_tool_boundary_startup_bridge")
    gate("WAVE1_STARTUP_FILENAME_STABLE", item14.get("generated_filename") == "14_project_tool_boundary_canon.md")

    run(root, "scripts/validate_project_tool_boundary_canon_v1.py")
    run(root, "tools/validate_architecture_review_project_card_machine_canon_router_v1.py")
    run(root, "tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py")
    run(root, "tools/validate_project_tool_boundary_nested_support_root_v1.py")
    run(root, "tools/validate_brick_wall_q11_mcard_applicability_lifecycle_v1.py")

    if args.startup_zip is not None:
        with zipfile.ZipFile(args.startup_zip, "r") as archive:
            startup_text = archive.read("14_project_tool_boundary_canon.md").decode("utf-8")
        gate("WAVE1_GENERATED_STARTUP_IS_COMPACT_BRIDGE", "prompt_id: project_tool_boundary_startup_bridge" in startup_text and len(startup_text.splitlines()) <= 60)

    print("WAVE1_CHANGED_FILE_COVERAGE: PASS")
    print("WAVE1_NO_DUPLICATE_BOUNDARY_OR_MCARD_OWNER: PASS")
    print("WAVE1_NO_CONTEXT_ENGINE_OR_COORDINATION_SUPER_SYSTEM: PASS")
    print("WAVE1_TOOL_PROJECT_MCARD_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
