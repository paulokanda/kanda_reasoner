"""Direct protection tests for Brain Navigator visual template assets."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_visual_template import build_neural_architecture_asset_preview_html


class BrainVisualTemplateDirectTests(unittest.TestCase):
    """Protect the inert Neural Architecture HTML asset template."""

    def test_template_contains_resize_and_marker_contract(self) -> None:
        """The template should preserve resize, marker, and floating-window tokens."""

        html = build_neural_architecture_asset_preview_html()
        self.assertIn("window.addEventListener", html)
        self.assertIn("renderer.setSize(width, height)", html)
        self.assertIn("camera.updateProjectionMatrix()", html)
        self.assertIn("pulse-marker", html)
        self.assertIn("floatingRegionWindow", html)
        self.assertIn("What is the airspeed velocity", html)


if __name__ == "__main__":
    unittest.main()
