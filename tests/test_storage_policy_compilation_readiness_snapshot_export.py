from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.compilation_readiness_snapshot_export import (
    COMPILATION_READINESS_SNAPSHOT_EXPORT_ACTION,
    COMPILATION_READINESS_SNAPSHOT_EXPORT_SCHEMA_VERSION,
    CompilationReadinessSnapshot,
    build_compilation_readiness_snapshot,
    build_compilation_readiness_snapshot_export_paths,
    build_compilation_readiness_snapshot_run_id,
    export_compilation_readiness_snapshot,
    render_compilation_readiness_snapshot_export_json,
    render_compilation_readiness_snapshot_export_text,
    render_compilation_readiness_snapshot_json,
    render_compilation_readiness_snapshot_text,
    write_compilation_readiness_snapshot_json,
    write_compilation_readiness_snapshot_text,
)


class StoragePolicyCompilationReadinessSnapshotExportTests(unittest.TestCase):
    def test_public_surface_is_declared(self) -> None:
        from kanda_reasoner_app.storage_policy import compilation_readiness_snapshot_export as module

        self.assertIn("build_compilation_readiness_snapshot", module.__all__)
        self.assertIn("export_compilation_readiness_snapshot", module.__all__)
        self.assertIn("write_compilation_readiness_snapshot_json", module.__all__)

    def test_import_does_not_export_or_create_live_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            __import__(
                "kanda_reasoner_app.storage_policy."
                "compilation_readiness_snapshot_export"
            )
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_run_id_builder_is_stable_with_injected_datetime(self) -> None:
        run_id = build_compilation_readiness_snapshot_run_id(
            datetime(2026, 6, 9, 12, 34, 56)
        )
        self.assertEqual(run_id, "20260609_123456")

    def test_paths_are_canonical_without_creating_folders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "source_project"
            maintenance = Path(tmp) / "maintenance"
            root.mkdir()

            paths = build_compilation_readiness_snapshot_export_paths(
                root,
                maintenance_root=maintenance,
                run_id="validation_smoke",
            )

            self.assertTrue(paths.output_root.endswith("validation_smoke"))
            self.assertIn("logs", paths.output_root)
            self.assertIn("audit", paths.output_root)
            self.assertIn("compilation_readiness_snapshot", paths.output_root)
            self.assertTrue(paths.text_path.endswith("compilation_readiness_snapshot.txt"))
            self.assertTrue(paths.json_path.endswith("compilation_readiness_snapshot.json"))
            self.assertFalse(Path(paths.output_root).exists())

    def test_clean_tree_snapshot_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kanda_reasoner_app").mkdir()

            snapshot = build_compilation_readiness_snapshot(
                root,
                run_id="clean_tree",
            )

            self.assertIsInstance(snapshot, CompilationReadinessSnapshot)
            self.assertEqual(snapshot.run_id, "clean_tree")
            self.assertTrue(snapshot.is_compilation_unblocked)
            self.assertEqual(snapshot.blocking_source_failures, 0)
            self.assertEqual(snapshot.blocking_secret_findings, 0)
            self.assertEqual(snapshot.source_debris_items, 0)

    def test_workbench_snapshot_is_warnings_only_and_packaging_covered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kanda_reasoner_app").mkdir()
            (root / "workbench" / "bundle_manifest").mkdir(parents=True)

            snapshot = build_compilation_readiness_snapshot(
                root,
                run_id="workbench_policy",
            )

            self.assertTrue(snapshot.is_compilation_unblocked)
            self.assertEqual(snapshot.blocking_source_failures, 0)
            self.assertEqual(snapshot.blocking_secret_findings, 0)
            self.assertEqual(snapshot.packaging_exclusion_review_items, 2)
            self.assertEqual(snapshot.packaging_exclusion.covered_items, 2)
            self.assertEqual(snapshot.packaging_exclusion.uncovered_items, 0)
            self.assertEqual(snapshot.readiness_status, "warnings_only")

    def test_export_writes_text_and_json_only_when_called(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            maintenance = Path(tmp) / "maintenance"
            root.mkdir()
            (root / "workbench" / "bundle_manifest").mkdir(parents=True)

            paths = build_compilation_readiness_snapshot_export_paths(
                root,
                maintenance_root=maintenance,
                run_id="manual_review_export",
            )
            self.assertFalse(Path(paths.output_root).exists())

            result = export_compilation_readiness_snapshot(
                root,
                maintenance_root=maintenance,
                run_id="manual_review_export",
            )

            self.assertTrue(Path(result.paths.text_path).exists())
            self.assertTrue(Path(result.paths.json_path).exists())
            self.assertTrue(result.snapshot.is_compilation_unblocked)
            data = json.loads(Path(result.paths.json_path).read_text(encoding="utf-8"))
            self.assertEqual(
                data["schema_version"],
                COMPILATION_READINESS_SNAPSHOT_EXPORT_SCHEMA_VERSION,
            )

    def test_export_respects_overwrite_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            maintenance = Path(tmp) / "maintenance"
            root.mkdir()

            export_compilation_readiness_snapshot(
                root,
                maintenance_root=maintenance,
                run_id="same_run",
            )
            with self.assertRaises(FileExistsError):
                export_compilation_readiness_snapshot(
                    root,
                    maintenance_root=maintenance,
                    run_id="same_run",
                )

            result = export_compilation_readiness_snapshot(
                root,
                maintenance_root=maintenance,
                run_id="same_run",
                overwrite=True,
            )
            self.assertTrue(Path(result.paths.json_path).exists())

    def test_renderers_are_stable_and_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workbench" / "bundle_manifest").mkdir(parents=True)
            result = export_compilation_readiness_snapshot(
                root,
                maintenance_root=Path(tmp) / "maintenance",
                run_id="render_smoke",
            )

            snapshot_text = render_compilation_readiness_snapshot_text(result.snapshot)
            snapshot_data = json.loads(
                render_compilation_readiness_snapshot_json(result.snapshot)
            )
            export_text = render_compilation_readiness_snapshot_export_text(result)
            export_data = json.loads(
                render_compilation_readiness_snapshot_export_json(result)
            )

            self.assertIn("final compilation-readiness snapshot", snapshot_text)
            self.assertEqual(snapshot_data["action"], COMPILATION_READINESS_SNAPSHOT_EXPORT_ACTION)
            self.assertIn("Output root:", export_text)
            self.assertIn("paths", export_data)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output_dir = root / "out"
            output_dir.mkdir()
            snapshot = build_compilation_readiness_snapshot(root, run_id="manual")
            text_path = output_dir / "snapshot.txt"
            json_path = output_dir / "snapshot.json"

            write_compilation_readiness_snapshot_text(snapshot, text_path)
            write_compilation_readiness_snapshot_json(snapshot, json_path)

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())
            with self.assertRaises(FileExistsError):
                write_compilation_readiness_snapshot_text(snapshot, text_path)

            write_compilation_readiness_snapshot_text(
                snapshot,
                text_path,
                overwrite=True,
            )

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snapshot = build_compilation_readiness_snapshot(root, run_id="manual")
            with self.assertRaises(ValueError):
                write_compilation_readiness_snapshot_json(
                    snapshot,
                    root / "missing" / "snapshot.json",
                )

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = Path(
            "kanda_reasoner_app/storage_policy/"
            "compilation_readiness_snapshot_export.py"
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
