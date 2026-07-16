
"""Local-AI correction loop primitives for Safe Mode docstring review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .review_state import (
    REVIEW_DECISION_EDITED,
    REVIEW_DECISION_REGENERATE_REQUESTED,
    REVIEW_SOURCE_AI,
    FolderReviewState,
    ReviewDecision,
    ReviewableDocstring,
)


CORRECTION_STATUS_REPAIRED = "repaired"
CORRECTION_STATUS_FAILED = "failed"
CORRECTION_STATUS_REJECTED = "rejected"

TRIPLE_DOUBLE = chr(34) * 3
TRIPLE_SINGLE = chr(39) * 3

FORBIDDEN_DOCSTRING_MARKERS = (
    "todo",
    "tbd",
    "unknown",
    "not implemented",
    "fixme",
    "placeholder",
)


@dataclass(frozen=True)
class CorrectionRequest:
    """Describe one bounded local-AI docstring correction request."""

    row: ReviewableDocstring
    source_context: str
    failure_reason: str
    current_docstring: str
    allowed_parameters: tuple[str, ...] = ()
    allowed_returns: tuple[str, ...] = ()
    allowed_raises: tuple[str, ...] = ()
    prompt: str = ""


@dataclass(frozen=True)
class CorrectionResult:
    """Store the result of one local-AI Safe Mode correction attempt."""

    row_id: str
    success: bool
    status: str
    corrected_docstring: str = ""
    source: str = REVIEW_SOURCE_AI
    error: str = ""
    raw_response: str = ""
    prompt: str = ""


LocalAiCorrector = Callable[[CorrectionRequest], str]


def create_correction_request(
    row: ReviewableDocstring,
    source_context: str,
    failure_reason: str = "",
    allowed_parameters: tuple[str, ...] = (),
    allowed_returns: tuple[str, ...] = (),
    allowed_raises: tuple[str, ...] = (),
) -> CorrectionRequest:
    """Create a local-AI correction request for one review row."""
    reason = failure_reason or row.failure_reason or row.action_hint or "review requested"
    current_docstring = row.proposed_docstring
    request = CorrectionRequest(
        row=row,
        source_context=source_context,
        failure_reason=reason,
        current_docstring=current_docstring,
        allowed_parameters=allowed_parameters,
        allowed_returns=allowed_returns,
        allowed_raises=allowed_raises,
        prompt="",
    )
    return CorrectionRequest(
        row=request.row,
        source_context=request.source_context,
        failure_reason=request.failure_reason,
        current_docstring=request.current_docstring,
        allowed_parameters=request.allowed_parameters,
        allowed_returns=request.allowed_returns,
        allowed_raises=request.allowed_raises,
        prompt=build_correction_prompt(request),
    )


def build_correction_prompt(request: CorrectionRequest) -> str:
    """Build an evidence-bound prompt for repairing one docstring."""
    row = request.row
    allowed_parameters = _format_allowed_values(request.allowed_parameters)
    allowed_returns = _format_allowed_values(request.allowed_returns)
    allowed_raises = _format_allowed_values(request.allowed_raises)

    return "\n".join(
        [
            "You are repairing one Python docstring.",
            "",
            "Safety rules:",
            "- Use only evidence present in the source context or allowed evidence lists.",
            "- Do not invent side effects, parameters, return values, exceptions, or behavior.",
            "- Do not include TODO, TBD, unknown, placeholder, or speculative wording.",
            "- Output only the final Python docstring text.",
            "",
            "Target:",
            f"- file: {row.file_path}",
            f"- kind: {row.target_kind}",
            f"- name: {row.target_name}",
            f"- insert_line: {row.insert_line}",
            "",
            "Correction reason:",
            request.failure_reason,
            "",
            "Current proposed docstring:",
            request.current_docstring,
            "",
            "Allowed parameters:",
            allowed_parameters,
            "",
            "Allowed returns:",
            allowed_returns,
            "",
            "Allowed raises:",
            allowed_raises,
            "",
            "Source context:",
            request.source_context,
            "",
            "Return only the corrected docstring.",
        ]
    )


def run_local_ai_correction(
    request: CorrectionRequest,
    corrector: LocalAiCorrector,
) -> CorrectionResult:
    """Run one local-AI correction attempt with validation."""
    try:
        raw_response = corrector(request)
    except Exception as exc:
        return CorrectionResult(
            row_id=request.row.row_id,
            success=False,
            status=CORRECTION_STATUS_FAILED,
            error=str(exc),
            prompt=request.prompt,
        )

    cleaned = normalize_docstring_response(raw_response)
    validation_error = validate_corrected_docstring(cleaned)
    if validation_error:
        return CorrectionResult(
            row_id=request.row.row_id,
            success=False,
            status=CORRECTION_STATUS_REJECTED,
            error=validation_error,
            raw_response=raw_response,
            prompt=request.prompt,
        )

    return CorrectionResult(
        row_id=request.row.row_id,
        success=True,
        status=CORRECTION_STATUS_REPAIRED,
        corrected_docstring=cleaned,
        raw_response=raw_response,
        prompt=request.prompt,
    )


def apply_correction_result(
    state: FolderReviewState,
    result: CorrectionResult,
) -> FolderReviewState:
    """Apply a successful correction result as an edited review decision."""
    if not result.success:
        return state

    decisions = dict(state.decisions)
    decisions[result.row_id] = ReviewDecision(
        row_id=result.row_id,
        decision=REVIEW_DECISION_EDITED,
        final_docstring=result.corrected_docstring,
        source=REVIEW_SOURCE_AI,
        reason=result.status,
    )

    return FolderReviewState(
        folder_relative_path=state.folder_relative_path,
        rows=state.rows,
        decisions=decisions,
    )


def request_rows_for_ai_retry(state: FolderReviewState) -> tuple[ReviewableDocstring, ...]:
    """Return rows currently marked for AI regeneration."""
    rows_by_id = {row.row_id: row for row in state.rows}
    requested: list[ReviewableDocstring] = []

    for row_id, decision in state.decisions.items():
        if decision.decision == REVIEW_DECISION_REGENERATE_REQUESTED and row_id in rows_by_id:
            requested.append(rows_by_id[row_id])

    return tuple(sorted(requested, key=lambda row: row.row_id))


def normalize_docstring_response(text: str) -> str:
    """Normalize a raw local-AI response into docstring text."""
    value = (text or "").strip()
    value = _strip_code_fence(value).strip()

    if value.startswith("```"):
        value = _strip_code_fence(value).strip()

    return value


def validate_corrected_docstring(docstring: str) -> str:
    """Return an error string when a corrected docstring is unsafe."""
    value = (docstring or "").strip()
    if not value:
        return "corrected docstring is empty"

    lower = value.lower()
    for marker in FORBIDDEN_DOCSTRING_MARKERS:
        if marker in lower:
            return f"corrected docstring contains forbidden marker: {marker}"

    is_triple_double = value.startswith(TRIPLE_DOUBLE) and value.endswith(TRIPLE_DOUBLE)
    is_triple_single = value.startswith(TRIPLE_SINGLE) and value.endswith(TRIPLE_SINGLE)
    if not (is_triple_double or is_triple_single):
        return "corrected docstring must be triple-quoted"

    if value.count(TRIPLE_DOUBLE) == 1 or value.count(TRIPLE_SINGLE) == 1:
        return "corrected docstring has unbalanced triple quotes"

    return ""


def _strip_code_fence(value: str) -> str:
    if not value.startswith("```"):
        return value

    lines = value.splitlines()
    if not lines:
        return value

    if lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines)


def _format_allowed_values(values: tuple[str, ...]) -> str:
    if not values:
        return "- none evidenced"
    return "\n".join(f"- {value}" for value in values)
