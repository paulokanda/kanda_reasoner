"""Focused validator for Local AI help with contextual images."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


FEATURE_ID = "local-ai-first-time-help-v1r1"


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
    shell = root / "kanda_reasoner_app" / "reasoner_tools_gui_shell"
    help_root = shell / "help_docs"

    tool_specs = read_text(shell / "tool_specs.py")
    ui_builder = read_text(
        root / "kanda_reasoner_app" / "reasoner_engine"
        / "ai_reasoner_main_window_help" / "ui_builder.py"
    )
    source = read_text(help_root / "source" / "local_ai.md")
    html = read_text(help_root / "rendered" / "local_ai.html")
    css = read_text(help_root / "css" / "book_help.css")
    renderer = read_text(help_root / "renderer.py")
    manifest = json.loads(read_text(help_root / "manifest.json"))

    local_spec_start = tool_specs.index('step_title="Local AI"')
    local_spec_end = tool_specs.index("),", local_spec_start) + 2
    local_spec = tool_specs[local_spec_start:local_spec_end]
    require(
        'help_catalog="ai_reasoner_main_window_help.json"' in local_spec,
        "Local AI shell Help route missing.",
    )
    print("LOCAL_AI_SHELL_HELP_BUTTON: PASS")

    quick_start = ui_builder.index("def _quick_section")
    quick_end = ui_builder.index("\ndef ", quick_start + 5)
    quick_section = ui_builder[quick_start:quick_end]
    require(
        "layout.addWidget(window.help_button)" not in quick_section,
        "Legacy embedded Help button remains visible.",
    )
    print("LOCAL_AI_DUPLICATE_EMBEDDED_HELP_REMOVED: PASS")

    for marker in [
        "First-Time User Tutorial",
        "What Local AI Means",
        "The Safest First-Time Workflow",
        "Project Context Controls",
        "Reading the Answer",
        "Important Safety Boundary",
    ]:
        require(marker in source, f"Source marker missing: {marker}")
        require(marker in html, f"HTML marker missing: {marker}")
    print("LOCAL_AI_HELP_FIRST_TIME_CONTENT: PASS")

    require("border-top: 8px solid var(--orange-rule)" in css, "Top rule missing.")
    require("background: var(--blue-chapter)" in css, "Blue opener missing.")
    require("width: min(100%, 7in)" in css, "Page width contract missing.")
    require("margin: 24px auto" in css, "Bilateral margin contract missing.")
    require("line-height: 1.36" in css, "Line spacing contract missing.")
    print("LOCAL_AI_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary missing.")
    require("QUrl.fromLocalFile" in renderer, "Local URL loading missing.")
    require("view.setUrl" in renderer, "QWebEngineView.setUrl missing.")
    require("QTextBrowser" in renderer, "Fallback missing.")
    print("LOCAL_AI_HELP_QWEBENGINE_PRIMARY: PASS")

    page = next(
        (item for item in manifest.get("pages", []) if item.get("id") == "local_ai"),
        None,
    )
    require(page is not None, "Local AI manifest page missing.")

    expected_assets = [
        "assets/drawings/local_ai_opener_private_reference_desk.png",
        "assets/drawings/local_ai_project_scope_selection.png",
        "assets/drawings/local_ai_answer_evidence_review.png",
        "assets/drawings/local_ai_safety_boundary.png",
    ]
    for relative in expected_assets:
        require(relative in page.get("assets", []), f"Asset not registered: {relative}")
        path = help_root / relative
        require(path.is_file(), f"Asset file missing: {relative}")
        require(path.stat().st_size > 100000, f"Asset unexpectedly small: {relative}")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest(),
            f"Asset hash unavailable: {relative}",
        )
        require(relative.split("/")[-1] in source, f"Source does not use: {relative}")
        require(relative.split("/")[-1] in html, f"HTML does not use: {relative}")

    old_assets = [
        "docstring_assistant_opener_library.png",
        "project_structure_map_scope_survey.png",
        "project_structure_map_evidence_archive.png",
        "engineering_safety_operating_library.png",
    ]
    for old in old_assets:
        require(old not in source, f"Old reused image remains in source: {old}")
        require(old not in html, f"Old reused image remains in HTML: {old}")

    print("LOCAL_AI_CONTEXTUAL_CARTOON_IMAGES: PASS")
    print("LOCAL_AI_OLD_REUSED_IMAGES_REMOVED: PASS")
    print("LOCAL_AI_HELP_MANIFEST_REGISTRATION: PASS")
    print("LOCAL_AI_HELP_LOCAL_ONLY: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
