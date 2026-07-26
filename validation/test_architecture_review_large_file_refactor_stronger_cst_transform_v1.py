# project-path: validation/test_architecture_review_large_file_refactor_stronger_cst_transform_v1.py
"""Validation for stronger CST transform fidelity."""
from __future__ import annotations

import importlib
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_transform_fidelity import (
    build_cst_transform_fidelity_report,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    RealPreviewWriteResult,
)


SAMPLE = (
    '"""Module docstring."""\n'
    'from __future__ import annotations\n'
    'import os\n'
    '\n'
    '# attached comment\n'
    '@staticmethod\n'
    'def moved(value: int) -> int:\n'
    '    return value + 1\n'
    '\n'
    'class Kept:\n'
    '    pass\n'
    '\n'
    'if __name__ == "__main__":\n'
    '    print(moved(1))\n'
)


class StrongerCstTransformTests(unittest.TestCase):
    """Focused tests for transform fidelity evidence."""

    def test_report_finds_requested_moved_symbol(self) -> None:
        report = build_cst_transform_fidelity_report(SAMPLE, {"moved"})
        self.assertIn(report.transform_backend, {
            "libcst_transform_partition",
            "ast_transform_partition_fallback",
            "libcst_parse_failed_ast_fallback",
        })
        self.assertIn("moved", report.moved_symbols_found)
        self.assertIn("Kept", report.retained_top_level_symbols)
        self.assertTrue(report.retained_module_docstring)
        self.assertTrue(report.retained_main_guard)
        self.assertEqual(report.blockers, [])

    def test_report_blocks_missing_symbol(self) -> None:
        report = build_cst_transform_fidelity_report(SAMPLE, {"missing_symbol"})
        self.assertIn("missing_symbol", report.missing_symbols)
        self.assertIn("MISSING_MOVED_SYMBOL:missing_symbol", report.blockers)

    def test_preview_result_contract_has_fidelity_fields(self) -> None:
        result = RealPreviewWriteResult(
            schema_version="1.0",
            feature_id="test",
            status="blocked",
            target_file="x.py",
            source_content_hash="abc",
            preview_root="preview",
            libcst_available=False,
        ).to_dict()
        self.assertTrue(result["cst_transform_fidelity_enabled"])
        self.assertIn("cst_transform_fidelity", result)

    def test_package_exports_transform_helper(self) -> None:
        package = importlib.import_module(
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
        )
        self.assertTrue(hasattr(package, "build_cst_transform_fidelity_report"))

    def test_module_line_counts_stay_under_limit(self) -> None:
        root = Path(__file__).resolve().parents[1]
        files = [
            root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_transform_fidelity.py",
            root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_real_preview_writer.py",
            root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        ]
        for path in files:
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
