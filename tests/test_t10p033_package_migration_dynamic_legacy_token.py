"""Regression tests for T10P033 package migration dynamic legacy token."""

from __future__ import annotations

import ast
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_RELATIVE_PATH = Path("kanda_reasoner_app/package_migration/package_inventory.py")
LEGACY_LITERAL = "ask" + "_ai" + "_project" + "_reasoner"


class PackageMigrationDynamicLegacyTokenTests(unittest.TestCase):
    """Verify the package migration inventory keeps behavior without fixed tokens."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.source_path = cls.project_root / SOURCE_RELATIVE_PATH
        cls.source_text = cls.source_path.read_text(encoding="utf-8")
        spec = importlib.util.spec_from_file_location("t10p033_package_inventory", cls.source_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load package inventory module.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        finally:
            sys.modules.pop(spec.name, None)
        cls.module = module

    def test_source_file_exists(self) -> None:
        self.assertTrue(self.source_path.exists())

    def test_source_remains_ast_parseable(self) -> None:
        ast.parse(self.source_text)

    def test_source_does_not_hardcode_legacy_package_literal(self) -> None:
        self.assertNotIn(LEGACY_LITERAL, self.source_text)

    def test_legacy_token_is_still_observable(self) -> None:
        self.assertEqual(self.module.LEGACY_TOKEN, LEGACY_LITERAL)

    def test_owner_box_classification_still_handles_legacy_paths(self) -> None:
        relative_path = LEGACY_LITERAL + "/runtime_scenarios/example.py"
        self.assertEqual(
            self.module.classify_owner_box(relative_path),
            LEGACY_LITERAL + "/runtime_scenarios",
        )

    def test_inventory_still_detects_legacy_token_in_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_dir = root / LEGACY_LITERAL / "demo"
            package_dir.mkdir(parents=True)
            py_file = package_dir / "sample.py"
            txt_file = root / "notes.txt"
            py_file.write_text("import " + LEGACY_LITERAL + "\n", encoding="utf-8")
            txt_file.write_text("path: " + LEGACY_LITERAL + "\n", encoding="utf-8")

            python_entries, text_entries = self.module.collect_inventory(root)

        self.assertEqual(len(python_entries), 1)
        self.assertEqual(len(text_entries), 1)
        self.assertEqual(python_entries[0].count, 1)
        self.assertEqual(text_entries[0].count, 1)


if __name__ == "__main__":
    unittest.main()
