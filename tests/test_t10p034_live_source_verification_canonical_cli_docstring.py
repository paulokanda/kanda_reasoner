"""T10P034 live source verification canonical CLI docstring tests."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PACKAGE_TOKEN = "ask" + "_ai_project_reasoner"
CANONICAL_PACKAGE_TOKEN = "kanda_reasoner_app"
CHANGED_FILE = PROJECT_ROOT / LEGACY_PACKAGE_TOKEN / "live_source_verification" / "__init__.py"


class LiveSourceVerificationCanonicalCliDocstringTests(unittest.TestCase):
    """Validate the T10P034 live-source verification docstring cleanup."""

    def test_changed_file_exists(self) -> None:
        """The patched live source verification facade should exist."""
        self.assertTrue(CHANGED_FILE.exists(), str(CHANGED_FILE))

    def test_changed_file_remains_ast_parseable(self) -> None:
        """The patched facade should remain syntactically valid Python."""
        ast.parse(CHANGED_FILE.read_text(encoding="utf-8"))

    def test_changed_file_does_not_hardcode_legacy_package_token(self) -> None:
        """The patched facade should not retain the fixed legacy token."""
        text = CHANGED_FILE.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_PACKAGE_TOKEN, text)

    def test_cli_docstring_uses_canonical_package(self) -> None:
        """The user-facing module command should point to the canonical package."""
        text = CHANGED_FILE.read_text(encoding="utf-8")
        expected = (
            "python -m "
            + CANONICAL_PACKAGE_TOKEN
            + ".live_source_verification.verifier"
        )
        self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
