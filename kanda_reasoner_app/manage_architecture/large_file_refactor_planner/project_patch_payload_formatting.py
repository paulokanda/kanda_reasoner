# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/project_patch_payload_formatting.py
"""Formatting helpers for governed project patch payload results."""
from __future__ import annotations

from .models import ProjectPatchPayloadResult

__all__ = ["format_project_patch_payload_result"]


def format_project_patch_payload_result(result: ProjectPatchPayloadResult) -> str:
    """Return a reviewable project patch payload summary."""
    lines = [
        "# Governed Project Patch Payload",
        f"Status: {result.status}",
        f"Patch payload created: {result.patch_payload_created}",
        f"Source hash verified: {result.source_hash_verified}",
        f"Payload ZIP: {result.payload_zip_path}",
        f"Payload manifest: {result.payload_manifest_path}",
        f"Preview root: {result.preview_root}",
        "",
        "Included files:",
    ]
    lines.extend("- " + item for item in result.included_files)
    if result.blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    lines.append("")
    lines.append("No selected project source was modified by payload creation.")
    return "\n".join(lines)
