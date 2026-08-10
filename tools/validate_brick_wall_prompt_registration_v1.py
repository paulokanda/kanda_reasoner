"""Validate Brick Wall prompt registration and routing contracts.

This validator is read-only and compatible with Python 3.10+.
"""

from __future__ import annotations

__all__: list[str] = []

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

FEATURE_ID = "brick-wall-comprehensive-quality-gate-prompt-registration-v1r5"
PROMPT_ID = "brick_wall_comprehensive_quality_gate"
PROMPT_CODE = "KPR-03-001"

DIAGNOSTIC_PREDECESSOR_SHA256 = (
    "8e6c313564ffb9ef007efbc9741dc4278b645d75a70cf7e3c25ef6389a2df2f3"
)
PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
PLIB = Path("kanda_prompt_workspace/prompt_library")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def gate(name: str, passed: bool, detail: str = "") -> None:
    if not passed:
        raise AssertionError(f"{name}: FAIL {detail}".rstrip())
    suffix = f" - {detail}" if detail else ""
    print(f"{name}: PASS{suffix}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_prompt(project_root: Path) -> None:
    prompt_path = project_root / PROMPT_REL
    meta_path = project_root / META_REL
    gate("BRICK_WALL_PROMPT_FILE", prompt_path.is_file(), str(prompt_path))
    gate("BRICK_WALL_METADATA_FILE", meta_path.is_file(), str(meta_path))

    prompt = read_text(prompt_path)
    meta = json.loads(read_text(meta_path))
    gate("BRICK_WALL_PROMPT_CODE", f"prompt_code: {PROMPT_CODE}" in prompt)
    gate("BRICK_WALL_PROMPT_ID", f"prompt_id: {PROMPT_ID}" in prompt)
    gate("BRICK_WALL_PROMPT_ROUTED", "load_type: routed" in prompt)
    gate("BRICK_WALL_METADATA_IDENTITY", meta.get("prompt_code") == PROMPT_CODE and meta.get("prompt_id") == PROMPT_ID)
    gate("BRICK_WALL_METADATA_PATH", meta.get("canonical_path") == PROMPT_REL.as_posix())
    gate("BRICK_WALL_METADATA_ROUTED", meta.get("load_type") == "routed")
    gate("BRICK_WALL_DIRECT_TRIGGER", "brick wall" in [str(item).lower() for item in meta.get("trigger_phrases", [])])

    missing = [f"Q{number:02d}" for number in range(1, 41) if f"Q{number:02d}" not in prompt]
    gate("BRICK_WALL_Q01_Q40", not missing, ",".join(missing) if missing else "all present")
    required_sections = [
        "BRICK WALL STATUS",
        "CURRENT BLOCKERS",
        "Q01-Q40 LIVE COVERAGE LEDGER",
        "NEXT SAFE ACTION",
        "AUTHORIZATION STATUS",
    ]
    gate("BRICK_WALL_RESPONSE_SHAPE", all(item in prompt for item in required_sections))
    gate("BRICK_WALL_FRESHNESS_RESET", "reset evidence-sensitive ticks" in prompt.lower())
    gate("BRICK_WALL_HUMAN_FREEZE_GUARD", "Confirm and Write" in prompt and "user-local validation" in prompt)
    gate("BRICK_WALL_COORDINATOR_NOT_OWNER", "does not replace the owner" in prompt.lower())
    sequence = "RECONCILE -> REPAIR -> VALIDATE -> SHIELD -> FREEZE -> EXTRACT -> ADOPT"
    gate("BRICK_WALL_Q37_PROVEN_EXTRACTION_SEQUENCE", sequence in prompt)
    gate(
        "BRICK_WALL_Q37_METADATA_SEQUENCE_GUARD",
        any(sequence in str(rule) for rule in meta.get("do_not_regress", [])),
    )


def validate_routing(project_root: Path) -> None:
    plib = project_root / PLIB
    files = {
        "active_navigation": plib / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "folder_card": plib / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md",
        "human_navigation": plib / "ROUTING/PROMPT_NAVIGATION_INDEX.md",
        "group_human": plib / "ROUTING/GROUP_ASSIMILATION_INDEX.md",
        "navigation_json": plib / "ROUTING/prompt_navigation_index.json",
        "group_json": plib / "ROUTING/group_assimilation_index.json",
        "coverage_csv": plib / "ROUTING/prompt_route_coverage_table.csv",
        "registry": plib / "ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_identity_code_registry_canon.md",
    }
    for name, path in files.items():
        gate(f"BRICK_WALL_{name.upper()}_FILE", path.is_file(), str(path))

    active_navigation = read_text(files["active_navigation"])
    folder_card = read_text(files["folder_card"])
    human_navigation = read_text(files["human_navigation"])
    group_human = read_text(files["group_human"])
    navigation_json = json.loads(read_text(files["navigation_json"]))
    group_json = json.loads(read_text(files["group_json"]))
    registry = read_text(files["registry"])

    gate("BRICK_WALL_STARTUP_ROUTE_BRIDGE", "BRICK_WALL_COMPREHENSIVE_QUALITY_GATE_V1_START" in active_navigation and PROMPT_CODE in active_navigation)
    gate("BRICK_WALL_FOLDER_REGISTRATION", PROMPT_ID in folder_card)
    gate("BRICK_WALL_HUMAN_ROUTING", PROMPT_ID in human_navigation and PROMPT_ID in group_human)

    entries = [entry for entry in navigation_json.get("entries", []) if entry.get("prompt_id") == PROMPT_ID]
    gate("BRICK_WALL_MACHINE_ROUTING", len(entries) == 1)
    gate("BRICK_WALL_MACHINE_CODE", entries[0].get("prompt_code") == PROMPT_CODE)
    gate("BRICK_WALL_PROMPT_COUNT", navigation_json.get("prompt_count") == len(navigation_json.get("entries", [])))

    tasks = [item for item in group_json.get("task_routes", []) if item.get("task_intent") == "BRICK_WALL_STATUS_CHECK"]
    gate("BRICK_WALL_GROUP_MACHINE_ROUTE", len(tasks) == 1)

    with files["coverage_csv"].open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    coverage = [row for row in rows if row.get("prompt_id") == PROMPT_ID]
    gate("BRICK_WALL_ROUTE_COVERAGE_TABLE", len(coverage) == 1)
    gate("BRICK_WALL_NEGATIVE_TRIGGER_BOUNDARY", "medical" not in " ".join(entries[0].get("trigger_phrases", [])).lower())
    gate("BRICK_WALL_CODE_REGISTRY", registry.count(f"{PROMPT_CODE} =") == 1)


def validate_no_startup_generator_change(project_root: Path) -> None:
    source_map = project_root / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    generator = project_root / "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
    gate("BRICK_WALL_STARTUP_SOURCE_MAP_PRESENT", source_map.is_file())
    gate("BRICK_WALL_STARTUP_GENERATOR_PRESENT", generator.is_file())
    data = json.loads(read_text(source_map))
    sources = data.get("startup_sources", [])
    bridge_sources = [item for item in sources if item.get("prompt_id") == "prompt_navigation_index"]
    gate("BRICK_WALL_STARTUP_BRIDGE_SOURCE_ALREADY_CANONICAL", len(bridge_sources) == 1)
    gate("BRICK_WALL_NOT_ALWAYS_STARTUP", all(item.get("prompt_id") != PROMPT_ID for item in sources))


def validate_patch_zip(project_root: Path, patch_zip: Path) -> None:
    if not patch_zip:
        return
    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)
    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip

    report = validate_patch_zip(patch_zip, expect_freeze_hint=True)
    gate("BRICK_WALL_EXACT_ZIP_CONTRACT", report.get("ok") is True)
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = archive.namelist()
        unsafe = []
        normalized = set()
        for name in names:
            clean = name.replace("\\", "/")
            parts = clean.split("/")
            if clean.startswith("/") or re.match(r"^[A-Za-z]:", clean) or ".." in parts:
                unsafe.append(name)
            folded = clean.casefold()
            if folded in normalized:
                unsafe.append(name)
            normalized.add(folded)
        gate("BRICK_WALL_ZIP_MEMBER_SAFETY", not unsafe, ",".join(unsafe))
        gate("BRICK_WALL_FREEZE_HINT_ROOT_ONLY", "KANDA_FREEZE_HINT.json" in names and not any(name.endswith("/KANDA_FREEZE_HINT.json") for name in names))
        install_manifest = json.loads(
            archive.read("INSTALL_MANIFEST.json").decode("utf-8")
        )
        accepted = (
            install_manifest.get("accepted_predecessor_sha256", {})
            .get("tools/validate_brick_wall_prompt_registration_v1.py", [])
        )
        gate(
            "BRICK_WALL_EXACT_DIAGNOSTIC_PREDECESSOR_HASH",
            DIAGNOSTIC_PREDECESSOR_SHA256 in accepted,
        )
        diagnostic = install_manifest.get("diagnostic_predecessor_evidence", {})
        gate(
            "BRICK_WALL_DIAGNOSTIC_PREDECESSOR_PROVENANCE",
            diagnostic.get("sha256") == DIAGNOSTIC_PREDECESSOR_SHA256
            and diagnostic.get("acceptance_mode") == "exact_sha256_only",
        )
        installer = archive.read("INSTALL.ps1").decode("utf-8")
        semantic_markers = [
            "function Test-BrickWallValidatorIdentity",
            "EXACT PREDECESSOR ACCEPTED",
            "SEMANTIC PREDECESSOR ACCEPTED",
            "PROMPT_CODE = \"KPR-03-001\"",
            "BRICK_WALL_GROUP_MACHINE_ROUTE",
        ]
        gate(
            "BRICK_WALL_VALIDATOR_SEMANTIC_RECOVERY_CONTRACT",
            all(marker in installer for marker in semantic_markers),
        )
        freeze_script = archive.read("FREEZE.ps1").decode("utf-8")
        freeze_markers = [
            "scan_and_save_latest_freeze_hint",
            "merge_validation_evidence_into_latest_hint",
            "load_latest_freeze_hint_record",
            "BRICK_WALL_CANONICAL_FREEZE_HINT_MERGE_CONTRACT: PASS",
        ]
        gate(
            "BRICK_WALL_CANONICAL_FREEZE_HINT_MERGE_CONTRACT",
            all(marker in freeze_script for marker in freeze_markers),
        )
        gate(
            "BRICK_WALL_FREEZE_HINT_DIRECT_JSON_WRITE_BLOCKED",
            'payload["validation_evidence_summary"] = evidence' not in freeze_script
            and 'output_hint.write_text' not in freeze_script,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip")
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve() if args.patch_zip else None

    try:
        validate_prompt(project_root)
        validate_routing(project_root)
        validate_no_startup_generator_change(project_root)
        if patch_zip:
            validate_patch_zip(project_root, patch_zip)
    except Exception as exc:
        print(f"BRICK WALL VALIDATION ERROR: {type(exc).__name__}: {exc}")
        return 1

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
