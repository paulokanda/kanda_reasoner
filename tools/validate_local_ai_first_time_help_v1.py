"""Focused validator for the Local AI first-time help feature."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "local-ai-first-time-help-v1"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic error when a contract is not met."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read a required UTF-8 text file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate Local AI shell help routing and help content."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    shell = root / "kanda_reasoner_app" / "reasoner_tools_gui_shell"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    ui_builder = read_text(
        root
        / "kanda_reasoner_app"
        / "reasoner_engine"
        / "ai_reasoner_main_window_help"
        / "ui_builder.py"
    )
    source = read_text(help_root / "source" / "local_ai.md")
    html = read_text(help_root / "rendered" / "local_ai.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))

    local_spec_start = tool_specs.index('step_title="Local AI"')
    next_spec = tool_specs.find("    ToolSpec(", local_spec_start + 1)
    local_spec = (
        tool_specs[local_spec_start:]
        if next_spec < 0
        else tool_specs[local_spec_start:next_spec]
    )
    require(
        'help_catalog="ai_reasoner_main_window_help.json"' in local_spec,
        "Local AI ToolSpec does not expose the shell Help route.",
    )
    print("LOCAL_AI_SHELL_HELP_BUTTON: PASS")

    quick_start = ui_builder.index("def _quick_section")
    quick_end = ui_builder.index("\ndef ", quick_start + 5)
    quick_section = ui_builder[quick_start:quick_end]
    require(
        "layout.addWidget(window.help_button)" not in quick_section,
        "Legacy embedded Help button remains visible in Quick questions.",
    )
    print("LOCAL_AI_DUPLICATE_EMBEDDED_HELP_REMOVED: PASS")

    source_markers = [
        "First-Time User Tutorial",
        "What Local AI Means",
        "The Safest First-Time Workflow",
        "Project Context Controls",
        "Local Runtime Controls",
        "Conversations and Memory",
        "What Local AI Can and Cannot Prove",
        "If Something Goes Wrong",
        "First-Time Checklist",
    ]
    for marker in source_markers:
        require(marker in source, f"Source marker missing: {marker}")
    print("LOCAL_AI_HELP_CANONICAL_SOURCE: PASS")

    html_markers = [
        'class="book-page"',
        'class="chapter-opener"',
        "First-Time User Tutorial",
        "What Local AI Means",
        "The Safest First-Time Workflow",
        "Project Context Controls",
        "Local Runtime Controls",
        "Quick Questions",
        "Reading the Answer",
        "Important Safety Boundary",
    ]
    for marker in html_markers:
        require(marker in html, f"HTML marker missing: {marker}")
    print("LOCAL_AI_HELP_FIRST_TIME_CONTENT: PASS")

    require(
        "border-top: 8px solid var(--orange-rule)" in css,
        "Orange-red top rule contract missing.",
    )
    require(
        "background: var(--blue-chapter)" in css,
        "Dark-blue chapter opener contract missing.",
    )
    require(
        "width: min(100%, 7in)" in css,
        "Centered seven-inch page contract missing.",
    )
    require(
        "margin: 24px auto" in css,
        "Bilateral margin contract missing.",
    )
    require("line-height: 1.36" in css, "Body line spacing contract missing.")
    print("LOCAL_AI_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local-file URL loading missing.")
    require("view.setUrl" in renderer, "QWebEngineView.setUrl missing.")
    require("QTextBrowser" in renderer, "QTextBrowser fallback missing.")
    print("LOCAL_AI_HELP_QWEBENGINE_PRIMARY: PASS")

    page = next(
        (
            item
            for item in manifest.get("pages", [])
            if item.get("id") == "local_ai"
        ),
        None,
    )
    require(page is not None, "Local AI manifest page missing.")
    require(page.get("tab_id") == "project_qa", "Local AI tab ID mismatch.")
    require(
        page.get("legacy_help_catalog")
        == "ai_reasoner_main_window_help.json",
        "Local AI legacy catalog mapping mismatch.",
    )
    expected_assets = [
        "assets/drawings/docstring_assistant_opener_library.png",
        "assets/drawings/project_structure_map_scope_survey.png",
        "assets/drawings/project_structure_map_evidence_archive.png",
        "assets/drawings/engineering_safety_operating_library.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        require((help_root / relative).is_file(), f"Asset file missing: {relative}")
    print("LOCAL_AI_HELP_MANIFEST_REGISTRATION: PASS")
    print("LOCAL_AI_HELP_EXISTING_PNG_REUSED: PASS")

    require("http://" not in html and "https://" not in html, "Remote resource found.")
    print("LOCAL_AI_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
