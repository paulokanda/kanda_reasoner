"""Closure audit tests for Tab 3 docstring generation.

These tests verify the frozen end-to-end contracts without requiring private
helper functions to remain public exports.
"""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path: str) -> str:
    """Read a project file as text for closure-contract assertions."""
    path = PROJECT_ROOT / relative_path
    return path.read_text(encoding="utf-8", errors="replace")


class Tab3ClosureAuditTests(unittest.TestCase):
    """Audit the frozen Tab 3 docstring-generation quality chain."""

    def test_prompt_packaging_keeps_evidence_and_guardrails(self) -> None:
        """Prompt packaging must expose evidence and anti-hallucination rules."""
        source = read_project_file(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "ai_docstring_generator_help/docstring_payloads.py"
        )
        normalized = source.lower()

        required_phrases = [
            "evidence ledger",
            "hallucination guardrails",
            "allowed parameter",
            "allowed class attribute",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in normalized]
        self.assertEqual([], missing)

        raise_markers = [
            "allowed raise types",
            "allowed explicit raise types",
            "explicit raise types",
            "raises_types",
        ]
        self.assertTrue(
            any(marker in normalized for marker in raise_markers),
            "Prompt packaging must continue to expose raise-type evidence.",
        )

    def test_context_inference_contract_remains_tested(self) -> None:
        """Parameter, return, and raise inference must remain behavior-tested."""
        context_test = read_project_file("tests/test_ai_docstring_context_inference.py")
        context_source = read_project_file(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/context_builder.py'
        )
        helper_path = PROJECT_ROOT / (
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "context_builder_help/inference_private_impl.py"
        )
        helper_source = ""
        if helper_path.exists():
            helper_source = helper_path.read_text(encoding="utf-8", errors="replace")

        required_tests = [
            "test_default_literals_are_evidence_backed_parameter_types",
            "test_generator_return_is_marked_as_iterator_object_when_unannotated",
            "test_nested_function_raises_do_not_leak_to_parent_context",
        ]
        missing_tests = [name for name in required_tests if name not in context_test]
        self.assertEqual([], missing_tests)

        combined_source = (context_source + "\n" + helper_source).lower()
        required_markers = ["return_annotation", "raises_types", "default"]
        missing_markers = [
            marker for marker in required_markers if marker not in combined_source
        ]
        self.assertEqual([], missing_markers)

    def test_generation_quality_chain_is_visible_and_blocking(self) -> None:
        """Generated docstrings must keep visible quality rejection behavior."""
        generator_source = read_project_file(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "ai_docstring_generator.py"
        )
        quality_test = read_project_file("tests/test_ai_docstring_quality_gate.py")
        combined = generator_source + "\n" + quality_test

        required_markers = [
            "quality_rejected",
            "Docstring quality gate rejected AI output",
            "test_low_information_summary_is_not_inserted_when_ai_success_required",
            "test_missing_parameter_description_is_quality_rejected_to_fallback",
        ]
        missing = [marker for marker in required_markers if marker not in combined]
        self.assertEqual([], missing)

    def test_fallback_quality_avoids_todo_placeholder_contract(self) -> None:
        """Heuristic fallback must keep the no-TODO regression tests active."""
        fallback_test = read_project_file("tests/test_ai_docstring_fallback_quality.py")
        required_tests = [
            "test_ai_call_failure_fallback_has_no_todo_placeholders",
            "test_class_attribute_fallback_uses_evidence_without_todo",
            "test_module_fallback_from_summary_block_stays_unchanged",
        ]
        missing = [name for name in required_tests if name not in fallback_test]
        self.assertEqual([], missing)

    def test_review_visibility_is_available_for_gui_review(self) -> None:
        """Report and GUI review layers must expose review-oriented fields."""
        reporting_source = read_project_file(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_help/reporting.py"
        )
        review_panel_source = read_project_file(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/report_review_panel.py"
        )
        review_test = read_project_file("tests/test_ai_docstring_gui_review_integration.py")
        combined = reporting_source + "\n" + review_panel_source + "\n" + review_test

        required_markers = [
            "review_status",
            "review_action_hint",
            "review_severity",
            "Ready for review",
            "Fallback review",
            "Blocked/rejected",
        ]
        missing = [marker for marker in required_markers if marker not in combined]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
