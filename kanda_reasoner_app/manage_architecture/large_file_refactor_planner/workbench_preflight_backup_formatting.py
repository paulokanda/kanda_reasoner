# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_preflight_backup_formatting.py
"""Operator-facing formatting for Workbench preflight backup readiness."""
from __future__ import annotations

from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult

__all__ = [
    "format_preflight_backup_readiness",
    "format_preflight_gate_reason",
]

_BLOCKER_EXPLANATIONS = {
    "PLANNER_PLAN_MISSING": "No Workbench-owned Planner snapshot can be materialized.",
    "REAL_PREVIEW_NOT_READY": "The exact real preview has not been generated successfully.",
    "STRUCTURAL_PREVIEW_VALIDATION_MISSING": "No structural preview validation evidence exists.",
    "REAL_PREVIEW_STRUCTURAL_VALIDATION_NOT_ACCEPTED": "Structural preview validation did not pass.",
    "PREVIEW_RESULT_ENABLED_SOURCE_MUTATION": "Preview evidence unexpectedly claims source mutation capability.",
    "STRUCTURAL_VALIDATION_ENABLED_SOURCE_MUTATION": "Structural validation unexpectedly claims source mutation capability.",
    "SOURCE_DRIFT_DETECTED": "The selected source content no longer matches the Planner basis hash.",
    "REAL_PREVIEW_RESULT_MISSING": "Real preview evidence is unavailable.",
    "BACKUP_DESTINATION_NOT_WRITABLE": "The governed backup location could not be written safely.",
    "BACKUP_SNAPSHOT_CREATE_FAILED": "The source-derived backup snapshot could not be created.",
    "BACKUP_SNAPSHOT_HASH_MISMATCH": "The created backup snapshot does not match the source basis hash.",
    "ROLLBACK_MANIFEST_PREPARE_FAILED": "Rollback intent evidence could not be created or re-read.",
    "ROLLBACK_MANIFEST_SOURCE_HASH_MISMATCH": "Rollback evidence does not preserve the source basis identity.",
    "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE": "Preview artifacts resolved inside the active project source tree.",
    "PREVIEW_ROOT_OUTSIDE_PROJECT_SUPPORT": "Preview artifacts resolved outside the selected project support root.",
    "BACKUP_ROOT_OUTSIDE_PREVIEW_ROOT": "Backup artifacts escaped the selected preview evidence root.",
    "BACKUP_ROOT_INSIDE_PROJECT_SOURCE": "Backup artifacts resolved inside active project source.",
    "PREFLIGHT_ARTIFACT_ROOT_INSIDE_PROTECTED_ROOT": "Preflight artifacts crossed into a protected support-memory root.",
}


def format_preflight_backup_readiness(
    result: WorkbenchPreflightBackupReadinessResult,
) -> str:
    """Return a detailed, operator-readable preflight readiness report."""
    lines = [
        "Large File Refactor Workbench - Preflight Backup Readiness",
        "",
        f"Status: {result.status}",
        f"Target file: {result.target_file or '<none>'}",
        f"Source basis hash: {result.source_content_hash or '<none>'}",
        f"Preview root: {result.preview_root}",
        f"Preflight manifest: {result.preflight_manifest_path}",
        f"Backup root: {result.backup_root}",
        f"Backup snapshot: {result.backup_snapshot_path}",
        f"Rollback manifest: {result.rollback_manifest_path}",
        "",
        "Readiness checks:",
        f"- source hash verified: {_yes_no(result.source_hash_verified)}",
        f"- preview hashes verified: {_yes_no(result.preview_hashes_verified)}",
        f"- destination collision free: {_yes_no(result.destination_collision_free)}",
        f"- backup destination writable: {_yes_no(result.backup_destination_writable)}",
        f"- backup snapshot verified: {_yes_no(result.backup_snapshot_verified)}",
        f"- rollback manifest prepared: {_yes_no(result.rollback_manifest_prepared)}",
        f"- source mutation enabled: {_yes_no(result.source_mutation_enabled)}",
        f"- apply enabled: {_yes_no(result.apply_enabled)}",
        f"- import rewrite enabled: {_yes_no(result.import_rewrite_enabled)}",
        "",
        "Checked preview files:",
    ]
    lines.extend(_bullets(result.checked_preview_files) or ["- none"])
    lines.extend(["", "Checked destination paths:"])
    lines.extend(_bullets(result.checked_destination_paths) or ["- none"])
    lines.extend(["", "Checked rules:"])
    lines.extend(_bullets(result.checked_rules) or ["- none"])
    lines.extend(["", "Blockers:"])
    if result.blockers:
        for blocker in result.blockers:
            lines.append("- " + blocker)
            explanation = explain_preflight_blocker(blocker)
            if explanation:
                lines.append("  " + explanation)
    else:
        lines.append("- none")
    lines.extend(["", "Warnings:"])
    lines.extend(_bullets(result.warnings) or ["- none"])
    lines.extend(
        [
            "",
            "Safety meaning:",
            "- Preflight readiness never applies project source changes.",
            "- The backup snapshot is recovery evidence, not canonical source truth.",
            "- Source or preview drift invalidates this evidence and must block payload construction.",
            "- A ready result allows only the next governed payload-construction stage.",
        ]
    )
    return "\n".join(lines)


