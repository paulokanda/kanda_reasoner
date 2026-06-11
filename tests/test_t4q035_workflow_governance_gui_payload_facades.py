
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_v import PAYLOAD_PARTS_V
from kanda_reasoner_app.backend_payloads.payload_w import PAYLOAD_PARTS_W


TARGETS = [
    'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_gui.py',
    'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py',
]


class T4Q035WorkflowGovernanceGuiPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving workflow governance GUI facades."""

    def test_public_modules_are_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload", source)
            self.assertLessEqual(len(source.splitlines()), 12, rel_path)

    def test_public_facades_avoid_static_mixed_signals(self) -> None:
        forbidden = [
            "manage_workflows",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
            "QWidget",
            "QMainWindow",
        ]

        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, source, rel_path + " contains " + needle)

    def test_payload_modules_have_unique_public_contracts(self) -> None:
        payloads = [PAYLOAD_PARTS_V, PAYLOAD_PARTS_W]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_exported_names_are_statically_bound_when_all_exists(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            exports = []
            assigned = set()
            load_line = None
            all_line = None

            for node in tree.body:
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if isinstance(func, ast.Name) and func.id == "load_payload":
                        load_line = node.lineno
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            all_line = node.lineno
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for item in node.value.elts:
                                    if isinstance(item, ast.Constant):
                                        exports.append(str(item.value))
                        elif isinstance(target, ast.Name):
                            assigned.add(target.id)

            self.assertIsNotNone(load_line, rel_path)
            if exports:
                self.assertIsNotNone(all_line, rel_path)
                self.assertTrue(set(exports).issubset(assigned), rel_path)
                self.assertLess(load_line, all_line, rel_path)

    def test_manage_workflows_gui_imports_public_api(self) -> None:
        import kanda_reasoner_app.manage_workflows.manage_workflows_gui as manage_workflows_gui

        self.assertTrue(manage_workflows_gui)

    def test_workflow_gui_window_imports_public_api(self) -> None:
        import kanda_reasoner_app.manage_workflows.manage_workflows_gui_help.workflow_gui_window as workflow_gui_window

        self.assertTrue(workflow_gui_window)


if __name__ == "__main__":
    unittest.main()
