"""Tests for canonical maintenance subfolder policy."""

from __future__ import annotations

import inspect
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy import maintenance_subfolder_policy
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    MAINTENANCE_SUBFOLDER_NAMES,
    MAINTENANCE_SUBFOLDER_PARTS,
    describe_maintenance_subfolder_policy,
    ensure_maintenance_structure,
    ensure_maintenance_subfolder,
    get_all_maintenance_subfolders,
    get_maintenance_subfolder,
    relative_maintenance_subfolder_parts,
)


class StoragePolicyMaintenanceSubfolderPolicyTests(unittest.TestCase):
    """Validate the side-effect-free canonical maintenance subfolder policy."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "MAINTENANCE_SUBFOLDER_NAMES",
            "MAINTENANCE_SUBFOLDER_PARTS",
            "describe_maintenance_subfolder_policy",
            "ensure_maintenance_structure",
            "ensure_maintenance_subfolder",
            "get_all_maintenance_subfolders",
            "get_maintenance_subfolder",
            "relative_maintenance_subfolder_parts",
        }

        self.assertEqual(set(maintenance_subfolder_policy.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(maintenance_subfolder_policy, name))

    def test_canonical_subfolder_names_include_expected_policy(self) -> None:
        expected = {
            "patch_backups",
            "restore_points",
            "pre_commit_backups",
            "failed_patch_payloads",
            "scratch_extracts",
            "scratch_cache",
            "scratch_temp_work",
            "scratch_downloads",
            "quarantine_manual",
            "quarantine_autodelete",
            "install_logs",
            "runtime_logs",
            "audit_logs",
            "migration_logs",
            "build_outputs",
            "release_outputs",
            "legacy_absorbed",
            "migrated_evidence",
            "crash_dumps",
            "diagnostic_screenshots",
            "staging",
        }

        self.assertEqual(set(MAINTENANCE_SUBFOLDER_NAMES), expected)
        self.assertEqual(set(MAINTENANCE_SUBFOLDER_PARTS), expected)

    def test_get_subfolder_builds_nested_path_without_creating(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "maintenance_root"
            folder = get_maintenance_subfolder("patch_backups", root)

            self.assertEqual(folder, root / "backups" / "patches")
            self.assertFalse(folder.exists())
            self.assertFalse(root.exists())

    def test_get_all_subfolders_returns_every_canonical_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "maintenance_root"
            folders = get_all_maintenance_subfolders(root)

            self.assertEqual(set(folders), set(MAINTENANCE_SUBFOLDER_NAMES))
            self.assertEqual(
                folders["restore_points"],
                root / "backups" / "restore",
            )
            self.assertEqual(
                folders["migrated_evidence"],
                root / "migration" / "migrated_evidence",
            )
            self.assertFalse(root.exists())

    def test_ensure_one_subfolder_creates_only_requested_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "maintenance_root"
            folder = ensure_maintenance_subfolder("scratch_extracts", root)

            self.assertTrue(folder.exists())
            self.assertEqual(folder, root / "scratch" / "extracts")
            self.assertFalse((root / "backups" / "patches").exists())

    def test_ensure_structure_creates_every_canonical_subfolder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "maintenance_root"
            folders = ensure_maintenance_structure(root)

            self.assertEqual(set(folders), set(MAINTENANCE_SUBFOLDER_NAMES))
            for folder in folders.values():
                self.assertTrue(folder.exists())
                self.assertTrue(folder.is_dir())

    def test_unknown_subfolder_raises(self) -> None:
        with self.assertRaises(ValueError):
            get_maintenance_subfolder("random_folder")

        with self.assertRaises(ValueError):
            relative_maintenance_subfolder_parts("random_folder")

    def test_relative_parts_are_stable(self) -> None:
        self.assertEqual(
            relative_maintenance_subfolder_parts("failed_patch_payloads"),
            ("backups", "failed_patches"),
        )
        self.assertEqual(
            relative_maintenance_subfolder_parts("diagnostic_screenshots"),
            ("diagnostics", "screenshots"),
        )

    def test_describe_policy_returns_copy(self) -> None:
        policy = describe_maintenance_subfolder_policy()

        self.assertEqual(policy, MAINTENANCE_SUBFOLDER_PARTS)
        self.assertIsNot(policy, MAINTENANCE_SUBFOLDER_PARTS)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(maintenance_subfolder_policy)
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
