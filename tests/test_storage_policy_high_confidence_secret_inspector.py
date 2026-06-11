"""Tests for the report-only high-confidence secret inspector."""

from __future__ import annotations

from pathlib import Path
import inspect
import json
import unittest

from kanda_reasoner_app.storage_policy.high_confidence_secret_inspector import (
    HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION,
    HIGH_CONFIDENCE_SECRET_RISK_ADVISORY,
    HIGH_CONFIDENCE_SECRET_RISK_BLOCKING,
    HIGH_CONFIDENCE_SECRET_STATUS_CLEAN,
    HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED,
    HighConfidenceSecretInspectionItem,
    HighConfidenceSecretInspectionReport,
    build_high_confidence_secret_inspection,
    build_high_confidence_secret_inspection_from_report,
    render_high_confidence_secret_inspection_json,
    render_high_confidence_secret_inspection_text,
    write_high_confidence_secret_inspection_json,
    write_high_confidence_secret_inspection_text,
)
from kanda_reasoner_app.storage_policy.secret_scan_gate import (
    SECRET_SCAN_SEVERITY_HIGH,
    SECRET_SCAN_SEVERITY_MEDIUM,
    SecretScanFinding,
    SecretScanReport,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSPECTOR_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "high_confidence_secret_inspector.py"
)


