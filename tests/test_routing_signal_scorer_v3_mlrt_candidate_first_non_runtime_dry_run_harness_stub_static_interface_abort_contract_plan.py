from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_20_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_ABORT_CONTRACT_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_abort_contract_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt20_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt20_answers_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-20." in text
    assert "Until those later milestones exist and are frozen with `FREEZE_MEMORY_STATUS: OK`, every MLRT step remains planning only" in text
    assert "Candidate reliability remains unvalidated." in text


def test_mlrt20_is_abort_contract_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface abort-contract planning milestone",
        "still not testing",
        "not source code, not an executable abort gate, not a static interface, not a source surface",
        "does not create Python source files",
        "does not create abort-contract code",
        "does not create rejection-contract code",
        "does not create a static interface",
        "does not create source-surface files",
        "does not create static-interface files",
        "does not create harness code",
        "does not create runner code",
        "does not create harness stub files",
        "does not create implementation modules",
        "does not create boundary-checker code",
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


def test_mlrt20_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-13 - first non-runtime dry-run execution planning" in text
    assert "MLRT-14 - future harness skeleton planning" in text
    assert "MLRT-15 - future harness contract planning" in text
    assert "MLRT-16 - future harness implementation boundary planning" in text
    assert "MLRT-17 - future harness stub implementation planning" in text
    assert "MLRT-18 - future harness stub source-surface planning" in text
    assert "MLRT-19 - future harness stub static-interface contract planning" in text
    assert "MLRT-20 - future harness stub static-interface abort-contract planning" in text
    assert "MLRT-21 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Rejection Contract Plan" in text


