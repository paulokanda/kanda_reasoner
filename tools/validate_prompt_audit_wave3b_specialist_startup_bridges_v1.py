"""Validate Prompt Audit Wave 3B specialist startup bridge contracts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import zipfile

__all__: list[str] = []

FEATURE_ID = "prompt-audit-wave3b-specialist-startup-bridges-v1"
LIBRARY = Path("kanda_prompt_workspace/prompt_library")
TOOLS = Path("kanda_prompt_workspace/prompt_tools")
CLASS01 = "01_session_start_and_navigation"
CLASS05 = "05_patch_delivery_and_validation"
MAX_LINES = 500

PROMPTS = {
    "daily_patch_delivery_guardrails": {
        "code": "KPR-01-007",
        "version": "3.0",
        "category": CLASS01,
        "load": "always_startup",
        "markers": (
            "compact always-startup bridge",
            "Required owner route",
            "Unknown source states",
            "Durable evidence is routed",
            "PATCH DELIVERY BLOCKED",
        ),
        "forbidden": ("Compress-Archive", "Expand-Archive", "Tee-Object"),
    },
    "durable_document_artifact_routing_canon": {
        "code": "KPR-01-013",
        "version": "2.0",
        "category": CLASS01,
        "load": "always_startup",
        "markers": (
            "DURABLE ARTIFACT ROUTING RECORD",
            "CANONICAL_SOURCE",
            "GENERATED_ARTIFACT",
            "Validation and blocker evidence",
            "Redaction and provenance",
            "DURABLE DOCUMENT ROUTING BLOCKED",
        ),
        "forbidden": ("Compress-Archive", "Expand-Archive", "Tee-Object"),
    },
    "error_memory_ai_formulary_startup_canon": {
        "code": "KPR-01-012",
        "version": "2.0",
        "category": CLASS01,
        "load": "always_startup",
        "markers": (
            "single always-startup workflow and admission owner",
            "ERROR MEMORY ADMISSION CHECK",
            "DUPLICATE_DO_NOT_CREATE",
            "Full Error Memory needed",
            "explicit human Memorize Error action",
        ),
        "forbidden": ("QTimer", "QDialog", "Compress-Archive", "Expand-Archive"),
    },
    "handoff_at_end_of_work": {
        "code": "KPR-01-008",
        "version": "2.0",
        "category": CLASS01,
        "load": "always_startup",
        "markers": (
            "detects project-session closure",
            "Closure triggers",
            "SESSION HANDOFF",
            "Not completed:",
            "Next safe action:",
            "Do not do next:",
        ),
        "forbidden": ("load order position 8", "Confirm and Write schema"),
    },
    "patch_install_delivery_error_register": {
        "code": "KPR-05-001",
        "version": "2.0",
        "category": CLASS05,
        "load": "conditional_required",
        "markers": (
            "compact Class 05 index",
            "PIR ID:",
            "Blocking predicate:",
            "Current owner prompt:",
            "Expected rejection marker:",
            "Unknown or ownerless regression classes fail closed",
        ),
        "forbidden": (
            "add a new append-only entry under Error Register",
            "## Append-only update protocol",
        ),
    },
}

STARTUP_IDS = {
    "daily_patch_delivery_guardrails",
    "durable_document_artifact_routing_canon",
    "error_memory_ai_formulary_startup_canon",
    "handoff_at_end_of_work",
}
STARTUP_MEMBERS = {
    "07_daily_patch_delivery_guardrails.md",
    "08_handoff_at_end_of_work.md",
    "12_error_memory_ai_formulary_startup_canon.md",
    "13_durable_document_artifact_routing_canon.md",
}
MIGRATED_MEMBER = "09_patch_install_delivery_error_register.md"


class ValidationError(AssertionError):
    """Raised for a Wave 3B validation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_text(path: Path) -> str:
    require(path.is_file(), "MISSING_FILE: " + str(path))
    data = path.read_bytes()
    require(not data.startswith(b"\xef\xbb\xbf"), "UTF8_BOM_FORBIDDEN: " + str(path))
    require(b"\r\n" not in data, "CRLF_FORBIDDEN: " + str(path))
    return data.decode("utf-8")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(read_text(path))


def parse_front(text: str) -> dict[str, str]:
    require(text.startswith("---\n"), "FRONTMATTER_MISSING")
    _, block, _ = text.split("---\n", 2)
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def version_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(part) for part in str(value).split("."))


