"""Validate Prompt Audit Wave 4A governance/freeze/handoff correction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

__all__: list[str] = []

FEATURE_ID = "prompt-audit-wave4a-governance-freeze-handoff-v1"
ACTIVE_IDS = (
    "brick_wall_comprehensive_quality_gate",
    "cooperative_implementation_methodology",
    "freeze_code_intake_and_form_protocol",
    "pre_output_contract_gates",
    "professional_engineering_governance_template",
    "workflow_handoff_template",
)
RETIRED_IDS = (
    "active_governance_freeze_update",
    "current_workflow_handoff_template",
    "end_of_chat_governance_update_template",
    "reasoner_professional_engineering_governance",
)
CODES = {
    "brick_wall_comprehensive_quality_gate": "KPR-03-001",
    "cooperative_implementation_methodology": "KPR-03-002",
    "freeze_code_intake_and_form_protocol": "KPR-03-003",
    "pre_output_contract_gates": "KPR-03-004",
    "professional_engineering_governance_template": "KPR-03-005",
    "workflow_handoff_template": "KPR-03-006",
}
BRICK_HASH = "fcf5169a3b1fb032c12406391055f24035e8bcaf36ad473792dd85feeb895eb3"


class ValidationError(RuntimeError):
    """Raised when the Wave 4A contract is not satisfied."""


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(loaded, dict):
        raise ValidationError("JSON root must be an object: " + str(path))
    return loaded


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise ValidationError(marker)
    print(marker + ": PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    library = root / "kanda_prompt_workspace/prompt_library"
    active = library / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff"
    metadata = library / "METADATA"
    routing = library / "ROUTING"

    brick = active / "brick_wall_comprehensive_quality_gate.md"
    require(brick.is_file() and sha256(brick) == BRICK_HASH, "WAVE4A_BRICK_WALL_Q01_Q40_PRESERVED")

    for prompt_id in ACTIVE_IDS:
        source = active / (prompt_id + ".md")
        meta = metadata / (prompt_id + ".meta.json")
        require(source.is_file() and meta.is_file(), "WAVE4A_ACTIVE_OWNER_" + prompt_id.upper())
        if prompt_id != "brick_wall_comprehensive_quality_gate":
            text = source.read_text(encoding="utf-8-sig")
            data = load_json(meta)
            require(len(text.splitlines()) <= 500, "WAVE4A_LINE_LIMIT_" + prompt_id.upper())
            require(data.get("prompt_code") == CODES[prompt_id], "WAVE4A_CODE_" + prompt_id.upper())
            source_stage = str(data.get("source_stage") or "").strip()
            updated_for = str(data.get("updated_for") or "").strip()
            require(
                bool(source_stage)
                and updated_for == source_stage
                and ("source_stage: " + source_stage) in text,
                "WAVE4A_METADATA_STAGE_" + prompt_id.upper(),
            )

    for prompt_id in RETIRED_IDS:
        require(not (active / (prompt_id + ".md")).exists(), "WAVE4A_RETIRED_SOURCE_" + prompt_id.upper())
        require(not (metadata / (prompt_id + ".meta.json")).exists(), "WAVE4A_RETIRED_METADATA_" + prompt_id.upper())

    app_paths = (
        "active/0000 3.6 PYARCHITECT PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.0.md",
        "active/0000 4.0 PYARCHITECT END OF CHAT GOVERNANCE UPDATE TEMPLATE v1.0.md",
        "active/0000 6.0 PYARCHITECT WORKFLOW HANDOFF TEMPLATE v1.0.md",
        "metadata/0000_3_6_professional_engineering_governance_layer.meta.json",
        "metadata/0000_4_0_end_of_chat_governance_update_template.meta.json",
        "metadata/0000_6_0_workflow_handoff_template.meta.json",
    )
    app_library = root / "kanda_reasoner_app/prompt_library"
    require(all(not (app_library / item).exists() for item in app_paths), "WAVE4A_APPLICATION_DUPLICATES_REMOVED")

    group_data = load_json(library / "GROUPS/PROMPT_GROUPS_DRAFT.json")
    group = next(item for item in group_data["groups"] if item.get("group_id") == "03_governance_freeze_and_handoff")
    require(group.get("prompt_ids") == list(ACTIVE_IDS), "WAVE4A_CLASS03_GROUP_OWNER_SET")
    require(group.get("prompt_count") == 6, "WAVE4A_CLASS03_PROMPT_COUNT")

    nav = load_json(routing / "prompt_navigation_index.json")
    nav_ids = [str(item.get("prompt_id")) for item in nav["entries"]]
    require(all(item in nav_ids for item in ACTIVE_IDS), "WAVE4A_ACTIVE_NAVIGATION_COMPLETE")
    require(all(item not in nav_ids for item in RETIRED_IDS), "WAVE4A_RETIRED_NAVIGATION_REMOVED")

    with (routing / "prompt_route_coverage_table.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    route_ids = [str(row.get("prompt_id")) for row in rows]
    require(all(item in route_ids for item in ACTIVE_IDS), "WAVE4A_ACTIVE_ROUTE_COVERAGE")
    require(all(item not in route_ids for item in RETIRED_IDS), "WAVE4A_RETIRED_ROUTE_COVERAGE_REMOVED")

    substitution = (library / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_substitution_map.md").read_text(encoding="utf-8-sig")
    require("## Wave 4A Class 03 lifecycle records" in substitution, "WAVE4A_SUBSTITUTION_RECORDS")
    require(all(item in substitution for item in RETIRED_IDS), "WAVE4A_RETIRED_ALIAS_COVERAGE")

    registry = (library / "ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_identity_code_registry_canon.md").read_text(encoding="utf-8-sig")
    require(all(code in registry and prompt_id in registry for prompt_id, code in CODES.items()), "WAVE4A_PROMPT_CODE_REGISTRY")

    current_surfaces = [
        library / "GROUPS/PROMPT_GROUPS_DRAFT.json",
        routing / "group_assimilation_index.json",
        routing / "folder_assimilation_cards_index.json",
        routing / "prompt_navigation_index.json",
        routing / "prompt_route_coverage_table.csv",
        app_library / "groups/PROMPT_GROUPS.json",
        app_library / "profiles/PROJECT_PROMPT_STACK_PROFILE_TEMPLATE.json",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8-sig") for path in current_surfaces)
    require(all(item not in combined for item in RETIRED_IDS), "WAVE4A_NO_ACTIVE_RETIRED_REFERENCES")

    cooperative = (active / "cooperative_implementation_methodology.md").read_text(encoding="utf-8-sig")
    require("May begin coding from this prompt: NO" in cooperative, "WAVE4A_COOPERATIVE_NO_CODING_AUTHORITY")
    freeze = (active / "freeze_code_intake_and_form_protocol.md").read_text(encoding="utf-8-sig")
    require("Preview Freeze Entry` is read-only" in freeze and "Confirm and Write` requires explicit human confirmation" in freeze, "WAVE4A_HUMAN_FREEZE_BOUNDARY")
    pre_output = (active / "pre_output_contract_gates.md").read_text(encoding="utf-8-sig")
    require("It does not duplicate each artifact's implementation rules" in pre_output, "WAVE4A_PRE_OUTPUT_DISPATCH_ONLY")
    require("governance super-system" not in cooperative.lower() + freeze.lower() + pre_output.lower(), "WAVE4A_NO_NEW_GOVERNANCE_SUPER_SYSTEM")

    print("WAVE4A_GOVERNANCE_FREEZE_HANDOFF_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print("WAVE4A_VALIDATION_ERROR: " + str(exc))
        raise SystemExit(1)
