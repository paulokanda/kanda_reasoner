"""Validate Project Structure 3D first-time Help."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "project-structure-3d-first-time-help-v1"


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
    visualizer = app / "project_structure_visualizer"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    tab = read_text(visualizer / "project_structure_3d_tab.py")
    ui = read_text(visualizer / "tab_ui_builder.py")
    visualizer_ui = tab + "\n" + ui
    navigation = read_text(visualizer / "tab_navigation_mixin.py")
    evidence = read_text(visualizer / "tab_evidence_mixin.py")
    source = read_text(help_root / "source" / "project_structure_3d.md")
    html = read_text(help_root / "rendered" / "project_structure_3d.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))
    fallback = json.loads(
        read_text(app / "reasoner_tools_gui_help" / "project_structure_3d.json")
    )

    title_index = tool_specs.index('step_title="Project Structure 3D"')
    start = tool_specs.rfind("ToolSpec(", 0, title_index)
    end = tool_specs.find("\n    ToolSpec(", title_index)
    require(start >= 0 and end >= 0, "Project Structure 3D ToolSpec missing.")
    spec = tool_specs[start:end]
    require(
        'help_catalog="project_structure_3d.json"' in spec,
        "Shell Help route missing.",
    )
    require('tab_id="project_structure_3d"' in spec, "Tab ID changed.")
    print("PROJECT_STRUCTURE_3D_STANDARD_HELP_BUTTON: PASS")

    require(
        'widget.project_structure_help_button = QPushButton("Help")' in visualizer_ui,
        "Embedded Help button missing.",
    )
    require(
        "toolbar.addWidget(widget.project_label)" in ui
        and "toolbar.addWidget(widget.project_structure_help_button)" in ui
        and ui.index("toolbar.addWidget(widget.project_structure_help_button)")
        > ui.index("toolbar.addWidget(widget.project_label)"),
        "Embedded Help button is not after the project label.",
    )
    require(
        "open_help_document_for_legacy_catalog" in tab
        and '"project_structure_3d.json"' in tab,
        "Embedded Help route missing.",
    )
    print("PROJECT_STRUCTURE_3D_INLINE_HELP_AFTER_PROJECT: PASS")
    print("PROJECT_STRUCTURE_3D_INLINE_HELP_CANONICAL_ROUTE: PASS")

    for marker in [
        'QLabel("READ-ONLY FIXTURE")',
        'QLabel("Project: not selected")',
        'addItem("Architecture", "architecture")',
        'addItem("Structure", "structure")',
        'QCheckBox("Imports")',
        'QCheckBox("External")',
        'QCheckBox("Symbols")',
        'QCheckBox("Semantic")',
        'QPushButton("Refresh evidence")',
        'QPushButton("Search")',
        'QPushButton("Fit graph")',
        'QPushButton("Reset camera")',
        'QPushButton("Open in browser")',
    ]:
        require(marker in visualizer_ui, f"Visible control missing: {marker}")
    print("PROJECT_STRUCTURE_3D_VISIBLE_CONTROLS_GROUNDED: PASS")

    require("Back" in navigation, "Back navigation missing.")
    require("Forward" in navigation, "Forward navigation missing.")
    require("Overview" in navigation, "Overview navigation missing.")
    require("Isolate" in navigation, "Isolate navigation missing.")
    require("Path to search" in navigation, "Path-to-search navigation missing.")
    require("Loading canonical Project evidence" in evidence, "Evidence loading contract missing.")
    require("Fixture fallback" in tab, "Fixture contract missing.")
    print("PROJECT_STRUCTURE_3D_NAVIGATION_AND_EVIDENCE: PASS")

    page = next(
        (p for p in manifest.get("pages", []) if p.get("id") == "project_structure_3d"),
        None,
    )
    require(page is not None, "Manifest page missing.")
    require(page.get("tab_id") == "project_structure_3d", "Manifest tab mismatch.")
    require(
        page.get("legacy_help_catalog") == "project_structure_3d.json",
        "Fallback mapping mismatch.",
    )
    print("PROJECT_STRUCTURE_3D_HELP_MANIFEST_REGISTRATION: PASS")

    for marker in [
        "First-Time User Tutorial",
        "What Project Structure 3D Means",
        "Fixture Versus Live Project Evidence",
        "Project JSON Controls",
        "Architecture and Structure Modes",
        "Filters",
        "Open in Browser",
        "Navigation Bar",
        "Renderer Status",
        "Read-Only Safety Boundary",
        "First-Time Checklist",
    ]:
        require(marker in source, f"Source marker missing: {marker}")
    print("PROJECT_STRUCTURE_3D_HELP_CANONICAL_SOURCE: PASS")

    for marker in [
        'class="book-page"',
        'class="chapter-opener"',
        "Fixture Versus Live Project Evidence",
        "Project JSON Controls",
        "Architecture and Structure Modes",
        "Read-Only Safety Boundary",
        "First-Time Checklist",
    ]:
        require(marker in html, f"HTML marker missing: {marker}")
    print("PROJECT_STRUCTURE_3D_HELP_FIRST_TIME_CONTENT: PASS")

    require("border-top: 8px solid var(--orange-rule)" in css, "Orange rule missing.")
    require("background: var(--blue-chapter)" in css, "Blue opener missing.")
    require("width: min(100%, 7in)" in css, "Page width missing.")
    require("margin: 24px auto" in css, "Page margins missing.")
    print("PROJECT_STRUCTURE_3D_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local help loading missing.")
    require("QTextBrowser" in renderer, "Text fallback missing.")
    print("PROJECT_STRUCTURE_3D_HELP_QWEBENGINE_PRIMARY: PASS")

    expected_assets = [
        "assets/drawings/project_structure_3d_opener_city_map.png",
        "assets/drawings/project_structure_3d_evidence_layers.png",
        "assets/drawings/project_structure_3d_navigation_filters.png",
        "assets/drawings/project_structure_3d_read_only_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        asset = help_root / relative
        require(asset.is_file(), f"Asset missing: {relative}")
        require(asset.stat().st_size > 100000, f"Asset too small: {relative}")
        name = Path(relative).name
        require(name in source, f"Source asset missing: {name}")
        require(name in html, f"HTML asset missing: {name}")
    print("PROJECT_STRUCTURE_3D_CONTEXTUAL_CARTOON_IMAGES: PASS")

    require(fallback.get("tab") == "Project Structure 3D", "Fallback title mismatch.")
    lowered = html.lower()
    for marker in (
        'src="http://', "src='http://", 'src="https://', "src='https://",
        'href="http://', "href='http://", 'href="https://', "href='https://",
    ):
        require(marker not in lowered, f"Remote help resource found: {marker}")
    print("PROJECT_STRUCTURE_3D_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
