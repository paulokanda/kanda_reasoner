"""Regression tests for T10P028 validation log canonicalization."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_FILES = [
    PROJECT_ROOT / "validation" / "jsonctx002a_architecture_validate.txt",
    PROJECT_ROOT / "validation" / "JSONCTX002A_VALIDATION.md",
    PROJECT_ROOT / "validation" / "jsonctx002a_workflow_validate.txt",
]
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'
CANONICAL_TOKEN = "kanda_reasoner_app"
LEGACY_PLACEHOLDER = "<LEGACY_PRODUCT_PACKAGE>"


class ValidationCanonicalLogReferenceTests(unittest.TestCase):
    """Validate project-agnostic validation evidence references."""

    def test_validation_files_exist(self) -> None:
        """All validation files covered by this patch should exist."""
        for path in VALIDATION_FILES:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), str(path))

    def test_validation_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Validation text should not keep hardcoded legacy package references."""
        for path in VALIDATION_FILES:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8", errors="replace")
                self.assertNotIn(LEGACY_TOKEN, text)

    def test_validation_command_examples_use_canonical_cli_paths(self) -> None:
        """Runnable validation command examples should use canonical CLI paths."""
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace") for path in VALIDATION_FILES
        )

        self.assertIn(
            "kanda_reasoner_app/manage_architecture/manage_architecture.py",
            text,
        )
        self.assertIn(
            "kanda_reasoner_app/manage_workflows/manage_workflows.py",
            text,
        )
        self.assertIn(CANONICAL_TOKEN, text)

    def test_historical_legacy_paths_use_placeholder(self) -> None:
        """Historical warnings may mention legacy scope only through a placeholder."""
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace") for path in VALIDATION_FILES
        )

        self.assertIn(LEGACY_PLACEHOLDER, text)


if __name__ == "__main__":
    unittest.main()
