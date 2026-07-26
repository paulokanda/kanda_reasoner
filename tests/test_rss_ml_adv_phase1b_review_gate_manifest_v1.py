import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREFIX = "ml_advisory_phase1b_design_audit_result_review_gate_v1"


def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_phase1b_review_manifest_records_feature_and_next_safe_phase2_contract():
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == "rss_ml_adv_phase1b_design_audit_result_review_gate_v1"
    assert data[f"{PREFIX}_feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Result Review Gate v1"
    assert data[f"{PREFIX}_reviewed_feature_id"] == "rss_ml_adv_phase1b_design_audit_contract_v1"
    assert data[f"{PREFIX}_phase"] == "phase_1b_result_review_gate"
    assert data[f"{PREFIX}_next_safe_feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1"
    assert data[f"{PREFIX}_new_real_prompt_selection_cases_added"] == 0
    assert data[f"{PREFIX}_mlrt_113_created"] is False


def test_phase1b_review_manifest_keeps_all_runtime_authority_flags_disabled():
    data = manifest()
    disabled = [
        "real_ml_enabled",
        "provider_calls_enabled",
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
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
        "runtime_pilot_behavior_enabled",
        "copilot_behavior_enabled",
    ]
    for suffix in disabled:
        assert data[f"{PREFIX}_{suffix}"] is False, suffix
    assert data[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_no_mlrt_113_artifacts_created_by_phase1b_review_gate():
    matches = []
    for path in ROOT.rglob("*"):
        if "__pycache__" in path.parts:
            continue
        name = path.name.lower()
        if "mlrt_113" in name or "mlrt113" in name:
            matches.append(str(path))
    assert matches == []
