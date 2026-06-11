"""Focused tests for Brain Navigator visual fit and mesh-anchored anatomy correction."""

from __future__ import annotations

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
TEMPLATE_PATH = ASSETS_ROOT / "brain_visual_template.py"
MARKERS_PATH = ASSETS_ROOT / "brain_visual_markers.py"
README_PATH = BOX_ROOT / "README.md"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"


class BrainNavigatorVisualFitAndAnatomyCorrectionTests(unittest.TestCase):
    """Protect the visual fit and corrected marker anatomy patch."""

    def test_template_keeps_seventy_percent_brain_fit_scale(self) -> None:
        """The visible brain should stay about 30 percent smaller than before."""

        text = TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn("const BRAIN_REFERENCE_SCALE_BEFORE_FIT_PATCH = 1.70", text)
        self.assertIn("const BRAIN_RENDER_SCALE = BRAIN_REFERENCE_SCALE_BEFORE_FIT_PATCH * 0.70", text)
        self.assertIn("const BRAIN_GHOST_SPHERE_RADIUS = 1.34", text)
        self.assertIn("const scale = BRAIN_RENDER_SCALE", text)
        self.assertNotIn("const scale = 1.70", text)

    def test_template_restores_original_mesh_colors(self) -> None:
        """The incorrect yellow occipital overlay should be removed."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("const TELENCEPHALON_COLOR = 0x005cff", html)
        self.assertIn("const CEREBELLUM_COLOR = 0x00aa40", html)
        self.assertIn("const MIDBRAIN_COLOR = 0xff8400", html)
        self.assertNotIn("OCCIPITAL_LOBE_COLOR", html)
        self.assertNotIn("filterLikelyOccipitalTelencephalon", html)
        self.assertNotIn("brainContent.add(occipitalPts)", html)

    def test_marker_data_uses_mesh_anchored_anatomical_coordinates(self) -> None:
        """Markers should use 3D anchors, not only fixed screen percentages."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            list_neural_architecture_pulse_markers,
        )

        markers = {marker.region_id: marker for marker in list_neural_architecture_pulse_markers()}

        self.assertGreater(markers["frontal_lobe"].anchor_z, markers["central_sulcus"].anchor_z)
        self.assertGreater(markers["central_sulcus"].anchor_z, markers["parietal_lobe"].anchor_z)
        self.assertGreater(markers["parietal_lobe"].anchor_z, markers["occipital_lobe"].anchor_z)
        self.assertLess(markers["cerebellum"].anchor_y, markers["occipital_lobe"].anchor_y)
        self.assertEqual("cerebellum", markers["cerebellum"].surface_cloud)
        self.assertEqual("cerebellum", markers["cerebellar_folia"].surface_cloud)
        self.assertEqual("midbrain", markers["brainstem_midbrain"].surface_cloud)
        self.assertEqual(0, markers["longitudinal_fissure"].preferred_side)

    def test_template_projects_markers_from_mesh_coordinates_each_frame(self) -> None:
        """The DOM markers should be glued to projected mesh coordinates."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("resolveMarkerSurfaceAnchorLocal(markerData)", html)
        self.assertIn("nearestSurfacePoint(target, cloud", html)
        self.assertIn("projectBrainLocalPointToScreen(anchorLocal)", html)
        self.assertIn("brain.localToWorld(point)", html)
        self.assertIn("updateProjectedMarkers();\n    renderer.render", html)
        self.assertIn("x = right-left hemisphere side, y = superior-inferior, z = anterior-posterior", MARKERS_PATH.read_text(encoding="utf-8"))

    def test_visual_spec_tracks_restored_colors_and_mesh_anchor_requirements(self) -> None:
        """The visual contract should preserve the corrected mesh-anchor requirements."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_neural_architecture_visual_spec,
        )

        spec = get_neural_architecture_visual_spec()

        self.assertIn("render_brain_about_30_percent_smaller_for_complete_fit", spec.responsive_requirements)
        self.assertIn("restore_original_mesh_colors_after_axis_correction", spec.responsive_requirements)
        self.assertIn("treat_model_x_as_left_right_and_z_as_anterior_posterior", spec.responsive_requirements)
        self.assertIn("snap_pulse_markers_to_mesh_surface_and_project_each_frame", spec.responsive_requirements)
        self.assertEqual(
            "visible_neural_architecture_with_restored_colors_and_mesh_anchored_markers",
            spec.current_integration_state,
        )

    def test_readme_and_manifest_track_mesh_anchored_correction_patch(self) -> None:
        """Docs and manifest should track the corrected visual patch."""

        readme = README_PATH.read_text(encoding="utf-8")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertIn("Patch 14 - Restored colors and mesh-anchored anatomy markers", readme)
        self.assertIn("x is\nhemisphere side, y is superior-inferior, and z is anterior-posterior", readme)
        self.assertIn("markers are snapped to the mesh and\nprojected every frame", readme)
        self.assertIn("original mesh colors", readme)
        self.assertIn(
            "tests/test_brain_navigator_visual_fit_and_anatomy_correction.py",
            manifest["validation"]["focused_tests"],
        )
        self.assertIn(
            "mesh_anchored_markers_restore_original_colors_without_navigation",
            manifest["communication_route"],
        )

    def test_marker_asset_remains_free_of_navigation_reach_in(self) -> None:
        """The correction should not add navigation or GUI reach-in to marker assets."""

        text = MARKERS_PATH.read_text(encoding="utf-8")

        self.assertNotIn("main_window", text)
        self.assertNotIn("tool_specs", text)
        self.assertNotIn("tab_navigation_controller", text)
        self.assertNotIn("setCurrentIndex", text)


if __name__ == "__main__":
    unittest.main()
