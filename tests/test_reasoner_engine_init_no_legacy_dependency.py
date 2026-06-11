"""Tests for the canonical reasoner_engine package initializer."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


class ReasonerEngineInitNoLegacyDependencyTests(unittest.TestCase):
    def test_reasoner_engine_init_source_has_no_retired_package_import(self):
        path = Path("kanda_reasoner_app/reasoner_engine/__init__.py")
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("project_reasoner_v10", text)
        self.assertNotIn("_legacy", text)

    def test_reasoner_engine_init_imports_without_retired_package(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                "import kanda_reasoner_app.reasoner_engine; print('ok')",
            ],
            cwd=str(Path.cwd()),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_lazy_symbol_exports_resolve(self):
        module = importlib.import_module("kanda_reasoner_app.reasoner_engine")
        self.assertIn("JsonProjectReasonerV10", module.__all__)
        self.assertTrue(hasattr(module, "JsonProjectReasonerV10"))
        self.assertTrue(hasattr(module, "main"))

    def test_lazy_module_exports_resolve(self):
        module = importlib.import_module("kanda_reasoner_app.reasoner_engine")
        self.assertIn("query_router", module.__all__)
        exported_module = module.query_router
        self.assertEqual(
            exported_module.__name__,
            "kanda_reasoner_app.reasoner_engine.query_router",
        )


if __name__ == "__main__":
    unittest.main()
