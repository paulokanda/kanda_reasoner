"""Final legacy root deletion audit.

This test module replaces the transitional deletion-readiness audit after the
final deletion of ask_ai_project_reasoner. Both legacy roots are now expected
to be physically absent and not importable in a fresh interpreter.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOP_LEVEL_LEGACY_ROOT = "ask_ai_project_reasoner"
DELETED_ENGINE_PACKAGE = "kanda_reasoner_app.project_reasoner_v10"
DELETED_ENGINE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"
CANONICAL_ENGINE_PACKAGE = "kanda_reasoner_app.reasoner_engine"
CANONICAL_MAIN_WINDOW = "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"

RUNTIME_SOURCE_FILES = (
    PROJECT_ROOT / "reasoner_tools_gui.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "tool_specs.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "gui_support.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "run_real_project_static_context_smoke.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "run_static_context_test_suite.py",
)


class AskAiProjectReasonerDeletionReadinessAuditTests(unittest.TestCase):
    """Final audit for removed legacy roots and canonical runtime imports."""

    def _run_fresh(self, code: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_both_legacy_root_folders_are_absent(self) -> None:
        self.assertFalse((PROJECT_ROOT / TOP_LEVEL_LEGACY_ROOT).exists())
        self.assertFalse(DELETED_ENGINE_PATH.exists())

    def test_top_level_legacy_root_is_not_importable_in_fresh_interpreter(self) -> None:
        result = self._run_fresh(
            "import importlib.util; "
            "spec = importlib.util.find_spec('ask_ai_project_reasoner'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_deleted_engine_package_is_not_importable_in_fresh_interpreter(self) -> None:
        result = self._run_fresh(
            "import importlib.util; "
            "spec = importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_canonical_runtime_imports_in_fresh_interpreter(self) -> None:
        result = self._run_fresh(
            "import kanda_reasoner_app.reasoner_engine; "
            "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
            "import kanda_reasoner_app.reasoner_engine.query_router; "
            "import kanda_reasoner_app.reasoner_engine.reasoner_retriever; "
            "import reasoner_tools_gui; "
            "print('canonical runtime imports ok after final deletion')"
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_runtime_sources_do_not_directly_import_deleted_roots(self) -> None:
        offenders: list[str] = []
        forbidden_tokens = (
            "import ask_ai_project_reasoner",
            "from ask_ai_project_reasoner",
            "ask_ai_project_reasoner.project_reasoner_v10",
            "kanda_reasoner_app.project_reasoner_v10",
            "kanda_reasoner_app/project_reasoner_v10",
            "kanda_reasoner_app\\project_reasoner_v10",
        )

        for path in RUNTIME_SOURCE_FILES:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(token in text for token in forbidden_tokens):
                offenders.append(str(path.relative_to(PROJECT_ROOT)))

        self.assertEqual([], sorted(set(offenders)))

    def test_canonical_main_window_imports_in_current_process(self) -> None:
        module = importlib.import_module(CANONICAL_MAIN_WINDOW)
        self.assertTrue(hasattr(module, "JsonProjectReasonerV10"))


if __name__ == "__main__":
    unittest.main()
