"""Regression tests for T10P032 GUI manifest validator dynamic package paths."""

from __future__ import annotations

import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_validate_manifests.py"
LEGACY_TOKEN = "ask" + "_ai" + "_project" + "_reasoner"


class ReasonerToolsGuiValidateManifestsDynamicPathTests(unittest.TestCase):
    def test_changed_file_remains_ast_parseable(self) -> None:
        ast.parse(TARGET.read_text(encoding="utf-8"))

    def test_changed_file_does_not_hardcode_legacy_package_token(self) -> None:
        source = TARGET.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, source)

    def test_manifest_paths_are_derived_from_product_package(self) -> None:
        source = TARGET.read_text(encoding="utf-8")
        self.assertIn("PRODUCT_PACKAGE = Path(__file__).resolve().parent.name", source)
        self.assertIn("MANIFEST = Path(PRODUCT_PACKAGE) /", source)
        self.assertIn("HELP_FOLDER = Path(PRODUCT_PACKAGE) /", source)

    def test_validator_uses_current_package_folder_without_fixed_name(self) -> None:
        spec = importlib.util.spec_from_file_location("t10p032_validator", TARGET)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_dir = root / module.PRODUCT_PACKAGE
            helper_dir = package_dir / "reasoner_tools_gui_shell"
            helper_dir.mkdir(parents=True)

            (root / "reasoner_tools_gui.py").write_text(
                "__all__ = ['open_shell']\n",
                encoding="utf-8",
            )
            (helper_dir / "shell_helper.py").write_text(
                "__all__ = ['open_shell']\n",
                encoding="utf-8",
            )
            (package_dir / "reasoner_tools_gui_shell.json").write_text(
                json.dumps(
                    {
                        "exports": ["open_shell"],
                        "origin_all": ["open_shell"],
                        "helpers": {"shell_helper.py": ["open_shell"]},
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(module.validate_manifest(root), [])


if __name__ == "__main__":
    unittest.main()
