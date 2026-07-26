# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_rollback_recovery_formatting.py
"""Formatting helpers for source apply rollback/recovery evidence."""
from __future__ import annotations

from .source_apply_rollback_recovery import SourceApplyRollbackRecoveryResult

__all__ = ["format_source_apply_rollback_recovery"]


def format_source_apply_rollback_recovery(result: SourceApplyRollbackRecoveryResult) -> str:
    """Return a compact human-readable rollback/recovery summary."""
    lines = [
        "SOURCE APPLY ROLLBACK / RECOVERY",
        "Status: " + result.status,
        "Target: " + result.target_file,
        "Backup: " + result.backup_snapshot_path,
        "Rollback enabled: " + str(result.rollback_enabled),
        "Selected source restored: " + str(result.selected_source_restored),
        "Import rewrite rollback enabled: " + str(result.import_rewrite_rollback_enabled),
        "Blockers: " + (", ".join(result.blockers) if result.blockers else "none"),
        "Warnings: " + (", ".join(result.warnings) if result.warnings else "none"),
    ]
    return "\n".join(lines)
