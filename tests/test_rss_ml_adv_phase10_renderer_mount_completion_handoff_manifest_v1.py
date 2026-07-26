from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PREFIX = "ml_advisory_phase10_read_only_advisory_panel_renderer_mount_completion_handoff_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created', 'autonomous_ml_router_enabled']


def test_phase10_renderer_mount_completion_handoff_manifest_gates() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "status"] == "completion_handoff_closes_phase10_renderer_mount_descriptor_line_no_route_authority"
    assert data[PREFIX + "completion_handoff_only"] is True
    assert data[PREFIX + "phase10_renderer_mount_line_closed"] is True
    assert data[PREFIX + "feature_flag_required"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_envelope_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_envelope_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "phase9_activation_envelope_lineage_only"] is True
    assert data[PREFIX + "bounded_phase8_sections_only"] is True
    assert data[PREFIX + "route_invariant"] is True
    assert data[PREFIX + "final_selection_invisible"] is True
    assert data[PREFIX + "non_training_feedback_slot"] is True
    assert data[PREFIX + "non_authoritative"] is True
    assert data[PREFIX + "visible_ml_integration_complete"] is False
    assert data[PREFIX + "host_binding_required_for_actual_runtime_visibility"] is True
    for flag in REQUIRED_FALSE:
        assert data[PREFIX + flag] is False, flag


def test_readme_records_phase10_completion_handoff_and_phase11_boundary() -> None:
    text = README.read_text(encoding="utf-8")
    assert "Phase 10 read-only advisory panel renderer mount completion handoff" in text
    assert "closes the Phase 10 renderer/mount descriptor line" in text
    assert "Actual runtime app-host visibility still requires a separate governed host-binding contract" in text
    assert "Phase 11 Read-Only Advisory Panel Host Binding Contract v1" in text


if __name__ == "__main__":
    test_phase10_renderer_mount_completion_handoff_manifest_gates()
    test_readme_records_phase10_completion_handoff_and_phase11_boundary()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount completion handoff manifest gates")
