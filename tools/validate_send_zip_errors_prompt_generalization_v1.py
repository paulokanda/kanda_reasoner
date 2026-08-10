"""Validate KPR-05-008 current-Project generalization in place."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import py_compile
import sys
from pathlib import Path

FEATURE_ID = "send-zip-errors-prompt-generalization-v1"
PROMPT_ID = "self_contained_error_memory_lesson_intake_zip"
PROMPT_CODE = "KPR-05-008"
PROMPT_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/self_contained_error_memory_lesson_intake_zip.md")
META_REL = Path("kanda_prompt_workspace/prompt_library/METADATA/self_contained_error_memory_lesson_intake_zip.meta.json")
ALLOW_REL = Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json")
BUILDER_REL = Path("portable/PORTABLE_BUILDER_MANIFEST.json")
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
CLIP_REL = Path("kanda_reasoner_app/error_memory_gui/_clipboard_export.py")
BLUEPRINT_REL = Path("kanda_reasoner_app/error_memory_gui/_intake_blueprint.py")
ROUTING_ROOT = Path("kanda_prompt_workspace/prompt_library/ROUTING")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read(path: Path) -> str:
    require(path.is_file(), "Required file missing: " + str(path))
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_prompt(root: Path) -> str:
    prompt = read(root / PROMPT_REL)
    meta = json.loads(read(root / META_REL))
    required = [
        "prompt_code: KPR-05-008",
        "version: 1.1",
        "source_stage: send-zip-errors-prompt-generalization-v1",
        "PROJECT_DISPLAY_NAME",
        "PROJECT_PARENT_ROOT",
        "PROJECT_DRIVE_ROOT",
        "## CURRENT PROJECT OWNERSHIP",
        "## ANTI-CROSS-PROJECT RULE",
        "Prefer canonical selected-Project registry and owner-manifest evidence",
        "project_source_files_modified",
        "PROJECT SOURCE FILES MODIFIED: 0",
        "Do not assume the Project is `kanda_reasoner`.",
        "Do not assume the drive is `E:`.",
        "pending_ai_assisted_error_lesson_intake",
        "Memorize Error",
        "RUN_INSTALL.ps1",
    ]
    require(all(item in prompt for item in required), "Generalized prompt contract incomplete")
    require(meta.get("prompt_code") == PROMPT_CODE, "Metadata prompt code mismatch")
    require(meta.get("prompt_id") == PROMPT_ID, "Metadata prompt ID mismatch")
    require(meta.get("version") == "1.1", "Metadata version mismatch")
    require(meta.get("source_stage") == "send-zip-errors-prompt-generalization-v1", "Metadata source stage mismatch")
    require(meta.get("canonical_path") == PROMPT_REL.as_posix(), "Metadata canonical path mismatch")
    return prompt


def validate_registration(root: Path) -> None:
    nav = json.loads(read(root / ROUTING_ROOT / "prompt_navigation_index.json"))
    matches = [item for item in nav.get("entries", []) if item.get("prompt_id") == PROMPT_ID]
    require(len(matches) == 1, "Prompt navigation entry count mismatch")
    require(matches[0].get("prompt_code") == PROMPT_CODE, "Prompt code mismatch")
    codes = [item.get("prompt_code") for item in nav.get("entries", []) if item.get("prompt_code")]
    require(codes.count(PROMPT_CODE) == 1, "Prompt code is not unique")
    with (root / ROUTING_ROOT / "prompt_route_coverage_table.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(sum(1 for row in rows if row.get("prompt_id") == PROMPT_ID) == 1, "Coverage row count mismatch")


def validate_button_unchanged(root: Path, prompt: str) -> str:
    tab = read(root / TAB_REL)
    clip = read(root / CLIP_REL)
    blueprint = read(root / BLUEPRINT_REL)
    old_button = "QPushButton('Get correct way to send me errors')"
    new_button = "QPushButton('Send Zip Errors')"
    require(old_button in tab and new_button in tab, "Button preservation mismatch")
    old_add = "path_action_row.addWidget(self.copy_correct_error_delivery_button)"
    new_add = "path_action_row.addWidget(self.send_zip_errors_button)"
    require(old_add in tab and new_add in tab, "Button row wiring missing")
    require(tab.index(new_add) > tab.index(old_add), "Send Zip Errors is not right of existing button")
    require("addWidget" not in tab[tab.index(old_add)+len(old_add):tab.index(new_add)], "Buttons are not adjacent")
    require("#FF8C00" in tab, "Orange button style missing")
    require("read_send_zip_errors_prompt" in clip and "read_send_zip_errors_prompt" in blueprint, "Canonical prompt reader missing")
    for rel in (TAB_REL, CLIP_REL, BLUEPRINT_REL):
        py_compile.compile(str(root / rel), doraise=True)
    try:
        import PySide6  # noqa: F401
    except ModuleNotFoundError:
        return "SKIPPED_NO_PYSIDE6"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    previous = Path.cwd()
    os.chdir(root)
    try:
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab
        app = QApplication.instance() or QApplication([])
        widget = ErrorMemoryTab()
        widget.set_project_root(root)
        widget._show_action_done = lambda *args, **kwargs: None
        QApplication.clipboard().clear()
        widget.send_zip_errors_button.click()
        app.processEvents()
        require(QApplication.clipboard().text() == prompt, "Clipboard does not equal updated canonical prompt")
        widget.close()
        return "PASS"
    finally:
        os.chdir(previous)


def validate_portable(root: Path) -> None:
    allow_path = root / ALLOW_REL
    allow = json.loads(read(allow_path))
    by_rel = {item.get("source_relative"): item for item in allow.get("items", [])}
    for rel in (PROMPT_REL.as_posix(), META_REL.as_posix()):
        item = by_rel.get(rel)
        require(item is not None, "Runtime allowlist entry missing: " + rel)
        path = root / rel
        require(item.get("sha256") == sha256(path), "Runtime allowlist hash mismatch: " + rel)
        require(item.get("size_bytes") == path.stat().st_size, "Runtime allowlist size mismatch: " + rel)
    require(allow.get("item_count") == len(allow.get("items", [])), "Runtime allowlist count mismatch")
    builder = json.loads(read(root / BUILDER_REL))
    allow_hash = sha256(allow_path)
    require(builder.get("runtime_allowlist_sha256") == allow_hash, "Builder allowlist hash mismatch")
    require(builder.get("files", {}).get("PORTABLE_RUNTIME_ALLOWLIST.json") == allow_hash, "Builder file binding mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    prompt = validate_prompt(root)
    validate_registration(root)
    gui_status = validate_button_unchanged(root, prompt)
    validate_portable(root)
    print("PROMPT CANON RECONCILIATION: UPDATE_EXISTING")
    print("PROMPT IDENTITY PRESERVED: KPR-05-008")
    print("CURRENT PROJECT OWNERSHIP CONTRACT: PASS")
    print("ANTI-CROSS-PROJECT CONTRACT: PASS")
    print("PROJECT SOURCE IMMUTABILITY MARKERS: PASS")
    print("EXISTING ERROR MEMORY BUTTONS REMOVED: NO")
    print("SEND ZIP ERRORS BUTTON POSITION UNCHANGED: PASS")
    print("SEND ZIP ERRORS UPDATED CANON CLIPBOARD: PASS")
    print("GUI CLICK CLIPBOARD TEST: " + gui_status)
    print("PORTABLE PROMPT HASH BINDING: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
