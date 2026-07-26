# project-path: scripts/validate_bridge_error_memory_implementation_error_gate_v1.py
"""Validate current correction incident and Error Memory dispatch behavior."""
from __future__ import annotations

__all__: list[str] = []

import json
from pathlib import Path

FEATURE_ID = "bridge-error-memory-implementation-error-gate-v2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_user_detected_correction.md"
USER_META = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library/METADATA/router_bridge_user_detected_correction.meta.json"
PRE_OUTPUT = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md"
ERROR_MEMORY_TAB = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
LAZY_TABS = PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(label + " missing fragment: " + fragment)


def main() -> int:
    user = read(USER)
    for fragment in (
        "prompt_code: KPR-05-006",
        "CORRECTION INCIDENT RECORD",
        "May begin correction coding: NO",
        "Direct owner dispatch",
        "pre_output_contract_gates",
        "terminal_cleanup_contract",
        "Never write directly into Lessons",
        "This dispatcher cannot authorize implementation",
    ):
        require(user, fragment, "correction dispatcher")
    meta = json.loads(read(USER_META))
    if meta.get("prompt_code") != "KPR-05-006" or meta.get("status") != "active":
        raise AssertionError("correction dispatcher metadata identity mismatch")
    if "router_bridge_governed_implementation" in meta.get("required_companion_prompts", []):
        raise AssertionError("retired governed bridge remains required")
    pre = read(PRE_OUTPUT)
    for fragment in ("PRE-OUTPUT ARTIFACT CONTRACT", "freeze hint or form", "Error Memory"):
        require(pre, fragment, "Pre-Output")
    tab = read(ERROR_MEMORY_TAB); lazy = read(LAZY_TABS)
    require(tab, "load_pending_ai_assisted_error_lesson_intake_now", "Error Memory tab")
    require(lazy, "load_pending_ai_assisted_error_lesson_intake_now", "lazy tab host")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
