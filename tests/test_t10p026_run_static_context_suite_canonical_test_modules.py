"""Validate T10P026 static-context suite canonical test module names."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'ask_' 'ai_project_reasoner' / "run_static_context_test_suite.py"
LEGACY_TOKEN = "kanda_reasoner_app."
CANONICAL_TOKEN = "kanda_reasoner_app."


class RunStaticContextSuiteCanonicalModuleTests(unittest.TestCase):
    """Check the static-context suite runner uses canonical module names."""

    def test_runner_source_remains_ast_parseable(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        ast.parse(source)

    def test_test_modules_use_canonical_package(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        tree = ast.parse(source)
        test_modules = None

        for node in tree.body:
            if isinstance(node, ast.Assign):
                names = [target.id for target in node.targets if isinstance(target, ast.Name)]
                if "TEST_MODULES" in names:
                    test_modules = ast.literal_eval(node.value)
                    break

        self.assertIsInstance(test_modules, list)
        self.assertGreater(len(test_modules), 0)

        for module_name in test_modules:
            self.assertTrue(module_name.startswith(CANONICAL_TOKEN), module_name)
            self.assertNotIn(LEGACY_TOKEN, module_name)

    def test_runner_does_not_hardcode_legacy_test_module_prefix(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, source)
        self.assertIn(CANONICAL_TOKEN, source)


if __name__ == "__main__":
    unittest.main()
