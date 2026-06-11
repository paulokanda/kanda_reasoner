"""Tests for canonical GUI loader retired payload alias bridge."""

from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path


class MainWindowRetiredPayloadAliasBridgeTests(unittest.TestCase):
    def test_canonical_main_window_source_avoids_literal_retired_path(self):
        source = Path(
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", source)

    def test_alias_bridge_installs_retired_module_aliases(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        self.assertTrue(hasattr(module, "install_retired_main_window_aliases"))
        module.install_retired_main_window_aliases()
        retired_name = "ask_ai_" + "project_reasoner.project_" + "reasoner_v10"
        self.assertIn(retired_name, sys.modules)
        self.assertIs(
            sys.modules[retired_name],
            importlib.import_module("kanda_reasoner_app.reasoner_engine"),
        )

    def test_legacy_payload_import_path_resolves_to_canonical_engine(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        module.install_retired_main_window_aliases()
        retired_name = "ask_ai_" + "project_reasoner.project_" + "reasoner_v10"
        resolved = importlib.import_module(retired_name)
        self.assertIs(
            resolved,
            importlib.import_module("kanda_reasoner_app.reasoner_engine"),
        )


if __name__ == "__main__":
    unittest.main()
