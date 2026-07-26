from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_27_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_AUTHORIZATION_GATE_PLAN.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_authorization_gate_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt27_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt27_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-27." in text
    assert "does not create a source file" in text
    assert "does not authorize creating a source file" in text
    assert "testing is now not expected before MLRT-30 or later" in text
    assert "final first-dry-run execution gate" in text


def test_mlrt27_is_authorization_gate_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface minimal stub source-file creation authorization-gate planning milestone",
        "not source-file creation",
        "not source-file authorization",
        "not a creation approval",
        "not an executable gate",
        "not a boundary checker",
        "not a source creation record",
        "not reliability evidence",
        "does not create Python source files",
        "does not create source files",
        "does not create source-surface files",
        "does not authorize source files",
        "does not create source-file authorization records",
        "does not create source-file authorization code",
        "does not create source creation gate code",
        "does not create source-creation records",
        "does not create source file skeletons",
        "does not create implementation modules",
        "does not create boundary-checker code",
        "does not create readiness-gate code",
        "does not create rejection-contract code",
        "does not create abort-contract code",
        "does not create executable readiness gates",
        "does not create executable rejection gates",
        "does not create executable abort gates",
        "does not create a static interface",
        "does not create static-interface files",
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


def test_mlrt27_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-22 - future test-start readiness-gate planning" in text
    assert "MLRT-23 - future source/implementation boundary-confirmation planning" in text
    assert "MLRT-24 - future source-file authorization planning" in text
    assert "MLRT-25 - future stub source creation gate planning" in text
    assert "MLRT-26 - future minimal stub source file planning" in text
    assert "MLRT-27 - future minimal stub source-file creation authorization-gate planning" in text
    assert "MLRT-28 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Plan" in text


