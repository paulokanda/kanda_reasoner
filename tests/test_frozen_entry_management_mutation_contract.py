#!/usr/bin/env python3
# project-path: tests/test_frozen_entry_management_mutation_contract.py
"""Regression tests for governed frozen-entry mutation and recovery."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.freeze_after_update.frozen_entry_management import (
    activate_frozen_entries,
    delete_last_deprecated_entry,
    delete_selected_deprecated_entries,
    inactivate_frozen_entries,
    list_managed_frozen_entries,
    undelete_last_frozen_entry,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths


def _write_entry(
    path: Path,
    *,
    freeze_id: str,
    title: str,
    date_text: str,
    status: str = "frozen",
    superseded_by: str = "null",
) -> None:
    """Write one deterministic frozen-entry fixture."""
    path.write_text(
        "---\n"
        f'freeze_id: "{freeze_id}"\n'
        f'feature_title: "{title}"\n'
        'box: "test.freeze.box"\n'
        f'status: "{status}"\n'
        f'date: "{date_text}"\n'
        f"superseded_by: {superseded_by}\n"
        "---\n\n"
        f"# {title}\n",
        encoding="utf-8",
        newline="\n",
    )


class FrozenEntryManagementMutationContractTests(unittest.TestCase):
    """Exercise the real mutation, persistence, and recovery boundary."""

    def setUp(self) -> None:
        """Create one isolated project and external support box."""
        self._temporary = tempfile.TemporaryDirectory(
            prefix="kanda_frozen_entry_management_test_"
        )
        self.project_root = Path(self._temporary.name) / "fixture_project"
        self.project_root.mkdir()
        self.paths = build_paths(self.project_root)
        self.support_root = self.paths.box_root.parent
        self.paths.entries_root.mkdir(parents=True)

    def tearDown(self) -> None:
        """Remove both the temporary project and its sibling support root."""
        shutil.rmtree(self.support_root, ignore_errors=True)
        self._temporary.cleanup()

    def _entry(
        self,
        name: str,
        *,
        date_text: str,
        status: str = "frozen",
        superseded_by: str = "null",
    ) -> Path:
        """Create and return one canonical entry path."""
        path = self.paths.entries_root / name
        _write_entry(
            path,
            freeze_id=path.stem,
            title=path.stem,
            date_text=date_text,
            status=status,
            superseded_by=superseded_by,
        )
        return path

    def test_active_state_and_selected_delete_round_trip(self) -> None:
        """Protect active entries and round-trip one deprecated selection."""
        older = self._entry("freeze-20260801-older.md", date_text="2026-08-01")
        newer = self._entry("freeze-20260802-newer.md", date_text="2026-08-02")

        entries = list_managed_frozen_entries(self.project_root)
        self.assertEqual(
            [item["freeze_id"] for item in entries],
            [newer.stem, older.stem],
        )

        with self.assertRaisesRegex(ValueError, "Active frozen entries cannot be deleted"):
            delete_selected_deprecated_entries(self.project_root, [newer])
        self.assertTrue(newer.is_file())

        inactivated = inactivate_frozen_entries(self.project_root, [newer])
        self.assertTrue(inactivated["ok"])
        self.assertEqual(inactivated["changed_paths"], [str(newer)])
        self.assertFalse(list_managed_frozen_entries(self.project_root)[0]["active"])

        deleted = delete_selected_deprecated_entries(self.project_root, [newer])
        moved = deleted["deleted"][0]
        deleted_path = Path(moved["to"])
        self.assertEqual(moved["from"], str(newer))
        self.assertFalse(newer.exists())
        self.assertTrue(deleted_path.is_file())
        self.assertEqual(deleted_path.parent.name, "deleted_entries")

        index = json.loads(self.paths.freeze_index.read_text(encoding="utf-8"))
        self.assertEqual(
            [item["freeze_id"] for item in index["freezes"]],
            [older.stem],
        )

        restored = undelete_last_frozen_entry(self.project_root)
        self.assertEqual(restored["restored_to"], str(newer))
        self.assertTrue(newer.is_file())

        activated = activate_frozen_entries(self.project_root, [newer])
        self.assertTrue(activated["active"])
        restored_text = newer.read_text(encoding="utf-8-sig")
        self.assertIn('status: "frozen"', restored_text)
        self.assertIn("superseded_by: null", restored_text)

    def test_delete_last_and_path_escape_guards(self) -> None:
        """Delete only the newest deprecated entry and reject path escape."""
        active = self._entry("freeze-20260801-active.md", date_text="2026-08-01")
        older = self._entry(
            "freeze-20260802-deprecated.md",
            date_text="2026-08-02",
            status="deprecated",
        )
        newer = self._entry(
            "freeze-20260803-superseded.md",
            date_text="2026-08-03",
            superseded_by='"freeze-20260804-replacement"',
        )

        result = delete_last_deprecated_entry(self.project_root)
        self.assertEqual(result["deleted_last"], str(newer))
        self.assertFalse(newer.exists())
        self.assertTrue(active.is_file())
        self.assertTrue(older.is_file())

        restored = undelete_last_frozen_entry(self.project_root)
        self.assertEqual(restored["restored_to"], str(newer))

        outside = self.project_root / "freeze-outside.md"
        _write_entry(
            outside,
            freeze_id="freeze-outside",
            title="outside",
            date_text="2026-08-04",
            status="deprecated",
        )
        with self.assertRaisesRegex(ValueError, "outside the canonical entries folder"):
            delete_selected_deprecated_entries(self.project_root, [outside])
        self.assertTrue(outside.is_file())

        with self.assertRaisesRegex(ValueError, "Select at least one frozen entry"):
            inactivate_frozen_entries(self.project_root, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
