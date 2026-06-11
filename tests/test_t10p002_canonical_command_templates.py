"""Focused checks for canonical validation command templates."""

from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.reasoner_context_bundle.validation_state_builder import (
    DEFAULT_VALIDATION_COMMANDS,
)
from kanda_reasoner_app.stack_compatibility.stack_briefs import (
    build_stack_compatibility_brief,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ARCH = "kanda_reasoner_app\\manage_architecture\\manage_architecture.py"
CANONICAL_WORKFLOW = "kanda_reasoner_app\\manage_workflows\\manage_workflows.py"
LEGACY_ARCH = 'ask_' 'ai_project_reasoner' '\\manage_architecture\\manage_architecture.py'
LEGACY_WORKFLOW = 'ask_' 'ai_project_reasoner' '\\manage_workflows\\manage_workflows.py'


class CanonicalCommandTemplateTests(unittest.TestCase):
    """Validate canonical CLI paths in user-facing command templates."""

    def test_validation_state_defaults_use_canonical_cli_paths(self) -> None:
        commands = [str(item["command"]) for item in DEFAULT_VALIDATION_COMMANDS]
        joined = "\n".join(commands)

        self.assertIn(CANONICAL_ARCH, joined)
        self.assertIn(CANONICAL_WORKFLOW, joined)
        self.assertNotIn(LEGACY_ARCH, joined)
        self.assertNotIn(LEGACY_WORKFLOW, joined)

        argv_joined = "\n".join(
            " ".join(str(part) for part in item["argv"])
            for item in DEFAULT_VALIDATION_COMMANDS
        )
        self.assertIn("kanda_reasoner_app/manage_architecture/manage_architecture.py", argv_joined)
        self.assertIn("kanda_reasoner_app/manage_workflows/manage_workflows.py", argv_joined)

    def test_stack_brief_suggests_canonical_cli_paths(self) -> None:
        report = build_stack_compatibility_brief([], python_version="3.10.0")
        joined = "\n".join(report.tests_to_run)

        self.assertIn(CANONICAL_ARCH, joined)
        self.assertIn(CANONICAL_WORKFLOW, joined)
        self.assertIn("<PROJECT_ROOT>", joined)
        self.assertNotIn("E:\\developer_tools", joined)
        self.assertNotIn(LEGACY_ARCH, joined)
        self.assertNotIn(LEGACY_WORKFLOW, joined)

    def test_bundle_gated_prompt_uses_canonical_cli_examples(self) -> None:
        prompt_path = PROJECT_ROOT / (
            'ask_' 'ai_project_reasoner' '/prompt_library/active/'
            "KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW.md"
        )
        text = prompt_path.read_text(encoding="utf-8")

        self.assertIn(CANONICAL_ARCH, text)
        self.assertIn(CANONICAL_WORKFLOW, text)
        self.assertNotIn(LEGACY_ARCH, text)
        self.assertNotIn(LEGACY_WORKFLOW, text)

    def test_workflow_reference_message_prefers_canonical_cli(self) -> None:
        detector_path = PROJECT_ROOT / (
            'ask_' 'ai_project_reasoner' '/manage_workflows/manage_workflows_help/'
            "workflow_validation_reference_detectors.py"
        )
        text = detector_path.read_text(encoding="utf-8")

        self.assertIn("Use kanda_reasoner_app/manage_architecture/manage_architecture.py.", text)
        self.assertIn("Use workbench/bundle_manifest for source/runtime bundle manifests.", text)
        self.assertNotIn('Use ask_' 'ai_project_reasoner' '/manage_architecture/manage_architecture.py.', text)
        self.assertNotIn("workbench/_bundle_temp", text)


if __name__ == "__main__":
    unittest.main()
