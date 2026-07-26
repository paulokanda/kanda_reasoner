from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.web_book_informed_surface_wiring_contract import (
    build_phase7_web_book_informed_surface_wiring_contract,
    evaluate_phase7_web_book_advisory_surface_wiring_request,
)


def test_phase7_web_book_research_contract_accepts_audit_and_blocks_authority():
    contract = build_phase7_web_book_informed_surface_wiring_contract()
    assert contract.feature_id == "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
    assert contract.reviewed_feature_id == "rss_ml_adv_phase6_guarded_runtime_advisory_display_completion_handoff_v1"
    assert contract.source_counts() == (7, 5)
    assert len(contract.gains) == 14
    codes = contract.gain_codes()
    assert "confusable_deputy_privilege_denial" in codes
    assert "structured_typed_payload_no_free_text_route_advice" in codes
    assert "eval_first_gates_for_code_payload_model_and_ui_changes" in codes
    assert "slo_error_budget_and_regression_budget_for_advisory_surface" in codes
    assert "latency_cost_and_availability_budget_before_provider_activation" in codes
    assert "route_influence_limited_to_future_deterministic_recheck_request_not_override" in codes
    assert "direct_ml_route_override" in contract.audit.rejected_or_deferred
    assert contract.direct_route_authority_allowed is False
    assert contract.runtime_panel_wired is False
    assert contract.provider_calls_allowed is False
    assert contract.router_final_selection_modified is False
    assert contract.persistence_allowed is False
    assert contract.critical_boundary_error_budget == 0


def test_phase7_web_book_wiring_decision_allows_read_only_design_not_route_effect():
    decision = evaluate_phase7_web_book_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        affect_route_choice=False,
    )
    assert decision.may_auto_use_after_router is True
    assert decision.may_show_visible_panel is True
    assert decision.may_affect_route_choice is False
    assert decision.required_next_contract == "phase_7_guarded_advisory_surface_wiring_contract_v1"
    assert "no route mutation" in decision.reason


def test_phase7_web_book_decision_blocks_direct_route_effect_provider_and_persistence():
    direct = evaluate_phase7_web_book_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        affect_route_choice=True,
    )
    assert direct.may_affect_route_choice is False
    assert direct.required_next_contract == "high_risk_route_authority_escalation_boundary_required_but_not_recommended"

    provider = evaluate_phase7_web_book_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        affect_route_choice=False,
        provider_backed=True,
    )
    assert provider.may_auto_use_after_router is False
    assert provider.required_next_contract == "provider_budgeted_adapter_boundary_required_before_activation"

    persistence = evaluate_phase7_web_book_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        affect_route_choice=False,
        persistent_logging=True,
    )
    assert persistence.may_show_visible_panel is False
    assert persistence.required_next_contract == "privacy_bounded_monitoring_contract_required_before_persistence"


if __name__ == "__main__":
    test_phase7_web_book_research_contract_accepts_audit_and_blocks_authority()
    test_phase7_web_book_wiring_decision_allows_read_only_design_not_route_effect()
    test_phase7_web_book_decision_blocks_direct_route_effect_provider_and_persistence()
    print("VALIDATION OK: phase7 web-and-book-informed advisory surface wiring research flux")
