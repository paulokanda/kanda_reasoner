"""Focused tests for the Brain Navigator WebView scaffold sub-box."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
)
CONTRACT_PATH = BOX_ROOT / "contract.py"
WEB_VIEW_PATH = BOX_ROOT / "_web_view_scaffold.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorWebViewScaffoldTests(unittest.TestCase):
    """Validate the WebView scaffold without requiring PySide6 at import time."""

    def test_public_contract_imports_without_webengine_side_effects(self) -> None:
        """The public contract should expose WebView scaffold helpers lazily."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.build_brain_web_view_scaffold_html))
        self.assertTrue(callable(contract.create_brain_web_view_scaffold))
        self.assertTrue(callable(contract.get_brain_web_view_scaffold_summary))

    def test_contract_lazily_delegates_to_web_view_internal(self) -> None:
        """The contract should not import the WebView scaffold at module import."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn("PySide6", top_level_imports)
        self.assertNotIn("._web_view_scaffold", top_level_imports)
        self.assertIn("from ._web_view_scaffold import", text)
        self.assertIn("build_brain_web_view_scaffold_html", text)

    def test_web_view_module_imports_without_pyside6(self) -> None:
        """The scaffold module should keep QWebEngine imports lazy."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import (
            _web_view_scaffold,
        )

        summary = _web_view_scaffold.get_brain_web_view_scaffold_summary()

        self.assertEqual("brain_web_view_scaffold", summary.box_id)
        self.assertEqual("qwebengine_scaffold_dry_run", summary.implementation_state)
        self.assertEqual(
            "not_wired_into_visible_brain_tab_yet",
            summary.visual_integration_state,
        )

    def test_html_contains_qwebchannel_and_region_intent_calls(self) -> None:
        """The local HTML should call the stable bridge slots."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_brain_web_view_scaffold_html,
        )

        html = build_brain_web_view_scaffold_html()

        self.assertIn("qrc:///qtwebchannel/qwebchannel.js", html)
        self.assertIn("window.brainNavigatorBridge", html)
        self.assertIn("notifyRegionHovered", html)
        self.assertIn("notifyRegionClicked", html)
        self.assertIn("onRegionHovered", html)
        self.assertIn("onRegionClicked", html)
        self.assertIn("Brain Navigator WebView Scaffold", html)
        self.assertIn("frontal_lobe", html)
        self.assertNotIn("setCurrentIndex", html)

    def test_web_view_source_has_lazy_qwebengine_factory_only(self) -> None:
        """The source should mention QWebEngine only in the lazy factory path."""

        text = WEB_VIEW_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertNotIn("PySide6.QtWebEngineWidgets", imported_modules)
        self.assertIn('import_module("PySide6.QtWebEngineWidgets")', text)
        self.assertIn('QWebEngineView = _qt_web_engine_widgets_attr("QWebEngineView")', text)
        self.assertIn("bridge_bundle.connect_to_page(web_view.page())", text)
        self.assertIn("web_view.setHtml(html)", text)

    def test_web_view_has_no_tab_or_main_window_reach_in(self) -> None:
        """The scaffold should not switch tabs or reach into other GUI boxes."""

        text = WEB_VIEW_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertNotIn("main_window", imported_modules)
        self.assertNotIn("tool_specs", imported_modules)
        self.assertNotIn("tab_navigation_controller", imported_modules)
        self.assertNotIn("setCurrentIndex", text)
        self.assertNotIn("self.tabs", text)
        self.assertNotIn("PromptLibraryTab", text)
        self.assertNotIn("IgnoreRulesTab", text)

    def test_manifest_tracks_web_view_scaffold(self) -> None:
        """The manifest should track the scaffold and focused tests."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("_web_view_scaffold.py", manifest["private_internals"])
        self.assertIn(
            "create_brain_web_view_scaffold",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "tests/test_brain_navigator_web_view_scaffold.py",
            manifest["validation"]["focused_tests"],
        )

    def test_readme_documents_not_wired_visible_state(self) -> None:
        """The README should document the dry-run boundary."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("WebView scaffold dry-run", readme)
        self.assertIn("not wired into the visible first tab yet", readme)
        self.assertIn("QWebEngineView", readme)
        self.assertIn("does not switch tabs", readme)


if __name__ == "__main__":
    unittest.main()
