# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_real_preview_formatting.py
"""Formatting helpers for real moved-code preview generation."""
from __future__ import annotations

from .cst_real_preview_writer import RealPreviewWriteResult

__all__ = ["format_real_preview_result"]


def format_real_preview_result(result: RealPreviewWriteResult) -> str:
    """Return GUI text for real preview generation."""
    lines = [
        "Real moved-code preview generation",
        f"Status: {result.status}",
        f"Target file: {result.target_file or '<none>'}",
        f"Source hash: {result.source_content_hash or '<none>'}",
        f"Preview root: {result.preview_root or '<none>'}",
        f"LibCST available: {result.libcst_available}",
        f"Source mutation enabled: {result.source_mutation_enabled}",
        "",
        "Generated preview files:",
    ]
    if result.files:
        for item in result.files:
            lines.extend(
                [
                    f"- {item.relative_path}",
                    f"  Role: {item.role}",
                    f"  Lines: {item.physical_lines}",
                    f"  Symbols: {', '.join(item.symbols) or '<none>'}",
                    f"  Hash: {item.content_hash}",
                ]
            )
    else:
        lines.append("- <none>")
    lines.extend(["", "Written files:"])
    if result.written_files:
        lines.extend(f"- {path}" for path in result.written_files)
    else:
        lines.append("- <none>")
    lines.extend(["", "Blockers:"])
    if result.blockers:
        lines.extend(f"- {item}" for item in result.blockers)
    else:
        lines.append("- <none>")
    lines.extend(["", "Warnings:"])
    if result.warnings:
        lines.extend(f"- {item}" for item in result.warnings)
    else:
        lines.append("- <none>")
    lines.extend(
        [
            "",
            "Safety:",
            "- This output is Preview state under selected project support.",
            "- It is not source truth.",
            "- It does not enable source apply.",
            "- Import migration apply remains disabled.",
        ]
    )
    return "\n".join(lines)
