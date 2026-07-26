# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_structural_validation_formatting.py
"""Formatting helpers for Workbench structural preview validation."""
from __future__ import annotations

from .real_preview_structural_validator import RealPreviewStructuralValidationResult

__all__ = ["format_real_preview_structural_validation"]


def format_real_preview_structural_validation(result: RealPreviewStructuralValidationResult) -> str:
    """Return a readable structural validation summary for the Workbench."""
    lines = [
        "Large File Refactor Workbench - Structural Preview Validation",
        "",
        f"Status: {result.status}",
        f"Structural status: {result.structural_status}",
        f"Behavior status: {result.behavior_status}",
        f"Target: {result.target_file}",
        f"Preview root: {result.preview_root}",
        f"Source hash verified: {result.source_hash_verified}",
        f"Source mutation enabled: {result.source_mutation_enabled}",
        f"Import migration preview: {result.import_migration_preview_status}",
        "",
        "Checked files:",
    ]
    lines.extend([f"- {path}" for path in result.checked_files] or ["- None"])
    lines.extend(["", "Report files:"])
    lines.extend([f"- {path}" for path in result.report_files] or ["- None"])
    lines.extend(["", "Generated file results:"])
    for item in result.file_results:
        lines.append(
            f"- {item.path} | role={item.role} | lines={item.physical_lines} | "
            f"compile={item.compile_ok} | ast={item.ast_parse_ok}"
        )
        if item.symbols:
            lines.append("  symbols: " + ", ".join(item.symbols))
        for blocker in item.blockers:
            lines.append("  BLOCKER: " + blocker)
        for warning in item.warnings:
            lines.append("  WARNING: " + warning)
    lines.extend(["", "Blockers:"])
    lines.extend([f"- {item}" for item in result.blockers] or ["- None"])
    lines.extend(["", "Warnings:"])
    lines.extend([f"- {item}" for item in result.warnings] or ["- None"])
    lines.extend(
        [
            "",
            "Notes:",
            "- This is structural validation only.",
            "- It does not claim behavior equivalence unless project tests or runtime probes pass.",
            "- Import migration remains preview-only and is not applied.",
        ]
    )
    return "\n".join(lines)
