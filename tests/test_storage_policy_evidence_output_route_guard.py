"""Tests for post-migration evidence output route guard."""

from __future__ import annotations

from pathlib import Path
import json
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    analysis_json_complete_dir,
    ensure_project_analysis_evidence_dirs,
)
from kanda_reasoner_app.storage_policy.evidence_output_route_guard import (  # noqa: E402
    EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED,
    EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN,
    build_evidence_output_route_guard,
    render_evidence_output_route_guard_json,
    render_evidence_output_route_guard_text,
    write_evidence_output_route_guard_text,
)


class StoragePolicyEvidenceOutputRouteGuardTests(unittest.TestCase):
    def test_import_does_not_scan_or_create_live_tree(self) -> None:
        root = PROJECT_ROOT
        before = root / "project_analysis_evidence"

        __import__("kanda_reasoner_app.storage_policy.evidence_output_route_guard")

        self.assertFalse(before.exists())

    def test_clean_external_route_is_clean_without_required_existing_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            report = build_evidence_output_route_guard(root)

            self.assertEqual(report.status(), EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN)
            self.assertFalse(report.in_source_evidence_exists)
            self.assertEqual(report.in_source_json_count, 0)
            self.assertEqual(report.total_findings, 0)

    def test_in_source_evidence_folder_blocks_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            evidence_root = root / "project_analysis_evidence"
            evidence_root.mkdir()

            report = build_evidence_output_route_guard(root)

            self.assertEqual(report.status(), EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED)
            self.assertTrue(report.in_source_evidence_exists)
            self.assertEqual(report.total_findings, 1)

    def test_in_source_json_blocks_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            json_root = root / "project_analysis_evidence" / "json_complete"
            json_root.mkdir(parents=True)
            (json_root / "sample_project__complete.json").write_text("{}", encoding="utf-8")

            report = build_evidence_output_route_guard(root)

            self.assertEqual(report.status(), EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED)
            self.assertEqual(report.in_source_json_count, 1)
            self.assertGreaterEqual(report.total_findings, 2)

    def test_expected_audit_count_can_block_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            ensure_project_analysis_evidence_dirs(root)
            audit_json = analysis_json_complete_dir(root)
            (audit_json / "sample_project__complete.json").write_text("{}", encoding="utf-8")

            report = build_evidence_output_route_guard(
                root,
                expected_min_audit_json_count=2,
                require_existing_audit_json_complete=True,
            )

            self.assertEqual(report.status(), EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED)
            self.assertEqual(report.audit_json_count, 1)

    def test_expected_audit_count_can_pass_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            ensure_project_analysis_evidence_dirs(root)
            audit_json = analysis_json_complete_dir(root)
            (audit_json / "sample_project__complete.json").write_text("{}", encoding="utf-8")

            report = build_evidence_output_route_guard(
                root,
                expected_min_audit_json_count=1,
                require_existing_audit_json_complete=True,
            )

            self.assertEqual(report.status(), EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN)
            self.assertEqual(report.audit_json_count, 1)

    def test_json_render_is_stable_and_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            report = build_evidence_output_route_guard(root)
            payload = json.loads(render_evidence_output_route_guard_json(report))

            self.assertEqual(payload["status"], EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN)
            self.assertIn("active_evidence_root", payload)

    def test_text_summary_contains_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            report = build_evidence_output_route_guard(root)
            text = render_evidence_output_route_guard_text(report)

            self.assertIn("Kanda Reasoner evidence output route guard", text)
            self.assertIn("In-source JSON count: 0", text)
            self.assertIn("Findings: 0", text)

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            report = build_evidence_output_route_guard(root)
            missing = Path(temp_dir) / "missing" / "report.txt"

            with self.assertRaises(FileNotFoundError):
                write_evidence_output_route_guard_text(report, missing)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source_path = (
            PROJECT_ROOT
            / "kanda_reasoner_app"
            / "storage_policy"
            / "evidence_output_route_guard.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertNotIn("E:\\kanda_reasoner", source)
        self.assertNotIn("E:/kanda_reasoner", source)
        self.assertNotIn("E:\\developer_tools", source)
        self.assertNotIn("<PROJECT_ROOT>", source)


if __name__ == "__main__":
    unittest.main()
