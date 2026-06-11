"""Focused tests for the Brain Navigator Web Bridge sub-box."""

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
WEB_BRIDGE_PATH = BOX_ROOT / "_web_bridge.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"

FORBIDDEN_BRIDGE_TOKENS = (
    "setCurrentIndex",
    "self.tabs",
    "main_window",
    "tool_specs",
    "PromptLibraryTab",
    "IgnoreRulesTab",
)


class BrainNavigatorWebBridgeBoxTests(unittest.TestCase):
    """Validate the bridge scaffold without requiring PySide6 at import time."""

    def test_public_contract_imports_without_qt_side_effects(self) -> None:
        """The public contract should expose bridge helpers lazily."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.create_brain_web_bridge))
        self.assertTrue(callable(contract.build_brain_web_channel_bootstrap_script))
        self.assertTrue(callable(contract.normalize_brain_region_id))
        self.assertTrue(callable(contract.get_brain_web_bridge_summary))

    def test_contract_lazily_delegates_to_web_bridge_internal(self) -> None:
        """The public contract should import the bridge only inside functions."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn("PySide6", top_level_imports)
        self.assertNotIn("._web_bridge", top_level_imports)
        self.assertIn("from ._web_bridge import create_brain_web_bridge", text)
        self.assertIn("from ._web_bridge import build_brain_web_channel_bootstrap_script", text)

    def test_web_bridge_module_imports_without_pyside6(self) -> None:
        """The internal bridge module should keep PySide6 imports lazy."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import _web_bridge

        self.assertEqual("frontal_lobe", _web_bridge.normalize_brain_region_id(" frontal_lobe "))
        self.assertEqual("unknown_region", _web_bridge.normalize_brain_region_id(""))

    def test_bridge_summary_declares_intent_only_boundary(self) -> None:
        """The bridge summary should state signals and forbidden dependencies."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator._web_bridge import (
            get_brain_web_bridge_summary,
        )

        summary = get_brain_web_bridge_summary()

        self.assertEqual("brain_web_bridge", summary.box_id)
        self.assertEqual("0.1", summary.contract_version)
        self.assertEqual("qt_web_channel_bridge_scaffold", summary.implementation_state)
        self.assertIn("regionHovered(region_id)", summary.emitted_signals)
        self.assertIn("regionClicked(region_id)", summary.emitted_signals)
        self.assertIn("onRegionHovered(region_id)", summary.javascript_slots)
        self.assertIn("onRegionClicked(region_id)", summary.javascript_slots)
        self.assertIn("main_window", summary.forbidden_dependencies)
        self.assertIn("direct_tab_index_switching", summary.forbidden_dependencies)

    def test_bootstrap_script_registers_stable_bridge_object(self) -> None:
        """The JS bootstrap should use QWebChannel and stable object names."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator._web_bridge import (
            build_brain_web_channel_bootstrap_script,
        )

        script = build_brain_web_channel_bootstrap_script("bridge")

        self.assertIn("QWebChannel", script)
        self.assertIn("channel.objects.bridge", script)
        self.assertIn("window.brainNavigatorBridge", script)
        self.assertNotIn("setCurrentIndex", script)

    def test_web_bridge_source_has_qt_signals_and_js_slots(self) -> None:
        """The bridge source should expose region-aware hover and click slots."""

        text = WEB_BRIDGE_PATH.read_text(encoding="utf-8")

        self.assertIn("QWebChannel", text)
        self.assertIn("QObject", text)
        self.assertIn("regionHovered = Signal(str)", text)
        self.assertIn("regionClicked = Signal(str)", text)
        self.assertIn("def onRegionHovered", text)
        self.assertIn("def onRegionClicked", text)
        self.assertIn("def onBrainClicked", text)
        self.assertIn("channel.registerObject(object_name, bridge)", text)

    def test_web_bridge_has_no_tab_or_main_window_reach_in(self) -> None:
        """The bridge should emit intent but never switch tabs directly."""

        text = WEB_BRIDGE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertNotIn("main_window", imported_modules)
        self.assertNotIn("tool_specs", imported_modules)
        self.assertNotIn("setCurrentIndex(", text)
        self.assertNotIn("self.tabs", text)
        self.assertNotIn("PromptLibraryTab", text)
        self.assertNotIn("IgnoreRulesTab", text)

    def test_manifest_tracks_web_bridge_internal(self) -> None:
        """The Brain Navigator manifest should include the web bridge scaffold."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("_web_bridge.py", manifest["private_internals"])
        self.assertIn(
            "create_brain_web_bridge",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "build_brain_web_channel_bootstrap_script",
            manifest["public_contract"]["provides_functions"],
        )

    def test_readme_documents_bridge_boundary(self) -> None:
        """The README should describe region-aware bridge behavior."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("visible Neural Architecture brain with safe fallback index available", readme)
        self.assertIn("onRegionHovered(region_id)", readme)
        self.assertIn("onRegionClicked(region_id)", readme)
        self.assertIn("regionHovered(region_id)", readme)
        self.assertIn("regionClicked(region_id)", readme)
        self.assertIn("does not switch", readme)


if __name__ == "__main__":
    unittest.main()
