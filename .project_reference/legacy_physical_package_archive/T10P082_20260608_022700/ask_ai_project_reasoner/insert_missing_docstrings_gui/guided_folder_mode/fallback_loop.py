
"""Heuristic fallback correction loop primitives for Safe Mode."""

from __future__ import annotations

from dataclasses import dataclass

from .correction_loop import validate_corrected_docstring
from .review_state import (
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_FALLBACK_REQUESTED,
    REVIEW_SOURCE_HEURISTIC,
    FolderReviewState,
    ReviewDecision,
    ReviewableDocstring,
)


FALLBACK_STATUS_GENERATED = "generated"
FALLBACK_STATUS_FAILED = "failed"
FALLBACK_STATUS_REJECTED = "rejected"

TRIPLE_DOUBLE = chr(34) * 3


@dataclass(frozen=True)
class HeuristicFallbackRequest:
    """Describe one evidence-limited heuristic fallback request."""

    row: ReviewableDocstring
    source_context: str = ""
    reason: str = ""
    allowed_parameters: tuple[str, ...] = ()
    allowed_returns: tuple[str, ...] = ()
    allowed_raises: tuple[str, ...] = ()
    class_attributes: tuple[str, ...] = ()


@dataclass(frozen=True)
class HeuristicFallbackResult:
    """Store the result of one heuristic fallback correction attempt."""

    row_id: str
    success: bool
    status: str
    fallback_docstring: str = ""
    source: str = REVIEW_SOURCE_HEURISTIC
    error: str = ""


def create_heuristic_fallback_request(
    row: ReviewableDocstring,
    source_context: str = "",
    reason: str = "",
    allowed_parameters: tuple[str, ...] = (),
    allowed_returns: tuple[str, ...] = (),
    allowed_raises: tuple[str, ...] = (),
    class_attributes: tuple[str, ...] = (),
) -> HeuristicFallbackRequest:
    """Create a heuristic fallback request for one review row."""
    return HeuristicFallbackRequest(
        row=row,
        source_context=source_context,
        reason=reason or row.failure_reason or row.action_hint or "fallback requested",
        allowed_parameters=allowed_parameters,
        allowed_returns=allowed_returns,
        allowed_raises=allowed_raises,
        class_attributes=class_attributes,
    )


def run_heuristic_fallback(request: HeuristicFallbackRequest) -> HeuristicFallbackResult:
    """Generate and validate one heuristic fallback docstring."""
    try:
        docstring = generate_heuristic_fallback_docstring(request)
    except Exception as exc:
        return HeuristicFallbackResult(
            row_id=request.row.row_id,
            success=False,
            status=FALLBACK_STATUS_FAILED,
            error=str(exc),
        )

    validation_error = validate_corrected_docstring(docstring)
    if validation_error:
        return HeuristicFallbackResult(
            row_id=request.row.row_id,
            success=False,
            status=FALLBACK_STATUS_REJECTED,
            fallback_docstring=docstring,
            error=validation_error,
        )

    return HeuristicFallbackResult(
        row_id=request.row.row_id,
        success=True,
        status=FALLBACK_STATUS_GENERATED,
        fallback_docstring=docstring,
    )


def apply_heuristic_fallback_result(
    state: FolderReviewState,
    result: HeuristicFallbackResult,
) -> FolderReviewState:
    """Apply a successful fallback result as an edited review decision."""
    if not result.success:
        return state

    decisions = dict(state.decisions)
    decisions[result.row_id] = ReviewDecision(
        row_id=result.row_id,
        decision=REVIEW_DECISION_EDITED,
        final_docstring=result.fallback_docstring,
        source=REVIEW_SOURCE_HEURISTIC,
        reason=result.status,
    )

    return FolderReviewState(
        folder_relative_path=state.folder_relative_path,
        rows=state.rows,
        decisions=decisions,
    )


def request_rows_for_fallback_retry(state: FolderReviewState) -> tuple[ReviewableDocstring, ...]:
    """Return rows currently marked for heuristic fallback repair."""
    rows_by_id = {row.row_id: row for row in state.rows}
    requested: list[ReviewableDocstring] = []

    for row_id, decision in state.decisions.items():
        if decision.decision == REVIEW_DECISION_FALLBACK_REQUESTED and row_id in rows_by_id:
            requested.append(rows_by_id[row_id])

    return tuple(sorted(requested, key=lambda row: row.row_id))


def generate_heuristic_fallback_docstring(request: HeuristicFallbackRequest) -> str:
    """Generate a conservative docstring from explicit evidence only."""
    row = request.row
    target_name = _humanize_name(row.target_name)
    target_kind = (row.target_kind or "target").lower()

    lines: list[str] = [_summary_line(target_kind, target_name)]

    if request.allowed_parameters:
        lines.append("")
        lines.append("Parameters:")
        for name in request.allowed_parameters:
            lines.append(f"    {name}: Parameter used by this {target_kind}.")

    if request.class_attributes:
        lines.append("")
        lines.append("Attributes:")
        for name in request.class_attributes:
            lines.append(f"    {name}: Attribute defined by this class.")

    if request.allowed_returns:
        lines.append("")
        lines.append("Returns:")
        for value in request.allowed_returns:
            lines.append(f"    {value}: Return value evidenced by annotations or source context.")

    if request.allowed_raises:
        lines.append("")
        lines.append("Raises:")
        for value in request.allowed_raises:
            lines.append(f"    {value}: Raised when the source path reaches this exception.")

    body = "\n".join(lines).strip()
    return f"{TRIPLE_DOUBLE}{body}{TRIPLE_DOUBLE}"


def _summary_line(target_kind: str, target_name: str) -> str:
    if target_kind == "module":
        return f"Provide module utilities for {target_name}."
    if target_kind == "class":
        return f"Represent {target_name}."
    if target_kind == "method":
        return f"Run the {target_name} method."
    if target_kind == "function":
        return f"Run the {target_name} function."
    return f"Describe {target_name}."


def _humanize_name(name: str) -> str:
    value = (name or "target").strip("_")
    value = value.replace("_", " ")
    return value or "target"
