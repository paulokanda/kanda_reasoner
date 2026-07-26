from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_41_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_EXECUTION_READINESS_OUTCOME_GATE_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_execution_readiness_outcome_gate_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer v3 MLRT-41 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Execution Readiness Outcome Gate Plan v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT = "MLRT-42 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Execution Gate Plan"
POS_LABEL = "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_EXECUTION_READINESS_OUTCOME_GATE_PLAN_READY_FOR_EXECUTION_GATE_PLANNING_ONLY"
PREFIX = "mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_execution_readiness_outcome_gate_plan"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt41_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt41_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-41" in text
    assert "testing is still not expected before MLRT-44 or MLRT-45" in text
    assert "candidate reliability" in text
    assert "does not unlock ML implementation" in text


def test_mlrt41_is_execution_readiness_outcome_gate_planning_only() -> None:
    text = read(DOC)
    required = [
        "Status: governed documentation-only controlled minimal source-file creation patch execution-readiness outcome-gate planning milestone.",
        "MLRT-41 is still not source code.",
        "It is not execution-readiness execution.",
        "It is not execution-readiness outcome approval.",
        "It is not an execution gate.",
        "It does not run that outcome gate.",
        "It does not produce an outcome.",
        "It does not approve readiness.",
        "It does not authorize source creation.",
        "It does not create the planned source file.",
    ]
    for item in required:
        assert item in text


def test_mlrt41_records_roadmap_progression() -> None:
    text = read(DOC)
    for marker in ["MLRT-31", "MLRT-32", "MLRT-33", "MLRT-34", "MLRT-35", "MLRT-36", "MLRT-37", "MLRT-38", "MLRT-39", "MLRT-40", "MLRT-41"]:
        assert marker in text
    assert NEXT in text


def test_mlrt41_defines_outcome_gate_without_execution() -> None:
    text = read(DOC)
    assert PLANNED_SOURCE in text
    assert "A later execution-readiness outcome gate, if it is ever executed" in text
    assert "The future outcome gate must not execute the patch" in text
    assert "It must not run source creation" in text
    assert "It must not create the source file" in text
    assert "may only define required evidence, allowed labels, rejection conditions, and escalation rules" in text


def test_mlrt41_required_evidence_is_safe() -> None:
    text = read(DOC)
    required = [
        "mlrt_40_freeze_confirmed",
        "freeze_memory_status_ok",
        "startup_freeze_context_refreshed",
        "mlrt_40_execution_readiness_plan_available",
        "planned_future_source_path_exact",
        "planned_future_source_path_absent_before_outcome_gate",
        "single_file_creation_limit_confirmed",
        "source_file_inert_contract_confirmed",
        "source_file_import_safe_contract_confirmed",
        "execution_readiness_outcome_gate_non_authoritative",
        "execution_readiness_outcome_gate_no_source_created",
        "execution_readiness_outcome_gate_no_patch_execution",
        "execution_readiness_outcome_gate_no_test_execution",
        "execution_readiness_outcome_gate_no_reliability_claim",
        "execution_readiness_outcome_gate_only_allows_execution_gate_planning",
    ]
    for item in required:
        assert item in text


def test_mlrt41_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    reasons = [
        "missing_mlrt41_freeze",
        "planned_future_source_path_already_exists",
        "source_creation_attempted_during_outcome_gate_plan",
        "source_authorization_attempted_during_outcome_gate_plan",
        "execution_readiness_outcome_gate_attempts_to_create_source_file",
        "execution_readiness_outcome_gate_attempts_to_execute_patch",
        "execution_readiness_outcome_gate_attempts_to_run_source_creation",
        "execution_readiness_outcome_gate_attempts_to_run_tests",
        "execution_readiness_outcome_gate_attempts_to_authorize_source_creation",
        "execution_readiness_outcome_gate_approves_source_creation",
        "execution_readiness_outcome_gate_creates_source_file",
        "execution_readiness_outcome_gate_executes_patch",
        "execution_readiness_outcome_gate_runs_tests",
        "execution_readiness_outcome_gate_claims_reliability",
        "execution_readiness_outcome_gate_grants_route_authority",
        "execution_readiness_outcome_gate_missing_import_safety",
        "execution_readiness_outcome_gate_missing_no_runtime_router",
        "execution_readiness_outcome_gate_missing_no_prompt_loader",
        "execution_readiness_outcome_gate_missing_no_provider",
        "execution_readiness_outcome_gate_missing_no_persistence",
        "execution_readiness_outcome_gate_exceeds_next_scope",
    ]
    for reason in reasons:
        assert reason in text


def test_mlrt41_vocabulary_remains_non_authoritative() -> None:
    text = read(DOC)
    assert "controlled_minimal_source_file_creation_patch_execution_readiness_outcome_ready_for_execution_gate_planning_only" in text
    assert POS_LABEL in text
    assert "This label does not authorize source creation" in text
    assert "It does not authorize execution" in text


