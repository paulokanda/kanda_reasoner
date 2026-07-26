"""Validate the Error Memory help and aligned clipboard label."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()

    tool_specs = root / "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py"
    relocation = root / "kanda_reasoner_app/reasoner_tools_gui_shell/_lazy_tab_layout_relocation.py"
    manifest_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/manifest.json"
    source_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/error_memory.md"
    html_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/error_memory.html"
    css_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/css/book_help.css"
    image_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/assets/drawings/architecture_review_issue_catalog_library.png"
    catalog_path = root / "kanda_reasoner_app/reasoner_tools_gui_help/error_memory.json"
    renderer_path = root / "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/renderer.py"
    tab_path = root / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"

    for path in (tool_specs, relocation, manifest_path, source_path, html_path, css_path, image_path, catalog_path, renderer_path, tab_path):
        require(path.is_file(), f"Missing required file: {path}")

    tool_text = tool_specs.read_text(encoding="utf-8")
    relocation_text = relocation.read_text(encoding="utf-8")
    source_text = source_path.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")
    renderer_text = renderer_path.read_text(encoding="utf-8")
    tab_text = tab_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    require('help_catalog="error_memory.json"' in tool_text, "Error Memory help catalog is not registered")
    require('setText("Lessons to Clipboard")' in relocation_text, "Clipboard button label is not aligned")
    require("self.export_button = QPushButton('Lessons to Clipboard')" in tab_text, "Canonical Error Editor clipboard label is not updated")
    button_order = [
        "preview_buttons.addWidget(self.save_preview_button)",
        "preview_buttons.addWidget(self.copy_error_draft_button)",
        "preview_buttons.addWidget(self.clean_editor_button)",
        "preview_buttons.addWidget(self.undo_button)",
        "preview_buttons.addWidget(self.delete_button)",
        "preview_buttons.addWidget(self.export_errors_button)",
        "preview_buttons.addWidget(self.import_errors_button)",
        "preview_buttons.addWidget(self.export_button)",
    ]
    positions = [tab_text.index(item) for item in button_order]
    require(positions == sorted(positions), "Error Editor buttons are not aligned in the required left-to-right order")
    require("transfer_buttons = QHBoxLayout()" not in tab_text, "Obsolete second transfer-button row remains")
    require("Copy Complete Error Memory JSON for AI" not in relocation_text, "Old label remains in relocation owner")
    require("Lessons to Clipboard" in source_text and "Lessons to Clipboard" in html_text, "Help does not document the renamed button")
    require("Memorize Error" in source_text and "Correct with AI" in source_text, "First-time workflow coverage is incomplete")
    require("chapter-opener" in html_text and "book-page" in html_text, "Canonical HTML layout is missing")
    require("../css/book_help.css" in html_text, "Shared book CSS is not linked")
    require("architecture_review_issue_catalog_library.png" in html_text, "Local opener image is not referenced")
    require("border-top: 8px solid var(--orange-rule)" in css_text, "Orange top rule contract is missing")
    require("background: var(--blue-chapter)" in css_text, "Blue opener contract is missing")
    require("margin: 24px auto" in css_text, "Bilateral page margin contract is missing")
    require("line-height: 1.36" in css_text, "Body line-spacing contract is missing")
    require("QWebEngineView" in renderer_text and "QUrl.fromLocalFile" in renderer_text and "setUrl" in renderer_text, "Browser-grade local renderer contract is missing")
    require("QTextBrowser" in renderer_text and "setSource" in renderer_text, "Readable fallback is missing")

    pages = [page for page in manifest.get("pages", []) if page.get("id") == "error_memory"]
    require(len(pages) == 1, "Error Memory manifest registration must be unique")
    page = pages[0]
    require(page.get("legacy_help_catalog") == "error_memory.json", "Manifest catalog mismatch")
    require(page.get("source") == "source/error_memory.md", "Manifest source mismatch")
    require(page.get("rendered") == "rendered/error_memory.html", "Manifest rendered mismatch")
    require(page.get("css") == "css/book_help.css", "Manifest CSS mismatch")
    require(catalog.get("tab") == "Error Memory", "Fallback catalog mismatch")

    print("ERROR_MEMORY_BUTTON_LABEL: PASS")
    print("ERROR_MEMORY_EDITOR_BUTTON_ALIGNMENT: PASS")
    print("ERROR_MEMORY_HELP_BUTTON_ROUTE: PASS")
    print("ERROR_MEMORY_HELP_CANONICAL_SOURCE: PASS")
    print("ERROR_MEMORY_HELP_EXACT_LAYOUT: PASS")
    print("ERROR_MEMORY_HELP_QWEBENGINE_PRIMARY: PASS")
    print("ERROR_MEMORY_HELP_FIRST_TIME_CONTENT: PASS")
    print("ERROR_MEMORY_HELP_EXISTING_PNG_REUSED: PASS")
    print("VALIDATION OK: error-memory-editor-button-alignment-v1r2")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
