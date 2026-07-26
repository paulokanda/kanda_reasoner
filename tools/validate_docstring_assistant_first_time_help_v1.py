"""Focused validator for the Docstring Assistant first-time help update."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FEATURE_ID = "docstring-assistant-first-time-help-v1"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic validation error when a contract fails."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read one UTF-8 text file."""
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    """Validate the installed Docstring Assistant help files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    help_root = (
        root
        / "kanda_reasoner_app"
        / "reasoner_tools_gui_shell"
        / "help_docs"
    )
    source_path = help_root / "source" / "docstring_assistant.md"
    html_path = help_root / "rendered" / "docstring_assistant.html"
    css_path = help_root / "css" / "book_help.css"
    manifest_path = help_root / "manifest.json"
    renderer_path = help_root / "renderer.py"

    source = read_text(source_path)
    html = read_text(html_path)
    css = read_text(css_path)
    renderer = read_text(renderer_path)
    manifest = json.loads(read_text(manifest_path))

    source_markers = [
        "First-Time User Tutorial",
        "What Is a Docstring?",
        "The Safest First-Time Workflow",
        "Scan, Diff, and Write Explained",
        "Common Mistakes",
        "If Something Goes Wrong",
        "First-Time Checklist",
        "Scan first, review one draft",
    ]
    for marker in source_markers:
        require(marker in source, f"Source marker missing: {marker}")
    print("DOCSTRING_HELP_CANONICAL_SOURCE: PASS")

    html_markers = [
        'class="book-page"',
        'class="chapter-opener"',
        "First-Time User Tutorial",
        "What Is a Docstring?",
        "The Safest First-Time Workflow",
        "Run Options",
        "AI Assistance",
        "The Report Area",
        "Review and Correct Missing Docstrings",
        "If Something Goes Wrong",
        "Important Safety Boundary",
    ]
    for marker in html_markers:
        require(marker in html, f"HTML marker missing: {marker}")
    print("DOCSTRING_HELP_FIRST_TIME_CONTENT: PASS")

    require("border-top: 8px solid var(--orange-rule)" in css, "Top rule missing")
    require("background: var(--blue-chapter)" in css, "Blue opener missing")
    require("width: min(100%, 7in)" in css, "Centered page width missing")
    require("margin: 24px auto" in css, "Bilateral margin contract missing")
    require("line-height: 1.36" in css, "Body line spacing missing")
    print("DOCSTRING_HELP_EXACT_LAYOUT: PASS")

    require("QWebEngineView" in renderer, "QWebEngineView primary renderer missing")
    require("QUrl.fromLocalFile" in renderer, "Local HTML URL loading missing")
    require("view.setUrl" in renderer, "QWebEngineView setUrl missing")
    require("QTextBrowser" in renderer, "QTextBrowser fallback missing")
    print("DOCSTRING_HELP_QWEBENGINE_PRIMARY: PASS")

    pages = manifest.get("pages", [])
    page = next(
        (item for item in pages if item.get("id") == "docstring_assistant"),
        None,
    )
    require(page is not None, "Manifest page is missing")
    require(
        page.get("source") == "source/docstring_assistant.md",
        "Manifest source path mismatch",
    )
    require(
        page.get("rendered") == "rendered/docstring_assistant.html",
        "Manifest rendered path mismatch",
    )
    assets = page.get("assets", [])
    expected_assets = [
        "assets/drawings/docstring_assistant_opener_library.png",
        "assets/drawings/docstring_assistant_scan_post_room.png",
        "assets/drawings/docstring_assistant_ai_copy_shop.png",
        "assets/drawings/docstring_assistant_review_tailor.png",
        "assets/drawings/docstring_assistant_report_clerk.png",
    ]
    for relative in expected_assets:
        require(relative in assets, f"Manifest asset missing: {relative}")
        require((help_root / relative).is_file(), f"Asset file missing: {relative}")
    print("DOCSTRING_HELP_EXISTING_PNG_REUSED: PASS")
    print("DOCSTRING_HELP_MANIFEST_REGISTRATION: PASS")

    require("http://" not in html and "https://" not in html, "Remote resource found")
    print("DOCSTRING_HELP_LOCAL_ONLY: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
