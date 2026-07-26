from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_CONTRACT_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_IMPLEMENTATION_READINESS_V1.md"
CONTRACT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_CONTRACT_V1.md"
PHASE9_HANDOFF = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_COMPLETION_HANDOFF_V1.md"

FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1_"
CONTRACT_PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_contract_v1_"
FALSE_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created', 'visible_ml_integration_complete']


def test_phase10_renderer_mount_contract_result_review_gate_accepts_contract_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "contract_result_review_gate_only"] is True
    assert data[PREFIX + "review_gate_only"] is True
    assert data[PREFIX + "accepted_contract_only"] is True
    assert data[PREFIX + "accepted_good_safe_for_later_implementation_only"] is True
    assert data[PREFIX + "accepted_phase9_activation_envelope_lineage_only"] is True
    assert data[PREFIX + "accepted_feature_flag_required"] is True
    assert data[PREFIX + "accepted_feature_flag_default_off"] is True
    assert data[PREFIX + "accepted_disabled_noop_path"] is True
    assert data[PREFIX + "accepted_missing_envelope_fail_open_path"] is True
    assert data[PREFIX + "accepted_bounded_renderer_input"] is True
    assert data[PREFIX + "accepted_bounded_renderer_output"] is True
    assert data[PREFIX + "accepted_removable_noop_mount"] is True
    assert data[PREFIX + "accepted_route_invariant"] is True
    assert data[PREFIX + "accepted_final_selection_invisible"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_non_authoritative"] is True
    assert data[PREFIX + "accepted_no_actual_renderer_mount"] is True
    assert data[PREFIX + "accepted_no_renderer_activation"] is True
    assert data[PREFIX + "accepted_no_mounted_panel"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Implementation v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_phase10_renderer_mount_contract_result_review_gate_preserves_contract_and_blocks_forbidden_flags() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[CONTRACT_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[CONTRACT_PREFIX + "contract_only"] is True
    assert data[CONTRACT_PREFIX + "actual_renderer_mount_enabled"] is False
    assert data[CONTRACT_PREFIX + "mounted_panel_enabled"] is False
    assert data[CONTRACT_PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[CONTRACT_PREFIX + "runtime_telemetry_surface_wired"] is False
    assert data[CONTRACT_PREFIX + "route_authority_enabled"] is False
    assert data[CONTRACT_PREFIX + "contract_result_review_gate_completed"] is True
    assert data[CONTRACT_PREFIX + "contract_result_review_gate_feature_id"] == FEATURE_ID
    for flag in FALSE_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_phase10_renderer_mount_contract_result_review_gate_docs_define_next_safe_implementation() -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    contract_text = CONTRACT_DOC.read_text(encoding="utf-8")
    handoff_text = PHASE9_HANDOFF.read_text(encoding="utf-8")
    assert "accepts the Phase 10 read-only advisory panel renderer/mount" in doc_text and "contract" in doc_text
    assert "not implement the renderer" in doc_text
    assert "not accepted as visible ML integration" in doc_text
    assert "Phase 10 Read-Only Advisory Panel Renderer Mount Implementation v1" in doc_text
    assert "implementation patch may only create a read-only" in next_text
    assert "Still forbidden" in next_text
    assert "renderer/mount contract only" in contract_text
    assert "Phase 10 Read-Only Advisory Panel Renderer Mount Contract v1" in handoff_text


if __name__ == "__main__":
    test_phase10_renderer_mount_contract_result_review_gate_accepts_contract_only()
    test_phase10_renderer_mount_contract_result_review_gate_preserves_contract_and_blocks_forbidden_flags()
    test_phase10_renderer_mount_contract_result_review_gate_docs_define_next_safe_implementation()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount contract result review gate")
