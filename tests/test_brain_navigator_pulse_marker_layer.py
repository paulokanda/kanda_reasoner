"""Focused tests for the Neural Architecture pulse marker layer."""

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
ASSETS_ROOT = BOX_ROOT / "assets"
CONTRACT_PATH = BOX_ROOT / "contract.py"
MARKERS_PATH = ASSETS_ROOT / "brain_visual_markers.py"
TEMPLATE_PATH = ASSETS_ROOT / "brain_visual_template.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorPulseMarkerLayerTests(unittest.TestCase):
    """Validate marker data, HTML behavior, and box boundaries."""

    def test_public_contract_exposes_marker_helpers_lazily(self) -> None:
        """The public contract should expose marker helpers without GUI imports."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.list_neural_architecture_pulse_markers))
        self.assertTrue(callable(contract.build_neural_architecture_marker_data_js))
        self.assertTrue(callable(contract.get_neural_architecture_pulse_marker_summary))

    def test_marker_regions_match_mapping_contract(self) -> None:
        """Every pulse marker should map to a known brain-region target."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            list_neural_architecture_pulse_markers,
        )
        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            list_brain_region_ids,
        )

        marker_ids = tuple(marker.region_id for marker in list_neural_architecture_pulse_markers())

        self.assertEqual(tuple(list_brain_region_ids()), marker_ids)

    def test_marker_data_is_pure_asset_without_gui_or_navigation_reach_in(self) -> None:
        """The marker module should not import GUI, registry, or navigation boxes."""

        text = MARKERS_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertNotIn("PySide6", imported_modules)
        self.assertNotIn("main_window", imported_modules)
        self.assertNotIn("tool_specs", imported_modules)
        self.assertNotIn("tab_navigation_controller", imported_modules)
        self.assertNotIn("brain_region_mapping", imported_modules)
        self.assertNotIn("setCurrentIndex", text)

    def test_contract_lazily_delegates_to_marker_asset(self) -> None:
        """The contract should import marker helpers only inside functions."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn(".assets.brain_visual_markers", top_level_imports)
        self.assertIn("from .assets.brain_visual_markers import", text)
        self.assertIn("list_neural_architecture_pulse_markers", text)

    def test_preview_html_contains_interactive_pulse_marker_layer(self) -> None:
        """The preview HTML should contain pulse markers and bridge calls."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("const NEURAL_ARCHITECTURE_PULSE_MARKERS", html)
        self.assertIn("createNeuralArchitecturePulseMarkers", html)
        self.assertIn("createNeuralArchitecturePulseMarker", html)
        self.assertIn("pulse-marker", html)
        self.assertIn("markerPulseSlow", html)
        self.assertIn("markerRippleSlow", html)
        self.assertIn("markerPulseFast", html)
        self.assertIn("markerRippleFast", html)
        self.assertIn("callBrainBridgeHover(markerData.region_id)", html)
        self.assertIn("callBrainBridgeOpenModule(windowData.region_id)", html)
        self.assertIn("window.brainNavigatorBridge.onRegionHovered", html)
        self.assertIn("window.brainNavigatorBridge.onRegionClicked", html)
        self.assertIn("showRegionTip(markerData.region_name", html)
        self.assertIn("applyMarkerScreenPosition", html)
        self.assertIn("updateProjectedMarkers()", html)
        self.assertNotIn("setCurrentIndex", html)

    def test_template_tracks_responsive_marker_creation(self) -> None:
        """The template should append markers to the stage and update on resize."""

        text = TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn("build_neural_architecture_marker_data_js", text)
        self.assertIn("stage.appendChild(marker.element)", text)
        self.assertIn("projectedMarkers.push(marker)", text)
        self.assertIn('window.addEventListener(\"resize\", resizeNeuralArchitectureStage)', text)
        self.assertIn("updateProjectedMarkers();", text)

    def test_manifest_tracks_pulse_marker_layer(self) -> None:
        """The Brain Navigator manifest should track Patch 10."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("assets/brain_visual_markers.py", manifest["private_internals"])
        self.assertIn(
            "list_neural_architecture_pulse_markers",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "tests/test_brain_navigator_pulse_marker_layer.py",
            manifest["validation"]["focused_tests"],
        )
        self.assertIn(
            "pulse_marker_layer_emits_region_id_to_web_bridge",
            manifest["communication_route"],
        )

    def test_readme_documents_marker_preview_state(self) -> None:
        """The README should document marker behavior and deferred floating windows."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Patch 10 - Responsive pulse marker layer", readme)
        self.assertIn("manual-preview-only pulse marker layer", readme)
        self.assertIn("dark blue slow pulsing circle", readme)
        self.assertIn("live red faster pulse", readme)
        self.assertIn("onRegionHovered(region_id)", readme)
        self.assertIn("floating Remember Box windows are intentionally deferred", readme)
        self.assertIn("does not switch tabs", readme)


if __name__ == "__main__":
    unittest.main()
