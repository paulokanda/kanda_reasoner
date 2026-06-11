
"""Per-docstring review state primitives for Safe Mode."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any


REVIEW_DECISION_PENDING = "pending"
REVIEW_DECISION_ACCEPTED = "accepted"
REVIEW_DECISION_EDITED = "edited"
REVIEW_DECISION_REGENERATE_REQUESTED = "regenerate_requested"
REVIEW_DECISION_FALLBACK_REQUESTED = "fallback_requested"
REVIEW_DECISION_SKIPPED = "skipped"
REVIEW_DECISION_REJECTED = "rejected"

FINAL_REVIEW_DECISIONS = {
    REVIEW_DECISION_ACCEPTED,
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_SKIPPED,
    REVIEW_DECISION_REJECTED,
}

AI_RETRY_REVIEW_DECISIONS = {
    REVIEW_DECISION_REGENERATE_REQUESTED,
    REVIEW_DECISION_FALLBACK_REQUESTED,
}

REVIEW_SOURCE_AI = "ai"
REVIEW_SOURCE_HEURISTIC = "heuristic"
REVIEW_SOURCE_MANUAL_EDIT = "manual_edit"
REVIEW_SOURCE_NONE = "none"

REVIEW_SEVERITY_INFO = "info"
REVIEW_SEVERITY_WARNING = "warning"
REVIEW_SEVERITY_BLOCKING = "blocking"


@dataclass(frozen=True)
class ReviewableDocstring:
    """Represent one docstring candidate waiting for Safe Mode review."""

    row_id: str
    file_path: str
    target_kind: str
    target_name: str
    insert_line: int | None
    proposed_docstring: str
    generation_source: str = REVIEW_SOURCE_NONE
    review_status: str = "needs_review"
    review_severity: str = REVIEW_SEVERITY_INFO
    action_hint: str = ""
    failure_reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewDecision:
    """Store the reviewer decision for one docstring candidate."""

    row_id: str
    decision: str = REVIEW_DECISION_PENDING
    final_docstring: str = ""
    source: str = REVIEW_SOURCE_NONE
    reason: str = ""
    reviewer_note: str = ""

    def is_final(self) -> bool:
        """Return True when this decision resolves the row."""
        return self.decision in FINAL_REVIEW_DECISIONS

    def needs_ai_retry(self) -> bool:
        """Return True when this row should be sent to AI or fallback repair."""
        return self.decision in AI_RETRY_REVIEW_DECISIONS


@dataclass(frozen=True)
class FolderReviewState:
    """Track all per-docstring decisions for one Safe Mode folder."""

    folder_relative_path: str
    rows: tuple[ReviewableDocstring, ...]
    decisions: dict[str, ReviewDecision] = field(default_factory=dict)

    def pending_rows(self) -> tuple[ReviewableDocstring, ...]:
        """Return rows that still need a final reviewer decision."""
        pending: list[ReviewableDocstring] = []
        for row in self.rows:
            decision = self.decisions.get(row.row_id)
            if decision is None or not decision.is_final():
                pending.append(row)
        return tuple(pending)

    def unresolved_count(self) -> int:
        """Return the number of rows without a final decision."""
        return len(self.pending_rows())

    def is_resolved(self) -> bool:
        """Return True when all rows have final decisions."""
        return self.unresolved_count() == 0

    def accepted_docstrings(self) -> tuple[ReviewDecision, ...]:
        """Return accepted or manually edited docstring decisions."""
        accepted = []
        for decision in self.decisions.values():
            if decision.decision in {REVIEW_DECISION_ACCEPTED, REVIEW_DECISION_EDITED}:
                accepted.append(decision)
        return tuple(sorted(accepted, key=lambda item: item.row_id))

    def skipped_or_rejected(self) -> tuple[ReviewDecision, ...]:
        """Return skipped or rejected decisions."""
        skipped = []
        for decision in self.decisions.values():
            if decision.decision in {REVIEW_DECISION_SKIPPED, REVIEW_DECISION_REJECTED}:
                skipped.append(decision)
        return tuple(sorted(skipped, key=lambda item: item.row_id))


def build_reviewable_docstring(row: dict[str, Any], row_index: int) -> ReviewableDocstring:
    """Create a reviewable Safe Mode row from a report-row dictionary."""
    row_id = str(
        row.get("row_id")
        or row.get("id")
        or f"{row.get('file', '')}:{row.get('target_name', '')}:{row_index}"
    )

    insert_line_value = row.get("insert_line")
    insert_line: int | None
    if isinstance(insert_line_value, int):
        insert_line = insert_line_value
    else:
        insert_line = None

    proposed = str(
        row.get("proposed_docstring")
        or row.get("docstring")
        or row.get("rendered_docstring")
        or row.get("source")
        or ""
    )

    return ReviewableDocstring(
        row_id=row_id,
        file_path=str(row.get("file") or row.get("path") or ""),
        target_kind=str(row.get("target_kind") or ""),
        target_name=str(row.get("target_name") or ""),
        insert_line=insert_line,
        proposed_docstring=proposed,
        generation_source=str(row.get("generation_source") or REVIEW_SOURCE_NONE),
        review_status=str(row.get("review_status") or "needs_review"),
        review_severity=str(row.get("review_severity") or REVIEW_SEVERITY_INFO),
        action_hint=str(row.get("review_action_hint") or ""),
        failure_reason=str(row.get("failure_reason") or ""),
        metadata=dict(row),
    )


def build_folder_review_state(
    folder_relative_path: str,
    report_rows: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> FolderReviewState:
    """Create a folder review state from report rows."""
    rows = tuple(
        build_reviewable_docstring(row, index)
        for index, row in enumerate(report_rows)
    )
    return FolderReviewState(folder_relative_path=folder_relative_path, rows=rows)


def accept_docstring(
    state: FolderReviewState,
    row_id: str,
    final_docstring: str | None = None,
    note: str = "",
) -> FolderReviewState:
    """Return state with one row accepted."""
    row = _find_row(state, row_id)
    docstring = final_docstring if final_docstring is not None else row.proposed_docstring
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_ACCEPTED,
            final_docstring=docstring,
            source=row.generation_source,
            reviewer_note=note,
        ),
    )


def edit_docstring(
    state: FolderReviewState,
    row_id: str,
    edited_docstring: str,
    note: str = "",
) -> FolderReviewState:
    """Return state with one row manually edited."""
    if not edited_docstring.strip():
        raise ValueError("Edited docstring cannot be empty.")
    _find_row(state, row_id)
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_EDITED,
            final_docstring=edited_docstring,
            source=REVIEW_SOURCE_MANUAL_EDIT,
            reviewer_note=note,
        ),
    )


def request_regeneration(
    state: FolderReviewState,
    row_id: str,
    reason: str,
) -> FolderReviewState:
    """Return state with one row marked for local-AI regeneration."""
    if not reason.strip():
        raise ValueError("Regeneration reason cannot be empty.")
    _find_row(state, row_id)
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_REGENERATE_REQUESTED,
            source=REVIEW_SOURCE_AI,
            reason=reason,
        ),
    )


def request_fallback(
    state: FolderReviewState,
    row_id: str,
    reason: str,
) -> FolderReviewState:
    """Return state with one row marked for heuristic fallback repair."""
    if not reason.strip():
        raise ValueError("Fallback reason cannot be empty.")
    _find_row(state, row_id)
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_FALLBACK_REQUESTED,
            source=REVIEW_SOURCE_HEURISTIC,
            reason=reason,
        ),
    )


def skip_docstring(
    state: FolderReviewState,
    row_id: str,
    reason: str = "",
) -> FolderReviewState:
    """Return state with one row skipped by the reviewer."""
    _find_row(state, row_id)
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_SKIPPED,
            source=REVIEW_SOURCE_NONE,
            reason=reason,
        ),
    )


def reject_docstring(
    state: FolderReviewState,
    row_id: str,
    reason: str,
) -> FolderReviewState:
    """Return state with one row rejected by the reviewer."""
    if not reason.strip():
        raise ValueError("Reject reason cannot be empty.")
    _find_row(state, row_id)
    return _with_decision(
        state,
        ReviewDecision(
            row_id=row_id,
            decision=REVIEW_DECISION_REJECTED,
            source=REVIEW_SOURCE_NONE,
            reason=reason,
        ),
    )


def clear_decision(state: FolderReviewState, row_id: str) -> FolderReviewState:
    """Return state with one row decision removed."""
    _find_row(state, row_id)
    decisions = dict(state.decisions)
    decisions.pop(row_id, None)
    return replace(state, decisions=decisions)


def _find_row(state: FolderReviewState, row_id: str) -> ReviewableDocstring:
    for row in state.rows:
        if row.row_id == row_id:
            return row
    raise KeyError(f"Unknown review row id: {row_id}")


def _with_decision(
    state: FolderReviewState,
    decision: ReviewDecision,
) -> FolderReviewState:
    _find_row(state, decision.row_id)
    decisions = dict(state.decisions)
    decisions[decision.row_id] = decision
    return replace(state, decisions=decisions)
