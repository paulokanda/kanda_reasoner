from __future__ import annotations

import ast
import tempfile
import textwrap
import unittest
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector import (
    collect_missing_docstring_insertions,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting import (
    apply_insertions_to_text,
)


class InsertionCollectorScopeTests(unittest.TestCase):
    """Regression tests for decorated functions with local wrapper functions."""

    def test_nested_local_wrapper_is_not_collected_for_docstring_insertion(self) -> None:
        source = textwrap.dedent(
            """
            from functools import wraps


            def audit_call(func):
                @wraps(func)
                def wrapper(*args: object, **kwargs: object) -> object:
                    return func(*args, **kwargs)

                return wrapper


            @audit_call
            def decorated_business_rule(amount: float, *, currency: str = "USD") -> str:
                if amount < 0:
                    raise ValueError("amount must not be negative")
                return f"{currency}:{amount:.2f}"


            class PropertyContainer:
                default_unit = "items"

                def __init__(self, count: int = 0) -> None:
                    self._count = count

                @property
                def count(self) -> int:
                    return self._count
            """
        ).lstrip()

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            path = root / "decorated_case.py"
            path.write_text(source, encoding="utf-8")

            insertions, skipped, current, had_bom, rows = collect_missing_docstring_insertions(
                root,
                path,
                include_module=True,
                include_classes=True,
                include_functions=True,
                include_init=True,
                manifest=None,
                generator=None,
            )

            self.assertFalse(skipped)
            self.assertFalse(had_bom)

            inserted = {
                (str(row.get("target_kind")), str(row.get("target_name")))
                for row in rows
                if row.get("action") == "inserted"
            }

            self.assertIn(("module", "decorated_case"), inserted)
            self.assertIn(("function", "audit_call"), inserted)
            self.assertIn(("function", "decorated_business_rule"), inserted)
            self.assertIn(("class", "PropertyContainer"), inserted)
            self.assertIn(("method", "PropertyContainer.__init__"), inserted)
            self.assertIn(("method", "PropertyContainer.count"), inserted)
            self.assertNotIn(("function", "wrapper"), inserted)

            desired = apply_insertions_to_text(current, insertions)
            parsed = ast.parse(desired, filename=str(path))

            nodes = {
                node.name: node
                for node in ast.walk(parsed)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }

            self.assertIsNotNone(ast.get_docstring(parsed))
            self.assertIsNotNone(ast.get_docstring(nodes["audit_call"]))
            self.assertIsNotNone(ast.get_docstring(nodes["decorated_business_rule"]))
            self.assertIsNotNone(ast.get_docstring(nodes["PropertyContainer"]))

            wrappers = [
                node
                for node in ast.walk(parsed)
                if isinstance(node, ast.FunctionDef) and node.name == "wrapper"
            ]
            self.assertEqual(1, len(wrappers))
            self.assertIsNone(ast.get_docstring(wrappers[0]))


if __name__ == "__main__":
    unittest.main()
