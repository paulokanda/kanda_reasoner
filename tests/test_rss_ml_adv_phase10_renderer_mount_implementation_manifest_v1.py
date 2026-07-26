from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_implementation_v1_"
REVIEW_PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1_"
CONTRACT_PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_contract_v1_"
REQUIRED_FALSE = [
    "real_ml_enabled",
    "adapter_execution_enabled",
    "candidate_execution_enabled",
    "provider_calls_enabled",
    "network_calls_enabled",
    "api_keys_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "persistence_enabled",
    "report_persistence_enabled",
    "prompt_loading_enabled",
    "prompt_registry_mutation_enabled",
    "prompt_library_read_enabled",
    "freeze_memory_read_enabled",
    "freeze_memory_write_enabled",
    "router_canon_read_enabled",
    "runtime_shadow_mode_enabled",
    "runtime_ui_mutation_enabled",
    "runtime_telemetry_surface_wired",
    "router_prompt_logic_modified",
    "router_final_selection_modified",
    "final_selection_hook_enabled",
    "prompt_selection_hook_enabled",
    "route_influence_enabled",
    "route_authority_enabled",
    "router_calls_enabled",
    "advisor_calls_enabled",
    "advisory_rankings_enabled",
    "prompt_rankings_enabled",
    "route_override_button_enabled",
    "use_ml_route_button_enabled",
    "best_route_claim_enabled",
    "free_text_route_advice_enabled",
    "free_text_explanations_enabled",
    "training_enabled",
    "calibration_enabled",
    "model_improvement_enabled",
    "runtime_pilot_behavior_enabled",
    "runtime_copilot_decision_behavior_enabled",
    "mlrt_113_created",
]


def test_phase10_renderer_mount_implementation_manifest_gates() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"
    assert data[PREFIX + "status"] == "read_only_renderer_mount_descriptor_implemented_default_off"
    assert data[PREFIX + "implementation_enabled"] is True
    assert data[PREFIX + "source_review_gate_feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1"
    assert data[PREFIX + "source_contract_feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
    assert data[PREFIX + "feature_flag_required"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_envelope_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_envelope_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "phase9_activation_envelope_input_required"] is True
    assert data[PREFIX + "read_only_mount_descriptor_ready_possible"] is True
    assert data[PREFIX + "visible_read_only_panel_descriptor_ready_possible"] is True
    assert data[PREFIX + "read_only"] is True
    assert data[PREFIX + "telemetry_only"] is True
    assert data[PREFIX + "in_memory_only"] is True
    assert data[PREFIX + "bounded"] is True
    assert data[PREFIX + "fail_open"] is True
    assert data[PREFIX + "removable_noop"] is True
    assert data[PREFIX + "route_invariant"] is True
    assert data[PREFIX + "final_selection_invisible"] is True
    assert data[PREFIX + "non_authoritative"] is True
    assert data[PREFIX + "bounded_rendered_sections"] is True
    assert data[PREFIX + "non_training_feedback_slot"] is True
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Implementation Result Review Gate v1"
    for flag in REQUIRED_FALSE:
        assert data[PREFIX + flag] is False, flag


def test_phase10_renderer_mount_implementation_preserves_prerequisite_manifest_state() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEW_PREFIX + "feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1"
    assert data[REVIEW_PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Implementation v1"
    assert data[CONTRACT_PREFIX + "feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
    assert data[CONTRACT_PREFIX + "contract_result_review_gate_completed"] is True
    assert data[CONTRACT_PREFIX + "route_authority_enabled"] is False


def test_readme_records_phase10_renderer_mount_implementation() -> None:
    text = README.read_text(encoding="utf-8")
    assert "Phase 10 read-only advisory panel renderer mount implementation" in text
    assert "feature-flagged, default-off" in text
    assert "does not mutate runtime UI" in text
    assert "Implementation Result Review Gate v1" in text


if __name__ == "__main__":
    test_phase10_renderer_mount_implementation_manifest_gates()
    test_phase10_renderer_mount_implementation_preserves_prerequisite_manifest_state()
    test_readme_records_phase10_renderer_mount_implementation()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount implementation manifest gates")
