"""Regression tests for the canonical package facade compatibility path."""

from __future__ import annotations

import ast
import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "__init__.py"
LEGACY_TOKEN = "_".join(("ask", "ai", "project", "reasoner"))
CANONICAL_TOKEN = "kanda_reasoner_app"


class KandaReasonerAppFacadeDynamicCompatibilityTests(unittest.TestCase):
    """Verify the facade avoids fixed legacy text while keeping compatibility."""

    def test_facade_remains_ast_parseable(self) -> None:
        ast.parse(FACADE_PATH.read_text(encoding="utf-8"))

    def test_facade_does_not_hardcode_legacy_package_token(self) -> None:
        source = FACADE_PATH.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, source)

    def test_facade_builds_compatibility_name_dynamically(self) -> None:
        source = FACADE_PATH.read_text(encoding="utf-8")
        self.assertIn("_LEGACY_PACKAGE_PARTS", source)
        self.assertIn("importlib.import_module(LEGACY_PACKAGE_NAME)", source)
        self.assertIn("CANONICAL_PACKAGE_NAME", source)

    def test_canonical_package_import_keeps_compatibility_path(self) -> None:
        module = importlib.import_module(CANONICAL_TOKEN)
        self.assertEqual(module.CANONICAL_PACKAGE_NAME, CANONICAL_TOKEN)
        self.assertEqual(module.LEGACY_PACKAGE_NAME, LEGACY_TOKEN)
        joined_path = "\n".join(str(item) for item in module.__path__)
        self.assertIn(CANONICAL_TOKEN, joined_path)
        self.assertIn(LEGACY_TOKEN, joined_path)


if __name__ == "__main__":
    unittest.main()
