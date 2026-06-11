from __future__ import annotations

import ast
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder import (
    build_function_context,
)


class AstInferenceContextTests(unittest.TestCase):
    def _first_function_context(self, source: str):
        tree = ast.parse(source)
        source_lines = source.splitlines()
        node = next(
            item for item in tree.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        return build_function_context(
            node=node,
            tree=tree,
            module_id="sample.module",
            source_lines=source_lines,
            module_summary=None,
        )

    def test_default_literals_are_evidence_backed_parameter_types(self) -> None:
        ctx = self._first_function_context(
            "def configure(limit=3, enabled=True, label='x', items=None):\n"
            "    return None\n"
        )
        annotations = {param.name: param.annotation for param in ctx.parameters}

        self.assertEqual(annotations["limit"], "int")
        self.assertEqual(annotations["enabled"], "bool")
        self.assertEqual(annotations["label"], "str")
        self.assertEqual(annotations["items"], "None")
        self.assertEqual(ctx.return_annotation, "None")

    def test_nested_function_raises_do_not_leak_to_parent_context(self) -> None:
        ctx = self._first_function_context(
            "def outer(flag):\n"
            "    def inner():\n"
            "        raise InnerError('nested')\n"
            "    if flag:\n"
            "        raise ValueError('visible')\n"
            "    return None\n"
        )

        self.assertEqual(ctx.raises_types, ["ValueError"])

    def test_generator_return_is_marked_as_iterator_object_when_unannotated(self) -> None:
        ctx = self._first_function_context(
            "def stream(items):\n"
            "    for item in items:\n"
            "        yield item\n"
        )

        self.assertEqual(ctx.return_annotation, "Iterator[object]")


if __name__ == "__main__":
    unittest.main()
