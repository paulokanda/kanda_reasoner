"""Tests for owner-box summaries in the package migration inventory."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.package_migration import package_inventory
from kanda_reasoner_app.package_migration.package_inventory import (
    InventoryEntry,
    classify_owner_box,
    collect_inventory,
    collect_owner_box_summary,
)


class LegacyReferenceOwnerBoxSummaryTests(unittest.TestCase):
    """Verify owner-box summaries for legacy package references."""

    def test_inventory_module_declares_owner_summary_public_surface(self) -> None:
        expected_names = {
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

        self.assertEqual(set(package_inventory.__all__), expected_names)

    def test_classify_owner_box_uses_first_package_subfolder(self) -> None:
        self.assertEqual(
            classify_owner_box('ask_' 'ai_project_reasoner' '/manage_workflows/demo.py'),
            'ask_' 'ai_project_reasoner' '/manage_workflows',
        )
        self.assertEqual(
            classify_owner_box('ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/demo.py'),
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui',
        )
        self.assertEqual(classify_owner_box("reasoner_tools_gui.py"), "reasoner_tools_gui.py")
        self.assertEqual(classify_owner_box("tests/test_demo.py"), "tests")

    def test_collect_owner_box_summary_counts_python_and_text_references(self) -> None:
        python_entries = [
            InventoryEntry('ask_' 'ai_project_reasoner' '/manage_workflows/a.py', 2),
            InventoryEntry('ask_' 'ai_project_reasoner' '/manage_workflows/b.py', 1),
            InventoryEntry("reasoner_tools_gui.py", 1),
        ]
        text_entries = [
            InventoryEntry('ask_' 'ai_project_reasoner' '/manage_workflows/help.json', 4),
            InventoryEntry('ask_' 'ai_project_reasoner' '/prompt_library/README.md', 3),
        ]

        summary = collect_owner_box_summary(python_entries, text_entries)
        by_owner = {entry.owner_box: entry for entry in summary}

        workflows = by_owner['ask_' 'ai_project_reasoner' '/manage_workflows']
        self.assertEqual(workflows.python_files, 2)
        self.assertEqual(workflows.python_references, 3)
        self.assertEqual(workflows.text_files, 1)
        self.assertEqual(workflows.text_references, 4)

        prompt_library = by_owner['ask_' 'ai_project_reasoner' '/prompt_library']
        self.assertEqual(prompt_library.python_files, 0)
        self.assertEqual(prompt_library.text_files, 1)

    def test_inventory_and_owner_summary_use_real_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_dir = root / 'ask_' 'ai_project_reasoner' / "demo_box"
            package_dir.mkdir(parents=True)
            (package_dir / "module.py").write_text(
                'import ask_' 'ai_project_reasoner' '\n',
                encoding="utf-8",
            )
            (package_dir / "help.md").write_text(
                'ask_' 'ai_project_reasoner' ' path\n',
                encoding="utf-8",
            )

            python_entries, text_entries = collect_inventory(root)
            summary = collect_owner_box_summary(python_entries, text_entries)

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0].owner_box, 'ask_' 'ai_project_reasoner' '/demo_box')
        self.assertEqual(summary[0].python_files, 1)
        self.assertEqual(summary[0].text_files, 1)


if __name__ == "__main__":
    unittest.main()
