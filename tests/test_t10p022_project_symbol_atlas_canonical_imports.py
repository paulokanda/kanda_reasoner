"""Regression tests for Project Symbol Atlas canonical import migration."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = (
    Path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/complete_json_adapter.py'),
    Path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/evidence_migration.py'),
    Path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/evidence_producer_status.py'),
    Path('ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/report_writer.py'),
)
LEGACY_IMPORT_PREFIX = 'from ask_' 'ai_project_reasoner'
CANONICAL_IMPORT_PREFIX = "from kanda_reasoner_app"


class ProjectSymbolAtlasCanonicalImportTests(unittest.TestCase):
    """Validate canonical imports for remaining Project Symbol Atlas helpers."""

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed atlas files should remain syntactically valid Python."""

        for relative_path in CHANGED_FILES:
            source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
            ast.parse(source, filename=str(relative_path))

    def test_changed_files_do_not_use_legacy_from_imports(self) -> None:
        """Changed atlas files should not use legacy package from-imports."""

        for relative_path in CHANGED_FILES:
            source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn(
                LEGACY_IMPORT_PREFIX,
                source,
                msg=f"Legacy package from-import remains in {relative_path}",
            )

    def test_changed_files_use_canonical_imports(self) -> None:
        """Changed atlas files should import dependencies through kanda_reasoner_app."""

        expected_files = {
            "complete_json_adapter.py": "project_analysis_evidence_paths",
            "evidence_migration.py": "reasoner_symbol_atlas.evidence_paths",
            "evidence_producer_status.py": "reasoner_symbol_atlas.reference_folder_policy",
            "report_writer.py": "reasoner_symbol_atlas.output_policy",
        }
        for relative_path in CHANGED_FILES:
            source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
            expected_fragment = expected_files[relative_path.name]
            self.assertIn(CANONICAL_IMPORT_PREFIX, source)
            self.assertIn(expected_fragment, source)



if __name__ == "__main__":
    unittest.main()
