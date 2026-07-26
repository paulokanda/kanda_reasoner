from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_31_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_FINAL_HUMAN_REVIEW_GATE_PLAN.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_final_human_review_gate_plan_v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt31_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-31 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Gate Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt31_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-31." in text
    assert "does not create a source file" in text
    assert "does not authorize creating a source file" in text
    assert "testing is still not expected before MLRT-34 or later" in text
    assert "final first-dry-run execution gate" in text


def test_mlrt31_is_final_human_review_gate_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface minimal stub source-file creation patch final human-review gate planning milestone",
        "not source code",
        "not a source-file creation patch",
        "not source-file authorization",
        "not final human review execution",
        "not a final human-review outcome",
        "not source creation approval",
        "not an executable gate",
        "not a boundary checker",
        "not a source creation record",
        "not reliability evidence",
        "does not create Python source files",
        "does not create source files",
        "does not create source-surface files",
        "does not authorize source files",
        "does not grant source creation authorization",
        "does not create source-file authorization records",
        "does not create source-file authorization code",
        "does not create source creation gate code",
        "does not create source-creation records",
        "does not create a source creation patch",
        "does not run final human review",
        "does not create final human-review records",
        "does not create final human-review outcomes",
        "does not approve final human-review outcomes",
        "does not run outcome gates",
        "does not create source file skeletons",
        "does not create implementation modules",
        "does not create a static interface",
        "does not create harness code",
        "does not create runner code",
        "does not create harness stub files",
        "does not execute a dry run",
        "does not execute a candidate",
        "does not create candidate outputs",
        "does not execute cases",
        "does not score cases",
        "does not compare routes",
        "does not generate reports",
        "does not validate candidate reliability",
        "does not unlock ML implementation",
    ]
    for phrase in required:
        assert phrase in text


def test_mlrt31_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-28 - future minimal stub source-file creation patch planning" in text
    assert "MLRT-29 - future minimal stub source-file creation patch safety-review planning" in text
    assert "MLRT-30 - future minimal stub source-file creation patch safety-review outcome-gate planning" in text
    assert "MLRT-31 - future minimal stub source-file creation patch final human-review gate planning" in text
    assert "MLRT-32 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Outcome Gate Plan" in text


