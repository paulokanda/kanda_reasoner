"""T10P016 tests for Tab 1 audit write support canonical imports."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAB1_SUPPORT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "tab1_audit_write_support"
PLANNING_PATH = TAB1_SUPPORT / "planning.py"
WORKER_PATH = TAB1_SUPPORT / "worker.py"
CHANGED_FILES = (
    PLANNING_PATH,
    WORKER_PATH,
)


class Tab1AuditWriteSupportCanonicalImportTests(unittest.TestCase):
    """Validate canonical package references in Tab 1 audit write support."""

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed Tab 1 audit support files should not contain the legacy token."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed Tab 1 audit support files should remain syntactically valid."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))

    def test_contract_imports_use_canonical_package(self) -> None:
        """Contract module import construction should use kanda_reasoner_app."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertIn('"kanda_reasoner_app"', source, path.as_posix())
            self.assertIn('"tab1_audit_write_contracts"', source, path.as_posix())

    def test_worker_backend_import_uses_canonical_package(self) -> None:
        """Worker backend import construction should use kanda_reasoner_app."""
        source = WORKER_PATH.read_text(encoding="utf-8")
        self.assertIn('"kanda_reasoner_app", package_part, module_part', source)


if __name__ == "__main__":
    unittest.main()
