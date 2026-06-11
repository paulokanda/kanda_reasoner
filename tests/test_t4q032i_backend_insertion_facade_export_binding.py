
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


class T4Q032IBackendInsertionFacadeExportBindingTests(unittest.TestCase):
    """Validate static export bindings for insertion facades."""

    def test_facades_load_payload_before_static_export_binding(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            load_line = None
            all_line = None
            assignment_lines = []
            for node in tree.body:
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if isinstance(func, ast.Name) and func.id == "load_payload":
                        load_line = node.lineno
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            all_line = node.lineno
                        elif isinstance(target, ast.Name):
                            assignment_lines.append(node.lineno)

            self.assertIsNotNone(load_line, rel_path)
            self.assertIsNotNone(all_line, rel_path)
            self.assertTrue(assignment_lines, rel_path)
            self.assertLess(load_line, min(assignment_lines), rel_path)
            self.assertLess(max(assignment_lines), all_line, rel_path)

    def test_facades_remain_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload(__name__, globals()", source)
            self.assertLessEqual(len(source.splitlines()), 12, rel_path)

    def test_exported_names_are_statically_bound(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            assigned = set()
            exports = []
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for item in node.value.elts:
                                    if isinstance(item, ast.Constant):
                                        exports.append(str(item.value))
                        elif isinstance(target, ast.Name):
                            assigned.add(target.id)

            self.assertTrue(exports, rel_path)
            self.assertTrue(set(exports).issubset(assigned), rel_path)


if __name__ == "__main__":
    unittest.main()
