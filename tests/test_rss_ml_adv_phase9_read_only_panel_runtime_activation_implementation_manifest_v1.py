import json
from pathlib import Path

PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_v1_"
REQUIRED_FALSE = [
    "real_ml_enabled", "adapter_execution_enabled", "candidate_execution_enabled", "provider_calls_enabled",
    "network_calls_enabled", "api_keys_enabled", "embeddings_enabled", "vector_store_enabled",
    "persistence_enabled", "report_persistence_enabled", "prompt_loading_enabled", "prompt_registry_mutation_enabled",
    "prompt_library_read_enabled", "freeze_memory_read_enabled", "freeze_memory_write_enabled", "router_canon_read_enabled",
    "runtime_shadow_mode_enabled", "actual_runtime_panel_activation_enabled", "runtime_panel_activation_enabled",
    "renderer_activation_enabled", "mounted_panel_enabled", "runtime_ui_mutation_enabled", "runtime_telemetry_surface_wired",
    "router_prompt_logic_modified", "router_final_selection_modified", "route_influence_enabled", "route_authority_enabled",
    "router_calls_enabled", "advisor_calls_enabled", "advisory_rankings_enabled", "prompt_rankings_enabled",
    "free_text_route_advice_enabled", "free_text_explanations_enabled", "training_enabled", "calibration_enabled",
    "model_improvement_enabled", "runtime_pilot_behavior_enabled", "runtime_copilot_decision_behavior_enabled", "mlrt_113_created",
]


def test_phase9_runtime_activation_implementation_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_result_review_gate_v1"
    assert manifest[PREFIX + "runtime_activation_envelope_builder_enabled"] is True
    assert manifest[PREFIX + "feature_flag_required"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert manifest[PREFIX + "missing_view_model_behavior"] == "fail_open"
    assert manifest[PREFIX + "unsafe_view_model_behavior"] == "blocked_fail_open"
    assert manifest[PREFIX + "phase8_panel_view_model_input_only"] is True
    assert manifest[PREFIX + "renderer_adapter_separate_future_contract_required"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "in_memory_only"] is True
    assert manifest[PREFIX + "bounded"] is True
    assert manifest[PREFIX + "fail_open"] is True
    assert manifest[PREFIX + "removable_noop"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "renderer_neutral"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    for flag in REQUIRED_FALSE:
        assert manifest[PREFIX + flag] is False, flag
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase9_runtime_activation_implementation_manifest_gates()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation implementation manifest gates")
