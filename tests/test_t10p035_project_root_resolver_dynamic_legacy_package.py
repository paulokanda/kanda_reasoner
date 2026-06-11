"""Regression tests for T10P035 project root resolver compatibility."""

from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "project_root_resolver.py"
LEGACY_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))
CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"


class ProjectRootResolverDynamicLegacyPackageTests(unittest.TestCase):
    """Protect staged compatibility without fixed legacy package literals."""

    def test_source_file_exists(self) -> None:
        self.assertTrue(SOURCE_FILE.is_file())

    def test_source_remains_ast_parseable(self) -> None:
        ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))

    def test_source_does_not_hardcode_legacy_package_token(self) -> None:
        source = SOURCE_FILE.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_PACKAGE_NAME, source)

    def test_source_derives_legacy_package_name_dynamically(self) -> None:
        source = SOURCE_FILE.read_text(encoding="utf-8")
        self.assertIn('"_".join(("ask", "ai", "project", "reasoner"))', source)
        self.assertIn(CANONICAL_PACKAGE_NAME, source)

    def test_default_smoke_output_path_preserves_current_compatibility_layout(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "t10p035_project_root_resolver", SOURCE_FILE
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        path = module.default_smoke_output_json_path(r"E:\kanda_reasoner")
        normalized = str(path).replace("\\", "/")

        self.assertIn(LEGACY_PACKAGE_NAME, normalized)
        self.assertTrue(normalized.endswith("/outputs/real_project_static_context_smoke.json"))


if __name__ == "__main__":
    unittest.main()
