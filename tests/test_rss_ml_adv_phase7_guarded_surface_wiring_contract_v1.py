from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.guarded_advisory_surface_wiring_contract import (
    REQUIRED_GAIN_CODES,
    SurfaceVisibilityMode,
    build_phase7_guarded_advisory_surface_wiring_contract,
    evaluate_phase7_guarded_advisory_surface_wiring_request,
)


def main() -> None:
    contract = build_phase7_guarded_advisory_surface_wiring_contract()
    policy = contract.policy

    assert contract.feature_id == "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_v1"
    assert contract.source_research_feature_id == "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
    assert contract.research_gain_count == 14
    assert policy.required_gain_codes == REQUIRED_GAIN_CODES
    assert SurfaceVisibilityMode.FUTURE_PANEL_READ_ONLY in policy.allowed_visibility_modes

    assert policy.contract_only is True
    assert policy.automatic_use_contract_defined is True
    assert policy.visible_panel_contract_defined is True
    assert policy.must_run_after_canonical_router_final_selection is True
    assert policy.requires_router_result_copy_unchanged is True
    assert policy.requires_already_computed_advisory_output is True
    assert policy.requires_guarded_display_payload is True
    assert policy.requires_typed_bounded_fields is True
    assert policy.requires_no_free_text_route_advice is True
    assert policy.requires_uncertainty_status_role_scope_labels is True
    assert policy.requires_disable_noop_control is True
    assert policy.requires_non_training_feedback_slot is True
    assert policy.requires_eval_first_gate_before_future_implementation is True
    assert policy.requires_slo_error_budget_before_activation is True
    assert policy.requires_latency_cost_availability_budget_before_provider_activation is True
    assert policy.requires_kill_switch_and_rollback is True

    assert policy.read_only is True
    assert policy.telemetry_only is True
    assert policy.route_invariant is True
    assert policy.in_memory_only is True
    assert policy.bounded is True
    assert policy.fail_open is True
    assert policy.removable_noop is True
    assert policy.final_selection_invisible is True
    assert policy.non_authoritative is True
    assert policy.critical_boundary_error_budget == 0

    forbidden_fields = (
        "real_ml_enabled",
        "adapter_execution_enabled",
        "candidate_execution_enabled",
        "provider_calls_enabled",
        "network_calls_enabled",
        "api_keys_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "report_persistence_enabled",
        "prompt_loading_enabled",
        "prompt_library_read_enabled",
        "prompt_registry_mutation_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "runtime_shadow_mode_enabled",
        "runtime_advisory_panel_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wired",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
    )
    for field in forbidden_fields:
        assert getattr(policy, field) is False, field

    decision = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
    )
    assert decision.may_define_auto_use_contract is True
    assert decision.may_define_visible_panel_contract is True
    assert decision.may_activate_runtime_wiring is False
    assert decision.may_show_runtime_panel is False
    assert decision.may_affect_route_choice is False
    assert decision.required_next_step == "phase_7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"

    activation = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        activate_runtime_wiring=True,
    )
    assert activation.may_activate_runtime_wiring is False
    assert activation.may_show_runtime_panel is False
    assert "implementation_contract" in activation.required_next_step

    direct_route = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        affect_route_choice=True,
    )
    assert direct_route.may_define_auto_use_contract is False
    assert direct_route.may_affect_route_choice is False
    assert "deterministic_recheck" in direct_route.required_next_step

    provider = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=True,
        provider_backed=True,
    )
    assert provider.may_define_auto_use_contract is False
    assert "provider_budgeted_adapter_boundary" in provider.required_next_step

    persistent = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=True,
        visible_panel=False,
        persistent_logging=True,
    )
    assert persistent.may_define_auto_use_contract is False
    assert "privacy_bounded_monitoring" in persistent.required_next_step

    ui_mutation = evaluate_phase7_guarded_advisory_surface_wiring_request(
        auto_use_after_router=False,
        visible_panel=True,
        ui_mutation=True,
    )
    assert ui_mutation.may_define_visible_panel_contract is False
    assert "ui_mutation_contract" in ui_mutation.required_next_step

    print("VALIDATION OK: phase7 guarded advisory surface wiring contract")


if __name__ == "__main__":
    main()
