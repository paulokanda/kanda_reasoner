# project-path: tools/engineering_diagnostics_wave2w_v1r2_validation_runtime.py
"""Bounded validation runner for Wave 2W v1r2 runtime collector correction."""

from __future__ import annotations

from pathlib import Path
import sys

from tools.engineering_diagnostics_wave2w_validation_runtime import run_wave2w_command

__all__ = ["run_wave2w_v1r2_focused_tests"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run_wave2w_v1r2_focused_tests(root: Path) -> None:
    """Run the complete frozen Diagnostics campaign plus v1r2 regressions."""
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
        "tests.test_engineering_diagnostics_wave2w_runtime_corrections",
    )
    output = run_wave2w_command(
        [sys.executable, "-m", "unittest", "-v", *modules],
        cwd=root,
        markers=("Ran 200 tests", "OK"),
    )
    _require("FAILED" not in output, "WAVE2W_V1R2_FOCUSED_TEST_FAILURE")
    print("FOCUSED PUBLIC CONTRACT TESTS: 200/200 PASS")
    print("BOM PUBLIC CLI EXECUTION CONTRACT: PASS")
    print("RUFF LARGE OUTPUT PIPE DRAIN CONTRACT: PASS")
    print("RUFF TIMEOUT FAIL-CLOSED CONTRACT: PASS")
    print("SHADOW RUNTIME STATEMENT IDENTITY CONTRACT: PASS")
