"""Regression tests for the reasoner_engine prompt_builder migration."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


class ReasonerEnginePromptBuilderCanonicalMigrationTests(unittest.TestCase):
    """Validate canonical prompt_builder availability during staged migration."""

    def test_canonical_prompt_builder_implementation_files_exist(self) -> None:
        expected_files = (
            CANONICAL_ENGINE / "prompt_builder.py",
            CANONICAL_ENGINE / "prompt_builder_help.json",
            CANONICAL_ENGINE / "prompt_builder_help" / "__init__.py",
            CANONICAL_ENGINE / "prompt_builder_help" / "answer_style.py",
            CANONICAL_ENGINE / "prompt_builder_help" / "callsite_evidence.py",
            CANONICAL_ENGINE / "prompt_builder_help" / "prompt_classification.py",
            CANONICAL_ENGINE / "prompt_builder_help" / "prompt_sections.py",
            CANONICAL_ENGINE / "prompt_builder_help" / "widget_registry_section.py",
        )

        for path in expected_files:
            self.assertTrue(path.is_file(), str(path))

    def test_legacy_prompt_builder_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_ENGINE / "prompt_builder.py").is_file())
        self.assertTrue((LEGACY_ENGINE / "prompt_builder_help").is_dir())

    def test_canonical_and_legacy_prompt_builder_imports_resolve(self) -> None:
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.prompt_builder"
        )

        self.assertTrue(hasattr(canonical, "PromptBuilder"))
        self.assertTrue(hasattr(legacy, "PromptBuilder"))
        self.assertTrue(hasattr(canonical, "PROJECT_SCOPE_GUARDRAIL"))
        self.assertTrue(hasattr(canonical, "is_which_method_calls_question"))

    def test_canonical_prompt_builder_helpers_import_through_public_contracts(self) -> None:
        answer_style = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.answer_style"
        )
        callsite_evidence = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.callsite_evidence"
        )
        prompt_classification = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.prompt_classification"
        )
        prompt_sections = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.prompt_sections"
        )
        widget_registry_section = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.widget_registry_section"
        )

        self.assertTrue(hasattr(answer_style, "build_answer_style_instructions"))
        self.assertTrue(hasattr(callsite_evidence, "append_callsite_evidence_section"))
        self.assertTrue(hasattr(callsite_evidence, "extract_exact_call_targets"))
        self.assertTrue(hasattr(callsite_evidence, "prioritize_callsite_snippets"))
        self.assertTrue(hasattr(prompt_classification, "is_which_method_calls_question"))
        self.assertTrue(hasattr(prompt_classification, "tokenize_query"))
        self.assertTrue(hasattr(prompt_sections, "append_project_summary"))
        self.assertTrue(hasattr(prompt_sections, "append_source_snippets_section"))
        self.assertTrue(hasattr(widget_registry_section, "append_widget_registry_section"))

    def test_canonical_prompt_builder_uses_reasoner_engine_manifest_paths(self) -> None:
        manifest_path = CANONICAL_ENGINE / "prompt_builder_help.json"
        source = manifest_path.read_text(encoding="utf-8-sig")

        self.assertIn("reasoner_engine", source)
        self.assertNotIn("project_reasoner_v10/prompt_builder", source)
        self.assertNotIn("project_reasoner_v10\\prompt_builder", source)

    def test_prompt_builder_classification_is_callable(self) -> None:
        prompt_classification = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.prompt_builder_help.prompt_classification"
        )
        self.assertIsInstance(
            prompt_classification.is_which_method_calls_question(
                "Which method calls build_main_window_ui?"
            ),
            bool,
        )


if __name__ == "__main__":
    unittest.main()
