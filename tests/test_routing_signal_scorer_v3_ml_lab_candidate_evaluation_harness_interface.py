from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation"
DOC = LAB_BOX / "LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE.md"
MODULE = LAB_BOX / "candidate_evaluation_harness_interface.py"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1"
ALLOWED_LAB_PYTHON_FILES = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
FORBIDDEN_RUNTIME_SNIPPETS = [
    "requests.", "urllib.", "httpx", "socket", "os.system", "Popen", "eval(", "exec(",
    "open(", "Path(", "read_text", "read_bytes", "write_text", "write_bytes", "importlib.import_module",
]


def _lab_python_files() -> list[str]:
    return sorted(
        p.relative_to(PROJECT_ROOT).as_posix()
        for p in LAB_BOX.rglob("*.py")
        if "__pycache__" not in p.parts
    )


def _load_module():
    return importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.lab_non_runtime_router_evaluation.candidate_evaluation_harness_interface"
    )


def test_lab10_files_and_python_boundary():
    assert DOC.exists()
    assert MODULE.exists()
    assert _lab_python_files() == ALLOWED_LAB_PYTHON_FILES


def test_lab10_module_source_has_no_runtime_or_io_patterns():
    source = MODULE.read_text(encoding="utf-8")
    for snippet in FORBIDDEN_RUNTIME_SNIPPETS:
        assert snippet not in source
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    assert imports == ["__future__", "dataclasses", "hashlib", "json", "types", "typing"]


def test_lab10_record_contract():
    mod = _load_module()
    record = mod.get_lab10_candidate_harness_interface_record()
    assert record.feature_id == FEATURE_ID
    assert record.schema_version == "lab-10-candidate-evaluation-harness-interface"
    assert record.design_kind == "non_runtime_candidate_evaluation_harness_interface_only"
    assert record.storage_status == "in_memory_only"
    assert record.routing_effect == "none"
    assert record.prompt_loading_effect == "none"
    assert record.runtime_effect == "none"
    assert record.activation_effect == "none"
    assert record.critical_boundary_error_budget == 0
    assert "candidate_output_metadata" in record.required_interface_inputs
    assert "no forbidden authority fields in candidate output metadata" in record.required_preconditions
    assert "route_decision" in record.forbidden_authority_fields
    assert "evaluate_candidate_output" in record.forbidden_operations
    assert "score_candidate_output" in record.forbidden_operations
    assert "compare_routes" in record.forbidden_operations
    assert "load_prompt" in record.forbidden_operations
    assert "call_provider" in record.forbidden_operations
    assert record.next_safe_milestone == "LAB-11 Corpus V1 Expansion"


def test_lab10_not_evaluated_envelope_is_non_authoritative():
    mod = _load_module()
    envelope = mod.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="lab-run-alpha-001",
        candidate_id="candidate-a",
        candidate_version="0.0.1",
        candidate_output_reference="memory://candidate-a/output",
        candidate_output_metadata={"non_authoritative_evaluation_record": True, "candidate_note": "metadata only"},
        test_case_reference="alpha-001",
        corpus_version="alpha_corpus_seed_v1",
        fixture_manifest_hash="abc123",
        self_validation_status="LAB_SELF_VALIDATION_PASS",
    )
    assert envelope.outcome == "NOT_EVALUATED"
    assert envelope.forbidden_authority_fields_present == ()
    assert envelope.non_authoritative is True
    assert envelope.candidate_evaluation_executed is False
    assert envelope.candidate_evaluation_allowed_by_this_interface is False
    assert envelope.case_execution_performed is False
    assert envelope.case_scoring_performed is False
    assert envelope.route_comparison_performed is False
    assert envelope.route_authority_granted is False
    assert envelope.prompt_loading_performed is False
    assert envelope.provider_call_performed is False
    assert envelope.embedding_call_performed is False
    assert envelope.persistence_performed is False
    assert envelope.report_generated is False
    assert envelope.report_persisted is False
    assert envelope.activation_performed is False
    assert envelope.field_test_performed is False
    assert envelope.runtime_pilot_behavior_performed is False
    assert envelope.copilot_behavior_performed is False
    assert envelope.next_safe_milestone == "LAB-11 Corpus V1 Expansion"


def test_lab10_rejects_forbidden_authority_fields_without_evaluating():
    mod = _load_module()
    envelope = mod.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="lab-run-alpha-002",
        candidate_id="candidate-b",
        candidate_version="0.0.1",
        candidate_output_reference="memory://candidate-b/output",
        candidate_output_metadata={"route_decision": "Fast Path", "load_prompt": "prompt_x"},
        test_case_reference="alpha-002",
        corpus_version="alpha_corpus_seed_v1",
        fixture_manifest_hash="abc123",
        self_validation_status="LAB_SELF_VALIDATION_PASS",
    )
    assert envelope.outcome == "HARNESS_INTERFACE_REJECTED"
    assert envelope.forbidden_authority_fields_present == ("route_decision", "load_prompt")
    assert envelope.candidate_evaluation_executed is False
    assert envelope.route_authority_granted is False
    assert envelope.prompt_loading_performed is False


