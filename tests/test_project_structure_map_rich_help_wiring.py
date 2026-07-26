"""Regression tests for Project Structure Map rich shell help."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS


HELP_DOCS_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "help_docs"
)
HELP_SOURCE = HELP_DOCS_ROOT / "source" / "project_structure_map.md"
HELP_RENDERED = HELP_DOCS_ROOT / "rendered" / "project_structure_map.html"
HELP_MANIFEST = HELP_DOCS_ROOT / "manifest.json"
HELP_FALLBACK = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_help"
    / "project_structure_map.json"
)
RUNNER_UI = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_shell"
    / "runner_help"
    / "window_methods_private_impl.py"
)
HELP_ASSETS = (
    "assets/drawings/project_structure_map_opener_city_planning.png",
    "assets/drawings/project_structure_map_scope_survey.png",
    "assets/drawings/project_structure_map_run_stations.png",
    "assets/drawings/project_structure_map_records_workshop.png",
    "assets/drawings/project_structure_map_evidence_archive.png",
    "assets/drawings/project_structure_map_zip_shipping.png",
)


def _project_structure_spec():
    for spec in TOOLS:
        if spec.step_title == "Project Structure Map":
            return spec
    raise AssertionError("Project Structure Map spec is missing")


def test_shell_help_catalog_is_registered() -> None:
    spec = _project_structure_spec()

    assert spec.tab_id == "project_structure_map"
    assert spec.help_catalog == "project_structure_map.json"
    assert spec.source_hint == "kanda_reasoner_app/reasoner_context_collector/runner.py"


def test_rich_help_manifest_source_rendered_assets_and_fallback_exist() -> None:
    manifest = json.loads(HELP_MANIFEST.read_text(encoding="utf-8"))
    page = next(
        entry for entry in manifest["pages"]
        if entry["id"] == "project_structure_map"
    )

    assert page["title"] == "Project Structure Map Help"
    assert page["tab_id"] == "project_structure_map"
    assert page["legacy_help_catalog"] == "project_structure_map.json"
    assert page["source"] == "source/project_structure_map.md"
    assert page["rendered"] == "rendered/project_structure_map.html"
    assert page["css"] == "css/book_help.css"
    assert page["assets"] == list(HELP_ASSETS)

    assert HELP_SOURCE.is_file()
    assert HELP_RENDERED.is_file()
    assert HELP_FALLBACK.is_file()
    for asset in HELP_ASSETS:
        assert (HELP_DOCS_ROOT / asset).is_file()

    html = HELP_RENDERED.read_text(encoding="utf-8")
    assert "<h1>Project Structure Map</h1>" in html
    assert "Tab 4" not in html
    assert "chapter-number" not in html
    assert "http://" not in html
    assert "https://" not in html


def test_rich_help_content_covers_real_controls_and_artwork() -> None:
    text = HELP_SOURCE.read_text(encoding="utf-8")

    required_phrases = [
        "Mode selected: Creation Pipeline",
        "Project Structure Map is registered as the `project_structure_map` lazy tool",
        "Technical source categories",
        "In plain English",
        "Visual-inspection result: PASS",
        "Project Root And Scope Safety",
        "Run Collector Pipeline",
        "Evidence Collection And Index Building",
        "Complete JSON And AI Context Bundle",
        "JSON ZIP Handoff Export",
        "Project root",
        "Output JSON",
        "Run Collector",
        "Zip JSON files",
        "Conservative 25 MB",
        "Default 40 MB",
        "Runtime trace JSON",
        "Complete JSON",
        "AI context bundle",
        "drive-root scans",
        "ignore rules",
    ]

    for phrase in required_phrases:
        assert phrase in text

    for asset in HELP_ASSETS:
        assert asset in text
    assert "Tab 4" not in text


def test_help_control_reference_matches_runner_owner_labels() -> None:
    owner_source = RUNNER_UI.read_text(encoding="utf-8")
    help_source = HELP_SOURCE.read_text(encoding="utf-8")

    for label in (
        "Project root:",
        "Output JSON:",
        "Run Collector",
        "Zip JSON files",
        "Conservative 25 MB",
        "Default 40 MB",
    ):
        assert label in owner_source
        assert label.rstrip(":") in help_source


if __name__ == "__main__":
    test_shell_help_catalog_is_registered()
    test_rich_help_manifest_source_rendered_assets_and_fallback_exist()
    test_rich_help_content_covers_real_controls_and_artwork()
    test_help_control_reference_matches_runner_owner_labels()
    print("Project Structure Map rich shell help tests passed.")