def test_mlrt20_defines_abort_contract_planning_groups() -> None:
    text = read(DOC)
    for heading in [
        "When tests start",
        "Planned abort-contract identity",
        "Planned abort triggers",
        "Planned abort output doctrine",
        "Planned rejection-contract dependency",
        "Planned import policy",
        "No implementation doctrine",
        "No testing doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Forbidden authority fields",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt20_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    forbidden_phrases = [
        "create Python source files",
        "create abort-contract code",
        "create rejection-contract code",
        "create executable abort gates",
        "create executable rejection gates",
        "create source-surface files",
        "create static interface files",
        "create harness code",
        "create runner code",
        "create harness stub files",
        "create implementation modules",
        "create boundary-checker code",
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


def test_mlrt20_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_ABORT_CONTRACT_PLAN_READY_FOR_REJECTION_CONTRACT_PLANNING_ONLY" in text
    assert "does not mean source files exist" in text
    assert "does not mean an abort contract exists" in text
    assert "does not mean a rejection contract exists" in text
    assert "does not mean executable abort gates exist" in text
    assert "does not mean executable rejection gates exist" in text
    assert "does not mean a source surface exists" in text
    assert "does not mean a static interface exists" in text
    assert "does not mean a harness exists" in text
    assert "does not mean a dry run has executed" in text
    assert "does not mean candidate reliability is validated" in text
    assert "does not mean ML implementation is unlocked" in text


def test_mlrt20_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt20_does_not_create_forbidden_implementation_paths() -> None:
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
        "contract_schema", "schema", "schemas", "source_surface", "source_surface_files", "static_interface",
        "static_interface_files", "abort_contract", "abort_contract_code", "abort_gate", "rejection_contract", "rejection_gate",
        "implementation_modules", "evidence_envelopes", "reliability_results", "runtime_activation",
        "provider_adapter", "embedding_adapter", "prompt_loader", "persistent_ml_decisions", "reports", "validators", "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_box_manifest_records_mlrt20_abort_contract_plan() -> None:
    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_abort_contract_plan"
    assert data[f"{prefix}_feature_id"] == FEATURE_ID
    assert data[f"{prefix}_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_20_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_ABORT_CONTRACT_PLAN.md"
    assert data[f"{prefix}_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data[f"{prefix}_test"] == "tests/test_routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_abort_contract_plan.py"
    assert data[f"{prefix}_documentation_only"] is True
    assert data[f"{prefix}_abort_contract_planning_only"] is True
    assert data[f"{prefix}_testing_started"] is False
    assert data[f"{prefix}_python_source_files_created"] is False
    assert data[f"{prefix}_abort_contract_code_created"] is False
    assert data[f"{prefix}_rejection_contract_code_created"] is False
    assert data[f"{prefix}_executable_abort_gate_created"] is False
    assert data[f"{prefix}_executable_rejection_gate_created"] is False
    assert data[f"{prefix}_source_surface_created"] is False
    assert data[f"{prefix}_static_interface_created"] is False
    assert data[f"{prefix}_static_interface_files_created"] is False
    assert data[f"{prefix}_harness_created"] is False
    assert data[f"{prefix}_runner_created"] is False
    assert data[f"{prefix}_harness_stub_files_created"] is False
    assert data[f"{prefix}_implementation_modules_created"] is False
    assert data[f"{prefix}_boundary_checker_created"] is False
    assert data[f"{prefix}_contract_schema_created"] is False
    assert data[f"{prefix}_executable_validators_created"] is False
    assert data[f"{prefix}_schema_code_created"] is False
    assert data[f"{prefix}_dry_run_executed"] is False
    assert data[f"{prefix}_candidate_executed"] is False
    assert data[f"{prefix}_candidate_outputs_created"] is False
    assert data[f"{prefix}_cases_executed"] is False
    assert data[f"{prefix}_cases_scored"] is False
    assert data[f"{prefix}_route_authority"] is False
    assert data[f"{prefix}_prompt_loading"] is False
    assert data[f"{prefix}_provider_calls"] is False
    assert data[f"{prefix}_embeddings"] is False
    assert data[f"{prefix}_network_calls"] is False
    assert data[f"{prefix}_subprocess_calls"] is False
    assert data[f"{prefix}_batch_mode"] is False
    assert data[f"{prefix}_persistence"] is False
    assert data[f"{prefix}_activation_key"] is False
    assert data[f"{prefix}_field_test_mode"] is False
    assert data[f"{prefix}_runtime_pilot_behavior"] is False
    assert data[f"{prefix}_copilot_behavior"] is False
    assert data[f"{prefix}_candidate_reliability_validated"] is False
    assert data[f"{prefix}_ml_implementation_unlocked"] is False
    assert data[f"{prefix}_critical_boundary_error_budget"] == 0
    assert data[f"{prefix}_positive_label"] == "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_ABORT_CONTRACT_PLAN_READY_FOR_REJECTION_CONTRACT_PLANNING_ONLY"
    assert data[f"{prefix}_next_safe_milestone"] == "MLRT-21 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Rejection Contract Plan after MLRT-20 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt20_docs_exist()
    test_mlrt20_answers_tests_do_not_start_yet()
    test_mlrt20_is_abort_contract_planning_only()
    test_mlrt20_records_roadmap_progression()
    test_mlrt20_defines_abort_contract_planning_groups()
    test_mlrt20_preserves_forbidden_boundaries()
    test_mlrt20_positive_label_is_planning_only()
    test_mlrt20_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt20_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt20_abort_contract_plan()
    print(
        "CONTRACT_TEST_OK: MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan v1, "
        "immutable governed documentation-only harness stub static-interface abort-contract planning after MLRT-19 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet and defines future non-authoritative abort-contract planning groups for test-start boundary, abort-contract identity, "
        "abort triggers, abort output doctrine, rejection-contract dependency, import policy, no-implementation doctrine, no-testing doctrine, no-reliability-claim doctrine, "
        "positive planning label, forbidden authority fields, and next-milestone doctrine only, candidate reliability not validated, ML implementation not unlocked, "
        "no Python source files created, no abort-contract code created, no rejection-contract code created, no executable abort gate created, no executable rejection gate created, "
        "no source surface created, no static interface created, no static interface files created, no executable validators, no schema code, no contract schema created, "
        "no boundary checker created, no harness created, no runner created, no harness stub files created, no implementation modules created, no dry run executed, "
        "no dry-run outputs created, no candidate execution, no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, "
        "no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistence, no activation key, "
        "no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is MLRT-21 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Rejection Contract Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_ABORT_CONTRACT_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
