"""Validate KPR-12-005 identity, lifecycle schema, and routing."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path

FEATURE_ID = "architecture-review-project-card-machine-canon-router-bridge-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
PROMPT_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
META_REL = PLIB / "METADATA/architecture_review_project_card_machine_canon.meta.json"
FOLDER_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md"
NAV_REL = PLIB / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
ROUTE_REL = PLIB / "ROUTING/prompt_navigation_index.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"

STATES = (
    "EMPTY",
    "CARD_INSERTED",
    "CARD_READ",
    "PLAN_READY",
    "WORKBENCH_READY",
    "PREVIEW_VALIDATED",
    "AUTHORIZED",
    "APPLYING",
    "APPLIED_NOT_VERIFIED",
    "VERIFIED_TERMINAL",
    "CARD_EJECTED",
    "ROLLBACK_REQUESTED",
    "ROLLBACK_VERIFIED",
)


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def load_json(path: Path) -> dict[str, object]:
    loaded = json.loads(read(path))
    if not isinstance(loaded, dict):
        raise AssertionError("JSON root must be object")
    return loaded


def version(value: object) -> tuple[int, ...]:
    parts = str(value).strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise AssertionError("invalid version")
    return tuple(int(part) for part in parts)


def gate(label: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()

    prompt = read(root / PROMPT_REL)
    for marker in (
        "Prompt ID: architecture_review_project_card_machine_canon",
        "Prompt code: KPR-12-005",
        "KANDA Reasoner Tool = reusable card machine",
        "Active Project = card owner",
        "## Lifecycle state machine",
        "APPLYING",
        "APPLIED_NOT_VERIFIED",
        "VERIFIED_TERMINAL",
        "operation_id",
        "apply_attempt_id",
        "rollback_id",
        "## Orthogonal operation locks",
        "## Cancellation rule",
        "## Crash and restart recovery",
        "## Concurrent-session rule",
        "MCard lifecycle gate: COMPLETE / NOT_APPLICABLE / BLOCKED",
        "May begin coding: NO",
    ):
        gate("MCARD_CANON_MARKER", marker in prompt)
    for state in STATES:
        gate("MCARD_STATE_" + state, state in prompt)
    gate("MCARD_NO_LOCAL_IMPLEMENT_AUTHORITY", "May implement: YES" not in prompt)
    gate("MCARD_PROMPT_WITHIN_LIMIT", len(prompt.splitlines()) <= 500)

    meta = load_json(root / META_REL)
    gate("MCARD_METADATA_IDENTITY", meta.get("prompt_code") == "KPR-12-005" and meta.get("load_type") == "routed")
    gate("MCARD_METADATA_VERSION", version(meta.get("version")) >= (2, 0))
    gate("MCARD_METADATA_STAGE", meta.get("source_stage") == meta.get("updated_for") and bool(str(meta.get("source_stage") or "").strip()))
    companions = set(meta.get("required_companion_prompts") or [])
    gate("MCARD_ROOT_OWNER_COMPANION", companions == {"project_tool_boundary_canon"})

    bridge_meta = load_json(root / BRIDGE_META_REL)
    gate("MCARD_BRIDGE_FORWARD_VERSION", version(bridge_meta.get("version")) >= (1, 3))
    _parse_version = version
    assert _parse_version(bridge_meta.get("version")) >= (1, 3)

    folder = read(root / FOLDER_REL)
    nav = read(root / NAV_REL)
    gate("MCARD_FOLDER_REGISTRATION", "architecture_review_project_card_machine_canon" in folder)
    gate("MCARD_NAVIGATION_REGISTRATION", "KPR-12-005 = architecture_review_project_card_machine_canon" in nav)

    route = load_json(root / ROUTE_REL)
    entries = [item for item in route.get("entries", []) if isinstance(item, dict) and item.get("prompt_id") == "architecture_review_project_card_machine_canon"]
    gate("MCARD_MACHINE_ROUTE_UNIQUE", len(entries) == 1)
    gate("MCARD_MACHINE_ROUTE_VERSIONED_OWNER", entries[0].get("prompt_code") == "KPR-12-005")

    print("CARD_MACHINE_CANON_PRINCIPLE: PASS")
    print("CARD_MACHINE_PROMPT_IDENTITY_METADATA: PASS")
    print("GENERALIZED_CANON_FOLDER_REGISTRATION: PASS")
    print("ROUTER_BRIDGE_CARD_LIFECYCLE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
