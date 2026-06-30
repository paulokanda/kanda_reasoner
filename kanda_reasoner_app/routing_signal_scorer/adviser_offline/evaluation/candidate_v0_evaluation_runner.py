# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/candidate_v0_evaluation_runner.py
"""Pure offline evaluation runner for Adviser Candidate v0.

The runner compares caller-supplied seed-gold case dictionaries with the
standard-library-only lexical Adviser candidate. It returns an in-memory report
for human review and promotion analysis.

Authority boundary:
- adviser-offline only;
- pure over caller-supplied case dictionaries;
- no file reads or writes;
- no source scanning;
- no prompt auto-loading;
- no artifact generation or persistence;
- no candidate-output persistence;
- no registry writer or scratch writer;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = ['evaluate_candidate_v0_against_gold_cases', 'EvaluationCaseResult']
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.candidate_v0.offline_lexical_scorer import (
    CANDIDATE_ID,
    CANDIDATE_VERSION,
    build_candidate_answer,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_output_guard import guard_candidate_output
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_resource_limits import check_all_resource_limits
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_severity import evaluate_guard_result

FEATURE_ID = "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1"
SCHEMA_VERSION = "3.53-adviser-candidate-v0-evaluation-runner"
AUTHORITY_STATEMENT = "advisory_only"
REPORT_KIND = "in_memory_offline_evaluation_evidence_only"
MAX_EVALUATION_CASES = 500
SAFE_NO_ACTION_VALUES = frozenset({"NO", "ABSTAIN", "UNKNOWN"})
UNSAFE_PROCEED_VALUES = frozenset({"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})

CandidateBuilder = Callable[..., Mapping[str, Any]]


@dataclass(frozen=True)
class EvaluationCaseResult:
    """In-memory per-case evaluation result."""

    case_id: str
    gold_case_id: str
    case_family: str
    candidate_guard_ok: bool
    resource_limits_ok: bool
    severity: str
    critical_failure: bool
    promotion_blocker: bool
    path_match: bool
    required_prompt_groups_match: bool
    risk_flag_overlap: bool
    must_not_permit_action_alignment: bool
    review_required: bool
    candidate_governance_domain: str
    candidate_path_recommendation: str
    candidate_advisory_proceed_recommendation: str
    expected_governance_path: str
    expected_required_prompt_groups: tuple[str, ...]
    expected_risk_flags: tuple[str, ...]
    notes: tuple[str, ...]
    authority_statement: str = AUTHORITY_STATEMENT

    def to_dict(self) -> dict[str, object]:
        """Support to dict behavior.
        
        Returns
        -------
        dict[str, object]
            The mapped values.
        """
        
        return {
            "case_id": self.case_id,
            "gold_case_id": self.gold_case_id,
            "case_family": self.case_family,
            "candidate_guard_ok": self.candidate_guard_ok,
            "resource_limits_ok": self.resource_limits_ok,
            "severity": self.severity,
            "critical_failure": self.critical_failure,
            "promotion_blocker": self.promotion_blocker,
            "path_match": self.path_match,
            "required_prompt_groups_match": self.required_prompt_groups_match,
            "risk_flag_overlap": self.risk_flag_overlap,
            "must_not_permit_action_alignment": self.must_not_permit_action_alignment,
            "review_required": self.review_required,
            "candidate_governance_domain": self.candidate_governance_domain,
            "candidate_path_recommendation": self.candidate_path_recommendation,
            "candidate_advisory_proceed_recommendation": self.candidate_advisory_proceed_recommendation,
            "expected_governance_path": self.expected_governance_path,
            "expected_required_prompt_groups": list(self.expected_required_prompt_groups),
            "expected_risk_flags": list(self.expected_risk_flags),
            "notes": list(self.notes),
            "authority_statement": self.authority_statement,
        }


def evaluate_candidate_v0_against_gold_cases(
    gold_cases: Iterable[Mapping[str, Any]],
    *,
    run_id: str = "m12-run-not-recorded",
    candidate_builder: CandidateBuilder = build_candidate_answer,
) -> dict[str, object]:
    """Evaluate Candidate v0 against caller-supplied seed-gold cases.

    The function does not discover cases, load files, write reports, mutate gold
    sets, or register runs. It returns a structured in-memory report only.
    """

    materialized = [case for case in gold_cases]
    if len(materialized) > MAX_EVALUATION_CASES:
        raise ValueError(f"gold_cases exceeds {MAX_EVALUATION_CASES} case limit")

    case_results: list[dict[str, object]] = []
    for index, gold_case in enumerate(materialized):
        if not isinstance(gold_case, Mapping):
            case_results.append(_invalid_case(index, "case must be a mapping"))
            continue
        case_results.append(_evaluate_one(gold_case, run_id=run_id, candidate_builder=candidate_builder).to_dict())

    aggregate = _aggregate(case_results)
    return {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "authority_statement": AUTHORITY_STATEMENT,
        "report_kind": REPORT_KIND,
        "run_id": str(run_id),
        "candidate_id": CANDIDATE_ID,
        "candidate_version": CANDIDATE_VERSION,
        "input_source_policy": "caller_supplied_cases_only_no_case_discovery",
        "output_policy": "in_memory_report_only_no_persistence",
        "router_authority": "none",
        "gold_mutation": "forbidden",
        "aggregate": aggregate,
        "case_results": case_results,
    }


def _evaluate_one(gold_case: Mapping[str, Any], *, run_id: str, candidate_builder: CandidateBuilder) -> EvaluationCaseResult:
    """Support evaluate one behavior.
    
    Parameters
    ----------
    gold_case : Mapping[str, Any]
        The gold case value.
    run_id : str
        The run id value.
    candidate_builder : CandidateBuilder
        The candidate builder value.
    
    Returns
    -------
    EvaluationCaseResult
        The evaluation case result result.
    """
    
    input_text = str(gold_case.get("input_text", ""))
    case_id = str(gold_case.get("case_id") or gold_case.get("gold_case_id") or "case-not-recorded")
    gold_case_id = str(gold_case.get("gold_case_id") or case_id)
    case_family = str(gold_case.get("case_family") or "unknown")

    notes: list[str] = []
    candidate = dict(candidate_builder(input_text=input_text, case_id=case_id, run_id=run_id))
    resource = check_all_resource_limits(input_text=input_text, candidate_output=candidate)
    guard = guard_candidate_output(candidate, input_text=input_text)
    severity = evaluate_guard_result(guard, candidate_output=candidate)

    if not bool(guard.get("ok")):
        notes.append("candidate_guard_failed")
    if not bool(resource.get("ok")):
        notes.append("resource_limits_failed")

    expected_path = str(gold_case.get("expected_governance_path") or "")
    candidate_path = str(candidate.get("path_recommendation") or "")
    path_match = _same_token(expected_path, candidate_path)
    if not path_match:
        notes.append("path_recommendation_differs_from_seed_gold")

    expected_groups = tuple(_as_strings(gold_case.get("expected_required_prompt_groups")))
    candidate_groups = tuple(_as_strings(candidate.get("required_prompt_groups")))
    groups_match = set(expected_groups) == set(candidate_groups)
    if not groups_match:
        notes.append("required_prompt_groups_differ_from_seed_gold")

    expected_flags = tuple(_as_strings(gold_case.get("expected_risk_flags")))
    candidate_flags = tuple(_as_strings(_risk_flags(candidate)))
    risk_overlap = bool(set(expected_flags).intersection(candidate_flags)) if expected_flags else not candidate_flags
    if not risk_overlap:
        notes.append("risk_flags_do_not_overlap_seed_gold")

    expected_no_action = bool(gold_case.get("expected_must_not_permit_action"))
    candidate_proceed = str(candidate.get("advisory_proceed_recommendation") or "UNKNOWN")
    if expected_no_action:
        no_action_alignment = candidate_proceed in SAFE_NO_ACTION_VALUES
    else:
        no_action_alignment = candidate_proceed not in UNSAFE_PROCEED_VALUES
    if not no_action_alignment:
        notes.append("must_not_permit_action_alignment_failed")

    critical_failure = bool(severity.get("critical_failure")) or candidate_proceed in UNSAFE_PROCEED_VALUES
    promotion_blocker = bool(severity.get("promotion_blocker")) or critical_failure
    review_required = any(
        (
            not bool(guard.get("ok")),
            not bool(resource.get("ok")),
            critical_failure,
            not path_match,
            not groups_match,
            not risk_overlap,
            not no_action_alignment,
        )
    )

    return EvaluationCaseResult(
        case_id=case_id,
        gold_case_id=gold_case_id,
        case_family=case_family,
        candidate_guard_ok=bool(guard.get("ok")),
        resource_limits_ok=bool(resource.get("ok")),
        severity=str(severity.get("severity") or "P4_INFO"),
        critical_failure=critical_failure,
        promotion_blocker=promotion_blocker,
        path_match=path_match,
        required_prompt_groups_match=groups_match,
        risk_flag_overlap=risk_overlap,
        must_not_permit_action_alignment=no_action_alignment,
        review_required=review_required,
        candidate_governance_domain=str(candidate.get("governance_domain") or "unknown"),
        candidate_path_recommendation=candidate_path,
        candidate_advisory_proceed_recommendation=candidate_proceed,
        expected_governance_path=expected_path,
        expected_required_prompt_groups=expected_groups,
        expected_risk_flags=expected_flags,
        notes=tuple(notes),
    )


def _invalid_case(index: int, message: str) -> dict[str, object]:
    """Support invalid case behavior.
    
    Parameters
    ----------
    index : int
        The index value.
    message : str
        The message text.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    return {
        "case_id": f"invalid-case-{index}",
        "gold_case_id": f"invalid-case-{index}",
        "case_family": "invalid",
        "candidate_guard_ok": False,
        "resource_limits_ok": False,
        "severity": "P1_HIGH",
        "critical_failure": False,
        "promotion_blocker": True,
        "path_match": False,
        "required_prompt_groups_match": False,
        "risk_flag_overlap": False,
        "must_not_permit_action_alignment": False,
        "review_required": True,
        "candidate_governance_domain": "invalid",
        "candidate_path_recommendation": "invalid",
        "candidate_advisory_proceed_recommendation": "UNKNOWN",
        "expected_governance_path": "unknown",
        "expected_required_prompt_groups": [],
        "expected_risk_flags": [],
        "notes": [message],
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _aggregate(case_results: list[Mapping[str, Any]]) -> dict[str, object]:
    """Support aggregate behavior.
    
    Parameters
    ----------
    case_results : list[Mapping[str, Any]]
        The case results value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    total = len(case_results)
    guard_failures = _count_false(case_results, "candidate_guard_ok")
    resource_failures = _count_false(case_results, "resource_limits_ok")
    critical_failures = _count_true(case_results, "critical_failure")
    promotion_blockers = _count_true(case_results, "promotion_blocker")
    review_required = _count_true(case_results, "review_required")

    return {
        "total_cases": total,
        "guard_failures": guard_failures,
        "resource_failures": resource_failures,
        "critical_failures": critical_failures,
        "promotion_blockers": promotion_blockers,
        "review_required_cases": review_required,
        "path_match_count": _count_true(case_results, "path_match"),
        "required_prompt_groups_match_count": _count_true(case_results, "required_prompt_groups_match"),
        "risk_flag_overlap_count": _count_true(case_results, "risk_flag_overlap"),
        "must_not_permit_action_alignment_count": _count_true(case_results, "must_not_permit_action_alignment"),
        "promotion_recommendation": _promotion_recommendation(
            total=total,
            guard_failures=guard_failures,
            resource_failures=resource_failures,
            critical_failures=critical_failures,
            review_required=review_required,
        ),
        "authority_statement": AUTHORITY_STATEMENT,
    }


def _promotion_recommendation(*, total: int, guard_failures: int, resource_failures: int, critical_failures: int, review_required: int) -> str:
    """Support promotion recommendation behavior.
    
    Parameters
    ----------
    total : int
        The total value.
    guard_failures : int
        The guard failures value.
    resource_failures : int
        The resource failures value.
    critical_failures : int
        The critical failures value.
    review_required : int
        The review required value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if total == 0:
        return "blocked_no_cases_supplied"
    if guard_failures or resource_failures or critical_failures:
        return "blocked_safety_failures_require_human_review"
    if review_required:
        return "blocked_candidate_v0_mismatches_require_human_review"
    return "eligible_for_next_offline_review_gate_not_runtime_authority"


def _count_true(items: list[Mapping[str, Any]], key: str) -> int:
    """Support count true behavior.
    
    Parameters
    ----------
    items : list[Mapping[str, Any]]
        The item values.
    key : str
        The key value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return sum(1 for item in items if bool(item.get(key)))


def _count_false(items: list[Mapping[str, Any]], key: str) -> int:
    """Support count false behavior.
    
    Parameters
    ----------
    items : list[Mapping[str, Any]]
        The item values.
    key : str
        The key value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return sum(1 for item in items if not bool(item.get(key)))


def _as_strings(value: object) -> list[str]:
    """Support as strings behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if isinstance(value, (str, bytes, bytearray)):
        return [str(value)] if value else []
    if isinstance(value, Iterable):
        return [str(item) for item in value if str(item)]
    return []


def _risk_flags(candidate: Mapping[str, Any]) -> list[str]:
    """Support risk flags behavior.
    
    Parameters
    ----------
    candidate : Mapping[str, Any]
        The candidate value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    risk = candidate.get("risk_assessment")
    if isinstance(risk, Mapping):
        return _as_strings(risk.get("flags"))
    return []


def _same_token(left: object, right: object) -> bool:
    """Support same token behavior.
    
    Parameters
    ----------
    left : object
        The left value.
    right : object
        The right value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return _normalize_token(left) == _normalize_token(right)


def _normalize_token(value: object) -> str:
    """Support normalize token behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
