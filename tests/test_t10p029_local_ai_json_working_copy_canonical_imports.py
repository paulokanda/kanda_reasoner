"""Regression tests for T10P029 local-AI working-copy canonical imports."""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PACKAGE = 'ask_' 'ai_project_reasoner'
CANONICAL_PACKAGE = "kanda_reasoner_app"

CHANGED_FILES = [
    Path('ask_' 'ai_project_reasoner' '/local_ai_json_working_copy/copy_manager.py'),
    Path('ask_' 'ai_project_reasoner' '/local_ai_json_working_copy/__init__.py'),
    Path('ask_' 'ai_project_reasoner' '/local_ai_json_working_copy/tests/test_copy_manager.py'),
]


class LocalAIJsonWorkingCopyCanonicalImportTests(unittest.TestCase):
    """Validate canonical package routing for the local-AI JSON copy box."""

    def _read_changed_file(self, relative_path: Path) -> str:
        return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed Python files should remain syntactically valid."""
        for relative_path in CHANGED_FILES:
            with self.subTest(path=str(relative_path)):
                ast.parse(self._read_changed_file(relative_path))

    def test_changed_files_do_not_hardcode_legacy_package_token(self) -> None:
        """Changed files should not retain legacy package references."""
        for relative_path in CHANGED_FILES:
            with self.subTest(path=str(relative_path)):
                source = self._read_changed_file(relative_path)
                self.assertNotIn(LEGACY_PACKAGE, source)

    def test_changed_files_use_canonical_package_references(self) -> None:
        """Changed files should route imports and user-facing text canonically."""
        copy_manager = self._read_changed_file(CHANGED_FILES[0])
        init_source = self._read_changed_file(CHANGED_FILES[1])
        package_test = self._read_changed_file(CHANGED_FILES[2])

        self.assertIn(
            "from kanda_reasoner_app.project_analysis_evidence_paths import (",
            copy_manager,
        )
        self.assertIn(
            "kanda_reasoner_app.local_ai_json_working_copy.copy_manager",
            copy_manager,
        )
        self.assertIn(
            "python -m kanda_reasoner_app.local_ai_json_working_copy.copy_manager",
            init_source,
        )
        self.assertIn(
            "from kanda_reasoner_app.local_ai_json_working_copy.copy_manager import (",
            package_test,
        )

    def test_working_copy_metadata_records_canonical_creator(self) -> None:
        """Observable metadata should identify the canonical module path."""
        from kanda_reasoner_app.local_ai_json_working_copy.copy_manager import (
            build_default_paths,
            ensure_local_ai_copy,
        )

        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            paths = build_default_paths(project_root)
            paths.canonical_json.parent.mkdir(parents=True, exist_ok=True)
            paths.canonical_json.write_text(
                json.dumps({"source": "canonical"}),
                encoding="utf-8",
            )

            result = ensure_local_ai_copy(project_root)
            metadata = json.loads(paths.metadata_json.read_text(encoding="utf-8"))

            self.assertEqual(result.action, "created")
            self.assertTrue(result.hashes_match)
            self.assertEqual(
                metadata["created_by"],
                "kanda_reasoner_app.local_ai_json_working_copy.copy_manager",
            )


if __name__ == "__main__":
    unittest.main()
