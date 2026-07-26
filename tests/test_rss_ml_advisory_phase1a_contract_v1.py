from __future__ import annotations

from dataclasses import FrozenInstanceError

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    AdvisoryFlag,
    AdvisoryInput,
    AdvisoryReasonCode,
    BoundaryStatus,
    MockAdvisor,
    NullAdvisor,
)

FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"


def test_advisory_contracts_are_frozen_and_non_authoritative() -> None:
    advisory_input = AdvisoryInput(
        scenario_id="case-001",
        sanitized_context_hash="hash-001",
        candidate_prompt_group_ids=("07_prompt_authoring_and_audit", "03_governance_freeze_and_handoff"),
        ambiguity_score=0.75,
        conflict_score=0.65,
        risk_family_id="prompt_gap",
    )
    advisor = MockAdvisor()
    output = advisor.advise(advisory_input)

    assert AdvisoryFlag.AMBIGUITY_DETECTED in output.advisory_flags
    assert AdvisoryFlag.CONFLICT_DETECTED in output.advisory_flags
    assert AdvisoryFlag.PROMPT_GAP_DETECTED in output.advisory_flags
    assert AdvisoryReasonCode.MOCK_DETERMINISTIC_RULE in output.advisory_reason_codes
    assert output.boundary_status is BoundaryStatus.SAFE_NON_AUTHORITATIVE
    assert output.is_mock is True
    assert output.advisory_should_abstain is False

    try:
        output.non_authoritative_confidence = 1.0  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("AdvisoryOutput must be frozen")


def test_null_advisor_abstains_without_route_authority() -> None:
    advisory_input = AdvisoryInput(
        scenario_id="case-002",
        sanitized_context_hash="hash-002",
        candidate_prompt_group_ids=(),
        ambiguity_score=0.0,
        conflict_score=0.0,
        risk_family_id=None,
    )
    output = NullAdvisor().advise(advisory_input)

    assert output.advisory_should_abstain is True
    assert AdvisoryFlag.ABSTAINED in output.advisory_flags
    assert output.boundary_status is BoundaryStatus.ABSTAINED
    assert output.is_mock is False


def test_contract_validation_rejects_invalid_scores_and_empty_ids() -> None:
    for kwargs in (
        dict(
            scenario_id="",
            sanitized_context_hash="hash",
            candidate_prompt_group_ids=(),
            ambiguity_score=0.0,
            conflict_score=0.0,
        ),
        dict(
            scenario_id="case",
            sanitized_context_hash="hash",
            candidate_prompt_group_ids=(),
            ambiguity_score=1.1,
            conflict_score=0.0,
        ),
    ):
        try:
            AdvisoryInput(**kwargs)
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError("Invalid AdvisoryInput was accepted")


if __name__ == "__main__":
    test_advisory_contracts_are_frozen_and_non_authoritative()
    test_null_advisor_abstains_without_route_authority()
    test_contract_validation_rejects_invalid_scores_and_empty_ids()
    print(f"VALIDATION OK: {FEATURE_ID}")
