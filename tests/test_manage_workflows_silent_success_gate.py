"""Focused tests for silent-success workflow command detection."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner import (  # noqa: E501
    command_list_results,
)


class WorkflowSilentSuccessGateTests(unittest.TestCase):
    """Protect opt-in detection for successful commands with empty output."""

    def test_silent_success_without_expect_output_still_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "silent command",
                            "args": [sys.executable, "-c", "pass"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_expect_output_fails_on_empty_stdout_and_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "silent expected output command",
                            "args": [sys.executable, "-c", "pass"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expect_output": True,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertIn("no informative", results[0].message)
        self.assertTrue(results[0].details["expect_output"])
        self.assertEqual(results[0].details["expected_output_stream"], "any")

    def test_expect_stdout_passes_when_stdout_has_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "stdout command",
                            "args": [
                                sys.executable,
                                "-c",
                                "print('workflow output ok')",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expect_output": True,
                            "expected_output_stream": "stdout",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")
        self.assertIn("workflow output ok", results[0].details["stdout"])

    def test_expect_both_fails_when_only_stdout_has_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "stdout only command",
                            "args": [sys.executable, "-c", "print('only stdout')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expect_output": True,
                            "expected_output_stream": "both",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
