# project-path: validation/test_architecture_review_large_file_refactor_docstring_insertion_install_repair_v2.py
"""Validation for docstring insertion install repair v2."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DocstringInsertionInstallRepairValidation(unittest.TestCase):
    def test_mandatory_validator_files_exist(self) -> None:
        expected = [
            "tools/validate_architecture_review_large_file_refactor_docstring_insertion_v1.py",
            "validation/test_architecture_review_large_file_refactor_docstring_insertion_v1.py",
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_docstring_inserter.py",
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_real_preview_writer.py",
        ]
        missing = [rel for rel in expected if not (PROJECT_ROOT / rel).exists()]
        self.assertEqual(missing, [])

    def test_original_docstring_validator_importable_and_passes(self) -> None:
        validator = PROJECT_ROOT / "tools/validate_architecture_review_large_file_refactor_docstring_insertion_v1.py"
        self.assertTrue(validator.exists(), validator)
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=str(PROJECT_ROOT),
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = result.stdout + "\n" + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("VALIDATION OK: architecture-review-large-file-refactor-docstring-insertion-v1", output)
        self.assertIn("STATUS: IN_SYNC", output)
        self.assertIn("ZIP CONTRACT: PASS", output)

    def test_import_chain_for_docstring_helpers(self) -> None:
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_docstring_inserter import (
            insert_missing_docstrings_for_preview_blocks,
        )
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
            RealPreviewWriteResult,
        )

        result = insert_missing_docstrings_for_preview_blocks({"alpha": "def alpha():\n    return 1\n"})
        self.assertEqual(result.blockers, [])
        self.assertIn("Describe alpha", result.blocks["alpha"])
        self.assertTrue(hasattr(RealPreviewWriteResult, "to_dict"))


if __name__ == "__main__":
    unittest.main()
