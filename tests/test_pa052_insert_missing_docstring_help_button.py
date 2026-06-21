"""Tests for PA052 Docstring Assistant rich shell help."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS
from kanda_reasoner_app.tab3_manual_review_runtime import (
    insert_missing_docstring_help_runtime,
)

LAYOUT_PATH = ROOT / "kanda_reasoner_app" / "tab3_manual_review_runtime" / "layout_runtime.py"
HELP_DOCS_ROOT = (
    ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "help_docs"
)
HELP_SOURCE = HELP_DOCS_ROOT / "source" / "docstring_assistant.md"
HELP_RENDERED = HELP_DOCS_ROOT / "rendered" / "docstring_assistant.html"
HELP_MANIFEST = HELP_DOCS_ROOT / "manifest.json"
HELP_FALLBACK = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_help" / "docstring_assistant.json"
HELP_ASSETS = (
    "assets/drawings/docstring_assistant_opener_library.png",
    "assets/drawings/docstring_assistant_scan_post_room.png",
    "assets/drawings/docstring_assistant_ai_copy_shop.png",
    "assets/drawings/docstring_assistant_review_tailor.png",
    "assets/drawings/docstring_assistant_report_clerk.png",
)


def _docstring_spec():
    for spec in TOOLS:
        if spec.step_title == "Docstring Assistant":
            return spec
    raise AssertionError("Docstring Assistant spec is missing")


def test_shell_help_catalog_is_registered_and_embedded_button_removed() -> None:
    """Verify the shell owns Help and the embedded panel does not duplicate it."""
    spec = _docstring_spec()
    source = LAYOUT_PATH.read_text(encoding="utf-8")

    assert spec.tab_id == "docstring_assistant"
    assert spec.help_catalog == "docstring_assistant.json"
    assert "_insert_missing_docstring_help_button" not in source
    assert "Help - Insert Missing Docstring" not in source
    assert "_insert_missing_docstring_help_slot" not in source
    assert "open_insert_missing_docstring_help(window)" not in source


def test_rich_help_manifest_source_rendered_assets_and_fallback_exist() -> None:
    """Verify the rich help page is registered and local-only."""
    manifest = json.loads(HELP_MANIFEST.read_text(encoding="utf-8"))
    page = next(
        entry for entry in manifest["pages"]
        if entry["id"] == "docstring_assistant"
    )

    assert page["title"] == "Docstring Assistant Help"
    assert page["tab_id"] == "docstring_assistant"
    assert page["legacy_help_catalog"] == "docstring_assistant.json"
    assert page["source"] == "source/docstring_assistant.md"
    assert page["rendered"] == "rendered/docstring_assistant.html"
    assert page["css"] == "css/book_help.css"
    assert page["assets"] == list(HELP_ASSETS)

    assert HELP_SOURCE.is_file()
    assert HELP_RENDERED.is_file()
    assert HELP_FALLBACK.is_file()
    for asset in HELP_ASSETS:
        assert (HELP_DOCS_ROOT / asset).is_file()

    html = HELP_RENDERED.read_text(encoding="utf-8")
    assert "<h1>Docstring Assistant</h1>" in html
    assert "Tab 3" not in html
    assert "chapter-number" not in html
    assert "http://" not in html
    assert "https://" not in html


def test_rich_help_content_covers_controls_workflow_and_artwork() -> None:
    """Verify the help content covers the tab controls and canonized drawings."""
    text = HELP_SOURCE.read_text(encoding="utf-8")

    required_phrases = [
        "Mode selected: Creation Pipeline",
        "Docstring Assistant is registered as the `docstring_assistant` lazy tool",
        "Technical source categories",
        "In plain English",
        "Visual-inspection result: PASS",
        "Scan Workflow",
        "Local AI And Heuristic Drafts",
        "Review And Correction",
        "Reports And Safety Boundary",
        "Scan Files for Missing Docstrings",
        "Generate Draft",
        "Enable Local AI",
        "Base URL",
        "Model",
        "Minimum confidence",
        "AI draft style",
        "Concise",
        "Balanced",
        "Detailed",
        "Save Review Decision",
        "Generate Visible Drafts",
        "Generate All Drafts",
        "Undo Last Bulk Drafts",
        "Minimum confidence and no-uncertain policy are acceptance controls",
        "Reports are usually JSONL-style review artifacts",
    ]

    for phrase in required_phrases:
        assert phrase in text

    for asset in HELP_ASSETS:
        assert asset in text
    assert "Tab 3" not in text


def test_legacy_help_runtime_remains_importable_as_fallback() -> None:
    """Verify the older plain help runtime stays available as fallback content."""
    assert callable(insert_missing_docstring_help_runtime.get_insert_missing_docstring_help_text)
    assert callable(insert_missing_docstring_help_runtime.open_insert_missing_docstring_help)


if __name__ == "__main__":
    test_shell_help_catalog_is_registered_and_embedded_button_removed()
    test_rich_help_manifest_source_rendered_assets_and_fallback_exist()
    test_rich_help_content_covers_controls_workflow_and_artwork()
    test_legacy_help_runtime_remains_importable_as_fallback()
    print("PA052 Docstring Assistant rich shell help tests passed.")
