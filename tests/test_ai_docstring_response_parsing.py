from __future__ import annotations

import json
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


class StubDocstringGenerator(AIDocstringGenerator):
    def __init__(self, model_response: dict[str, object], *, include_private: bool = True) -> None:
        self.request_count = 0
        self.model_response = model_response
        config = AIConfig(
            cache_enabled=False,
            include_private=include_private,
            fallback_to_heuristic=False,
            require_ai_success=True,
            use_structured_outputs=True,
        )
        super().__init__(
            config=config,
            project_root=Path.cwd(),
            policy=DocstringPolicy.default(),
        )

    def _request_content(self, payload: dict[str, object]) -> str:
        self.request_count += 1
        return json.dumps(self.model_response)


class NoRequestDocstringGenerator(StubDocstringGenerator):
    def _request_content(self, payload: dict[str, object]) -> str:
        raise AssertionError("The public generate path should not call the model.")


class StructuredDocstringPublicContractTests(unittest.TestCase):
    def test_public_generator_renders_module_docstring(self) -> None:
        generator = StubDocstringGenerator(
            {"summary": "Coordinate sample module behavior"},
        )
        ctx = SymbolContext(
            kind="module",
            name="sample_module",
            module_id="pkg.sample_module",
        )

        result = generator.generate(ctx)

        self.assertEqual(result.body, "Coordinate sample module behavior.")
        self.assertEqual(result.source, "ai")
        self.assertEqual(generator.request_count, 1)

    def test_public_generator_renders_class_docstring(self) -> None:
        generator = StubDocstringGenerator(
            {
                "summary": "Manage sample state",
                "attributes": [
                    {"name": "state", "description": "Maps keys to sample values"},
                ],
            },
        )
        ctx = SymbolContext(
            kind="class",
            name="SampleManager",
            module_id="pkg.sample_module",
            class_attributes=[AttributeInfo("state", "dict[str, str]")],
        )

        result = generator.generate(ctx)

        self.assertIn("Manage sample state.", result.body)
        self.assertIn("Attributes", result.body)
        self.assertIn("state : dict[str, str]", result.body)
        self.assertIn("Maps keys to sample values.", result.body)
        self.assertEqual(result.source, "ai")

    def test_public_generator_renders_function_docstring(self) -> None:
        generator = StubDocstringGenerator(
            {
                "summary": "Build a sample mapping",
                "parameters": [
                    {"name": "name", "description": "Sample name to include"},
                ],
                "returns": {"description": "Mapping with normalized sample data"},
                "raises": [
                    {"type": "ValueError", "description": "If the name is empty"},
                ],
            },
        )
        ctx = SymbolContext(
            kind="function",
            name="build_sample",
            module_id="pkg.sample_module",
            parameters=[ParameterInfo("name", "str", False)],
            return_annotation="dict[str, str]",
            raises_types=["ValueError"],
        )

        result = generator.generate(ctx)

        self.assertIn("Build a sample mapping.", result.body)
        self.assertIn("Parameters", result.body)
        self.assertIn("name : str", result.body)
        self.assertIn("Sample name to include.", result.body)
        self.assertIn("Returns", result.body)
        self.assertIn("dict[str, str]", result.body)
        self.assertIn("Mapping with normalized sample data.", result.body)
        self.assertIn("Raises", result.body)
        self.assertIn("ValueError", result.body)
        self.assertIn("If the name is empty.", result.body)
        self.assertEqual(result.source, "ai")

    def test_public_generator_renders_method_docstring(self) -> None:
        generator = StubDocstringGenerator(
            {
                "summary": "Reset managed state",
                "parameters": [
                    {"name": "force", "description": "Whether to reset even when unchanged"},
                ],
                "returns": {"description": "Whether state changed"},
            },
        )
        ctx = SymbolContext(
            kind="method",
            name="reset_state",
            module_id="pkg.sample_module",
            enclosing_class="SampleManager",
            parameters=[ParameterInfo("force", "bool", True)],
            return_annotation="bool",
        )

        result = generator.generate(ctx)

        self.assertIn("Reset managed state.", result.body)
        self.assertIn("force : bool, optional", result.body)
        self.assertIn("Whether to reset even when unchanged.", result.body)
        self.assertIn("Whether state changed.", result.body)
        self.assertEqual(result.source, "ai")

    def test_public_generator_can_skip_private_without_ai_call(self) -> None:
        generator = NoRequestDocstringGenerator(
            {"summary": "This response should not be used"},
            include_private=False,
        )
        ctx = SymbolContext(
            kind="function",
            name="_private_helper",
            module_id="pkg.sample_module",
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "heuristic")
        self.assertTrue(result.used_fallback)
        self.assertIn("Private symbols", result.issues[0])
        self.assertEqual(generator.request_count, 0)


if __name__ == "__main__":
    unittest.main()
