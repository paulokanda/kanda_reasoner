# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_formatting.py
"""Formatting for import rewrite apply readiness evidence."""
from __future__ import annotations

from .workbench_import_rewrite_apply_readiness import ImportRewriteApplyReadinessResult

__all__ = ["format_import_rewrite_apply_readiness"]


def format_import_rewrite_apply_readiness(result: ImportRewriteApplyReadinessResult) -> str:
    """Return a compact readable import rewrite readiness report."""
    lines = [
        "IMPORT REWRITE APPLY READINESS",
        f"Status: {result.status}",
        f"Importers: {result.importer_count}",
        f"No-op facade-owned records: {result.no_op_importer_count}",
        f"Manual-review records: {result.manual_review_count}",
        f"Rewrite enabled: {result.rewrite_enabled}",
        f"Apply enabled: {result.apply_enabled}",
        f"Exact token valid: {result.exact_token_valid}",
        f"Manifest: {result.readiness_manifest_path}",
        f"Diff preview: {result.diff_preview_path}",
        "",
        "Checked rules:",
    ]
    lines.extend(f"- {rule}" for rule in result.checked_rules)
    if result.blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend(f"- {blocker}" for blocker in result.blockers)
    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in result.warnings)
    return "\n".join(lines)
