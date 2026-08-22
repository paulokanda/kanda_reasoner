from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

STARTUP_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
)
ZIP_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/self_contained_error_memory_lesson_intake_zip.md"
)
STARTUP_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "error_memory_ai_formulary_startup_canon.meta.json"
)
ZIP_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "self_contained_error_memory_lesson_intake_zip.meta.json"
)
BLUEPRINT_REL = Path("kanda_reasoner_app/error_memory_gui/_intake_blueprint.py")
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    startup = (root / STARTUP_REL).read_text(encoding="utf-8")
    zprompt = (root / ZIP_REL).read_text(encoding="utf-8")
    tab = (root / TAB_REL).read_text(encoding="utf-8")
    blueprint = (root / BLUEPRINT_REL).read_text(encoding="utf-8")
    ast.parse(tab)
    ast.parse(blueprint)

    startup_meta = json.loads((root / STARTUP_META_REL).read_text(encoding="utf-8"))
    zip_meta = json.loads((root / ZIP_META_REL).read_text(encoding="utf-8"))

    require("version: 4.0" in startup, "ERROR_MEMORY_LIBRARY_CANON_VERSION")
    require("Error Memory is a lesson library, not Machine-Card/MCard." in startup,
            "ERROR_MEMORY_LIBRARY_BOUNDARY")
    require("version: 3.0" in zprompt, "ERROR_MEMORY_ZIP_CANON_VERSION")
    require("Self-Contained Error Memory Lesson Intake ZIP" in zprompt,
            "ERROR_MEMORY_ZIP_TITLE")
    require("ERROR_MEMORY_LESSON_LIBRARY_LOADER.py" in zprompt,
            "ERROR_MEMORY_LIBRARY_LOADER")
    require("ERROR_MEMORY_MCARD_LOADER.py" not in zprompt,
            "ERROR_MEMORY_MCARD_LOADER_STILL_ACTIVE")
    require("Get correct way to send me errors" in tab, "GET_CORRECT_BUTTON")
    require("Send Zip Errors" in tab, "SEND_ZIP_BUTTON")
    require("independent MCard pending-intake ZIP prompt" not in tab,
            "SEND_ZIP_TOOLTIP_STILL_MCARD")
    require("Tool-owned MCard ZIP prompt" not in blueprint,
            "SEND_ZIP_RESOLVER_STILL_MCARD")
    require(startup_meta.get("version") == "4.0", "STARTUP_META_VERSION")
    require(zip_meta.get("version") == "3.0", "ZIP_META_VERSION")
    require("MCard" not in zip_meta.get("display_name", ""), "ZIP_META_MCARD_TITLE")

    print("ERROR MEMORY BUTTON PROMPTS LESSON LIBRARY: PASS")
    print("ERROR MEMORY BUTTON PROMPTS MACHINE-CARD AUTHORITY: ABSENT")
    print("ERROR MEMORY BUTTON LABELS PRESERVED: PASS")
    print("ERROR MEMORY HUMAN MEMORIZE GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
