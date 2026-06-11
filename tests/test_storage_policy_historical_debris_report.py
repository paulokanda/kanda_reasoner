"""Tests for Kanda Reasoner legacy debris reporting."""

from __future__ import annotations

import inspect
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy import historical_debris_report as module
from kanda_reasoner_app.storage_policy.historical_debris_report import (
    LEGACY_DEBRIS_DESTINATION_NAMES,
    LEGACY_DEBRIS_FOLDER_NAMES,
    LEGACY_DEBRIS_REPORT_ACTION,
    LegacyDebrisFolderReport,
    build_legacy_debris_path,
    describe_legacy_debris_policy,
    get_legacy_debris_destination,
    report_one_legacy_debris_folder,
    scan_legacy_debris_folders,
    summarize_historical_debris_reports,
)


class StoragePolicyLegacyDebrisReportTests(unittest.TestCase):
    """Validate report-only detection of old top-level debris folders."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "LEGACY_DEBRIS_DESTINATION_NAMES",
            "LEGACY_DEBRIS_FOLDER_NAMES",
            "LEGACY_DEBRIS_REPORT_ACTION",
            "LegacyDebrisFolderReport",
            "build_legacy_debris_path",
            "describe_legacy_debris_policy",
            "get_legacy_debris_destination",
            "report_one_legacy_debris_folder",
            "scan_legacy_debris_folders",
            "summarize_historical_debris_reports",
        }

        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_legacy_folder_names_are_stable(self) -> None:
        self.assertEqual(
            LEGACY_DEBRIS_FOLDER_NAMES,
            (
                "_kanda_patch_backups",
                "_kanda_restore_points",
                "_kanda_temp",
            ),
        )

    def test_legacy_destinations_are_canonical(self) -> None:
        self.assertEqual(
            LEGACY_DEBRIS_DESTINATION_NAMES["_kanda_patch_backups"],
            "patch_backups",
        )
        self.assertEqual(
            LEGACY_DEBRIS_DESTINATION_NAMES["_kanda_restore_points"],
            "restore_points",
        )
        self.assertEqual(
            LEGACY_DEBRIS_DESTINATION_NAMES["_kanda_temp"],
            "legacy_absorbed",
        )

    def test_describe_policy_returns_copy(self) -> None:
        described = describe_legacy_debris_policy()
        described["_kanda_temp"] = "changed"

        self.assertEqual(
            LEGACY_DEBRIS_DESTINATION_NAMES["_kanda_temp"],
            "legacy_absorbed",
        )

    def test_build_legacy_debris_path_from_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = build_legacy_debris_path(
                "_kanda_temp",
                drive_or_anchor=tmp_dir,
            )

            self.assertEqual(path, Path(tmp_dir) / "_kanda_temp")

    def test_build_legacy_debris_path_from_windows_drive_string(self) -> None:
        path = build_legacy_debris_path(
            "_kanda_temp",
            drive_or_anchor="Z:",
        )

        self.assertIn("_kanda_temp", str(path))
        self.assertIn("Z:", str(path))

    def test_unknown_legacy_folder_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown legacy debris folder"):
            build_legacy_debris_path("unknown")

    def test_destination_resolves_under_maintenance_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            destination = get_legacy_debris_destination(
                "_kanda_patch_backups",
                maintenance_root=tmp_dir,
            )

            self.assertEqual(
                destination,
                Path(tmp_dir).resolve() / "backups" / "patches",
            )

    def test_report_absent_folder_is_report_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = report_one_legacy_debris_folder(
                "_kanda_patch_backups",
                drive_or_anchor=tmp_dir,
                maintenance_root=Path(tmp_dir) / "maintenance",
            )

            self.assertIsInstance(report, LegacyDebrisFolderReport)
            self.assertFalse(report.exists)
            self.assertFalse(report.is_dir)
            self.assertEqual(report.file_count, 0)
            self.assertEqual(report.total_bytes, 0)
            self.assertIsNone(report.latest_modified_timestamp)
            self.assertEqual(report.action, LEGACY_DEBRIS_REPORT_ACTION)

    def test_report_present_folder_counts_files_and_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            legacy_folder = Path(tmp_dir) / "_kanda_patch_backups"
            legacy_folder.mkdir()
            (legacy_folder / "a.txt").write_text("abc", encoding="utf-8")
            nested = legacy_folder / "nested"
            nested.mkdir()
            (nested / "b.txt").write_text("defg", encoding="utf-8")

            report = report_one_legacy_debris_folder(
                "_kanda_patch_backups",
                drive_or_anchor=tmp_dir,
                maintenance_root=Path(tmp_dir) / "maintenance",
            )

            self.assertTrue(report.exists)
            self.assertTrue(report.is_dir)
            self.assertEqual(report.file_count, 2)
            self.assertEqual(report.total_bytes, 7)
            self.assertIsNotNone(report.latest_modified_timestamp)
            self.assertIn("backups", report.recommended_destination_path)
            self.assertIn("patches", report.recommended_destination_path)

    def test_scan_returns_every_legacy_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            reports = scan_legacy_debris_folders(
                drive_or_anchor=tmp_dir,
                maintenance_root=Path(tmp_dir) / "maintenance",
            )

            self.assertEqual(len(reports), len(LEGACY_DEBRIS_FOLDER_NAMES))
            self.assertEqual(
                {report.legacy_name for report in reports},
                set(LEGACY_DEBRIS_FOLDER_NAMES),
            )

    def test_summary_states_report_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            reports = scan_legacy_debris_folders(
                drive_or_anchor=tmp_dir,
                maintenance_root=Path(tmp_dir) / "maintenance",
            )
            summary = summarize_historical_debris_reports(reports)

            self.assertIn("report only", summary)
            self.assertIn("No files were moved or deleted", summary)
            self.assertIn("_kanda_patch_backups", summary)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(module)
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "project_analysis_evidence",
            "kanda_reasoner_architecture_audit",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
