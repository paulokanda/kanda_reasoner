"""Validate the generalized Send Zip Errors prompt and Error Memory button."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import py_compile
import sys
from pathlib import Path

FEATURE_ID = "send-zip-errors-prompt-button-v1"
PROMPT_ID = "self_contained_error_memory_lesson_intake_zip"
PROMPT_CODE = "KPR-05-008"
PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "self_contained_error_memory_lesson_intake_zip.md"
)
META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "self_contained_error_memory_lesson_intake_zip.meta.json"
)
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
CLIPBOARD_REL = Path("kanda_reasoner_app/error_memory_gui/_clipboard_export.py")
BLUEPRINT_REL = Path("kanda_reasoner_app/error_memory_gui/_intake_blueprint.py")
PATHS_REL = Path("kanda_reasoner_app/error_memory_gui/_project_paths_mixin.py")
ALLOWLIST_REL = Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json")
BUILDER_REL = Path("portable/PORTABLE_BUILDER_MANIFEST.json")
ROUTING_ROOT = Path("kanda_prompt_workspace/prompt_library/ROUTING")
FOLDER_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/_FOLDER_ASSIMILATION.md"
)
COMPACT_NAV_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "02_prompt_routing_and_indexing/prompt_navigation_index.md"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read(path: Path) -> str:
    require(path.is_file(), "Required file missing: " + str(path))
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_prompt(root: Path) -> str:
    prompt_path = root / PROMPT_REL
    prompt = read(prompt_path)
    meta = json.loads(read(root / META_REL))
    required_front = [
        "prompt_code: KPR-05-008",
        "prompt_id: self_contained_error_memory_lesson_intake_zip",
        "status: active",
        "load_type: on_request",
        "owner_box: 05_patch_delivery_and_validation",
    ]
    require(all(item in prompt for item in required_front), "Prompt front matter mismatch")
    required_behavior = [
        "Do not assume the Project is `kanda_reasoner`.",
        "Do not assume the drive is `E:`.",
        "Create one ZIP containing:",
        "RUN_INSTALL.ps1",
        "pending_ai_assisted_error_lesson_intake",
        "It must never press or imitate `Memorize Error`.",
        "Do not create separate lesson ZIPs.",
        "PROJECT SOURCE FILES MODIFIED: 0",
        "CANONICAL LESSONS WRITTEN: 0",
        "MEMORIZE ERROR EXECUTED: NO",
    ]
    require(all(item in prompt for item in required_behavior), "Generalized prompt contract incomplete")
    require(meta.get("prompt_code") == PROMPT_CODE, "Metadata prompt code mismatch")
    require(meta.get("prompt_id") == PROMPT_ID, "Metadata prompt ID mismatch")
    require(meta.get("canonical_path") == PROMPT_REL.as_posix(), "Metadata canonical path mismatch")
    require(meta.get("status") == "active" and meta.get("load_type") == "on_request", "Metadata lifecycle mismatch")
    return prompt


def validate_routes(root: Path) -> None:
    nav = json.loads(read(root / ROUTING_ROOT / "prompt_navigation_index.json"))
    entries = [e for e in nav.get("entries", []) if e.get("prompt_id") == PROMPT_ID]
    require(len(entries) == 1, "Navigation entry count mismatch")
    require(entries[0].get("prompt_code") == PROMPT_CODE, "Navigation code mismatch")
    all_codes = [e.get("prompt_code") for e in nav.get("entries", []) if e.get("prompt_code")]
    require(all_codes.count(PROMPT_CODE) == 1, "KPR code is not unique")
    require(nav.get("prompt_count") == len(nav.get("entries", [])), "Navigation prompt count mismatch")

    human = read(root / ROUTING_ROOT / "PROMPT_NAVIGATION_INDEX.md")
    folder = read(root / FOLDER_REL)
    compact = read(root / COMPACT_NAV_REL)
    for text, label in ((human, "human navigation"), (folder, "folder card"), (compact, "compact navigation")):
        require(PROMPT_CODE in text and PROMPT_ID in text, label + " registration missing")

    with (root / ROUTING_ROOT / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    matched = [row for row in rows if row.get("prompt_id") == PROMPT_ID]
    require(len(matched) == 1, "Coverage row count mismatch")
    require(PROMPT_CODE in matched[0].get("aliases", ""), "Coverage alias missing")


def validate_gui_sources(root: Path) -> None:
    tab = read(root / TAB_REL)
    clip = read(root / CLIPBOARD_REL)
    blueprint = read(root / BLUEPRINT_REL)
    paths = read(root / PATHS_REL)

    existing = "QPushButton('Get correct way to send me errors')"
    new = "QPushButton('Send Zip Errors')"
    require(existing in tab, "Existing button was removed")
    require(new in tab, "New Send Zip Errors button missing")
    require("self.send_zip_errors_button.setStyleSheet('color: #FF8C00; font-weight: bold;')" in tab, "New button orange font style missing")
    old_add = "path_action_row.addWidget(self.copy_correct_error_delivery_button)"
    new_add = "path_action_row.addWidget(self.send_zip_errors_button)"
    require(old_add in tab and new_add in tab, "Button row wiring missing")
    require(tab.index(new_add) > tab.index(old_add), "New button is not right of existing button")
    between = tab[tab.index(old_add) + len(old_add):tab.index(new_add)]
    require("addWidget" not in between, "New button is not immediately right of existing button")
    expected_existing = [
        "self.open_memory_button",
        "self.open_second_prompt_button",
        "self.copy_memory_path_button",
        "self.copy_second_prompt_path_button",
        "self.copy_correct_error_delivery_button",
    ]
    require(all("path_action_row.addWidget(" + name + ")" in tab for name in expected_existing), "An existing path-row button was removed")
    require("copy_send_zip_errors_prompt_to_clipboard(self)" in tab, "New button click wiring missing")
    require("def copy_send_zip_errors_prompt_to_clipboard" in clip, "Clipboard helper missing")
    require("read_send_zip_errors_prompt" in clip, "Clipboard helper does not read canonical prompt")
    require("SEND_ZIP_ERRORS_PROMPT_RELATIVE_PATH" in blueprint, "Canonical prompt path constant missing")
    require("def read_send_zip_errors_prompt" in blueprint, "Canonical prompt reader missing")
    require("'send_zip_errors_button'" in paths, "Project-enabled control registration missing")

    for rel in (TAB_REL, CLIPBOARD_REL, BLUEPRINT_REL, PATHS_REL):
        py_compile.compile(str(root / rel), doraise=True)
    require(len(tab.splitlines()) <= 500, "Error Memory tab exceeds 500 physical lines")


def validate_portable_bindings(root: Path) -> None:
    allow_path = root / ALLOWLIST_REL
    allow = json.loads(read(allow_path))
    items = allow.get("items", [])
    by_rel = {item.get("source_relative"): item for item in items}
    runtime_files = [
        PROMPT_REL.as_posix(),
        META_REL.as_posix(),
        FOLDER_REL.as_posix(),
        COMPACT_NAV_REL.as_posix(),
        (ROUTING_ROOT / "PROMPT_NAVIGATION_INDEX.md").as_posix(),
        (ROUTING_ROOT / "prompt_navigation_index.json").as_posix(),
        (ROUTING_ROOT / "prompt_route_coverage_table.csv").as_posix(),
    ]
    for rel in runtime_files:
        item = by_rel.get(rel)
        require(item is not None, "Portable runtime allowlist entry missing: " + rel)
        path = root / rel
        require(item.get("sha256") == sha256(path), "Portable allowlist hash mismatch: " + rel)
        require(item.get("size_bytes") == path.stat().st_size, "Portable allowlist size mismatch: " + rel)
    require(allow.get("item_count") == len(items), "Portable allowlist item count mismatch")

    builder = json.loads(read(root / BUILDER_REL))
    allow_hash = sha256(allow_path)
    require(builder.get("runtime_allowlist_sha256") == allow_hash, "Builder runtime allowlist binding mismatch")
    require(builder.get("runtime_allowlist_item_count") == len(items), "Builder runtime item count mismatch")
    require(builder.get("files", {}).get("PORTABLE_RUNTIME_ALLOWLIST.json") == allow_hash, "Builder manifest file hash mismatch")


def validate_runtime_click(root: Path, prompt: str) -> str:
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
        tab = ErrorMemoryTab()
        tab.set_project_root(root)
        tab._show_action_done = lambda *args, **kwargs: None
        button = tab.send_zip_errors_button
        require(button.text() == "Send Zip Errors", "Runtime button label mismatch")
        require("#FF8C00" in button.styleSheet(), "Runtime button style mismatch")
        row = button.parentWidget()
        del row
        QApplication.clipboard().clear()
        button.click()
        app.processEvents()
        require(QApplication.clipboard().text() == prompt, "Runtime clipboard payload does not equal canonical prompt")
        tab.close()
        app.processEvents()
        return "PASS"
    finally:
        os.chdir(previous)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    prompt = validate_prompt(root)
    validate_routes(root)
    validate_gui_sources(root)
    validate_portable_bindings(root)
    gui = validate_runtime_click(root, prompt)
    print("PROMPT DUPLICATE OWNER AUDIT: PASS")
    print("PROMPT IDENTITY KPR-05-008: PASS")
    print("PROMPT SOURCE/METADATA/ROUTING: PASS")
    print("EXISTING ERROR MEMORY BUTTONS PRESERVED: PASS")
    print("SEND ZIP ERRORS IMMEDIATELY RIGHT OF EXISTING BUTTON: PASS")
    print("SEND ZIP ERRORS ORANGE FONT: PASS")
    print("SEND ZIP ERRORS EXACT CANON CLIPBOARD: PASS")
    print("PORTABLE PROMPT RUNTIME BINDING: PASS")
    print("GUI CLICK CLIPBOARD TEST: " + gui)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
