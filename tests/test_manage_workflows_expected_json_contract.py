"""Focused tests for workflow expected JSON file contracts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner import (  # noqa: E501
    command_list_results,
)


class WorkflowExpectedJsonContractTests(unittest.TestCase):
    """Protect opt-in expected JSON file checks after command execution."""

    def test_expected_json_file_passes_when_required_keys_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected json pass",
                            "args": [
                                sys.executable,
                                "-c",
                                (
                                    "from pathlib import Path; "
                                    "Path('artifact.json').write_text("
                                    "'{\"status\": \"ok\", \"count\": 1}', "
                                    "encoding='utf-8')"
                                ),
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_json_files": ["artifact.json"],
                            "expected_json_required_keys": ["status", "count"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_expected_json_file_fails_when_json_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected json invalid",
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
                            "timeout_seconds": 30,
                            "expected_json_files": ["artifact.json"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        details = results[0].details["missing_file_contract"]
        self.assertEqual(
            details["invalid_expected_json_files"][0]["path"],
            "artifact.json",
        )

    def test_expected_json_file_fails_when_required_key_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected json missing key",
                            "args": [
                                sys.executable,
                                "-c",
                                (
                                    "from pathlib import Path; "
                                    "Path('artifact.json').write_text("
                                    "'{\"status\": \"ok\"}', encoding='utf-8')"
                                ),
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_json_files": ["artifact.json"],
                            "expected_json_required_keys": ["status", "count"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        details = results[0].details["missing_file_contract"]
        self.assertEqual(
            details["missing_expected_json_keys"][0]["missing_keys"],
            ["count"],
        )

    def test_expected_json_file_fails_when_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected json missing file",
                            "args": [sys.executable, "-c", "print('no artifact')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_json_files": ["missing.json"],
                            "expected_json_required_keys": ["status"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        details = results[0].details["missing_file_contract"]
        self.assertEqual(details["missing_expected_files"], ["missing.json"])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
