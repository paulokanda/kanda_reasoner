import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prefix = "ml_advisory_phase3_fixture_catalog_result_review_gate_v1_"

    require(manifest.get(prefix + "feature_id") == "rss_ml_adv_phase3_fixture_catalog_result_review_gate_v1", "feature ID mismatch")
    require(manifest.get(prefix + "feature_title") == "Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Result Review Gate v1", "feature title mismatch")
    require(manifest.get(prefix + "reviewed_feature_id") == "rss_ml_adv_phase3_offline_fixture_catalog_contract_v1", "reviewed feature ID mismatch")
    require(manifest.get(prefix + "next_safe_feature_title") == "Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1", "next safe feature mismatch")
    require(manifest.get(prefix + "new_real_prompt_selection_cases_added") == 0, "new real prompt-selection case count must be zero")
    require(manifest.get(prefix + "critical_boundary_error_budget") == 0, "critical boundary error budget must be zero")

    expected_doc = "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE3_OFFLINE_FIXTURE_CATALOG_RESULT_REVIEW_GATE_V1.md"
    expected_readiness = "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE4_OFFLINE_ADVISOR_COMPARISON_CONTRACT_READINESS_V1.md"
    require(manifest.get(prefix + "doc") == expected_doc, "review gate doc path mismatch")
    require(manifest.get(prefix + "phase4_readiness_doc") == expected_readiness, "Phase 4 readiness doc path mismatch")

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
    for suffix in false_keys:
        require(manifest.get(prefix + suffix) is False, f"manifest flag must be false: {suffix}")

    tests = manifest.get(prefix + "validation_tests")
    require(isinstance(tests, list), "validation tests must be listed")
    require("tests/test_rss_ml_adv_phase3_result_review_gate_v1.py" in tests, "review gate test missing")
    require("tests/test_rss_ml_adv_phase3_result_review_gate_manifest_v1.py" in tests, "manifest test missing")

    print("VALIDATION OK: rss_ml_adv_phase3_fixture_catalog_result_review_gate_manifest_v1")


if __name__ == "__main__":
    main()
