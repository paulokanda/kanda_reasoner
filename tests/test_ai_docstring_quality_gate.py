"""Tests for post-generation docstring quality gating."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.ai_config import AIConfig
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator import (
    AIDocstringGenerator,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder import (
    ParameterInfo,
    SymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.docstring_policy import (
    DocstringPolicy,
)


class QualityGateStubGenerator(AIDocstringGenerator):
    def __init__(
        self,
        response: dict[str, object],
        *,
        fallback_to_heuristic: bool = True,
        require_ai_success: bool = False,
    ) -> None:
        self.request_count = 0
        self.response = response
        config = AIConfig(
            cache_enabled=False,
            include_private=True,
            fallback_to_heuristic=fallback_to_heuristic,
            require_ai_success=require_ai_success,
            use_structured_outputs=True,
        )
        super().__init__(
            config=config,
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )

    def _request_content(self, payload: dict[str, object]) -> str:
        self.request_count += 1
        return json.dumps(self.response)


class PostGenerationQualityGateTests(unittest.TestCase):
    def test_missing_parameter_description_is_quality_rejected_to_fallback(self) -> None:
        generator = QualityGateStubGenerator(
            {
                "summary": "Build a sample mapping",
                "parameters": [
                    {"name": "name", "description": ""},
                ],
                "returns": {"description": "Mapping with normalized data"},
            }
        )
        ctx = SymbolContext(
            kind="function",
            name="build_sample",
            module_id="pkg.sample",
            parameters=[ParameterInfo("name", "str", False)],
            return_annotation="dict[str, str]",
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertEqual(result.generation_source, "heuristic_fallback")
        self.assertEqual(result.failure_reason, "quality_rejected")
        self.assertIn("contains TODO placeholder", result.failure_detail)
        self.assertEqual(generator.stats.failure_reasons["quality_rejected"], 1)

    def test_low_information_summary_is_not_inserted_when_ai_success_required(self) -> None:
        generator = QualityGateStubGenerator(
            {
                "summary": "TODO",
                "parameters": [],
                "returns": {"description": ""},
            },
            fallback_to_heuristic=False,
            require_ai_success=True,
        )
        ctx = SymbolContext(
            kind="function",
            name="build_sample",
            module_id="pkg.sample",
        )

        with self.assertRaises(ValueError) as raised:
            generator.generate(ctx)

        self.assertIn("quality gate rejected", str(raised.exception).lower())
        self.assertEqual(generator.stats.fallback, 0)

    def test_high_information_structured_output_still_passes(self) -> None:
        generator = QualityGateStubGenerator(
            {
                "summary": "Build a sample mapping",
                "parameters": [
                    {"name": "name", "description": "Sample name to include"},
                ],
                "returns": {"description": "Mapping with normalized sample data"},
            },
            fallback_to_heuristic=False,
            require_ai_success=True,
        )
        ctx = SymbolContext(
            kind="function",
            name="build_sample",
            module_id="pkg.sample",
            parameters=[ParameterInfo("name", "str", False)],
            return_annotation="dict[str, str]",
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "ai")
        self.assertEqual(result.failure_reason, "none")
        self.assertIn("Build a sample mapping.", result.body)
        self.assertIn("Sample name to include.", result.body)


if __name__ == "__main__":
    unittest.main()
