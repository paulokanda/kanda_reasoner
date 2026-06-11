"Final legacy deletion GUI importlib alias repair tests."""

from __future__ import annotations

import importlib
import importlib.util
import pathlib
import subprocess
import sys
import unittest


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
ASK_AI_ROOT = PROJECT_ROOT / "ask_ai_project_reasoner"
PROJECT_V10_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


def run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class FinalLegacyDeletionGuiImportlibAliasRepairTests(unittest.TestCase):
    def test_deleted_legacy_folders_remain_absent(self) -> None:
        self.assertFalse(ASK_AI_ROOT.exists())
        self.assertFalse(PROJECT_V10_ROOT.exists())

    def test_deleted_roots_are_not_importable_in_fresh_interpreter(self) -> None:
        code = (
            "import importlib.util; "
            "raise SystemExit(0 if importlib.util.find_spec('ask_ai_project_reasoner') is None else 1)"
        )
        result = run_python(code)
        self.assertEqual(0, result.returncode, result.stderr)

        code = (
            "import importlib.util; "
            "raise SystemExit(0 if importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10') is None else 1)"
        )
        result = run_python(code)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_gui_runtime_modules_import_without_physical_legacy_roots(self) -> None:
        code = (
            "import kanda_reasoner_app.manage_architecture.manage_architecture_gui; "
            "import kanda_reasoner_app.reasoner_tools_shell.runner; "
            "import reasoner_tools_gui; "
            "print('gui runtime imports ok')"
        )
        result = run_python(code)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("gui runtime imports ok", result.stdout)

    def test_canonical_runtime_imports_without_legacy_roots(self) -> None:
        code = (
            "import kanda_reasoner_app.reasoner_engine; "
            "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
            "import kanda_reasoner_app.reasoner_engine.query_router; "
            "import kanda_reasoner_app.reasoner_engine.reasoner_retriever; "
            "print('canonical runtime imports ok')"
        )
        result = run_python(code)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("canonical runtime imports ok", result.stdout)

    def test_manage_architecture_gui_source_has_importlib_alias_bootstrap(self) -> None:
        source_path = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture_gui.py"
        text = source_path.read_text(encoding="utf-8", errors="replace")
        self.assertIn("_install_deleted_legacy_root_importlib_aliases", text)
        self.assertIn("_install_deleted_legacy_root_importlib_aliases()", text)

    def test_shell_runner_source_has_payload_alias_bootstrap(self) -> None:
        source_path = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner.py"
        text = source_path.read_text(encoding="utf-8", errors="replace")
        self.assertIn("_install_deleted_legacy_root_importlib_aliases", text)
        self.assertIn("_install_deleted_legacy_root_importlib_aliases()", text)


if __name__ == "__main__":
    unittest.main()
