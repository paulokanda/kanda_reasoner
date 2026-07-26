"""Validate current module-size law and retired bridge compatibility."""
from __future__ import annotations

import json
from pathlib import Path

from _wave6a_prompt_contract import validate_current_contract

__all__: list[str] = []

FEATURE_ID = "router-bridge-module-size-law-v1"
ROOT = Path(__file__).resolve().parents[1]
BRIDGE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
STARTUP = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/start_of_day_master_stack.md"
)
ROUTING = Path(
    "kanda_prompt_workspace/prompt_library/ROUTING/"
    "PROMPT_NAVIGATION_INDEX.md"
)


def read(relative: Path) -> str:
    """Read one required project-relative UTF-8 file."""
    path = ROOT / relative
    if not path.is_file():
        raise AssertionError("Missing required file: " + str(relative))
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, label: str) -> None:
    """Emit one deterministic compatibility gate."""
    if not condition:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def main() -> None:
    """Validate the current owner and deprecated bridge redirect."""
    validate_current_contract(ROOT)

    bridge = read(BRIDGE)
    metadata = json.loads(read(BRIDGE_META))
    startup = read(STARTUP)
    routing = read(ROUTING)

    require(
        metadata.get("status") == "deprecated",
        "ROUTER_BRIDGE_MODULE_SIZE_TOMBSTONE_STATUS",
    )
    require(
        metadata.get("load_type") == "never",
        "ROUTER_BRIDGE_MODULE_SIZE_NO_ACTIVE_ROUTE",
    )
    require(
        "DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE" in bridge,
        "ROUTER_BRIDGE_MODULE_SIZE_TOMBSTONE_TEXT",
    )
    require(
        "brick_wall_comprehensive_quality_gate" in bridge,
        "ROUTER_BRIDGE_MODULE_SIZE_CURRENT_GATE_REDIRECT",
    )
    require(
        "large_module_refactor_protocol.md" in startup
        and "500 physical lines" in startup,
        "STARTUP_CURRENT_MODULE_SIZE_OWNER",
    )
    require(
        "KPR-06-007" in routing
        and "large_module_refactor_protocol" in routing,
        "ROUTING_CURRENT_MODULE_SIZE_OWNER",
    )

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
