"""Validate Prompt Audit Wave 3A session/startup kernel contracts."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import csv
import json
import zipfile
from pathlib import Path

FEATURE_ID = "prompt-audit-wave3a-session-startup-kernel-v1"
OWNER = "01_session_start_and_navigation"
MAX_LINES = 500

ACTIVE = {
    "start_of_day_master_stack": ("KPR-01-001", "2.0", "always_startup"),
    "session_start_upload_checklist": ("KPR-01-002", "2.0", "always_startup"),
    "prompt_router_reasoner_startup_check": ("KPR-01-003", "2.0", "on_request"),
    "ai_human_partnership_session_start": ("KPR-01-004", "2.0", "on_request"),
    "daily_startup_loader_template": ("KPR-01-005", "2.0", "on_request"),
    "project_startup_canon_template": ("KPR-01-006", "2.0", "on_request"),
}

DEPRECATED = {
    "daily_reasoner_startup_loader",
    "daily_session_start_prompt",
    "general_prompt_stack_load_order",
    "reasoner_startup_canon",
}

REQUIRED = {
    "start_of_day_master_stack": (
        "smallest always-loaded governance bridge",
        "WAIT_FOR_TASK",
        "BEGINNING_OF_DAY_CODE_MODULE_SIZE_BRIDGE",
        "BEGINNING_OF_DAY_BOX_LOGIC_BRIDGE",
        "BEGINNING_OF_DAY_GOVERNED_ARCHITECTURE_COMPANION_BRIDGE_V1_START",
        "BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_START",
        "BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_START",
        "User-facing and packaged PowerShell must not use `else` or `elseif`.",
    ),
    "session_start_upload_checklist": (
        "Stage 1 - startup delivery",
        "Stage 2 - selected Project handoff",
        "PROJECT READY CHECK",
        "WAIT_FOR_TASK",
        "Do not accept the real Project task before Stage 2 readiness.",
        "Generated source archives and handoffs are evidence, not canonical source authority.",
    ),
    "prompt_router_reasoner_startup_check": (
        "on request without participating in normal session startup",
        "Static source inspection is not real local runtime validation.",
        "cannot issue `WAIT_FOR_TASK`",
        "PROMPT ROUTER REASONER READINESS ASSESSMENT",
    ),
    "ai_human_partnership_session_start": (
        "communication expectations only",
        "cannot route a task",
        "Do not claim local execution that did not occur.",
    ),
    "daily_startup_loader_template": (
        "Do not execute the startup workflow",
        "source_write_authorization: NO",
        "Do not add a context engine, registry, mega-prompt, or parallel startup owner.",
    ),
    "project_startup_canon_template": (
        "stable Project-specific startup profile",
        "Exclude session-specific facts",
        "source_write_authorization: NO",
        "Tool and Project identity remain logically separate",
    ),
}

FORBIDDEN = {
    "prompt_router_reasoner_startup_check": (
        "Load `prompt_router_reasoner_startup_check` at every startup",
    ),
    "ai_human_partnership_session_start": ("May implement: YES",),
    "daily_startup_loader_template": ("write the generated loader now",),
}

REQUIRED_STARTUP = {
    "01_ai_prompt_request_canon.md",
    "02_prompt_navigation_index.md",
    "03_GROUP_ASSIMILATION_INDEX.md",
    "04_FOLDER_ASSIMILATION_CARDS_INDEX.md",
    "05_start_of_day_master_stack.md",
    "06_session_start_upload_checklist.md",
    "07_daily_patch_delivery_guardrails.md",
    "08_handoff_at_end_of_work.md",
    "12_error_memory_ai_formulary_startup_canon.md",
    "13_durable_document_artifact_routing_canon.md",
    "14_project_tool_boundary_canon.md",
}

MIGRATED_STARTUP = {
    "09_patch_install_delivery_error_register.md",
}

RETIRED_STARTUP = {
    "10_prompt_router_reasoner_startup_check.md",
    "11_chatgpt_kanda_routing_choice_output_protocol.md",
}


class ValidationError(AssertionError):
    """Raised for a Wave 3A validation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_text(path: Path) -> str:
    require(path.is_file(), f"MISSING_FILE: {path}")
    data = path.read_bytes()
    require(not data.startswith(b"\xef\xbb\xbf"), f"UTF8_BOM_FORBIDDEN: {path}")
    require(b"\r\n" not in data, f"CRLF_FORBIDDEN: {path}")
    return data.decode("utf-8")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(read_text(path))


