"""Contract tests for LAB-8 Alpha Corpus Seed v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1"
CONTRACT_DOC = LAB_BOX / "LAB_ALPHA_CORPUS_SEED.md"
CORPUS = LAB_BOX / "alpha_corpus" / "alpha_corpus_seed_v1.json"
HASH_MANIFEST = LAB_BOX / "alpha_corpus" / "alpha_corpus_seed_v1_hash_manifest.json"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
ALLOWED_LAB_PYTHON_FILES = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
FORBIDDEN_AUTHORITY_FIELDS = ['route_decision', 'load_prompt', 'execute_route', 'approve_readiness', 'record_human_approval', 'write_freeze_memory', 'write_gold_registry', 'write_prompt_library', 'write_router_canon', 'activate_pilot', 'activate_copilot', 'enable_field_test', 'call_provider', 'call_embedding_model', 'start_batch_mode', 'persist_ml_decision', 'runtime_command', 'copilot_instruction']


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path):
    return json.loads(_read(path))


def test_lab8_files_exist_and_python_surface_is_unchanged() -> None:
    assert CONTRACT_DOC.is_file()
    assert CORPUS.is_file()
    assert HASH_MANIFEST.is_file()
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    assert python_files == ALLOWED_LAB_PYTHON_FILES


def test_lab8_doc_declares_static_non_runtime_corpus_seed_only() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    for phrase in (
        "small governed static alpha corpus seed",
        "static corpus seed only",
        "not reliability evidence",
        "does not evaluate candidates",
        "does not compare routes",
        "does not load prompts",
        "does not read live prompt-library content",
        "does not read live freeze memory",
        "does not create a runner",
        "Critical boundary error budget: zero",
        "LAB-9 — Offline Observability + Experiment Report",
    ):
        assert phrase in text, phrase


def test_lab8_corpus_shape_and_case_count_are_static_seed_only() -> None:
    corpus = _load_json(CORPUS)
    assert corpus["feature_id"] == FEATURE_ID
    assert corpus["schema_version"] == "lab-8-alpha-corpus-seed"
    assert corpus["status"] == "static_seed_only_not_executed_not_scored_not_reliability_evidence"
    assert corpus["case_count"] == 12
    assert len(corpus["cases"]) == corpus["case_count"]
    assert corpus["non_authority_declarations"]["candidate_evaluation_executed"] is False
    assert corpus["non_authority_declarations"]["route_authority_granted"] is False
    assert corpus["non_authority_declarations"]["prompt_loading_performed"] is False
    assert corpus["non_authority_declarations"]["provider_call_performed"] is False
    assert corpus["non_authority_declarations"]["embedding_call_performed"] is False
    assert corpus["non_authority_declarations"]["persistence_performed"] is False
    assert corpus["non_authority_declarations"]["runtime_pilot_behavior_performed"] is False
    assert corpus["non_authority_declarations"]["copilot_behavior_performed"] is False


def test_lab8_cases_cover_expected_governance_categories_without_execution() -> None:
    corpus = _load_json(CORPUS)
    categories = {case["case_category"] for case in corpus["cases"]}
    for expected in (
        "simple_task_fast_path",
        "governed_project_patch",
        "bypass_attempt_prompt_authoring",
        "freeze_governance",
        "box_boundary",
        "critical_boundary_violation",
        "fixture_boundary",
        "missing_context",
        "match_before_disagree",
        "lab_roadmap",
    ):
        assert expected in categories
    paths = {case["expected"]["path"] for case in corpus["cases"]}
    assert "Fast Path" in paths
    assert "Routed Work Path" in paths
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


def test_lab8_case_contract_fields_are_complete_and_non_authoritative() -> None:
    corpus = _load_json(CORPUS)
    required_fields = {
        "case_id", "case_version", "schema_version", "corpus_id", "corpus_version", "case_category", "scenario",
        "canon_version_reference", "canon_rule_references", "fixture_hash_reference", "expected", "rubric",
        "candidate_output_contract", "static_seed_status", "candidate_evaluation_status",
    }
    for case in corpus["cases"]:
        assert required_fields <= set(case), case["case_id"]
        assert case["candidate_output_contract"]["must_be_wrapped_as"] == "non_authoritative_evaluation_record"
        assert case["candidate_output_contract"]["must_use_two_pass_match_before_disagree"] is True
        assert case["candidate_output_contract"]["must_yield_to_canon"] is True
        assert case["candidate_output_contract"]["forbidden_authority_fields"] == FORBIDDEN_AUTHORITY_FIELDS
        assert set(case).isdisjoint(FORBIDDEN_AUTHORITY_FIELDS)


def test_lab8_hash_manifest_matches_static_corpus_sha256() -> None:
    hash_manifest = _load_json(HASH_MANIFEST)
    assert hash_manifest["feature_id"] == FEATURE_ID
    assert hash_manifest["hash_algorithm"] == "SHA-256"
    assert hash_manifest["fixture_entries"] == []
    entries = hash_manifest["corpus_entries"]
    assert len(entries) == 1
    digest = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    assert entries[0]["sha256"] == digest
    assert entries[0]["case_count"] == 12
    assert entries[0]["static_seed_status"] == "not_executed_not_scored_not_reliability_evidence"
    assert hash_manifest["non_authority_declarations"]["candidate_evaluation_executed"] is False
    assert hash_manifest["non_authority_declarations"]["route_authority_granted"] is False
    assert hash_manifest["non_authority_declarations"]["prompt_loading_performed"] is False


def test_lab8_manifest_metadata_declares_static_corpus_without_authority() -> None:
    data = _load_json(MANIFEST)
    assert data["ml_lab_alpha_corpus_seed_feature_id"] == FEATURE_ID
    assert data["ml_lab_alpha_corpus_seed_schema_version"] == "lab-8-alpha-corpus-seed"
    assert data["ml_lab_alpha_corpus_seed_case_count"] == 12
    assert data["ml_lab_alpha_corpus_seed_contains_static_corpus"] is True
    assert data["ml_lab_alpha_corpus_seed_contains_hash_manifest_data"] is True
    assert data["ml_lab_alpha_corpus_seed_contains_actual_fixtures"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_lab_python_modules"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_candidate_evaluation"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_route_comparison"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_route_authority"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_prompt_loading"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_persistence"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_provider_calls"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_embeddings"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_batch_mode"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_activation_key"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_field_test_mode"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_runtime_pilot"] is False
    assert data["ml_lab_alpha_corpus_seed_contains_copilot_behavior"] is False
    assert data["ml_lab_alpha_corpus_seed_corpus_sha256"] == hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    assert data["ml_lab_alpha_corpus_seed_critical_boundary_error_budget"] == 0
    assert "LAB-9 Offline Observability + Experiment Report" in data["ml_lab_alpha_corpus_seed_next_safe_milestone"]


if __name__ == "__main__":
    test_lab8_files_exist_and_python_surface_is_unchanged()
    test_lab8_doc_declares_static_non_runtime_corpus_seed_only()
    test_lab8_corpus_shape_and_case_count_are_static_seed_only()
    test_lab8_cases_cover_expected_governance_categories_without_execution()
    test_lab8_case_contract_fields_are_complete_and_non_authoritative()
    test_lab8_hash_manifest_matches_static_corpus_sha256()
    test_lab8_manifest_metadata_declares_static_corpus_without_authority()
    print(
        "CONTRACT_TEST_OK: LAB-8 ML LAB Alpha Corpus Seed v1, "
        "immutable governed static alpha corpus seed after LAB-7 freeze with FREEZE_MEMORY_STATUS OK, "
        "adds 12 static non-authoritative alpha cases and a SHA-256 static corpus hash manifest, covers simple-vs-governed routing, freeze governance, prompt-authoring bypass, box boundaries, prompt-loading prohibition, live-fixture prohibition, missing context, match-before-disagree, and LAB roadmap lock, "
        "candidate evaluation not executed, cases not scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-9 Offline Observability + Experiment Report next"
    )
