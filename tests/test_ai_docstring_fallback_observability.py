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
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting import (
    build_report_row,
    result_failure_reason,
    result_generation_source,
    result_issues,
)


class StubDocstringGenerator(AIDocstringGenerator):
    def __init__(
        self,
        response_text: str,
        *,
        use_structured_outputs: bool = True,
        fallback_to_heuristic: bool = True,
        require_ai_success: bool = False,
        include_private: bool = True,
    ) -> None:
        self.request_count = 0
        self.response_text = response_text
        config = AIConfig(
            cache_enabled=False,
            include_private=include_private,
            fallback_to_heuristic=fallback_to_heuristic,
            require_ai_success=require_ai_success,
            use_structured_outputs=use_structured_outputs,
        )
        super().__init__(
            config=config,
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )

    def _request_content(self, payload: dict[str, object]) -> str:
        self.request_count += 1
        return self.response_text


class FallbackObservabilityTests(unittest.TestCase):
    def test_invalid_structured_json_is_visible_fallback(self) -> None:
        generator = StubDocstringGenerator("not json")
        ctx = SymbolContext(kind="function", name="build_sample", module_id="pkg.sample")

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertEqual(result.generation_source, "heuristic_fallback")
        self.assertEqual(result.failure_reason, "model_invalid_json")
        self.assertTrue(result.used_fallback)
        self.assertEqual(generator.stats.failure_reasons["model_invalid_json"], 1)
        self.assertEqual(generator.request_count, 2)

    def test_unsupported_structured_claim_is_rejected_before_insert(self) -> None:
        payload = {
            "summary": "Build a sample value",
            "parameters": [
                {"name": "invented", "description": "Unsupported parameter"},
            ],
        }
        generator = StubDocstringGenerator(json.dumps(payload))
        ctx = SymbolContext(
            kind="function",
            name="build_sample",
            module_id="pkg.sample",
            parameters=[ParameterInfo("name", "str", False)],
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertEqual(result.generation_source, "heuristic_fallback")
        self.assertEqual(result.failure_reason, "unsupported_ai_claim")
        self.assertIn("unsupported parameter: invented", result.failure_detail)
        self.assertTrue(result.used_fallback)

    def test_validation_rejection_is_visible_fallback(self) -> None:
        generator = StubDocstringGenerator(
            "def build_sample(): pass",
            use_structured_outputs=False,
        )
        ctx = SymbolContext(kind="function", name="build_sample", module_id="pkg.sample")

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertEqual(result.generation_source, "heuristic_fallback")
        self.assertEqual(result.failure_reason, "validation_rejected")
        self.assertIn("source code", result.failure_detail)
        self.assertEqual(generator.stats.failure_reasons["validation_rejected"], 1)

    def test_require_ai_success_keeps_rejected_ai_from_falling_back(self) -> None:
        generator = StubDocstringGenerator(
            "not json",
            fallback_to_heuristic=False,
            require_ai_success=True,
        )
        ctx = SymbolContext(kind="function", name="build_sample", module_id="pkg.sample")

        with self.assertRaises(RuntimeError):
            generator.generate(ctx)

        self.assertEqual(generator.stats.fallback, 0)

    def test_private_skip_has_canonical_failure_reason(self) -> None:
        generator = StubDocstringGenerator(
            json.dumps({"summary": "Unused"}),
            include_private=False,
        )
        ctx = SymbolContext(kind="function", name="_private_helper", module_id="pkg.sample")

        result = generator.generate(ctx)

        self.assertEqual(result.generation_source, "skipped_private")
        self.assertEqual(result.failure_reason, "private_symbol_skipped")
        self.assertEqual(generator.request_count, 0)

    def test_report_rows_can_surface_generation_source_and_failure_reason(self) -> None:
        generator = StubDocstringGenerator("not json")
        ctx = SymbolContext(kind="function", name="build_sample", module_id="pkg.sample")
        result = generator.generate(ctx)

        row = build_report_row(
            Path.cwd(),
            Path.cwd() / "sample.py",
            target_kind="function",
            target_name="build_sample",
            line=1,
            action="inserted",
            reason="missing docstring",
            source=result.source,
            confidence=result.confidence,
            generation_source=result_generation_source(result),
            failure_reason=result_failure_reason(result),
            issues=result_issues(result),
        )

        self.assertEqual(row["generation_source"], "heuristic_fallback")
        self.assertEqual(row["failure_reason"], "model_invalid_json")
        self.assertTrue(row["issues"])


if __name__ == "__main__":
    unittest.main()