def test_mlrt27_defines_future_authorization_gate_sections() -> None:
    text = read(DOC)
    for heading in [
        "When tests start",
        "Future authorization gate inputs",
        "Future authorization gate required rejection reasons",
        "Future authorization gate allowed outcome vocabulary",
        "Future authorization gate forbidden outcome vocabulary",
        "Future source-file creation dependency",
        "No implementation doctrine",
        "No testing doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt27_authorization_inputs_are_closed() -> None:
    text = read(DOC)
    assert "MLRT-25 freeze with `FREEZE_MEMORY_STATUS: OK`." in text
    assert "MLRT-26 freeze with `FREEZE_MEMORY_STATUS: OK`." in text
    assert "MLRT-27 freeze with `FREEZE_MEMORY_STATUS: OK`." in text
    assert "source_surface/minimal_non_runtime_harness_stub.py" in text
    assert "inert, non-runtime, non-authoritative, standard-library-only, deterministic, in-memory-only, and closed by default" in text
    assert "does not mean candidate testing, dry-run execution, reliability validation, ML unlock, Pilot activation, or Copilot behavior" in text
    assert "MLRT-27 does not collect, write, execute, or approve them" in text


def test_mlrt27_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    for reason in [
        "missing_mlrt25_freeze",
        "missing_mlrt26_freeze",
        "missing_mlrt27_freeze",
        "missing_freeze_memory_status_ok",
        "stale_startup_freeze_context",
        "unexpected_source_path",
        "source_file_already_exists",
        "runtime_router_import_requested",
        "prompt_loader_requested",
        "provider_call_requested",
        "embedding_or_vector_store_requested",
        "network_call_requested",
        "subprocess_call_requested",
        "persistence_requested",
        "live_prompt_library_read_requested",
        "live_router_canon_read_requested",
        "live_freeze_memory_read_requested",
        "candidate_execution_requested",
        "case_execution_requested",
        "case_scoring_requested",
        "route_comparison_requested",
        "report_generation_requested",
        "reliability_claim_requested",
        "route_authority_field_requested",
        "activation_key_requested",
        "field_test_requested",
        "runtime_pilot_requested",
        "copilot_requested",
        "human_review_missing",
    ]:
        assert reason in text


def test_mlrt27_outcomes_remain_non_authoritative() -> None:
    text = read(DOC)
    for allowed in [
        "SOURCE_CREATION_AUTHORIZATION_NOT_EVALUATED",
        "SOURCE_CREATION_AUTHORIZATION_REJECTED",
        "SOURCE_CREATION_AUTHORIZATION_ABORTED",
        "SOURCE_CREATION_AUTHORIZATION_READY_FOR_SEPARATE_CREATION_PATCH_PLANNING_ONLY",
    ]:
        assert allowed in text
    for forbidden in [
        "SOURCE_CREATION_APPROVED_FOR_RUNTIME",
        "SOURCE_FILE_CREATED",
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


def test_mlrt27_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_AUTHORIZATION_GATE_PLAN_READY_FOR_CREATION_PATCH_PLANNING_ONLY" in text
    assert "does not mean tests can start" in text
    assert "does not mean source creation is authorized" in text
    assert "does not mean a source file exists" in text
    assert "does not mean source files may be created now" in text
    assert "does not mean a source creation record exists" in text
    assert "does not mean source creation code exists" in text
    assert "does not mean a boundary checker exists" in text
    assert "does not mean a readiness gate exists" in text
    assert "does not mean a source surface exists" in text
    assert "does not mean a static interface exists" in text
    assert "does not mean a harness exists" in text
    assert "does not mean a dry run has executed" in text
    assert "does not mean candidate reliability is validated" in text
    assert "does not mean ML implementation is unlocked" in text


def test_mlrt27_manifest_records_planning_only_boundaries() -> None:
    import json

    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_authorization_gate_plan_"
    assert data[prefix + "feature_id"] == FEATURE_ID
    assert data[prefix + "documentation_only"] is True
    assert data[prefix + "authorization_gate_planning_only"] is True
    assert data[prefix + "testing_started"] is False
    assert data[prefix + "source_creation_authorized"] is False
    assert data[prefix + "python_source_files_created"] is False
    assert data[prefix + "source_files_created"] is False
    assert data[prefix + "source_files_authorized"] is False
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
    assert data[prefix + "next_safe_milestone"] == "MLRT-28 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Plan after MLRT-27 freeze with FREEZE_MEMORY_STATUS OK"


def test_mlrt27_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt27_does_not_create_forbidden_implementation_paths() -> None:
    forbidden_paths = [
        "candidate", "candidate_package", "candidate_packages", "candidate_outputs", "candidate_results",
        "package_intake_records", "static_review", "static_review_records", "static_review_results",
        "static_review_evidence", "static_review_evidence_records", "static_review_outcome", "static_review_outcome_records",
        "outcome_gate", "outcome_gate_records", "dry_run", "dry_run_execution", "dry_run_execution_records",
        "dry_run_readiness", "dry_run_readiness_records", "dry_run_protocol", "dry_run_protocol_records",
        "dry_run_protocol_execution_records", "dry_run_inputs", "dry_run_input_records", "dry_run_input_manifests",
        "dry_run_outputs", "dry_run_output_records", "dry_run_output_manifests", "output_capture",
        "output_capture_envelopes", "output_capture_records", "output_capture_rejection_records", "output_rejection_gate",
        "output_rejection_gate_records", "contract_conformance", "contract_conformance_records", "contract_conformance_evidence",
        "contract_conformance_rejection_gate", "contract_conformance_rejection_records", "conformance_checker",
        "harness", "runner", "harness_skeleton", "harness_contract", "harness_stub", "boundary_checker",
        "boundary_confirmation", "boundary_confirmation_code", "contract_schema", "schema", "schemas", "source_surface", "source_surface_files",
        "source_file_authorization", "source_file_authorization_records", "source_file_authorization_code", "source_creation_gate", "source_creation_records", "source_creation_code", "source_file_skeletons",
        "minimal_non_runtime_harness_stub.py", "static_interface", "static_interface_files", "abort_contract", "abort_contract_code", "abort_gate",
        "rejection_contract", "rejection_contract_code", "rejection_gate", "readiness_gate", "readiness_gate_code",
        "test_start_readiness", "test_start_readiness_gate", "implementation_modules", "evidence_envelopes", "reliability_results",
        "runtime_activation", "provider_adapter", "embedding_adapter", "prompt_loader", "persistent_ml_decisions", "reports", "validators", "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_mlrt27_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert "MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan v1" in readme
    assert FEATURE_ID in manifest
    assert "MLRT-28 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Plan" in readme
    assert "Tests do not start at MLRT-27" in readme


if __name__ == "__main__":
    test_mlrt27_docs_exist()
    test_mlrt27_tests_do_not_start_yet()
    test_mlrt27_is_authorization_gate_planning_only()
    test_mlrt27_records_roadmap_progression()
    test_mlrt27_defines_future_authorization_gate_sections()
    test_mlrt27_authorization_inputs_are_closed()
    test_mlrt27_rejection_reasons_are_comprehensive()
    test_mlrt27_outcomes_remain_non_authoritative()
    test_mlrt27_positive_label_is_planning_only()
    test_mlrt27_manifest_records_planning_only_boundaries()
    test_mlrt27_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt27_does_not_create_forbidden_implementation_paths()
    test_mlrt27_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan v1, "
        "immutable governed documentation-only minimal stub source-file creation authorization-gate planning after MLRT-26 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, testing not expected before MLRT-30 or later if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source files authorized, no source files created, "
        "no source creation authorization granted, no source creation records created, no source creation code created, no source file skeletons created, no source surface created, "
        "no static interface created, no harness created, no runner created, no harness stub files created, no dry run executed, no candidate execution, "
        "no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, no prompt loading, no provider calls, "
        "no embeddings, no network calls, no subprocess calls, no batch mode, no persistence, no activation key, no field-test mode, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero, next safe milestone is MLRT-28 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_AUTHORIZATION_GATE_PLAN_V1_VALIDATION_OK")
