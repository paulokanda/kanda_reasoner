"""Validate that .project_reference is treated as hidden human/reference space.

The dot-prefixed .project_reference folder lives inside the project root for
human convenience, but it is not active project source. Project scanners and
architecture validators must ignore it the same way they already ignore the
legacy _project_reference folder.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.project_exclusion_policy import (
    filter_reasoner_path_strings,
    iter_reasoner_project_files,
    load_reasoner_project_exclusion_rules,
    should_exclude_reasoner_project_path,
)
from kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl import (
    load_manage_architecture_source,
)
from kanda_reasoner_app.reasoner_symbol_atlas.reference_folder_policy import (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
    is_reasoner_symbol_atlas_reference_path,
)


class DotProjectReferenceExclusionPolicyTests(unittest.TestCase):
    def test_shared_exclusion_rules_include_dot_project_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rules = load_reasoner_project_exclusion_rules(root)

        self.assertIn(".project_reference", rules["folders"])
        self.assertIn("_project_reference", rules["folders"])

    def test_dot_project_reference_paths_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hidden_note = root / ".project_reference" / "notes" / "example.py"
            hidden_note.parent.mkdir(parents=True)
            hidden_note.write_text("SHOULD_NOT_BE_SCANNED = True\n", encoding="utf-8")

            active_file = root / "kanda_reasoner_app" / "active_module.py"
            active_file.parent.mkdir(parents=True)
            active_file.write_text("ACTIVE = True\n", encoding="utf-8")

            self.assertTrue(should_exclude_reasoner_project_path(hidden_note, root))
            self.assertFalse(should_exclude_reasoner_project_path(active_file, root))

            scanned = {path.relative_to(root).as_posix() for path in iter_reasoner_project_files(root, suffixes=(".py",))}
            self.assertIn("kanda_reasoner_app/active_module.py", scanned)
            self.assertNotIn(".project_reference/notes/example.py", scanned)

    def test_filter_path_strings_removes_dot_project_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kept = "kanda_reasoner_app/live.py"
            removed = ".project_reference/human_notes.py"
            filtered = filter_reasoner_path_strings([kept, removed], root)

        self.assertIn(kept, filtered)
        self.assertNotIn(removed, filtered)

    def test_architecture_loader_excludes_dot_project_reference(self) -> None:
        source = load_manage_architecture_source()
        self.assertIn('".project_reference"', source)
        self.assertIn('"_project_reference"', source)

    def test_symbol_atlas_reference_policy_treats_dot_folder_as_inactive(self) -> None:
        self.assertIn(".project_reference", PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS)
        self.assertTrue(is_reasoner_symbol_atlas_reference_path(".project_reference/chats/example.py"))
        self.assertTrue(is_reasoner_symbol_atlas_reference_path("_project_reference/chats/example.py"))
        self.assertFalse(is_reasoner_symbol_atlas_reference_path("kanda_reasoner_app/live.py"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
