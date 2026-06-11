"""Tests for the canonical main window helper package alias bridge."""

from __future__ import annotations

import importlib
import sys
import unittest


class MainWindowHelperPackageAliasBridgeTests(unittest.TestCase):
    """Protect the alias needed by embedded main-window payload imports."""

    def test_helper_package_alias_resolves_after_main_window_import(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        self.assertIsNotNone(module)

        alias_name = "kanda_reasoner_app.reasoner_engine.main_window_help"
        canonical_name = (
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
        )

        self.assertIn(alias_name, sys.modules)
        self.assertIs(sys.modules[alias_name], sys.modules[canonical_name])

    def test_alias_ui_components_import_resolves(self):
        importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )

        alias_module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.main_window_help.ui_components"
        )
        self.assertIsNotNone(alias_module)

    def test_canonical_source_does_not_reference_retired_engine_package(self):
        path = "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()

        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)


if __name__ == "__main__":
    unittest.main()
