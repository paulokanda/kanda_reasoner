"""Tests for the package migration inventory helper."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.package_migration import package_inventory
from kanda_reasoner_app.package_migration.package_inventory import collect_inventory


class LegacyPackageReferenceInventoryTests(unittest.TestCase):
    """Verify the non-mutating package inventory helper."""

    def test_inventory_module_declares_public_surface(self) -> None:
        expected = {
            "CANONICAL_TOKEN",
            "InventoryEntry",
            "LEGACY_TOKEN",
            "LEGACY_TOKEN_PARTS",
            "OwnerBoxSummary",
            "build_argument_parser",
            "classify_owner_box",
            "collect_inventory",
            "collect_owner_box_summary",
            "iter_candidate_files",
            "main",
        }

        self.assertEqual(set(package_inventory.__all__), expected)

    def test_inventory_excludes_workbench_and_reference_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_dir = root / "src"
            source_dir.mkdir()
            (source_dir / "active_module.py").write_text(
                'import ask_' 'ai_project_reasoner' '\n',
                encoding="utf-8",
            )

            reference_dir = root / "project_freeze_ledger"
            reference_dir.mkdir()
            (reference_dir / "note.py").write_text(
                'import ask_' 'ai_project_reasoner' '\n',
                encoding="utf-8",
            )

            workbench_dir = root / "workbench" / "bundle_manifest"
            workbench_dir.mkdir(parents=True)
            (workbench_dir / "manifest.txt").write_text(
                'ask_' 'ai_project_reasoner' '\n',
                encoding="utf-8",
            )

            python_entries, text_entries = collect_inventory(root)

        self.assertEqual([entry.relative_path for entry in python_entries], ["src/active_module.py"])
        self.assertEqual(text_entries, [])

    def test_inventory_separates_python_and_text_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module.py").write_text(
                'from ask_' 'ai_project_reasoner.demo import value\n',
                encoding="utf-8",
            )
            (root / "notes.md").write_text(
                'Path: ask_' 'ai_project_reasoner' '/demo.py\n',
                encoding="utf-8",
            )

            python_entries, text_entries = collect_inventory(root)

        self.assertEqual(len(python_entries), 1)
        self.assertEqual(python_entries[0].relative_path, "module.py")
        self.assertEqual(python_entries[0].count, 1)
        self.assertEqual(len(text_entries), 1)
        self.assertEqual(text_entries[0].relative_path, "notes.md")
        self.assertEqual(text_entries[0].count, 1)


if __name__ == "__main__":
    unittest.main()
