# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_behavior_formatting.py
"""Formatting helpers for optional Workbench behavior validation."""
from __future__ import annotations

from .workbench_behavior_validation import WorkbenchBehaviorValidationResult

__all__ = ["format_workbench_behavior_validation"]


def format_workbench_behavior_validation(result: WorkbenchBehaviorValidationResult) -> str:
    """Return human-readable behavior validation evidence."""
    lines = [
        "OPTIONAL BEHAVIOR / TEST VALIDATION",
        "Status: " + result.status,
        "Behavior status: " + result.behavior_status,
        "Behavior validation claimed: " + str(result.behavior_validation_claimed),
        "Command allowed: " + str(result.command_allowed),
        "Command exit code: " + str(result.command_exit_code),
        "Command timed out: " + str(result.command_timed_out),
        "Target: " + result.target_file,
        "Preview root: " + result.preview_root,
        "Report: " + result.report_path,
    ]
    if result.test_command:
        lines.append("Command: " + result.test_command)
    if result.blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    if result.stdout_excerpt:
        lines.append("")
        lines.append("STDOUT excerpt:")
        lines.append(result.stdout_excerpt)
    if result.stderr_excerpt:
        lines.append("")
        lines.append("STDERR excerpt:")
        lines.append(result.stderr_excerpt)
    return "\n".join(lines)
