# project-path: validation/test_architecture_review_large_file_refactor_docstring_insertion_v1.py
"""Validation for Large File Refactor docstring insertion train."""
from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_docstring_inserter import (
    insert_missing_docstrings_for_preview_blocks,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    RealPreviewWriteResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_symbol_source_extractor import (
    extract_source_blocks,
)


class DocstringInsertionValidation(unittest.TestCase):
    def test_inserts_function_and_method_docstrings(self) -> None:
        block = 'class Alpha:\n    def public(self, value):\n        return value\n\ndef beta(x):\n    return x + 1\n'
        result = insert_missing_docstrings_for_preview_blocks({"Alpha": block.split("\n\ndef beta")[0], "beta": "def beta(x):\n    return x + 1\n"})
        self.assertEqual(result.blockers, [])
        self.assertGreaterEqual(len(result.insertions), 3)
        ast.parse(result.blocks["Alpha"])
        ast.parse(result.blocks["beta"])
        self.assertIn('"""Describe Alpha.', result.blocks["Alpha"])
        self.assertIn('"""Describe Alpha.public.', result.blocks["Alpha"])
        self.assertIn('"""Describe beta.', result.blocks["beta"])

    def test_preserves_existing_docstrings(self) -> None:
        block = 'def already():\n    """Existing."""\n    return 1\n'
        result = insert_missing_docstrings_for_preview_blocks({"already": block})
        self.assertEqual(result.blockers, [])
        self.assertEqual(result.insertions, [])
        self.assertEqual(result.blocks["already"], block)

    def test_extraction_plus_insertion_compiles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "module.py"
            path.write_text(
                "# attached comment\n"
                "@staticmethod\n"
                "def gamma(x):\n"
                "    return x\n",
                encoding="utf-8",
            )
            extraction = extract_source_blocks(path, {"gamma"})
            result = insert_missing_docstrings_for_preview_blocks(extraction.symbol_blocks)
            self.assertEqual(result.blockers, [])
            self.assertIn("gamma", result.blocks)
            self.assertIn("# attached comment", result.blocks["gamma"])
            ast.parse(result.blocks["gamma"])

    def test_manifest_result_has_docstring_fields(self) -> None:
        result = RealPreviewWriteResult(
            schema_version="1",
            feature_id="x",
            status="s",
            target_file="target.py",
            source_content_hash="abc",
            preview_root="daily",
            libcst_available=False,
            docstring_insertions=[{"symbol": "a", "target": "a", "kind": "function"}],
        )
        data = result.to_dict()
        self.assertTrue(data["docstring_insertion_enabled"])
        self.assertEqual(data["docstring_insertions"][0]["symbol"], "a")


if __name__ == "__main__":
    unittest.main()
