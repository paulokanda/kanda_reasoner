# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_dry_run_validator_formatting.py
"""Formatting helpers for source apply dry-run validation evidence."""
from __future__ import annotations

from .source_apply_dry_run_validator import SourceApplyDryRunValidationResult

__all__ = ["format_source_apply_dry_run_validation"]


def format_source_apply_dry_run_validation(result: SourceApplyDryRunValidationResult) -> str:
    """Return a compact operator-readable source apply dry-run validation summary."""
    lines = [
        "SOURCE APPLY DRY-RUN VALIDATION",
        f"status: {result.status}",
        f"target: {result.target_file}",
        f"preview_root: {result.preview_root}",
        f"dry_run_manifest: {result.dry_run_manifest_path}",
        f"token_valid: {result.dry_run_confirmation_valid}",
        f"source_hash_verified: {result.source_hash_verified}",
        f"planned_write_target_count: {result.planned_write_target_count}",
        f"rewrite_enabled: {result.rewrite_enabled}",
        f"apply_enabled: {result.apply_enabled}",
        f"source_mutation_enabled: {result.source_mutation_enabled}",
        f"dry_run_only: {result.dry_run_only}",
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
