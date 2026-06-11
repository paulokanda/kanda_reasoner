"""Regression tests for T10P027 stack compatibility import-smoke command."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.stack_compatibility.stack_briefs import (
    build_stack_compatibility_brief,
    render_stack_compatibility_markdown,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILE = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "stack_compatibility" / "stack_briefs.py"
LEGACY_IMPORT_SMOKE = 'import ask_' 'ai_project_reasoner'
CANONICAL_IMPORT_SMOKE = "import kanda_reasoner_app"


class StackCompatibilityCanonicalImportSmokeTests(unittest.TestCase):
    """Validate canonical stack compatibility smoke recommendations."""

    def test_stack_brief_recommends_canonical_import_smoke(self) -> None:
        """Observable report output should recommend canonical package import smoke."""
        report = build_stack_compatibility_brief(["pyside6==6.7.0"], python_version="3.12.0")
        tests_to_run = "\n".join(report.tests_to_run)

        self.assertIn(CANONICAL_IMPORT_SMOKE, tests_to_run)
        self.assertNotIn(LEGACY_IMPORT_SMOKE, tests_to_run)

    def test_markdown_output_uses_canonical_import_smoke(self) -> None:
        """Rendered Markdown should also use the canonical package import smoke."""
        report = build_stack_compatibility_brief(["numpy==1.26.0"])
        rendered = render_stack_compatibility_markdown(report)

        self.assertIn(CANONICAL_IMPORT_SMOKE, rendered)
        self.assertNotIn(LEGACY_IMPORT_SMOKE, rendered)

    def test_changed_file_does_not_hardcode_legacy_import_smoke(self) -> None:
        """Changed source should not hardcode the legacy import smoke command."""
        source = CHANGED_FILE.read_text(encoding="utf-8")

        self.assertNotIn(LEGACY_IMPORT_SMOKE, source)
        self.assertIn(CANONICAL_IMPORT_SMOKE, source)

    def test_changed_file_remains_ast_parseable(self) -> None:
        """Changed source should remain syntactically valid Python."""
        ast.parse(CHANGED_FILE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
