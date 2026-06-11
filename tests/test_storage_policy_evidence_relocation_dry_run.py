"""Tests for the storage policy evidence relocation dry-run planner."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.evidence_relocation_dry_run import (
    EVIDENCE_RELOCATION_CATEGORY_JSON,
    EVIDENCE_RELOCATION_CATEGORY_REVIEW,
    EVIDENCE_RELOCATION_DRY_RUN_ACTION,
    EVIDENCE_RELOCATION_STATUS_ABSENT,
    EVIDENCE_RELOCATION_STATUS_READY,
    EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED,
    EvidenceRelocationItem,
    EvidenceRelocationPlan,
    get_in_source_evidence_root,
    plan_evidence_relocation_dry_run,
    summarize_evidence_relocation_dry_run,
)
import kanda_reasoner_app.storage_policy.evidence_relocation_dry_run as dry_run_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "evidence_relocation_dry_run.py"
)


class StoragePolicyEvidenceRelocationDryRunTests(unittest.TestCase):
    """Validate report-only evidence relocation planning."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "EVIDENCE_RELOCATION_CATEGORY_JSON",
            "EVIDENCE_RELOCATION_CATEGORY_REVIEW",
            "EVIDENCE_RELOCATION_DRY_RUN_ACTION",
            "EVIDENCE_RELOCATION_STATUS_ABSENT",
            "EVIDENCE_RELOCATION_STATUS_READY",
            "EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED",
            "EvidenceRelocationItem",
            "EvidenceRelocationPlan",
            "IN_SOURCE_EVIDENCE_FOLDER_NAME",
            "get_in_source_evidence_root",
            "plan_evidence_relocation_dry_run",
            "summarize_evidence_relocation_dry_run",
        }

        self.assertEqual(set(dry_run_module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(dry_run_module, name))

    def test_absent_source_folder_is_report_only_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            plan = plan_evidence_relocation_dry_run(root)

        self.assertIsInstance(plan, EvidenceRelocationPlan)
        self.assertEqual(plan.action, EVIDENCE_RELOCATION_DRY_RUN_ACTION)
        self.assertFalse(plan.source_exists)
        self.assertEqual(plan.status(), EVIDENCE_RELOCATION_STATUS_ABSENT)
        self.assertEqual(plan.total_items, 0)

    def test_get_in_source_evidence_root_uses_old_folder_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            source_root = get_in_source_evidence_root(root)

        self.assertEqual(source_root.name, "project_analysis_evidence")
        self.assertEqual(source_root.parent.name, "sample_project")
        self.assertFalse(source_root.exists())

    def test_json_under_canonical_subfolder_plans_to_audit_current(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence" / "json_complete"
            source.mkdir(parents=True)
            evidence_file = source / "sample_project__complete.json"
            evidence_file.write_text("{}\n", encoding="utf-8")

            plan = plan_evidence_relocation_dry_run(root)

        self.assertTrue(plan.source_exists)
        self.assertEqual(plan.status(), EVIDENCE_RELOCATION_STATUS_READY)
        self.assertEqual(plan.total_json_items, 1)
        self.assertEqual(plan.total_review_items, 0)
        item = plan.json_items[0]
        self.assertIsInstance(item, EvidenceRelocationItem)
        self.assertEqual(item.category, EVIDENCE_RELOCATION_CATEGORY_JSON)
        self.assertEqual(item.relative_path, "json_complete/sample_project__complete.json")
        self.assertIn("sample_project_architecture_audit", item.planned_destination_path)
        self.assertIn("current", item.planned_destination_path)
        self.assertIn("json_complete", item.planned_destination_path)

    def test_root_level_json_plans_to_json_complete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")

            plan = plan_evidence_relocation_dry_run(root)

        item = plan.json_items[0]
        self.assertEqual(item.relative_path, "sample_project__complete.json")
        self.assertIn("current", item.planned_destination_path)
        self.assertIn("json_complete", item.planned_destination_path)
        self.assertTrue(item.planned_destination_path.endswith("sample_project__complete.json"))

    def test_mixed_content_requires_review_and_quarantine_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")
            (source / "notes.txt").write_text("manual note\n", encoding="utf-8")

            plan = plan_evidence_relocation_dry_run(root)

        self.assertEqual(plan.status(), EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED)
        self.assertEqual(plan.total_json_items, 1)
        self.assertEqual(plan.total_review_items, 1)
        review_item = plan.review_items[0]
        self.assertEqual(review_item.category, EVIDENCE_RELOCATION_CATEGORY_REVIEW)
        self.assertIn("quarantine", review_item.planned_destination_path)
        self.assertIn("sample_project", review_item.planned_destination_path)

    def test_summary_contains_dry_run_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")

            plan = plan_evidence_relocation_dry_run(root)
            summary = summarize_evidence_relocation_dry_run(plan)

        self.assertIn("Kanda Reasoner evidence relocation dry-run report", summary)
        self.assertIn("Action: dry_run_only", summary)
        self.assertIn("JSON evidence items: 1", summary)

    def test_file_instead_of_folder_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "project_analysis_evidence").write_text("not a folder\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                plan_evidence_relocation_dry_run(root)

    def test_import_does_not_scan_live_tree(self) -> None:
        self.assertTrue(hasattr(dry_run_module, "plan_evidence_relocation_dry_run"))

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = DRY_RUN_SOURCE.read_text(encoding="utf-8")
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
