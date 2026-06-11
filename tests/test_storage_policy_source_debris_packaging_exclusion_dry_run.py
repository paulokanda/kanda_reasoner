from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_packaging_exclusion_dry_run import (
    SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_ACTION,
    SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_SCHEMA_VERSION,
    SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED,
    SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY,
    SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_POLICY_GAP,
    SourceDebrisPackagingExclusionDryRunItem,
    SourceDebrisPackagingExclusionDryRunPlan,
    build_source_debris_packaging_exclusion_dry_run,
    render_source_debris_packaging_exclusion_dry_run_json,
    render_source_debris_packaging_exclusion_dry_run_text,
    write_source_debris_packaging_exclusion_dry_run_json,
    write_source_debris_packaging_exclusion_dry_run_text,
)


class StoragePolicySourceDebrisPackagingExclusionDryRunTests(unittest.TestCase):
    def test_public_surface_is_declared(self) -> None:
        from kanda_reasoner_app.storage_policy import source_debris_packaging_exclusion_dry_run as module

        self.assertIn(
            "build_source_debris_packaging_exclusion_dry_run",
            module.__all__,
        )
        self.assertIn(
            "render_source_debris_packaging_exclusion_dry_run_json",
            module.__all__,
        )
        self.assertIn(
            "write_source_debris_packaging_exclusion_dry_run_text",
            module.__all__,
        )

    def test_import_does_not_scan_or_create_live_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            __import__(
                "kanda_reasoner_app.storage_policy."
                "source_debris_packaging_exclusion_dry_run"
            )
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_clean_tree_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kanda_reasoner_app").mkdir()
            plan = build_source_debris_packaging_exclusion_dry_run(root)

            self.assertEqual(plan.total_items, 0)
            self.assertEqual(plan.covered_items, 0)
            self.assertEqual(plan.uncovered_items, 0)
            self.assertEqual(plan.status(), SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY)

    def test_workbench_items_are_covered_by_parent_packaging_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workbench" / "bundle_manifest").mkdir(parents=True)

            plan = build_source_debris_packaging_exclusion_dry_run(root)

            self.assertEqual(plan.total_items, 2)
            self.assertEqual(plan.covered_items, 2)
            self.assertEqual(plan.uncovered_items, 0)
            self.assertEqual(plan.status(), SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED)
            relative_paths = {item.relative_path for item in plan.items}
            self.assertEqual(relative_paths, {"workbench/", "workbench/bundle_manifest/"})
            for item in plan.items:
                self.assertEqual(item.matched_exclude_pattern, "workbench/")
                self.assertTrue(item.is_covered_by_packaging_policy)

    def test_policy_gap_is_reported_when_exclusion_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workbench" / "bundle_manifest").mkdir(parents=True)

            plan = build_source_debris_packaging_exclusion_dry_run(
                root,
                packaging_exclude_patterns=(),
            )

            self.assertEqual(plan.total_items, 2)
            self.assertEqual(plan.covered_items, 0)
            self.assertEqual(plan.uncovered_items, 2)
            self.assertEqual(plan.status(), SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_POLICY_GAP)
            self.assertTrue(all(not item.matched_exclude_pattern for item in plan.items))

    def test_quarantine_and_evidence_items_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.py.bak").write_text("backup", encoding="utf-8")
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            (evidence / "tool__complete.json").write_text("{}", encoding="utf-8")

            plan = build_source_debris_packaging_exclusion_dry_run(root)

            self.assertEqual(plan.total_items, 0)
            self.assertEqual(plan.status(), SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY)

    def test_renderers_are_stable_and_serializable(self) -> None:
        item = SourceDebrisPackagingExclusionDryRunItem(
            relative_path="workbench/",
            source_path="root/workbench",
            pattern="workbench/",
            is_directory=True,
            matched_exclude_pattern="workbench/",
            is_covered_by_packaging_policy=True,
            message="keep in development source tree and exclude from packaged builds",
        )
        plan = SourceDebrisPackagingExclusionDryRunPlan(
            source_root="root",
            project_slug="root",
            items=(item,),
        )

        text = render_source_debris_packaging_exclusion_dry_run_text(plan)
        data = json.loads(render_source_debris_packaging_exclusion_dry_run_json(plan))

        self.assertIn("Kanda Reasoner source debris packaging exclusion", text)
        self.assertEqual(data["schema_version"], SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_SCHEMA_VERSION)
        self.assertEqual(data["action"], SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_ACTION)
        self.assertEqual(data["status"], SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED)
        self.assertEqual(data["covered_items"], 1)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output_dir = root / "out"
            output_dir.mkdir()
            plan = SourceDebrisPackagingExclusionDryRunPlan(
                source_root=str(root),
                project_slug="demo",
            )
            text_path = output_dir / "plan.txt"
            json_path = output_dir / "plan.json"

            write_source_debris_packaging_exclusion_dry_run_text(plan, text_path)
            write_source_debris_packaging_exclusion_dry_run_json(plan, json_path)

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())
            with self.assertRaises(FileExistsError):
                write_source_debris_packaging_exclusion_dry_run_text(plan, text_path)

            write_source_debris_packaging_exclusion_dry_run_text(
                plan,
                text_path,
                overwrite=True,
            )

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = SourceDebrisPackagingExclusionDryRunPlan(
                source_root=str(root),
                project_slug="demo",
            )
            with self.assertRaises(ValueError):
                write_source_debris_packaging_exclusion_dry_run_json(
                    plan,
                    root / "missing" / "plan.json",
                )

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = Path(
            "kanda_reasoner_app/storage_policy/"
            "source_debris_packaging_exclusion_dry_run.py"
        ).read_text(encoding="utf-8")
        forbidden = (
            "E:\\",
            "E:/",
            "C:\\",
            "C:/",
            "D:\\",
            "D:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
        )
        for value in forbidden:
            self.assertNotIn(value, source)


if __name__ == "__main__":
    unittest.main()
