"""Tests for evidence output writer shortlist."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
    EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE,
    EVIDENCE_OUTPUT_RISK_TEST_REFERENCE,
    EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE,
    EvidenceOutputIntegrationAuditReport,
    EvidenceOutputReference,
)
from kanda_reasoner_app.storage_policy.evidence_output_writer_shortlist import (
    EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER,
    EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW,
    EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND,
    EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CLEAN,
    build_evidence_output_writer_shortlist,
    build_evidence_output_writer_shortlist_from_audit,
    render_evidence_output_writer_shortlist_json,
    render_evidence_output_writer_shortlist_text,
    write_evidence_output_writer_shortlist_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "evidence_output_writer_shortlist.py"
)


class StoragePolicyEvidenceOutputWriterShortlistTests(unittest.TestCase):
    """Validate report-only evidence writer shortlisting."""

    def _reference(
        self,
        relative_path: str,
        line_number: int,
        line_preview: str,
        risk: str = EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE,
        token: str = "project_analysis_evidence",
    ) -> EvidenceOutputReference:
        return EvidenceOutputReference(
            relative_path=relative_path,
            line_number=line_number,
            matched_token=token,
            risk=risk,
            line_preview=line_preview,
            recommendation="test recommendation",
        )

    def test_import_does_not_scan_live_tree(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.evidence_output_writer_shortlist"
        )
        self.assertTrue(hasattr(module, "build_evidence_output_writer_shortlist"))

    def test_clean_audit_report_is_clean(self) -> None:
        report = EvidenceOutputIntegrationAuditReport(source_root="demo")
        shortlist = build_evidence_output_writer_shortlist_from_audit(report)

        self.assertEqual(shortlist.status(), EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CLEAN)
        self.assertEqual(shortlist.total_items, 0)
        self.assertEqual(shortlist.source_reference_count, 0)

    def test_runtime_writer_candidate_is_shortlisted(self) -> None:
        audit = EvidenceOutputIntegrationAuditReport(
            source_root="demo",
            references=(
                self._reference(
                    "kanda_reasoner_app/context_bundle/writer.py",
                    12,
                    "target = root / 'project_analysis_evidence' / 'json_complete'",
                ),
                self._reference(
                    "kanda_reasoner_app/context_bundle/writer.py",
                    18,
                    "target.write_text(json_text, encoding='utf-8')",
                    token="json_complete",
                ),
            ),
        )

        shortlist = build_evidence_output_writer_shortlist_from_audit(audit)

        self.assertEqual(
            shortlist.status(),
            EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND,
        )
        self.assertEqual(shortlist.total_items, 1)
        item = shortlist.items[0]
        self.assertEqual(item.relative_path, "kanda_reasoner_app/context_bundle/writer.py")
        self.assertEqual(item.reference_count, 2)
        self.assertEqual(item.risk, EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER)

    def test_tests_policy_and_non_python_files_are_filtered(self) -> None:
        audit = EvidenceOutputIntegrationAuditReport(
            source_root="demo",
            references=(
                self._reference(
                    "tests/test_writer.py",
                    1,
                    "project_analysis_evidence",
                    risk=EVIDENCE_OUTPUT_RISK_TEST_REFERENCE,
                ),
                self._reference(
                    "kanda_reasoner_app/storage_policy/policy.py",
                    2,
                    "project_analysis_evidence",
                    risk=EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE,
                ),
                self._reference(
                    "README.md",
                    3,
                    "project_analysis_evidence output",
                ),
            ),
        )

        shortlist = build_evidence_output_writer_shortlist_from_audit(audit)
        self.assertEqual(shortlist.total_items, 0)
        self.assertEqual(shortlist.source_writer_candidate_count, 1)

    def test_low_score_runtime_candidate_requires_review(self) -> None:
        audit = EvidenceOutputIntegrationAuditReport(
            source_root="demo",
            references=(
                self._reference(
                    "kanda_reasoner_app/some_module.py",
                    5,
                    "json_complete name appears here",
                    token="json_complete",
                ),
            ),
        )

        shortlist = build_evidence_output_writer_shortlist_from_audit(audit)
        self.assertEqual(shortlist.total_items, 1)
        self.assertEqual(shortlist.items[0].risk, EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW)

    def test_max_items_must_be_positive(self) -> None:
        audit = EvidenceOutputIntegrationAuditReport(source_root="demo")
        with self.assertRaises(ValueError):
            build_evidence_output_writer_shortlist_from_audit(audit, max_items=0)

    def test_json_render_is_stable_and_serializable(self) -> None:
        audit = EvidenceOutputIntegrationAuditReport(
            source_root="demo",
            references=(
                self._reference(
                    "kanda_reasoner_app/context_bundle/writer.py",
                    12,
                    "target.write_text('project_analysis_evidence')",
                ),
            ),
        )
        shortlist = build_evidence_output_writer_shortlist_from_audit(audit)
        rendered = render_evidence_output_writer_shortlist_json(shortlist)
        parsed = json.loads(rendered)

        self.assertEqual(parsed["status"], EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND)
        self.assertEqual(parsed["total_items"], 1)

    def test_text_summary_contains_counts(self) -> None:
        report = EvidenceOutputIntegrationAuditReport(source_root="demo")
        rendered = render_evidence_output_writer_shortlist_text(
            build_evidence_output_writer_shortlist_from_audit(report)
        )

        self.assertIn("Kanda Reasoner evidence output writer shortlist", rendered)
        self.assertIn("Shortlisted files: 0", rendered)

    def test_write_rejects_missing_parent(self) -> None:
        report = EvidenceOutputIntegrationAuditReport(source_root="demo")
        shortlist = build_evidence_output_writer_shortlist_from_audit(report)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "missing" / "report.txt"
            with self.assertRaises(ValueError):
                write_evidence_output_writer_shortlist_text(shortlist, output)

    def test_path_scan_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            writer = root / "kanda_reasoner_app" / "context_bundle" / "writer.py"
            writer.parent.mkdir(parents=True)
            writer.write_text(
                "target = root / 'project_analysis_evidence' / 'json_complete'\n"
                "target.write_text('{}')\n",
                encoding="utf-8",
            )

            before = sorted(path.as_posix() for path in root.rglob("*"))
            shortlist = build_evidence_output_writer_shortlist(root)
            after = sorted(path.as_posix() for path in root.rglob("*"))

            self.assertEqual(before, after)
            self.assertEqual(shortlist.total_items, 1)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = SOURCE_PATH.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.evidence_output_writer_shortlist"
        )
        for name in module.__all__:
            self.assertTrue(hasattr(module, name))


if __name__ == "__main__":
    unittest.main()
