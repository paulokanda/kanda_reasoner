"""Focused validator for the Web AI first-time help feature."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "web-ai-first-time-help-v1"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a required UTF-8 file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate the Web AI Help button, page, layout, and assets."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    shell = root / "kanda_reasoner_app" / "reasoner_tools_gui_shell"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    source = read_text(help_root / "source" / "web_ai.md")
    html = read_text(help_root / "rendered" / "web_ai.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    fallback = json.loads(
        read_text(
            root
            / "kanda_reasoner_app"
            / "reasoner_tools_gui_help"
            / "web_ai.json"
        )
    )
    manifest = json.loads(read_text(help_root / "manifest.json"))

    title_index = tool_specs.index('step_title="Web AI"')
    spec_start = tool_specs.rfind("ToolSpec(", 0, title_index)
    next_spec = tool_specs.find("\n    ToolSpec(", title_index)
    require(spec_start >= 0 and next_spec >= 0, "Web AI ToolSpec block missing.")
    spec = tool_specs[spec_start:next_spec]
    require('help_catalog="web_ai.json"' in spec, "Web AI Help route missing.")
    require('tab_id="project_web_ai"' in spec, "Web AI internal tab ID changed.")
    print("WEB_AI_STANDARD_HELP_BUTTON: PASS")

    page = next(
        (item for item in manifest.get("pages", []) if item.get("id") == "web_ai"),
        None,
    )
    require(page is not None, "Web AI manifest page missing.")
    require(page.get("tab_id") == "project_web_ai", "Manifest tab ID mismatch.")
    require(
        page.get("legacy_help_catalog") == "web_ai.json",
        "Legacy catalog mapping mismatch.",
    )
    print("WEB_AI_HELP_MANIFEST_REGISTRATION: PASS")

    source_markers = [
        "First-Time User Tutorial",
        "What Web AI Means",
        "The Safest First-Time Workflow",
        "Selecting the Correct Project",
        "Web Model and Provider Controls",
        "Reading an Answer Correctly",
        "Shadow Preview",
        "First-Time Checklist",
        "Important Safety Boundary",
    ]
    for marker in source_markers:
        require(marker in source, f"Source marker missing: {marker}")
    print("WEB_AI_HELP_CANONICAL_SOURCE: PASS")

    html_markers = [
        'class="book-page"',
        'class="chapter-opener"',
        "First-Time User Tutorial",
        "What Web AI Means",
        "The Safest First-Time Workflow",
        "Source Quality",
        "Brain Navigator and Project Mapping",
        "Shadow Preview",
        "Important Safety Boundary",
    ]
    for marker in html_markers:
        require(marker in html, f"HTML marker missing: {marker}")
    print("WEB_AI_HELP_FIRST_TIME_CONTENT: PASS")

    require(
        "border-top: 8px solid var(--orange-rule)" in css,
        "Orange top rule contract missing.",
    )
    require(
        "background: var(--blue-chapter)" in css,
        "Blue opener contract missing.",
    )
    require(
        "width: min(100%, 7in)" in css,
        "Centered page width contract missing.",
    )
    require("margin: 24px auto" in css, "Bilateral margin contract missing.")
    require("line-height: 1.36" in css, "Body line spacing contract missing.")
    print("WEB_AI_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local-file URL loading missing.")
    require("view.setUrl" in renderer, "QWebEngineView.setUrl missing.")
    require("QTextBrowser" in renderer, "QTextBrowser fallback missing.")
    print("WEB_AI_HELP_QWEBENGINE_PRIMARY: PASS")

    expected_assets = [
        "assets/drawings/web_ai_opener_research_desk.png",
        "assets/drawings/web_ai_answer_sources_project_map.png",
        "assets/drawings/web_ai_project_scope_selection.png",
        "assets/drawings/web_ai_safety_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        asset = help_root / relative
        require(asset.is_file(), f"Asset missing: {relative}")
        require(asset.stat().st_size > 100000, f"Asset too small: {relative}")
        filename = Path(relative).name
        require(filename in source, f"Source does not use asset: {filename}")
        require(filename in html, f"HTML does not use asset: {filename}")
    print("WEB_AI_CONTEXTUAL_CARTOON_IMAGES: PASS")

    require(fallback.get("tab") == "Web AI", "Fallback catalog title mismatch.")
    require("http://" not in html and "https://" not in html, "Remote resource found.")
    print("WEB_AI_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
