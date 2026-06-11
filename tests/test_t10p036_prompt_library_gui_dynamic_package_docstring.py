"""Regression tests for T10P036 prompt library GUI dynamic package docstring."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "prompt_library_gui" / "library_paths.py"
LEGACY_PACKAGE_TOKEN = 'ask_' 'ai_project_reasoner'


class PromptLibraryGuiDynamicPackageDocstringTests(unittest.TestCase):
    """Validate the prompt library GUI path helper cleanup."""

    def test_source_file_exists(self) -> None:
        """The patched source file should exist."""
        self.assertTrue(SOURCE_PATH.exists(), SOURCE_PATH)

    def test_source_remains_ast_parseable(self) -> None:
        """The changed source should remain syntactically valid Python."""
        ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))

    def test_source_does_not_hardcode_legacy_package_token(self) -> None:
        """The changed source should not retain the fixed legacy package token."""
        source_text = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_PACKAGE_TOKEN, source_text)

    def test_package_root_is_derived_from_file_location(self) -> None:
        """package_root should still derive the package folder from __file__."""
        module = importlib.import_module(
            "kanda_reasoner_app.prompt_library_gui.library_paths"
        )
        package_root = module.package_root()

        self.assertEqual(package_root.name, 'ask_' 'ai_project_reasoner')
        self.assertEqual(package_root.parent, PROJECT_ROOT)


if __name__ == "__main__":
    unittest.main()
