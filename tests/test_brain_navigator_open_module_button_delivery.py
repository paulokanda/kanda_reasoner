"""Focused tests for robust Open module button delivery."""

from __future__ import annotations

import unittest


class BrainNavigatorOpenModuleButtonDeliveryTests(unittest.TestCase):
    """Protect the Fancy Index button from being a dead text label."""

    def test_open_module_button_is_explicit_clickable_control(self) -> None:
        """The floating index should render an accessible, clickable button."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn('type="button" class="floating-remember-window-action"', html)
        self.assertIn('title="Open mapped module"', html)
        self.assertIn('aria-label="Open mapped module"', html)
        self.assertIn('pointer-events: auto', html)
        self.assertIn('cursor: pointer', html)
        self.assertIn('callBrainBridgeOpenModule(windowData.region_id)', html)
        self.assertIn('actionButton.dataset.lastDeliveryState', html)

    def test_open_module_delivery_retries_while_bridge_connects(self) -> None:
        """The button should retry briefly if QWebChannel is not connected yet."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn('return true;', html)
        self.assertIn('return false;', html)
        self.assertIn('window.pendingBrainNavigatorOpenRegionId', html)
        self.assertIn('Bridge connecting - click again', html)
        self.assertIn('Opening mapped module', html)
        self.assertIn('window.setTimeout(function()', html)

    def test_marker_click_still_opens_floating_map_not_immediate_navigation(self) -> None:
        """Marker click should open the map; only the button requests navigation."""

        from pathlib import Path

        template_path = Path(__file__).resolve().parents[1] / (
            'kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_template.py'
        )
        text = template_path.read_text(encoding='utf-8')

        self.assertIn('showFloatingRememberWindow(markerData, event.clientX, event.clientY)', text)
        self.assertNotIn('callBrainBridgeOpenModule(markerData.region_id)', text)
        self.assertNotIn('callBrainBridgeClick(markerData.region_id)', text)


if __name__ == "__main__":
    unittest.main()
