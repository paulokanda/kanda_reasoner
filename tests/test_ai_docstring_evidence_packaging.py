from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.ai_config import AIConfig
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator import AIDocstringGenerator
from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder import (
    AttributeInfo,
    ParameterInfo,
    SymbolContext,
)


class PromptCaptureGenerator(AIDocstringGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payloads = []

    def _request_content(self, payload):
        self.payloads.append(payload)
        user_prompt = payload["messages"][1]["content"]
        if "KIND: class" in user_prompt:
            return json.dumps(
                {
                    "summary": "Represent a cache record.",
                    "extended_description": "Stores cache metadata described by the class source evidence.",
                    "parameters": [],
                    "returns": {"description": "Class construction details are defined by the class body."},
                    "raises": [],
                    "attributes": [
                        {
                            "name": "path",
                            "description": "Path stored by the cache record.",
                        }
                    ],
                    "notes": [],
                }
            )
        return json.dumps(
            {
                "summary": "Return the validated value.",
                "extended_description": "Uses the provided value after the source-level negative-value guard.",
                "parameters": [
                    {
                        "name": "value",
                        "description": "Integer value to validate and return.",
                    }
                ],
                "returns": {"description": "The validated integer value."},
                "raises": [
                    {
                        "type": "ValueError",
                        "description": "Raised when the value is negative.",
                    }
                ],
                "attributes": [],
                "notes": [],
            }
        )


class EvidenceContextPackagingTests(unittest.TestCase):
    def _generator(self) -> PromptCaptureGenerator:
        cfg = AIConfig.default()
        cfg.cache_enabled = False
        cfg.use_structured_outputs = True
        cfg.fallback_to_heuristic = False
        cfg.require_ai_success = True
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        return PromptCaptureGenerator(config=cfg, project_root=Path(tmpdir.name))

    def test_public_generator_prompt_contains_evidence_ledger(self) -> None:
        generator = self._generator()
        ctx = SymbolContext(
            kind="function",
            name="return_value",
            module_id="example.module",
            source_lines=[
                "def return_value(value: int) -> int:",
                "    if value < 0:",
                "        raise ValueError('negative')",
                "    return value",
            ],
            signature="def return_value(value: int) -> int",
            parameters=[ParameterInfo(name="value", annotation="int", has_default=False)],
            return_annotation="int",
            raises_types=["ValueError"],
            decorators=["staticmethod"],
            lineno=10,
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "ai")
        self.assertTrue(generator.payloads)
        user_prompt = generator.payloads[0]["messages"][1]["content"]
        self.assertIn("EVIDENCE LEDGER:", user_prompt)
        self.assertIn("Allowed parameter names: value", user_prompt)
        self.assertIn("Allowed explicit raise types: ValueError", user_prompt)
        self.assertIn("SOURCE EVIDENCE:", user_prompt)
        self.assertIn("10: def return_value(value: int) -> int:", user_prompt)
        self.assertIn("HALLUCINATION GUARDRAILS:", user_prompt)

    def test_public_generator_prompt_contains_class_attributes(self) -> None:
        generator = self._generator()
        ctx = SymbolContext(
            kind="class",
            name="CacheRecord",
            module_id="example.module",
            source_lines=["class CacheRecord:", "    path: str"],
            class_attributes=[AttributeInfo(name="path", type_hint="str")],
            lineno=20,
        )

        result = generator.generate(ctx)

        self.assertEqual(result.source, "ai")
        user_prompt = generator.payloads[0]["messages"][1]["content"]
        self.assertIn("Allowed class attribute names: path", user_prompt)
        self.assertIn("CLASS ATTRIBUTES:", user_prompt)
        self.assertIn("20: class CacheRecord:", user_prompt)


if __name__ == "__main__":
    unittest.main()
