"""Focused tests for workflow command output content contracts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner import (  # noqa: E501
    command_list_results,
)


class WorkflowOutputContentContractTests(unittest.TestCase):
    """Protect opt-in expected text and regex output contracts."""

    def test_expected_output_contains_passes_when_text_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "contains pass",
                            "args": [
                                sys.executable,
                                "-c",
                                "print('alpha beta gamma')",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_output_contains": "beta",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_expected_output_contains_fails_when_text_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "contains fail",
                            "args": [sys.executable, "-c", "print('alpha')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_output_contains": "missing text",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertIn("content contract", results[0].message)
        missing = results[0].details["missing_output_contract"]
        self.assertEqual(missing["expected_output_contains"], ["missing text"])

    def test_expected_stdout_regex_passes_when_pattern_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "regex pass",
                            "args": [
                                sys.executable,
                                "-c",
                                "print('files indexed: 410')",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_stdout_regex": r"files indexed: [0-9]+",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_expected_stderr_contains_fails_when_only_stdout_has_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "stderr contract fail",
                            "args": [sys.executable, "-c", "print('stdout only')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_stderr_contains": "stderr text",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        missing = results[0].details["missing_output_contract"]
        self.assertEqual(missing["expected_stderr_contains"], ["stderr text"])

    def test_default_forbidden_traceback_fails_even_with_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "hidden traceback",
                            "args": [
                                sys.executable,
                                "-c",
                                (
                                    "import sys; "
                                    "sys.stderr.write("
                                    "'Traceback (most recent call last):\\n'"
                                    ")"
                                ),
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertIn("forbidden content", results[0].message)
        details = results[0].details["missing_output_contract"]
        self.assertIn("forbidden_output_regex", details)

    def test_default_forbidden_error_regex_does_not_match_errors_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="business_checks",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "architecture summary",
                            "args": [
                                sys.executable,
                                "-c",
                                "print('Total issues: 32 | Errors: 0 | Warnings: 32')",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_custom_forbidden_stdout_regex_fails_when_pattern_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "custom forbidden regex",
                            "args": [
                                sys.executable,
                                "-c",
                                "print('soft failure marker: upload skipped')",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "forbidden_stdout_regex": r"upload skipped",
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        details = results[0].details["missing_output_contract"]
        self.assertEqual(details["forbidden_stdout_regex"], [r"upload skipped"])

    def test_default_forbidden_error_regex_can_be_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "allowed error text",
                            "args": [sys.executable, "-c", "print('ERROR allowed note')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "forbid_default_error_output": False,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
