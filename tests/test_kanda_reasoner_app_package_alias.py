"""Tests for the staged canonical package rename."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class KandaReasonerAppPackageAliasTests(unittest.TestCase):
    """Cover the canonical package facade before full import migration."""

    def test_canonical_package_imports(self) -> None:
        package = importlib.import_module("kanda_reasoner_app")

        self.assertEqual("kanda_reasoner_app", package.CANONICAL_PACKAGE_NAME)
        self.assertEqual('ask_' 'ai_project_reasoner', package.LEGACY_PACKAGE_NAME)

    def test_canonical_submodule_import_resolves_project_root_resolver(self) -> None:
        module = importlib.import_module("kanda_reasoner_app.project_root_resolver")

        self.assertTrue(module.is_reasoner_project_root(Path.cwd()))

    def test_root_gui_launcher_uses_canonical_package_path(self) -> None:
        module = importlib.import_module("reasoner_tools_gui")

        self.assertIn("main", module.__all__)
        self.assertTrue(callable(module.main))


if __name__ == "__main__":
    unittest.main()
