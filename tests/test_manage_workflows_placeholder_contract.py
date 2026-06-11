"""Focused tests for workflow command placeholder contract validation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner import (  # noqa: E501
    execute_command,
)


class WorkflowPlaceholderContractTests(unittest.TestCase):
    """Protect Tab 2 workflow command placeholder misuse detection."""

    def test_unknown_placeholder_fails_before_command_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            marker = root / "should_not_exist.txt"
            spec = {
                "name": "unknown_placeholder",
                "command": (
                    "{python} -c \"from pathlib import Path; "
                    "Path(r'" + str(marker) + "').write_text('ran')\" "
                    "{missing_placeholder}"
                ),
            }

            result = execute_command(
                category="runtime_smoke",
                spec=spec,
                root=root,
                default_timeout=60,
            )

            self.assertEqual(result.status, "fail")
            self.assertEqual(
                result.message,
                "Command placeholder contract was not satisfied.",
            )
            self.assertIn("placeholder_contract", result.details)
            self.assertIn(
                "unsupported_placeholders",
                result.details["placeholder_contract"],
            )
            self.assertFalse(marker.exists())

    def test_allowed_root_and_python_placeholders_run_normally(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            spec = {
                "name": "allowed_placeholders",
                "args": [
                    "{python}",
                    "-c",
                    "print('placeholder contract ok')",
                ],
                "cwd": "{root}",
                "expect_output": True,
                "expected_stdout_contains": "placeholder contract ok",
                "allow_forbidden_output": True,
            }

            result = execute_command(
                category="runtime_smoke",
                spec=spec,
                root=root,
                default_timeout=60,
            )

            self.assertEqual(result.status, "pass")
            self.assertIn("placeholder contract ok", result.details["stdout"])

    def test_python_placeholder_is_rejected_in_expected_file_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            spec = {
                "name": "wrong_field_placeholder",
                "args": [
                    "{python}",
                    "-c",
                    "print('ok')",
                ],
                "expected_files": "{python}",
            }

            result = execute_command(
                category="runtime_smoke",
                spec=spec,
                root=root,
                default_timeout=60,
            )

            self.assertEqual(result.status, "fail")
            details = result.details["placeholder_contract"]
            self.assertIn("wrong_field_placeholders", details)
            self.assertEqual(
                details["wrong_field_placeholders"][0]["placeholder"],
                "python",
            )

    def test_malformed_placeholder_fragment_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            spec = {
                "name": "malformed_placeholder",
                "args": [
                    sys.executable,
                    "-c",
                    "print('ok')",
                    "{root",
                ],
            }

            result = execute_command(
                category="runtime_smoke",
                spec=spec,
                root=root,
                default_timeout=60,
            )

            self.assertEqual(result.status, "fail")
            details = result.details["placeholder_contract"]
            self.assertIn("malformed_placeholders", details)
            self.assertEqual(
                details["malformed_placeholders"][0]["fragment"],
                "{root",
            )

    def test_unknown_placeholder_in_extra_env_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            spec = {
                "name": "extra_env_placeholder",
                "args": [
                    "{python}",
                    "-c",
                    "print('ok')",
                ],
            }

            result = execute_command(
                category="gui_workflows",
                spec=spec,
                root=root,
                default_timeout=60,
                extra_env={"PYTHONPATH": "{root}", "BAD_PATH": "{project_root}"},
            )

            self.assertEqual(result.status, "fail")
            details = result.details["placeholder_contract"]
            self.assertIn("unsupported_placeholders", details)
            self.assertEqual(
                details["unsupported_placeholders"][0]["placeholder"],
                "project_root",
            )

    def test_literal_braces_in_inline_python_do_not_fail_placeholder_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            artifact = root / "artifact.json"
            spec = {
                "name": "literal_braces",
                "args": [
                    sys.executable,
                    "-c",
                    (
                        "from pathlib import Path; "
                        "Path('artifact.json').write_text('{bad json', "
                        "encoding='utf-8')"
                    ),
                ],
                "cwd": "{root}",
                "expected_json_files": ["artifact.json"],
            }

            result = execute_command(
                category="runtime_smoke",
                spec=spec,
                root=root,
                default_timeout=60,
            )

            self.assertEqual(result.status, "fail")
            self.assertNotIn("placeholder_contract", result.details)
            self.assertIn("missing_file_contract", result.details)
            self.assertTrue(artifact.exists())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
