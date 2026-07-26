from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_contract_v1_"
PREV_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_completion_handoff_v1_"
IMPL_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'actual_renderer_mount_enabled', 'renderer_activation_enabled', 'mounted_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']


def test_phase10_renderer_mount_contract_manifest_gates() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
    assert data[PREFIX + "status"] == "contract_only_future_renderer_mount_path_defined_no_runtime_mount_or_ui_mutation"
    assert data[PREFIX + "contract_only"] is True
    assert data[PREFIX + "renderer_mount_contract_only"] is True
    assert data[PREFIX + "future_renderer_mount_contract_ready_possible"] is True
    assert data[PREFIX + "visible_ml_integration_complete"] is False
    assert data[PREFIX + "actual_visible_panel_implemented"] is False
    assert data[PREFIX + "phase9_activation_envelope_input_required"] is True
    assert data[PREFIX + "feature_flag_required"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_envelope_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_envelope_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "read_only"] is True
    assert data[PREFIX + "telemetry_only"] is True
    assert data[PREFIX + "in_memory_only"] is True
    assert data[PREFIX + "bounded"] is True
    assert data[PREFIX + "renderer_input_bounded_required"] is True
    assert data[PREFIX + "renderer_output_bounded_required"] is True
    assert data[PREFIX + "fail_open"] is True
    assert data[PREFIX + "removable_noop"] is True
    assert data[PREFIX + "route_invariant"] is True
    assert data[PREFIX + "final_selection_invisible"] is True
    assert data[PREFIX + "non_authoritative"] is True
    assert data[PREFIX + "non_training_feedback_slot_required"] is True
    assert data[PREFIX + "accepted_no_renderer_activation"] is True
    assert data[PREFIX + "accepted_no_actual_renderer_mount"] is True
    assert data[PREFIX + "accepted_no_mounted_panel"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "requires_phase9_completion_handoff"] is True
    assert data[PREFIX + "requires_phase9_activation_implementation"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 10 Read-Only Advisory Panel Renderer Mount Contract Result Review Gate v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0
    for flag in REQUIRED_FALSE:
        assert data[PREFIX + flag] is False, flag


def test_phase10_renderer_mount_contract_preserves_prerequisite_manifest_state() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREV_PREFIX + "feature_id"] == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_completion_handoff_v1"
    assert data[PREV_PREFIX + "phase9_runtime_activation_line_complete"] is True
    assert data[PREV_PREFIX + "phase10_renderer_mount_contract_required_next"] is True
    assert data[IMPL_PREFIX + "feature_id"] == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
    assert data[IMPL_PREFIX + "runtime_activation_envelope_builder_enabled"] is True
    assert data[IMPL_PREFIX + "renderer_activation_enabled"] is False
    assert data[IMPL_PREFIX + "mounted_panel_enabled"] is False
    assert data[IMPL_PREFIX + "route_authority_enabled"] is False


def test_readme_records_phase10_renderer_mount_contract() -> None:
    text = README.read_text(encoding="utf-8")
    assert "Phase 10 read-only advisory panel renderer mount contract" in text
    assert "does not activate a renderer" in text
    assert "Phase 10 Read-Only Advisory Panel Renderer Mount Contract Result Review Gate v1" in text


if __name__ == "__main__":
    test_phase10_renderer_mount_contract_manifest_gates()
    test_phase10_renderer_mount_contract_preserves_prerequisite_manifest_state()
    test_readme_records_phase10_renderer_mount_contract()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount contract manifest gates")
