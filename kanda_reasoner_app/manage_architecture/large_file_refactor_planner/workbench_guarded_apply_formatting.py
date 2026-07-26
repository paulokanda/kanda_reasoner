# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_guarded_apply_formatting.py
"""Formatting helpers for Workbench exact-token guarded source apply."""
from __future__ import annotations

from .workbench_guarded_source_apply import GuardedSourceApplyResult
from .workbench_post_apply_validator import WorkbenchPostApplyValidationResult

__all__ = ["format_guarded_source_apply", "format_post_apply_validation"]


def format_guarded_source_apply(result: GuardedSourceApplyResult) -> str:
    """Return a readable guarded source apply summary."""
    lines = [
        "Guarded Source Apply",
        "Status: " + result.status,
        "Target: " + result.target_file,
        "Expected token: " + result.expected_confirmation_token,
        "Token valid: " + str(result.confirmation_token_valid),
        "Source mutation enabled: " + str(result.source_mutation_enabled),
        "Import rewrite enabled: " + str(result.import_rewrite_enabled),
        "Written files: " + str(len(result.written_files)),
    ]
    if result.written_files:
        lines.append("Written file paths:")
        lines.extend("- " + path for path in result.written_files)
    if result.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)


def format_post_apply_validation(result: WorkbenchPostApplyValidationResult) -> str:
    """Return a readable post-apply validation summary."""
    lines = [
        "Post-Apply Validation",
        "Status: " + result.status,
        "Structural status: " + result.structural_status,
        "Behavior status: " + result.behavior_status,
        "Checked files: " + str(len(result.checked_files)),
        "Rollback manifest: " + result.rollback_manifest_path,
    ]
    if result.checked_files:
        lines.append("Checked file paths:")
        lines.extend("- " + path for path in result.checked_files)
    if result.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)
