"""Tests for the storage policy source-cleanliness validator."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_cleanliness_validator import (
    SOURCE_CLEANLINESS_ACTION,
    SOURCE_CLEANLINESS_CATEGORY_FAILURE,
    SOURCE_CLEANLINESS_CATEGORY_WARNING,
    SourceCleanlinessFinding,
    SourceCleanlinessReport,
    scan_source_cleanliness,
    summarize_source_cleanliness,
)
import kanda_reasoner_app.storage_policy.source_cleanliness_validator as validator_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_cleanliness_validator.py"
)


class StoragePolicySourceCleanlinessValidatorTests(unittest.TestCase):
    """Validate report-only source-cleanliness scanning."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "SOURCE_CLEANLINESS_ACTION",
            "SOURCE_CLEANLINESS_CATEGORY_FAILURE",
            "SOURCE_CLEANLINESS_CATEGORY_WARNING",
            "SourceCleanlinessFinding",
            "SourceCleanlinessReport",
            "scan_source_cleanliness",
            "summarize_source_cleanliness",
        }

        self.assertEqual(set(validator_module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(validator_module, name))

    def test_clean_tree_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "main.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_main.py").write_text("pass\n", encoding="utf-8")

            report = scan_source_cleanliness(root)

        self.assertIsInstance(report, SourceCleanlinessReport)
        self.assertTrue(report.is_clean())
        self.assertTrue(report.is_compilation_clean())
        self.assertEqual(report.action, SOURCE_CLEANLINESS_ACTION)

    def test_detects_backup_and_cache_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module.py").write_text("pass\n", encoding="utf-8")
            (root / "module.py.bak").write_text("backup\n", encoding="utf-8")
            (root / "__pycache__").mkdir()
            (root / ".pytest_cache").mkdir()

            report = scan_source_cleanliness(root)

        paths = {finding.relative_path for finding in report.failures}
        self.assertIn("module.py.bak", paths)
        self.assertIn("__pycache__/", paths)
        self.assertIn(".pytest_cache/", paths)
        self.assertEqual(report.total_warnings, 0)
        self.assertFalse(report.is_compilation_clean())

    def test_detects_project_evidence_and_generated_json_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "project_analysis_evidence").mkdir()
            (root / "kanda_reasoner__complete.json").write_text("{}", encoding="utf-8")
            (root / "other_architecture_audit").mkdir()

            report = scan_source_cleanliness(root)

        paths = {finding.relative_path for finding in report.failures}
        self.assertIn("project_analysis_evidence/", paths)
        self.assertIn("kanda_reasoner__complete.json", paths)
        self.assertIn("other_architecture_audit/", paths)

    def test_workbench_is_warning_not_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "workbench").mkdir()
            (root / "workbench" / "bundle_manifest").mkdir()
            (root / "workbench" / "bundle_manifest" / "x.txt").write_text(
                "manifest\n",
                encoding="utf-8",
            )

            report = scan_source_cleanliness(root)

        warning_paths = {finding.relative_path for finding in report.warnings}
        failure_paths = {finding.relative_path for finding in report.failures}
        self.assertIn("workbench/", warning_paths)
        self.assertIn("workbench/bundle_manifest/", warning_paths)
        self.assertNotIn("workbench/", failure_paths)
        self.assertTrue(report.is_compilation_clean())
        self.assertFalse(report.is_clean())

    def test_allowlisted_generated_source_is_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "architecture_manifest.json").write_text("{}", encoding="utf-8")
            (root / "workflow_manifest.json").write_text("{}", encoding="utf-8")

            report = scan_source_cleanliness(root)

        self.assertTrue(report.is_clean())

    def test_report_summary_contains_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "file.backup").write_text("backup\n", encoding="utf-8")
            (root / "workbench").mkdir()

            report = scan_source_cleanliness(root)
            summary = summarize_source_cleanliness(report)

        self.assertIn("Kanda Reasoner source cleanliness report", summary)
        self.assertIn("Failures: 1", summary)
        self.assertIn("Warnings: 1", summary)

    def test_missing_source_root_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"
            with self.assertRaises(ValueError):
                scan_source_cleanliness(missing)

    def test_finding_dataclass_is_immutable_data(self) -> None:
        finding = SourceCleanlinessFinding(
            relative_path="file.bak",
            pattern="*.bak",
            category=SOURCE_CLEANLINESS_CATEGORY_FAILURE,
            is_directory=False,
            recommended_action="review",
        )

        self.assertEqual(finding.relative_path, "file.bak")
        self.assertEqual(finding.category, SOURCE_CLEANLINESS_CATEGORY_FAILURE)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = VALIDATOR_SOURCE.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "C:/",
            "D:\\",
            "D:/",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
