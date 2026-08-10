# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/comparison_engine.py
"""Offline Adviser pure comparison engine.

This module compares a provided teacher answer with a provided candidate answer.
It is deterministic, standard-library-only, and side-effect free.

Authority boundary:
- It does not create or execute an Adviser candidate.
- It does not route.
- It does not load prompts.
- It does not read or write files.
- It does not call models, providers, networks, embeddings, or vector stores.
- It emits review evidence only and has zero router authority.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from ..core.adviser_contract import validate_candidate_answer
from ..core.adviser_output_guard import guard_candidate_output
from ..core.adviser_resource_limits import check_all_resource_limits
from ..core.adviser_severity import evaluate_guard_result

from ._comparison_engine_analysis import (
    _candidate_domain,
    _compare_core_fields,
    _severity_from_guard,
)
from ._comparison_engine_result_model import (
    _final_result,
)
from ._comparison_engine_support import (
    GOVERNED_DOMAINS,
    TEACHER_REVIEWED_STATUSES,
    _answer_ref,
    _disagreement,
    _extract_case_id,
    _teacher_payload,
    _teacher_review_status,
)
from .model_contracts.comparison_result import AdviserComparisonResult

__all__ = [
    "AdviserComparisonResult",
    "compare_many",
    "compare_teacher_and_candidate",
]

# Preserve the historical public class identity for repr/pickle/import contracts.
AdviserComparisonResult.__module__ = __name__


def compare_teacher_and_candidate(
    *,
    teacher_answer: Mapping[str, Any] | object,
    candidate_answer: Mapping[str, Any] | object,
    input_text: object = "",
    run_id: str = "run-not-recorded-pure-harness",
) -> dict[str, object]:
    """Compare supplied teacher and candidate answers without side effects.

    The teacher answer is not assumed to be ground truth unless its review status
    is human-reviewed or approved-as-gold. Candidate safety checks always run
    before disagreement interpretation.
    """

    case_id = _extract_case_id(teacher_answer, candidate_answer)
    teacher_ref = _answer_ref(teacher_answer, "teacher")
    candidate_ref = _answer_ref(candidate_answer, "candidate")
    report_id = f"comparison-{run_id}-{case_id}"

    disagreements: list[dict[str, object]] = []
    teacher_payload = _teacher_payload(teacher_answer)
    teacher_review_status = _teacher_review_status(teacher_answer)
    teacher_reviewed = teacher_review_status in TEACHER_REVIEWED_STATUSES

    if not teacher_reviewed:
        disagreements.append(_disagreement(
            field="teacher_answer.review_status",
            teacher_value=teacher_review_status,
            candidate_value="not_applicable",
            severity="medium",
            impact="teacher answer is draft evidence and must not be treated as ground truth",
            recommendation="queue human review before using this comparison as gold evidence",
        ))

    if not isinstance(candidate_answer, Mapping):
        disagreements.append(_disagreement(
            field="candidate_answer",
            teacher_value="mapping_expected",
            candidate_value=type(candidate_answer).__name__,
            severity="critical",
            impact="candidate output cannot be guarded or compared safely",
            recommendation="reject candidate output and keep Adviser advisory-only",
        ))
        return _final_result(
            report_id=report_id,
            run_id=run_id,
            case_id=case_id,
            teacher_ref=teacher_ref,
            candidate_ref=candidate_ref,
            disagreements=disagreements,
            teacher_review_status=teacher_review_status,
            candidate_guard_ok=False,
            resource_limits_ok=False,
        )

    resource_result = check_all_resource_limits(input_text=input_text, candidate_output=candidate_answer)
    if not resource_result.get("ok"):
        disagreements.append(_disagreement(
            field="candidate_answer.resource_limits",
            teacher_value="within_limits",
            candidate_value=list(resource_result.get("errors", [])),
            severity="high" if _candidate_domain(candidate_answer) in GOVERNED_DOMAINS else "medium",
            impact="candidate output exceeds offline Adviser resource limits",
            recommendation="reject or shrink candidate output before comparison trust",
        ))

    contract_result = validate_candidate_answer(candidate_answer)
    guard_result = guard_candidate_output(candidate_answer, input_text=str(input_text or ""))
    severity_result = evaluate_guard_result(guard_result, candidate_output=candidate_answer)
    if not guard_result.get("ok"):
        disagreements.append(_disagreement(
            field="candidate_answer.guard",
            teacher_value="guard_ok",
            candidate_value={
                "contract_errors": list(contract_result.get("errors", [])),
                "guard_errors": list(guard_result.get("errors", [])),
                "triggered_patterns": list(guard_result.get("triggered_patterns", [])),
            },
            severity=_severity_from_guard(severity_result),
            impact="candidate output failed advisory-only guard before comparison trust",
            recommendation="block promotion and route to human review",
        ))

    if isinstance(teacher_payload, Mapping):
        disagreements.extend(_compare_core_fields(teacher_payload, candidate_answer))
    else:
        disagreements.append(_disagreement(
            field="teacher_answer.answer",
            teacher_value=type(teacher_payload).__name__,
            candidate_value="mapping_expected",
            severity="medium",
            impact="teacher payload cannot be compared as structured Adviser evidence",
            recommendation="repair teacher answer before gold review",
        ))

    return _final_result(
        report_id=report_id,
        run_id=run_id,
        case_id=case_id,
        teacher_ref=teacher_ref,
        candidate_ref=candidate_ref,
        disagreements=disagreements,
        teacher_review_status=teacher_review_status,
        candidate_guard_ok=bool(guard_result.get("ok")),
        resource_limits_ok=bool(resource_result.get("ok")),
    )


def compare_many(
    cases: Sequence[Mapping[str, Any]],
    *,
    run_id: str = "run-not-recorded-pure-harness",
) -> list[dict[str, object]]:
    """Compare a sequence of supplied case mappings.

    Each case must already contain teacher_answer and candidate_answer. This
    function does not discover, load, or write cases.
    """

    results: list[dict[str, object]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, Mapping):
            results.append(compare_teacher_and_candidate(
                teacher_answer={},
                candidate_answer={},
                input_text="",
                run_id=f"{run_id}-invalid-case-{index}",
            ))
            continue
        results.append(compare_teacher_and_candidate(
            teacher_answer=case.get("teacher_answer", {}),
            candidate_answer=case.get("candidate_answer", {}),
            input_text=case.get("input_text", ""),
            run_id=str(case.get("run_id") or run_id),
        ))
    return results

