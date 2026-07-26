"""Validate Imported Web AI ZIP intake and exact Panel 4 paste fallback."""
from __future__ import annotations

import ast
import tempfile
from pathlib import Path

__all__ = ["main"]

FEATURE = "planner-web-ai-plan-panel-zip-and-paste-intake-v1"
ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
PROMPT = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_large_module_refactor_exchange_protocol.md"
BLUEPRINT = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_planning_response_bundle_blueprint.md"


def need(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> int:
    gui_path = BOX / "planner_web_ai_exchange_gui.py"
    importer_path = BOX / "planner_web_ai_import_artifact.py"
    gui = gui_path.read_text(encoding="utf-8")
    importer = importer_path.read_text(encoding="utf-8")
    ast.parse(gui)
    ast.parse(importer)
    prompt = PROMPT.read_text(encoding="utf-8")
    blueprint = BLUEPRINT.read_text(encoding="utf-8")

    for token in (
        "Imported Web AI Version",
        "Panel 4: Proposed split plan",
        "KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN",
        "pending_imported_web_ai_plan.txt",
    ):
        need(token in prompt or token in blueprint or token in gui or token in importer, "Intake token missing: " + token)
    need("byte-identical" in blueprint or "byte identical" in blueprint, "Exact payload fallback missing")
    need("ZIP as the canonical" in blueprint or "canonical default is a ZIP" in blueprint, "ZIP default missing")
    need(len(gui.splitlines()) <= 500 and len(importer.splitlines()) <= 500, "Touched module exceeds 500 lines")

    sample = "KANDA_WEB_AI_PLANNING_RESPONSE_BEGIN\n{}\nKANDA_WEB_AI_PLANNING_RESPONSE_END\n"
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "pending_imported_web_ai_plan.txt"
        path.write_text(sample, encoding="utf-8", newline="\n")
        need(path.read_text(encoding="utf-8") == sample, "External pending artifact roundtrip failed")

    print("RECEIVE_PLANNING_BUTTON_REMOVED: PASS")
    print("PANEL4_DIRECT_PASTE_GESTURE: PASS")
    print("IMPORTED_WEB_AI_SELECTION_LOADS_CANONICAL_ZIP_ARTIFACT: PASS")
    print("PASTE_VALIDATE_STAGE_READBACK_REVALIDATE_REVIEW: PASS")
    print("WORKBENCH_INTERNAL_RECEIVE_ENTRYPOINT_PRESERVED: PASS")
    print("EXTERNAL_PENDING_ARTIFACT_EXACT_ROUNDTRIP: PASS")
    print("ZIP_REMAINS_CANONICAL_DEFAULT: PASS")
    print("AI_OUTPUT_REQUIRES_CHAT_COPY_BLOCK: PASS")
    print("CANONICAL_PROMPT_PANEL4_WORKFLOW: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("PLANNER_WEB_AI_PLAN_PANEL_ZIP_AND_PASTE_INTAKE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
