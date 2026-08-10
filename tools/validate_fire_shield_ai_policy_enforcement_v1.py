# project-path: tools/validate_fire_shield_ai_policy_enforcement_v1.py
"""Validate prompt/workflow policy binding to the frozen Fire Shield authority."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

FEATURE_ID = "kanda-reasoner-fire-shield-ai-policy-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
FULL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
BRIDGE = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md"
ADMISSION = PLIB / "ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md"
NAV = PLIB / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
ROUTINE = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md"
ROUTE_JSON = PLIB / "ROUTING/prompt_navigation_index.json"
FIRE_SHIELD = Path("kanda_reasoner_app/project_fire_shield.py")

META = {
    "project_tool_boundary_canon": PLIB / "METADATA/project_tool_boundary_canon.meta.json",
    "project_tool_boundary_startup_bridge": PLIB / "METADATA/project_tool_boundary_startup_bridge.meta.json",
    "ai_prompt_request_canon": PLIB / "METADATA/ai_prompt_request_canon.meta.json",
    "prompt_navigation_index": PLIB / "METADATA/prompt_navigation_index.meta.json",
    "patch_validate_freeze_error_memory_routine_blueprint": PLIB / "METADATA/patch_validate_freeze_error_memory_routine_blueprint.meta.json",
}

EXPECTED_VERSIONS = {
    "project_tool_boundary_canon": "2.3",
    "project_tool_boundary_startup_bridge": "2.4",
    "ai_prompt_request_canon": "3.2",
    "prompt_navigation_index": "5.1",
    "patch_validate_freeze_error_memory_routine_blueprint": "3.3",
}


def read(root: Path, relative: Path) -> str:
    path = root / relative
    if not path.is_file():
        raise AssertionError("missing file: " + str(relative))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def load_json(root: Path, relative: Path) -> dict[str, object]:
    data = json.loads(read(root, relative))
    if not isinstance(data, dict):
        raise AssertionError("JSON root must be object: " + str(relative))
    return data


def gate(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def require(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        gate(label + " " + marker, marker in text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()

    full = read(root, FULL)
    bridge = read(root, BRIDGE)
    admission = read(root, ADMISSION)
    nav = read(root, NAV)
    routine = read(root, ROUTINE)
    fire_shield = read(root, FIRE_SHIELD)

    require(
        full,
        (
            "## Fire Shield programmatic authority",
            "kanda-reasoner-fire-shield-cross-project-immutability-v1",
            "Prompt compliance coordinates intent; it is not a security boundary",
            "kanda_reasoner_app.project_fire_shield",
            "Never reach into `_project_fire_shield_*`",
            "Do not fall back to direct filesystem writes",
            "Path-string equality alone is never sufficient",
            "Fire Shield is an application-level guard, not an operating-system sandbox",
        ),
        "FULL_CANON_MARKER",
    )
    require(
        bridge,
        (
            "## Fire Shield startup gate",
            "alone is never authorization",
            "kanda_reasoner_app.project_fire_shield",
            "never `_project_fire_shield_*`",
            "BLOCKED Fire Shield means STOP",
            "Path equality alone never grants self-hosting",
        ),
        "STARTUP_BRIDGE_MARKER",
    )
    require(
        admission,
        (
            "External selected-Project consequential mutation",
            "Tool-owned public Fire Shield authority",
            "classify the next consequential action as `HARD STOP`",
            "bypass Fire Shield",
        ),
        "REQUEST_ADMISSION_MARKER",
    )
    require(
        nav,
        (
            "cross-project access, or Fire Shield policy",
            "Tool-owned public Fire Shield authority",
            "prompt-only compliance is not a fallback",
        ),
        "NAVIGATION_MARKER",
    )
    require(
        routine,
        (
            "preflight, install, restore, move, rename, delete",
            "Tool-owned public Fire Shield authority",
            "private `_project_fire_shield_*` reach-in",
            "resolve Tool/Project identity and Fire Shield applicability",
        ),
        "ROUTINE_MARKER",
    )

    require(
        fire_shield,
        (
            "FIRE_SHIELD_FEATURE_ID",
            "build_current_fire_shield_context",
            "assert_fire_shield_context_current",
            "assert_fire_shield_write_allowed",
            "assert_fire_shield_payload_bytes_allowed",
            "assert_fire_shield_source_transfer_allowed",
            "preflight_fire_shield_archive",
        ),
        "PUBLIC_FIRE_SHIELD_SURFACE",
    )
    gate("PUBLIC_FIRE_SHIELD_PRIVATE_MODULE_NOT_PROMPT_OWNER", "_project_fire_shield_*`" in full and "_project_fire_shield_*`" in bridge)
    gate("FULL_CANON_WITHIN_500_LINES", len(full.splitlines()) <= 500)
    gate("STARTUP_BRIDGE_WITHIN_200_LINES", len(bridge.splitlines()) <= 200)
    combined = "\n".join((full, bridge, admission, nav, routine))
    gate("PROMPT_POLICY_NO_FIXED_E_DRIVE", "E:\\" not in combined)
    gate("PROMPT_POLICY_NO_OS_SANDBOX_OVERCLAIM", "not an operating-system sandbox" in full and "not an OS sandbox" in bridge)

    for prompt_id, relative in META.items():
        meta = load_json(root, relative)
        gate("META_ID " + prompt_id, meta.get("prompt_id") == prompt_id)
        gate("META_VERSION " + prompt_id, str(meta.get("version")) == EXPECTED_VERSIONS[prompt_id])
        gate("META_STAGE " + prompt_id, meta.get("source_stage") == "fire-shield-ai-policy-enforcement-v1" and meta.get("updated_for") == "fire-shield-ai-policy-enforcement-v1")
        triggers = [str(item).lower() for item in meta.get("trigger_phrases", [])]
        gate("META_FIRE_SHIELD_TRIGGER " + prompt_id, "fire shield" in triggers)

    route = load_json(root, ROUTE_JSON)
    entries = route.get("entries")
    if not isinstance(entries, list):
        raise AssertionError("route entries must be list")
    ids = [item.get("prompt_id") for item in entries if isinstance(item, dict)]
    for prompt_id in (
        "project_tool_boundary_canon",
        "project_tool_boundary_startup_bridge",
        "ai_prompt_request_canon",
        "patch_validate_freeze_error_memory_routine_blueprint",
    ):
        gate("ROUTE_UNIQUE " + prompt_id, ids.count(prompt_id) == 1)
        item = next(x for x in entries if isinstance(x, dict) and x.get("prompt_id") == prompt_id)
        triggers = [str(value).lower() for value in item.get("trigger_phrases", [])]
        gate("ROUTE_FIRE_SHIELD_TRIGGER " + prompt_id, "fire shield" in triggers)

    gate("NO_NEW_FIRE_SHIELD_PROMPT_OWNER", not any(str(value).startswith("fire_shield_") for value in ids))
    print("FIRE_SHIELD_AI_POLICY_OWNER_REUSE: PASS")
    print("FIRE_SHIELD_AI_POLICY_FAIL_CLOSED: PASS")
    print("FIRE_SHIELD_AI_POLICY_PUBLIC_SURFACE_ONLY: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
