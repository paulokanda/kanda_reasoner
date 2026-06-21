"""Regression tests for Architecture Review rich desktop help."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from kanda_reasoner_app.reasoner_tools_gui_shell.help_docs.path_resolver import (
    HELP_DOCS_ROOT,
    find_page_by_legacy_catalog,
    load_help_manifest,
    resolve_help_child,
)


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_help" / "tab1_architecture.json"
GUI_SUPPORT = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "gui_support.py"
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
RENDERER = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "help_docs" / "renderer.py"
PROMPT_WORKSPACE_ROOT = ROOT / "kanda_prompt_workspace" / "prompt_library"
HELP_LAYOUT_PROMPT = (
    PROMPT_WORKSPACE_ROOT
    / "ACTIVE_PROMPTS"
    / "12_generalized_project_canons"
    / "desktop_help_document_layout_canon.md"
)
HELP_LAYOUT_META = PROMPT_WORKSPACE_ROOT / "METADATA" / "desktop_help_document_layout_canon.meta.json"
PROMPT_NAVIGATION_JSON = PROMPT_WORKSPACE_ROOT / "ROUTING" / "prompt_navigation_index.json"
GROUP_ASSIMILATION_JSON = PROMPT_WORKSPACE_ROOT / "ROUTING" / "group_assimilation_index.json"
FOLDER_ASSIMILATION_INDEX_MD = PROMPT_WORKSPACE_ROOT / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
FOLDER_CARD = (
    PROMPT_WORKSPACE_ROOT
    / "ACTIVE_PROMPTS"
    / "12_generalized_project_canons"
    / "_FOLDER_ASSIMILATION.md"
)


class ArchitectureReviewRichHelpDocumentTests(unittest.TestCase):
    def test_manifest_maps_legacy_architecture_catalog_to_rich_help_page(self) -> None:
        manifest = load_help_manifest()
        self.assertEqual(manifest["schema"], "kanda-desktop-help-docs/v1")

        page = find_page_by_legacy_catalog("tab1_architecture.json")
        self.assertIsNotNone(page)
        assert page is not None
        self.assertEqual(page.page_id, "architecture_review")
        self.assertEqual(page.legacy_help_catalog, "tab1_architecture.json")
        self.assertTrue(page.source_path.is_file())
        self.assertTrue(page.rendered_path.is_file())
        self.assertTrue(page.css_path.is_file())
        drawing_assets = []
        for asset in page.asset_paths:
            self.assertTrue(asset.is_file(), asset)
            self.assertTrue(str(asset.resolve()).startswith(str(HELP_DOCS_ROOT.resolve())))
            if "assets\\drawings" in str(asset) or "assets/drawings" in str(asset):
                drawing_assets.append(asset)
            if asset.suffix == ".png":
                self.assertGreater(asset.stat().st_size, 100000)
                self.assertEqual(asset.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            else:
                asset_text = asset.read_text(encoding="utf-8")
                for forbidden in ("https://", "//cdn.", "fonts.googleapis", "tracker"):
                    self.assertNotIn(forbidden, asset_text)
                self.assertNotIn('href="http://', asset_text)
                self.assertNotIn("href='http://", asset_text)
        self.assertGreaterEqual(len(drawing_assets), 4)

    def test_rendered_html_is_local_static_book_style_document(self) -> None:
        page = find_page_by_legacy_catalog("tab1_architecture.json")
        assert page is not None
        html = page.rendered_path.read_text(encoding="utf-8")
        css = page.css_path.read_text(encoding="utf-8")

        self.assertIn('<article class="book-page">', html)
        self.assertIn('<link rel="stylesheet" href="../css/book_help.css">', html)
        self.assertIn('class="chapter-opener', html)
        self.assertIn('class="chapter-drawing', html)
        self.assertIn('class="section-drawing"', html)
        self.assertIn("../assets/drawings/architecture_review_summary_inspector.png", html)
        self.assertIn("../assets/drawings/architecture_review_workflow_cafe.png", html)
        self.assertIn("../assets/drawings/architecture_review_issue_catalog_library.png", html)
        self.assertIn("../assets/drawings/architecture_review_checklist_airport.png", html)
        self.assertIn("../assets/diagrams/architecture_review_pipeline.svg", html)
        self.assertIn("<figcaption>", html)
        self.assertNotIn("<table>", html)
        self.assertIn('class="route-steps"', html)
        self.assertGreaterEqual(html.count('class="control-card"'), 23)
        self.assertEqual(html.count('class="issue-card"'), 25)
        self.assertEqual(html.count('class="reading-map"'), 6)
        self.assertIn("Table AR-3 is rendered as issue cards", html)
        self.assertIn("Architecture Review reports risks", html)
        self.assertIn("Book Grounding Map", html)
        self.assertIn("running-footer", html)

        for forbidden in ("http://", "https://", "//cdn.", "fonts.googleapis", "tracker"):
            self.assertNotIn(forbidden, html)
            self.assertNotIn(forbidden, css)

        self.assertIn("--xref: #1a4e8c", css)
        self.assertIn("--blue-chapter: #0f3460", css)
        self.assertIn("--blue-light: #dbeafe", css)
        self.assertIn("--orange-mid: #f59e0b", css)
        self.assertIn("--orange-rule: #ea580c", css)
        self.assertIn(".callout-warning", css)
        self.assertIn("overflow-wrap: anywhere", css)
        self.assertIn("white-space: pre-wrap", css)
        self.assertIn(".control-card", css)
        self.assertIn('"Minion Pro"', css)
        self.assertIn('"Myriad Pro Cond"', css)
        self.assertIn('"Ubuntu Mono"', css)

        for drawing_name in (
            "architecture_review_summary_inspector.png",
            "architecture_review_workflow_cafe.png",
            "architecture_review_issue_catalog_library.png",
            "architecture_review_checklist_airport.png",
        ):
            drawing_path = HELP_DOCS_ROOT / "assets" / "drawings" / drawing_name
            self.assertGreater(drawing_path.stat().st_size, 100000)
            self.assertEqual(drawing_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_adviser_to_pilot_bridge_help_uses_local_bitmap_artwork(self) -> None:
        manifest = load_help_manifest()
        entry = next(
            item
            for item in manifest["pages"]
            if item["id"] == "adviser_to_pilot_copilot_bridge"
        )
        self.assertEqual(entry["tab_id"], "routing_signal_scorer_v3_bridge")
        self.assertEqual(entry["legacy_help_catalog"], "")

        source_path = resolve_help_child(entry["source"])
        rendered_path = resolve_help_child(entry["rendered"])
        css_path = resolve_help_child(entry["css"])
        asset_paths = [resolve_help_child(asset) for asset in entry["assets"]]

        self.assertTrue(source_path.is_file())
        self.assertTrue(rendered_path.is_file())
        self.assertTrue(css_path.is_file())
        self.assertEqual(len(asset_paths), 3)

        root = HELP_DOCS_ROOT.resolve()
        for asset_path in asset_paths:
            self.assertTrue(asset_path.is_file(), asset_path)
            self.assertTrue(str(asset_path.resolve()).startswith(str(root)))
            self.assertEqual(asset_path.suffix, ".png")
            self.assertGreater(asset_path.stat().st_size, 100000)
            self.assertEqual(asset_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

        html = rendered_path.read_text(encoding="utf-8")
        source = source_path.read_text(encoding="utf-8")
        css = css_path.read_text(encoding="utf-8")

        for file_name in (
            "adviser_to_pilot_bridge_opener.png",
            "adviser_to_pilot_shadow_observation_cafe.png",
            "adviser_to_pilot_frozen_roadmap_station.png",
        ):
            self.assertIn(file_name, html)
            self.assertIn(file_name, source)

        self.assertEqual(html.count("../assets/drawings/adviser_to_pilot_"), 3)
        self.assertEqual(source.count("Image note:"), 3)
        self.assertEqual(source.count("Density-rule justification:"), 3)
        self.assertEqual(source.count("local PNG bitmap"), 3)
        self.assertGreaterEqual(source.count("gorgeous hand-made daily-life cartoon"), 3)

        self.assertIn("Adviser-to-Pilot/Copilot bridge is closed and frozen", html)
        self.assertIn("P0", html)
        self.assertIn("not runtime activation", html)
        self.assertIn("No runtime authority.", html)
        self.assertIn("<strong>Technical:</strong>", html)
        self.assertIn("<strong>In plain English:</strong>", html)
        self.assertIn("<strong>Further reading:</strong>", html)
        self.assertIn("running-footer", html)

        for forbidden in ("http://", "https://", "//cdn.", "fonts.googleapis", "tracker"):
            self.assertNotIn(forbidden, html)
            self.assertNotIn(forbidden, source)
            self.assertNotIn(forbidden, css)

    def test_all_legacy_architecture_issue_families_are_visible_in_rich_help(self) -> None:
        payload = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(len(payload["errors"]), 25)

        page = find_page_by_legacy_catalog("tab1_architecture.json")
        assert page is not None
        html = page.rendered_path.read_text(encoding="utf-8")
        source = page.source_path.read_text(encoding="utf-8")
        html_plain = re.sub(r"<[^>]+>", "", html)
        source_plain = source.replace("`", "")

        for item in payload["errors"]:
            self.assertIn(str(item["error"]), html_plain)
            self.assertIn(str(item["error"]), source_plain)
        self.assertEqual(html.count('class="issue-card"'), 25)
        self.assertGreaterEqual(html.count("<strong>Technical:</strong>"), 25)
        self.assertGreaterEqual(html.count("<strong>In plain English:</strong>"), 25)
        self.assertGreaterEqual(html.count("<strong>If ignored:</strong>"), 25)
        self.assertIn("Table AR-3 is rendered as issue cards", html)
        self.assertIn("Table AR-3 is rendered as issue cards", source)
        self.assertNotIn("Density-rule justification:", source)

        issue_cards = html.split('class="issue-card"')[1:]
        self.assertEqual(len(issue_cards), 25)
        for card in issue_cards:
            self.assertIn("<strong>Technical:</strong>", card)
            self.assertIn("<strong>In plain English:</strong>", card)
            self.assertIn("<strong>If ignored:</strong>", card)

    def test_path_resolver_rejects_traversal_and_absolute_paths(self) -> None:
        with self.assertRaises(ValueError):
            resolve_help_child("../outside.html")
        with self.assertRaises(ValueError):
            resolve_help_child("C:/outside.html")
        self.assertTrue(resolve_help_child("rendered/architecture_review.html").is_file())

    def test_gui_prefers_rich_help_and_keeps_plain_text_fallback(self) -> None:
        lazy_source = LAZY_TABS.read_text(encoding="utf-8")
        gui_support_source = GUI_SUPPORT.read_text(encoding="utf-8")
        renderer_source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("open_help_document_for_legacy_catalog", lazy_source)
        self.assertIn("_format_help_catalog_text(path)", lazy_source)
        self.assertIn("CANONICAL_PACKAGE_NAME", gui_support_source)
        self.assertIn("canonical_path.exists()", gui_support_source)

        self.assertIn("QWebEngineView", renderer_source)
        self.assertIn("QTextBrowser", renderer_source)
        self.assertNotIn("from PySide6.QtWebEngineWidgets import", renderer_source)
        self.assertNotIn("import PySide6.QtWebEngineWidgets", renderer_source)

    def test_help_layout_prompt_is_registered_in_prompt_workspace(self) -> None:
        prompt_text = HELP_LAYOUT_PROMPT.read_text(encoding="utf-8")
        metadata = json.loads(HELP_LAYOUT_META.read_text(encoding="utf-8"))
        navigation = json.loads(PROMPT_NAVIGATION_JSON.read_text(encoding="utf-8"))
        groups = json.loads(GROUP_ASSIMILATION_JSON.read_text(encoding="utf-8"))
        folder_index = FOLDER_ASSIMILATION_INDEX_MD.read_text(encoding="utf-8")
        folder_card = FOLDER_CARD.read_text(encoding="utf-8")

        self.assertEqual(metadata["prompt_id"], "desktop_help_document_layout_canon")
        self.assertEqual(metadata["category"], "12_generalized_project_canons")
        self.assertEqual(metadata["load_type"], "on_request")
        self.assertIn("desktop help layout", metadata["trigger_phrases"])

        route = next(
            item
            for item in navigation["entries"]
            if item["prompt_id"] == "desktop_help_document_layout_canon"
        )
        self.assertEqual(
            route["relative_path"],
            "ACTIVE_PROMPTS/12_generalized_project_canons/desktop_help_document_layout_canon.md",
        )
        self.assertIn("shared_visual_render_engine_canon", route["required_companion_prompts"])

        group = next(item for item in groups["groups"] if item["group_id"] == "12_generalized_project_canons")
        self.assertIn("desktop_help_document_layout_canon.md", group["main_prompts"])
        self.assertEqual(group["prompt_count"], 6)
        self.assertIn("desktop help-document layout", folder_index)
        self.assertIn("| 6 |", folder_index)
        self.assertIn("desktop_help_document_layout_canon", folder_card)

        self.assertIn(
            "Markdown source -> local-code-grounded dual-audience explanations -> optional official/maintainer/spec/book grounding -> beautiful hand-made daily-life cartoon illustrations -> deterministic local HTML/CSS -> desktop Qt help window",
            prompt_text,
        )
        self.assertIn("Reference notes under `.project_reference/` are not active project prompt artifacts", prompt_text)
        self.assertIn("No runtime or prompt-library test depends on `.project_reference`", prompt_text)
        self.assertIn("--blue-chapter: #0f3460", prompt_text)
        self.assertIn("--orange-mid: #f59e0b", prompt_text)
        self.assertIn("QWebEngineView", prompt_text)
        self.assertIn("QTextBrowser", prompt_text)
        self.assertIn("beautiful hand-made daily-life cartoon", prompt_text)
        self.assertIn("colorful editorial cartoon line art", prompt_text)
        self.assertIn("funny daily-life", prompt_text)
        self.assertIn("visible hatching", prompt_text)
        self.assertIn("hand-lettered signs", prompt_text)
        self.assertIn("Drawing Density Rule", prompt_text)
        self.assertIn("simple schematic vector art", prompt_text)
        self.assertIn("geometric placeholder", prompt_text)
        self.assertIn("copied compositions", prompt_text)
        self.assertIn("local `PNG` or `WebP`", prompt_text)
        self.assertIn("SVG is reserved for technical diagrams", prompt_text)
        self.assertIn("Page Boundary And No-Overflow Rule", prompt_text)
        self.assertIn("No horizontal overflow is allowed", prompt_text)
        self.assertIn("issue-family catalogs", prompt_text)


if __name__ == "__main__":
    unittest.main()
