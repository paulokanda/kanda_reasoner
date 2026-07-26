# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_patch5_executor_proof.py
"""Read-only canonical freeze proof lookup for the Patch 5 real-apply executor."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_support_boundary import (
    assert_no_forbidden_nested_support_root,
)

from .models import SCHEMA_VERSION

__all__ = [
    "PATCH5_EXECUTOR_PROOF_FEATURE_ID",
    "PATCH5_FREEZE_FEATURE_TITLE",
    "ExecutorProofEvidence",
    "find_patch5_executor_proof",
]

PATCH5_EXECUTOR_PROOF_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-patch5-journaled-apply-adversarial-proof-v1"
)
PATCH5_FREEZE_FEATURE_TITLE = (
    "Large File Refactor Workbench Patch 5 - Journaled Apply and Adversarial Transaction Proof"
)
_EXPECTED_FREEZE_SLUG = "large-file-refactor-workbench-patch-5-journaled-apply-and-adversarial-transaction-proof"


@dataclass(frozen=True)
class ExecutorProofEvidence:
    """Read-only evidence that canonical project freeze memory contains Patch 5 proof."""

    schema_version: str
    feature_id: str
    status: str
    project_root: str
    freeze_memory_root: str
    matched_entry: str
    proof_available: bool
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        return data


def find_patch5_executor_proof(project_root: str | Path) -> ExecutorProofEvidence:
    """Find canonical Patch 5 frozen entry without mutating freeze memory."""
    root = Path(project_root).resolve()
    freeze_root = (
        assert_no_forbidden_nested_support_root(root)
        / "project_freeze_after_update"
        / "frozen_features_memory"
    )
    entries_root = freeze_root / "entries"
    blockers: list[str] = []
    matched = ""
    if not entries_root.is_dir():
        blockers.append("CANONICAL_FROZEN_FEATURE_ENTRIES_ROOT_MISSING")
    else:
        candidates = sorted(entries_root.glob("*.md"), key=lambda path: path.name.casefold())
        for path in candidates:
            if _entry_proves_patch5(path):
                matched = str(path.resolve())
                break
        if not matched:
            blockers.append("PATCH5_EXECUTOR_CANONICAL_FREEZE_ENTRY_NOT_FOUND")
    return ExecutorProofEvidence(
        schema_version=SCHEMA_VERSION,
        feature_id=PATCH5_EXECUTOR_PROOF_FEATURE_ID,
        status="executor_proof_available" if not blockers else "executor_proof_unavailable",
        project_root=str(root),
        freeze_memory_root=str(freeze_root.resolve()),
        matched_entry=matched,
        proof_available=not blockers,
        blockers=tuple(sorted(set(blockers))),
    )


def _entry_proves_patch5(path: Path) -> bool:
    """Return whether one read-only freeze entry proves the exact Patch 5 feature."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    lowered_name = path.stem.casefold()
    has_identity = (
        PATCH5_EXECUTOR_PROOF_FEATURE_ID in text
        or PATCH5_FREEZE_FEATURE_TITLE in text
        or _EXPECTED_FREEZE_SLUG in lowered_name
    )
    has_frozen_status = 'status: "frozen"' in text or "Status: `frozen" in text or "Status: frozen" in text
    has_required_claim = (
        "journaled" in text.casefold()
        and "rollback" in text.casefold()
        and "recovery" in text.casefold()
        and "sealed payload" in text.casefold()
    )
    return bool(has_identity and has_frozen_status and has_required_claim)


def _proof_contract_notes() -> tuple[str, ...]:
    """Return stable explanatory labels for integration and validator evidence."""
    return (
        "freeze_memory_is_read_only",
        "project_specific_memory_owner_is_external_show_project_root",
        "patch5_button_enablement_requires_canonical_frozen_entry",
        "local_validation_alone_does_not_enable_real_apply_gui",
        "validator_may_exercise_executor_only_inside_disposable_fixture_projects",
    )
