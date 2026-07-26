# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/guarded_source_apply_executor_formatting.py
"""Formatting helpers for guarded source apply executor evidence."""
from __future__ import annotations

from .guarded_source_apply_executor import GuardedSourceApplyExecutionResult

__all__ = ["format_guarded_source_apply_execution"]


def format_guarded_source_apply_execution(result: GuardedSourceApplyExecutionResult) -> str:
    """Return a compact operator-readable guarded source apply summary."""
    lines = [
        "GUARDED SOURCE APPLY EXECUTION",
        f"status: {result.status}",
        f"target: {result.target_file}",
        f"preview_root: {result.preview_root}",
        f"payload_zip: {result.payload_zip_path}",
        f"execution_manifest: {result.execution_manifest_path}",
        f"token_valid: {result.execution_confirmation_valid}",
        f"backup_snapshot_verified: {result.backup_snapshot_verified}",
        f"source_hash_verified_before_write: {result.source_hash_verified_before_write}",
        f"payload_manifest_verified: {result.payload_manifest_verified}",
        f"apply_enabled: {result.apply_enabled}",
        f"rewrite_enabled: {result.rewrite_enabled}",
        f"source_mutation_enabled: {result.source_mutation_enabled}",
        f"planned_write_target_count: {len(result.planned_write_targets)}",
        f"written_file_count: {result.written_file_count}",
    ]
    if result.planned_write_targets:
        lines.append("planned_write_targets:")
        lines.extend("  - " + item for item in result.planned_write_targets)
    if result.blockers:
        lines.append("blockers:")
        lines.extend("  - " + item for item in result.blockers)
    if result.warnings:
        lines.append("warnings:")
        lines.extend("  - " + item for item in result.warnings)
    return "\n".join(lines)