def test_mlrt41_manifest_records_planning_only_boundaries() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        "controlled_minimal_source_file_creation_patch_execution_readiness_outcome_gate_planning_only",
        "python_source_files_created",
        "source_files_created",
        "execution_readiness_outcome_gate_run",
        "execution_readiness_outcome_approved",
        "execution_gate_run",
        "planned_future_source_path",
        "testing_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_python_source_files_created": false' in manifest
    assert f'"{PREFIX}_source_files_created": false' in manifest
    assert f'"{PREFIX}_execution_readiness_outcome_gate_run": false' in manifest
    assert f'"{PREFIX}_execution_readiness_outcome_approved": false' in manifest
    assert f'"{PREFIX}_execution_gate_run": false' in manifest
    assert f'"{PREFIX}_testing_started": false' in manifest


def test_mlrt41_has_no_python_implementation_files() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt41_does_not_create_future_source_path() -> None:
    assert not (ROOT / PLANNED_SOURCE).exists()


def test_mlrt41_does_not_create_forbidden_implementation_paths() -> None:
    forbidden_paths = [
        "source_surface",
        "source_creation_patch",
        "source_creation_records",
        "source_creation_code",
        "source_file_authorization",
        "source_file_authorization_records",
        "source_file_authorization_code",
        "source_creation_authorization",
        "source_creation_authorization_gate",
        "source_creation_authorization_records",
        "source_creation_authorization_outcome",
        "source_creation_authorization_outcomes",
        "source_creation_authorization_outcome_gate",
        "source_creation_authorization_outcome_gate_records",
        "controlled_minimal_source_file_creation_patch",
        "controlled_minimal_source_file_creation_patch_records",
        "controlled_minimal_source_file_creation_patch_execution_readiness",
        "controlled_minimal_source_file_creation_patch_execution_readiness_records",
        "controlled_minimal_source_file_creation_patch_execution_readiness_outcome_gate",
        "controlled_minimal_source_file_creation_patch_execution_readiness_outcome_gate_records",
        "controlled_minimal_source_file_creation_patch_execution_gate",
        "controlled_minimal_source_file_creation_patch_execution_gate_records",
        "safety_review",
        "safety_review_records",
        "safety_review_outcomes",
        "safety_review_outcome_gate",
        "safety_review_outcome_gate_records",
        "final_human_review",
        "final_human_review_records",
        "final_human_review_outcome",
        "final_human_review_outcomes",
        "final_human_review_gate",
        "final_human_review_gate_records",
        "final_human_review_outcome_gate",
        "final_human_review_outcome_gate_records",
        "harness",
        "runner",
        "harness_stub",
        "boundary_checker",
        "readiness_gate",
        "dry_run",
        "dry_run_execution",
        "dry_run_outputs",
        "candidate",
        "candidate_outputs",
        "candidate_results",
        "reliability_results",
        "runtime_activation",
        "provider_adapter",
        "embedding_adapter",
        "prompt_loader",
        "persistent_ml_decisions",
        "reports",
        "schemas",
        "validators",
        "scorer",
    ]
    for rel in forbidden_paths:
        assert not (MLRT / rel).exists(), rel


def test_mlrt41_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in manifest
    assert NEXT in readme
    assert "Tests do not start at MLRT-41" in readme


if __name__ == "__main__":
    test_mlrt41_docs_exist()
    test_mlrt41_tests_do_not_start_yet()
    test_mlrt41_is_execution_readiness_outcome_gate_planning_only()
    test_mlrt41_records_roadmap_progression()
    test_mlrt41_defines_outcome_gate_without_execution()
    test_mlrt41_required_evidence_is_safe()
    test_mlrt41_rejection_reasons_are_comprehensive()
    test_mlrt41_vocabulary_remains_non_authoritative()
    test_mlrt41_manifest_records_planning_only_boundaries()
    test_mlrt41_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt41_does_not_create_future_source_path()
    test_mlrt41_does_not_create_forbidden_implementation_paths()
    test_mlrt41_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-41 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Execution Readiness Outcome Gate Plan v1, "
        "immutable governed documentation-only controlled minimal source-file creation patch execution-readiness outcome-gate planning after MLRT-40 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, testing still not expected before MLRT-44 or MLRT-45 if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source files authorized, no source files created, "
        "no parent folders created, no source creation authorization granted, no source creation authorization gate run, no source creation authorization records created, "
        "no source creation authorization outcomes created, no source creation authorization outcome approved, no source creation authorization outcome gate run, "
        "no source creation authorization outcome-gate records created, no source creation code created, no source creation patch created, "
        "no controlled minimal source-file creation patch created, no future source path created, no execution-readiness checks run, no execution-readiness records created, "
        "no execution-readiness outcome gate run, no execution-readiness outcome approved, no execution gate run, no execution gate records created, "
        "no safety review run, no safety-review records created, no safety-review outcomes created, no final human review run, no final human-review gate run, "
        "no final human-review outcome gate run, no source file skeletons created, no source surface created, no static interface created, no harness created, no runner created, "
        "no harness stub files created, no dry run executed, no candidate execution, no candidate outputs created, no case execution, no case scoring, "
        "no route comparison, no route authority, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, "
        f"no persistence, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is {NEXT}"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_EXECUTION_READINESS_OUTCOME_GATE_PLAN_V1_VALIDATION_OK")
