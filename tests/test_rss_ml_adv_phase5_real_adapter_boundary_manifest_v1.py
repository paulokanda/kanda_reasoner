import json
from pathlib import Path

MANIFEST = Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json")
FEATURE_ID = "rss_ml_adv_phase5_offline_real_adapter_boundary_contract_v1"

FALSE_KEYS = (
    "ml_advisory_phase5_real_adapter_boundary_mlrt113_created",
    "ml_advisory_phase5_real_adapter_boundary_real_ml_enabled",
    "ml_advisory_phase5_real_adapter_boundary_provider_calls_enabled",
    "ml_advisory_phase5_real_adapter_boundary_network_calls_enabled",
    "ml_advisory_phase5_real_adapter_boundary_api_keys_enabled",
    "ml_advisory_phase5_real_adapter_boundary_embeddings_enabled",
    "ml_advisory_phase5_real_adapter_boundary_vector_store_enabled",
    "ml_advisory_phase5_real_adapter_boundary_persistence_enabled",
    "ml_advisory_phase5_real_adapter_boundary_report_persistence_enabled",
    "ml_advisory_phase5_real_adapter_boundary_prompt_loading_enabled",
    "ml_advisory_phase5_real_adapter_boundary_prompt_registry_mutation_enabled",
    "ml_advisory_phase5_real_adapter_boundary_prompt_library_read_enabled",
    "ml_advisory_phase5_real_adapter_boundary_freeze_memory_read_enabled",
    "ml_advisory_phase5_real_adapter_boundary_freeze_memory_write_enabled",
    "ml_advisory_phase5_real_adapter_boundary_router_canon_read_enabled",
    "ml_advisory_phase5_real_adapter_boundary_runtime_shadow_mode_enabled",
    "ml_advisory_phase5_real_adapter_boundary_router_prompt_logic_modified",
    "ml_advisory_phase5_real_adapter_boundary_router_final_selection_modified",
    "ml_advisory_phase5_real_adapter_boundary_route_authority_enabled",
    "ml_advisory_phase5_real_adapter_boundary_advisory_rankings_enabled",
    "ml_advisory_phase5_real_adapter_boundary_free_text_explanations_enabled",
    "ml_advisory_phase5_real_adapter_boundary_training_enabled",
    "ml_advisory_phase5_real_adapter_boundary_calibration_enabled",
    "ml_advisory_phase5_real_adapter_boundary_model_improvement_enabled",
    "ml_advisory_phase5_real_adapter_boundary_runtime_pilot_behavior_enabled",
    "ml_advisory_phase5_real_adapter_boundary_runtime_copilot_behavior_enabled",
    "ml_advisory_phase5_real_adapter_boundary_adapter_execution_enabled",
)


def test_phase5_manifest_preserves_boundary_flags():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["ml_advisory_phase5_real_adapter_boundary_feature_id"] == FEATURE_ID
    assert data["ml_advisory_phase5_real_adapter_boundary_adapter_descriptor_only"] is True
    assert data["ml_advisory_phase5_real_adapter_boundary_critical_boundary_error_budget"] == 0
    assert data["ml_advisory_phase5_real_adapter_boundary_new_real_prompt_selection_cases_added"] == 0
    assert data["ml_advisory_phase5_real_adapter_boundary_next_safe_feature_title"] == (
        "Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Result Review Gate v1"
    )
    for key in FALSE_KEYS:
        assert data[key] is False, key


print("VALIDATION OK: test_rss_ml_adv_phase5_real_adapter_boundary_manifest_v1")
