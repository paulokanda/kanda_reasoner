# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/import_rewrite_application_gate_formatting.py
"""Formatting for import rewrite application gate evidence."""
from __future__ import annotations

from .import_rewrite_application_gate import ImportRewriteApplicationGateResult

__all__ = ["format_import_rewrite_application_gate"]


def format_import_rewrite_application_gate(gate: ImportRewriteApplicationGateResult) -> str:
    """Return a readable review-only import rewrite gate report."""
    lines = [
        "IMPORT REWRITE APPLICATION GATE",
        f"Status: {gate.status}",
        f"Importers: {gate.importer_count}",
        f"Rewrite enabled: {gate.rewrite_enabled}",
        f"Apply enabled: {gate.apply_enabled}",
        f"Source hash verified: {gate.source_hash_verified}",
        f"Manifest: {gate.import_rewrite_gate_manifest_path}",
        "",
        "Checked rules:",
    ]
    lines.extend(f"- {rule}" for rule in gate.checked_rules)
    if gate.blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend(f"- {blocker}" for blocker in gate.blockers)
    if gate.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in gate.warnings)
    return "\n".join(lines)
