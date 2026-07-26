from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_24_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_SOURCE_FILE_AUTHORIZATION_PLAN.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_source_file_authorization_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt24_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-24 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Source File Authorization Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt24_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-24." in text
    assert "It does not authorize source files." in text
    assert "It does not create source files." in text
    assert "It does not open the source boundary." in text
    assert "testing is still not expected before approximately MLRT-26 or MLRT-27" in text
    assert "final first-dry-run execution gate" in text


def test_mlrt24_is_source_file_authorization_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface source-file authorization planning milestone",
        "still not source code",
        "not an implementation",
        "not an actual source-file authorization",
        "not a source-file creation gate",
        "not a test run, not a dry run, not a candidate execution",
        "does not create Python source files",
        "does not create source-surface files",
        "does not authorize source files",
        "does not create source-file authorization records",
        "does not create source-file authorization code",
        "does not create implementation modules",
        "does not create boundary-confirmation code",
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
        "does not create executable validators",
        "does not create schema code",
        "does not create contract schema files",
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


def test_mlrt24_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-13 - first non-runtime dry-run execution planning" in text
    assert "MLRT-14 - future harness skeleton planning" in text
    assert "MLRT-15 - future harness contract planning" in text
    assert "MLRT-16 - future harness implementation boundary planning" in text
    assert "MLRT-17 - future harness stub implementation planning" in text
    assert "MLRT-18 - future harness stub source-surface planning" in text
    assert "MLRT-19 - future harness stub static-interface contract planning" in text
    assert "MLRT-20 - future harness stub static-interface abort-contract planning" in text
    assert "MLRT-21 - future harness stub static-interface rejection-contract planning" in text
    assert "MLRT-22 - future harness stub static-interface test-start readiness-gate planning" in text
    assert "MLRT-23 - future harness stub static-interface source/implementation boundary-confirmation planning" in text
    assert "MLRT-24 - future harness stub static-interface source-file authorization planning" in text
    assert "MLRT-25 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Stub Source Creation Gate Plan" in text


