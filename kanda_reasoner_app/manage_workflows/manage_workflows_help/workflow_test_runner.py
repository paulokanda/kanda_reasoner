# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_test_runner.py
"""Execute selected-Project pytest and unittest through governed Python."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from .workflow_models import CheckResult
from .workflow_python_runtime import (
    project_python_has_module,
    resolve_project_python,
    run_project_python_probe,
)

__all__: list[str] = []


def _test_environment() -> dict[str, str]:
    """Return a bytecode-safe environment for Project test execution."""
    env = dict(os.environ)
    for key in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
        env.pop(key, None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    return env


def _display_command(python: Path, python_args: Sequence[str]) -> str:
    """Render test command evidence without invoking a shell."""
    return subprocess.list2cmdline(
        [str(python), *[str(part) for part in python_args]]
    )


def _result_from_completed(
    *,
    name: str,
    root: Path,
    python_args: Sequence[str],
    completed: subprocess.CompletedProcess[str],
    duration: float,
) -> CheckResult:
    """Map one governed Project-Python execution to Workflow Review evidence."""
    python = resolve_project_python(root)
    status = "pass" if completed.returncode == 0 else "fail"
    message = "Exit code " + str(completed.returncode) + "."
    return CheckResult(
        category="tests",
        name=name,
        status=status,
        message=message,
        duration_seconds=duration,
        command=_display_command(python, python_args),
        details={
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "returncode": completed.returncode,
            "cwd": str(root),
            "expect_output": False,
            "expected_output_stream": "either",
            "missing_output_contract": {},
            "missing_file_contract": {},
        },
    )


def _run_project_test_process(
    *,
    name: str,
    root: Path,
    python_args: Sequence[str],
    timeout: float,
    env: Mapping[str, str],
) -> CheckResult:
    """Run one Project test command through the frozen v2b Python owner."""
    start = time.perf_counter()
    try:
        completed = run_project_python_probe(
            root,
            python_args,
            cwd=root,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - start
        python = resolve_project_python(root)
        return CheckResult(
            category="tests",
            name=name,
            status="fail",
            message="Timed out after " + str(timeout) + " second(s).",
            duration_seconds=duration,
            command=_display_command(python, python_args),
            details={
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
            },
        )
    except Exception as exc:
        duration = time.perf_counter() - start
        python = resolve_project_python(root)
        return CheckResult(
            category="tests",
            name=name,
            status="fail",
            message="Command failed to start: " + str(exc),
            duration_seconds=duration,
            command=_display_command(python, python_args),
        )
    return _result_from_completed(
        name=name,
        root=root,
        python_args=python_args,
        completed=completed,
        duration=time.perf_counter() - start,
    )


def _run_project_tests(
    root: Path,
    discovered: dict[str, Any],
    cfg: dict[str, Any],
) -> list[CheckResult]:
    """Run configured pytest or unittest under selected-Project authority."""
    if not cfg.get("enabled", True):
        return [CheckResult("tests", "tests", "skip", "Workflow disabled.")]

    project_root = root.expanduser().resolve()
    timeout = float(cfg.get("timeout_seconds", 900))
    runner = str(cfg.get("runner", "auto")).lower()
    pytest_args = cfg.get("pytest_args") or ["-q"]
    if not isinstance(pytest_args, list):
        return [
            CheckResult(
                "tests",
                "tests",
                "fail",
                "pytest_args must be a list.",
            )
        ]

    should_try_pytest = runner in {"auto", "pytest"}
    has_pytest_signals = bool(
        discovered["pytest_files"] or discovered["test_dirs"]
    )
    env = _test_environment()

    if (
        should_try_pytest
        and project_python_has_module(project_root, "pytest")
        and has_pytest_signals
    ):
        result = _run_project_test_process(
            name="pytest",
            root=project_root,
            python_args=[
                "-m",
                "pytest",
                "-p",
                "no:cacheprovider",
                *[str(item) for item in pytest_args],
            ],
            timeout=timeout,
            env=env,
        )
        if result.status == "pass" or runner == "pytest":
            return [result]

    if runner in {"auto", "unittest"} and discovered["test_dirs"]:
        start_dir = str(
            cfg.get("unittest_start_dir") or discovered["test_dirs"][0]
        )
        return [
            _run_project_test_process(
                name="unittest",
                root=project_root,
                python_args=[
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    start_dir,
                ],
                timeout=timeout,
                env=env,
            )
        ]

    return [
        CheckResult(
            "tests",
            "tests",
            "warn",
            "No runnable test workflow discovered. Configure tests in "
            "workflow_manifest.json.",
        )
    ]