class StoragePolicyHighConfidenceSecretInspectorTests(unittest.TestCase):
    """Validate report-only high-confidence secret inspection helpers."""

    def test_clean_report_is_clean(self) -> None:
        report = SecretScanReport(source_root="demo", findings=())

        inspection = build_high_confidence_secret_inspection_from_report(report)

        self.assertEqual(inspection.action, HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION)
        self.assertEqual(inspection.status(), HIGH_CONFIDENCE_SECRET_STATUS_CLEAN)
        self.assertTrue(inspection.is_clean())
        self.assertEqual(inspection.total_items, 0)

    def test_high_confidence_finding_requires_review_without_raw_value(self) -> None:
        raw_value = "raw-sensitive-value"
        finding = SecretScanFinding(
            relative_path="config.py",
            line_number=7,
            pattern_name="private_key_block",
            severity=SECRET_SCAN_SEVERITY_HIGH,
            redacted_preview="secret = <redacted>",
            recommended_action="review",
        )
        report = SecretScanReport(source_root="demo", findings=(finding,))

        inspection = build_high_confidence_secret_inspection_from_report(report)
        text = render_high_confidence_secret_inspection_text(inspection)

        self.assertEqual(inspection.status(), HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED)
        self.assertEqual(inspection.blocking_items, 1)
        self.assertEqual(inspection.items[0].risk_class, HIGH_CONFIDENCE_SECRET_RISK_BLOCKING)
        self.assertIn("<redacted>", text)
        self.assertNotIn(raw_value, text)

    def test_medium_findings_are_ignored_by_default(self) -> None:
        finding = SecretScanFinding(
            relative_path="settings.py",
            line_number=3,
            pattern_name="credential_assignment",
            severity=SECRET_SCAN_SEVERITY_MEDIUM,
            redacted_preview="api_key = <redacted>",
            recommended_action="review",
        )
        report = SecretScanReport(source_root="demo", findings=(finding,))

        inspection = build_high_confidence_secret_inspection_from_report(report)

        self.assertEqual(inspection.total_items, 0)
        self.assertEqual(inspection.status(), HIGH_CONFIDENCE_SECRET_STATUS_CLEAN)

    def test_include_advisory_can_include_medium_findings(self) -> None:
        finding = SecretScanFinding(
            relative_path="settings.py",
            line_number=3,
            pattern_name="credential_assignment",
            severity=SECRET_SCAN_SEVERITY_MEDIUM,
            redacted_preview="api_key = <redacted>",
            recommended_action="review",
        )
        report = SecretScanReport(source_root="demo", findings=(finding,))

        inspection = build_high_confidence_secret_inspection_from_report(
            report,
            include_advisory=True,
        )

        self.assertEqual(inspection.total_items, 1)
        self.assertEqual(inspection.advisory_items, 1)
        self.assertEqual(inspection.items[0].risk_class, HIGH_CONFIDENCE_SECRET_RISK_ADVISORY)
        self.assertEqual(inspection.status(), HIGH_CONFIDENCE_SECRET_STATUS_CLEAN)

    def test_json_render_is_stable_and_serializable(self) -> None:
        report = HighConfidenceSecretInspectionReport(
            source_root="demo",
            items=(
                HighConfidenceSecretInspectionItem(
                    relative_path="config.py",
                    line_number=1,
                    pattern_name="private_key_block",
                    severity=SECRET_SCAN_SEVERITY_HIGH,
                    risk_class=HIGH_CONFIDENCE_SECRET_RISK_BLOCKING,
                    redacted_preview="<redacted>",
                    recommended_action="review",
                ),
            ),
            scanned_findings=2,
        )

        data = json.loads(render_high_confidence_secret_inspection_json(report))

        self.assertEqual(data["status"], HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED)
        self.assertEqual(data["scanned_findings"], 2)
        self.assertEqual(data["blocking_items"], 1)
        self.assertEqual(data["items"][0]["redacted_preview"], "<redacted>")

    def test_path_scan_does_not_write_files(self) -> None:
        root = self._make_root("path_scan")
        (root / "main.py").write_text("print('hello')\n", encoding="utf-8")
        before = sorted(item.relative_to(root).as_posix() for item in root.rglob("*"))

        inspection = build_high_confidence_secret_inspection(root)
        after = sorted(item.relative_to(root).as_posix() for item in root.rglob("*"))

        self.assertTrue(inspection.is_clean())
        self.assertEqual(before, after)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        root = self._make_root("write_reports")
        report = HighConfidenceSecretInspectionReport(source_root="demo")
        text_path = root / "report.txt"
        json_path = root / "report.json"

        write_high_confidence_secret_inspection_text(report, text_path)
        write_high_confidence_secret_inspection_json(report, json_path)

        self.assertTrue(text_path.exists())
        self.assertTrue(json_path.exists())
        with self.assertRaises(FileExistsError):
            write_high_confidence_secret_inspection_text(report, text_path)
        with self.assertRaises(FileExistsError):
            write_high_confidence_secret_inspection_json(report, json_path)

    def test_write_rejects_missing_parent(self) -> None:
        report = HighConfidenceSecretInspectionReport(source_root="demo")
        missing_parent = PROJECT_ROOT / "missing_secret_inspector_parent_xyz"

        with self.assertRaises(ValueError):
            write_high_confidence_secret_inspection_text(
                report,
                missing_parent / "report.txt",
            )
        with self.assertRaises(ValueError):
            write_high_confidence_secret_inspection_json(
                report,
                missing_parent / "report.json",
            )

    def test_public_surface_is_declared(self) -> None:
        import kanda_reasoner_app.storage_policy.high_confidence_secret_inspector as module

        expected = {
            "HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION",
            "HIGH_CONFIDENCE_SECRET_INSPECTION_SCHEMA_VERSION",
            "HIGH_CONFIDENCE_SECRET_RISK_ADVISORY",
            "HIGH_CONFIDENCE_SECRET_RISK_BLOCKING",
            "HIGH_CONFIDENCE_SECRET_STATUS_CLEAN",
            "HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED",
            "HighConfidenceSecretInspectionItem",
            "HighConfidenceSecretInspectionReport",
            "build_high_confidence_secret_inspection",
            "build_high_confidence_secret_inspection_from_report",
            "render_high_confidence_secret_inspection_json",
            "render_high_confidence_secret_inspection_text",
            "write_high_confidence_secret_inspection_json",
            "write_high_confidence_secret_inspection_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = INSPECTOR_SOURCE.read_text(encoding="utf-8")

        forbidden_fragments = [
            "E:\\",
            "E:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
            "project_analysis_evidence",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)

    def test_import_does_not_scan_live_tree(self) -> None:
        import kanda_reasoner_app.storage_policy.high_confidence_secret_inspector as module

        source = inspect.getsource(module)
        self.assertIn("report-only", source)
        self.assertNotIn("build_high_confidence_secret_inspection(get_app_root", source)

    def _make_root(self, name: str) -> Path:
        root = PROJECT_ROOT / "workbench" / "bundle_manifest" / "test_tmp" / name
        if root.exists():
            for item in sorted(root.rglob("*"), reverse=True):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    item.rmdir()
            root.rmdir()
        root.mkdir(parents=True)
        return root


if __name__ == "__main__":
    unittest.main()