def test_mlrt24_defines_authorization_planning_groups() -> None:
    text = read(DOC)
    for heading in [
        "When tests start",
        "Source-file authorization identity",
        "Candidate authorization target doctrine",
        "Authorization preconditions",
        "Planned authorization record shape",
        "Closed-by-default authorization doctrine",
        "Human review doctrine",
        "No implementation doctrine",
        "No testing doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Forbidden authority fields",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt24_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    forbidden_phrases = [
        "create Python source files",
        "create source-surface files",
        "authorize source files",
        "create source-file authorization records",
        "create source-file authorization code",
        "create implementation modules",
        "create boundary-confirmation code",
        "create boundary-checker code",
        "create readiness-gate code",
        "create rejection-contract code",
        "create abort-contract code",
        "create executable readiness gates",
        "create executable rejection gates",
        "create executable abort gates",
        "create static interface files",
        "create harness code",
        "create runner code",
        "create harness stub files",
        "create executable validators",
        "create schema code",
        "create contract schema files",
        "run a dry run",
        "execute a candidate",
        "create candidate outputs",
        "run cases",
        "score cases",
        "compare routes",
        "generate reports",
        "persist reports",
        "validate candidate reliability",
        "unlock ML implementation",
        "grant route authority",
        "load prompts",
        "read live prompt-library files",
        "read live freeze memory",
        "read live router canon",
        "import runtime router modules",
        "call providers",
        "call embedding models",
        "use vector stores",
        "use network calls",
        "use subprocess calls",
        "start batch mode",
        "persist ML decisions",
        "create activation keys",
        "enable field-test mode",
        "create runtime Pilot behavior",
        "create Copilot behavior",
    ]
    for phrase in forbidden_phrases:
        assert phrase in text
    assert "The critical boundary error budget remains `0`." in text


def test_mlrt24_authorization_preconditions_are_closed_by_default() -> None:
    text = read(DOC)
    assert "fail closed unless all of the following are true" in text
    assert "MLRT-23 and MLRT-24 are both frozen with `FREEZE_MEMORY_STATUS: OK`." in text
    assert "standard-library-only" in text
    assert "import-isolated from runtime router modules" in text
    assert "returns only inert planning, rejection, or not-evaluated states" in text
    assert "A human review gate confirms this is still non-runtime and non-authoritative." in text
    assert "If any field is ambiguous, stale, missing, inconsistent, or suggests runtime behavior, the authorization state is `NOT_AUTHORIZED`." in text


def test_mlrt24_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_SOURCE_FILE_AUTHORIZATION_READY_FOR_NON_RUNTIME_STUB_SOURCE_CREATION_GATE_PLANNING_ONLY" in text
    assert "does not mean tests can start" in text
    assert "does not mean source files exist" in text
    assert "does not mean source files are authorized" in text
    assert "does not mean authorization records exist" in text
    assert "does not mean source-file authorization code exists" in text
    assert "does not mean a boundary checker exists" in text
    assert "does not mean a readiness gate exists" in text
    assert "does not mean executable readiness gates exist" in text
    assert "does not mean a source surface exists" in text
    assert "does not mean a static interface exists" in text
    assert "does not mean a harness exists" in text
    assert "does not mean a dry run has executed" in text
    assert "does not mean candidate reliability is validated" in text
    assert "does not mean ML implementation is unlocked" in text


def test_mlrt24_manifest_records_planning_only_boundaries() -> None:
    import json

    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_source_file_authorization_plan_"
    assert data[prefix + "feature_id"] == FEATURE_ID
    assert data[prefix + "documentation_only"] is True
    assert data[prefix + "source_file_authorization_planning_only"] is True
    assert data[prefix + "python_source_files_created"] is False
    assert data[prefix + "source_files_authorized"] is False
    assert data[prefix + "source_file_authorization_records_created"] is False
    assert data[prefix + "source_file_authorization_code_created"] is False
    assert data[prefix + "source_surface_created"] is False
    assert data[prefix + "static_interface_created"] is False
    assert data[prefix + "harness_created"] is False
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
    assert data[prefix + "next_safe_milestone"] == "MLRT-25 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Stub Source Creation Gate Plan after MLRT-24 freeze with FREEZE_MEMORY_STATUS OK"


def test_mlrt24_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt24_does_not_create_forbidden_implementation_paths() -> None:
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
        "source_file_authorization", "source_file_authorization_records", "source_file_authorization_code", "source_creation_gate",
        "static_interface", "static_interface_files", "abort_contract", "abort_contract_code", "abort_gate",
        "rejection_contract", "rejection_contract_code", "rejection_gate", "readiness_gate", "readiness_gate_code",
        "test_start_readiness", "test_start_readiness_gate", "implementation_modules", "evidence_envelopes", "reliability_results",
        "runtime_activation", "provider_adapter", "embedding_adapter", "prompt_loader", "persistent_ml_decisions", "reports", "validators", "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_mlrt24_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert "MLRT-24 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Source File Authorization Plan v1" in readme
    assert FEATURE_ID in manifest
    assert "MLRT-25 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Stub Source Creation Gate Plan" in readme
    assert "Tests do not start at MLRT-24" in readme


if __name__ == "__main__":
    test_mlrt24_docs_exist()
    test_mlrt24_tests_do_not_start_yet()
    test_mlrt24_is_source_file_authorization_planning_only()
    test_mlrt24_records_roadmap_progression()
    test_mlrt24_defines_authorization_planning_groups()
    test_mlrt24_preserves_forbidden_boundaries()
    test_mlrt24_authorization_preconditions_are_closed_by_default()
    test_mlrt24_positive_label_is_planning_only()
    test_mlrt24_manifest_records_planning_only_boundaries()
    test_mlrt24_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt24_does_not_create_forbidden_implementation_paths()
    test_mlrt24_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-24 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Source File Authorization Plan v1, "
        "immutable governed documentation-only source-file authorization planning after MLRT-23 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, estimates testing is still not expected before approximately MLRT-26 or MLRT-27 if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source-surface files created, "
        "no source files authorized, no source-file authorization records created, no source-file authorization code created, no boundary-confirmation code created, "
        "no boundary checker created, no readiness-gate code created, no rejection-contract code created, no abort-contract code created, "
        "no executable readiness gate created, no executable rejection gate created, no executable abort gate created, no source surface created, "
        "no static interface created, no static interface files created, no executable validators, no schema code, no contract schema created, "
        "no harness created, no runner created, no harness stub files created, no implementation modules created, no dry run executed, no dry-run outputs created, "
        "no candidate execution, no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, no prompt loading, "
        "no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistence, no activation key, no field-test mode, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is MLRT-25 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Stub Source Creation Gate Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_SOURCE_FILE_AUTHORIZATION_PLAN_V1_VALIDATION_OK")
