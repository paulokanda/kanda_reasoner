"""Focused tests for stale renamed folder cleanup."""

from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

import tools.kanda_stale_folder_cleanup as stale_cleanup
from tools.kanda_stale_folder_cleanup import (
    STALE_ACTIVE_FOLDERS,
    build_stale_folder_report,
    delete_stale_folders,
)


def make_canonical_folders(root: Path) -> None:
    """Create canonical folders required by the cleanup guard."""

    for relative_path in (
        "kanda_reasoner_app/reasoner_engine",
        "kanda_reasoner_app/reasoner_context_collector",
        "kanda_reasoner_app/reasoner_runtime_collector",
        "kanda_reasoner_app/reasoner_symbol_atlas",
    ):
        (root / Path(relative_path)).mkdir(parents=True, exist_ok=True)


class KandaStaleFolderCleanupTests(unittest.TestCase):
    """Protect stale renamed folder cleanup behavior."""

    def test_public_surface_uses_unique_names(self) -> None:
        exported_names = getattr(stale_cleanup, "__all__", None)

        self.assertIsInstance(exported_names, list)
        self.assertIn("build_stale_folder_report", exported_names)
        self.assertIn("parse_stale_folder_cleanup_args", exported_names)
        self.assertNotIn("build_report", exported_names)
        self.assertNotIn("parse_args", exported_names)

        missing_names = [
            name
            for name in exported_names
            if not hasattr(stale_cleanup, name)
        ]
        self.assertEqual([], missing_names)

    def test_report_lists_all_stale_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            make_canonical_folders(root)

            report = build_stale_folder_report(root)
            listed = {
                item["relative_path"]
                for item in report["stale_folders"]
            }

            self.assertEqual(set(STALE_ACTIVE_FOLDERS), listed)
            self.assertEqual(0, report["present_count"])

    def test_delete_stale_folder_with_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            backup = Path(temp_dir) / "backup"
            make_canonical_folders(root)

            stale = root / "kanda_reasoner_app" / "project_symbol_atlas"
            stale.mkdir(parents=True)
            (stale / "old.txt").write_text("old", encoding="utf-8")

            report = delete_stale_folders(root, backup)

            self.assertFalse(stale.exists())
            self.assertTrue(
                (
                    backup
                    / "kanda_reasoner_app"
                    / "project_symbol_atlas"
                    / "old.txt"
                ).exists()
            )
            self.assertEqual(1, report["deleted_count"])

    def test_backup_inside_project_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            make_canonical_folders(root)

            with self.assertRaises(ValueError):
                delete_stale_folders(root, root / "_bad_backup")


if __name__ == "__main__":
    unittest.main()
