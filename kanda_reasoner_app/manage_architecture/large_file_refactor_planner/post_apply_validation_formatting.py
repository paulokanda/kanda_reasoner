# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/post_apply_validation_formatting.py
"""Formatting helpers for post-apply validation evidence."""
from __future__ import annotations

from .post_apply_validation import PostApplyValidationResult

__all__: list[str] = []


def format_post_apply_validation(result: PostApplyValidationResult) -> str:
    """Return a compact operator-readable post-apply validation summary."""
    lines = [
        "POST-APPLY VALIDATION",
        f"status: {result.status}",
        f"target: {result.target_file}",
        f"preview_root: {result.preview_root}",
        f"execution_manifest: {result.execution_manifest_path}",
        f"post_apply_manifest: {result.post_apply_manifest_path}",
        f"payload_zip: {result.payload_zip_path}",
        f"token_valid: {result.validation_confirmation_valid}",
        f"source_hash_transition_verified: {result.source_hash_transition_verified}",
        f"backup_snapshot_verified_unchanged: {result.backup_snapshot_verified_unchanged}",
        f"written_files_verified: {result.written_files_verified}",
        f"module_size_gate_passed: {result.module_size_gate_passed}",
        f"syntax_gate_passed: {result.syntax_gate_passed}",
    ]
    if result.written_files:
        lines.append("written_files:")
        lines.extend("  - " + item for item in result.written_files)
    if result.blockers:
        lines.append("blockers:")
        lines.extend("  - " + item for item in result.blockers)
    if result.warnings:
        lines.append("warnings:")
        lines.extend("  - " + item for item in result.warnings)
    return "\n".join(lines)
