# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_rollback_formatting.py
"""Formatting helpers for Large File Refactor Workbench rollback reports."""
from __future__ import annotations

from .workbench_rollback_executor import WorkbenchRollbackResult

__all__ = ["format_workbench_rollback"]


def format_workbench_rollback(result: WorkbenchRollbackResult | None) -> str:
    """Return a concise human-readable rollback report."""
    if result is None:
        return "No rollback has been executed."
    lines = [
        "Rollback Execution",
        "==================",
        f"Status: {result.status}",
        f"Target: {result.target_file}",
        f"Preview root: {result.preview_root}",
        f"Rollback manifest: {result.rollback_manifest_path}",
        f"Rollback report: {result.rollback_report_path}",
        f"Token present: {result.confirmation_token_present}",
        f"Token valid: {result.confirmation_token_valid}",
        f"Backup verified: {result.backup_snapshot_verified}",
        f"Selected source restored: {result.selected_source_restored}",
        f"Generated files removed: {result.generated_files_removed}",
        f"Source mutation enabled: {result.source_mutation_enabled}",
        f"Import rewrite enabled: {result.import_rewrite_enabled}",
        "",
        "Removed files:",
    ]
    lines.extend(["- " + item for item in result.removed_files] or ["- None"])
    lines.append("")
    lines.append("Retained files:")
    lines.extend(["- " + item for item in result.retained_files] or ["- None"])
    lines.append("")
    lines.append("Blockers:")
    lines.extend(["- " + item for item in result.blockers] or ["- None"])
    lines.append("")
    lines.append("Warnings:")
    lines.extend(["- " + item for item in result.warnings] or ["- None"])
    return "\n".join(lines)
