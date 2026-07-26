# project-path: tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py
"""Validate delegation between KPR-12-001 and Workbench path owners."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
from pathlib import Path

FEATURE_ID = "project-tool-boundary-workbench-preview-router-bridge-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
CANON_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
CANON_META_REL = PLIB / "METADATA/project_tool_boundary_canon.meta.json"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
ROUTE_REL = PLIB / "ROUTING/prompt_navigation_index.json"


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def gate(label: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()

    canon = read(root / CANON_REL)
    bridge = read(root / BRIDGE_REL)
    gate("PROJECT_TOOL_BOUNDARY_CANON_WORKBENCH_DELEGATION", "Workbench Preview, Shadow, transaction, and receipt paths: current Workbench owner" in canon)
    gate("PROJECT_TOOL_BOUNDARY_NO_DUPLICATE_WORKBENCH_PATHS", "<active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>" not in canon)
    gate("PROJECT_TOOL_BOUNDARY_TRANSIENT_TERM_FIXED", "ownership-free transient" not in canon.lower())
    gate("ROUTER_BRIDGE_WORKBENCH_OWNERSHIP_GATE", "## Workbench Preview / Shadow ownership bridge" in bridge)

    meta = json.loads(read(root / CANON_META_REL))
    gate("PROJECT_TOOL_BOUNDARY_ROUTED_METADATA", meta.get("load_type") == "routed" and meta.get("prompt_code") == "KPR-12-001")
    route = json.loads(read(root / ROUTE_REL))
    entries = [item for item in route.get("entries", []) if isinstance(item, dict) and item.get("prompt_id") == "project_tool_boundary_canon"]
    gate("ROUTING_METADATA_AND_INDEX_SYNC", len(entries) == 1 and entries[0].get("load_type") == "routed")
    gate("NO_COMPETING_PROJECT_TOOL_BOUNDARY_PROMPT", sum(1 for path in (root / PLIB / "METADATA").glob("*.meta.json") if json.loads(read(path)).get("prompt_code") == "KPR-12-001") == 1)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
