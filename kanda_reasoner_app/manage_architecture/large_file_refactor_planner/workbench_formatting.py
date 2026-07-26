# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_formatting.py
"""Formatting helpers for the Large File Refactor Workbench."""
from __future__ import annotations

from .workbench_plan_intake import WorkbenchPlanIntakeResult

__all__ = ["format_workbench_intake"]


def format_workbench_intake(result: WorkbenchPlanIntakeResult) -> str:
    """Return a readable Workbench intake report."""
    lines = [
        "Large File Refactor Workbench - Plan Intake",
        "",
        f"Status: {result.status}",
        f"Active project root: {result.active_project_root}",
        f"Target file: {result.target_file or '<none>'}",
        f"Planner status: {result.planner_status}",
        f"Planner candidate verified: {_yes_no(result.planner_candidate_verified)}",
        f"Source hash fresh: {_yes_no(result.source_hash_fresh)}",
        f"Ready for real preview: {_yes_no(result.ready_for_real_preview)}",
        f"Source mutation enabled: {_yes_no(result.source_mutation_enabled)}",
        f"Real preview generation enabled: {_yes_no(result.real_preview_generation_enabled)}",
        "",
        "Stored source hash:",
        result.source_content_hash or "<missing>",
        "",
        "Current source hash:",
        result.current_source_content_hash or "<missing>",
        "",
        "Checked rules:",
    ]
    lines.extend(_bullet_lines(result.checked_rules))
    lines.append("")
    lines.append("Blockers:")
    lines.extend(_bullet_lines(result.blockers) or ["- none"])
    lines.append("")
    lines.append("Warnings:")
    lines.extend(_bullet_lines(result.warnings) or ["- none"])
    lines.append("")
    lines.append(
        "Next train: generate real LibCST preview files only after this "
        "intake is ready and a dedicated preview writer is implemented."
    )
    return "\n".join(lines)


def _yes_no(value: bool) -> str:
    """Return a stable yes/no token."""
    return "YES" if value else "NO"


def _bullet_lines(values: list[str]) -> list[str]:
    """Return bullet-formatted values."""
    return [f"- {value}" for value in values]
