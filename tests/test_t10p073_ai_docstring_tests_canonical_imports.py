"""Regression tests for canonical imports in AI-docstring test modules."""

from __future__ import annotations

from pathlib import Path
import ast
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TESTS_ROOT = PROJECT_ROOT / "tests"
LEGACY_TOKEN = "_".join(("ask", "ai", "project", "reasoner"))
CANONICAL_TOKEN = "kanda_reasoner_app"


class AiDocstringTestsCanonicalImportsTests(unittest.TestCase):
    """Keep AI-docstring tests off legacy import syntax during migration."""

    def test_ai_docstring_tests_do_not_use_legacy_dotted_imports(self) -> None:
        offenders: list[str] = []
        forbidden_fragments = (
            f"from {LEGACY_TOKEN}.",
            f"import {LEGACY_TOKEN}.",
            f'"{LEGACY_TOKEN}.',
            f"'{LEGACY_TOKEN}.",
        )

        for path in sorted(TESTS_ROOT.glob("test_ai_docstring*.py")):
            source = path.read_text(encoding="utf-8")
            for fragment in forbidden_fragments:
                if fragment in source:
                    offenders.append(f"{path.relative_to(PROJECT_ROOT)} contains {fragment!r}")

        self.assertEqual([], offenders)

    def test_ai_docstring_tests_use_canonical_dotted_imports(self) -> None:
        source = (TESTS_ROOT / "test_ai_docstring_response_parsing.py").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            f"from {CANONICAL_TOKEN}.insert_missing_docstrings_gui.ai_config import",
            source,
        )
        self.assertIn(
            f"from {CANONICAL_TOKEN}.insert_missing_docstrings_gui.ai_docstring_generator import",
            source,
        )

    def test_staged_physical_path_references_are_not_rewritten_blindly(self) -> None:
        target = TESTS_ROOT / "test_ai_docstring_safe_mode_actual_gui_smoke.py"
        source = target.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(target))

        target_gui_value = None
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(
                isinstance(item, ast.Name) and item.id == "TARGET_GUI"
                for item in node.targets
            ):
                continue
            target_gui_value = ast.literal_eval(node.value)
            break

        self.assertIsNotNone(target_gui_value)
        self.assertIn(f"{LEGACY_TOKEN}/insert_missing_docstrings_gui/", target_gui_value)
        self.assertNotIn(f"{CANONICAL_TOKEN}/insert_missing_docstrings_gui/", target_gui_value)


if __name__ == "__main__":
    unittest.main()
