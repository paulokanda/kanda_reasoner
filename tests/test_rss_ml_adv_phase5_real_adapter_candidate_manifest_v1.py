import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "rss_ml_adv_phase5_offline_real_adapter_candidate_contract_v1"
NEXT_TITLE = "Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Result Review Gate v1"


FALSE_KEYS = [
    "ml_advisory_phase5_real_adapter_candidate_real_ml_enabled",
    "ml_advisory_phase5_real_adapter_candidate_adapter_execution_enabled",
    "ml_advisory_phase5_real_adapter_candidate_candidate_execution_enabled",
    "ml_advisory_phase5_real_adapter_candidate_provider_calls_enabled",
    "ml_advisory_phase5_real_adapter_candidate_network_calls_enabled",
    "ml_advisory_phase5_real_adapter_candidate_api_keys_enabled",
    "ml_advisory_phase5_real_adapter_candidate_embeddings_enabled",
    "ml_advisory_phase5_real_adapter_candidate_vector_store_enabled",
    "ml_advisory_phase5_real_adapter_candidate_persistence_enabled",
    "ml_advisory_phase5_real_adapter_candidate_report_persistence_enabled",
    "ml_advisory_phase5_real_adapter_candidate_prompt_loading_enabled",
    "ml_advisory_phase5_real_adapter_candidate_prompt_registry_mutation_enabled",
    "ml_advisory_phase5_real_adapter_candidate_prompt_library_read_enabled",
    "ml_advisory_phase5_real_adapter_candidate_freeze_memory_read_enabled",
    "ml_advisory_phase5_real_adapter_candidate_freeze_memory_write_enabled",
    "ml_advisory_phase5_real_adapter_candidate_router_canon_read_enabled",
    "ml_advisory_phase5_real_adapter_candidate_runtime_shadow_mode_enabled",
    "ml_advisory_phase5_real_adapter_candidate_router_prompt_logic_modified",
    "ml_advisory_phase5_real_adapter_candidate_router_final_selection_modified",
    "ml_advisory_phase5_real_adapter_candidate_route_authority_enabled",
    "ml_advisory_phase5_real_adapter_candidate_advisory_rankings_enabled",
    "ml_advisory_phase5_real_adapter_candidate_free_text_explanations_enabled",
    "ml_advisory_phase5_real_adapter_candidate_training_enabled",
    "ml_advisory_phase5_real_adapter_candidate_calibration_enabled",
    "ml_advisory_phase5_real_adapter_candidate_model_improvement_enabled",
    "ml_advisory_phase5_real_adapter_candidate_runtime_pilot_behavior_enabled",
    "ml_advisory_phase5_real_adapter_candidate_runtime_copilot_behavior_enabled",
]


def test_phase5_candidate_manifest_gates():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["ml_advisory_phase5_real_adapter_candidate_feature_id"] == FEATURE_ID
    assert manifest["ml_advisory_phase5_real_adapter_candidate_next_safe_feature_title"] == NEXT_TITLE
    assert manifest["ml_advisory_phase5_real_adapter_candidate_prerequisite_feature_id"] == (
        "rss_ml_adv_phase5_real_adapter_boundary_result_review_gate_v1"
    )
    assert manifest["ml_advisory_phase5_real_adapter_candidate_new_real_prompt_selection_cases_added"] == 0
    assert manifest["ml_advisory_phase5_real_adapter_candidate_mlrt113_created"] is False
    assert manifest["ml_advisory_phase5_real_adapter_candidate_fixture_bound_only"] is True
    assert manifest["ml_advisory_phase5_real_adapter_candidate_offline_descriptor_only"] is True
    assert manifest["ml_advisory_phase5_real_adapter_candidate_critical_boundary_error_budget"] == 0
    for key in FALSE_KEYS:
        assert manifest[key] is False, key


def main():
    test_phase5_candidate_manifest_gates()


if __name__ == "__main__":
    main()
