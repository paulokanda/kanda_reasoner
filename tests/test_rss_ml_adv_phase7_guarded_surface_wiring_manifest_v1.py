import json
from pathlib import Path

PREFIX = "ml_advisory_phase7_guarded_advisory_surface_wiring_contract_v1_"


def main() -> None:
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))

    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
    assert manifest[PREFIX + "uses_web_book_research_flux"] is True
    assert manifest[PREFIX + "required_gain_count"] == 14
    assert len(manifest[PREFIX + "required_gain_codes"]) == 14
    assert manifest[PREFIX + "automatic_use_contract_defined"] is True
    assert manifest[PREFIX + "visible_panel_contract_defined"] is True
    assert manifest[PREFIX + "automatic_use_allowed_only_after_router_final_selection"] is True
    assert manifest[PREFIX + "requires_router_result_copy_unchanged"] is True
    assert manifest[PREFIX + "requires_guarded_display_payload"] is True
    assert manifest[PREFIX + "requires_no_free_text_route_advice"] is True
    assert manifest[PREFIX + "requires_kill_switch_and_rollback"] is True
    assert manifest[PREFIX + "route_effect_model"] == "direct_route_effect_blocked_future_deterministic_recheck_request_only"
    assert manifest[PREFIX + "contract_only"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0

    forbidden_false = (
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
        "prompt_registry_mutation_enabled",
        "prompt_library_read_enabled",
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
        "mlrt_113_created",
    )
    for suffix in forbidden_false:
        assert manifest[PREFIX + suffix] is False, suffix

    assert manifest[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract Result Review Gate v1"

    print("VALIDATION OK: phase7 guarded advisory surface wiring manifest gates")


if __name__ == "__main__":
    main()
