# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_preflight_backup_contract_formatting.py
"""Formatting helpers for source apply preflight backup contract evidence."""
from __future__ import annotations

from .source_apply_preflight_backup_contract import SourceApplyPreflightBackupContractResult

__all__ = ["format_source_apply_preflight_backup_contract"]


def format_source_apply_preflight_backup_contract(result: SourceApplyPreflightBackupContractResult) -> str:
    """Return a compact operator-readable preflight backup summary."""
    lines = [
        "SOURCE APPLY PREFLIGHT BACKUP CONTRACT",
        f"status: {result.status}",
        f"target: {result.target_file}",
        f"preview_root: {result.preview_root}",
        f"dry_run_manifest: {result.dry_run_manifest_path}",
        f"preflight_manifest: {result.preflight_manifest_path}",
        f"backup_snapshot: {result.backup_snapshot_path}",
        f"token_valid: {result.preflight_confirmation_valid}",
        f"source_hash_verified: {result.source_hash_verified}",
        f"backup_snapshot_expected: {result.backup_snapshot_expected}",
        f"preview_artifacts_used_as_source_of_truth: {result.preview_artifacts_used_as_source_of_truth}",
        f"rewrite_enabled: {result.rewrite_enabled}",
        f"apply_enabled: {result.apply_enabled}",
        f"source_mutation_enabled: {result.source_mutation_enabled}",
    ]
    if result.blockers:
        lines.append("blockers:")
        lines.extend("  - " + item for item in result.blockers)
    if result.warnings:
        lines.append("warnings:")
        lines.extend("  - " + item for item in result.warnings)
    return "\n".join(lines)
