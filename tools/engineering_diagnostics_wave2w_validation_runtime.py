# project-path: tools/engineering_diagnostics_wave2w_validation_runtime.py
"""Bounded runtime validation for Engineering Safety hierarchy Wave 2W."""

from __future__ import annotations

from pathlib import Path
import sys

from tools.engineering_diagnostics_wave2v_validation_runtime import run_wave2v_command

__all__ = ["run_wave2w_command", "run_wave2w_focused_tests"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run_wave2w_command(
    command: list[str],
    *,
    cwd: Path,
    markers: tuple[str, ...] = (),
    timeout_seconds: float = 900.0,
) -> str:
    """Reuse the frozen command runner with Wave 2W naming."""
    return run_wave2v_command(
        command,
        cwd=cwd,
        markers=markers,
        timeout_seconds=timeout_seconds,
    )


def run_wave2w_focused_tests(root: Path) -> None:
    """Run every Diagnostics contract through the two-level hierarchy."""
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
        "tests.test_engineering_diagnostics_wave2t",
        "tests.test_engineering_diagnostics_wave2t_gui_scale",
        "tests.test_engineering_diagnostics_wave2u",
        "tests.test_engineering_diagnostics_wave2u_gui_scale",
        "tests.test_engineering_diagnostics_wave2v",
        "tests.test_engineering_diagnostics_wave2v_gui_scale",
        "tests.test_engineering_diagnostics_wave2w",
        "tests.test_engineering_diagnostics_wave2w_gui_scale",
    )
    output = run_wave2w_command(
        [sys.executable, "-m", "unittest", "-v", *modules],
        cwd=root,
        markers=("Ran 194 tests", "OK"),
    )
    _require("FAILED" not in output, "WAVE2W_FOCUSED_TEST_FAILURE")
    print("FOCUSED PUBLIC CONTRACT TESTS: 194/194 PASS")
