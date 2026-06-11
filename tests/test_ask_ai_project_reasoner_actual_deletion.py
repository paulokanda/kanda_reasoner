"""Validation for actual deletion of the top-level ask_ai_project_reasoner package."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASK_AI_DIR = PROJECT_ROOT / "ask_ai_project_reasoner"
DELETED_ENGINE_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


def run_fresh_python(code: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["kanda_reasoner_project_root"] = str(PROJECT_ROOT)
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PROJECT_ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class AskAiProjectReasonerActualDeletionTests(unittest.TestCase):
    """Verify the final retired top-level package is physically deleted."""

    def test_ask_ai_project_reasoner_folder_is_absent(self) -> None:
        self.assertFalse(ASK_AI_DIR.exists(), str(ASK_AI_DIR))

    def test_deleted_engine_package_folder_remains_absent(self) -> None:
        self.assertFalse(DELETED_ENGINE_DIR.exists(), str(DELETED_ENGINE_DIR))

    def test_ask_ai_project_reasoner_not_importable_in_fresh_interpreter(self) -> None:
        result = run_fresh_python(
            "import importlib.util; "
            "spec = importlib.util.find_spec('ask_ai_project_reasoner'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )

    def test_project_reasoner_v10_not_importable_in_fresh_interpreter(self) -> None:
        result = run_fresh_python(
            "import importlib.util; "
            "spec = importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )

    def test_canonical_runtime_imports_without_legacy_roots(self) -> None:
        import kanda_reasoner_app.reasoner_engine
        import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window
        import kanda_reasoner_app.reasoner_engine.query_router
        import kanda_reasoner_app.reasoner_engine.reasoner_retriever
        import reasoner_tools_gui

        self.assertTrue(kanda_reasoner_app.reasoner_engine)
        self.assertTrue(kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window)
        self.assertTrue(kanda_reasoner_app.reasoner_engine.query_router)
        self.assertTrue(kanda_reasoner_app.reasoner_engine.reasoner_retriever)
        self.assertTrue(reasoner_tools_gui)

    def test_fresh_interpreter_canonical_runtime_imports(self) -> None:
        result = run_fresh_python(
            "import kanda_reasoner_app.reasoner_engine; "
            "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
            "import kanda_reasoner_app.reasoner_engine.query_router; "
            "import kanda_reasoner_app.reasoner_engine.reasoner_retriever; "
            "import reasoner_tools_gui; "
            "print('canonical runtime imports ok after ask_ai_project_reasoner deletion')"
        )
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
