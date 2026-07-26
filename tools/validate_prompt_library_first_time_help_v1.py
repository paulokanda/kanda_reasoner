"""Validate Prompt Library first-time Help."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "prompt-library-first-time-help-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    app = root / "kanda_reasoner_app"
    shell = app / "reasoner_tools_gui_shell"
    prompt_gui = app / "prompt_library_gui"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    tab = read_text(prompt_gui / "prompt_library_tab.py")
    group_window = read_text(prompt_gui / "group_window.py")
    library_catalog = read_text(prompt_gui / "library_catalog.py")
    library_paths = read_text(prompt_gui / "library_paths.py")
    group_catalog = read_text(prompt_gui / "group_catalog.py")
    source = read_text(help_root / "source" / "prompt_library.md")
    html = read_text(help_root / "rendered" / "prompt_library.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))
    fallback = json.loads(
        read_text(app / "reasoner_tools_gui_help" / "prompt_library.json")
    )

    title_index = tool_specs.index('step_title="Prompt Library"')
    start = tool_specs.rfind("ToolSpec(", 0, title_index)
    end = tool_specs.find("\n    ToolSpec(", title_index)
    if end < 0:
        end = len(tool_specs)
    require(start >= 0, "Prompt Library ToolSpec missing.")
    spec = tool_specs[start:end]
    require('help_catalog="prompt_library.json"' in spec, "Shell Help route missing.")
    require('tab_id="prompt_library"' in spec, "Tab ID changed.")
    print("PROMPT_LIBRARY_STANDARD_HELP_BUTTON: PASS")

    require(
        'self.prompt_library_help_button = QPushButton("Help")' in tab,
        "Embedded Help button missing.",
    )
    reload_marker = "button_row.addWidget(self.reload_button)"
    help_marker = "button_row.addWidget(self.prompt_library_help_button)"
    require(reload_marker in tab and help_marker in tab, "Button-row markers missing.")
    require(tab.index(help_marker) > tab.index(reload_marker), "Help is not after Reload.")
    require(
        "open_help_document_for_legacy_catalog" in tab
        and '"prompt_library.json"' in tab,
        "Embedded canonical Help route missing.",
    )
    print("PROMPT_LIBRARY_INLINE_HELP_AFTER_RELOAD: PASS")
    print("PROMPT_LIBRARY_INLINE_HELP_CANONICAL_ROUTE: PASS")

    for marker in [
        'QPushButton("Reload Canonical Library")',
        "PromptGroupDashboard()",
        "open_group_window",
        "canonical workspace",
        "legacy compatibility fallback",
        "Deprecated and retired entries are hidden.",
    ]:
        require(marker in tab, f"Main behavior missing: {marker}")
    print("PROMPT_LIBRARY_DASHBOARD_BEHAVIOR_GROUNDED: PASS")

    for marker in [
        'QPushButton("Copy Selected Prompt")',
        'QPushButton("Copy Full Group Stack")',
        'QPushButton("Open File Location")',
        'QPushButton("Close")',
        "metadata_view",
        "preview",
        "Copied prompt text:",
        "Copied full group stack:",
    ]:
        require(marker in group_window, f"Group-window control missing: {marker}")
    print("PROMPT_LIBRARY_GROUP_WINDOW_CONTROLS: PASS")

    for marker in [
        '"archived"',
        '"deprecated"',
        '"inactive"',
        '"retired"',
        '"superseded"',
        'load_type == "never"',
        'selected_root / "ACTIVE_PROMPTS"',
    ]:
        require(marker in library_catalog, f"Current-only rule missing: {marker}")
    require("canonical_prompt_library_root" in library_paths, "Canonical path missing.")
    require("legacy_prompt_library_root" in library_paths, "Legacy path missing.")
    require("_ordered_current_prompt_ids" in group_catalog, "Group reconciliation missing.")
    require("build_group_stack_text" in group_catalog, "Group stack builder missing.")
    print("PROMPT_LIBRARY_CURRENT_ONLY_AND_RECONCILIATION: PASS")

    page = next(
        (item for item in manifest.get("pages", []) if item.get("id") == "prompt_library"),
        None,
    )
    require(page is not None, "Manifest page missing.")
    require(page.get("tab_id") == "prompt_library", "Manifest tab mismatch.")
    require(
        page.get("legacy_help_catalog") == "prompt_library.json",
        "Fallback mapping mismatch.",
    )
    print("PROMPT_LIBRARY_HELP_MANIFEST_REGISTRATION: PASS")

    for marker in [
        "First-Time User Tutorial",
        "What Prompt Library Means",
        "Canonical Workspace and Legacy Fallback",
        "Current Prompts Only",
        "Reload Canonical Library",
        "The Group Cube Dashboard",
        "The Group Window",
        "Copy Selected Prompt",
        "Copy Full Group Stack",
        "Read-Only Governance Boundary",
        "First-Time Checklist",
    ]:
        require(marker in source, f"Source marker missing: {marker}")
    print("PROMPT_LIBRARY_HELP_CANONICAL_SOURCE: PASS")

    for marker in [
        'class="book-page"',
        'class="chapter-opener"',
        "Canonical Workspace and Legacy Fallback",
        "The Group Cube Dashboard",
        "Read-Only Governance Boundary",
        "First-Time Checklist",
    ]:
        require(marker in html, f"HTML marker missing: {marker}")
    print("PROMPT_LIBRARY_HELP_FIRST_TIME_CONTENT: PASS")

    require("border-top: 8px solid var(--orange-rule)" in css, "Orange rule missing.")
    require("background: var(--blue-chapter)" in css, "Blue opener missing.")
    require("width: min(100%, 7in)" in css, "Page width missing.")
    require("margin: 24px auto" in css, "Page margins missing.")
    print("PROMPT_LIBRARY_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngine primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local help loading missing.")
    require("QTextBrowser" in renderer, "Text fallback missing.")
    print("PROMPT_LIBRARY_HELP_QWEBENGINE_PRIMARY: PASS")

    expected_assets = [
        "assets/drawings/prompt_library_opener_canonical_vault.png",
        "assets/drawings/prompt_library_active_group_cubes.png",
        "assets/drawings/prompt_library_group_browser.png",
        "assets/drawings/prompt_library_read_only_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        asset = help_root / relative
        require(asset.is_file(), f"Asset missing: {relative}")
        require(asset.stat().st_size > 100000, f"Asset too small: {relative}")
        name = Path(relative).name
        require(name in source, f"Source asset missing: {name}")
        require(name in html, f"HTML asset missing: {name}")
    print("PROMPT_LIBRARY_CONTEXTUAL_CARTOON_IMAGES: PASS")

    require(fallback.get("tab") == "Prompt Library", "Fallback title mismatch.")
    lowered = html.lower()
    for marker in (
        'src="http://', "src='http://", 'src="https://', "src='https://",
        'href="http://', "href='http://", 'href="https://', "href='https://",
    ):
        require(marker not in lowered, f"Remote resource found: {marker}")
    print("PROMPT_LIBRARY_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
