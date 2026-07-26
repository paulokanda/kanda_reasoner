"""Validate prompt-library transient garbage root non-ownership canon."""
from __future__ import annotations

import json
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library"
ACTIVE_ROOT = LIBRARY_ROOT / "ACTIVE_PROMPTS"
METADATA_ROOT = LIBRARY_ROOT / "METADATA"
FEATURE_ID = "transient-garbage-root-non-ownership-canon-v1"


def main() -> None:
    """Validate owner canon, routing surfaces, and prompt terminology."""
    owner = _read(
        ACTIVE_ROOT
        / "12_generalized_project_canons/project_tool_boundary_canon.md"
    )
    required_owner_markers = (
        "transient_garbage_root = <project_drive>/<active_project_slug>_delete_after_daily_work",
        "outside both the Tool ownership box and the Active Project ownership box",
        "owns no Tool state, Project state, evidence authority, or durable support state",
        "project-derived name is a namespace/staging convention only",
    )
    _require_markers("OWNER_CANON", owner, required_owner_markers)
    print("TRANSIENT_GARBAGE_OWNER_CANON: PASS")

    required_surfaces = {
        "prompt_navigation_index": ACTIVE_ROOT
        / "02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "prompt_router": ACTIVE_ROOT
        / "02_prompt_routing_and_indexing/prompt_router.md",
        "routing_system_canon": ACTIVE_ROOT
        / "02_prompt_routing_and_indexing/kanda_routing_system_canon.md",
        "governed_implementation_bridge": ACTIVE_ROOT
        / "05_patch_delivery_and_validation/router_bridge_governed_implementation.md",
        "card_machine_canon": ACTIVE_ROOT
        / "12_generalized_project_canons/architecture_review_project_card_machine_canon.md",
        "daily_patch_guardrails": ACTIVE_ROOT
        / "01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
    }
    for label, path in required_surfaces.items():
        text = _read(path)
        if "transient_garbage_root" not in text and label != "daily_patch_guardrails":
            raise AssertionError("TRANSIENT_GARBAGE_ROUTE_MISSING:" + label)
        if label == "daily_patch_guardrails" and "garbage/staging path only" not in text:
            raise AssertionError("TRANSIENT_GARBAGE_NON_OWNERSHIP_GUARD_MISSING")
    print("TRANSIENT_GARBAGE_ROUTING_SURFACES: PASS")

    durable_surfaces = {
        "large_module_refactor_protocol": ACTIVE_ROOT
        / "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md",
        "large_module_refactor_template": ACTIVE_ROOT
        / "06_refactor_and_architecture_hardening/large_module_refactor_template.md",
        "web_ai_large_module_refactor_exchange_protocol": ACTIVE_ROOT
        / "06_refactor_and_architecture_hardening/web_ai_large_module_refactor_exchange_protocol.md",
    }
    durable_markers = (
        "*_show_project_to_AI",
        "transient garbage",
    )
    for label, path in durable_surfaces.items():
        text = _read(path)
        missing = [marker for marker in durable_markers if marker not in text]
        if missing:
            raise AssertionError(
                "DURABLE_SUPPORT_ROUTING_MISSING:" + label + ":" + "|".join(missing)
            )
    protocol = _read(durable_surfaces["large_module_refactor_protocol"])
    if "<drive>/<project>_show_project_to_AI/large_module_split_audits/" not in protocol:
        raise AssertionError("AST_AUDIT_SUPPORT_OWNER_ROUTE_MISSING")
    template = _read(durable_surfaces["large_module_refactor_template"])
    if (
        "Write durable audits, handoffs, and validation evidence" not in template
        or "`*_show_project_to_AI` support root" not in template
    ):
        raise AssertionError("REFACTOR_TEMPLATE_DURABLE_SUPPORT_ROUTE_MISSING")
    print("DURABLE_PROJECT_EVIDENCE_ROUTED_TO_SUPPORT: PASS")

    forbidden_terms = (
        "active_project_daily_work_root",
        "Active Project daily-work",
        "selected project's daily-work root",
        "active project daily-work root",
        "project-linked daily-work folder",
    )
    offenders: list[str] = []
    for root in (ACTIVE_ROOT, METADATA_ROOT):
        for path in root.rglob("*"):
            if path.suffix not in {".md", ".json"}:
                continue
            text = _read(path)
            for term in forbidden_terms:
                if term in text:
                    offenders.append(f"{path.relative_to(LIBRARY_ROOT)}::{term}")
    if offenders:
        raise AssertionError("FORBIDDEN_DAILY_WORK_OWNERSHIP_LANGUAGE:" + "|".join(offenders))
    print("NO_DAILY_WORK_OWNERSHIP_LANGUAGE: PASS")

    metadata_files = (
        METADATA_ROOT / "project_tool_boundary_canon.meta.json",
        METADATA_ROOT / "architecture_review_project_card_machine_canon.meta.json",
        METADATA_ROOT / "router_bridge_governed_implementation.meta.json",
        METADATA_ROOT / "large_module_refactor_protocol.meta.json",
        METADATA_ROOT / "patch_validate_freeze_error_memory_routine_blueprint.meta.json",
    )
    for path in metadata_files:
        json.loads(path.read_text(encoding="utf-8"))
    print("PROMPT_METADATA_JSON_VALID: PASS")

    operational_mentions = sum(
        _read(path).count("_delete_after_daily_work")
        for path in ACTIVE_ROOT.rglob("*.md")
    )
    if operational_mentions < 1:
        raise AssertionError("TRANSIENT_GARBAGE_OPERATIONAL_PATHS_REMOVED")
    print("TRANSIENT_GARBAGE_OPERATIONAL_USE_PRESERVED: PASS")
    print("TRANSIENT_GARBAGE_ROOT_NON_OWNERSHIP_CANON: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _require_markers(label: str, text: str, markers: tuple[str, ...]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise AssertionError(label + "_MARKERS_MISSING:" + "|".join(missing))


if __name__ == "__main__":
    main()
