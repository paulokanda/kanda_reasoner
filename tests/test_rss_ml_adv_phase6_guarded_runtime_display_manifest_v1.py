import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'box_manifest.json'

PREFIX = 'ml_advisory_phase6_guarded_runtime_advisory_display_contract_v1_'
FEATURE_ID = 'rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_v1'
FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1'
PREV_FEATURE_ID = 'rss_ml_adv_phase5_real_adapter_candidate_result_review_gate_v1'
NEXT_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract Result Review Gate v1'


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def test_manifest_registers_phase6_contract_and_next_review_gate():
    manifest = load_manifest()
    assert manifest[PREFIX + 'feature_id'] == FEATURE_ID
    assert manifest[PREFIX + 'feature_title'] == FEATURE_TITLE
    assert manifest[PREFIX + 'prerequisite_feature_id'] == PREV_FEATURE_ID
    assert manifest[PREFIX + 'next_safe_feature_title'] == NEXT_TITLE
    assert manifest[PREFIX + 'phase'] == 'phase_6_guarded_runtime_advisory_display_contract'
    assert manifest[PREFIX + 'status'] == 'contract_only_no_runtime_display_no_runtime_ml_no_route_authority_no_router_prompt_logic_change'
    assert manifest[PREFIX + 'doc'].endswith('ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_CONTRACT_V1.md')
    assert manifest[PREFIX + 'runtime_display_contract_defined'] is True


def test_manifest_forbids_runtime_display_authority_and_provider_paths():
    manifest = load_manifest()
    false_suffixes = [
        'mlrt_113_created',
        'real_ml_enabled',
        'adapter_execution_enabled',
        'candidate_execution_enabled',
        'provider_calls_enabled',
        'network_calls_enabled',
        'api_keys_enabled',
        'embeddings_enabled',
        'vector_store_enabled',
        'persistence_enabled',
        'report_persistence_enabled',
        'prompt_loading_enabled',
        'prompt_registry_mutation_enabled',
        'prompt_library_read_enabled',
        'freeze_memory_read_enabled',
        'freeze_memory_write_enabled',
        'router_canon_read_enabled',
        'runtime_shadow_mode_enabled',
        'runtime_display_enabled',
        'runtime_advisory_panel_enabled',
        'runtime_telemetry_surface_enabled',
        'runtime_ui_mutation_enabled',
        'router_prompt_logic_modified',
        'router_final_selection_modified',
        'route_authority_enabled',
        'advisory_rankings_enabled',
        'free_text_explanations_enabled',
        'training_enabled',
        'calibration_enabled',
        'model_improvement_enabled',
        'runtime_pilot_behavior_enabled',
        'runtime_copilot_behavior_enabled',
    ]
    for suffix in false_suffixes:
        assert manifest[PREFIX + suffix] is False, suffix
    assert manifest[PREFIX + 'new_real_prompt_selection_cases_added'] == 0
    assert manifest[PREFIX + 'critical_boundary_error_budget'] == 0


def test_manifest_validation_tests_are_local_to_phase6_contract():
    manifest = load_manifest()
    tests = manifest[PREFIX + 'validation_tests']
    assert tests == [
        'tests/test_rss_ml_adv_phase6_guarded_runtime_display_contract_v1.py',
        'tests/test_rss_ml_adv_phase6_guarded_runtime_display_import_v1.py',
        'tests/test_rss_ml_adv_phase6_guarded_runtime_display_manifest_v1.py',
    ]


if __name__ == '__main__':
    test_manifest_registers_phase6_contract_and_next_review_gate()
    test_manifest_forbids_runtime_display_authority_and_provider_paths()
    test_manifest_validation_tests_are_local_to_phase6_contract()
    print('VALIDATION OK: rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_v1_manifest')
