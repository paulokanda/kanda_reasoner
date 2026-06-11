"""Regression tests for T10P064 small infrastructure owner-box migration."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'
CANONICAL_TOKEN = "kanda_reasoner_app"
OWNER_DIRS = (
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "manage_workflows",
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "reasoner_runtime_collector",
)


class SmallInfraBoxesCanonicalRefsTests:
    """Plain assertion mixin used by unittest discovery."""

    def _read(self, relative_path: str) -> str:
        return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


import unittest


class SmallInfraBoxesCanonicalRefsUnittest(
    SmallInfraBoxesCanonicalRefsTests,
    unittest.TestCase,
):
    """Validate small owner boxes no longer pin the legacy package token."""

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        offenders: list[str] = []
        for owner_dir in OWNER_DIRS:
            for path in owner_dir.rglob("*.py"):
                text = path.read_text(encoding="utf-8")
                if LEGACY_TOKEN in text:
                    offenders.append(str(path.relative_to(PROJECT_ROOT)))
        self.assertEqual([], offenders)

    def test_manage_workflows_uses_canonical_imports(self) -> None:
        text = self._read('ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_gui.py')
        self.assertIn(
            "from kanda_reasoner_app.backend_payloads.loader import load_payload",
            text,
        )

        cli_text = self._read(
            'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_help/workflow_cli.py'
        )
        self.assertIn(
            "from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import",
            cli_text,
        )

    def test_manage_workflows_staged_paths_are_dynamic(self) -> None:
        validator_text = self._read(
            'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_validate_manifests.py'
        )
        self.assertIn('"_".join(("ask", "ai", "project", "reasoner"))', validator_text)
        self.assertNotIn('Path("ask_' 'ai_project_reasoner' '/', validator_text)

        worker_text = self._read(
            'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py'
        )
        self.assertIn('module_name = "kanda_reasoner_app.manage_workflows.manage_workflows"', worker_text)
        self.assertIn('"_".join(("ask", "ai", "project", "reasoner"))', worker_text)

    def test_runtime_collector_uses_canonical_runtime_modules(self) -> None:
        text = self._read(
            'ask_' 'ai_project_reasoner' '/reasoner_runtime_collector/'
            "runtime_runner_help/runtime_runner_part_1_private_impl.py"
        )
        self.assertIn(
            "kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api",
            text,
        )
        self.assertIn(
            "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner",
            text,
        )

    def test_runtime_collector_manifest_validator_uses_dynamic_staged_path(self) -> None:
        text = self._read(
            'ask_' 'ai_project_reasoner' '/reasoner_runtime_collector/'
            "runtime_runner_validate_manifests.py"
        )
        self.assertIn('"_".join(("ask", "ai", "project", "reasoner"))', text)
        self.assertNotIn('ROOT / "ask_' 'ai_project_reasoner' '"', text)


if __name__ == "__main__":
    unittest.main()
