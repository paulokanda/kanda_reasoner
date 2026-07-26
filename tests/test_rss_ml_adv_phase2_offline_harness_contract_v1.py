from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    AdvisoryFlag,
    AdvisoryInput,
    MockAdvisor,
    NullAdvisor,
    OfflineEvaluationFixture,
    OfflineEvaluationStatus,
    run_offline_evaluation,
)


def _fixture(fixture_id, ambiguity, conflict, decision="route_canon_safe"):
    return OfflineEvaluationFixture(
        fixture_id=fixture_id,
        advisory_input=AdvisoryInput(
            scenario_id=fixture_id,
            sanitized_context_hash="hash_" + fixture_id,
            candidate_prompt_group_ids=("07_prompt_authoring_and_audit", "03_governance_freeze_and_handoff"),
            ambiguity_score=ambiguity,
            conflict_score=conflict,
            risk_family_id="prompt_gap" if ambiguity > 0.7 else None,
        ),
        governed_decision_before_advisory=decision,
        governed_decision_after_advisory=decision,
    )


def test_phase2_null_advisor_evaluates_in_memory_and_abstains():
    summary = run_offline_evaluation(
        advisor=NullAdvisor(),
        fixtures=(_fixture("fx_null_001", 0.1, 0.0),),
        advisor_label="null_advisor",
    )

    assert summary.feature_id == "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1"
    assert summary.total_fixtures == 1
    assert summary.invariant_pass_count == 1
    assert summary.fail_open_count == 0
    assert summary.rejected_variance_count == 0
    assert summary.results[0].advisor_abstained is True
    assert summary.results[0].status == OfflineEvaluationStatus.PASSED


def test_phase2_mock_advisor_returns_telemetry_without_route_change():
    summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=(
            _fixture("fx_mock_001", 0.8, 0.1),
            _fixture("fx_mock_002", 0.2, 0.9),
        ),
        advisor_label="mock_advisor",
    )

    assert summary.total_fixtures == 2
    assert summary.invariant_pass_count == 2
    assert summary.fail_open_count == 0
    assert summary.rejected_variance_count == 0
    flags = summary.results[0].advisory_output.advisory_flags
    assert AdvisoryFlag.AMBIGUITY_DETECTED in flags
    assert all(result.route_invariant for result in summary.results)


def test_phase2_rejects_route_variance_but_does_not_choose_route():
    fixture = OfflineEvaluationFixture(
        fixture_id="fx_variance_001",
        advisory_input=AdvisoryInput(
            scenario_id="fx_variance_001",
            sanitized_context_hash="hash_variance",
            candidate_prompt_group_ids=("07_prompt_authoring_and_audit",),
            ambiguity_score=0.9,
            conflict_score=0.9,
        ),
        governed_decision_before_advisory="route_a",
        governed_decision_after_advisory="route_b",
    )

    summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=(fixture,),
        advisor_label="mock_advisor",
    )

    assert summary.total_fixtures == 1
    assert summary.invariant_pass_count == 0
    assert summary.rejected_variance_count == 1
    assert summary.results[0].status == OfflineEvaluationStatus.REJECTED_ROUTE_VARIANCE


def test_phase2_fail_open_when_advisor_raises():
    class BrokenAdvisor:
        def advise(self, advisory_input):
            del advisory_input
            raise RuntimeError("simulated advisor failure")

    summary = run_offline_evaluation(
        advisor=BrokenAdvisor(),
        fixtures=(_fixture("fx_fail_open_001", 0.4, 0.4),),
        advisor_label="broken_advisor",
    )

    assert summary.total_fixtures == 1
    assert summary.fail_open_count == 1
    assert summary.results[0].status == OfflineEvaluationStatus.FAIL_OPEN_ABSTAINED
    assert summary.results[0].advisor_abstained is True
