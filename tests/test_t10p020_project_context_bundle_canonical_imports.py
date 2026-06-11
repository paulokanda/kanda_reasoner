"""Tests for T10P020 project-context-bundle canonical imports."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = (
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "exclusion_engine.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "exclusion_provider.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "exclusion_rules_exporter.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "output_paths.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "project_context.py",
)


class ProjectContextBundleCanonicalImportTests(unittest.TestCase):
    """Validate canonical package usage in project context bundle helpers."""

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed project-context-bundle files should remain valid Python."""
        for path in CHANGED_FILES:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed files should not contain the legacy package token."""
        for path in CHANGED_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_exclusion_policy_imports_use_canonical_package(self) -> None:
        """Exclusion policy adapters should import through kanda_reasoner_app."""
        engine_source = CHANGED_FILES[0].read_text(encoding="utf-8")
        provider_source = CHANGED_FILES[1].read_text(encoding="utf-8")
        self.assertIn("from kanda_reasoner_app.project_exclusion_policy import", engine_source)
        self.assertIn("from kanda_reasoner_app.project_exclusion_policy import", provider_source)
        self.assertIn("kanda_reasoner_app.project_exclusion_policy.", provider_source)

    def test_evidence_path_imports_use_canonical_package(self) -> None:
        """Evidence path helpers should import through kanda_reasoner_app."""
        output_paths_source = CHANGED_FILES[3].read_text(encoding="utf-8")
        project_context_source = CHANGED_FILES[4].read_text(encoding="utf-8")
        self.assertIn(
            "from kanda_reasoner_app.project_analysis_evidence_paths import",
            output_paths_source,
        )
        self.assertIn(
            "from kanda_reasoner_app.project_analysis_evidence_paths import",
            project_context_source,
        )

    def test_decision_examples_are_project_agnostic(self) -> None:
        """Decision examples should avoid fixed package-folder names."""
        source = CHANGED_FILES[2].read_text(encoding="utf-8")
        self.assertIn("<PRODUCT_PACKAGE>/example.py", source)
        self.assertNotIn('"ask_' 'ai_project_reasoner' '/example.py"', source)


if __name__ == "__main__":
    unittest.main()
