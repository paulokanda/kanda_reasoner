from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    MockAdvisor,
    OfflineEvaluationStatus,
    build_phase3_synthetic_fixture_catalog,
    catalog_fixtures,
    run_offline_evaluation,
)


def test_phase3_catalog_builds_synthetic_in_memory_fixtures():
    catalog = build_phase3_synthetic_fixture_catalog()

    assert catalog.feature_id == "rss_ml_adv_phase3_offline_fixture_catalog_contract_v1"
    assert catalog.non_runtime is True
    assert catalog.non_authoritative is True
    assert len(catalog.entries) == 5
    assert len({entry.catalog_entry_id for entry in catalog.entries}) == 5
    assert all("synthetic_only" in entry.safety_scope_codes for entry in catalog.entries)
    assert all(
        entry.fixture.advisory_input.scenario_id == entry.fixture.fixture_id
        for entry in catalog.entries
    )


def test_phase3_catalog_feeds_phase2_harness_without_route_authority():
    catalog = build_phase3_synthetic_fixture_catalog()
    fixtures = catalog_fixtures(catalog)

    summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=fixtures,
        advisor_label="mock_advisor",
    )

    assert summary.total_fixtures == 5
    assert summary.invariant_pass_count == 4
    assert summary.rejected_variance_count == 1
    assert summary.fail_open_count == 0
    statuses = tuple(result.status for result in summary.results)
    assert statuses.count(OfflineEvaluationStatus.PASSED) == 4
    assert statuses.count(OfflineEvaluationStatus.REJECTED_ROUTE_VARIANCE) == 1
    assert all("governed_choice" in item.governed_decision_before_advisory for item in fixtures)


def test_phase3_catalog_expected_statuses_match_harness_statuses():
    catalog = build_phase3_synthetic_fixture_catalog()
    summary = run_offline_evaluation(
        advisor=MockAdvisor(),
        fixtures=catalog_fixtures(catalog),
        advisor_label="mock_advisor",
    )

    expected_by_id = {
        entry.fixture.fixture_id: entry.expected_status for entry in catalog.entries
    }
    for result in summary.results:
        assert result.status == expected_by_id[result.fixture_id]
