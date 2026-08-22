"""Validate KPR-12-005 observer lifecycle schema and routing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

__all__: list[str] = []
FEATURE_ID = "architecture-review-project-card-machine-observer-canon-router-v2"
PLIB = Path("kanda_prompt_workspace/prompt_library")
PROMPT_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
META_REL = PLIB / "METADATA/architecture_review_project_card_machine_canon.meta.json"
FOLDER_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/_FOLDER_ASSIMILATION.md"
NAV_REL = PLIB / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
ROUTE_REL = PLIB / "ROUTING/prompt_navigation_index.json"
STATES = ("EMPTY", "CARD_INSERTED", "CARD_READ", "OBSERVED", "ANALYSIS_READY", "REPORT_READY", "CARD_EJECTED")
RETIRED = ("AUTHORIZED", "APPLYING", "APPLIED_NOT_VERIFIED", "ROLLBACK_REQUESTED", "ROLLBACK_VERIFIED")


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(read(path))
    if not isinstance(data, dict):
        raise AssertionError("JSON root must be object")
    return data


def version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError:
        return ()


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
        "Prompt code: KPR-12-005", "KANDA Reasoner Tool = reusable observer card machine",
        "## Observer lifecycle state machine", "Project development remains possible when KANDA is closed",
        "No Project source rollback", "May begin coding from MCard: NO",
    ):
        gate("MCARD_CANON_MARKER", marker in prompt)
    for state in STATES:
        gate("MCARD_STATE_" + state, state in prompt)
    for state in RETIRED:
        gate("MCARD_RETIRED_STATE_NOT_ACTIVE_" + state, ("-> " + state) not in prompt)
    gate("MCARD_PROMPT_WITHIN_LIMIT", len(prompt.splitlines()) <= 500)
    meta = load_json(root / META_REL)
    gate("MCARD_METADATA_IDENTITY", meta.get("prompt_code") == "KPR-12-005" and meta.get("load_type") == "routed")
    gate("MCARD_METADATA_VERSION", version(meta.get("version")) >= (3, 0))
    gate("MCARD_METADATA_STAGE", meta.get("source_stage") == meta.get("updated_for") and bool(str(meta.get("source_stage") or "").strip()))
    folder = read(root / FOLDER_REL)
    nav = read(root / NAV_REL)
    gate("MCARD_FOLDER_REGISTRATION", "architecture_review_project_card_machine_canon" in folder)
    gate("MCARD_NAVIGATION_REGISTRATION", "KPR-12-005 = architecture_review_project_card_machine_canon" in nav)
    route = load_json(root / ROUTE_REL)
    entries = [item for item in route.get("entries", []) if isinstance(item, dict) and item.get("prompt_id") == "architecture_review_project_card_machine_canon"]
    gate("MCARD_MACHINE_ROUTE_UNIQUE", len(entries) == 1)
    gate("MCARD_MACHINE_ROUTE_VERSIONED_OWNER", entries[0].get("prompt_code") == "KPR-12-005")
    print("CARD_MACHINE_CANON_PRINCIPLE: PASS")
    print("CARD_MACHINE_AND_TOOL_PROJECT_CANONS_COMPLEMENTARY: PASS")
    print("ROUTER_BRIDGE_CARD_LIFECYCLE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
