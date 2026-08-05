"""Validate Prompt Audit Wave 5A Class 05 lifecycle reconciliation."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import csv
import json
from pathlib import Path

FEATURE_ID = "prompt-audit-wave5a-patch-lifecycle-core-v1"
CLASS_ID = "05_patch_delivery_and_validation"
ACTIVE = {
    "bundle_gated_development_workflow": ("KPR-05-002", "2.0", "routed"),
    "implementation_and_delivery_protocol": ("KPR-05-003", "2.0", "routed"),
    "implementation_roadmap_builder": ("KPR-05-004", "2.0", "on_request"),
    "patch_validate_freeze_error_memory_routine_blueprint": (
        "KPR-05-005",
        "3.2",
        "on_request",
    ),
}
RETIRED = {
    "evidence_freshness_gate",
    "patch_registry_validation_freeze",
}
MAIN_IDS = {
    "bundle_gated_development_workflow",
    "implementation_and_delivery_protocol",
    "implementation_roadmap_builder",
    "patch_install_delivery_error_register",
    "patch_validate_freeze_error_memory_routine_blueprint",
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


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def version_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(part) for part in str(value).split("."))


def validate_active_prompts(root: Path) -> None:
    library = root / "kanda_prompt_workspace" / "prompt_library"
    class_root = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata_root = library / "METADATA"
    codes: set[str] = set()
    markers = {
        "bundle_gated_development_workflow": (
            "RELEASE WORKFLOW STATUS",
            "CONTRACT_VALIDATED",
            "LOCALLY_VALIDATED",
            "atomic multi-owner contract migration",
            "historical aliases",
            "cannot authorize source writes",
        ),
        "implementation_and_delivery_protocol": (
            "SURGICAL DELIVERY INPUT",
            "raw backslash separators",
            "unknown third hash",
            "<project_drive>/<project_name>_delete_after_daily_work",
            "restore all changed and deleted files",
            "cannot authorize coding",
        ),
        "implementation_roadmap_builder": (
            "Draft Template",
            "CONCEPTUAL",
            "SOURCE_GROUNDED",
            "RELEASE_READY_DRAFT",
            "tracker is a human convenience",
            "cannot authorize source writes",
        ),
        "patch_validate_freeze_error_memory_routine_blueprint": (
            "canonical continuation wrapper",
            "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT",
            "ROUTINE_POST_IMPLEMENTATION_COMPLETION",
            "INSTALLATION_FAILURE",
            "No ZIP link may be emitted alone",
            "Need new training prompt: NO",
            "ANSWER VALIDATE FREEZE MEMORIZE ROUTINE BLOCKED",
            "does not itself authorize implementation",
            "Paste-safe PowerShell hard gate",
            "Windows PowerShell 5.1-compatible APIs",
            "One self-contained feature ZIP",
            "Required user-visible delivery shape",
            "Terminal 1 - INSTALL",
            "Terminal 2 - VALIDATE",
            "Terminal 3 - FREEZE",
            "Terminal 4 - ERROR MEMORY",
            "No-orphan-report rule",
        ),
    }
    forbidden = {
        "bundle_gated_development_workflow": (
            "KANDA_ERROR_LESSON_JSON_BEGIN",
            "Compress-Archive",
            "Read-Host",
            "FREEZE FORM JSON",
        ),
        "implementation_and_delivery_protocol": (
            "May begin coding: YES",
            "Confirm and Write schema",
            "final response must contain",
        ),
        "implementation_roadmap_builder": (
            "A049",
            "exactly 7 phases",
            "completion percentage",
            "minimum 5 items",
        ),
        "patch_validate_freeze_error_memory_routine_blueprint": (
            "Windows 11 Install code contract",
            "pending_ai_assisted_error_lesson_intake",
            "router_bridge_patch_delivery_contract,",
        ),
    }
    for prompt_id, (code, version, load_type) in ACTIVE.items():
        text = read_text(class_root / (prompt_id + ".md"))
        meta = load_json(metadata_root / (prompt_id + ".meta.json"))
        require(
            f"prompt_id: {prompt_id}" in text
            and f"prompt_code: {code}" in text
            and f"version: {version}" in text
            and "status: active" in text
            and f"load_type: {load_type}" in text
            and len(text.splitlines()) <= 300,
            "WAVE5A_SOURCE_" + prompt_id.upper(),
        )
        require(
            meta.get("prompt_id") == prompt_id
            and meta.get("prompt_code") == code
            and version_tuple(meta.get("version", "0")) >= version_tuple(version)
            and meta.get("status") == "active"
            and meta.get("load_type") == load_type
            and meta.get("owner_box") == CLASS_ID
            and meta.get("source_stage") == (
                "separated-terminal-release-phases-v1"
                if prompt_id == "patch_validate_freeze_error_memory_routine_blueprint"
                else FEATURE_ID
            )
            and meta.get("updated_for") == meta.get("source_stage")
            and meta.get("source_write_authorization") == "NO",
            "WAVE5A_METADATA_" + prompt_id.upper(),
        )
        for marker in markers[prompt_id]:
            require(marker in text, "WAVE5A_MARKER_" + prompt_id.upper())
        for marker in forbidden[prompt_id]:
            require(marker not in text, "WAVE5A_FORBIDDEN_" + prompt_id.upper())
        require(code not in codes, "WAVE5A_CODE_UNIQUENESS")
        codes.add(code)
    print("WAVE5A_ACTIVE_CORE_OWNERS: PASS")


def validate_retirements(root: Path) -> None:
    library = root / "kanda_prompt_workspace" / "prompt_library"
    class_root = library / "ACTIVE_PROMPTS" / CLASS_ID
    metadata_root = library / "METADATA"
    for prompt_id in RETIRED:
        require(
            not (class_root / (prompt_id + ".md")).exists()
            and not (metadata_root / (prompt_id + ".meta.json")).exists(),
            "WAVE5A_RETIRED_" + prompt_id.upper(),
        )
    substitution = read_text(
        library
        / "ACTIVE_PROMPTS"
        / "02_prompt_routing_and_indexing"
        / "prompt_substitution_map.md"
    )
    require(
        "## Wave 5A Class 05 lifecycle records" in substitution
        and all(prompt_id in substitution for prompt_id in RETIRED)
        and "deprecated_application_duplicate" in substitution,
        "WAVE5A_SUBSTITUTION_RECORDS",
    )


def validate_routing(root: Path) -> None:
    library = root / "kanda_prompt_workspace" / "prompt_library"
    nav = load_json(library / "ROUTING" / "prompt_navigation_index.json")
    entries = list(nav.get("entries", []))
    by_id = {entry.get("prompt_id"): entry for entry in entries}
    require(nav.get("prompt_count") == len(entries), "WAVE5A_NAV_COUNT")
    require(not (RETIRED & set(by_id)), "WAVE5A_RETIRED_NAV_REMOVED")
    for prompt_id, (code, _, load_type) in ACTIVE.items():
        entry = by_id.get(prompt_id)
        require(
            isinstance(entry, dict)
            and entry.get("prompt_code") == code
            and entry.get("category") == CLASS_ID
            and entry.get("status") == "active"
            and entry.get("load_type") == load_type
            and "evidence_freshness_gate" not in entry.get("required_companion_prompts", [])
            and "patch_registry_validation_freeze" not in entry.get("required_companion_prompts", []),
            "WAVE5A_NAV_" + prompt_id.upper(),
        )

    draft = load_json(library / "GROUPS" / "PROMPT_GROUPS_DRAFT.json")
    draft_group = next(
        item for item in draft.get("groups", []) if item.get("group_id") == CLASS_ID
    )
    require(
        draft_group.get("prompt_count") == len(draft_group.get("prompt_ids", []))
        and MAIN_IDS.issubset(set(draft_group.get("prompt_ids", []))),
        "WAVE5A_DRAFT_GROUP_OWNER_SET",
    )

    machine = load_json(library / "ROUTING" / "group_assimilation_index.json")
    machine_group = next(
        item for item in machine.get("groups", []) if item.get("group_id") == CLASS_ID
    )
    require(
        machine_group.get("prompt_count") == len(machine_group.get("main_prompts", []))
        and MAIN_IDS.issubset({Path(item).stem for item in machine_group.get("main_prompts", [])}),
        "WAVE5A_MACHINE_GROUP_OWNER_SET",
    )

    cards = load_json(library / "ROUTING" / "folder_assimilation_cards_index.json")
    card = next(
        item for item in cards.get("folders", []) if item.get("folder_id") == CLASS_ID
    )
    require(
        card.get("prompt_count") == len(card.get("main_prompt_ids", []))
        and MAIN_IDS.issubset(set(card.get("main_prompt_ids", []))),
        "WAVE5A_FOLDER_CARD_OWNER_SET",
    )

    with (library / "ROUTING" / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    coverage = {row.get("prompt_id"): row for row in rows}
    require(not (RETIRED & set(coverage)), "WAVE5A_RETIRED_COVERAGE_REMOVED")
    for prompt_id in ACTIVE:
        require(prompt_id in coverage, "WAVE5A_COVERAGE_" + prompt_id.upper())
    require(
        not any(
            retired in str(row.get("companions") or "")
            for row in rows
            for retired in RETIRED
        ),
        "WAVE5A_RETIRED_COMPANION_REMOVED",
    )

    human_group = read_text(library / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md")
    class_root = library / "ACTIVE_PROMPTS" / CLASS_ID
    declared_count = len(machine_group.get("main_prompts", []))
    require(
        f"| 05_patch_delivery_and_validation | {declared_count} |" in human_group,
        "WAVE5A_HUMAN_ACTIVE_COUNT",
    )
    print("WAVE5A_ROUTING_AND_DEPENDENCY_MIGRATION: PASS")


def validate_no_active_retired_references(root: Path) -> None:
    library = root / "kanda_prompt_workspace" / "prompt_library"
    roots = [
        library / "METADATA",
        library / "ROUTING",
        library / "GROUPS",
        library / "HUMAN_APPENDIX",
    ]
    allowed = {
        library
        / "ACTIVE_PROMPTS"
        / "02_prompt_routing_and_indexing"
        / "prompt_substitution_map.md",
        library / "ACTIVE_PROMPTS" / CLASS_ID / "_FOLDER_ASSIMILATION.md",
    }
    violations: list[str] = []
    for scan_root in roots:
        for path in scan_root.rglob("*"):
            if not path.is_file() or path in allowed:
                continue
            if path.suffix.lower() not in {".json", ".md", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            for retired in RETIRED:
                if retired in text:
                    violations.append(path.relative_to(root).as_posix() + ":" + retired)
    require(not violations, "WAVE5A_NO_ACTIVE_RETIRED_REFERENCES")


def validate_application_duplicate(root: Path) -> None:
    app = root / "kanda_reasoner_app" / "prompt_library"
    redirect = read_text(app / "active" / "KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md")
    meta = load_json(app / "metadata" / "kanda_bundle_gated_development_workflow.meta.json")
    groups = load_json(app / "groups" / "PROMPT_GROUPS.json")
    require(
        "Status: deprecated historical redirect" in redirect
        and "KPR-05-002 bundle_gated_development_workflow" in redirect
        and meta.get("status") == "deprecated"
        and meta.get("load_type") == "never"
        and meta.get("active_route") is False,
        "WAVE5A_APPLICATION_DUPLICATE_DEPRECATED",
    )
    require(
        not any(
            "kanda_bundle_gated_development_workflow" in group.get("prompt_ids", [])
            for group in groups.get("groups", [])
        ),
        "WAVE5A_APPLICATION_DUPLICATE_ROUTE_REMOVED",
    )
    print("WAVE5A_BUNDLE_IDENTITY_RECONCILIATION: PASS")


def validate_folder_card(root: Path) -> None:
    path = (
        root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / CLASS_ID
        / "_FOLDER_ASSIMILATION.md"
    )
    text = read_text(path)
    require(
        "KPR-05-001 patch_install_delivery_error_register" in text
        and "KPR-05-002 bundle_gated_development_workflow" in text
        and "KPR-05-003 implementation_and_delivery_protocol" in text
        and "KPR-05-004 implementation_roadmap_builder" in text
        and "KPR-05-005 patch_validate_freeze_error_memory_routine_blueprint" in text
        and (
            "Compatibility surfaces pending" in text
            or "KPR-05-006 router_bridge_user_detected_correction" in text
        )
        and "No prompt in this folder can authorize coding by itself" in text,
        "WAVE5A_FOLDER_CARD_RECONCILIATION",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    validate_active_prompts(root)
    validate_retirements(root)
    validate_routing(root)
    validate_no_active_retired_references(root)
    validate_application_duplicate(root)
    validate_folder_card(root)
    print("WAVE5A_PATCH_LIFECYCLE_CORE_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("WAVE5A_VALIDATION_ERROR: " + type(exc).__name__ + ": " + str(exc))
        raise
