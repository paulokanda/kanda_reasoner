"""Tests for T10P019 prompt template canonical package placeholders."""

from __future__ import annotations

from pathlib import Path
import unittest


class PromptTemplateCanonicalPathTests(unittest.TestCase):
    """Validate template prompt-library paths remain project agnostic."""

    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]
        self.template_dir = (
            self.root
            / 'ask_' 'ai_project_reasoner'
            / "templates"
            / "prompt_library_templates"
        )
        self.files = (
            self.template_dir / "PROMPT_TEMPLATE_BLUEPRINT.md",
            self.template_dir / "README.md",
        )
        self.legacy_token = "ask_ai" + "_project_reasoner"

    def test_templates_use_product_package_placeholder(self) -> None:
        expected = "<PROJECT_ROOT>\\<PRODUCT_PACKAGE>\\prompt_library\\"
        for path in self.files:
            text = path.read_text(encoding="utf-8")
            self.assertIn(expected, text, path.as_posix())

    def test_templates_do_not_hardcode_legacy_package_name(self) -> None:
        for path in self.files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(self.legacy_token, text, path.as_posix())

    def test_template_docs_keep_project_agnostic_placeholders(self) -> None:
        readme = (self.template_dir / "README.md").read_text(encoding="utf-8")
        self.assertIn("<PROJECT_ROOT>", readme)
        self.assertIn("<PROJECT_NAME>", readme)
        self.assertIn("<PRODUCT_PACKAGE>", readme)


if __name__ == "__main__":
    unittest.main()