def test_mlrt31_defines_future_final_human_review_sections() -> None:
    text = read(DOC)
    for heading in [
        "When tests start",
        "Planned final human-review gate inputs",
        "Planned future source path",
        "Planned final human-review checklist",
        "Planned final human-review required rejection reasons",
        "Planned final human-review allowed outcome vocabulary",
        "Planned final human-review forbidden outcome vocabulary",
        "No implementation doctrine",
        "No testing doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt31_future_inputs_are_read_only_planning() -> None:
    text = read(DOC)
    for phrase in [
        "MLRT-28 freeze evidence",
        "MLRT-29 freeze evidence",
        "MLRT-30 freeze evidence",
        "MLRT-31 freeze evidence",
        "Future safety-review checklist results",
        "Future safety-review outcome-gate notes",
        "Future human review notes",
        "MLRT-31 does not create, fetch, inspect, or validate those inputs",
    ]:
        assert phrase in text


def test_mlrt31_future_source_path_is_not_created_or_authorized() -> None:
    text = read(DOC)
    assert PLANNED_SOURCE in text
    assert "MLRT-31 does not create this path" in text
    assert "does not create the parent folder" in text
    assert "does not authorize creating this path" in text


def test_mlrt31_final_human_review_checklist_is_safe() -> None:
    text = read(DOC)
    for phrase in [
        "MLRT-28, MLRT-29, MLRT-30, and MLRT-31 are frozen",
        "complete non-runtime checklist",
        "no unresolved rejection reasons",
        "explicit, non-authoritative, and closed by default",
        "exactly equals",
        "at most one Python source file",
        "inert, non-runtime, non-authoritative, and standard-library-only",
        "no runtime router imports, prompt-loader imports, provider access, embeddings, vector-store access, persistence, network, subprocess, or batch mode",
        "no candidate execution, case execution, scoring, route comparison, report generation, reliability claim, activation key, field-test mode, runtime Pilot behavior, or Copilot behavior",
        "does not mutate prompt library, router canon, freeze memory, gold registry, fixtures, corpus, runtime configuration, or route authority surfaces",
        "does not start tests, execute a dry run, execute a candidate, execute cases, score cases, compare routes, generate reports, or claim reliability",
        "not source creation now",
    ]:
        assert phrase in text


def test_mlrt31_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    for reason in [
        "missing_mlrt28_freeze",
        "missing_mlrt29_freeze",
        "missing_mlrt30_freeze",
        "missing_mlrt31_freeze",
        "missing_freeze_memory_status_ok",
        "stale_startup_freeze_context",
        "missing_safety_review_result",
        "safety_review_not_run",
        "safety_review_incomplete",
        "safety_review_has_unresolved_rejections",
        "safety_review_ambiguous",
        "missing_outcome_gate_result",
        "outcome_gate_not_run",
        "outcome_gate_incomplete",
        "outcome_gate_ambiguous",
        "outcome_gate_has_unresolved_rejections",
        "missing_final_human_review",
        "final_human_review_not_run",
        "final_human_review_incomplete",
        "final_human_review_ambiguous",
        "final_human_review_has_unresolved_rejections",
        "final_human_review_claims_runtime_approval",
        "final_human_review_claims_reliability",
        "unexpected_source_path",
        "multiple_source_files_requested",
        "source_file_already_exists_without_review",
        "source_file_not_minimal",
        "source_file_not_inert",
        "source_file_not_closed_by_default",
        "source_file_has_runtime_router_import",
        "source_file_has_prompt_loader_import",
        "source_file_has_provider_import",
        "source_file_has_embedding_or_vector_store_import",
        "source_file_has_persistence_import",
        "source_file_has_network_call",
        "source_file_has_subprocess_call",
        "source_file_has_batch_mode",
        "source_file_reads_live_prompt_library",
        "source_file_reads_live_router_canon",
        "source_file_reads_live_freeze_memory",
        "source_file_imports_candidate_package",
        "source_file_executes_candidate",
        "source_file_executes_cases",
        "source_file_scores_cases",
        "source_file_compares_routes",
        "source_file_generates_report",
        "source_file_claims_reliability",
        "source_file_sets_route_authority",
        "source_file_contains_activation_key",
        "source_file_enables_field_test",
        "source_file_enables_runtime_pilot",
        "source_file_enables_copilot",
        "patch_mutates_prompt_library",
        "patch_mutates_router_canon",
        "patch_mutates_freeze_memory",
        "patch_mutates_gold_registry",
        "patch_mutates_fixtures",
        "patch_mutates_corpus",
        "patch_mutates_runtime_configuration",
        "human_review_missing",
        "human_review_not_explicit",
        "human_review_attempts_to_authorize_runtime",
        "human_review_attempts_to_unlock_ml_implementation",
    ]:
        assert reason in text


def test_mlrt31_outcomes_remain_non_authoritative() -> None:
    text = read(DOC)
    for allowed in [
        "FINAL_HUMAN_REVIEW_GATE_NOT_RUN",
        "FINAL_HUMAN_REVIEW_GATE_REJECTED",
        "FINAL_HUMAN_REVIEW_GATE_ABORTED",
        "FINAL_HUMAN_REVIEW_GATE_READY_FOR_OUTCOME_GATE_PLANNING_ONLY",
    ]:
        assert allowed in text
    for forbidden in [
        "SOURCE_FILE_CREATED_BY_HUMAN_REVIEW_GATE",
        "SOURCE_CREATION_APPROVED_FOR_RUNTIME",
        "SOURCE_CREATION_AUTHORIZED_NOW",
        "DRY_RUN_READY",
        "TESTING_STARTED",
        "CANDIDATE_EXECUTED",
        "CASE_SCORED",
        "ROUTE_APPROVED",
        "RELIABILITY_VALIDATED",
        "ML_IMPLEMENTATION_UNLOCKED",
        "RUNTIME_PILOT_ENABLED",
        "COPILOT_ENABLED",
    ]:
        assert forbidden in text


def test_mlrt31_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_FINAL_HUMAN_REVIEW_GATE_PLAN_READY_FOR_FINAL_HUMAN_REVIEW_OUTCOME_GATE_PLANNING_ONLY" in text
    assert "does not mean tests can start" in text
    assert "does not mean source creation is authorized" in text
    assert "does not mean a source file exists" in text
    assert "does not mean source files may be created now" in text
    assert "does not mean a source creation patch exists" in text
    assert "does not mean a source creation record exists" in text
    assert "does not mean source creation code exists" in text
    assert "does not mean final human review has run" in text
    assert "does not mean a final human-review outcome exists" in text
    assert "does not mean an outcome gate has run" in text
    assert "does not mean a source surface exists" in text
    assert "does not mean a static interface exists" in text
    assert "does not mean a harness exists" in text
    assert "does not mean a dry run has executed" in text
    assert "does not mean candidate reliability is validated" in text
    assert "does not mean ML implementation is unlocked" in text


def test_mlrt31_manifest_records_planning_only_boundaries() -> None:
    import json

    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_final_human_review_gate_plan_"
    assert data[prefix + "feature_id"] == FEATURE_ID
    assert data[prefix + "documentation_only"] is True
    assert data[prefix + "final_human_review_gate_planning_only"] is True
    assert data[prefix + "testing_started"] is False
    assert data[prefix + "source_creation_authorized"] is False
    assert data[prefix + "python_source_files_created"] is False
    assert data[prefix + "source_files_created"] is False
    assert data[prefix + "source_patch_created"] is False
    assert data[prefix + "safety_review_run"] is False
    assert data[prefix + "safety_review_outcome_created"] is False
    assert data[prefix + "outcome_gate_run"] is False
    assert data[prefix + "outcome_gate_records_created"] is False
    assert data[prefix + "final_human_review_run"] is False
    assert data[prefix + "final_human_review_records_created"] is False
    assert data[prefix + "final_human_review_outcome_created"] is False
    assert data[prefix + "source_creation_records_created"] is False
    assert data[prefix + "source_creation_code_created"] is False
    assert data[prefix + "source_surface_created"] is False
    assert data[prefix + "static_interface_created"] is False
    assert data[prefix + "harness_created"] is False
    assert data[prefix + "harness_stub_files_created"] is False
    assert data[prefix + "dry_run_executed"] is False
    assert data[prefix + "candidate_reliability_validated"] is False
    assert data[prefix + "ml_implementation_unlocked"] is False
    assert data[prefix + "route_authority"] is False
    assert data[prefix + "prompt_loading"] is False
    assert data[prefix + "provider_calls"] is False
    assert data[prefix + "persistence"] is False
    assert data[prefix + "runtime_pilot_behavior"] is False
    assert data[prefix + "copilot_behavior"] is False
    assert data[prefix + "critical_boundary_error_budget"] == 0
    assert data[prefix + "planned_future_source_path"] == PLANNED_SOURCE
    assert data[prefix + "next_safe_milestone"] == "MLRT-32 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Outcome Gate Plan after MLRT-31 freeze with FREEZE_MEMORY_STATUS OK"


def test_mlrt31_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt31_does_not_create_forbidden_implementation_paths() -> None:
    forbidden_paths = [
        "candidate", "candidate_package", "candidate_packages", "candidate_outputs", "candidate_results",
        "package_intake_records", "static_review", "static_review_records", "static_review_results",
        "static_review_evidence", "static_review_evidence_records", "static_review_outcome", "static_review_outcome_records",
        "outcome_gate", "outcome_gate_records", "final_human_review", "final_human_review_records",
        "final_human_review_outcome", "final_human_review_outcomes", "final_human_review_outcome_gate", "final_human_review_outcome_gate_records",
        "dry_run", "dry_run_execution", "dry_run_execution_records", "dry_run_readiness", "dry_run_readiness_records",
        "dry_run_protocol", "dry_run_protocol_records", "dry_run_protocol_execution_records", "dry_run_inputs",
        "dry_run_input_records", "dry_run_input_manifests", "dry_run_outputs", "dry_run_output_records",
        "dry_run_output_manifests", "output_capture", "output_capture_envelopes", "output_capture_records",
        "output_capture_rejection_records", "output_rejection_gate", "output_rejection_gate_records",
        "contract_conformance", "contract_conformance_records", "contract_conformance_evidence",
        "contract_conformance_rejection_gate", "contract_conformance_rejection_records", "conformance_checker",
        "harness", "runner", "harness_skeleton", "harness_contract", "harness_stub", "boundary_checker",
        "boundary_confirmation", "boundary_confirmation_code", "contract_schema", "schema", "schemas", "source_surface", "source_surface_files",
        "source_file_authorization", "source_file_authorization_records", "source_file_authorization_code", "source_creation_gate",
        "source_creation_records", "source_creation_code", "source_file_skeletons", "source_creation_patch",
        "source_creation_patch_safety_review", "safety_review", "safety_review_records", "safety_review_outcome", "safety_review_outcomes",
        "source_creation_patch_safety_review_outcome_gate", "source_creation_patch_safety_review_outcome_gate_records",
        "minimal_non_runtime_harness_stub.py", "static_interface", "static_interface_files", "abort_contract", "abort_contract_code",
        "abort_gate", "rejection_contract", "rejection_contract_code", "rejection_gate", "readiness_gate", "readiness_gate_code",
        "test_start_readiness", "test_start_readiness_gate", "implementation_modules", "evidence_envelopes", "reliability_results",
        "runtime_activation", "provider_adapter", "embedding_adapter", "prompt_loader", "persistent_ml_decisions", "reports", "validators", "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_mlrt31_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert "MLRT-31 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Gate Plan v1" in readme
    assert FEATURE_ID in manifest
    assert "MLRT-32 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Outcome Gate Plan" in readme
    assert "Tests do not start at MLRT-31" in readme


if __name__ == "__main__":
    test_mlrt31_docs_exist()
    test_mlrt31_tests_do_not_start_yet()
    test_mlrt31_is_final_human_review_gate_planning_only()
    test_mlrt31_records_roadmap_progression()
    test_mlrt31_defines_future_final_human_review_sections()
    test_mlrt31_future_inputs_are_read_only_planning()
    test_mlrt31_future_source_path_is_not_created_or_authorized()
    test_mlrt31_final_human_review_checklist_is_safe()
    test_mlrt31_rejection_reasons_are_comprehensive()
    test_mlrt31_outcomes_remain_non_authoritative()
    test_mlrt31_positive_label_is_planning_only()
    test_mlrt31_manifest_records_planning_only_boundaries()
    test_mlrt31_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt31_does_not_create_forbidden_implementation_paths()
    test_mlrt31_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-31 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Gate Plan v1, "
        "immutable governed documentation-only final human-review gate planning after MLRT-30 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, testing still not expected before MLRT-34 or later if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source files authorized, no source files created, "
        "no source creation authorization granted, no source creation records created, no source creation code created, no source creation patch created, "
        "no safety review run, no safety-review records created, no safety-review outcomes created, no safety-review outcome approved, no outcome gate run, "
        "no outcome-gate records created, no final human review run, no final human-review records created, no final human-review outcomes created, "
        "no final human-review outcome approved, no source file skeletons created, no source surface created, no static interface created, no harness created, no runner created, "
        "no harness stub files created, no dry run executed, no candidate execution, no candidate outputs created, no case execution, no case scoring, "
        "no route comparison, no route authority, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, "
        "no persistence, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, "
        "next safe milestone is MLRT-32 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Final Human Review Outcome Gate Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_FINAL_HUMAN_REVIEW_GATE_PLAN_V1_VALIDATION_OK")
