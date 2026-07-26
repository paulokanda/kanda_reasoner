# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_formatting.py
"""Formatting helpers for import rewrite rollback evidence."""
from __future__ import annotations

from .workbench_import_rewrite_rollback_executor import ImportRewriteRollbackResult

__all__ = ["format_import_rewrite_rollback_result"]


def format_import_rewrite_rollback_result(result: ImportRewriteRollbackResult) -> str:
    """Return a readable import rewrite rollback summary."""
    lines = [
        "Import Rewrite Rollback Visibility",
        f"Status: {result.status}",
        f"Validation: {result.validation_status}",
        f"Exact token valid: {result.exact_token_valid}",
        f"Restored files: {len(result.restored_files)}",
        f"Retained files: {len(result.retained_files)}",
        f"Rollback execution: {result.rollback_execution_path}",
        f"Post-rollback validation: {result.post_rollback_validation_path}",
    ]
    if result.blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend(f"- {item}" for item in result.blockers)
    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in result.warnings)
    return "\n".join(lines)
