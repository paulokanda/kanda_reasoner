# project-path: kanda_reasoner_app/engineering_diagnostics_patch_preview/policy.py
"""Eligibility and exact-source policy for governed Patch Preview."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticFindingRecord,
    DiagnosticRemediationIntent,
    DiagnosticRunRecord,
)

from .models import GovernedPatchPreviewPlan
from .storage import governed_preview_sha256_file

__all__ = ["build_governed_patch_preview_plan", "patch_preview_approval_token"]

_SUPPORTED_RUFF = {
    "F401": "RUFF_SAFE_UNUSED_IMPORT",
    "I001": "RUFF_SAFE_IMPORT_FORMAT",
}


def patch_preview_approval_token(issue_fingerprint: str) -> str:
    """Return the exact local confirmation token for one issue."""
    value = str(issue_fingerprint or "").strip()
    if len(value) < 12:
        raise ValueError("PATCH_PREVIEW_ISSUE_FINGERPRINT_INVALID")
    return "PREVIEW " + value[:12]


def _source_file(root: Path, relative_path: str) -> Path:
    relative = Path(str(relative_path or "").replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("PATCH_PREVIEW_PATH_OUTSIDE_PROJECT")
    target = (root / relative).resolve(strict=True)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("PATCH_PREVIEW_PATH_OUTSIDE_PROJECT") from exc
    if not target.is_file():
        raise ValueError("PATCH_PREVIEW_SOURCE_FILE_MISSING")
    return target


def build_governed_patch_preview_plan(
    project_root: str | Path,
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    intent: DiagnosticRemediationIntent,
    *,
    decision_state: str,
    owner_status: str,
    approval_token: str,
) -> GovernedPatchPreviewPlan:
    """Build one plan only for a reviewed, safe, exact-file correction."""
    root = Path(project_root).expanduser().resolve(strict=True)
    if str(decision_state or "").strip().upper() != "PATCH_PREPARED":
        raise ValueError("PATCH_PREVIEW_REQUIRES_PATCH_PREPARED_LIFECYCLE")
    if str(owner_status or "").strip().upper() != "READY":
        raise ValueError("PATCH_PREVIEW_REQUIRES_READY_CANONICAL_OWNER")
    if intent.target_issue_fingerprint != finding.issue_fingerprint:
        raise ValueError("PATCH_PREVIEW_INTENT_ISSUE_MISMATCH")
    if intent.action_class != "SAFE_MECHANICAL_FIX_AVAILABLE":
        raise ValueError("PATCH_PREVIEW_ACTION_CLASS_NOT_ELIGIBLE")
    if intent.mechanical_safety != "SAFE_MECHANICAL":
        raise ValueError("PATCH_PREVIEW_MECHANICAL_SAFETY_NOT_PROVEN")
    if intent.semantic_review_requirement != "NOT_REQUIRED":
        raise ValueError("PATCH_PREVIEW_SEMANTIC_REVIEW_STILL_REQUIRED")
    if intent.frozen_path_impact != "UNFROZEN" or intent.governing_freeze_ids:
        raise ValueError("PATCH_PREVIEW_FROZEN_PATH_HARD_BLOCK")
    if len(intent.expected_affected_files) != 1:
        raise ValueError("PATCH_PREVIEW_EXACTLY_ONE_FILE_REQUIRED")
    if intent.expected_affected_files[0] != finding.relative_path:
        raise ValueError("PATCH_PREVIEW_EXPECTED_FILE_MISMATCH")

    token = patch_preview_approval_token(finding.issue_fingerprint)
    if str(approval_token or "").strip() != token:
        raise ValueError("PATCH_PREVIEW_EXACT_HUMAN_CONFIRMATION_REQUIRED")

    if run.producer_id == BOM_PRODUCER_ID:
        kind = "UTF8_BOM_REMOVAL"
    elif run.producer_id == RUFF_PRODUCER_ID and finding.code in _SUPPORTED_RUFF:
        kind = _SUPPORTED_RUFF[finding.code]
    else:
        raise ValueError("PATCH_PREVIEW_CORRECTION_KIND_NOT_ELIGIBLE")

    source = _source_file(root, finding.relative_path)
    original_sha256 = governed_preview_sha256_file(source)
    return GovernedPatchPreviewPlan(
        intent_id=intent.intent_id,
        issue_fingerprint=finding.issue_fingerprint,
        run_id=run.run_id,
        producer_id=run.producer_id,
        code=finding.code,
        relative_path=finding.relative_path,
        correction_kind=kind,
        original_sha256=original_sha256,
        focused_validation=(
            "Compile the isolated proposed Python file.",
            "Re-run only the originating BOM or Ruff rule in the isolated workspace.",
            "Prove active Project source remains byte-identical during preview generation.",
        ),
        required_project_validation=(
            "Run the canonical focused owner tests from the remediation intent.",
            "Run Validate Project and architecture non-regression on the governed source patch.",
            "Install only through normal exact-source governed delivery after human review.",
        ),
        rollback_expectation=(
            "The preview bundle must retain the exact original bytes and SHA-256 in a "
            "separate rollback ZIP before any later governed source installation."
        ),
        approval_token=token,
        installable=False,
        source_mutation_allowed=False,
    )
