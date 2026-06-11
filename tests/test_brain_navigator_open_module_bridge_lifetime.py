"""Focused tests for Open module bridge lifetime hardening."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "brain_navigator"
VISIBLE_PATH = BOX_ROOT / "_visible_neural_architecture_tab.py"
PREVIEW_PATH = BOX_ROOT / "_neural_architecture_preview.py"


class BrainNavigatorOpenModuleBridgeLifetimeTests(unittest.TestCase):
    """Protect the runtime bridge references used by the Open module action."""

    def test_visible_tab_keeps_preview_bundle_alive(self) -> None:
        """The visible tab should retain the preview bundle after factory return."""

        text = VISIBLE_PATH.read_text(encoding="utf-8")

        self.assertIn('"_brain_navigator_preview_bundle"', text)
        self.assertIn('"_brain_navigator_open_tab_by_id"', text)
        self.assertIn("setattr(bundle.widget", text)
        self.assertIn("open_mapped_tab_by_region_id", text)
        self.assertNotIn("setCurrentIndex(", text)
        self.assertNotIn("import main_window", text)
        self.assertNotIn("from .main_window", text)
        self.assertNotIn("import tool_specs", text)

    def test_preview_keeps_qwebchannel_bridge_alive(self) -> None:
        """The preview should retain QWebChannel and QObject bridge references."""

        text = PREVIEW_PATH.read_text(encoding="utf-8")

        self.assertIn('"_brain_navigator_bridge_bundle"', text)
        self.assertIn("setattr(widget", text)
        self.assertIn("setattr(web_view", text)
        self.assertIn("bridge_bundle.connect_to_page(web_view.page())", text)
        self.assertNotIn("setCurrentIndex(", text)
        self.assertNotIn("import main_window", text)
        self.assertNotIn("from .main_window", text)
        self.assertNotIn("import tool_specs", text)


if __name__ == "__main__":
    unittest.main()
