"""Direct tests for floating Remember Box template fragments."""

from __future__ import annotations

import unittest


class BrainVisualFloatingWindowTemplateDirectTests(unittest.TestCase):
    """Validate CSS and JS fragments used by the brain visual template."""

    def test_css_and_runtime_js_fragments_are_available(self) -> None:
        """The fragment module should expose stable floating-window tokens."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets.brain_visual_floating_window_template import (
            build_floating_remember_window_css,
            build_floating_remember_window_runtime_js,
        )

        css = build_floating_remember_window_css()
        js = build_floating_remember_window_runtime_js()

        self.assertIn("#floatingRegionWindow", css)
        self.assertIn("floating-remember-window-title", css)
        self.assertIn("showFloatingRememberWindow", js)
        self.assertIn("hideFloatingRememberWindow", js)
        self.assertIn("findFloatingRememberWindowData", js)
        self.assertIn("positionFloatingRememberWindow", js)
        self.assertNotIn("setCurrentIndex", js)


if __name__ == "__main__":
    unittest.main()
