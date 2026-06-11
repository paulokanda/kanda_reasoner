"""Focused tests for the isolated Neural Architecture WebView preview."""

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
PREVIEW_PATH = BOX_ROOT / "_neural_architecture_preview.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"
MANUAL_PREVIEW_PATH = (
    PROJECT_ROOT / "workbench" / "manual_preview" / "run_neural_architecture_preview.ps1"
)


class BrainNavigatorNeuralArchitecturePreviewTests(unittest.TestCase):
    """Validate isolated preview wiring without changing visible GUI behavior."""

    def test_public_contract_exposes_preview_helpers_lazily(self) -> None:
        """The public contract should expose preview helpers without GUI imports."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.build_neural_architecture_preview_html))
        self.assertTrue(callable(contract.create_neural_architecture_preview))
        self.assertTrue(callable(contract.get_neural_architecture_preview_summary))

    def test_contract_lazily_delegates_to_preview_internal(self) -> None:
        """The contract should not import the preview sub-box at module import."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn("PySide6", top_level_imports)
        self.assertNotIn("._neural_architecture_preview", top_level_imports)
        self.assertIn("from ._neural_architecture_preview import", text)
        self.assertIn("create_neural_architecture_preview", text)

    def test_preview_module_imports_without_pyside6(self) -> None:
        """The preview module should keep QWebEngine imports lazy."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import (
            _neural_architecture_preview,
        )

        summary = _neural_architecture_preview.get_neural_architecture_preview_summary()

        self.assertEqual("neural_architecture_preview", summary.box_id)
        self.assertEqual(
            "isolated_neural_architecture_webview_preview",
            summary.implementation_state,
        )
        self.assertEqual(
            "manual_preview_only_not_default_visible_tab",
            summary.visual_integration_state,
        )

    def test_preview_html_contains_asset_bridge_and_responsive_tokens(self) -> None:
        """The preview HTML should load the extracted asset and bridge bootstrap."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("Neural Architecture", html)
        self.assertIn("Knowledge and Architecture Navigator for Developer Assistance", html)
        self.assertIn("What is the airspeed velocity of an unladen swallow?", html)
        self.assertIn("qrc:///qtwebchannel/qwebchannel.js", html)
        self.assertIn("window.brainNavigatorBridge", html)
        self.assertIn("const TEL_PTS", html)
        self.assertIn("const SURFACE_DOT_COUNT = 9255", html)
        self.assertIn("pulse-marker", html)
        self.assertIn('window.addEventListener("resize", resizeNeuralArchitectureStage)', html)
        self.assertIn("renderer.setSize(width, height)", html)
        self.assertIn("camera.aspect = width / height", html)
        self.assertIn("camera.updateProjectionMatrix()", html)
        self.assertIn("updateProjectedMarkers()", html)
        self.assertNotIn("setCurrentIndex", html)

    def test_preview_source_has_lazy_qwebengine_factory_only(self) -> None:
        """The source should mention QWebEngine only in the lazy factory path."""

        text = PREVIEW_PATH.read_text(encoding="utf-8")
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

    def test_preview_has_no_tab_or_main_window_reach_in(self) -> None:
        """The preview should not switch tabs or reach into other GUI boxes."""

        text = PREVIEW_PATH.read_text(encoding="utf-8")
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

    def test_manual_preview_launcher_uses_public_contract_only(self) -> None:
        """The manual preview launcher should avoid private Brain Navigator imports."""

        text = MANUAL_PREVIEW_PATH.read_text(encoding="utf-8")

        self.assertIn("create_neural_architecture_preview", text)
        self.assertIn("get_neural_architecture_preview_summary", text)
        self.assertIn("brain_navigator.contract", text)
        self.assertNotIn("._neural_architecture_preview", text)
        self.assertIn("QApplication", text)

    def test_manifest_tracks_isolated_preview(self) -> None:
        """The Brain Navigator manifest should track the isolated preview."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("_neural_architecture_preview.py", manifest["private_internals"])
        self.assertIn(
            "create_neural_architecture_preview",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "tests/test_brain_navigator_neural_architecture_preview.py",
            manifest["validation"]["focused_tests"],
        )
        self.assertIn(
            "isolated_neural_architecture_preview_manual_only",
            manifest["communication_route"],
        )

    def test_readme_documents_manual_preview_state(self) -> None:
        """The README should document Patch 9 preview-only behavior."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Patch 9 - Isolated Neural Architecture WebView preview", readme)
        self.assertIn("manual preview-only", readme)
        self.assertIn("not wired into the visible first tab", readme)
        self.assertIn("run_neural_architecture_preview.ps1", readme)
        self.assertIn("does not switch tabs", readme)


if __name__ == "__main__":
    unittest.main()
