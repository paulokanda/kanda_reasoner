"""Contract tests for LAB-11 Corpus V1 Expansion v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1"
CONTRACT_DOC = LAB_BOX / "LAB_CORPUS_V1_EXPANSION.md"
CORPUS = LAB_BOX / "corpus_v1" / "corpus_v1_expansion_seed_v1.json"
HASH_MANIFEST = LAB_BOX / "corpus_v1" / "corpus_v1_expansion_seed_v1_hash_manifest.json"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
ALLOWED_LAB_PYTHON_FILES = [
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py",
]
FORBIDDEN_AUTHORITY_FIELDS = [
    "route_decision",
    "load_prompt",
    "execute_route",
    "approve_readiness",
    "record_human_approval",
    "write_freeze_memory",
    "write_gold_registry",
    "write_prompt_library",
    "write_router_canon",
    "activate_pilot",
    "activate_copilot",
    "enable_field_test",
    "call_provider",
    "call_embedding_model",
    "start_batch_mode",
    "persist_ml_decision",
    "runtime_command",
    "copilot_instruction",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path):
    return json.loads(_read(path))


def test_lab11_files_exist_and_python_surface_is_unchanged() -> None:
    assert CONTRACT_DOC.is_file()
    assert CORPUS.is_file()
    assert HASH_MANIFEST.is_file()
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    assert python_files == ALLOWED_LAB_PYTHON_FILES


def test_lab11_doc_declares_static_non_runtime_corpus_expansion_only() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    for phrase in (
        "static Corpus V1 expansion seed",
        "48 static Corpus V1 expansion cases",
        "combined static corpus coverage after LAB-11 is therefore 60 cases",
        "not reliability evidence",
        "does not evaluate candidates",
        "does not compare routes",
        "does not load prompts",
        "does not read live prompt-library files",
        "does not read live freeze memory",
        "does not create a scoring engine",
        "Critical boundary error budget: zero",
        "LAB-12 - Error Canonization Intake Spec",
    ):
        assert phrase in text, phrase


def test_lab11_corpus_shape_and_non_authority_declarations() -> None:
    corpus = _load_json(CORPUS)
    assert corpus["feature_id"] == FEATURE_ID
    assert corpus["schema_version"] == "lab-11-corpus-v1-expansion"
    assert corpus["status"] == "static_expansion_only_not_executed_not_scored_not_reliability_evidence"
    assert corpus["alpha_case_count_reference"] == 12
    assert corpus["case_count"] == 48
    assert corpus["combined_static_case_count_after_lab11"] == 60
    assert corpus["target_corpus_v1_case_count_later"] == 100
    assert len(corpus["cases"]) == corpus["case_count"]
    declarations = corpus["non_authority_declarations"]
    for key, value in declarations.items():
        assert value is False, key


def test_lab11_cases_cover_expected_governance_categories_without_execution() -> None:
    corpus = _load_json(CORPUS)
    categories = {case["case_category"] for case in corpus["cases"]}
    expected_categories = {
        "fast_path_simple_task",
        "medical_document_distinction",
        "governed_project_patch",
        "governed_project_audit",
        "multi_turn_shorthand",
        "missing_context",
        "lab_roadmap_lock",
        "critical_boundary_violation",
        "freeze_governance",
        "patch_delivery_governance",
        "prompt_library_governance",
        "startup_delivery_governance",
        "prompt_injection_bypass",
        "box_boundary_leakage",
        "candidate_output_shielding",
        "stale_context_rejection",
        "multilingual_ambiguous",
        "typo_shorthand",
        "error_canonization_boundary",
    }
    assert expected_categories <= categories
    paths = {case["expected"]["path"] for case in corpus["cases"]}
    assert "Fast Path" in paths
    assert "Routed Work Path" in paths
    assert any(case["critical_boundary_flag"] is True for case in corpus["cases"])
    assert any(case["adversarial_flag"] is True for case in corpus["cases"])
    for case in corpus["cases"]:
        assert case["static_seed_status"] == "not_executed_not_scored_not_reliability_evidence"
        assert case["candidate_evaluation_status"] == "not_executed"
        assert case["route_authority_granted"] is False
        assert case["prompt_loading_allowed"] is False
        assert case["provider_calls_allowed"] is False
        assert case["embedding_calls_allowed"] is False
        assert case["persistence_allowed"] is False
        assert case["activation_allowed"] is False
        assert case["field_test_allowed"] is False
        assert case["runtime_pilot_allowed"] is False
        assert case["copilot_behavior_allowed"] is False


def test_lab11_case_contract_fields_are_complete_and_non_authoritative() -> None:
    corpus = _load_json(CORPUS)
    required_fields = {
        "case_id",
        "case_version",
        "schema_version",
        "corpus_id",
        "corpus_version",
        "case_category",
        "case_subcategory",
        "scenario",
        "severity",
        "critical_boundary_flag",
        "adversarial_flag",
        "regression_source",
        "canon_version_reference",
        "canon_rule_references",
        "fixture_hash_reference",
        "expected",
        "rubric",
        "candidate_output_contract",
        "static_seed_status",
        "candidate_evaluation_status",
    }
    seen = set()
    for case in corpus["cases"]:
        assert required_fields <= set(case), case["case_id"]
        assert case["case_id"] not in seen
        seen.add(case["case_id"])
        assert case["schema_version"] == "lab-11-corpus-v1-expansion"
        assert case["candidate_output_contract"]["must_be_wrapped_as"] == "non_authoritative_evaluation_record"
        assert case["candidate_output_contract"]["must_use_two_pass_match_before_disagree"] is True
        assert case["candidate_output_contract"]["must_yield_to_canon"] is True
        assert case["candidate_output_contract"]["forbidden_authority_fields"] == FORBIDDEN_AUTHORITY_FIELDS
        assert set(case).isdisjoint(FORBIDDEN_AUTHORITY_FIELDS)


def test_lab11_hash_manifest_matches_static_corpus_sha256() -> None:
    hash_manifest = _load_json(HASH_MANIFEST)
    assert hash_manifest["feature_id"] == FEATURE_ID
    assert hash_manifest["schema_version"] == "lab-11-corpus-v1-expansion"
    assert hash_manifest["hash_algorithm"] == "SHA-256"
    assert hash_manifest["fixture_entries"] == []
    entries = hash_manifest["corpus_entries"]
    assert len(entries) == 1
    digest = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    assert entries[0]["sha256"] == digest
    assert entries[0]["case_count"] == 48
    assert entries[0]["combined_static_case_count_after_lab11"] == 60
    assert entries[0]["static_seed_status"] == "not_executed_not_scored_not_reliability_evidence"
    declarations = hash_manifest["non_authority_declarations"]
    for key, value in declarations.items():
        assert value is False, key


def test_lab11_manifest_metadata_declares_static_expansion_without_authority() -> None:
    data = _load_json(MANIFEST)
    assert data["ml_lab_corpus_v1_expansion_feature_id"] == FEATURE_ID
    assert data["ml_lab_corpus_v1_expansion_schema_version"] == "lab-11-corpus-v1-expansion"
    assert data["ml_lab_corpus_v1_expansion_static_only"] is True
    assert data["ml_lab_corpus_v1_expansion_case_count"] == 48
    assert data["ml_lab_corpus_v1_expansion_alpha_case_count_reference"] == 12
    assert data["ml_lab_corpus_v1_expansion_combined_static_case_count_after_lab11"] == 60
    assert data["ml_lab_corpus_v1_expansion_target_corpus_v1_case_count_later"] == 100
    assert data["ml_lab_corpus_v1_expansion_not_reliability_evidence"] is True
    assert data["ml_lab_corpus_v1_expansion_candidate_evaluation_executed"] is False
    assert data["ml_lab_corpus_v1_expansion_cases_executed"] is False
    assert data["ml_lab_corpus_v1_expansion_cases_scored"] is False
    assert data["ml_lab_corpus_v1_expansion_route_comparison"] is False
    assert data["ml_lab_corpus_v1_expansion_route_authority"] is False
    assert data["ml_lab_corpus_v1_expansion_prompt_loading"] is False
    assert data["ml_lab_corpus_v1_expansion_provider_calls"] is False
    assert data["ml_lab_corpus_v1_expansion_embedding_calls"] is False
    assert data["ml_lab_corpus_v1_expansion_activation_key"] is False
    assert data["ml_lab_corpus_v1_expansion_field_test_mode"] is False
    assert data["ml_lab_corpus_v1_expansion_runtime_pilot"] is False
    assert data["ml_lab_corpus_v1_expansion_copilot_behavior"] is False
    assert data["ml_lab_corpus_v1_expansion_critical_boundary_error_budget"] == 0
    assert data["ml_lab_corpus_v1_expansion_corpus_sha256"] == hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    assert data["ml_lab_corpus_v1_expansion_hash_manifest_sha256"] == hashlib.sha256(HASH_MANIFEST.read_bytes()).hexdigest()
    assert data["ml_lab_corpus_v1_expansion_allowed_lab_python_files"] == ALLOWED_LAB_PYTHON_FILES
    assert "LAB-12 Error Canonization Intake Spec" in data["ml_lab_corpus_v1_expansion_next_safe_milestone"]


if __name__ == "__main__":
    test_lab11_files_exist_and_python_surface_is_unchanged()
    test_lab11_doc_declares_static_non_runtime_corpus_expansion_only()
    test_lab11_corpus_shape_and_non_authority_declarations()
    test_lab11_cases_cover_expected_governance_categories_without_execution()
    test_lab11_case_contract_fields_are_complete_and_non_authoritative()
    test_lab11_hash_manifest_matches_static_corpus_sha256()
    test_lab11_manifest_metadata_declares_static_expansion_without_authority()
    print(
        "CONTRACT_TEST_OK: LAB-11 ML LAB Corpus V1 Expansion v1, "
        "immutable governed static corpus expansion after LAB-10 freeze with FREEZE_MEMORY_STATUS OK, "
        "adds 48 static non-authoritative Corpus V1 expansion cases for 60 combined static cases after LAB-11, "
        "cases not executed or scored, candidate evaluation not executed, not reliability evidence, "
        "no route comparison, no route authority, no prompt loading, no live prompt-library reads, "
        "no live freeze-memory reads, no live router-canon reads, no runtime router imports, "
        "no fixture reads, no actual fixture snapshots, no corpus mutation outside governed static files, "
        "no scoring engine, no metrics engine, no executable candidate harness, no report generation, "
        "no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, "
        "no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, "
        "no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, "
        "zero critical boundary doctrine preserved, ML implementation continuation remains blocked until "
        "LAB/test fulfills its mission and ML router prompt logic reliability is validated, "
        "LAB-12 Error Canonization Intake Spec next"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CORPUS_V1_EXPANSION_V1_VALIDATION_OK")
