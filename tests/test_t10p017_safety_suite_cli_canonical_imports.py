"""Tests for T10P017 safety-suite CLI canonical imports."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = (
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "safety_suite_cli" / "commands.py",
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "safety_suite_cli"
    / "reasoner_symbol_atlas_commands.py",
)


class SafetySuiteCliCanonicalImportTests(unittest.TestCase):
    """Validate safety-suite CLI package-name migration."""

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed safety-suite files should not contain the legacy token."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed files should remain syntactically valid Python."""
        for path in CHANGED_FILES:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_safety_suite_cli_imports_use_canonical_package(self) -> None:
        """Safety-suite CLI imports should route through kanda_reasoner_app."""
        source = (
            PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "safety_suite_cli" / "commands.py"
        ).read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app.safety_suite_cli", source)
        self.assertIn("kanda_reasoner_app.engineering_safety", source)
        self.assertIn("kanda_reasoner_app.governance_automation", source)
        self.assertIn("kanda_reasoner_app.source_hygiene", source)

    def test_reasoner_symbol_atlas_cli_imports_use_canonical_package(self) -> None:
        """Project Symbol Atlas CLI imports should route through kanda_reasoner_app."""
        source = (
            PROJECT_ROOT
            / 'ask_' 'ai_project_reasoner'
            / "safety_suite_cli"
            / "reasoner_symbol_atlas_commands.py"
        ).read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app.reasoner_symbol_atlas", source)
        self.assertNotIn('from ask_' 'ai_project_reasoner', source)


if __name__ == "__main__":
    unittest.main()