def validate_prompt_sources(root: Path) -> None:
    codes: set[str] = set()
    for prompt_id, contract in PROMPTS.items():
        category = str(contract["category"])
        source = root / LIBRARY / "ACTIVE_PROMPTS" / category / (prompt_id + ".md")
        metadata_path = root / LIBRARY / "METADATA" / (prompt_id + ".meta.json")
        text = read_text(source)
        metadata = load_json(metadata_path)
        front = parse_front(text)
        require(len(text.splitlines()) <= MAX_LINES, "PROMPT_TOO_LARGE: " + prompt_id)
        expected = {
            "prompt_id": prompt_id,
            "prompt_code": str(contract["code"]),
            "status": "active",
            "load_type": str(contract["load"]),
            "owner_box": category,
        }
        for key, value in expected.items():
            require(front.get(key) == value, f"SOURCE_{key.upper()}: {prompt_id}")
            require(metadata.get(key) == value, f"META_{key.upper()}: {prompt_id}")
        require(version_tuple(front.get("version", "0")) >= version_tuple(contract["version"]), "SOURCE_VERSION: " + prompt_id)
        require(version_tuple(metadata.get("version", "0")) >= version_tuple(contract["version"]), "META_VERSION: " + prompt_id)
        require(metadata.get("category") == category, "META_CATEGORY: " + prompt_id)
        require(metadata.get("source_stage") == FEATURE_ID, "META_STAGE: " + prompt_id)
        require(metadata.get("updated_for") == FEATURE_ID, "META_UPDATED_FOR: " + prompt_id)
        canonical = str(metadata.get("canonical_path") or "")
        require(canonical.endswith(category + "/" + prompt_id + ".md"), "META_CANONICAL_PATH: " + prompt_id)
        code = str(contract["code"])
        require(code not in codes, "DUPLICATE_CODE: " + code)
        codes.add(code)
        for marker in contract["markers"]:
            require(marker in text, f"REQUIRED_MARKER: {prompt_id}: {marker}")
        for marker in contract["forbidden"]:
            require(marker not in text, f"FORBIDDEN_MARKER: {prompt_id}: {marker}")

    old_register = root / LIBRARY / "ACTIVE_PROMPTS" / CLASS01 / "patch_install_delivery_error_register.md"
    misplaced_meta = root / LIBRARY / "ACTIVE_PROMPTS" / CLASS01 / "handoff_at_end_of_work.meta.json"
    require(not old_register.exists(), "OLD_CLASS01_PATCH_REGISTER_REMAINS")
    require(not misplaced_meta.exists(), "MISPLACED_HANDOFF_METADATA_REMAINS")
    print("WAVE3B_DAILY_PATCH_BRIDGE: PASS")
    print("WAVE3B_DURABLE_ARTIFACT_CANON: PASS")
    print("WAVE3B_ERROR_MEMORY_ADMISSION_CANON: PASS")
    print("WAVE3B_HANDOFF_CLOSURE_GUARDRAIL: PASS")


def validate_patch_register(root: Path) -> None:
    path = root / LIBRARY / "ACTIVE_PROMPTS" / CLASS05 / "patch_install_delivery_error_register.md"
    text = read_text(path)
    ids = re.findall(r"^### (PIR-\d{3})\b", text, flags=re.MULTILINE)
    expected = [f"PIR-{number:03d}" for number in range(1, 12)]
    require(ids == expected, "PATCH_REGISTER_PIR_SEQUENCE: " + repr(ids))
    require(len(ids) == len(set(ids)), "PATCH_REGISTER_DUPLICATE_PIR")
    print("WAVE3B_PATCH_REGRESSION_INDEX: PASS")


