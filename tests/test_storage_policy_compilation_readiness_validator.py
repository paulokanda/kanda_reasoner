"""Tests for the storage policy compilation-readiness validator."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.compilation_readiness_validator import (
    COMPILATION_READINESS_ACTION,
    COMPILATION_READINESS_STATUS_BLOCKED,
    COMPILATION_READINESS_STATUS_READY,
    COMPILATION_READINESS_STATUS_WARNINGS_ONLY,
    CompilationReadinessReport,
    summarize_compilation_readiness,
    validate_compilation_readiness,
)
import kanda_reasoner_app.storage_policy.compilation_readiness_validator as validator_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "compilation_readiness_validator.py"
)


class StoragePolicyCompilationReadinessValidatorTests(unittest.TestCase):
    """Validate report-only compilation-readiness behavior."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "COMPILATION_READINESS_ACTION",
            "COMPILATION_READINESS_STATUS_BLOCKED",
            "COMPILATION_READINESS_STATUS_READY",
            "COMPILATION_READINESS_STATUS_WARNINGS_ONLY",
            "CompilationReadinessReport",
            "summarize_compilation_readiness",
            "validate_compilation_readiness",
        }

        self.assertEqual(set(validator_module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(validator_module, name))

    def test_clean_tree_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "main.py").write_text("print('ok')\n", encoding="utf-8")

            report = validate_compilation_readiness(root)

        self.assertIsInstance(report, CompilationReadinessReport)
        self.assertEqual(report.action, COMPILATION_READINESS_ACTION)
        self.assertTrue(report.is_ready())
        self.assertEqual(report.status(), COMPILATION_READINESS_STATUS_READY)

    def test_source_debris_blocks_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module_old.py").write_text("print('old')\n", encoding="utf-8")

            report = validate_compilation_readiness(root)

        self.assertFalse(report.is_ready())
        self.assertEqual(report.status(), COMPILATION_READINESS_STATUS_BLOCKED)
        self.assertEqual(report.blocking_source_failures, 1)

    def test_high_confidence_secret_blocks_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            token_prefix = "ghp" + "_"
            token_body = "abcdefghijklmnopqrstuvwxyz123456"
            (root / "settings.py").write_text(
                f"TOKEN = '{token_prefix}{token_body}'\n",
                encoding="utf-8",
            )

            report = validate_compilation_readiness(root)

        self.assertFalse(report.is_ready())
        self.assertEqual(report.status(), COMPILATION_READINESS_STATUS_BLOCKED)
        self.assertEqual(report.blocking_secret_findings, 1)

    def test_workbench_warning_does_not_block_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "workbench").mkdir()

            report = validate_compilation_readiness(root)

        self.assertTrue(report.is_ready())
        self.assertEqual(report.status(), COMPILATION_READINESS_STATUS_WARNINGS_ONLY)
        self.assertEqual(report.blocking_source_failures, 0)
        self.assertGreater(report.advisory_warnings, 0)

    def test_medium_secret_is_advisory_not_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes.txt").write_text(
                "password = not_a_real_password_value\n",
                encoding="utf-8",
            )

            report = validate_compilation_readiness(root)

        self.assertTrue(report.is_ready())
        self.assertEqual(report.status(), COMPILATION_READINESS_STATUS_WARNINGS_ONLY)
        self.assertEqual(report.blocking_secret_findings, 0)
        self.assertGreater(report.advisory_warnings, 0)

    def test_summary_contains_readiness_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "file.backup").write_text("backup\n", encoding="utf-8")

            report = validate_compilation_readiness(root)
            summary = summarize_compilation_readiness(report)

        self.assertIn("Kanda Reasoner compilation readiness report", summary)
        self.assertIn("Status: blocked", summary)
        self.assertIn("Blocking source failures: 1", summary)

    def test_missing_source_root_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"
            with self.assertRaises(ValueError):
                validate_compilation_readiness(missing)

    def test_import_does_not_scan_live_tree(self) -> None:
        self.assertTrue(hasattr(validator_module, "validate_compilation_readiness"))

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
