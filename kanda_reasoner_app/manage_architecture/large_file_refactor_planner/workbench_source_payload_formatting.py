# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_source_payload_formatting.py
"""Formatting helpers for Workbench source-apply payload readiness."""
from __future__ import annotations

from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult

__all__ = ["format_source_apply_payload_readiness"]


def format_source_apply_payload_readiness(result: SourceApplyPayloadReadinessResult) -> str:
    """Return a compact operator-readable source payload summary."""
    lines = [
        "SOURCE APPLY PAYLOAD READINESS",
        f"status: {result.status}",
        f"target: {result.target_file}",
        f"preview_root: {result.preview_root}",
        f"payload_root: {result.payload_root}",
        f"payload_manifest: {result.payload_manifest_path}",
        f"structural_validation: {result.structural_validation_status}",
        f"behavior_status: {result.behavior_status}",
        f"preflight_backup: {result.preflight_backup_status}",
        f"source_hash_verified: {result.source_hash_verified}",
        f"source_mutation_enabled: {result.source_mutation_enabled}",
        f"apply_enabled: {result.apply_enabled}",
        f"import_rewrite_enabled: {result.import_rewrite_enabled}",
        f"payload_file_count: {len(result.files)}",
    ]
    if result.files:
        lines.append("payload_files:")
        for item in result.files:
            status = "ok" if not item.blockers else "blocked"
            lines.append(
                "  - " + item.relative_path + " -> " + item.destination_path + " [" + status + "]"
            )
    if result.blockers:
        lines.append("blockers:")
        lines.extend("  - " + item for item in result.blockers)
    if result.warnings:
        lines.append("warnings:")
        lines.extend("  - " + item for item in result.warnings)
    return "\n".join(lines)
