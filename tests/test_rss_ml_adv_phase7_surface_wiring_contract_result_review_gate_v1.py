from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_GUARDED_ADVISORY_SURFACE_WIRING_CONTRACT_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_IMPLEMENTATION_READINESS_V1.md"
CONTRACT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_GUARDED_ADVISORY_SURFACE_WIRING_CONTRACT_V1.md"

FEATURE_ID = "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract Result Review Gate v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_v1"
PREFIX = "ml_advisory_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase7_guarded_advisory_surface_wiring_contract_v1_"

FORBIDDEN_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_advisory_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_authority_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']


def test_phase7_surface_wiring_contract_review_gate_accepts_contract_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "feature_title"] == FEATURE_TITLE
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "accepted_only_as_contract"] is True
    assert data[PREFIX + "accepted_automatic_use_contract_only"] is True
    assert data[PREFIX + "accepted_visible_panel_contract_only"] is True
    assert data[PREFIX + "accepted_router_result_copy_unchanged_requirement"] is True
    assert data[PREFIX + "accepted_already_computed_advisory_output_requirement"] is True
    assert data[PREFIX + "accepted_guarded_display_payload_requirement"] is True
    assert data[PREFIX + "accepted_no_free_text_route_advice_requirement"] is True
    assert data[PREFIX + "accepted_future_route_influence_only_as_deterministic_recheck_request_contract"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_contract_still_blocks_runtime_activation_and_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "contract_only"] is True
    assert data[REVIEWED_PREFIX + "visible_panel_contract_defined"] is True
    assert data[REVIEWED_PREFIX + "automatic_use_contract_defined"] is True
    assert data[REVIEWED_PREFIX + "route_effect_model"] == "direct_route_effect_blocked_future_deterministic_recheck_request_only"
    for flag in FORBIDDEN_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag
        assert data[PREFIX + flag] is False, flag


def test_review_docs_preserve_next_safe_implementation_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    contract = CONTRACT_DOC.read_text(encoding="utf-8")
    assert FEATURE_TITLE in review
    assert REVIEWED_FEATURE_ID in review
    assert "not as runtime UI wiring" in review
    assert "not as advisory panel activation" in review
    assert "not as route authority" in review
    assert "deterministic re-check request" in review
    assert "copy the router result unchanged" in next_doc
    assert "attach the advisory payload under a clearly separate telemetry/display key" in next_doc
    assert "expose no route override hook" in next_doc
    assert "advisory surface wiring contract" in contract.lower()


if __name__ == "__main__":
    test_phase7_surface_wiring_contract_review_gate_accepts_contract_only()
    test_reviewed_contract_still_blocks_runtime_activation_and_authority()
    test_review_docs_preserve_next_safe_implementation_scope()
    print("VALIDATION OK: phase7 surface wiring contract result review gate")
