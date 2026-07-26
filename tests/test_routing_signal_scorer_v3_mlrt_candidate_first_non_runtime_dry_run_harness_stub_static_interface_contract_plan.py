from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_19_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_CONTRACT_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_contract_plan_v1"
ALLOWED_LAB_PY = {
    "candidate_evaluation_harness_interface.py",
    "deterministic_runner_skeleton.py",
    "lab_self_validation_gate.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt19_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    text = read(DOC)
    assert "MLRT-19 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Contract Plan v1" in text
    assert FEATURE_ID in text


def test_mlrt19_is_static_interface_contract_planning_only() -> None:
    text = read(DOC)
    required = [
        "documentation-only first non-runtime dry-run harness stub static-interface contract planning milestone",
        "still not source code, not a static interface, not a source surface, and not a harness implementation",
        "does not create Python source files",
        "does not create a static interface",
        "does not create a source surface",
        "does not create static interface files",
        "does not create source-surface files",
        "does not create harness code",
        "does not create runner code",
        "does not create harness stub files",
        "does not create implementation modules",
        "does not create executable validators",
        "does not create schema code",
        "does not create contract schema files",
        "does not implement a boundary checker",
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


def test_mlrt19_records_roadmap_progression() -> None:
    text = read(DOC)
    assert "MLRT-13 - first non-runtime dry-run execution planning" in text
    assert "MLRT-14 - future harness skeleton planning" in text
    assert "MLRT-15 - future harness contract planning" in text
    assert "MLRT-16 - future harness implementation boundary planning" in text
    assert "MLRT-17 - future harness stub implementation planning" in text
    assert "MLRT-18 - future harness stub source-surface planning" in text
    assert "MLRT-19 - future harness stub static-interface contract planning" in text
    assert "MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan" in text


def test_mlrt19_defines_static_interface_contract_planning_groups() -> None:
    text = read(DOC)
    for heading in [
        "Planned static-interface contract identity",
        "Planned static input contract",
        "Planned static output contract",
        "Planned abort-contract dependency",
        "Planned import policy",
        "No implementation doctrine",
        "No reliability claim doctrine",
        "Positive label doctrine",
        "Forbidden authority fields",
        "Next safe milestone",
    ]:
        assert f"## {heading}" in text


def test_mlrt19_preserves_forbidden_boundaries() -> None:
    text = read(DOC)
    forbidden_phrases = [
        "create Python source files",
        "create source-surface files",
        "create source-surface directories",
        "create static interface files",
        "create static interface directories",
        "create harness code",
        "create runner code",
        "create harness stub files",
        "create implementation modules",
        "create executable validators",
        "create schema code",
        "create contract schema files",
        "create static interface implementation files",
        "create boundary checker implementation files",
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


def test_mlrt19_positive_label_is_planning_only() -> None:
    text = read(DOC)
    assert "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_CONTRACT_PLAN_READY_FOR_ABORT_CONTRACT_PLANNING_ONLY" in text
    assert "does not mean source files exist" in text
    assert "does not mean a source surface exists" in text
    assert "does not mean a static interface exists" in text
    assert "does not mean static interface files exist" in text
    assert "does not mean a harness exists" in text
    assert "does not mean runner code exists" in text
    assert "does not mean harness stub files exist" in text
    assert "does not mean implementation modules exist" in text
    assert "does not mean a boundary checker exists" in text
    assert "does not mean a contract schema exists" in text
    assert "does not mean a dry run has executed" in text
    assert "does not mean candidate outputs exist" in text
    assert "does not mean cases were executed" in text
    assert "does not mean scores exist" in text
    assert "does not mean reports exist" in text
    assert "does not mean candidate reliability is validated" in text
    assert "does not mean ML implementation is unlocked" in text


def test_mlrt19_has_no_python_implementation_files() -> None:
    py_files = sorted(path.name for path in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(path.name for path in LAB.rglob("*.py"))
    assert set(py_files) == ALLOWED_LAB_PY
    assert len(py_files) == 3


def test_mlrt19_does_not_create_forbidden_implementation_paths() -> None:
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
        "static_interface_files", "implementation_modules", "evidence_envelopes", "reliability_results", "runtime_activation",
        "provider_adapter", "embedding_adapter", "prompt_loader", "persistent_ml_decisions", "reports", "validators", "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_box_manifest_records_mlrt19_static_interface_contract_plan() -> None:
    data = json.loads(read(MANIFEST))
    prefix = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_contract_plan"
    assert data[f"{prefix}_feature_id"] == FEATURE_ID
    assert data[f"{prefix}_doc"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_19_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_CONTRACT_PLAN.md"
    assert data[f"{prefix}_readme"] == "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
    assert data[f"{prefix}_test"] == "tests/test_routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_contract_plan.py"
    assert data[f"{prefix}_documentation_only"] is True
    assert data[f"{prefix}_source_surface_planning_only"] is False
    assert data[f"{prefix}_static_interface_contract_planning_only"] is True
    assert data[f"{prefix}_abort_contract_planning_only"] is False
    assert data[f"{prefix}_python_source_files_created"] is False
    assert data[f"{prefix}_source_surface_created"] is False
    assert data[f"{prefix}_static_interface_created"] is False
    assert data[f"{prefix}_static_interface_files_created"] is False
    assert data[f"{prefix}_harness_created"] is False
    assert data[f"{prefix}_runner_created"] is False
    assert data[f"{prefix}_harness_stub_files_created"] is False
    assert data[f"{prefix}_implementation_modules_created"] is False
    assert data[f"{prefix}_boundary_checker_created"] is False
    assert data[f"{prefix}_harness_contract_created"] is False
    assert data[f"{prefix}_contract_schema_created"] is False
    assert data[f"{prefix}_executable_validators_created"] is False
    assert data[f"{prefix}_schema_code_created"] is False
    assert data[f"{prefix}_dry_run_executed"] is False
    assert data[f"{prefix}_dry_run_execution_records_created"] is False
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
    assert data[f"{prefix}_positive_label"] == "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_CONTRACT_PLAN_READY_FOR_ABORT_CONTRACT_PLANNING_ONLY"
    assert data[f"{prefix}_next_safe_milestone"] == "MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan after MLRT-19 freeze with FREEZE_MEMORY_STATUS OK"


def main() -> None:
    test_mlrt19_docs_exist()
    test_mlrt19_is_static_interface_contract_planning_only()
    test_mlrt19_records_roadmap_progression()
    test_mlrt19_defines_static_interface_contract_planning_groups()
    test_mlrt19_preserves_forbidden_boundaries()
    test_mlrt19_positive_label_is_planning_only()
    test_mlrt19_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt19_does_not_create_forbidden_implementation_paths()
    test_box_manifest_records_mlrt19_static_interface_contract_plan()
    print(
        "CONTRACT_TEST_OK: MLRT-19 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Contract Plan v1, "
        "immutable governed documentation-only harness stub static-interface contract planning after MLRT-18 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms roadmap progress and defines future non-authoritative harness stub static-interface contract planning groups for static-interface contract identity, "
        "static input contract, static output contract, abort-contract dependency, import policy, no-implementation doctrine, no-reliability-claim doctrine, "
        "positive planning label, forbidden authority fields, and next-milestone doctrine only, candidate reliability not validated, ML implementation not unlocked, "
        "no Python source files created, no source surface created, no static interface created, no static interface files created, no executable validators, no schema code, "
        "no contract schema created, no boundary checker created, no harness created, no runner created, no harness stub files created, no implementation modules created, "
        "no harness skeleton created, no harness contract created, no candidate package created, no candidate package accepted, no candidate package installed, "
        "no candidate package imported, no candidate implementation, no candidate execution, no candidate outputs created, no package intake records created, "
        "no static review performed, no static review records created, no static review evidence records created, no evidence envelopes created, "
        "no static review outcome records created, no outcome gate records created, no dry-run readiness review performed, no dry-run readiness records created, "
        "no dry-run protocol records created, no dry-run protocol execution records created, no dry-run input records created, no dry-run input manifests created, "
        "no dry-run execution records created, no dry-run output records created, no dry-run output manifests created, no output capture envelopes created, "
        "no output capture rejection records created, no output rejection gate records created, no output rejection gate run, no contract-conformance records created, "
        "no contract-conformance evidence created, no contract-conformance check run, no contract-conformance rejection records created, "
        "no contract-conformance rejection gate run, no dry run executed, no dry-run outputs created, no case execution, no case scoring, no route comparison, "
        "no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, "
        "no corpus mutation, no fixture mutation, no router-canon mutation, no prompt-library mutation, no freeze-memory mutation, no gold-registry mutation, "
        "no report generation, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, "
        "no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, "
        "candidate first non-runtime dry-run harness stub static-interface contract plan remains non-authoritative, next safe milestone is MLRT-20 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Abort Contract Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_CONTRACT_PLAN_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
