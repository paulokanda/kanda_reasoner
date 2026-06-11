"""Tests for dynamic Project Symbol Atlas package-path status checks."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FINAL_STATUS_PATH = Path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/final_status.py')
EVIDENCE_STATUS_PATH = Path(
    'ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/evidence_producer_status.py'
)
CHANGED_FILES = (FINAL_STATUS_PATH, EVIDENCE_STATUS_PATH)
LEGACY_PACKAGE_TOKEN = 'ask_' 'ai_project_reasoner'
PRODUCT_PACKAGE_PLACEHOLDER = "<PRODUCT_PACKAGE>"


class ProjectSymbolAtlasDynamicPackagePathTests(unittest.TestCase):
    """Validate project-agnostic Project Symbol Atlas status path handling."""

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed atlas status files should remain syntactically valid Python."""

        for relative_path in CHANGED_FILES:
            source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
            ast.parse(source, filename=str(relative_path))

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed atlas status files should not hardcode the legacy package token."""

        for relative_path in CHANGED_FILES:
            source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn(
                LEGACY_PACKAGE_TOKEN,
                source,
                msg=f"Legacy package token remains in {relative_path}",
            )

    def test_final_status_uses_product_package_placeholder_contract(self) -> None:
        """Final status expected-source paths should use a package placeholder."""

        source = (PROJECT_ROOT / FINAL_STATUS_PATH).read_text(encoding="utf-8")
        self.assertIn("PRODUCT_PACKAGE_PLACEHOLDER", source)
        self.assertIn(PRODUCT_PACKAGE_PLACEHOLDER, source)
        self.assertIn("_resolve_product_package_placeholders", source)

    def test_final_status_keeps_expected_files_without_fixed_package_root(self) -> None:
        """Final status file lists should keep file names separate from package root."""

        source = (PROJECT_ROOT / FINAL_STATUS_PATH).read_text(encoding="utf-8")
        self.assertIn("EXPECTED_PROJECT_SYMBOL_ATLAS_FILES", source)
        self.assertIn("EXPECTED_ADJACENT_PACKAGE_FILES", source)
        self.assertIn("relative_module.parts[0]", source)

    def test_evidence_status_uses_dynamic_product_package_root(self) -> None:
        """Evidence producer status should derive the product package root."""

        source = (PROJECT_ROOT / EVIDENCE_STATUS_PATH).read_text(encoding="utf-8")
        self.assertIn("_current_product_package_root", source)
        self.assertIn("relative_module.parts[0]", source)
        self.assertIn("reasoner_tools_gui_shell", source)


if __name__ == "__main__":
    unittest.main()
