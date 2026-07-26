# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/final_guarded_source_apply_planning_formatting.py
"""Formatting helpers for final guarded source-apply planning."""
from __future__ import annotations

from .final_guarded_source_apply_planning import FinalGuardedSourceApplyPlanResult

__all__ = ["format_final_guarded_source_apply_plan"]


def format_final_guarded_source_apply_plan(plan: FinalGuardedSourceApplyPlanResult) -> str:
    """Return a readable summary of the final guarded source-apply plan."""
    lines = [
        "FINAL GUARDED SOURCE-APPLY PLAN",
        "Status: " + plan.status,
        "Target: " + plan.target_file,
        "Preview root: " + plan.preview_root,
        "Apply enabled: " + str(plan.apply_enabled),
        "Rewrite enabled: " + str(plan.rewrite_enabled),
        "Source mutation enabled: " + str(plan.source_mutation_enabled),
        "Future-train evidence only: " + str(plan.planning_recorded_for_future_train_only),
    ]
    if plan.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in plan.blockers)
    if plan.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in plan.warnings)
    return "\n".join(lines)
