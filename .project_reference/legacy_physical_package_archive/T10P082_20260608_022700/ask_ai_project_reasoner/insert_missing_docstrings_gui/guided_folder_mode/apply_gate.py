
"""Folder apply-gate primitives for Safe Mode docstring review."""

from __future__ import annotations

from dataclasses import dataclass

from .correction_loop import validate_corrected_docstring
from .review_state import (
    REVIEW_DECISION_ACCEPTED,
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_REJECTED,
    REVIEW_DECISION_SKIPPED,
    FolderReviewState,
    ReviewableDocstring,
)


APPLY_GATE_STATUS_READY = "ready"
APPLY_GATE_STATUS_BLOCKED = "blocked"
APPLY_GATE_STATUS_EMPTY = "empty"


@dataclass(frozen=True)
class ApprovedDocstringPatch:
    """Represent one approved docstring insertion candidate."""

    row_id: str
    file_path: str
    target_kind: str
    target_name: str
    insert_line: int
    final_docstring: str
    source: str


@dataclass(frozen=True)
class FolderApplyPlan:
    """Represent approved Safe Mode docstrings for one folder."""

    folder_relative_path: str
    patches: tuple[ApprovedDocstringPatch, ...]
    skipped_row_ids: tuple[str, ...] = ()
    rejected_row_ids: tuple[str, ...] = ()

    def has_patches(self) -> bool:
        """Return True when this plan contains approved patches."""
        return bool(self.patches)


@dataclass(frozen=True)
class FolderApplyGateResult:
    """Store the result of evaluating whether a folder can be applied."""

    success: bool
    status: str
    plan: FolderApplyPlan | None = None
    error: str = ""
    blocked_row_ids: tuple[str, ...] = ()

    def can_apply(self) -> bool:
        """Return True when approved patches can be applied safely."""
        return self.success and self.status in {
            APPLY_GATE_STATUS_READY,
            APPLY_GATE_STATUS_EMPTY,
        }


def build_folder_apply_gate(state: FolderReviewState) -> FolderApplyGateResult:
    """Build an apply plan or return a blocking reason.

    This gate does not write source files. It only proves that the current
    folder has been fully reviewed and that accepted or edited docstrings are
    safe enough to hand to the later writer/validation stage.
    """
    pending_rows = state.pending_rows()
    if pending_rows:
        return FolderApplyGateResult(
            success=False,
            status=APPLY_GATE_STATUS_BLOCKED,
            error="folder review has unresolved rows",
            blocked_row_ids=tuple(row.row_id for row in pending_rows),
        )

    rows_by_id = {row.row_id: row for row in state.rows}
    patches: list[ApprovedDocstringPatch] = []
    skipped: list[str] = []
    rejected: list[str] = []

    for row_id in sorted(state.decisions):
        decision = state.decisions[row_id]
        row = rows_by_id.get(row_id)
        if row is None:
            return FolderApplyGateResult(
                success=False,
                status=APPLY_GATE_STATUS_BLOCKED,
                error=f"decision references unknown row: {row_id}",
                blocked_row_ids=(row_id,),
            )

        if not _row_belongs_to_folder(state.folder_relative_path, row):
            return FolderApplyGateResult(
                success=False,
                status=APPLY_GATE_STATUS_BLOCKED,
                error=f"row is outside selected folder: {row.file_path}",
                blocked_row_ids=(row_id,),
            )

        if decision.decision in {REVIEW_DECISION_ACCEPTED, REVIEW_DECISION_EDITED}:
            if row.insert_line is None:
                return FolderApplyGateResult(
                    success=False,
                    status=APPLY_GATE_STATUS_BLOCKED,
                    error=f"approved row has no insert line: {row_id}",
                    blocked_row_ids=(row_id,),
                )

            validation_error = validate_corrected_docstring(decision.final_docstring)
            if validation_error:
                return FolderApplyGateResult(
                    success=False,
                    status=APPLY_GATE_STATUS_BLOCKED,
                    error=f"approved docstring failed validation: {validation_error}",
                    blocked_row_ids=(row_id,),
                )

            patches.append(
                ApprovedDocstringPatch(
                    row_id=row_id,
                    file_path=row.file_path,
                    target_kind=row.target_kind,
                    target_name=row.target_name,
                    insert_line=row.insert_line,
                    final_docstring=decision.final_docstring,
                    source=decision.source,
                )
            )
            continue

        if decision.decision == REVIEW_DECISION_SKIPPED:
            skipped.append(row_id)
            continue

        if decision.decision == REVIEW_DECISION_REJECTED:
            rejected.append(row_id)
            continue

        return FolderApplyGateResult(
            success=False,
            status=APPLY_GATE_STATUS_BLOCKED,
            error=f"decision is not final-applicable: {decision.decision}",
            blocked_row_ids=(row_id,),
        )

    plan = FolderApplyPlan(
        folder_relative_path=state.folder_relative_path,
        patches=tuple(patches),
        skipped_row_ids=tuple(sorted(skipped)),
        rejected_row_ids=tuple(sorted(rejected)),
    )

    if not patches:
        return FolderApplyGateResult(
            success=True,
            status=APPLY_GATE_STATUS_EMPTY,
            plan=plan,
        )

    return FolderApplyGateResult(
        success=True,
        status=APPLY_GATE_STATUS_READY,
        plan=plan,
    )


def summarize_folder_apply_plan(plan: FolderApplyPlan) -> dict[str, int | str]:
    """Return a compact apply-plan summary for GUI/report display."""
    return {
        "folder_relative_path": plan.folder_relative_path,
        "approved_patch_count": len(plan.patches),
        "skipped_count": len(plan.skipped_row_ids),
        "rejected_count": len(plan.rejected_row_ids),
    }


def approved_file_paths(plan: FolderApplyPlan) -> tuple[str, ...]:
    """Return unique files that would be touched by an apply plan."""
    return tuple(sorted({patch.file_path for patch in plan.patches}))


def _row_belongs_to_folder(folder_relative_path: str, row: ReviewableDocstring) -> bool:
    folder = (folder_relative_path or ".").replace("\\", "/").strip("/")
    file_path = (row.file_path or "").replace("\\", "/").strip("/")

    if not file_path:
        return False
    if folder in {"", "."}:
        return True

    return file_path == folder or file_path.startswith(folder + "/")
