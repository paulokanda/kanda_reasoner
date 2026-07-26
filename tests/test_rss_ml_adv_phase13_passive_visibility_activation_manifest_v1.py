import json
from pathlib import Path


PREFIX = "ml_advisory_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'actual_host_binding_enabled', 'host_binding_activation_enabled', 'actual_runtime_app_host_visibility_enabled', 'runtime_app_host_visibility_activation_enabled', 'visibility_activation_enabled', 'actual_passive_visibility_activation_enabled', 'passive_visibility_activation_enabled', 'passive_visibility_slot_registered', 'passive_visibility_slot_mutated', 'mounted_runtime_panel_enabled', 'runtime_panel_mount_side_effects_enabled', 'host_event_subscription_enabled', 'host_callback_registration_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'autonomous_ml_router_enabled', 'visible_ml_integration_complete', 'actual_visible_panel_host_bound', 'mlrt_113_created']


def test_phase13_passive_visibility_activation_contract_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1"
    assert manifest[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract v1"
    assert manifest[PREFIX + "status"] == "contract_only_future_passive_visibility_activation_boundary"
    assert manifest[PREFIX + "source_completion_handoff_feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_completion_handoff_v1"
    assert manifest[PREFIX + "source_runtime_app_host_visibility_implementation_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"
    assert manifest[PREFIX + "phase12_runtime_app_host_visibility_descriptor_input_required"] is True
    assert manifest[PREFIX + "contract_only"] is True
    assert manifest[PREFIX + "future_passive_visibility_activation_contract_ready"] is True
    assert manifest[PREFIX + "feature_flag_required"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert manifest[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert manifest[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert manifest[PREFIX + "bounded_passive_visibility_input_required"] is True
    assert manifest[PREFIX + "bounded_passive_visibility_output_required"] is True
    assert manifest[PREFIX + "read_only_passive_visibility_slot_required"] is True
    assert manifest[PREFIX + "removable_noop"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0
    assert manifest[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract Result Review Gate v1"
    for flag in REQUIRED_FALSE:
        assert manifest[PREFIX + flag] is False, flag


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_contract_manifest_gates()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation contract manifest gates")
