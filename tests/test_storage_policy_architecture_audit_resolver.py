"""Tests for storage policy architecture audit resolver."""

from __future__ import annotations

from datetime import datetime
import inspect
from pathlib import Path
import tempfile
import unittest

import kanda_reasoner_app.storage_policy.architecture_audit_resolver as resolver


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StoragePolicyArchitectureAuditResolverTests(unittest.TestCase):
    """Validate side-effect-free architecture audit path resolution."""

    def test_build_audit_root_from_windows_drive_string(self) -> None:
        root = resolver.build_architecture_audit_root_from_drive_or_anchor(
            "X:",
            "My Project",
        )

        self.assertEqual(str(root), "X:\\my_project_architecture_audit")

    def test_build_audit_root_from_posix_anchor(self) -> None:
        root = resolver.build_architecture_audit_root_from_drive_or_anchor(
            "/",
            "My Project",
        )

        self.assertEqual(root, Path("/") / "my_project_architecture_audit")

    def test_build_audit_root_rejects_empty_anchor(self) -> None:
        with self.assertRaises(ValueError):
            resolver.build_architecture_audit_root_from_drive_or_anchor(
                "",
                "project",
            )

    def test_default_audit_root_is_outside_actual_project_root(self) -> None:
        root = resolver.get_architecture_audit_root(PROJECT_ROOT)

        self.assertNotIn(PROJECT_ROOT, root.parents)
        self.assertNotEqual(root, PROJECT_ROOT)

    def test_default_audit_root_name_uses_project_slug(self) -> None:
        root = resolver.get_architecture_audit_root(PROJECT_ROOT)

        expected_name = f"{resolver.get_project_slug(PROJECT_ROOT)}_architecture_audit"
        self.assertEqual(root.name, expected_name)

    def test_current_root_uses_current_folder(self) -> None:
        root = resolver.get_architecture_audit_current_root(PROJECT_ROOT)

        self.assertEqual(root.name, resolver.ARCHITECTURE_AUDIT_CURRENT_FOLDER)
        expected_name = f"{resolver.get_project_slug(PROJECT_ROOT)}_architecture_audit"
        self.assertEqual(root.parent.name, expected_name)

    def test_run_root_uses_runs_and_run_id(self) -> None:
        root = resolver.get_architecture_audit_run_root(
            PROJECT_ROOT,
            run_id="2026-01-01 12:00:00",
        )

        self.assertEqual(root.parent.name, resolver.ARCHITECTURE_AUDIT_RUNS_FOLDER)
        self.assertEqual(root.name, "2026_01_01_12_00_00")

    def test_run_id_timestamp_is_windows_filename_safe(self) -> None:
        run_id = resolver.build_architecture_audit_run_id(
            datetime(2026, 1, 1, 12, 0, 0),
        )

        self.assertEqual(run_id, "20260101_120000")
        self.assertNotIn(":", run_id)

    def test_subfolder_resolution_uses_json_complete_by_default(self) -> None:
        path = resolver.get_architecture_audit_subfolder(PROJECT_ROOT)

        self.assertEqual(path.name, "json_complete")
        self.assertEqual(path.parent.name, "current")

    def test_unknown_subfolder_raises(self) -> None:
        with self.assertRaises(ValueError):
            resolver.get_architecture_audit_subfolder(
                PROJECT_ROOT,
                subfolder_name="unknown",
            )

    def test_artifact_path_uses_double_underscore_name(self) -> None:
        path = resolver.get_architecture_audit_artifact_path(
            PROJECT_ROOT,
            suffix="complete",
        )

        expected_name = f"{resolver.get_project_slug(PROJECT_ROOT)}__complete.json"
        self.assertEqual(path.name, expected_name)
        self.assertEqual(path.parent.name, "json_complete")

    def test_all_artifact_suffixes_resolve(self) -> None:
        for suffix in resolver.ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES:
            path = resolver.get_architecture_audit_artifact_path(
                PROJECT_ROOT,
                suffix=suffix,
            )
            self.assertEqual(path.suffix, ".json")
            self.assertIn(f"__{suffix}.json", path.name)

    def test_unknown_artifact_suffix_raises(self) -> None:
        with self.assertRaises(ValueError):
            resolver.get_architecture_audit_artifact_path(
                PROJECT_ROOT,
                suffix="unknown",
            )

    def test_current_subfolders_returns_every_canonical_subfolder(self) -> None:
        folders = resolver.get_architecture_audit_current_subfolders(PROJECT_ROOT)

        self.assertEqual(
            set(folders),
            set(resolver.ARCHITECTURE_AUDIT_SUBFOLDER_NAMES),
        )
        for name, path in folders.items():
            self.assertEqual(path.name, name)

    def test_assert_audit_root_outside_project_accepts_external_root(self) -> None:
        audit_root = resolver.get_architecture_audit_root(PROJECT_ROOT)

        self.assertEqual(
            resolver.assert_architecture_audit_root_outside_project(
                audit_root,
                PROJECT_ROOT,
            ),
            audit_root.resolve(),
        )

    def test_assert_audit_root_outside_project_rejects_inside_root(self) -> None:
        inside = PROJECT_ROOT / "kanda_reasoner_architecture_audit"

        with self.assertRaises(ValueError):
            resolver.assert_architecture_audit_root_outside_project(
                inside,
                PROJECT_ROOT,
            )

    def test_ensure_current_structure_creates_only_explicit_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "demo_project"
            project_root.mkdir()

            folders = resolver.ensure_architecture_audit_current_structure(
                project_root,
            )

            for path in folders.values():
                self.assertTrue(path.exists())
                self.assertTrue(path.is_dir())

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER",
            "ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES",
            "ARCHITECTURE_AUDIT_CURRENT_FOLDER",
            "ARCHITECTURE_AUDIT_DOMAIN",
            "ARCHITECTURE_AUDIT_RUNS_FOLDER",
            "ARCHITECTURE_AUDIT_SUBFOLDER_NAMES",
            "ARCHITECTURE_AUDIT_TIMESTAMP_FORMAT",
            "assert_architecture_audit_root_outside_project",
            "build_architecture_audit_root_from_drive_or_anchor",
            "build_architecture_audit_run_id",
            "ensure_architecture_audit_current_structure",
            "get_architecture_audit_artifact_path",
            "get_architecture_audit_current_root",
            "get_architecture_audit_current_subfolders",
            "get_architecture_audit_root",
            "get_architecture_audit_run_root",
            "get_architecture_audit_subfolder",
            "get_project_slug",
        }

        self.assertEqual(set(resolver.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(resolver, name))

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(resolver)
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "D:\\",
            "developer_tools",
            "project_analysis_evidence",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
