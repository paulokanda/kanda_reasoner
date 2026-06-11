"""Focused tests for Brain Navigator neural architecture asset extraction."""

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
ASSET_ROOT = BOX_ROOT / "assets"
MESH_PATH = ASSET_ROOT / "brain_mesh_data.py"
SPEC_PATH = ASSET_ROOT / "brain_visual_spec.py"
TEMPLATE_PATH = ASSET_ROOT / "brain_visual_template.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorAssetExtractionTests(unittest.TestCase):
    """Validate extracted visual assets without changing visible GUI behavior."""

    def test_public_contract_exposes_asset_helpers_lazily(self) -> None:
        """The public contract should expose asset helpers without GUI imports."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.get_brain_mesh_data_summary))
        self.assertTrue(callable(contract.get_brain_mesh_data_js))
        self.assertTrue(callable(contract.get_neural_architecture_visual_spec))
        self.assertTrue(callable(contract.build_neural_architecture_asset_preview_html))

    def test_contract_has_no_top_level_asset_or_gui_imports(self) -> None:
        """The contract should import asset internals only inside functions."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn("PySide6", top_level_imports)
        self.assertNotIn(".assets.brain_mesh_data", top_level_imports)
        self.assertNotIn(".assets.brain_visual_template", top_level_imports)
        self.assertIn("from .assets.brain_mesh_data import", text)
        self.assertIn("from .assets.brain_visual_template import", text)

    def test_mesh_asset_summary_matches_uploaded_model_metadata(self) -> None:
        """The mesh asset should preserve source metadata from the uploaded model."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_brain_mesh_data_js,
            get_brain_mesh_data_summary,
        )

        summary = get_brain_mesh_data_summary()
        mesh_js = get_brain_mesh_data_js()

        self.assertEqual(
            "brain_dashboard_pyside_25fps_anatomy_v5_hover_tooltip_fixed_visible.py",
            summary.source_file,
        )
        self.assertEqual("male_brain.glb", summary.model_name)
        self.assertEqual(2605, summary.source_vertex_count)
        self.assertEqual(4850, summary.source_face_count)
        self.assertEqual(9255, summary.surface_dot_count)
        self.assertEqual(3724, summary.visible_edge_count)
        self.assertEqual("extracted_inert_asset_not_visible_yet", summary.implementation_state)
        self.assertIn("const TEL_PTS", mesh_js)
        self.assertIn("const CERB_PTS", mesh_js)
        self.assertIn("const MID_PTS", mesh_js)
        self.assertIn("const EDGE_PTS", mesh_js)

    def test_visual_spec_freezes_title_footer_markers_and_resize_requirements(self) -> None:
        """The visual spec should capture the user's final brain-tab requirements."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_neural_architecture_visual_spec,
        )

        spec = get_neural_architecture_visual_spec()

        self.assertEqual("brain_neural_architecture_visual_asset", spec.box_id)
        self.assertEqual(
            (
                "Neural Architecture",
                "of",
                "Knowledge and Architecture Navigator for Developer Assistance (KANDA)",
            ),
            spec.title_lines,
        )
        self.assertEqual(
            "What is the airspeed velocity of an unladen swallow?",
            spec.footer_text,
        )
        self.assertIn("neural_architecture_brain", spec.visual_modes)
        self.assertIn("fill_available_tab_space", spec.responsive_requirements)
        self.assertIn("update_camera_aspect_on_window_resize", spec.responsive_requirements)
        self.assertIn(
            "recalculate_projected_marker_positions_on_resize",
            spec.responsive_requirements,
        )
        self.assertIn("dark_blue_slow_pulsing_circle_default", spec.marker_behavior)
        self.assertIn("live_red_fast_pulse_on_hover", spec.marker_behavior)
        self.assertEqual(
            "visible_neural_architecture_with_restored_colors_and_mesh_anchored_markers",
            spec.current_integration_state,
        )

    def test_asset_preview_html_contains_mesh_visual_tokens_and_responsive_contract(self) -> None:
        """The inert preview HTML should assemble visual assets for later preview."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_asset_preview_html,
        )

        html = build_neural_architecture_asset_preview_html()

        self.assertIn("Neural Architecture", html)
        self.assertIn(
            "Knowledge and Architecture Navigator for Developer Assistance (KANDA)",
            html,
        )
        self.assertIn("What is the airspeed velocity of an unladen swallow?", html)
        self.assertIn("qrc:///qtwebchannel/qwebchannel.js", html)
        self.assertIn("const SOURCE_VERTEX_COUNT = 2605", html)
        self.assertIn("const SURFACE_DOT_COUNT = 9255", html)
        self.assertIn("pulse-marker", html)
        self.assertIn("markerPulseSlow", html)
        self.assertIn("markerPulseFast", html)
        self.assertIn("#floatingRegionWindow", html)
        self.assertIn("window.addEventListener(\"resize\", resizeNeuralArchitectureStage)", html)
        self.assertIn("renderer.setSize(width, height)", html)
        self.assertIn("camera.aspect = width / height", html)
        self.assertIn("camera.updateProjectionMatrix()", html)
        self.assertIn("updateProjectedMarkers()", html)
        self.assertNotIn("setCurrentIndex", html)


    def test_asset_modules_import_directly_without_gui_deps(self) -> None:
        """Asset modules should be importable directly for protection tracking."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets import (
            brain_mesh_data,
            brain_visual_spec,
            brain_visual_template,
        )

        self.assertEqual(2605, brain_mesh_data.get_brain_mesh_data_summary().source_vertex_count)
        self.assertEqual(
            "brain_neural_architecture_visual_asset",
            brain_visual_spec.get_neural_architecture_visual_spec().box_id,
        )
        self.assertTrue(callable(brain_visual_template.build_neural_architecture_asset_preview_html))

    def test_asset_modules_have_no_gui_or_navigation_reach_in(self) -> None:
        """Asset modules should stay data/template only."""

        for path in (MESH_PATH, SPEC_PATH, TEMPLATE_PATH):
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
            imported_modules: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_modules.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_modules.add(node.module)

            self.assertNotIn("PySide6", imported_modules)
            self.assertNotIn("PySide6.QtWebEngineWidgets", imported_modules)
            self.assertNotIn("main_window", imported_modules)
            self.assertNotIn("tool_specs", imported_modules)
            self.assertNotIn("tab_navigation_controller", imported_modules)
            self.assertNotIn("setCurrentIndex", text)
            self.assertNotIn("self.tabs", text)

    def test_manifest_tracks_asset_extraction(self) -> None:
        """The Brain Navigator manifest should track the extracted assets."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("assets/brain_mesh_data.py", manifest["private_internals"])
        self.assertIn("assets/brain_visual_spec.py", manifest["private_internals"])
        self.assertIn("assets/brain_visual_template.py", manifest["private_internals"])
        self.assertIn(
            "get_neural_architecture_visual_spec",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "tests/test_brain_navigator_asset_extraction.py",
            manifest["validation"]["focused_tests"],
        )
        self.assertIn(
            "neural_architecture_asset_extraction_not_visible_yet",
            manifest["communication_route"],
        )

    def test_readme_documents_asset_extraction_and_responsive_requirement(self) -> None:
        """The README should document Patch 8 and the resizing rule."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Patch 8 - Brain asset extraction", readme)
        self.assertIn("not wired into the visible first tab", readme)
        self.assertIn("Neural Architecture", readme)
        self.assertIn("What is the airspeed velocity of an unladen swallow?", readme)
        self.assertIn("fit the available tab space", readme)
        self.assertIn("window.addEventListener", readme)


if __name__ == "__main__":
    unittest.main()
