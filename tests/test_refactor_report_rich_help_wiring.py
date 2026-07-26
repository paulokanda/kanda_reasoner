"""Regression tests for Refactor Report rich shell help."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.daily_rfctr_report.daily_refactor_report_help.source_loader_private_impl import (
    load_daily_refactor_report_source,
)
from kanda_reasoner_app.reasoner_tools_gui_shell.help_docs.path_resolver import (
    find_page_by_legacy_catalog,
)
from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS


HELP_DOCS_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "help_docs"
)
HELP_SOURCE = HELP_DOCS_ROOT / "source" / "refactor_report.md"
HELP_RENDERED = HELP_DOCS_ROOT / "rendered" / "refactor_report.html"
HELP_MANIFEST = HELP_DOCS_ROOT / "manifest.json"
HELP_FALLBACK = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_help"
    / "refactor_report.json"
)
HELP_ASSETS = (
    "assets/drawings/refactor_report_opener_workshop.png",
    "assets/drawings/refactor_report_mode_a_scan_workbench.png",
    "assets/drawings/refactor_report_bundle_shipping_desk.png",
)


def _refactor_report_spec():
    for spec in TOOLS:
        if spec.step_title == "Refactor Report":
            return spec
    raise AssertionError("Refactor Report spec is missing")


def test_shell_help_catalog_is_registered() -> None:
    spec = _refactor_report_spec()

    assert spec.tab_id == "refactor_report"
    assert spec.help_catalog == "refactor_report.json"
    assert spec.source_hint == "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py"


def test_rich_help_manifest_source_rendered_assets_and_fallback_exist() -> None:
    manifest = json.loads(HELP_MANIFEST.read_text(encoding="utf-8"))
    page = next(
        entry for entry in manifest["pages"]
        if entry["id"] == "refactor_report"
    )

    assert page["title"] == "Refactor Report Help"
    assert page["tab_id"] == "refactor_report"
    assert page["legacy_help_catalog"] == "refactor_report.json"
    assert page["source"] == "source/refactor_report.md"
    assert page["rendered"] == "rendered/refactor_report.html"
    assert page["css"] == "css/book_help.css"
    assert page["assets"] == list(HELP_ASSETS)

    assert HELP_SOURCE.is_file()
    assert HELP_RENDERED.is_file()
    assert HELP_FALLBACK.is_file()
    for asset in HELP_ASSETS:
        assert (HELP_DOCS_ROOT / asset).is_file()

    html = HELP_RENDERED.read_text(encoding="utf-8")
    assert "<h1>Refactor Report</h1>" in html
    assert 'href="../css/book_help.css"' in html
    assert "http://" not in html
    assert "https://" not in html
    assert "//cdn" not in html


def test_legacy_catalog_resolves_to_rich_help_page() -> None:
    page = find_page_by_legacy_catalog("refactor_report.json")

    assert page is not None
    assert page.page_id == "refactor_report"
    assert page.source_path == HELP_SOURCE
    assert page.rendered_path == HELP_RENDERED
    assert page.css_path == HELP_DOCS_ROOT / "css" / "book_help.css"
    assert page.asset_paths == tuple(HELP_DOCS_ROOT / asset for asset in HELP_ASSETS)


def test_rich_help_content_covers_real_controls_and_artwork() -> None:
    text = HELP_SOURCE.read_text(encoding="utf-8")

    required_phrases = [
        "Mode selected: Creation Pipeline",
        "Refactor Report is registered as the `refactor_report` lazy tool",
        "In plain English",
        "Visual-inspection result: PASS",
        "Mode A Project Folder Scan",
        "Mode B Existing State Vector",
        "Output JSON And AI Bundle Path",
        "Compile, Refresh, And Save Bundle",
        "Control Reference",
        "Authority Boundary",
        "Select Project Folder",
        "Output JSON",
        "Choose Folder",
        "Load Existing JSON",
        "AI Bundle Path",
        "Set Bundle Path",
        "Clear",
        "Compile State Vector",
        "Force Re-extract",
        "Save Bundle Now",
        "daily_refactor/bundles",
        "not source-code edits",
    ]

    for phrase in required_phrases:
        assert phrase in text

    for asset in HELP_ASSETS:
        assert asset in text


def test_help_control_reference_matches_decoded_owner_labels() -> None:
    owner_source = load_daily_refactor_report_source()
    help_source = HELP_SOURCE.read_text(encoding="utf-8")

    for label in (
        "Mode A:",
        "Select Project Folder",
        "Output JSON",
        "Choose Folder",
        "Load Existing JSON",
        "AI Bundle Path",
        "Set Bundle Path",
        "Mode B:",
        "Compile State Vector",
        "Force Re-extract",
        "Save Bundle Now",
    ):
        assert label in owner_source
        assert label.rstrip(":") in help_source


if __name__ == "__main__":
    test_shell_help_catalog_is_registered()
    test_rich_help_manifest_source_rendered_assets_and_fallback_exist()
    test_legacy_catalog_resolves_to_rich_help_page()
    test_rich_help_content_covers_real_controls_and_artwork()
    test_help_control_reference_matches_decoded_owner_labels()
    print("Refactor Report rich shell help tests passed.")
