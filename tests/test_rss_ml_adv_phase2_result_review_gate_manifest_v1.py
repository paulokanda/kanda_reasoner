import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREFIX = "ml_advisory_phase2_offline_harness_result_review_gate_v1_"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    require(data.get(PREFIX + "feature_id") == "rss_ml_adv_phase2_offline_harness_result_review_gate_v1", "feature id mismatch")
    require(data.get(PREFIX + "feature_title") == "Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Result Review Gate v1", "feature title mismatch")
    require(data.get(PREFIX + "reviewed_feature_id") == "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1", "reviewed feature id mismatch")
    require(data.get(PREFIX + "reviewed_feature_title") == "Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1", "reviewed feature title mismatch")
    require(data.get(PREFIX + "next_safe_feature_title") == "Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1", "next safe feature mismatch")
    require(data.get(PREFIX + "new_real_prompt_selection_cases_added") == 0, "new real cases must be zero")
    require(data.get(PREFIX + "critical_boundary_error_budget") == 0, "critical boundary error budget must be zero")

    false_keys = [
        "mlrt_113_created",
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
        "runtime_copilot_behavior_enabled",
    ]
    for key in false_keys:
        require(data.get(PREFIX + key) is False, key + " must be false")

    tests = data.get(PREFIX + "validation_tests")
    require(isinstance(tests, list), "validation tests must be a list")
    require("tests/test_rss_ml_adv_phase2_result_review_gate_v1.py" in tests, "missing doc test")
    require("tests/test_rss_ml_adv_phase2_result_review_gate_manifest_v1.py" in tests, "missing manifest test")

    print("VALIDATION OK: rss_ml_adv_phase2_result_review_gate_manifest_v1")


if __name__ == "__main__":
    main()
