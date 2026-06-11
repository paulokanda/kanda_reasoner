"""Tests for report-only evidence output integration audit helpers."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "evidence_output_integration_audit.py"
)


class StoragePolicyEvidenceOutputIntegrationAuditTests(unittest.TestCase):
    """Validate evidence output integration audit behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.evidence_output_integration_audit"
        )
        expected = {
            "EVIDENCE_OUTPUT_INTEGRATION_AUDIT_ACTION",
            "EVIDENCE_OUTPUT_INTEGRATION_AUDIT_SCHEMA_VERSION",
            "EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE",
            "EVIDENCE_OUTPUT_RISK_REFERENCE_ONLY",
            "EVIDENCE_OUTPUT_RISK_TEST_REFERENCE",
            "EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE",
            "EVIDENCE_OUTPUT_STATUS_CLEAN",
            "EVIDENCE_OUTPUT_STATUS_REVIEW_REQUIRED",
            "EVIDENCE_OUTPUT_STATUS_WRITERS_FOUND",
            "EvidenceOutputIntegrationAuditReport",
            "EvidenceOutputReference",
            "render_evidence_output_integration_audit_json",
            "render_evidence_output_integration_audit_text",
            "scan_evidence_output_integration_references",
            "write_evidence_output_integration_audit_json",
            "write_evidence_output_integration_audit_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_scan_live_tree(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.evidence_output_integration_audit"
        )
        self.assertEqual(module.EVIDENCE_OUTPUT_INTEGRATION_AUDIT_ACTION, "report_only")

    def test_clean_tree_is_clean(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            scan_evidence_output_integration_references,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "app.py").write_text("print('ok')\n", encoding="utf-8")
            report = scan_evidence_output_integration_references(root)

        self.assertEqual(report.status(), "clean")
        self.assertEqual(report.total_references, 0)
        self.assertEqual(report.writer_candidates, 0)

    def test_writer_candidate_is_detected(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE,
            scan_evidence_output_integration_references,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            old_token = "project_analysis" + "_evidence"
            code = (
                "from pathlib import Path\n"
                f"target = Path(root) / '{old_token}' / 'json_complete'\n"
                "target.mkdir(parents=True, exist_ok=True)\n"
            )
            (root / "writer.py").write_text(code, encoding="utf-8")
            report = scan_evidence_output_integration_references(root)

        self.assertEqual(report.status(), "writers_found")
        self.assertGreaterEqual(report.writer_candidates, 1)
        self.assertIn(
            EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE,
            {item.risk for item in report.references},
        )

    def test_tests_and_policy_references_are_classified(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE,
            EVIDENCE_OUTPUT_RISK_TEST_REFERENCE,
            scan_evidence_output_integration_references,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            old_token = "project_analysis" + "_evidence"
            tests_dir = root / "tests"
            policy_dir = root / "kanda_reasoner_app" / "storage_policy"
            tests_dir.mkdir(parents=True)
            policy_dir.mkdir(parents=True)
            (tests_dir / "test_paths.py").write_text(
                f"assert '{old_token}'\n",
                encoding="utf-8",
            )
            (policy_dir / "migration.py").write_text(
                f"OLD = '{old_token}'\n",
                encoding="utf-8",
            )
            report = scan_evidence_output_integration_references(root)

        risks = {item.risk for item in report.references}
        self.assertIn(EVIDENCE_OUTPUT_RISK_TEST_REFERENCE, risks)
        self.assertIn(EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE, risks)
        self.assertEqual(report.writer_candidates, 0)
        self.assertEqual(report.status(), "review_required")

    def test_json_render_is_stable_and_serializable(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            render_evidence_output_integration_audit_json,
            scan_evidence_output_integration_references,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "note.md").write_text("json_complete\n", encoding="utf-8")
            report = scan_evidence_output_integration_references(root)
            payload = json.loads(render_evidence_output_integration_audit_json(report))

        self.assertEqual(payload["action"], "report_only")
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["total_references"], 1)
        self.assertEqual(len(payload["references"]), 1)

    def test_text_summary_contains_counts(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            render_evidence_output_integration_audit_text,
            scan_evidence_output_integration_references,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "note.md").write_text("architecture_audit\n", encoding="utf-8")
            report = scan_evidence_output_integration_references(root)
            text = render_evidence_output_integration_audit_text(report)

        self.assertIn("Kanda Reasoner evidence output integration audit", text)
        self.assertIn("References: 1", text)
        self.assertIn("Writer candidates: 0", text)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            scan_evidence_output_integration_references,
            write_evidence_output_integration_audit_json,
            write_evidence_output_integration_audit_text,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "note.md").write_text("json_complete\n", encoding="utf-8")
            report = scan_evidence_output_integration_references(root)
            text_path = root / "report.txt"
            json_path = root / "report.json"

            write_evidence_output_integration_audit_text(report, text_path)
            write_evidence_output_integration_audit_json(report, json_path)

            with self.assertRaises(FileExistsError):
                write_evidence_output_integration_audit_text(report, text_path)

            write_evidence_output_integration_audit_text(
                report,
                text_path,
                overwrite=True,
            )

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())

    def test_write_rejects_missing_parent(self) -> None:
        from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
            scan_evidence_output_integration_references,
            write_evidence_output_integration_audit_json,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report = scan_evidence_output_integration_references(root)
            output_path = root / "missing" / "report.json"

            with self.assertRaises(ValueError):
                write_evidence_output_integration_audit_json(report, output_path)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = MODULE_PATH.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "E:\\\\",
            "kanda_reasoner_architecture_audit",
            "_kanda_reasoner_temp",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
