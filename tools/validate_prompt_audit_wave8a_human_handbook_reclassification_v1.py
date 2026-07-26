"""Validate Wave 8A human-process and handbook reclassification."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from zipfile import ZipFile

FEATURE_ID = "prompt-audit-wave8a-human-handbook-reclassification-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    lib = root / "kanda_prompt_workspace/prompt_library"
    active08 = lib / "ACTIVE_PROMPTS/08_python_engineering_core"
    active12 = lib / "ACTIVE_PROMPTS/12_generalized_project_canons"
    meta_root = lib / "METADATA"
    routing = lib / "ROUTING"

    old_paths = [
        active08 / "peopleware_team_boundary.md",
        active08 / "practical_field_handbook_template.md",
    ]
    for path in old_paths:
        require(not path.exists(), "Retired Class 08 path still exists: " + str(path))

    people_path = active12 / "peopleware_team_boundary.md"
    handbook_path = active12 / "practical_field_handbook_template.md"
    require(people_path.is_file(), "KPR-12-007 source missing")
    require(handbook_path.is_file(), "KPR-12-008 source missing")

    people = read(people_path)
    handbook = read(handbook_path)
    for marker in (
        "prompt_code: KPR-12-007",
        "Human-process versus technical classification",
        "Privacy and anti-surveillance rules",
        "Do not diagnose burnout",
        "does not authorize source mutation",
    ):
        require(marker in people, "Peopleware marker missing: " + marker)
    for forbidden in (
        "10\u201320 times more productive",
        "80% async, 20% sync",
        "fails if a commit is after 10pm",
        "I am now acting as a Peopleware expert",
    ):
        require(forbidden not in people, "Peopleware stale doctrine remains: " + forbidden)

    for marker in (
        "prompt_code: KPR-12-008",
        "SOURCE ACCESS MODE",
        "SOURCE-DERIVED",
        "Copyright-safe synthesis",
        "SOURCE_UNAVAILABLE",
        "does not authorize\nsource mutation",
    ):
        require(marker in handbook, "Handbook marker missing: " + marker)
    for forbidden in (
        "follow this order exactly",
        "reply GO to continue",
        "All code examples must be in [DOMAIN]",
        "30-DAY ADOPTION PLAN",
    ):
        require(forbidden not in handbook, "Handbook stale doctrine remains: " + forbidden)

    expected = {
        "peopleware_team_boundary": ("KPR-12-007", "active"),
        "practical_field_handbook_template": ("KPR-12-008", "active_template"),
    }
    for prompt_id, (code, status) in expected.items():
        meta = json.loads(read(meta_root / (prompt_id + ".meta.json")))
        require(meta.get("prompt_code") == code, prompt_id + " prompt_code mismatch")
        require(meta.get("category") == "12_generalized_project_canons", prompt_id + " category mismatch")
        require(meta.get("status") == status, prompt_id + " status mismatch")
        require(meta.get("load_type") == "on_request", prompt_id + " load_type mismatch")
        require(meta.get("box_logic_required") is False, prompt_id + " box logic flag must be false")

    groups = json.loads(read(lib / "GROUPS/PROMPT_GROUPS_DRAFT.json"))["groups"]
    g08 = next(g for g in groups if g["group_id"] == "08_python_engineering_core")
    g12 = next(g for g in groups if g["group_id"] == "12_generalized_project_canons")
    for prompt_id in expected:
        require(prompt_id not in g08["prompt_ids"], prompt_id + " remains in Class 08 group")
        require(prompt_id in g12["prompt_ids"], prompt_id + " missing from Class 12 group")
    require(g08.get("prompt_count") == 10, "Class 08 group count mismatch")
    require(g12.get("prompt_count") == 14, "Class 12 group count mismatch")

    nav = json.loads(read(routing / "prompt_navigation_index.json"))
    entries = {e.get("prompt_id"): e for e in nav.get("entries", [])}
    for prompt_id, (code, _status) in expected.items():
        entry = entries[prompt_id]
        require(entry.get("category") == "12_generalized_project_canons", prompt_id + " nav category mismatch")
        require(entry.get("prompt_code") == code, prompt_id + " nav code mismatch")
        require(entry.get("relative_path", "").startswith("ACTIVE_PROMPTS/12_generalized_project_canons/"), prompt_id + " nav path mismatch")

    with (routing / "prompt_route_coverage_table.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        coverage = {row["prompt_id"]: row for row in csv.DictReader(handle)}
    for prompt_id in expected:
        require(coverage[prompt_id]["category"] == "12_generalized_project_canons", prompt_id + " coverage category mismatch")

    group_index = json.loads(read(routing / "group_assimilation_index.json"))["groups"]
    gi08 = next(g for g in group_index if g["group_id"] == "08_python_engineering_core")
    gi12 = next(g for g in group_index if g["group_id"] == "12_generalized_project_canons")
    require(gi08.get("prompt_count") == 10, "Class 08 assimilation count mismatch")
    require(gi12.get("prompt_count") == 14, "Class 12 assimilation count mismatch")

    cards = json.loads(read(routing / "folder_assimilation_cards_index.json"))
    records = cards.get("folders", cards.get("cards", []))
    c08 = next(g for g in records if g["folder_id"] == "08_python_engineering_core")
    c12 = next(g for g in records if g["folder_id"] == "12_generalized_project_canons")
    require(c08.get("prompt_count") == 10, "Class 08 folder-card count mismatch")
    require(c12.get("prompt_count") == 14, "Class 12 folder-card count mismatch")

    startup_map = root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    startup_text = read(startup_map)
    require("peopleware_team_boundary" not in startup_text, "Peopleware must not become startup-loaded")
    require("practical_field_handbook_template" not in startup_text, "Handbook must not become startup-loaded")

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        show_project_to_ai_root_from_hint,
    )
    first_prompt_dir = show_project_to_ai_root_from_hint(root) / "first_prompt_files"
    prompt_library_zip = first_prompt_dir / "prompt_library.zip"
    startup_zip = first_prompt_dir / "first_prompts_to_ai.zip"
    require(prompt_library_zip.is_file(), "Generated prompt_library.zip missing")
    require(startup_zip.is_file(), "Generated startup ZIP missing")
    with ZipFile(prompt_library_zip) as archive:
        names = set(archive.namelist())
    require("ACTIVE_PROMPTS/12_generalized_project_canons/peopleware_team_boundary.md" in names, "Peopleware missing from generated prompt library ZIP")
    require("ACTIVE_PROMPTS/12_generalized_project_canons/practical_field_handbook_template.md" in names, "Handbook missing from generated prompt library ZIP")
    require("ACTIVE_PROMPTS/08_python_engineering_core/peopleware_team_boundary.md" not in names, "Old Peopleware path remains in prompt library ZIP")
    require("ACTIVE_PROMPTS/08_python_engineering_core/practical_field_handbook_template.md" not in names, "Old handbook path remains in prompt library ZIP")
    with ZipFile(startup_zip) as archive:
        startup_payload = "\n".join(
            archive.read(name).decode("utf-8-sig", errors="replace")
            for name in archive.namelist()
            if name.endswith(".md")
        )
    require("# Peopleware Team Boundary" not in startup_payload, "Peopleware source must remain on-request")
    require("# Practical Field Handbook Template" not in startup_payload, "Handbook source must remain on-request")

    active_nav = read(lib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md")
    require("KPR-12-007 = peopleware_team_boundary" in active_nav, "KPR-12-007 startup navigation registration missing")
    require("KPR-12-008 = practical_field_handbook_template" in active_nav, "KPR-12-008 startup navigation registration missing")

    print("WAVE8A_CLASS08_NON_PYTHON_REMOVAL: PASS")
    print("WAVE8A_CLASS12_RECLASSIFICATION: PASS")
    print("WAVE8A_PEOPLEWARE_PRIVACY_BOUNDARY: PASS")
    print("WAVE8A_HANDBOOK_PROVENANCE_BOUNDARY: PASS")
    print("WAVE8A_ROUTING_COMPLETENESS: PASS")
    print("WAVE8A_NO_STARTUP_PROMOTION: PASS")
    print("WAVE8A_HUMAN_HANDBOOK_RECLASSIFICATION_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
