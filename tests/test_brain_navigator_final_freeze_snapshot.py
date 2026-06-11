"""Final freeze snapshot tests for the Brain Navigator interaction chain."""

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
FREEZE_PATH = BOX_ROOT / "_freeze_snapshot.py"
VISIBLE_PATH = BOX_ROOT / "_visible_neural_architecture_tab.py"
PREVIEW_PATH = BOX_ROOT / "_neural_architecture_preview.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorFinalFreezeSnapshotTests(unittest.TestCase):
    """Protect the final Brain Navigator freeze snapshot."""

    def test_public_contract_exposes_final_freeze_snapshot(self) -> None:
        """The public contract should expose the final data-only snapshot."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_brain_navigator_freeze_snapshot,
        )

        snapshot = get_brain_navigator_freeze_snapshot()

        self.assertEqual("brain_navigator", snapshot.box_id)
        self.assertEqual("1.0", snapshot.contract_version)
        self.assertEqual(
            "final_brain_navigator_interaction_chain_frozen",
            snapshot.freeze_state,
        )
        self.assertIn(
            "marker_click_opens_floating_fancy_index_only",
            snapshot.frozen_flow,
        )
        self.assertIn(
            "open_module_button_emits_region_intent_through_qwebchannel",
            snapshot.frozen_flow,
        )
        self.assertIn(
            "mapped_tab_opens_through_injected_stable_tab_callback",
            snapshot.frozen_flow,
        )

    def test_final_flow_tokens_remain_in_html_and_python_bridge(self) -> None:
        """The final flow should remain wired from HTML to the kept-alive bridge."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()
        visible_text = VISIBLE_PATH.read_text(encoding="utf-8")
        preview_text = PREVIEW_PATH.read_text(encoding="utf-8")

        self.assertIn("showFloatingRememberWindow(markerData", html)
        self.assertIn("callBrainBridgeOpenModule(windowData.region_id)", html)
        self.assertIn("window.pendingBrainNavigatorOpenRegionId", html)
        self.assertIn("floating-remember-window-action", html)
        self.assertIn("data-region-id", html)
        self.assertIn("window.brainNavigatorBridge", html)
        self.assertIn("open_mapped_tab_by_region_id", visible_text)
        self.assertIn("_brain_navigator_preview_bundle", visible_text)
        self.assertIn("_brain_navigator_open_tab_by_id", visible_text)
        self.assertIn("_brain_navigator_bridge_bundle", preview_text)
        self.assertIn("bridge_bundle.connect_to_page(web_view.page())", preview_text)

    def test_snapshot_module_is_data_only_and_navigation_free(self) -> None:
        """The freeze snapshot should not own runtime GUI or navigation internals."""

        text = FREEZE_PATH.read_text(encoding="utf-8")

        self.assertNotIn("PySide6", text)
        self.assertNotIn("QWebEngine", text)
        self.assertNotIn("import main_window", text)
        self.assertNotIn("import tool_specs", text)
        self.assertNotIn("setCurrentIndex(", text)
        self.assertNotIn("import tab_navigation_controller", text)

    def test_manifest_and_readme_track_final_freeze_snapshot(self) -> None:
        """Manifest and README should document the final freeze state."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("get_brain_navigator_freeze_snapshot", manifest["public_contract"]["provides_functions"])
        self.assertIn("_freeze_snapshot.py", manifest["private_internals"])
        self.assertIn("final_freeze_snapshot_data_only", manifest["allowed_dependencies"])
        self.assertIn(
            "final_brain_navigator_freeze_snapshot_documents_validated_flow_without_runtime_change",
            manifest["communication_route"],
        )
        self.assertIn("tests/test_brain_navigator_final_freeze_snapshot.py", manifest["validation"]["focused_tests"])
        self.assertIn("Patch 19 - Final Brain Navigator freeze snapshot", readme)
        self.assertIn("Open module emits region intent through QWebChannel", readme)
        self.assertIn("navigation uses only the injected stable-tab callback", readme)


if __name__ == "__main__":
    unittest.main()
