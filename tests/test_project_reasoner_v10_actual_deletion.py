"""Focused tests for project_reasoner_v10 actual deletion."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DELETED_PACKAGE_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


def run_fresh_python(code: str) -> subprocess.CompletedProcess[str]:
    """Run code in a fresh interpreter with the project root on PYTHONPATH."""
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    if existing_pythonpath:
        env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + existing_pythonpath
    else:
        env["PYTHONPATH"] = str(PROJECT_ROOT)

    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PROJECT_ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class ProjectReasonerV10ActualDeletionTests(unittest.TestCase):
    """Validate that the retired engine package is physically deleted."""

    def test_retired_package_folder_is_absent(self) -> None:
        self.assertFalse(DELETED_PACKAGE_DIR.exists(), str(DELETED_PACKAGE_DIR))

    def test_retired_package_is_not_importable_in_fresh_interpreter(self) -> None:
        code = (
            "import importlib.util; "
            "spec = importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        result = run_fresh_python(code)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_canonical_runtime_imports_without_retired_package(self) -> None:
        import kanda_reasoner_app.reasoner_engine as reasoner_engine
        import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window as main_window
        import kanda_reasoner_app.reasoner_engine.query_router as query_router
        import kanda_reasoner_app.reasoner_engine.reasoner_retriever as retriever

        self.assertIsNotNone(reasoner_engine)
        self.assertIsNotNone(main_window)
        self.assertIsNotNone(query_router)
        self.assertIsNotNone(retriever)

    def test_fresh_interpreter_canonical_runtime_imports(self) -> None:
        code = (
            "import kanda_reasoner_app.reasoner_engine; "
            "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
            "import kanda_reasoner_app.reasoner_engine.query_router; "
            "import kanda_reasoner_app.reasoner_engine.reasoner_retriever; "
            "import reasoner_tools_gui; "
            "print('canonical runtime imports ok after project_reasoner_v10 deletion')"
        )
        result = run_fresh_python(code)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("canonical runtime imports ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
