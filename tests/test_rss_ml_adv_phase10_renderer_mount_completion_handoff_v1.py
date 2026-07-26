from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_COMPLETION_HANDOFF_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_CONTRACT_READINESS_V1.md"
FINAL_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_FINAL_SAFETY_GATE_V1.md"
IMPLEMENTATION_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_IMPLEMENTATION_V1.md"

FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_completion_handoff_v1"
FINAL_FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_final_safety_gate_v1"
PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_completion_handoff_v1_"
FINAL_PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_final_safety_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_implementation_v1_"
FALSE_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created', 'autonomous_ml_router_enabled']


def test_phase10_renderer_mount_completion_handoff_closes_only_descriptor_line() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_final_safety_gate_feature_id"] == FINAL_FEATURE_ID
    assert data[PREFIX + "completion_handoff_only"] is True
    assert data[PREFIX + "phase10_renderer_mount_line_closed"] is True
    assert data[PREFIX + "renderer_mount_descriptor_line_complete"] is True
    assert data[PREFIX + "renderer_mount_descriptor_in_memory_only"] is True
    assert data[PREFIX + "renderer_mount_descriptor_read_only"] is True
    assert data[PREFIX + "renderer_mount_descriptor_removable_noop"] is True
    assert data[PREFIX + "safe_for_phase11_host_binding_contract_only"] is True
    assert data[PREFIX + "visible_ml_integration_complete"] is False
    assert data[PREFIX + "host_binding_required_for_actual_runtime_visibility"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Contract v1"
    assert data[PREFIX + "critical_boundary_error_budget"] == 0
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0


def test_phase10_renderer_mount_completion_handoff_preserves_no_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[FINAL_PREFIX + "feature_id"] == FINAL_FEATURE_ID
    assert data[FINAL_PREFIX + "completion_handoff_completed"] is True
    assert data[FINAL_PREFIX + "completion_handoff_feature_id"] == FEATURE_ID
    assert data[FINAL_PREFIX + "phase10_renderer_mount_line_closed"] is True
    assert data[FINAL_PREFIX + "visible_ml_integration_complete"] is False
    assert data[FINAL_PREFIX + "host_binding_required_for_actual_runtime_visibility"] is True
    assert data[IMPL_PREFIX + "feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"
    assert data[IMPL_PREFIX + "completion_handoff_completed"] is True
    assert data[IMPL_PREFIX + "completion_handoff_feature_id"] == FEATURE_ID
    assert data[IMPL_PREFIX + "phase10_renderer_mount_line_closed"] is True
    assert data[IMPL_PREFIX + "visible_ml_integration_complete"] is False
    assert data[IMPL_PREFIX + "host_binding_required_for_actual_runtime_visibility"] is True
    for flag in FALSE_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_phase10_renderer_mount_completion_handoff_docs_define_next_contract() -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    final_text = FINAL_DOC.read_text(encoding="utf-8")
    implementation_text = IMPLEMENTATION_DOC.read_text(encoding="utf-8")
    assert "closes the Phase 10 read-only advisory panel renderer/mount descriptor line" in doc_text
    assert "does not claim autonomous ML routing" in doc_text
    assert "does not claim completed runtime app-host visibility" in doc_text
    assert "Phase 11 Read-Only Advisory Panel Host Binding Contract" in doc_text
    assert "Why a separate Phase 11 is required" in next_text
    assert "governed deterministic router remains the final selector" in next_text
    assert "safe for a separate completion handoff" in final_text
    assert "renderer/mount descriptor" in implementation_text


if __name__ == "__main__":
    test_phase10_renderer_mount_completion_handoff_closes_only_descriptor_line()
    test_phase10_renderer_mount_completion_handoff_preserves_no_authority()
    test_phase10_renderer_mount_completion_handoff_docs_define_next_contract()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount completion handoff")
