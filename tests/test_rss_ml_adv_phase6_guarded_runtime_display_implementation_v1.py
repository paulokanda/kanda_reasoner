from dataclasses import fields

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    AdvisoryFlag,
    AdvisoryInput,
    AdvisoryReasonCode,
    BoundaryStatus,
    GuardedRuntimeAdvisoryDisplayPayload,
    GuardedRuntimeAdvisoryDisplaySurfacePolicy,
    MockAdvisor,
    build_guarded_runtime_advisory_display_payload,
    build_phase6_guarded_runtime_display_payload_probe,
)


FEATURE_ID = (
    "rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_v1"
)


def test_phase6_display_payload_probe_is_read_only_telemetry_only():
    payload = build_phase6_guarded_runtime_display_payload_probe()

    assert isinstance(payload, GuardedRuntimeAdvisoryDisplayPayload)
    assert payload.feature_id == FEATURE_ID
    assert payload.read_only is True
    assert payload.telemetry_only is True
    assert payload.route_invariant is True
    assert payload.final_selection_invisible is True
    assert payload.non_authoritative is True
    assert payload.removable_noop is True
    assert payload.runtime_display_implementation_enabled is True
    assert payload.runtime_telemetry_payload_builder_enabled is True
    assert payload.runtime_advisory_panel_enabled is False
    assert payload.runtime_ui_mutation_enabled is False
    assert payload.router_prompt_logic_modified is False
    assert payload.router_final_selection_modified is False
    assert payload.route_authority_enabled is False
    assert payload.advisory_rankings_enabled is False
    assert payload.free_text_explanations_enabled is False
    assert payload.runtime_copilot_behavior_enabled is False
    assert payload.boundary_status == BoundaryStatus.SAFE_NON_AUTHORITATIVE
    assert AdvisoryFlag.AMBIGUITY_DETECTED in payload.advisory_flags
    assert AdvisoryReasonCode.MULTIPLE_CANDIDATE_GROUPS in (
        payload.advisory_reason_codes
    )


def test_phase6_display_payload_has_no_route_or_prompt_selection_fields():
    payload_fields = {field.name for field in fields(GuardedRuntimeAdvisoryDisplayPayload)}
    forbidden = {
        "route",
        "selected_route",
        "final_route",
        "selected_prompt",
        "final_prompt",
        "winner",
        "ranking",
        "rankings",
        "override",
        "prompt_group_id",
        "advisory_group_observations",
    }
    assert payload_fields.isdisjoint(forbidden)


def test_phase6_display_payload_is_bounded_and_reports_truncation():
    policy = GuardedRuntimeAdvisoryDisplaySurfacePolicy(
        surface_id="bounded_payload_test",
        display_label="bounded_payload_test",
        source_feature_id=FEATURE_ID,
        allowed_field_codes=("advisory_flags", "advisory_reason_codes"),
        allowed_failure_state_codes=("display_payload_truncated",),
        max_flags=1,
        max_reason_codes=1,
    )
    advisory_input = AdvisoryInput(
        scenario_id="bounded_payload_case",
        sanitized_context_hash="bounded_hash",
        candidate_prompt_group_ids=("synthetic_group_alpha",),
        ambiguity_score=0.80,
        conflict_score=0.80,
        risk_family_id="prompt_gap",
    )
    output = MockAdvisor().advise(advisory_input)
    payload = build_guarded_runtime_advisory_display_payload(policy, output)

    assert len(payload.advisory_flags) == 1
    assert len(payload.advisory_reason_codes) == 1
    assert "display_payload_truncated" in payload.display_failure_state_codes
    assert payload.route_authority_enabled is False


def test_phase6_display_policy_rejects_forbidden_authority():
    try:
        GuardedRuntimeAdvisoryDisplaySurfacePolicy(
            surface_id="bad_policy",
            display_label="bad_policy",
            source_feature_id=FEATURE_ID,
            allowed_field_codes=("advisory_flags",),
            allowed_failure_state_codes=("boundary_rejected",),
            route_authority_enabled=True,
        )
    except ValueError as exc:
        assert "route_authority_enabled" in str(exc)
    else:
        raise AssertionError("route authority must be rejected")


if __name__ == "__main__":
    test_phase6_display_payload_probe_is_read_only_telemetry_only()
    test_phase6_display_payload_has_no_route_or_prompt_selection_fields()
    test_phase6_display_payload_is_bounded_and_reports_truncation()
    test_phase6_display_policy_rejects_forbidden_authority()
    print("VALIDATION OK: phase6 display implementation contract tests")