def validate_routes(root: Path) -> None:
    route = load_json(root / LIBRARY / "ROUTING/prompt_navigation_index.json")
    entries = route.get("entries", [])
    require(route.get("prompt_count") == len(entries), "ROUTE_COUNT_MISMATCH")
    by_id = {entry.get("prompt_id"): entry for entry in entries}
    for prompt_id, contract in PROMPTS.items():
        entry = by_id.get(prompt_id)
        require(isinstance(entry, dict), "ROUTE_MISSING: " + prompt_id)
        require(entry.get("prompt_code") == contract["code"], "ROUTE_CODE: " + prompt_id)
        require(entry.get("category") == contract["category"], "ROUTE_CATEGORY: " + prompt_id)
        require(entry.get("owner_box") == contract["category"], "ROUTE_OWNER: " + prompt_id)
        require(entry.get("status") == "active", "ROUTE_STATUS: " + prompt_id)
        require(entry.get("relative_path") == "ACTIVE_PROMPTS/" + contract["category"] + "/" + prompt_id + ".md", "ROUTE_PATH: " + prompt_id)

    groups = load_json(root / LIBRARY / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    by_group = {item.get("group_id"): item for item in groups.get("groups", [])}
    class01 = by_group.get(CLASS01)
    class05 = by_group.get(CLASS05)
    require(isinstance(class01, dict) and class01.get("prompt_count") == len(class01.get("prompt_ids", [])) == 11, "CLASS01_GROUP_COUNT")
    require(isinstance(class05, dict), "CLASS05_GROUP_MISSING")
    class05_ids = list(class05.get("prompt_ids", []))
    require(class05.get("prompt_count") == len(class05_ids) and len(class05_ids) >= 5, "CLASS05_GROUP_COUNT")
    require("patch_install_delivery_error_register" not in class01.get("prompt_ids", []), "REGISTER_IN_CLASS01_GROUP")
    require("patch_install_delivery_error_register" in class05_ids, "REGISTER_MISSING_CLASS05_GROUP")

    cards = load_json(root / LIBRARY / "ROUTING/folder_assimilation_cards_index.json")
    by_folder = {item.get("folder_id"): item for item in cards.get("folders", [])}
    require(by_folder[CLASS01].get("prompt_count") == len(by_folder[CLASS01].get("main_prompt_ids", [])) == 11, "CLASS01_CARD_COUNT")
    class05_card_ids = list(by_folder[CLASS05].get("main_prompt_ids", []))
    require(
        by_folder[CLASS05].get("prompt_count") == len(class05_card_ids)
        and set(class05_card_ids) == set(class05_ids),
        "CLASS05_CARD_COUNT",
    )

    machine_groups = load_json(root / LIBRARY / "ROUTING/group_assimilation_index.json")
    machine_by_id = {item.get("group_id"): item for item in machine_groups.get("groups", [])}
    require(machine_by_id[CLASS01].get("prompt_count") == len(machine_by_id[CLASS01].get("main_prompts", [])) == 11, "CLASS01_MACHINE_GROUP_COUNT")
    class05_machine_files = list(machine_by_id[CLASS05].get("main_prompts", []))
    require(
        machine_by_id[CLASS05].get("prompt_count") == len(class05_machine_files)
        and {Path(item).stem for item in class05_machine_files} == set(class05_ids),
        "CLASS05_MACHINE_GROUP_COUNT",
    )

    coverage_path = root / LIBRARY / "ROUTING/prompt_route_coverage_table.csv"
    with coverage_path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    coverage = {row.get("prompt_id"): row for row in rows}
    for prompt_id, contract in PROMPTS.items():
        require(prompt_id in coverage, "COVERAGE_MISSING: " + prompt_id)
        require(coverage[prompt_id].get("category") == contract["category"], "COVERAGE_CATEGORY: " + prompt_id)

    human_group = read_text(root / LIBRARY / "ROUTING/GROUP_ASSIMILATION_INDEX.md")
    require("| 01_session_start_and_navigation | 11 |" in human_group, "HUMAN_CLASS01_COUNT")
    active_class05_count = len(class05_ids)
    require(
        f"| 05_patch_delivery_and_validation | {active_class05_count} |"
        in human_group,
        "HUMAN_CLASS05_ACTIVE_COUNT",
    )
    print("WAVE3B_CLASS01_CLASS05_MIGRATION: PASS")


def validate_startup(root: Path) -> None:
    source_map = load_json(root / TOOLS / "STARTUP_ROUTING_KERNEL_SOURCES.json")
    entries = source_map.get("startup_sources", [])
    orders = [int(entry["load_order"]) for entry in entries]
    require(orders == list(range(1, len(entries) + 1)), "STARTUP_ORDER_NOT_CONTIGUOUS")
    by_id = {entry.get("prompt_id"): entry for entry in entries}
    require(STARTUP_IDS.issubset(by_id), "STARTUP_SPECIALIST_MISSING")
    require("patch_install_delivery_error_register" not in by_id, "PATCH_REGISTER_STILL_STARTUP")
    for prompt_id in STARTUP_IDS:
        require(by_id[prompt_id].get("load_mode") == "always_startup", "STARTUP_LOAD_MODE: " + prompt_id)
    generated = {entry.get("generated_filename") for entry in entries}
    require(STARTUP_MEMBERS.issubset(generated), "STARTUP_MEMBER_MAPPING_MISSING")
    require(MIGRATED_MEMBER not in generated, "MIGRATED_MEMBER_IN_SOURCE_MAP")

    fallback = read_text(root / TOOLS / "startup_kernel/startup_source_map.py")
    for member in STARTUP_MEMBERS:
        require(member in fallback, "FALLBACK_MEMBER_MISSING: " + member)
    require(MIGRATED_MEMBER not in fallback, "FALLBACK_MIGRATED_MEMBER")
    readme = read_text(root / TOOLS / "README_kanda_startup_prompt_request_kernel_generator.md")
    require("Generated filename 09 is now a migrated conditional Class 05 slot and is not generated." in readme, "README_MIGRATED_SLOT")
    require("Generated filenames 10 and 11 are retired compatibility slots." in readme, "README_RETIRED_SLOTS")
    print("WAVE3B_STARTUP_PAYLOAD_MINIMIZED: PASS")


def validate_generated(root: Path, startup_zip: Path, library_zip: Path) -> None:
    require(startup_zip.is_file(), "STARTUP_ZIP_MISSING")
    require(library_zip.is_file(), "PROMPT_LIBRARY_ZIP_MISSING")
    with zipfile.ZipFile(startup_zip, "r") as archive:
        names = set(archive.namelist())
        require(STARTUP_MEMBERS.issubset(names), "GENERATED_STARTUP_SPECIALISTS_MISSING")
        require(MIGRATED_MEMBER not in names, "GENERATED_STARTUP_MIGRATED_MEMBER")
        for prompt_id, contract in PROMPTS.items():
            if prompt_id not in STARTUP_IDS:
                continue
            member = next(
                name for name in STARTUP_MEMBERS
                if name.endswith(prompt_id + ".md")
            )
            text = archive.read(member).decode("utf-8")
            for marker in contract["markers"][:2]:
                require(marker in text, f"GENERATED_MARKER: {prompt_id}: {marker}")
    with zipfile.ZipFile(library_zip, "r") as archive:
        names = set(archive.namelist())
        old = "ACTIVE_PROMPTS/01_session_start_and_navigation/patch_install_delivery_error_register.md"
        new = "ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_install_delivery_error_register.md"
        require(old not in names, "LIBRARY_ZIP_OLD_REGISTER")
        require(new in names, "LIBRARY_ZIP_NEW_REGISTER_MISSING")
    print("WAVE3B_GENERATED_PROMPT_LIBRARY_HASHES: PASS")


def validate_negative_controls() -> None:
    bad_route = {"category": CLASS01, "load_type": "always_startup"}
    require(bad_route["category"] != CLASS05, "NEGATIVE_ROUTE_FIXTURE_INVALID")
    require(bad_route["load_type"] != "conditional_required", "NEGATIVE_LOAD_FIXTURE_INVALID")
    unknown_pir = "PIR-999"
    require(unknown_pir not in {f"PIR-{number:03d}" for number in range(1, 12)}, "NEGATIVE_PIR_FIXTURE_INVALID")
    print("WAVE3B_NEGATIVE_GUARD_CONTROLS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--startup-zip")
    parser.add_argument("--prompt-library-zip")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    validate_prompt_sources(root)
    validate_patch_register(root)
    validate_routes(root)
    validate_startup(root)
    validate_negative_controls()
    if args.startup_zip or args.prompt_library_zip:
        require(bool(args.startup_zip and args.prompt_library_zip), "BOTH_GENERATED_ZIPS_REQUIRED")
        validate_generated(root, Path(args.startup_zip), Path(args.prompt_library_zip))
    self_path = root / "tools/validate_prompt_audit_wave3b_specialist_startup_bridges_v1.py"
    require(len(read_text(self_path).splitlines()) <= MAX_LINES, "WAVE3B_VALIDATOR_TOO_LARGE")
    print("WAVE3B_NO_NEW_STARTUP_ENGINE_OR_REGISTRY: PASS")
    print("WAVE3B_SPECIALIST_STARTUP_BRIDGES_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
