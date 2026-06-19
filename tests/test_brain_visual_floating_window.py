"""Direct tests for Neural Architecture floating Remember Box data."""

from __future__ import annotations

import unittest


class BrainVisualFloatingWindowDirectTests(unittest.TestCase):
    """Validate floating Remember Box payloads and JS serialization."""

    def test_windows_are_complete_and_serialized_to_js(self) -> None:
        """The click window data should cover all initial brain-region IDs."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_visual_floating_window import (
            build_neural_architecture_floating_window_data_js,
            get_neural_architecture_floating_window_summary,
            list_neural_architecture_floating_windows,
        )

        windows = list_neural_architecture_floating_windows()
        summary = get_neural_architecture_floating_window_summary()
        payload = build_neural_architecture_floating_window_data_js()

        self.assertEqual(12, len(windows))
        self.assertEqual(12, summary.window_count)
        self.assertEqual(windows[0].region_id, summary.region_ids[0])
        self.assertIn("const NEURAL_ARCHITECTURE_FLOATING_WINDOWS", payload)
        self.assertIn("Architecture Review", payload)
        self.assertIn("Broca Area", payload)
        self.assertIn("Hippocampus", payload)
        self.assertIn("Open module", payload)
        self.assertIn("floating_fancy_index_with_controlled_open_module_action", summary.implementation_state)


if __name__ == "__main__":
    unittest.main()
