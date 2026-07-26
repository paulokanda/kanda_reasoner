# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/patch_gate_formatting.py
"""Formatting helpers for patch ZIP creation gate results."""
from __future__ import annotations

from .patch_zip_gate import PatchZipCreationGateResult

__all__ = ["format_patch_zip_creation_gate"]


def format_patch_zip_creation_gate(result: PatchZipCreationGateResult) -> str:
    """Return a compact review-only patch gate report."""
    lines = [
        "Patch ZIP creation gate",
        "=======================",
        f"Status: {result.status}",
        f"Patch ZIP creation enabled: {result.patch_zip_creation_enabled}",
        f"Preview root: {result.preview_root}",
        f"Gate manifest: {result.gate_manifest_path}",
        "",
        "Checked rules:",
    ]
    lines.extend(f"- {rule}" for rule in result.checked_rules)
    lines.append("")
    lines.append("Blockers:")
    lines.extend(f"- {item}" for item in result.blockers or ["<none>"])
    lines.append("")
    lines.append("Warnings:")
    lines.extend(f"- {item}" for item in result.warnings or ["<none>"])
    lines.append("")
    lines.append("No project patch payload was created by this train.")
    return "\n".join(lines)
