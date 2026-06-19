"""Direct protection tests for Neural Architecture pulse markers."""

from __future__ import annotations

import unittest


class BrainVisualMarkersDirectTests(unittest.TestCase):
    """Protect marker data as a pure visual asset."""

    def test_markers_are_complete_and_serialized_to_js(self) -> None:
        """The marker data should cover all initial brain-region IDs."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_visual_markers import (
            build_neural_architecture_marker_data_js,
            get_neural_architecture_pulse_marker_summary,
            list_neural_architecture_pulse_markers,
        )

        markers = list_neural_architecture_pulse_markers()
        summary = get_neural_architecture_pulse_marker_summary()
        marker_js = build_neural_architecture_marker_data_js()

        self.assertEqual(12, len(markers))
        self.assertEqual(12, summary.marker_count)
        self.assertEqual("neural_architecture_pulse_marker_layer", summary.box_id)
        self.assertEqual(
            "mesh_anchored_pulse_marker_layer",
            summary.implementation_state,
        )
        self.assertIn("const NEURAL_ARCHITECTURE_PULSE_MARKERS", marker_js)
        self.assertIn("frontal_lobe", marker_js)
        self.assertIn("broca_area", marker_js)
        self.assertIn("hippocampus", marker_js)
        self.assertIn("longitudinal_fissure", marker_js)
        self.assertIn("dark_blue_slow_pulsing_circle", marker_js)
        self.assertIn("live_red_fast_pulsing_circle", marker_js)
        self.assertIn("anchor_z", marker_js)
        self.assertIn("surface_cloud", marker_js)


if __name__ == "__main__":
    unittest.main()
