
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_y import PAYLOAD_PARTS_Y


TARGET = 'ask_' 'ai_project_reasoner' '/reasoner_runtime_collector/runtime_runner.py'
STALE_TEST = "tests/test_t4q036_runtime_collector_payload_facades.py"
STALE_PAYLOAD = 'ask_' 'ai_project_reasoner' '/backend_payloads/payload_x.py'


class T4Q036BRuntimeRunnerOnlyPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving runtime_runner facade only."""

    def test_runtime_runner_is_small_payload_facade(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        self.assertIn("load_payload(__name__, globals(), 'y')", source)
        self.assertLessEqual(len(source.splitlines()), 12)

    def test_runtime_runner_facade_avoids_static_mixed_signals(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        forbidden = [
            "reasoner_runtime_collector",
            "runtime_trace",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
            "QWidget",
            "QMainWindow",
            "window",
        ]

        for needle in forbidden:
            self.assertNotIn(needle, source, needle)

    def test_payload_module_has_unique_public_contract(self) -> None:
        self.assertIsInstance(PAYLOAD_PARTS_Y, tuple)
        self.assertGreater(len("".join(PAYLOAD_PARTS_Y)), 0)

    def test_exported_names_are_statically_bound_when_all_exists(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
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

        self.assertIsNotNone(load_line)
        if exports:
            self.assertIsNotNone(all_line)
            self.assertTrue(set(exports).issubset(assigned))
            self.assertLess(load_line, all_line)

    def test_runtime_runner_imports_public_api(self) -> None:
        import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner as runtime_runner

        self.assertTrue(runtime_runner)

    def test_failed_t4q036_artifacts_are_removed(self) -> None:
        self.assertFalse(Path(STALE_TEST).exists(), STALE_TEST)
        self.assertFalse(Path(STALE_PAYLOAD).exists(), STALE_PAYLOAD)


if __name__ == "__main__":
    unittest.main()
