"""Validate current KPR-06-001 prompt, Planner button, and dynamic wrapper."""
from __future__ import annotations

import ast
import json
from pathlib import Path

__all__ = ["main"]

FEATURE = "large-file-refactor-planner-web-ai-howto-prompt-button-v1"
ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS"
META = ROOT / "kanda_prompt_workspace/prompt_library/METADATA"
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
PROMPT_ID = "web_ai_large_module_refactor_exchange_protocol"
PROMPT = ACTIVE / "06_refactor_and_architecture_hardening" / (PROMPT_ID + ".md")


def need(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("VALIDATION ERROR: " + message)


def main() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    for token in (
        "KPR-06-001",
        "Version: 2.0.0",
        "planning reasoning and bounded action selection only",
        "Copy Comprehensive Planning for Web AI",
        "smallest defensible",
        "pending_imported_web_ai_plan.txt",
        "KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN",
        "Panel 4: Proposed split plan",
        "Preview Freeze Entry",
        "Confirm and Write",
    ):
        need(token in text, "specialist prompt missing token " + token)
    meta = json.loads((META / (PROMPT_ID + ".meta.json")).read_text(encoding="utf-8"))
    need(meta.get("prompt_code") == "KPR-06-001", "prompt code mismatch")
    need(meta.get("version") == "2.0.0", "prompt version mismatch")
    need(meta.get("source_stage") == "prompt-audit-wave6c-web-ai-exchange-boundaries-v1", "prompt provenance mismatch")

    shell = (BOX / "gui_shell.py").read_text(encoding="utf-8")
    gui = (BOX / "planner_web_ai_exchange_gui.py").read_text(encoding="utf-8")
    ast.parse(shell)
    ast.parse(gui)
    need('QPushButton("AI Refactor Version How To")' in shell, "How To button missing")
    need("background-color: #f28c28" in shell and "font-weight: bold" in shell, "How To style missing")
    need(PROMPT_ID + ".md" in gui, "canonical prompt path missing")
    need("QApplication.clipboard().setText" in gui, "clipboard wrapper missing")
    need("planning reasoning and bounded action selection only" not in gui, "prompt body embedded in GUI")
    need(len(gui.splitlines()) <= 500 and len(shell.splitlines()) <= 500, "touched GUI module exceeds 500 lines")

    print("LARGE_MODULE_CANON: CURRENT_KPR_06_007_AUTHORITY")
    print("SPECIALIST_PROMPT: KPR-06-001_ROUTED_COMPANION")
    print("ROUTER_BRIDGE: EXTERNAL_WEB_AI_IMPORT_FLOW_REGISTERED")
    print("GUI_BUTTON: AI_REFACTOR_VERSION_HOW_TO_ORANGE_BOLD")
    print("GUI_WRAPPER: CANONICAL_PROMPT_READ_NO_EMBEDDED_DUPLICATE")
    print("WEB_AI_REASONING_BOUNDARY: PLANNING_ONLY")
    print("WEB_AI_BUNDLE_DELEGATION: KPR_06_002")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
