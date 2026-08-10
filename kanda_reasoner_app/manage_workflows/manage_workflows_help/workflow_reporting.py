# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_reporting.py
"""Own terminal result rendering and summary aggregation."""

from __future__ import annotations


from .workflow_models import (
    CheckResult,
)

__all__ = [
    "print_results",
    "summarize_results",
]

def print_results(results: list[CheckResult]) -> None:
    """Support print results behavior.
    
    Parameters
    ----------
    results : list[CheckResult]
        The results value.
    """
    
    if not results:
        print("No workflow results.")
        return

    for result in results:
        duration = f"{result.duration_seconds:.2f}s" if result.duration_seconds else "-"
        print(
            f"{result.status.upper():5} {result.category:15} {result.name:30} "
            f"{duration:>8} :: {result.message}"
        )
        if result.command:
            print(f"      command: {result.command}")
        cwd = str(result.details.get("cwd", "")).strip()
        if cwd:
            print(f"      cwd: {cwd}")
        stdout = str(result.details.get("stdout", "")).strip()
        stderr = str(result.details.get("stderr", "")).strip()
        if stdout:
            print("      stdout:")
            for line in stdout.splitlines():
                print(f"        {line}")
        if stderr:
            print("      stderr:")
            for line in stderr.splitlines():
                print(f"        {line}")

def summarize_results(results: list[CheckResult]) -> dict[str, int]:
    """Support summarize results behavior.
    
    Parameters
    ----------
    results : list[CheckResult]
        The results value.
    
    Returns
    -------
    dict[str, int]
        The mapped values.
    """
    
    summary = {"pass": 0, "fail": 0, "warn": 0, "skip": 0}
    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1
    return summary
