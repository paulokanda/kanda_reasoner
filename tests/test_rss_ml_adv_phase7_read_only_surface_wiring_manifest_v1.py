from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PREFIX = "ml_advisory_phase7_read_only_advisory_surface_wiring_implementation_v1_"
REVIEW_PREFIX = "ml_advisory_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1_"

FORBIDDEN_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_advisory_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_authority_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']


def test_phase7_read_only_surface_wiring_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
    assert data[PREFIX + "source_review_feature_id"] == "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"
    assert data[PREFIX + "implements_read_only_surface_envelope_builder"] is True
    assert data[PREFIX + "copies_canonical_result_snapshot_unchanged"] is True
    assert data[PREFIX + "attaches_payload_under_separate_surface_field"] is True
    assert data[PREFIX + "consumes_already_computed_display_payload_only"] is True
    assert data[PREFIX + "does_not_call_router"] is True
    assert data[PREFIX + "does_not_call_advisor"] is True
    assert data[PREFIX + "does_not_execute_adapter"] is True
    assert data[PREFIX + "does_not_activate_panel"] is True
    assert data[PREFIX + "disabled_noop_path"] is True
    assert data[PREFIX + "invalid_payload_fail_open_path"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation Result Review Gate v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0
    for flag in FORBIDDEN_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_source_review_gate_still_present_and_readme_updated() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEW_PREFIX + "feature_id"] == "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"
    assert data[REVIEW_PREFIX + "accepted_only_as_contract"] is True
    readme = README.read_text(encoding="utf-8")
    assert "Phase 7 read-only advisory surface wiring implementation" in readme
    assert "copies the caller-supplied" in readme and "canonical dispatch snapshot unchanged" in readme
    assert "not advisory panel activation" in readme


if __name__ == "__main__":
    test_phase7_read_only_surface_wiring_manifest()
    test_source_review_gate_still_present_and_readme_updated()
    print("VALIDATION OK: phase7 read-only advisory surface wiring manifest gates")
