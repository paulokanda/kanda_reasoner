from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_FINAL_SAFETY_GATE_READINESS_V1.md"
IMPL_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_IMPLEMENTATION_V1.md"

FEATURE_ID = "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
PREFIX = "ml_advisory_phase7_read_only_advisory_surface_wiring_implementation_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase7_read_only_advisory_surface_wiring_implementation_v1_"
FORBIDDEN_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_advisory_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_authority_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']


def test_phase7_surface_wiring_implementation_review_gate_accepts_read_only_builder_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "accepted_only_as_read_only_surface_envelope_builder"] is True
    assert data[PREFIX + "accepted_canonical_snapshot_unchanged"] is True
    assert data[PREFIX + "accepted_separate_telemetry_surface_field"] is True
    assert data[PREFIX + "accepted_already_built_guarded_display_payload_only"] is True
    assert data[PREFIX + "accepted_disabled_noop_path"] is True
    assert data[PREFIX + "accepted_invalid_payload_fail_open_path"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_wiring"] is True
    assert data[PREFIX + "accepted_no_advisory_panel_activation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_final_selection_hook"] is True
    assert data[PREFIX + "accepted_no_prompt_selection_hook"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Final Safety Gate v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_implementation_still_blocks_route_authority_and_runtime_activation() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "implements_read_only_surface_envelope_builder"] is True
    assert data[REVIEWED_PREFIX + "copies_canonical_result_snapshot_unchanged"] is True
    assert data[REVIEWED_PREFIX + "attaches_payload_under_separate_surface_field"] is True
    assert data[REVIEWED_PREFIX + "does_not_call_router"] is True
    assert data[REVIEWED_PREFIX + "does_not_call_advisor"] is True
    assert data[REVIEWED_PREFIX + "does_not_execute_adapter"] is True
    assert data[REVIEWED_PREFIX + "does_not_activate_panel"] is True
    for flag in FORBIDDEN_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag
        assert data[PREFIX + flag] is False, flag


def test_review_docs_preserve_final_safety_gate_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    impl_doc = IMPL_DOC.read_text(encoding="utf-8")
    assert "runtime" in review and "UI wiring" in review
    assert "not as advisory panel activation" in review
    assert "runtime telemetry surface" in review
    assert "route influence" in review
    assert "no final-selection hook" in review
    assert "no prompt-selection hook" in review
    assert "Only after the final safety gate" in next_doc
    assert "in-memory envelope" in impl_doc and "separate telemetry surface" in impl_doc


if __name__ == "__main__":
    test_phase7_surface_wiring_implementation_review_gate_accepts_read_only_builder_only()
    test_reviewed_implementation_still_blocks_route_authority_and_runtime_activation()
    test_review_docs_preserve_final_safety_gate_scope()
    print("VALIDATION OK: phase7 read-only advisory surface wiring implementation result review gate")
