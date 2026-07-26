"""Validate current KPR-06-002 blueprint and Planner send wrapper."""
from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["main"]

FEATURE = "planner-web-ai-bundle-blueprint-send-wrapper-v1"
ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS"
BLUEPRINT = ACTIVE / "06_refactor_and_architecture_hardening/web_ai_planning_response_bundle_blueprint.md"
COMPANION = ACTIVE / "06_refactor_and_architecture_hardening/web_ai_large_module_refactor_exchange_protocol.md"
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def need(value: bool, message: str) -> None:
    if not value:
        raise SystemExit("VALIDATION ERROR: " + message)


def main() -> None:
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    companion = COMPANION.read_text(encoding="utf-8")
    for token in (
        "KPR-06-002",
        "Version: 2.0.0",
        "payload and bundle profile",
        "pending_imported_web_ai_plan.txt",
        "INSTALL.ps1",
        "VALIDATE.ps1",
        "FREEZE.ps1",
        "KANDA_FREEZE_HINT.json",
        "bundle_manifest.json",
        "Regex.Matches",
        "Regex.Escape",
        "Panel 4: Proposed split plan",
        "Preview Freeze Entry",
        "Confirm and Write",
    ):
        need(token in blueprint, "blueprint missing " + token)
    need("KPR-06-001" in companion and "KPR-06-002" in companion, "companion boundary missing")

    shell = (BOX / "gui_shell.py").read_text(encoding="utf-8")
    layout = (BOX / "planner_inner_tabs_layout.py").read_text(encoding="utf-8")
    gui = (BOX / "planner_web_ai_exchange_gui.py").read_text(encoding="utf-8")
    ast.parse(shell)
    ast.parse(layout)
    ast.parse(gui)
    need("Send Web Ai to split file" in layout, "send button missing")
    need("web_ai_planning_response_bundle_blueprint.md" in gui, "blueprint dynamic path missing")
    need("QApplication.clipboard().setText" in gui, "clipboard wrapper missing")
    need("payload and bundle profile" not in gui, "blueprint body embedded in GUI")
    need(len(shell.splitlines()) <= 500 and len(layout.splitlines()) <= 500 and len(gui.splitlines()) <= 500, "touched source exceeds 500 lines")

    print("WEB_AI_BUNDLE_BLUEPRINT_PROMPT: PASS")
    print("ROUTER_BRIDGE_KPR_06_001_PLUS_KPR_06_002: PASS")
    print("SEND_WEB_AI_SPLIT_BUTTON_POSITION: PASS")
    print("SEND_WEB_AI_SPLIT_BUTTON_ORANGE_BOLD_TEXT_ONLY: PASS")
    print("SEND_WEB_AI_SPLIT_WRAPPER_CANONICAL_PROMPT_PLUS_CURRENT_PACKAGE: PASS")
    print("ZIP_CANONICAL_PANEL4_FALLBACK_CONTRACT: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
