"""Tests for ML Advisory Phase 1a result-review gate.

The gate is a documentation and manifest review only. It must not add route
authority, real ML, runtime behavior, or MLRT expansion.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RSS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MANIFEST = RSS / "box_manifest.json"
REVIEW_DOC = RSS / "ml_advisory_signal" / "ML_ADVISORY_PHASE1A_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = RSS / "ml_advisory_signal" / "ML_ADVISORY_PHASE1B_DESIGN_AUDIT_READINESS_V1.md"
PHASE1A_DOC = RSS / "ml_advisory_signal" / "ML_ADVISORY_AND_PROMPT_INTAKE_BOUNDARY_MODEL_V1.md"

FORBIDDEN_TRUE_KEYS = (
    "real_ml_enabled",
    "provider_calls_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "persistence_enabled",
    "prompt_loading_enabled",
    "prompt_registry_mutation_enabled",
    "router_prompt_logic_modified",
    "router_final_selection_modified",
    "route_authority_enabled",
    "runtime_shadow_mode_enabled",
    "advisory_rankings_enabled",
    "free_text_explanations_enabled",
    "freeze_memory_write_enabled",
    "training_enabled",
    "model_improvement_enabled",
    "mlrt_113_created",
)


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_phase1a_review_gate_docs_exist_and_preserve_scope() -> None:
    assert REVIEW_DOC.exists()
    assert NEXT_DOC.exists()
    assert PHASE1A_DOC.exists()

    review = REVIEW_DOC.read_text(encoding="utf-8")
    required = (
        "Phase 1a is accepted only as boundary-contract",
        "0 new real prompt-selection cases",
        "does not create MLRT-113",
        "ML Advisory Signal is telemetry, not authority",
        "Governed Router remains the final selector",
        "Critical boundary error budget remains zero",
        "Phase 1b should be a design audit",
    )
    for phrase in required:
        assert phrase in review


def test_phase1a_review_gate_manifest_is_non_authoritative() -> None:
    manifest = _manifest()
    prefix = "ml_advisory_phase1a_result_review_gate_v1_"

    assert manifest[prefix + "feature_id"] == "rss_ml_adv_phase1a_review_gate_v1"
    assert manifest[prefix + "reviewed_feature_id"] == "rss_ml_advisory_prompt_intake_boundary_v1"
    assert manifest[prefix + "new_real_mlrt_cases_added"] == 0
    assert manifest[prefix + "critical_boundary_error_budget"] == 0

    for suffix in FORBIDDEN_TRUE_KEYS:
        key = prefix + suffix
        assert key in manifest, key
        assert manifest[key] is False, key


def test_phase1b_readiness_doc_blocks_runtime_ml() -> None:
    doc = NEXT_DOC.read_text(encoding="utf-8")
    required = (
        "Phase 1b is not runtime ML integration",
        "no real ML model execution",
        "no provider calls",
        "no embeddings or vector store",
        "no prompt library direct access",
        "no freeze-memory direct access",
        "no router final selection modification",
        "no MLRT-113",
        "must not end by enabling runtime ML",
    )
    for phrase in required:
        assert phrase in doc


def test_no_mlrt_113_file_created_by_review_gate() -> None:
    forbidden_names = []
    for path in ROOT.rglob("*"):
        if "__pycache__" in path.parts:
            continue
        name = path.name.lower()
        if "mlrt_113" in name or "mlrt113" in name:
            forbidden_names.append(str(path.relative_to(ROOT)))
    assert forbidden_names == []


def test_phase1a_review_gate_does_not_add_authority_fields() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8").lower()
    forbidden_phrases = (
        "selected route is chosen by ml",
        "ml chooses final route",
        "ml overrides router",
        "runtime shadow mode is enabled",
        "provider call is allowed",
        "embeddings are enabled",
    )
    for phrase in forbidden_phrases:
        assert phrase not in review


def main() -> None:
    test_phase1a_review_gate_docs_exist_and_preserve_scope()
    test_phase1a_review_gate_manifest_is_non_authoritative()
    test_phase1b_readiness_doc_blocks_runtime_ml()
    test_no_mlrt_113_file_created_by_review_gate()
    test_phase1a_review_gate_does_not_add_authority_fields()
    print("VALIDATION OK: rss_ml_adv_phase1a_review_gate_v1")
    print(
        "CONTRACT_TEST_OK: Routing Signal Scorer ML Advisory-Signal Phase 1a "
        "Result Review Gate v1, reviewed the frozen Phase 1a ML Advisory-Signal "
        "and Governed Prompt Intake Boundary Contract as good and safe only for "
        "continued governed implementation; accepted Phase 1a only as "
        "boundary-contract, stub, documentation, and validation evidence, not as "
        "reliability, maturity, production-readiness, runtime ML, or route-authority "
        "evidence; preserved ML Advisory Signal as telemetry only, Governed Prompt "
        "Intake as the only safe door for future prompts, Manual Prompt Code Hint as "
        "classification help only, and the governed router as final selector; "
        "identified the next safe correction as Phase 1b non-runtime design audit, "
        "not real ML integration; added 0 new real prompt-selection cases, created "
        "no MLRT-113, no real ML, no provider calls, no embeddings, no persistence, "
        "no prompt loading, no prompt registry mutation, no freeze-memory write, no "
        "runtime shadow mode, no router prompt logic modification, no router final "
        "selection modification, no route authority, no runtime Pilot, no Copilot "
        "behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_ML_ADV_PHASE1A_REVIEW_GATE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
