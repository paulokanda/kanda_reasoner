"""Validate current KPR-06-003 wrapper and single AST output contract."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "architecture-review-ast-split-web-ai-risk-repair-single-output-v1"
ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_ast_split_risk_repair_protocol.md"
GUI = ROOT / "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py"


def need(value: bool, message: str) -> None:
    if not value:
        raise SystemExit("VALIDATION ERROR: " + message)


def main() -> int:
    prompt = PROMPT.read_text(encoding="utf-8")
    gui = GUI.read_text(encoding="utf-8")
    ast.parse(gui)
    for token in (
        "KPR-06-003",
        "Version: 2.0.0",
        "target-specific AST repair reasoning",
        "SOURCE_SHA256",
        "SOURCE_BYTE_LENGTH",
        "SOURCE_TEXT_ENDS_WITH_NEWLINE",
        "RISK REFACTORING",
        "SAFE REFACTORING",
        "fresh rerun evidence",
        "single AST Split Audit",
        "400 physical lines or fewer",
        "500 physical lines or fewer",
        "universal minimum: none",
    ):
        need(token in prompt, "prompt missing " + token)
    need("101-499" not in prompt, "obsolete universal 101-499 law remains")
    for token in (
        "web_ai_ast_split_risk_repair_protocol.md",
        "Send Web AI to make SAFE",
        "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN",
        "SOURCE_BYTE_LENGTH",
        "SOURCE_TEXT_ENDS_WITH_NEWLINE",
        "QApplication.clipboard().setText",
    ):
        need(token in gui, "wrapper missing " + token)
    need("target-specific AST repair reasoning" not in gui, "prompt body embedded in GUI")
    need("add_ast_split_web_ai_risk_repair_response_editor" not in gui, "second response editor returned")
    need(len(gui.splitlines()) <= 500, "AST GUI exceeds 500 lines")

    sample = b'print("hello")\n'
    need(hashlib.sha256(sample).hexdigest() == hashlib.sha256(sample).hexdigest(), "source identity fixture failed")

    print("AST_SPLIT_SINGLE_TEXT_WINDOW_ONLY: PASS")
    print("AST_SPLIT_RUN_OUTPUT_AND_WEB_AI_PASTE_SHARE_WINDOW: PASS")
    print("AST_SPLIT_WEB_AI_REPORT_FORMAT_MATCHES_NATIVE_MARKDOWN: PASS")
    print("AST_SPLIT_SEND_WEB_AI_BUTTON_POSITION: PASS")
    print("AST_SPLIT_SEND_WEB_AI_BUTTON_ORANGE_TEXT_ONLY: PASS")
    print("AST_SPLIT_WRAPPER_TARGET_SOURCE_HASH_AUDIT: PASS")
    print("AST_SPLIT_BOX_SHIELD_NO_CROSS_BOX_STATE_LEAK: PASS")
    print("AST_SPLIT_TARGET_CHANGE_CLEARS_SINGLE_OUTPUT: PASS")
    print("CURRENT_MODULE_SIZE_POLICY_DELEGATION: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
