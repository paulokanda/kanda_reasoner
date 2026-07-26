# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_multifile_recovery_evidence_formatting.py
"""Formatting helpers for multi-file recovery evidence."""
from __future__ import annotations

from .source_apply_multifile_recovery_evidence import SourceApplyMultiFileRecoveryEvidenceResult

__all__ = ["format_source_apply_multifile_recovery_evidence"]


def format_source_apply_multifile_recovery_evidence(result: SourceApplyMultiFileRecoveryEvidenceResult) -> str:
    """Return a compact review string for multi-file recovery evidence."""
    lines = [
        "SOURCE APPLY MULTI-FILE RECOVERY EVIDENCE",
        "Status: " + result.status,
        "Target: " + result.target_file,
        "Non-target files: " + str(len(result.non_target_written_files)),
        "Automated multi-file recovery enabled: " + str(result.automated_multifile_recovery_enabled),
        "Non-target removal enabled: " + str(result.non_target_removal_enabled),
        "Per-file backup evidence present: " + str(result.per_file_backup_evidence_present),
    ]
    if result.blockers:
        lines.append("Blockers: " + ", ".join(result.blockers))
    if result.warnings:
        lines.append("Warnings: " + ", ".join(result.warnings))
    return "\n".join(lines)