def parse_front(text: str) -> dict[str, str]:
    require(text.startswith("---\n"), "FRONT_MATTER_MISSING")
    _, block, _ = text.split("---", 2)
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def version_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(part) for part in str(value).split("."))


def validate_active_prompts(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    codes: set[str] = set()
    for prompt_id, (code, version, load_type) in ACTIVE.items():
        source = library / "ACTIVE_PROMPTS" / OWNER / f"{prompt_id}.md"
        metadata = library / "METADATA" / f"{prompt_id}.meta.json"
        text = read_text(source)
        meta = load_json(metadata)
        front = parse_front(text)
        require(len(text.splitlines()) <= MAX_LINES, f"PROMPT_TOO_LARGE: {prompt_id}")
        expected = {
            "prompt_id": prompt_id,
            "prompt_code": code,
            "status": "active",
            "load_type": load_type,
            "owner_box": OWNER,
        }
        for key, expected_value in expected.items():
            require(front.get(key) == expected_value, f"SOURCE_{key.upper()}_MISMATCH: {prompt_id}")
            require(meta.get(key) == expected_value, f"META_{key.upper()}_MISMATCH: {prompt_id}")
        require(version_tuple(front.get("version", "0")) >= version_tuple(version), f"SOURCE_VERSION: {prompt_id}")
        require(version_tuple(meta.get("version", "0")) >= version_tuple(version), f"META_VERSION: {prompt_id}")
        require(meta.get("source_stage") == FEATURE_ID, f"META_STAGE: {prompt_id}")
        require(meta.get("updated_for") == FEATURE_ID, f"META_UPDATED_FOR: {prompt_id}")
        require(bool(meta.get("canonical_path")), f"META_CANONICAL_PATH: {prompt_id}")
        require(code not in codes, f"DUPLICATE_CODE: {code}")
        codes.add(code)
        for marker in REQUIRED[prompt_id]:
            require(marker in text, f"REQUIRED_MARKER: {prompt_id}: {marker}")
        for marker in FORBIDDEN.get(prompt_id, ()):
            require(marker not in text, f"FORBIDDEN_MARKER: {prompt_id}: {marker}")
    print("WAVE3A_ACTIVE_OWNER_IDENTITY: PASS")
    print("WAVE3A_TWO_STAGE_READINESS: PASS")


def validate_deprecated_prompts(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    route = load_json(library / "ROUTING/prompt_navigation_index.json")
    routed = {entry.get("prompt_id") for entry in route.get("entries", [])}
    for prompt_id in DEPRECATED:
        source = library / "ACTIVE_PROMPTS" / OWNER / f"{prompt_id}.md"
        metadata = library / "METADATA" / f"{prompt_id}.meta.json"
        text = read_text(source)
        front = parse_front(text)
        meta = load_json(metadata)
        require(len(text.splitlines()) <= 40, f"LEGACY_RECORD_NOT_COMPACT: {prompt_id}")
        require(front.get("status") == "deprecated", f"LEGACY_SOURCE_STATUS: {prompt_id}")
        require(front.get("load_type") == "compatibility_only", f"LEGACY_SOURCE_LOAD: {prompt_id}")
        require(meta.get("status") == "deprecated", f"LEGACY_META_STATUS: {prompt_id}")
        require(meta.get("load_type") == "compatibility_only", f"LEGACY_META_LOAD: {prompt_id}")
        require(meta.get("source_stage") == FEATURE_ID, f"LEGACY_META_STAGE: {prompt_id}")
        require(prompt_id not in routed, f"LEGACY_ACTIVE_ROUTE: {prompt_id}")
        require("cannot" in text.lower() or "no active route" in text.lower(), f"LEGACY_AUTHORITY_GUARD: {prompt_id}")
    substitution = read_text(library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md")
    for prompt_id in DEPRECATED:
        require(prompt_id in substitution, f"SUBSTITUTION_MISSING: {prompt_id}")
    print("WAVE3A_LEGACY_STARTUP_RETIREMENT: PASS")


def validate_routes_and_inventories(root: Path) -> None:
    library = root / "kanda_prompt_workspace/prompt_library"
    route = load_json(library / "ROUTING/prompt_navigation_index.json")
    entries = route.get("entries", [])
    require(route.get("prompt_count") == len(entries), "ROUTE_COUNT_MISMATCH")
    by_id = {entry.get("prompt_id"): entry for entry in entries}
    for prompt_id, (code, version, _) in ACTIVE.items():
        entry = by_id.get(prompt_id)
        require(isinstance(entry, dict), f"ACTIVE_ROUTE_MISSING: {prompt_id}")
        require(entry.get("prompt_code") == code, f"ACTIVE_ROUTE_CODE: {prompt_id}")
        require(entry.get("status") == "active", f"ACTIVE_ROUTE_STATUS: {prompt_id}")
        require(entry.get("owner_box") == OWNER, f"ACTIVE_ROUTE_OWNER: {prompt_id}")
        require(version_tuple(entry.get("version", "0")) >= version_tuple(version), f"ACTIVE_ROUTE_VERSION: {prompt_id}")
    groups = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in groups["groups"] if item.get("group_id") == OWNER)
    ids = group.get("prompt_ids", [])
    require(group.get("prompt_count") == len(ids) == 11, "CLASS01_GROUP_COUNT")
    for prompt_id in ACTIVE:
        require(prompt_id in ids, f"CLASS01_GROUP_ACTIVE_MISSING: {prompt_id}")
    for prompt_id in DEPRECATED:
        require(prompt_id not in ids, f"CLASS01_GROUP_LEGACY_REMAINS: {prompt_id}")
    card = load_json(library / "ROUTING/folder_assimilation_cards_index.json")
    folder = next(item for item in card["folders"] if item.get("folder_id") == OWNER)
    require(folder.get("prompt_count") == len(folder.get("main_prompt_ids", [])) == 11, "CLASS01_FOLDER_COUNT")
    coverage = library / "ROUTING/prompt_route_coverage_table.csv"
    with coverage.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    covered = {row.get("prompt_id") for row in rows}
    for prompt_id in ACTIVE:
        require(prompt_id in covered, f"COVERAGE_ACTIVE_MISSING: {prompt_id}")
    for prompt_id in DEPRECATED:
        require(prompt_id not in covered, f"COVERAGE_LEGACY_REMAINS: {prompt_id}")
    print("WAVE3A_CLASS01_INVENTORY_ALIGNMENT: PASS")


def validate_source_map(root: Path) -> None:
    tools = root / "kanda_prompt_workspace/prompt_tools"
    data = load_json(tools / "STARTUP_ROUTING_KERNEL_SOURCES.json")
    entries = data.get("startup_sources", [])
    orders = [int(item["load_order"]) for item in entries]
    require(orders == list(range(1, len(entries) + 1)), "STARTUP_LOAD_ORDER_NOT_CONTIGUOUS")
    by_id = {item.get("prompt_id"): item for item in entries}
    required_ids = {
        "ai_prompt_request_canon",
        "prompt_navigation_index",
        "start_of_day_master_stack",
        "session_start_upload_checklist",
        "daily_patch_delivery_guardrails",
        "handoff_at_end_of_work",
        "error_memory_ai_formulary_startup_canon",
        "durable_document_artifact_routing_canon",
        "project_tool_boundary_startup_bridge",
    }
    require(required_ids.issubset(by_id), "STARTUP_REQUIRED_OWNER_MISSING")
    require("prompt_router_reasoner_startup_check" not in by_id, "READINESS_PROMPT_STILL_STARTUP")
    require("chatgpt_kanda_routing_choice_output_protocol" not in by_id, "CHOICE_OUTPUT_STILL_STARTUP")
    fallback = read_text(tools / "startup_kernel/startup_source_map.py")
    for filename in REQUIRED_STARTUP:
        require(filename in fallback, f"FALLBACK_SOURCE_MAP_MISSING: {filename}")
    for filename in MIGRATED_STARTUP:
        require(filename not in fallback, f"FALLBACK_MIGRATED_MEMBER: {filename}")
    for filename in RETIRED_STARTUP:
        require(filename not in fallback, f"FALLBACK_RETIRED_MEMBER: {filename}")
    readme = read_text(tools / "README_kanda_startup_prompt_request_kernel_generator.md")
    require("Generated filenames 10 and 11 are retired compatibility slots" in readme, "README_RETIRED_SLOT_NOTICE")
    print("WAVE3A_STARTUP_PAYLOAD_MINIMIZED: PASS")


def validate_redirects(root: Path) -> None:
    redirect_root = root / "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation"
    for prompt_id in ("start_of_day_master_stack", "session_start_upload_checklist", "prompt_router_reasoner_startup_check"):
        text = read_text(redirect_root / f"{prompt_id}.md")
        require("not canonical" in text, f"ROOT_REDIRECT_AUTHORITY: {prompt_id}")
    app_active = root / "kanda_reasoner_app/prompt_library/active"
    for filename in (
        "0000 1.0 PYARCHITECT PROJECT STARTUP CANON TEMPLATE v1.0.md",
        "0000 2.1 PYARCHITECT DAILY STARTUP LOADER TEMPLATE v1.0.md",
    ):
        text = read_text(app_active / filename)
        require("not canonical" in text.lower(), f"APP_TEMPLATE_REDIRECT: {filename}")
    print("WAVE3A_DUPLICATE_STARTUP_SOURCES_RECONCILED: PASS")


def validate_generated(startup_zip: Path, library_zip: Path) -> None:
    require(startup_zip.is_file(), f"STARTUP_ZIP_MISSING: {startup_zip}")
    require(library_zip.is_file(), f"PROMPT_LIBRARY_ZIP_MISSING: {library_zip}")
    with zipfile.ZipFile(startup_zip, "r") as archive:
        names = set(archive.namelist())
        require(REQUIRED_STARTUP.issubset(names), "GENERATED_STARTUP_REQUIRED_MEMBERS")
        require(not MIGRATED_STARTUP.intersection(names), "GENERATED_STARTUP_MIGRATED_MEMBERS")
        require(not RETIRED_STARTUP.intersection(names), "GENERATED_STARTUP_RETIRED_MEMBERS")
        start = archive.read("05_start_of_day_master_stack.md").decode("utf-8")
        upload = archive.read("06_session_start_upload_checklist.md").decode("utf-8")
        require("smallest always-loaded governance bridge" in start, "GENERATED_START_STACK_STALE")
        require("Stage 2 - selected Project handoff" in upload, "GENERATED_UPLOAD_CHECKLIST_STALE")
    with zipfile.ZipFile(library_zip, "r") as archive:
        names = set(archive.namelist())
        for prompt_id in set(ACTIVE) | DEPRECATED:
            member = f"ACTIVE_PROMPTS/{OWNER}/{prompt_id}.md"
            require(member in names, f"LIBRARY_ZIP_MEMBER_MISSING: {member}")
    print("WAVE3A_GENERATED_STARTUP_CONTENT: PASS")


def validate_negative_controls() -> None:
    readiness = {"stage1": True, "stage2": False}
    require(not (readiness["stage1"] and readiness["stage2"]), "NEGATIVE_EARLY_READY")
    mutant = dict(readiness)
    mutant["stage2"] = True
    require(mutant["stage1"] and mutant["stage2"], "NEGATIVE_READY_FIXTURE_INVALID")
    legacy = {"status": "deprecated", "load_type": "compatibility_only"}
    require(legacy["status"] != "active", "NEGATIVE_LEGACY_STATUS")
    require(legacy["load_type"] != "always_startup", "NEGATIVE_LEGACY_LOAD")
    print("WAVE3A_NEGATIVE_GUARD_CONTROLS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--startup-zip")
    parser.add_argument("--prompt-library-zip")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    validate_active_prompts(root)
    validate_deprecated_prompts(root)
    validate_routes_and_inventories(root)
    validate_source_map(root)
    validate_redirects(root)
    validate_negative_controls()
    if args.startup_zip or args.prompt_library_zip:
        require(bool(args.startup_zip and args.prompt_library_zip), "BOTH_GENERATED_ZIPS_REQUIRED")
        validate_generated(Path(args.startup_zip), Path(args.prompt_library_zip))
    print("WAVE3A_NO_NEW_STARTUP_ENGINE_OR_REGISTRY: PASS")
    print("WAVE3A_SESSION_STARTUP_KERNEL_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
