"""Direct protection tests for Brain Navigator visual spec assets."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_visual_spec import get_neural_architecture_visual_spec


class BrainVisualSpecDirectTests(unittest.TestCase):
    """Protect the frozen Neural Architecture visual spec."""

    def test_spec_contains_title_footer_and_responsive_requirements(self) -> None:
        """The visual spec should preserve the frozen user requirements."""

        spec = get_neural_architecture_visual_spec()
        self.assertEqual("Neural Architecture", spec.title_lines[0])
        self.assertIn("Knowledge and Architecture Navigator", spec.title_lines[2])
        self.assertEqual(
            "What is the airspeed velocity of an unladen swallow?",
            spec.footer_text,
        )
        self.assertIn("fill_available_tab_space", spec.responsive_requirements)
        self.assertIn("live_red_fast_pulse_on_hover", spec.marker_behavior)


if __name__ == "__main__":
    unittest.main()
