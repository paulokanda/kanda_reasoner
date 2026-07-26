import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE3_OFFLINE_FIXTURE_CATALOG_CONTRACT_V1.md"
BOUNDARY = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE3_OFFLINE_FIXTURE_CATALOG_BOUNDARY_MODEL_V1.md"
READINESS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE3_RESULT_REVIEW_READINESS_V1.md"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(
        manifest.get("ml_advisory_phase3_fixture_catalog_feature_id")
        == "rss_ml_adv_phase3_offline_fixture_catalog_contract_v1",
        "missing Phase 3 fixture catalog feature id",
    )
    false_keys = [
        "ml_advisory_phase3_fixture_catalog_contains_real_ml",
        "ml_advisory_phase3_fixture_catalog_contains_provider_calls",
        "ml_advisory_phase3_fixture_catalog_contains_embeddings",
        "ml_advisory_phase3_fixture_catalog_contains_vector_store",
        "ml_advisory_phase3_fixture_catalog_contains_persistence",
        "ml_advisory_phase3_fixture_catalog_contains_prompt_loading",
        "ml_advisory_phase3_fixture_catalog_contains_prompt_registry_mutation",
        "ml_advisory_phase3_fixture_catalog_contains_prompt_library_read",
        "ml_advisory_phase3_fixture_catalog_contains_freeze_memory_read",
        "ml_advisory_phase3_fixture_catalog_contains_router_canon_read",
        "ml_advisory_phase3_fixture_catalog_contains_runtime_shadow_mode",
        "ml_advisory_phase3_fixture_catalog_contains_router_prompt_logic_modification",
        "ml_advisory_phase3_fixture_catalog_contains_router_final_selection_modification",
        "ml_advisory_phase3_fixture_catalog_contains_route_authority",
        "ml_advisory_phase3_fixture_catalog_creates_mlrt_113",
    ]
    for key in false_keys:
        require(manifest.get(key) is False, key + " must be false")

    for path in (DOC, BOUNDARY, READINESS):
        require(path.exists(), "missing doc: " + str(path))
        text = path.read_text(encoding="utf-8")
        require("MLRT-113" in text, "doc missing MLRT-113 boundary: " + path.name)
        require("No real ML" in text or "real ML" in text, "doc missing real ML boundary: " + path.name)
        require("No route authority" in text or "route authority" in text, "doc missing route boundary: " + path.name)

    doc_text = DOC.read_text(encoding="utf-8")
    for item in [
        "Feature ID: rss_ml_adv_phase3_offline_fixture_catalog_contract_v1",
        "adds 0 real prompt-selection cases",
        "no runtime integration",
        "No prompt library read",
        "No freeze-memory read or write",
        "No router-canon read",
        "critical boundary error budget zero",
        "Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Result Review Gate v1",
    ]:
        require(item in doc_text, "Phase 3 doc missing: " + item)

    print("VALIDATION OK: rss_ml_adv_phase3_fixture_catalog_manifest_v1")


if __name__ == "__main__":
    main()
