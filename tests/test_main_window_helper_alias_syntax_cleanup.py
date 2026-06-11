"""Focused syntax cleanup tests for canonical main window helper alias bridge."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class MainWindowHelperAliasSyntaxCleanupTests(unittest.TestCase):
    """Protect the canonical GUI module after helper alias insertion."""

    def test_canonical_main_window_source_has_valid_function_headers(self):
        source_path = Path(
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
        )
        text = source_path.read_text(encoding="utf-8")
        self.assertNotIn("def def ", text)
        self.assertIn(
            "def install_canonical_main_window_helper_package_aliases()", text
        )
        self.assertIn("def install_retired_main_window_aliases()", text)

    def test_canonical_main_window_imports_after_syntax_cleanup(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        self.assertTrue(
            hasattr(module, "install_canonical_main_window_helper_package_aliases")
        )

    def test_helper_alias_package_resolves_to_canonical_package(self):
        importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        alias = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.main_window_help"
        )
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
        )
        self.assertIs(alias, canonical)


if __name__ == "__main__":
    unittest.main()
