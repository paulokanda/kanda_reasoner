# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_formatting.py
"""Formatting helpers for governed preview generation."""
from __future__ import annotations

from .models import (
    ImportMigrationPreview,
    PreviewArtifactValidationResult,
    PreviewBundle,
    PreviewValidationResult,
    PreviewWriteResult,
)

__all__ = [
    "format_import_migration_preview",
    "format_preview_artifact_validation",
    "format_preview_bundle",
    "format_preview_validation",
    "format_preview_write_result",
]


def format_preview_bundle(bundle: PreviewBundle) -> str:
    """Return a reviewable preview bundle summary."""
    lines = [
        "Governed preview bundle generated.",
        "Important:",
        "- Selected project source files were not modified.",
        "- Preview files may be written only to the project-support Preview area.",
        "- LibCST is still a parse/availability gate; source transforms remain future-scoped.",
        "",
        f"Status: {bundle.status}",
        f"Target file: {bundle.target_file}",
        f"Preview root: {bundle.preview_root or '<not resolved>'}",
        f"Write mode: {bundle.write_mode}",
        f"LibCST available: {bundle.libcst_available}",
        "",
        "Preview file drafts:",
    ]
    for draft in bundle.files:
        lines.append(
            f"- {draft.relative_path} | role={draft.source_role} | "
            f"symbols={len(draft.planned_symbols)} | write_enabled={draft.write_enabled}"
        )
    if bundle.validation_blockers:
        lines.append("")
        lines.append("Blockers:")
        lines.extend("- " + item for item in bundle.validation_blockers)
    if bundle.risk_flags:
        lines.append("")
        lines.append("Warnings:")
        lines.extend("- " + item for item in bundle.risk_flags)
    return "\n".join(lines)


def format_preview_validation(result: PreviewValidationResult) -> str:
    """Return a reviewable preview validation summary."""
    lines = ["Preview validation result.", f"Status: {result.status}", "Checked rules:"]
    lines.extend("- " + rule for rule in result.checked_rules)
    if result.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)


def format_preview_write_result(result: PreviewWriteResult) -> str:
    """Return a reviewable preview artifact write summary."""
    lines = ["Preview artifact write result.", f"Status: {result.status}", f"Root: {result.preview_root}"]
    if result.written_files:
        lines.append("Written files:")
        lines.extend("- " + item for item in result.written_files)
    if result.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)


def format_import_migration_preview(preview: ImportMigrationPreview) -> str:
    """Return a reviewable import migration preview summary."""
    lines = [
        "Import migration preview.",
        "Important:",
        "- This is review-only and does not rewrite project imports.",
        "- Public API imports should keep targeting the facade unless later validation approves otherwise.",
        f"Status: {preview.status}",
        f"Rewrite enabled: {preview.rewrite_enabled}",
        f"Records: {len(preview.records)}",
    ]
    for record in preview.records:
        lines.append(
            f"- {record.importer_file} | action={record.action} | suggestion={record.suggested_import}"
        )
    if preview.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in preview.blockers)
    if preview.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in preview.warnings)
    return "\n".join(lines)


def format_preview_artifact_validation(result: PreviewArtifactValidationResult) -> str:
    """Return a reviewable preview artifact validation summary."""
    lines = [
        "Preview artifact validation result.",
        f"Status: {result.status}",
        f"Root: {result.preview_root}",
        f"Source hash verified: {result.source_hash_verified}",
        f"Manifest present: {result.manifest_present}",
        f"No-source-write proof present: {result.proof_present}",
        f"Import migration preview: {result.import_migration_preview_status}",
    ]
    if result.checked_files:
        lines.append("Checked files:")
        lines.extend("- " + item for item in result.checked_files)
    if result.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in result.blockers)
    if result.warnings:
        lines.append("Warnings:")
        lines.extend("- " + item for item in result.warnings)
    return "\n".join(lines)
