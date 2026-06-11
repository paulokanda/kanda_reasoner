"""Tests for Kanda Reasoner storage policy backup path resolver."""

from __future__ import annotations

import inspect
from pathlib import Path
import time
import unittest

from kanda_reasoner_app.storage_policy import patch_restore_resolver
from kanda_reasoner_app.storage_policy.patch_restore_resolver import (
    BACKUP_RESTORE_SEARCH_SUBFOLDERS,
    PATCH_BACKUP_TIMESTAMP_FORMAT,
    PatchBackupCandidate,
    build_patch_backup_folder_name,
    ensure_patch_backup_path,
    find_latest_patch_backup,
    get_backup_restore_search_roots,
    get_patch_backup_path,
)


class StoragePolicyPatchRestoreResolverTests(unittest.TestCase):
    """Validate backup path resolver behavior."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "BACKUP_RESTORE_SEARCH_SUBFOLDERS",
            "PATCH_BACKUP_TIMESTAMP_FORMAT",
            "PatchBackupCandidate",
            "build_patch_backup_folder_name",
            "ensure_patch_backup_path",
            "find_latest_patch_backup",
            "get_backup_restore_search_roots",
            "get_patch_backup_path",
        }

        self.assertEqual(set(patch_restore_resolver.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(patch_restore_resolver, name))

    def test_timestamp_format_is_windows_filename_safe(self) -> None:
        self.assertEqual(PATCH_BACKUP_TIMESTAMP_FORMAT, "%Y%m%d_%H%M%S")
        self.assertNotIn(":", PATCH_BACKUP_TIMESTAMP_FORMAT)

    def test_build_patch_backup_folder_name_is_stable(self) -> None:
        folder_name = build_patch_backup_folder_name(
            "My Patch Name",
            timestamp="20260101_120000",
        )

        self.assertEqual(folder_name, "my_patch_name_20260101_120000")

    def test_build_patch_backup_folder_name_rejects_empty_patch(self) -> None:
        with self.assertRaises(ValueError):
            build_patch_backup_folder_name("---", timestamp="20260101_120000")

    def test_get_patch_backup_path_does_not_create_folder(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            maintenance_root = Path(tmp_dir) / "maintenance"
            path = get_patch_backup_path(
                "my_patch",
                timestamp="20260101_120000",
                maintenance_root=maintenance_root,
            )

            self.assertEqual(path.name, "my_patch_20260101_120000")
            self.assertEqual(path.parent, maintenance_root / "backups" / "patches")
            self.assertFalse(path.exists())

    def test_ensure_patch_backup_path_creates_only_explicit_path(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            maintenance_root = Path(tmp_dir) / "maintenance"
            path = ensure_patch_backup_path(
                "my_patch",
                timestamp="20260101_120000",
                maintenance_root=maintenance_root,
            )

            self.assertTrue(path.exists())
            self.assertTrue(path.is_dir())
            self.assertEqual(path.parent, maintenance_root / "backups" / "patches")

    def test_restore_search_roots_order_is_new_first_legacy_second(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            maintenance_root = base / "maintenance"
            roots = get_backup_restore_search_roots(
                maintenance_root=maintenance_root,
                drive_or_anchor=str(base),
            )

            self.assertEqual(roots[0], maintenance_root / "backups" / "patches")
            self.assertEqual(roots[1], maintenance_root / "backups" / "restore")
            self.assertEqual(roots[2], base / "_kanda_patch_backups")
            self.assertEqual(roots[3], base / "_kanda_restore_points")
            self.assertEqual(
                BACKUP_RESTORE_SEARCH_SUBFOLDERS,
                ("patch_backups", "restore_points"),
            )

    def test_find_latest_patch_backup_returns_none_when_absent(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = find_latest_patch_backup(
                "absent_patch",
                maintenance_root=Path(tmp_dir) / "maintenance",
                drive_or_anchor=tmp_dir,
            )

            self.assertIsNone(result)

    def test_find_latest_patch_backup_finds_new_storage_candidate(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            maintenance_root = Path(tmp_dir) / "maintenance"
            folder = ensure_patch_backup_path(
                "my_patch",
                timestamp="20260101_120000",
                maintenance_root=maintenance_root,
            )

            result = find_latest_patch_backup(
                "my_patch",
                maintenance_root=maintenance_root,
                drive_or_anchor=tmp_dir,
            )

            self.assertIsInstance(result, PatchBackupCandidate)
            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(Path(result.path), folder)
            self.assertTrue(result.exists)
            self.assertEqual(result.source_name, "patches")

    def test_find_latest_patch_backup_prefers_newest_candidate(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            maintenance_root = Path(tmp_dir) / "maintenance"
            older = ensure_patch_backup_path(
                "my_patch",
                timestamp="20260101_120000",
                maintenance_root=maintenance_root,
            )
            time.sleep(0.01)
            newer = ensure_patch_backup_path(
                "my_patch",
                timestamp="20260101_120001",
                maintenance_root=maintenance_root,
            )

            result = find_latest_patch_backup(
                "my_patch",
                maintenance_root=maintenance_root,
                drive_or_anchor=tmp_dir,
            )

            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(Path(result.path), newer)
            self.assertNotEqual(Path(result.path), older)

    def test_find_latest_patch_backup_can_search_legacy_fallback(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            legacy_folder = base / "_kanda_patch_backups"
            candidate = legacy_folder / "my_patch_20260101_120000"
            candidate.mkdir(parents=True)

            result = find_latest_patch_backup(
                "my_patch",
                maintenance_root=base / "maintenance",
                drive_or_anchor=str(base),
            )

            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(Path(result.path), candidate)
            self.assertEqual(result.source_name, "_kanda_patch_backups")

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(patch_restore_resolver)
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "E:",
            "kanda_reasoner_architecture_audit",
            "project_analysis_evidence",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
