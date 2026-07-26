import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_OFFLINE_EVALUATION_HARNESS_CONTRACT_V1.md"
BOUNDARY = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_OFFLINE_HARNESS_BOUNDARY_MODEL_V1.md"
READINESS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_RESULT_REVIEW_READINESS_V1.md"


def test_phase2_manifest_records_contract_and_boundaries():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prefix = "ml_advisory_phase2_offline_evaluation_harness_contract_v1"

    assert data[prefix + "_feature_id"] == "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1"
    assert data[prefix + "_caller_supplied_fixtures_only"] is True
    assert data[prefix + "_in_memory_only"] is True
    assert data[prefix + "_route_invariance_required"] is True
    assert data[prefix + "_fail_open_required"] is True
    assert data[prefix + "_new_real_prompt_selection_cases_added"] == 0
    assert data[prefix + "_mlrt_113_created"] is False
    assert data[prefix + "_real_ml_enabled"] is False
    assert data[prefix + "_provider_calls_enabled"] is False
    assert data[prefix + "_embeddings_enabled"] is False
    assert data[prefix + "_vector_store_enabled"] is False
    assert data[prefix + "_persistence_enabled"] is False
    assert data[prefix + "_prompt_loading_enabled"] is False
    assert data[prefix + "_router_prompt_logic_modified"] is False
    assert data[prefix + "_router_final_selection_modified"] is False
    assert data[prefix + "_route_authority_enabled"] is False
    assert data[prefix + "_advisory_rankings_enabled"] is False
    assert data[prefix + "_free_text_explanations_enabled"] is False
    assert data[prefix + "_critical_boundary_error_budget"] == 0


def test_phase2_docs_record_no_runtime_or_authority_scope():
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in (DOC, BOUNDARY, READINESS)
    ).lower()
    required = [
        "not runtime shadow mode",
        "does not choose a route",
        "no real ml",
        "no provider calls",
        "no embeddings",
        "no persistence",
        "no prompt loading",
        "no router prompt logic",
        "no route authority",
        "creates no mlrt-113",
    ]
    for phrase in required:
        assert phrase in combined, phrase
