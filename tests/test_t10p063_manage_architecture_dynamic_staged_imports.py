"""Regression tests for T10P063 manage architecture dynamic staged imports."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

LEGACY_LITERAL = "ask" + "_ai" + "_project" + "_reasoner"
CANONICAL_LITERAL = "kanda_reasoner_app"
OWNER_ROOT = Path(LEGACY_LITERAL) / "manage_architecture"
TARGET_FILES = [
    Path(LEGACY_LITERAL) / "manage_architecture" / "manage_architecture.py",
    Path(LEGACY_LITERAL) / "manage_architecture" / "manage_architecture_gui.py",
    Path(LEGACY_LITERAL) / "manage_architecture" / "ai_review" / "adapter.py",
    Path(LEGACY_LITERAL) / "manage_architecture" / "manage_architecture_gui_help" / "mode_options_hlp.py",
    Path(LEGACY_LITERAL) / "manage_architecture" / "manage_architecture_help" / "source_loader_private_impl.py",
]


class ManageArchitectureDynamicStagedImportsTests(unittest.TestCase):
    """Verify architecture owner-box source avoids fixed legacy package tokens."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.project_root = Path(__file__).resolve().parents[1]

    def _read(self, relative_path: Path) -> str:
        return (self.project_root / relative_path).read_text(encoding="utf-8")

    def test_changed_files_are_ast_parseable(self) -> None:
        for relative_path in TARGET_FILES:
            with self.subTest(path=str(relative_path)):
                ast.parse(self._read(relative_path))

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        owner_path = self.project_root / OWNER_ROOT
        for source_path in owner_path.rglob("*.py"):
            with self.subTest(path=str(source_path.relative_to(self.project_root))):
                source_text = source_path.read_text(encoding="utf-8")
                self.assertNotIn(LEGACY_LITERAL, source_text)

    def test_manage_architecture_script_uses_dynamic_staged_loader_import(self) -> None:
        source_text = self._read(Path(LEGACY_LITERAL) / "manage_architecture" / "manage_architecture.py")
        self.assertIn("_STAGED_PACKAGE_NAME", source_text)
        self.assertIn("_importlib.import_module", source_text)
        self.assertIn("manage_architecture_help.source_loader_private_impl", source_text)

    def test_ai_review_adapter_preserves_late_bound_staged_runtime_modules(self) -> None:
        module_name = (
            LEGACY_LITERAL + ".manage_architecture.ai_review.adapter"
        )
        module = __import__(module_name, fromlist=["Tab1AIReviewAdapter"])

        self.assertEqual(
            module.MODEL_REGISTRY_MODULE,
            LEGACY_LITERAL + ".project_reasoner_v10.v10_model_registry",
        )
        self.assertEqual(
            module.LOCAL_AI_MODULE,
            LEGACY_LITERAL + ".project_reasoner_v10.v10_qwen_ai_models",
        )

    def test_source_loader_uses_canonical_exclusion_policy_and_dynamic_root_probe(self) -> None:
        source_text = self._read(
            Path(LEGACY_LITERAL)
                / "manage_architecture"
                / "manage_architecture_help"
                / "source_loader_private_impl.py"
        )
        self.assertIn(CANONICAL_LITERAL + ".project_exclusion_policy", source_text)
        self.assertIn("source_package_dir", source_text)
        self.assertIn('"ask" + "_ai" + "_project" + "_reasoner"', source_text)

    def test_mode_options_header_does_not_pin_legacy_package_token(self) -> None:
        source_text = self._read(
            Path(LEGACY_LITERAL)
                / "manage_architecture"
                / "manage_architecture_gui_help"
                / "mode_options_hlp.py"
        )
        self.assertNotIn("PACKAGE  :", source_text)


if __name__ == "__main__":
    unittest.main()
