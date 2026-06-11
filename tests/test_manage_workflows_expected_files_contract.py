"""Focused tests for workflow expected-file command contracts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner import (  # noqa: E501
    command_list_results,
)


class WorkflowExpectedFilesContractTests(unittest.TestCase):
    """Protect opt-in expected-file checks after command execution."""

    def test_expected_file_passes_when_file_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected file pass",
                            "args": [
                                sys.executable,
                                "-c",
                                (
                                    "from pathlib import Path; "
                                    "Path('artifact.txt').write_text('ok', encoding='utf-8')"
                                ),
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_files": ["artifact.txt"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")

    def test_expected_file_fails_when_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected file missing",
                            "args": [sys.executable, "-c", "print('no artifact')"],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_files": ["missing.txt"],
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertIn("file contract", results[0].message)
        missing = results[0].details["missing_file_contract"]
        self.assertEqual(missing["missing_expected_files"], ["missing.txt"])

    def test_expected_file_nonempty_fails_for_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected file nonempty",
                            "args": [
                                sys.executable,
                                "-c",
                                "from pathlib import Path; Path('empty.txt').touch()",
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_files": ["empty.txt"],
                            "expected_file_nonempty": True,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        missing = results[0].details["missing_file_contract"]
        self.assertEqual(missing["undersized_expected_files"][0]["path"], "empty.txt")

    def test_expected_file_min_bytes_passes_for_large_enough_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            results = command_list_results(
                category="runtime_smoke",
                cfg={
                    "enabled": True,
                    "commands": [
                        {
                            "name": "expected file min bytes",
                            "args": [
                                sys.executable,
                                "-c",
                                (
                                    "from pathlib import Path; "
                                    "Path('sized.txt').write_text('abcdef', encoding='utf-8')"
                                ),
                            ],
                            "cwd": "{root}",
                            "timeout_seconds": 30,
                            "expected_files": ["sized.txt"],
                            "expected_file_min_bytes": 6,
                        }
                    ],
                },
                root=Path(temp_dir),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "pass")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
