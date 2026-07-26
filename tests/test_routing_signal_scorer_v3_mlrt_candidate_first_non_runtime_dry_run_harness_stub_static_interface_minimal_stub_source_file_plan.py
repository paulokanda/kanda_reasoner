from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_26_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_PLAN.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt26_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-26 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt26_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-26." in text
    assert "does not create the future source file" in text
    assert "does not open any executable path" in text
    assert "testing is now still not expected before MLRT-28 or later" in text
    assert "final first-dry-run execution gate" in text


def test_mlrt26_is_minimal_source_file_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface minimal stub source file planning milestone",
        "still not source code",
        "not an implementation",
        "not source-file creation",
        "not source-file authorization",
        "not a source creation gate implementation",
        "not a created source surface",
        "not a created static interface",
        "not a created harness stub",
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


def test_mlrt26_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-22 - future test-start readiness-gate planning" in text
    assert "MLRT-23 - future source/implementation boundary-confirmation planning" in text
    assert "MLRT-24 - future source-file authorization planning" in text
    assert "MLRT-25 - future stub source creation gate planning" in text
    assert "MLRT-26 - future minimal stub source file planning" in text
    assert "MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan" in text


def test_mlrt26_defines_future_minimal_file_sections() -> None:
    text = read(DOC)
    for heading in [
        "When tests start",
        "Future minimal source-file candidate identity",
        "Future minimal source-file allowed shape",
        "Future minimal source-file allowed symbols",
        "Future minimal source-file forbidden symbols",
        "Creation authorization dependency",
        "No implementation doctrine",
        "No testing doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt26_future_file_identity_is_planning_only() -> None:
    text = read(DOC)
    assert "minimal_non_runtime_harness_stub.py" in text
    assert "candidate future location: kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/" in text
    assert "This candidate identity is not authorization." in text
    assert "It is not creation." in text
    assert "It is not an instruction to create the file." in text
    assert "It is not an import target." in text
    assert "It is not test-ready." in text


def test_mlrt26_allowed_and_forbidden_future_symbols_are_non_authoritative() -> None:
    text = read(DOC)
    for allowed in [
        "MINIMAL_STUB_SOURCE_FILE_VERSION",
        "MINIMAL_STUB_SOURCE_FILE_STATUS",
        "build_rejected_stub_envelope",
        "build_aborted_stub_envelope",
        "build_not_evaluated_stub_envelope",
    ]:
        assert allowed in text
    for forbidden in [
        "route_decision",
        "route_authority",
        "authoritative_route",
        "load_prompt",
        "execute_candidate",
        "run_case",
        "score_case",
        "compare_route",
        "generate_report",
        "authorize_source_file",
        "create_source_file",
        "activation_key",
        "runtime_pilot_enabled",
        "copilot_enabled",
        "persist_decision",
        "write_freeze_memory",
        "mutate_prompt_library",
        "mutate_router_canon",
        "mutate_gold_registry",
    ]:
        assert forbidden in text


def test_mlrt26_creation_authorization_dependency_is_closed() -> None:
    text = read(DOC)
    assert "A future minimal source file must not be created until a later creation authorization gate verifies" in text
    assert "MLRT-25 and MLRT-26 are both frozen with `FREEZE_MEMORY_STATUS: OK`." in text
    assert "explicitly approved under a later governed milestone" in text
    assert "standard-library-only" in text
    assert "no runtime router imports" in text
    assert "A human review confirms source creation remains non-runtime and non-authoritative." in text


def test_mlrt26_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_PLAN_READY_FOR_CREATION_AUTHORIZATION_GATE_PLANNING_ONLY" in text
    assert "does not mean tests can start" in text
    assert "does not mean a source file exists" in text
    assert "does not mean source files are authorized" in text
    assert "does not mean source files may be created" in text
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


def test_mlrt26_manifest_records_planning_only_boundaries() -> None:
    import json

    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_plan_"
    assert data[prefix + "feature_id"] == FEATURE_ID
    assert data[prefix + "documentation_only"] is True
    assert data[prefix + "minimal_stub_source_file_planning_only"] is True
    assert data[prefix + "testing_started"] is False
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
    assert data[prefix + "next_safe_milestone"] == "MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan after MLRT-26 freeze with FREEZE_MEMORY_STATUS OK"


def test_mlrt26_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt26_does_not_create_forbidden_implementation_paths() -> None:
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


def test_mlrt26_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert "MLRT-26 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Plan v1" in readme
    assert FEATURE_ID in manifest
    assert "MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan" in readme
    assert "Tests do not start at MLRT-26" in readme


if __name__ == "__main__":
    test_mlrt26_docs_exist()
    test_mlrt26_tests_do_not_start_yet()
    test_mlrt26_is_minimal_source_file_planning_only()
    test_mlrt26_records_roadmap_progression()
    test_mlrt26_defines_future_minimal_file_sections()
    test_mlrt26_future_file_identity_is_planning_only()
    test_mlrt26_allowed_and_forbidden_future_symbols_are_non_authoritative()
    test_mlrt26_creation_authorization_dependency_is_closed()
    test_mlrt26_positive_label_is_planning_only()
    test_mlrt26_manifest_records_planning_only_boundaries()
    test_mlrt26_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt26_does_not_create_forbidden_implementation_paths()
    test_mlrt26_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-26 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Plan v1, "
        "immutable governed documentation-only minimal stub source file planning after MLRT-25 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, testing still not expected before MLRT-28 or later if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source files authorized, no source files created, "
        "no source creation records created, no source creation code created, no source file skeletons created, no source surface created, "
        "no static interface created, no harness created, no runner created, no harness stub files created, no dry run executed, no candidate execution, "
        "no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, no prompt loading, no provider calls, "
        "no embeddings, no network calls, no subprocess calls, no batch mode, no persistence, no activation key, no field-test mode, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero, next safe milestone is MLRT-27 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Authorization Gate Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_PLAN_V1_VALIDATION_OK")