def test_lab10_hashing_is_deterministic_and_read_only_mapping():
    mod = _load_module()
    metadata_a = {"b": 2, "a": 1}
    metadata_b = {"a": 1, "b": 2}
    assert mod.canonicalize_candidate_output_metadata(metadata_a) == mod.canonicalize_candidate_output_metadata(metadata_b)
    assert mod.compute_candidate_output_metadata_hash(metadata_a) == mod.compute_candidate_output_metadata_hash(metadata_b)
    envelope = mod.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="lab-run-alpha-003",
        candidate_id="candidate-c",
        candidate_version="0.0.1",
        candidate_output_reference="memory://candidate-c/output",
        candidate_output_metadata=metadata_a,
        test_case_reference="alpha-003",
        corpus_version="alpha_corpus_seed_v1",
        fixture_manifest_hash="abc123",
        self_validation_status="LAB_SELF_VALIDATION_PASS",
    )
    mapping = mod.as_read_only_mapping(envelope)
    assert mapping["outcome"] == "NOT_EVALUATED"
    try:
        mapping["outcome"] = "PASS"  # type: ignore[index]
    except TypeError:
        pass
    else:
        raise AssertionError("mapping must be read-only")


def test_lab10_docs_and_manifest_contract():
    doc = DOC.read_text(encoding="utf-8")
    for phrase in [
        FEATURE_ID,
        "non-runtime candidate evaluation harness interface only",
        "not the harness itself",
        "does not evaluate candidates",
        "does not execute any case or candidate",
        "HARNESS_INTERFACE_REJECTED",
        "NOT_EVALUATED",
        "critical boundary error budget remains `0`",
        "LAB-11 — Corpus V1 Expansion",
    ]:
        assert phrase in doc
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["ml_lab_candidate_harness_interface_feature_id"] == FEATURE_ID
    assert data["ml_lab_candidate_harness_interface_allowed_python_modules"] == ALLOWED_LAB_PYTHON_FILES
    assert data["ml_lab_candidate_harness_interface_contains_candidate_evaluation"] is False
    assert data["ml_lab_candidate_harness_interface_contains_case_execution"] is False
    assert data["ml_lab_candidate_harness_interface_contains_case_scoring"] is False
    assert data["ml_lab_candidate_harness_interface_contains_route_comparison"] is False
    assert data["ml_lab_candidate_harness_interface_contains_route_authority"] is False
    assert data["ml_lab_candidate_harness_interface_contains_prompt_loading"] is False
    assert data["ml_lab_candidate_harness_interface_contains_provider_calls"] is False
    assert data["ml_lab_candidate_harness_interface_contains_embeddings"] is False
    assert data["ml_lab_candidate_harness_interface_contains_report_generation"] is False
    assert data["ml_lab_candidate_harness_interface_contains_report_persistence"] is False
    assert data["ml_lab_candidate_harness_interface_critical_boundary_error_budget"] == 0
    assert data["ml_lab_candidate_harness_interface_next_safe_milestone"] == "LAB-11 Corpus V1 Expansion after local validation and freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_lab10_files_and_python_boundary()
    test_lab10_module_source_has_no_runtime_or_io_patterns()
    test_lab10_record_contract()
    test_lab10_not_evaluated_envelope_is_non_authoritative()
    test_lab10_rejects_forbidden_authority_fields_without_evaluating()
    test_lab10_hashing_is_deterministic_and_read_only_mapping()
    test_lab10_docs_and_manifest_contract()
    print("VALIDATION OK: routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1")
    print(
        "CONTRACT_TEST_OK: LAB-10 ML LAB Candidate Evaluation Harness Interface v1, immutable governed non-runtime in-memory candidate harness interface after LAB-9 freeze with FREEZE_MEMORY_STATUS OK, adds exactly one new allowed LAB Python interface file, accepts caller-supplied candidate metadata and references only, returns NOT_EVALUATED or HARNESS_INTERFACE_REJECTED only, computes deterministic SHA-256 metadata hashes, blocks forbidden authority fields, candidate evaluation not executed, cases not executed or scored, reports not generated or persisted, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixture snapshots, no corpus mutation, no scoring engine, no metrics engine, no executable candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-11 Corpus V1 Expansion next"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
