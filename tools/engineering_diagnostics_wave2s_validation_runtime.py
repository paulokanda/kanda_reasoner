# project-path: tools/engineering_diagnostics_wave2s_validation_runtime.py
"""Focused runtime validation helpers for Engineering Diagnostics Wave 2S."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

__all__ = ["run_wave2s_command", "run_wave2s_focused_tests"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run_wave2s_command(
    command: list[str],
    *,
    cwd: Path,
    markers: tuple[str, ...] = (),
    timeout_seconds: float = 900.0,
) -> str:
    """Run one bounded command from an explicit Tool-root environment."""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(cwd)
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
        check=False,
    )
    output = completed.stdout + completed.stderr
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    _require(
        completed.returncode == 0,
        "VALIDATION_COMMAND_FAILED:" + " ".join(command),
    )
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def run_wave2s_focused_tests(root: Path) -> None:
    """Run all frozen Engineering Diagnostics tests through Wave 2S."""
    modules = (
        "tests.test_reasoner_symbol_atlas_active_owner_filtering_wave2n",
        "tests.test_engineering_diagnostics_wave2oa",
        "tests.test_engineering_diagnostics_wave2ob",
        "tests.test_engineering_diagnostics_wave2oc",
        "tests.test_engineering_diagnostics_wave2od",
        "tests.test_engineering_diagnostics_wave2pa",
        "tests.test_engineering_diagnostics_wave2pb",
        "tests.test_engineering_diagnostics_wave2qa",
        "tests.test_engineering_diagnostics_wave2qa_gui_scale",
        "tests.test_engineering_diagnostics_wave2qb",
        "tests.test_engineering_diagnostics_wave2qb_gui_scale",
        "tests.test_engineering_diagnostics_wave2r",
        "tests.test_engineering_diagnostics_wave2r_gui_scale",
        "tests.test_engineering_diagnostics_wave2s",
        "tests.test_engineering_diagnostics_wave2s_gui_scale",
    )
    output = run_wave2s_command(
        [sys.executable, "-m", "unittest", "-v", *modules],
        cwd=root,
        markers=("Ran 143 tests", "OK"),
    )
    _require("FAILED" not in output, "WAVE2S_FOCUSED_TEST_FAILURE")
    print("FOCUSED PUBLIC CONTRACT TESTS: 143/143 PASS")
