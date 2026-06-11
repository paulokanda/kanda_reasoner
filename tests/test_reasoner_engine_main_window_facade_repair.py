"""Regression tests for the canonical main window module.

The canonical module was first introduced as a facade, then promoted to a
real copied GUI module. The public contract may expose __all__ as either a
list or a tuple, matching normal Python module conventions.
"""

from __future__ import annotations

import importlib
import unittest


class ReasonerEngineMainWindowFacadeRepairTests(unittest.TestCase):
    """Protect canonical and legacy main window import contracts."""

    def test_canonical_main_window_imports(self) -> None:
        """The canonical main window module must be importable."""
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        self.assertIsNotNone(module)

    def test_canonical_public_contract_is_sequence(self) -> None:
        """The canonical module should expose a public __all__ contract."""
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        public_names = getattr(module, "__all__", ())
        self.assertIsInstance(public_names, (list, tuple))
        self.assertIn("JsonProjectReasonerV10", public_names)

    def test_canonical_helpers_still_import(self) -> None:
        """The canonical helper package must remain importable."""
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
        )
        self.assertIsNotNone(module)

    def test_legacy_gui_window_still_imports(self) -> None:
        """The active legacy GUI module must remain available."""
        module = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window"
        )
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
