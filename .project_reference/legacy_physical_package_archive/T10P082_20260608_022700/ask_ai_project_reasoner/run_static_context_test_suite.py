"""Support the run static context test suite module for Project Reasoner."""

from __future__ import annotations

import importlib
import inspect
import sys
import tempfile
import types
import unittest
from pathlib import Path


CURRENT_FILE = Path(__file__).resolve()
PACKAGE_PARENT = CURRENT_FILE.parent.parent

if __name__ == "__main__":
    if str(PACKAGE_PARENT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_PARENT))


TEST_MODULES = [
    "kanda_reasoner_app.reasoner_context_collector.tests.test_collector_packaging_metadata",
    "kanda_reasoner_app.reasoner_context_collector.tests.test_collector_documentation_intent",
    "kanda_reasoner_app.reasoner_context_collector.tests.test_collector_main_static_context_sections",
    "kanda_reasoner_app.reasoner_context_collector.tests.test_static_context_json_contract",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_retrieval_section_priorities",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_v10_index_loader_new_sections",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_v10_index_loader_reads_static_context_sections",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_v10_retriever_section_evidence",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_v10_prompt_builder_evidence_rules",
    "kanda_reasoner_app.project_reasoner_v10.tests.test_v10_static_context_end_to_end",
]


def _wrap_test_function(candidate):
    signature = inspect.signature(candidate)
    parameter_names = list(signature.parameters.keys())

    def _runner():
        if not parameter_names:
            return candidate()

        if parameter_names == ["tmp_path"]:
            with tempfile.TemporaryDirectory() as temp_dir:
                return candidate(Path(temp_dir))

        raise TypeError(
            "Unsupported test function signature for unittest runner: "
            f"{candidate.__name__}{signature}"
        )

    return _runner


def _load_module_function_tests(module: types.ModuleType) -> unittest.TestSuite:
    suite = unittest.TestSuite()

    for name in sorted(dir(module)):
        if not name.startswith("test_"):
            continue

        candidate = getattr(module, name)
        if not callable(candidate):
            continue

        suite.addTest(unittest.FunctionTestCase(_wrap_test_function(candidate)))

    return suite


def main() -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module_name in TEST_MODULES:
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))
        suite.addTests(_load_module_function_tests(module))

    if suite.countTestCases() == 0:
        print("ERROR: static context test suite loaded 0 tests.")
        return 1

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
