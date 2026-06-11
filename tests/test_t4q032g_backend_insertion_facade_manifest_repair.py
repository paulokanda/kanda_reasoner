
from __future__ import annotations

import ast
from pathlib import Path
import unittest


TARGETS = [
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/ast_safety.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/insertion_collector.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/insertion_formatting.py"
    ),
]


class T4Q032GBackendInsertionFacadeManifestRepairTests(unittest.TestCase):
    """Validate static helper export visibility for insertion facades."""

    def test_insertion_facades_have_static_all_before_payload_load(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            all_line = None
            load_line = None
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            all_line = node.lineno
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if isinstance(func, ast.Name) and func.id == "load_payload":
                        load_line = node.lineno

            self.assertIsNotNone(all_line, rel_path)
            self.assertIsNotNone(load_line, rel_path)
            self.assertLess(all_line, load_line, rel_path)

    def test_insertion_facades_static_all_is_non_empty(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            module = ast.parse(source)

            found = False
            for node in module.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            self.assertIsInstance(node.value, (ast.List, ast.Tuple))
                            self.assertGreater(len(node.value.elts), 0, rel_path)
                            found = True

            self.assertTrue(found, rel_path)

    def test_insertion_facades_still_load_payload(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload(__name__, globals()", source)


if __name__ == "__main__":
    unittest.main()
