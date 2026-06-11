"""Focused checks for canonical CLI paths in workflow_manifest.json."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_MANIFEST = PROJECT_ROOT / "workflow_manifest.json"
CANONICAL_ARCH = "kanda_reasoner_app/manage_architecture/manage_architecture.py"
CANONICAL_WORKFLOW = "kanda_reasoner_app/manage_workflows/manage_workflows.py"
LEGACY_ARCH = 'ask_' 'ai_project_reasoner' '/manage_architecture/manage_architecture.py'
LEGACY_WORKFLOW = 'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows.py'


class WorkflowManifestCanonicalCliTests(unittest.TestCase):
    """Validate workflow_manifest uses canonical validation commands."""

    def _manifest(self) -> dict:
        return json.loads(WORKFLOW_MANIFEST.read_text(encoding="utf-8"))

    def _command_text(self) -> str:
        manifest = self._manifest()
        command_texts = []
        workflows = manifest.get("workflows", {})
        for section in ("runtime_smoke", "business_checks"):
            for command in workflows.get(section, {}).get("commands", []):
                args = command.get("args", [])
                command_texts.append(" ".join(str(part) for part in args))
        return "\n".join(command_texts)

    def test_runtime_and_business_commands_prefer_canonical_cli(self) -> None:
        text = self._command_text()

        self.assertIn(CANONICAL_ARCH, text)
        self.assertIn(CANONICAL_WORKFLOW, text)
        self.assertNotIn(LEGACY_ARCH, text)
        self.assertNotIn(LEGACY_WORKFLOW, text)

    def test_workflow_manifest_project_root_is_current_root(self) -> None:
        manifest = self._manifest()
        self.assertEqual(manifest.get("project_root"), r"E:\kanda_reasoner")


if __name__ == "__main__":
    unittest.main()
