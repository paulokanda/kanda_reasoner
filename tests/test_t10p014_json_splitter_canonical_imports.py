"""Regression tests for T10P014 json_splitter canonical imports."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_SPLITTER = ROOT / 'ask_' 'ai_project_reasoner' / "json_splitter"


class JsonSplitterCanonicalImportTests(unittest.TestCase):
    """Validate json_splitter migration away from hardcoded legacy imports."""

    def test_project_exclusion_filter_imports_use_canonical_package(self) -> None:
        """Project exclusion filter imports should use kanda_reasoner_app."""

        paths = [
            JSON_SPLITTER / "json_splitter_8_help" / "source_loader_private_impl.py",
            JSON_SPLITTER / "__init__.py",
        ]
        for path in paths:
            source = path.read_text(encoding="utf-8")
            self.assertIn("kanda_reasoner_app.project_json_scope_filter", source)
            self.assertNotIn("kanda_reasoner_app.project_json_scope_filter", source)

    def test_validation_manifest_paths_are_relative_to_current_package(self) -> None:
        """Manifest validator should not hardcode the legacy package folder name."""

        path = JSON_SPLITTER / "json_splitter_split_reassemble_validation_validate_manifests.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("package_dir = Path(__file__).resolve().parent", source)
        self.assertIn('origin = package_dir / "json_splitter_split_reassemble_validation.py"', source)
        self.assertIn('manifest = package_dir / "json_splitter_split_reassemble_validation_help.json"', source)
        self.assertNotIn('project_root / "ask_' 'ai_project_reasoner' '"', source)

    def test_changed_json_splitter_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed json_splitter files should not contain the legacy package token."""

        paths = [
            JSON_SPLITTER / "json_splitter_8_help" / "source_loader_private_impl.py",
            JSON_SPLITTER / "__init__.py",
            JSON_SPLITTER / "json_splitter_split_reassemble_validation_validate_manifests.py",
        ]
        for path in paths:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_changed_json_splitter_files_remain_ast_parseable(self) -> None:
        """Changed files should remain syntactically valid Python."""

        paths = [
            JSON_SPLITTER / "json_splitter_8_help" / "source_loader_private_impl.py",
            JSON_SPLITTER / "__init__.py",
            JSON_SPLITTER / "json_splitter_split_reassemble_validation_validate_manifests.py",
        ]
        for path in paths:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


if __name__ == "__main__":
    unittest.main()
