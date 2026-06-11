"""Final migration freeze audit.

This audit distinguishes physical legacy folders from in-process compatibility
aliases. Compatibility aliases may exist after canonical modules are imported,
but physical legacy folders must remain absent.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KANDA_APP = PROJECT_ROOT / "kanda_reasoner_app"

DELETED_DIRS = (
    PROJECT_ROOT / "ask_ai_project_reasoner",
    KANDA_APP / "project_reasoner_v10",
    KANDA_APP / "project_reasoner_v10_data_collector",
    KANDA_APP / "project_reasoner_v10_runtime_collector",
)

CANONICAL_DIRS = (
    KANDA_APP / "reasoner_engine",
    KANDA_APP / "reasoner_context_collector",
    KANDA_APP / "reasoner_runtime_collector",
)

DELETED_IMPORTS = (
    "ask_ai_project_reasoner",
    "kanda_reasoner_app.project_reasoner_v10",
    "kanda_reasoner_app.project_reasoner_v10_data_collector",
    "kanda_reasoner_app.project_reasoner_v10_runtime_collector",
)


class ReasonerFinalMigrationFreezeAuditTests(unittest.TestCase):
    """Verify the final canonical migration state."""

    def test_canonical_directories_exist(self) -> None:
        for directory in CANONICAL_DIRS:
            with self.subTest(directory=str(directory)):
                self.assertTrue(directory.is_dir())

    def test_deleted_legacy_directories_are_absent(self) -> None:
        for directory in DELETED_DIRS:
            with self.subTest(directory=str(directory)):
                self.assertFalse(directory.exists())

    def test_deleted_imports_are_absent_in_fresh_interpreter(self) -> None:
        for module_name in DELETED_IMPORTS:
            code = (
                "import importlib.util; "
                f"spec = importlib.util.find_spec({module_name!r}); "
                "raise SystemExit(0 if spec is None else 1)"
            )
            result = subprocess.run(
                [sys.executable, "-c", code],
                cwd=str(PROJECT_ROOT),
                text=True,
                capture_output=True,
                check=False,
            )
            with self.subTest(module_name=module_name):
                self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_canonical_imports_work_in_fresh_interpreter(self) -> None:
        code = (
            "import kanda_reasoner_app.reasoner_engine; "
            "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
            "import kanda_reasoner_app.reasoner_context_collector.runner; "
            "import kanda_reasoner_app.reasoner_runtime_collector.runner; "
            "import kanda_reasoner_app.manage_architecture.manage_architecture_gui; "
            "import kanda_reasoner_app.reasoner_tools_shell.runner; "
            "import reasoner_tools_gui; "
            "print('final canonical imports ok')"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_final_state_aliases_do_not_recreate_physical_legacy_roots(self) -> None:
        importlib.import_module("kanda_reasoner_app.manage_architecture.manage_architecture_gui")
        importlib.import_module("kanda_reasoner_app.reasoner_tools_shell.runner")
        importlib.import_module("kanda_reasoner_app.reasoner_context_collector.runner")
        importlib.import_module("kanda_reasoner_app.reasoner_runtime_collector.runner")

        for directory in DELETED_DIRS:
            with self.subTest(directory=str(directory)):
                self.assertFalse(directory.exists())

    def test_gui_specs_prefer_canonical_main_window(self) -> None:
        spec_file = KANDA_APP / "reasoner_tools_gui_shell" / "tool_specs.py"
        text = spec_file.read_text(encoding="utf-8", errors="replace")
        self.assertIn("kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window", text)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window", text)


if __name__ == "__main__":
    unittest.main()
