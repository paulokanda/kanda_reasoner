"Direct architecture protection tests for canonical prompt_builder modules."

import unittest

from kanda_reasoner_app.reasoner_engine.prompt_builder import (
    PROJECT_SCOPE_GUARDRAIL,
    PromptBuilder,
    is_which_method_calls_question,
)
from kanda_reasoner_app.reasoner_engine.prompt_builder_help.answer_style import (
    build_answer_style_instructions,
)
from kanda_reasoner_app.reasoner_engine.prompt_builder_help.callsite_evidence import (
    append_callsite_evidence_section,
    extract_exact_call_targets,
    prioritize_callsite_snippets,
)
from kanda_reasoner_app.reasoner_engine.prompt_builder_help.prompt_classification import (
    is_chain_or_flow_question,
    is_code_localized_explanation_question,
    is_explain_implementation_question,
    is_which_method_calls_question as classify_which_method_calls_question,
    norm_text,
    tokenize_query,
)
from kanda_reasoner_app.reasoner_engine.prompt_builder_help.prompt_sections import (
    append_file_evidence_section,
    append_live_source_evidence_section,
    append_memory_section,
    append_project_summary,
    append_source_snippets_section,
    append_symbol_evidence_section,
    is_live_source_snippet,
)
from kanda_reasoner_app.reasoner_engine.prompt_builder_help.widget_registry_section import (
    append_widget_registry_section,
)


class ReasonerEnginePromptBuilderArchitectureProtectionTests(unittest.TestCase):
    """Protect canonical prompt_builder public contracts from orphan warnings."""

    def test_prompt_builder_public_contracts_are_directly_importable(self):
        self.assertIsInstance(PROJECT_SCOPE_GUARDRAIL, str)
        self.assertTrue(PROJECT_SCOPE_GUARDRAIL.strip())
        self.assertTrue(callable(PromptBuilder))
        self.assertTrue(callable(is_which_method_calls_question))

    def test_prompt_builder_helper_contracts_are_directly_importable(self):
        public_functions = (
            build_answer_style_instructions,
            append_callsite_evidence_section,
            extract_exact_call_targets,
            prioritize_callsite_snippets,
            is_chain_or_flow_question,
            is_code_localized_explanation_question,
            is_explain_implementation_question,
            classify_which_method_calls_question,
            norm_text,
            tokenize_query,
            append_file_evidence_section,
            append_live_source_evidence_section,
            append_memory_section,
            append_project_summary,
            append_source_snippets_section,
            append_symbol_evidence_section,
            is_live_source_snippet,
            append_widget_registry_section,
        )

        for function in public_functions:
            with self.subTest(function=function.__name__):
                self.assertTrue(callable(function))

    def test_prompt_classification_basic_helpers_are_callable(self):
        normalized = norm_text("  Which method calls build_ui?  ")
        tokens = tokenize_query("Which method calls build_ui?")

        self.assertIsInstance(normalized, str)
        self.assertIn("which", normalized)
        self.assertTrue(tokens)


if __name__ == "__main__":
    unittest.main()
