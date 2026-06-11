"""Focused tests for Brain Navigator mesh-anchor marker refinement."""

from __future__ import annotations

import unittest


class BrainNavigatorMeshAnchorMarkerRefinementTests(unittest.TestCase):
    """Protect the refined anatomical marker anchors after manual GUI review."""

    def test_refined_marker_positions_match_requested_anatomical_shift(self) -> None:
        """The refined markers should reflect the manual GUI correction feedback."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            list_neural_architecture_pulse_markers,
        )

        markers = {marker.region_id: marker for marker in list_neural_architecture_pulse_markers()}

        self.assertGreater(markers["frontal_lobe"].anchor_z, 0.50)
        self.assertLess(markers["parietal_lobe"].anchor_y, 0.34)
        self.assertLess(markers["parietal_lobe"].anchor_y, markers["central_sulcus"].anchor_y)
        self.assertLess(markers["brainstem_midbrain"].anchor_y, -0.30)
        self.assertLess(markers["occipital_lobe"].anchor_y, 0.10)
        self.assertLess(markers["occipital_lobe"].anchor_z, -0.55)
        self.assertLess(markers["cerebellum"].anchor_y, markers["occipital_lobe"].anchor_y)
        self.assertEqual(0, markers["cerebellum"].preferred_side)
        self.assertEqual("cerebellum", markers["cerebellum"].surface_cloud)
        self.assertEqual("cerebellum", markers["cerebellar_folia"].surface_cloud)
        self.assertLess(markers["cerebellar_folia"].anchor_y, -0.40)

    def test_marker_asset_remains_navigation_free(self) -> None:
        """The refinement patch must remain data-only and navigation free."""

        from pathlib import Path

        marker_path = Path(__file__).resolve().parents[1] / (
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_markers.py"
        )
        text = marker_path.read_text(encoding="utf-8")

        self.assertNotIn("setCurrentIndex", text)
        self.assertNotIn("main_window", text)
        self.assertNotIn("tool_specs", text)
        self.assertNotIn("tab_navigation_controller", text)


if __name__ == "__main__":
    unittest.main()
