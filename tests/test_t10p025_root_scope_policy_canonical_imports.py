"""Regression tests for T10P025 root scope policy canonical imports."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = (
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "project_exclusion_policy.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "project_json_scope_filter.py",
)


class RootScopePolicyCanonicalImportTests(unittest.TestCase):
    """Validate canonical import routing for root scope policy helpers."""

    def _read(self, relative_path: str) -> str:
        return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed files should remain syntactically valid Python."""
        for path in CHANGED_FILES:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_changed_files_do_not_use_legacy_from_imports(self) -> None:
        """Changed files should not import dependencies through the legacy package."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('from ask_' 'ai_project_reasoner', source)

    def test_project_exclusion_policy_imports_use_canonical_package(self) -> None:
        """Project exclusion policy should import root detection via kanda_reasoner_app."""
        source = self._read('ask_' 'ai_project_reasoner' '/project_exclusion_policy.py')
        self.assertIn(
            "from kanda_reasoner_app.project_root_resolver import is_reasoner_project_root",
            source,
        )

    def test_project_json_scope_filter_imports_use_canonical_package(self) -> None:
        """Project JSON scope filter should import policy helpers via kanda_reasoner_app."""
        source = self._read('ask_' 'ai_project_reasoner' '/project_json_scope_filter.py')
        self.assertIn(
            "from kanda_reasoner_app.project_exclusion_policy import (",
            source,
        )


if __name__ == "__main__":
    unittest.main()
