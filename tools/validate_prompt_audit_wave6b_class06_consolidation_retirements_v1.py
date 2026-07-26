"""Validate Prompt Audit Wave 6B Class 06 consolidation and retirements."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

__all__: list[str] = []

FEATURE_ID = "prompt-audit-wave6b-class06-consolidation-retirements-v1"
CLASS_ID = "06_refactor_and_architecture_hardening"
RETIRED = {
    "problem_set_roadmap_solver",
    "refactor_fragmentation_audit_runner",
    "tab1_tab2_audit_taxonomy",
}


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker + ": FAIL")
    print(marker + ": PASS")


def read_text(path: Path) -> str:
    require(path.is_file(), "MISSING_FILE_" + path.as_posix())
    data = path.read_bytes()
    require(not data.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN_" + path.name)
    require(b"\r\n" not in data, "CRLF_FORBIDDEN_" + path.name)
    return data.decode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(read_text(path))
    require(isinstance(loaded, dict), "JSON_OBJECT_" + path.name)
    return loaded


def version_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", str(value or "0")))


def validate_retirements(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    active = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata = library / "METADATA"
    for prompt_id in RETIRED:
        require(
            not (active / (prompt_id + ".md")).exists()
            and not (metadata / (prompt_id + ".meta.json")).exists(),
            "WAVE6B_RETIRED_" + prompt_id.upper(),
        )

    substitution = read_text(
        library
        / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md"
    )
    require(
        "## Wave 6B Class 06 consolidation and retirement records" in substitution
        and all(prompt_id in substitution for prompt_id in RETIRED)
        and "active_reduced_dispatcher" in substitution,
        "WAVE6B_SUBSTITUTION_RECORDS",
    )
    print("WAVE6B_GOVERNED_RETIREMENTS: PASS")


def validate_current_owners(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    active = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata = library / "METADATA"

    safe = read_text(active / "safe_refactor_how_to.md")
    for marker in (
        "Prompt code: `KPR-06-004`",
        "Version: 2.0.0",
        "user-facing KANDA safe-refactor refresher",
        "Specialist dispatch",
        "KPR-06-003",
        "KPR-06-005",
        "KPR-06-007",
        "There is no universal 101-line minimum",
        "Post-refactor verification route",
        "Appended support-artifact roles",
        "Non-authorization statement",
    ):
        require(marker in safe, "WAVE6B_SAFE_REFACTOR_MARKER")
    for forbidden in (
        "strictly more than 100 physical lines",
        "101 through 499 physical lines inclusive",
        "Drive-root staging law",
        "Governed release construction",
        "Required delivery response",
    ):
        require(forbidden not in safe, "WAVE6B_SAFE_REFACTOR_SCOPE")
    require(100 <= len(safe.splitlines()) <= 220, "WAVE6B_SAFE_REFACTOR_REDUCED")

    safe_meta = load_json(metadata / "safe_refactor_how_to.meta.json")
    require(
        safe_meta.get("prompt_code") == "KPR-06-004"
        and safe_meta.get("version") == "2.0.0"
        and safe_meta.get("status") == "active"
        and safe_meta.get("load_type") == "routed"
        and safe_meta.get("source_stage") == FEATURE_ID
        and len(safe_meta.get("support_artifacts", [])) == 3,
        "WAVE6B_SAFE_REFACTOR_METADATA",
    )

    architecture = read_text(active / "architecture_hardening_triage_protocol.md")
    architecture_meta = load_json(metadata / "architecture_hardening_triage_protocol.meta.json")
    require(
        "Version: 2.1.0" in architecture
        and "## Detector coverage record" in architecture
        and "new detector" in architecture.lower()
        and version_tuple(architecture_meta.get("version")) >= (2, 1, 0)
        and architecture_meta.get("source_stage") == FEATURE_ID,
        "WAVE6B_DETECTOR_TAXONOMY_MIGRATED",
    )

    large = read_text(active / "large_module_refactor_protocol.md")
    large_meta = load_json(metadata / "large_module_refactor_protocol.meta.json")
    require(
        "Version: 9.1.0" in large
        and "## Post-refactor verification ownership" in large
        and "do not create a parallel universal fragmentation runner" in large
        and version_tuple(large_meta.get("version")) >= (9, 1, 0)
        and large_meta.get("source_stage") == FEATURE_ID,
        "WAVE6B_FRAGMENTATION_TAXONOMY_MIGRATED",
    )
    print("WAVE6B_CLASS06_OWNER_CONSOLIDATION: PASS")


def validate_routing(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    routing = library / "ROUTING"
    nav = load_json(routing / "prompt_navigation_index.json")
    entries = list(nav.get("entries", []))
    ids = {str(item.get("prompt_id")) for item in entries if isinstance(item, dict)}
    require(nav.get("prompt_count") == len(entries), "WAVE6B_NAV_COUNT")
    require(not (RETIRED & ids), "WAVE6B_RETIRED_NAV_REMOVED")

    with (routing / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    coverage = {str(row.get("prompt_id")) for row in rows}
    require(not (RETIRED & coverage), "WAVE6B_RETIRED_COVERAGE_REMOVED")
    safe_row = next(row for row in rows if row.get("prompt_id") == "safe_refactor_how_to")
    require(
        "KPR-06-004" in str(safe_row.get("aliases"))
        and "brick_wall_comprehensive_quality_gate" in str(safe_row.get("companions"))
        and "freeze authority" in str(safe_row.get("when_not_to_load")),
        "WAVE6B_SAFE_ROUTE_NARROWED",
    )

    machine = load_json(routing / "group_assimilation_index.json")
    group = next(item for item in machine.get("groups", []) if item.get("group_id") == CLASS_ID)
    stems = {Path(name).stem for name in group.get("main_prompts", [])}
    require(
        group.get("prompt_count") == len(group.get("main_prompts", [])) == 8
        and not (RETIRED & stems)
        and "safe_refactor_how_to" in stems,
        "WAVE6B_MACHINE_GROUP_COUNT",
    )

    cards = load_json(routing / "folder_assimilation_cards_index.json")
    card = next(item for item in cards.get("folders", []) if item.get("folder_id") == CLASS_ID)
    card_ids = set(card.get("main_prompt_ids", []))
    require(
        card.get("prompt_count") == len(card_ids) == 4
        and not (RETIRED & card_ids),
        "WAVE6B_FOLDER_CARD_COUNT",
    )

    draft = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    draft_group = next(item for item in draft.get("groups", []) if item.get("group_id") == CLASS_ID)
    draft_ids = set(draft_group.get("prompt_ids", []))
    require(
        draft_group.get("prompt_count") == len(draft_ids) == 4
        and not (RETIRED & draft_ids),
        "WAVE6B_DRAFT_GROUP_COUNT",
    )

    human_group = read_text(routing / "GROUP_ASSIMILATION_INDEX.md")
    human_folder = read_text(routing / "FOLDER_ASSIMILATION_CARDS_INDEX.md")
    require(
        "| 06_refactor_and_architecture_hardening | 8 |" in human_group,
        "WAVE6B_HUMAN_GROUP_COUNT",
    )
    require(
        "| `06_refactor_and_architecture_hardening` | "
        "`ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md` | "
        "Current architecture triage and behavior-preserving refactor ownership without duplicate historical engines. | 4 |"
        in human_folder,
        "WAVE6B_HUMAN_FOLDER_COUNT",
    )
    print("WAVE6B_ACTIVE_ROUTING_RETIREMENT: PASS")


def validate_no_active_retired_references(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    allowed = {
        library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md",
        library / "ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md",
    }
    scan_roots = [
        library / "METADATA",
        library / "ROUTING",
        library / "GROUPS",
        library / "HUMAN_APPENDIX",
        library / "ACTIVE_PROMPTS",
    ]
    violations: list[str] = []
    for scan_root in scan_roots:
        for path in scan_root.rglob("*"):
            if not path.is_file() or path in allowed:
                continue
            if "RECONCILIATION_REPORTS" in path.parts:
                continue
            if path.suffix.lower() not in {".md", ".json", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            for retired in RETIRED:
                if retired in text:
                    violations.append(path.relative_to(root).as_posix() + ":" + retired)
    require(not violations, "WAVE6B_NO_ACTIVE_RETIRED_REFERENCES")


def validate_existing_roadmap_coverage(root: Path) -> None:
    path = root / (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "05_patch_delivery_and_validation/implementation_roadmap_builder.md"
    )
    text = read_text(path)
    for marker in (
        "Primary owner:",
        "Supporting owners:",
        "Dependencies:",
        "Risks:",
        "Validation or review evidence:",
        "Rollback or rejection condition:",
        "Authority source:",
    ):
        require(marker in text, "WAVE6B_ROADMAP_RECORD_COVERAGE")
    print("WAVE6B_PROBLEM_SEQUENCE_RECORD_MIGRATED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    validate_retirements(root)
    validate_current_owners(root)
    validate_routing(root)
    validate_no_active_retired_references(root)
    validate_existing_roadmap_coverage(root)
    print("WAVE6B_CLASS06_CONSOLIDATION_RETIREMENTS_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("WAVE6B_VALIDATION_ERROR: " + type(exc).__name__ + ": " + str(exc))
        raise
