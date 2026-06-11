"""Tests for evidence-bound heuristic fallback quality."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.ai_config import AIConfig
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator import (
    AIDocstringGenerator,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder import (
    AttributeInfo,
    ParameterInfo,
    SymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.docstring_policy import (
    DocstringPolicy,
)


class FailingRequestGenerator(AIDocstringGenerator):
    def __init__(self) -> None:
        super().__init__(
            config=AIConfig(
                cache_enabled=False,
                include_private=True,
                fallback_to_heuristic=True,
                require_ai_success=False,
                use_structured_outputs=True,
            ),
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )

    def _request_content(self, payload: dict[str, object]) -> str:
        raise OSError("local AI unavailable")


class HeuristicFallbackQualityTests(unittest.TestCase):
    def test_ai_call_failure_fallback_has_no_todo_placeholders(self) -> None:
        generator = FailingRequestGenerator()
        ctx = SymbolContext(
            kind="function",
            name="build_user_record",
            module_id="pkg.sample",
            parameters=[
                ParameterInfo("user_name", "str", False),
                ParameterInfo("limit", "int", True),
            ],
            return_annotation="dict[str, str]",
            raises_types=["ValueError"],
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertEqual(result.generation_source, "heuristic_fallback")
        self.assertEqual(result.failure_reason, "ai_call_failed")
        self.assertNotIn("TODO", result.body)
        self.assertIn("Build user record.", result.body)
        self.assertIn("Value for user name.", result.body)
        self.assertIn("Optional value for limit.", result.body)
        self.assertIn("Return value produced by build user record.", result.body)
        self.assertIn("Raised by build user record", result.body)

    def test_class_attribute_fallback_uses_evidence_without_todo(self) -> None:
        generator = AIDocstringGenerator(
            config=AIConfig(
                cache_enabled=False,
                include_private=False,
                fallback_to_heuristic=True,
                use_structured_outputs=True,
            ),
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )
        ctx = SymbolContext(
            kind="class",
            name="_RuntimeConfig",
            module_id="pkg.sample",
            class_attributes=[
                AttributeInfo("timeout_seconds", "float", "timeout seconds"),
            ],
        )

        result = generator.generate(ctx)

        self.assertEqual(result.generation_source, "skipped_private")
        self.assertNotIn("TODO", result.body)
        self.assertIn("timeout_seconds : float", result.body)
        self.assertIn("Attribute related to timeout seconds.", result.body)

    def test_module_fallback_from_summary_block_stays_unchanged(self) -> None:
        generator = AIDocstringGenerator(
            config=AIConfig(
                cache_enabled=False,
                include_private=False,
                fallback_to_heuristic=True,
                use_structured_outputs=True,
            ),
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )
        ctx = SymbolContext(
            kind="module",
            name="sample_module",
            module_id="pkg.sample_module",
            module_summary_block="Module purpose: Build sample context objects.\nOther text",
        )

        result = generator.generate(ctx)

        self.assertEqual(result.body, "Build sample context objects.")
        self.assertNotIn("TODO", result.body)


if __name__ == "__main__":
    unittest.main()
