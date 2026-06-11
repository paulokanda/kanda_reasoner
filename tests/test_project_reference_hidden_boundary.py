"""Verify hidden project-reference folders stay outside active source scope."""

from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.project_exclusion_rules import (
    iter_python_files,
)
from kanda_reasoner_app.project_analysis_evidence_paths import PROJECT_REFERENCE_DIR
from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
    should_exclude_reasoner_project_path,
)
from kanda_reasoner_app.reasoner_context_collector.collector_scope import (
    iter_project_python_files,
)


class ProjectReferenceHiddenBoundaryTests(unittest.TestCase):
    """Cover the canonical .project_reference non-source boundary."""

    def test_canonical_reference_folder_name_is_hidden_dot_folder(self) -> None:
        self.assertEqual(".project_reference", PROJECT_REFERENCE_DIR)

    def test_unified_exclusion_policy_excludes_canonical_and_legacy_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for folder_name in (".project_reference", "_project_reference"):
                path = root / folder_name / "notes.py"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("VALUE = 1\n", encoding="utf-8")

                self.assertTrue(
                    should_exclude_reasoner_project_path(path, root),
                    folder_name,
                )

            rules = load_reasoner_project_exclusion_rules(root)
            self.assertIn(".project_reference", rules["folders"])
            self.assertIn("_project_reference", rules["folders"])

    def test_docstring_scanner_excludes_canonical_reference_folder_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            active_file = root / "app.py"
            reference_file = root / ".project_reference" / "memo.py"
            legacy_reference_file = root / "_project_reference" / "memo.py"

            active_file.write_text("VALUE = 1\n", encoding="utf-8")
            reference_file.parent.mkdir(parents=True, exist_ok=True)
            reference_file.write_text("VALUE = 2\n", encoding="utf-8")
            legacy_reference_file.parent.mkdir(parents=True, exist_ok=True)
            legacy_reference_file.write_text("VALUE = 3\n", encoding="utf-8")

            found = {path.relative_to(root).as_posix() for path in iter_python_files(root)}

            self.assertEqual({"app.py"}, found)

    def test_static_context_collector_excludes_canonical_reference_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            active_file = root / "app.py"
            reference_file = root / ".project_reference" / "memo.py"
            legacy_reference_file = root / "_project_reference" / "memo.py"

            active_file.write_text("VALUE = 1\n", encoding="utf-8")
            reference_file.parent.mkdir(parents=True, exist_ok=True)
            reference_file.write_text("VALUE = 2\n", encoding="utf-8")
            legacy_reference_file.parent.mkdir(parents=True, exist_ok=True)
            legacy_reference_file.write_text("VALUE = 3\n", encoding="utf-8")

            found = {
                path.relative_to(root).as_posix()
                for path in iter_project_python_files(root)
            }

            self.assertEqual({"app.py"}, found)


if __name__ == "__main__":
    unittest.main()
