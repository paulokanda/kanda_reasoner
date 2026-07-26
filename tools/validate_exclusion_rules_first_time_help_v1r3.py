"""Focused validator for Exclusion Rules first-time Help."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "exclusion-rules-first-time-help-v1r3"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a required UTF-8 file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate Help routing, grounded content, layout, and artwork."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app = root / "kanda_reasoner_app"
    shell = app / "reasoner_tools_gui_shell"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    tab = read_text(shell / "ignore_rules_tab.py")
    ui = read_text(shell / "ignore_rules_tab_help" / "ui_builders.py")
    actions = read_text(shell / "ignore_rules_tab_help" / "list_actions.py")
    prefs = read_text(shell / "ignore_rules_tab_help" / "prefs_io.py")
    defaults = read_text(shell / "ignore_rules_tab_help" / "rule_defaults.py")
    source = read_text(help_root / "source" / "exclusion_rules.md")
    html = read_text(help_root / "rendered" / "exclusion_rules.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))
    fallback = json.loads(
        read_text(app / "reasoner_tools_gui_help" / "exclusion_rules.json")
    )

    title_index = tool_specs.index('step_title="Exclusion Rules"')
    spec_start = tool_specs.rfind("ToolSpec(", 0, title_index)
    next_spec = tool_specs.find("\n    ToolSpec(", title_index)
    require(spec_start >= 0 and next_spec >= 0, "Exclusion Rules ToolSpec missing.")
    spec = tool_specs[spec_start:next_spec]
    require(
        'help_catalog="exclusion_rules.json"' in spec,
        "Exclusion Rules Help route missing.",
    )
    require('tab_id="exclusion_rules"' in spec, "Internal tab ID changed.")
    print("EXCLUSION_RULES_STANDARD_HELP_BUTTON: PASS")

    require(
        "Files, folders, and extensions listed here are treated as not part"
        in tab,
        "Core exclusion meaning missing.",
    )
    require("Changes are auto-saved" in tab, "Auto-save contract missing.")
    require('QPushButton("Search")' in tab, "Search button missing.")

    scope_start = tab.index("def _refresh_project_label")
    scope_end = tab.find("\n    def ", scope_start + 5)
    if scope_end < 0:
        scope_end = len(tab)
    scope_block = tab[scope_start:scope_end]
    require(
        "fallback " in scope_block and "rules only." in scope_block,
        "Fallback scope text fragments are missing.",
    )
    require(
        "Select a project root to save exclusions for that " in scope_block
        and "project without affecting other projects." in scope_block,
        "Fallback scope guidance is missing.",
    )
    print("EXCLUSION_RULES_FALLBACK_SCOPE_TEXT: PASS")
    print("EXCLUSION_RULES_CORE_BEHAVIOR_GROUNDED: PASS")

    for marker in [
        "Add Folder (browse)",
        "Edit Folder",
        "Remove Folder",
        "Clear All Folders",
        "Add File (browse)",
        "Edit File",
        "Remove File",
        "Clear All Files",
        "Add Extension (text)",
        "Edit Extension",
        "Remove Extension",
        "Clear All Extensions",
        "Save Rules (auto-save is on - optional)",
        "Reset to Defaults (auto-saved)",
    ]:
        require(marker in ui, f"UI control missing: {marker}")
    print("EXCLUSION_RULES_VISIBLE_CONTROLS_GROUNDED: PASS")

    require("Duplicate" in actions, "Duplicate protection missing.")
    require("_save_rules()" in actions, "Action auto-save missing.")
    require("project_ignore_rules" in prefs, "Project-specific persistence missing.")
    require("_merge_with_default_rules" in prefs, "Default merge call missing.")
    require("extensions" in defaults, "Default extensions missing.")
    require("*backup*" in defaults, "Reasoner wildcard defaults missing.")
    print("EXCLUSION_RULES_PERSISTENCE_AND_DEFAULTS: PASS")

    page = next(
        (
            item
            for item in manifest.get("pages", [])
            if item.get("id") == "exclusion_rules"
        ),
        None,
    )
    require(page is not None, "Manifest page missing.")
    require(page.get("tab_id") == "exclusion_rules", "Manifest tab ID mismatch.")
    require(
        page.get("legacy_help_catalog") == "exclusion_rules.json",
        "Fallback catalog mapping mismatch.",
    )
    print("EXCLUSION_RULES_HELP_MANIFEST_REGISTRATION: PASS")

    for marker in [
        "First-Time User Tutorial",
        "What Exclusion Rules Means",
        "The Safest First-Time Workflow",
        "Project-Specific Rules",
        "Fallback Rules",
        "The Three Rule Categories",
        "Auto-Save",
        "Reset to Defaults",
        "Exclusion Does Not Mean Deletion",
        "First-Time Checklist",
    ]:
        require(marker in source, f"Source marker missing: {marker}")
    print("EXCLUSION_RULES_HELP_CANONICAL_SOURCE: PASS")

    for marker in [
        'class="book-page"',
        'class="chapter-opener"',
        "What Exclusion Rules Means",
        "The Safest First-Time Workflow",
        "The Three Rule Categories",
        "Exclusion Does Not Mean Deletion",
        "First-Time Checklist",
    ]:
        require(marker in html, f"HTML marker missing: {marker}")
    print("EXCLUSION_RULES_HELP_FIRST_TIME_CONTENT: PASS")

    require(
        "border-top: 8px solid var(--orange-rule)" in css,
        "Orange top rule missing.",
    )
    require(
        "background: var(--blue-chapter)" in css,
        "Blue opener missing.",
    )
    require(
        "width: min(100%, 7in)" in css,
        "Centered page width missing.",
    )
    require("margin: 24px auto" in css, "Bilateral margin contract missing.")
    require("line-height: 1.36" in css, "Body line spacing missing.")
    print("EXCLUSION_RULES_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local-file URL loading missing.")
    require("view.setUrl" in renderer, "QWebEngineView.setUrl missing.")
    require("QTextBrowser" in renderer, "QTextBrowser fallback missing.")
    print("EXCLUSION_RULES_HELP_QWEBENGINE_PRIMARY: PASS")

    expected_assets = [
        "assets/drawings/exclusion_rules_opener_project_filter.png",
        "assets/drawings/exclusion_rules_project_scope.png",
        "assets/drawings/exclusion_rules_rule_categories.png",
        "assets/drawings/exclusion_rules_safety_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        asset = help_root / relative
        require(asset.is_file(), f"Asset missing: {relative}")
        require(asset.stat().st_size > 100000, f"Asset too small: {relative}")
        filename = Path(relative).name
        require(filename in source, f"Source does not use asset: {filename}")
        require(filename in html, f"HTML does not use asset: {filename}")
    print("EXCLUSION_RULES_CONTEXTUAL_CARTOON_IMAGES: PASS")

    require(fallback.get("tab") == "Exclusion Rules", "Fallback title mismatch.")

    lowered_html = html.lower()
    for marker in (
        'src="http://',
        "src='http://",
        'src="https://',
        "src='https://",
        'href="http://',
        "href='http://",
        'href="https://',
        "href='https://",
    ):
        require(marker not in lowered_html, f"Remote resource found: {marker}")
    print("EXCLUSION_RULES_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
