import json
from pathlib import Path

FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_completion_handoff_v1"
PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_completion_handoff_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_panel_activation_enabled', 'runtime_advisory_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'renderer_activation_enabled', 'mounted_panel_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'visible_panel_runtime_enabled', 'mlrt_113_created']


def test_phase8_panel_ui_completion_handoff_manifest_gates():
    manifest = json.loads(
        Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json")
        .read_text(encoding="utf-8")
    )
    assert manifest[PREFIX + "feature_id"] == FEATURE_ID
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase8_read_only_advisory_panel_ui_final_safety_gate_v1"
    assert manifest[PREFIX + "completion_handoff_only"] is True
    assert manifest[PREFIX + "phase8_read_only_panel_ui_path_completed"] is True
    assert manifest[PREFIX + "safe_completed_state"] == "dormant_renderer_neutral_bounded_in_memory_read_only_panel_view_model_foundation_only"
    assert manifest[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Contract v1"
    assert manifest[PREFIX + "governed_router_remains_final_selector"] is True
    assert manifest[PREFIX + "ml_advisory_signal_telemetry_only"] is True
    assert manifest[PREFIX + "manual_prompt_code_hint_classification_help_only"] is True
    assert manifest[PREFIX + "governed_prompt_intake_only_safe_door"] is True
    assert manifest[PREFIX + "phase7_surface_envelope_input_only"] is True
    assert manifest[PREFIX + "display_only_canonical_identifiers_only"] is True
    assert manifest[PREFIX + "bounded_typed_panel_sections_only"] is True
    assert manifest[PREFIX + "advisory_role_label_required"] is True
    assert manifest[PREFIX + "canonical_route_unchanged_label_required"] is True
    assert manifest[PREFIX + "no_route_authority_label_required"] is True
    assert manifest[PREFIX + "confidence_not_correctness_label_required"] is True
    assert manifest[PREFIX + "non_training_feedback_slot_preserved"] is True
    assert manifest[PREFIX + "renderer_neutral"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "in_memory_only"] is True
    assert manifest[PREFIX + "bounded"] is True
    assert manifest[PREFIX + "fail_open"] is True
    assert manifest[PREFIX + "removable_noop"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0
    for flag in REQUIRED_FALSE:
        assert manifest[PREFIX + flag] is False, flag


if __name__ == "__main__":
    test_phase8_panel_ui_completion_handoff_manifest_gates()
    print("VALIDATION OK: phase8 read-only advisory panel UI completion handoff manifest gates")