def format_preflight_gate_reason(
    structural_status: str,
    *,
    source_drift: bool = False,
    preview_drift: bool = False,
    owner_available: bool = True,
) -> str:
    """Return explicit machine-readable gate text for a blocked Preflight action."""
    reason = "REAL_PREVIEW_STRUCTURAL_VALIDATION_NOT_ACCEPTED"
    detail = "Validate Real Preview successfully before Preflight."
    if not owner_available:
        reason = "PREFLIGHT_OWNER_MODULE_UNAVAILABLE"
        detail = "The Workbench Preflight owner module is unavailable."
    elif source_drift:
        reason = "SOURCE_DRIFT_DETECTED"
        detail = "Reload or re-plan against the current source before continuing."
    elif preview_drift:
        reason = "PREVIEW_HASH_CHANGED"
        detail = "Regenerate and revalidate the exact preview artifacts."
    elif structural_status.startswith("passed"):
        reason = "AQR_REQUIRED"
        detail = (
            "Structural validation is accepted. Run Advanced Quality Review; "
            "Preflight remains closed until AQR authorizes it."
        )
    return "\n".join(
        [
            "PREFLIGHT GATE",
            "",
            "Reason: " + reason,
            "Structural status: " + (structural_status or "missing"),
            "Next action: " + detail,
        ]
    )


def explain_preflight_blocker(blocker: str) -> str:
    """Return a concise explanation for one blocker, including prefixed variants."""
    if blocker in _BLOCKER_EXPLANATIONS:
        return _BLOCKER_EXPLANATIONS[blocker]
    for prefix, explanation in (
        ("PREVIEW_HASH_CHANGED:", "A generated preview file no longer matches its recorded generation hash."),
        ("PREVIEW_FILE_MISSING:", "A generated preview file disappeared after preview generation."),
        ("PREVIEW_FILE_OUTSIDE_PREVIEW_ROOT:", "A preview file path escaped the governed preview root."),
        ("DESTINATION_HELPER_COLLISION:", "A planned helper destination already exists and would be overwritten."),
        ("DESTINATION_OUTSIDE_PROJECT_ROOT:", "A planned destination escapes the selected project root."),
        ("DESTINATION_OUTSIDE_TARGET_DIRECTORY:", "A planned destination escapes the target module directory."),
        ("DESTINATION_INSIDE_PROTECTED_ROOT:", "A planned destination crosses into a protected support root."),
        ("UNSAFE_DESTINATION_RELATIVE_PATH:", "A planned destination uses an unsafe absolute or traversal path."),
    ):
        if blocker.startswith(prefix):
            return explanation
    return ""


def _yes_no(value: bool) -> str:
    """Return stable human-readable Boolean text."""
    return "YES" if value else "NO"


def _bullets(values: list[str]) -> list[str]:
    """Return values as stable bullet lines."""
    return ["- " + value for value in values]
