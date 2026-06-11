"""Focused tests for visible Neural Architecture Brain Navigator integration."""

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
VISIBLE_TAB_PATH = BOX_ROOT / "_visible_neural_architecture_tab.py"
TEMPLATE_PATH = BOX_ROOT / "assets" / "brain_visual_template.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorVisibleNeuralArchitectureTabTests(unittest.TestCase):
    """Validate that the real brain visual is now the visible default."""

    def test_contract_delegates_visible_tab_to_neural_architecture_factory(self) -> None:
        """create_brain_navigator_tab should no longer return fallback directly."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")

        self.assertIn("create_visible_neural_architecture_brain_tab", text)
        self.assertIn("from ._visible_neural_architecture_tab import", text)
        create_body = text.split("def create_brain_navigator_tab", 1)[1]
        self.assertIn("_create_visible_tab", create_body)
        self.assertNotIn("create_brain_navigator_fallback_widget(*args", create_body)

    def test_visible_tab_factory_preserves_safe_fallback_without_tab_reach_in(self) -> None:
        """The visible factory may fallback but must not switch tabs directly."""

        text = VISIBLE_TAB_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertIn("_neural_architecture_preview", imported_modules)
        self.assertIn("_fallback_index_widget", imported_modules)
        self.assertNotIn("main_window", imported_modules)
        self.assertNotIn("tool_specs", imported_modules)
        self.assertNotIn("tab_navigation_controller", imported_modules)
        self.assertNotIn("setCurrentIndex", text)
        self.assertIn("except Exception", text)
        self.assertIn("create_brain_navigator_fallback_widget", text)

    def test_template_contains_real_threejs_brain_renderer(self) -> None:
        """The asset template should render the brain, not only inert mesh data."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("THREE.WebGLRenderer", html)
        self.assertIn("new THREE.PerspectiveCamera", html)
        self.assertIn("buildPointRegion", html)
        self.assertIn("buildMeshLines", html)
        self.assertIn("initializeNeuralArchitectureBrain", html)
        self.assertIn("loopNeuralArchitectureBrain", html)
        self.assertIn("const TEL_PTS", html)
        self.assertIn("const CERB_PTS", html)
        self.assertIn("const MID_PTS", html)
        self.assertIn("const EDGE_PTS", html)
        self.assertIn("const NEURAL_ARCHITECTURE_PULSE_MARKERS", html)
        self.assertIn("Neural Architecture", html)
        self.assertIn("Knowledge and Architecture Navigator for Developer Assistance", html)
        self.assertIn("What is the airspeed velocity of an unladen swallow?", html)
        self.assertNotIn("Safe fallback index", html)
        self.assertNotIn("Brain structures as app modules", html)

    def test_template_keeps_responsive_resize_contract(self) -> None:
        """Visible brain rendering should fit and resize with the tab."""

        html = (
            __import__(
                "kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract",
                fromlist=["build_neural_architecture_preview_html"],
            )
            .build_neural_architecture_preview_html()
        )

        self.assertIn('window.addEventListener("resize", resizeNeuralArchitectureStage)', html)
        self.assertIn("renderer.setSize(width, height)", html)
        self.assertIn("camera.aspect = width / height", html)
        self.assertIn("camera.updateProjectionMatrix()", html)
        self.assertIn("fitBrainToViewport()", html)
        self.assertIn("updateProjectedMarkers()", html)

    def test_summary_and_manifest_track_visible_default(self) -> None:
        """Metadata should state that the brain is now the visible default."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_brain_navigator_contract_summary,
            get_visible_neural_architecture_tab_summary,
        )

        summary = get_brain_navigator_contract_summary()
        visible_summary = get_visible_neural_architecture_tab_summary()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(
            "visible_neural_architecture_brain_with_fancy_index_open_module_action",
            summary.implementation_state,
        )
        self.assertEqual(
            "visible_default_neural_architecture_with_fancy_index_open_module_action",
            visible_summary.visual_integration_state,
        )
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("_visible_neural_architecture_tab.py", manifest["private_internals"])
        self.assertIn(
            "create_visible_neural_architecture_brain_tab",
            manifest["public_contract"]["provides_functions"],
        )

    def test_readme_documents_visible_default_and_fallback_exception(self) -> None:
        """README should explain why the normal app no longer shows the index."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Patch 11 - Visible Neural Architecture default tab", readme)
        self.assertIn("normal visible Brain", readme)
        self.assertIn("should no longer show the text-heavy fallback index by", readme)
        self.assertIn("fallback index remains available only if WebEngine", readme)
        self.assertIn("does not switch tabs", readme)


if __name__ == "__main__":
    unittest.main()
