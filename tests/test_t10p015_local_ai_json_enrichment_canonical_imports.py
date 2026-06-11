"""T10P015 tests for Local-AI JSON Enrichment canonical imports."""

from __future__ import annotations

import ast
import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INIT_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "local_ai_json_enrichment" / "__init__.py"
WRITER_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "local_ai_json_enrichment" / "enrichment_writer.py"
CHANGED_FILES = (
    INIT_PATH,
    WRITER_PATH,
)


class LocalAIJsonEnrichmentCanonicalImportTests(unittest.TestCase):
    """Validate canonical package references for Local-AI JSON Enrichment."""

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed enrichment files should not contain the legacy package token."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed enrichment files should remain syntactically valid Python."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))

    def test_enrichment_writer_imports_use_canonical_package(self) -> None:
        """The enrichment writer should import dependencies through kanda_reasoner_app."""
        source = WRITER_PATH.read_text(encoding="utf-8")
        self.assertIn("from kanda_reasoner_app.live_source_verification import", source)
        self.assertIn("from kanda_reasoner_app.local_ai_json_working_copy import", source)

    def test_legacy_enrichment_package_still_exposes_public_api_names(self) -> None:
        """The legacy package path should still expose stable public API names."""
        module = importlib.import_module("kanda_reasoner_app.local_ai_json_enrichment")
        self.assertIn("DEFAULT_ENRICHMENT_KEY", module.__all__)
        self.assertIn("enrich_local_ai_json_with_live_sources", module.__all__)


if __name__ == "__main__":
    unittest.main()
