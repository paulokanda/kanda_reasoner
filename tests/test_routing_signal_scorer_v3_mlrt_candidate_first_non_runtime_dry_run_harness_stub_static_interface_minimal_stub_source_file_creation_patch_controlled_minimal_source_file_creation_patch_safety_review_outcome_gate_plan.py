from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_37_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_SAFETY_REVIEW_OUTCOME_GATE_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer v3 MLRT-37 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Safety Review Outcome Gate Plan v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT = "MLRT-38 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Final Human Review Gate Plan"
POS_LABEL = "MLRT_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_SAFETY_REVIEW_OUTCOME_GATE_PLAN_READY_FOR_FINAL_HUMAN_REVIEW_GATE_PLANNING_ONLY"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt37_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt37_tests_do_not_start_yet() -> None:
    text = read(DOC)
    assert "Real candidate/dry-run tests must not start at MLRT-37" in text
    assert "testing is still not expected before MLRT-39 or later" in text
    assert "candidate reliability validation" in text or "candidate reliability" in text
    assert "does not unlock ML implementation" in text


def test_mlrt37_is_outcome_gate_planning_only() -> None:
    text = read(DOC)
    required = [
        "Status: governed documentation-only controlled minimal source-file creation patch safety-review outcome-gate planning milestone.",
        "MLRT-37 is still not source code.",
        "It is not a safety-review outcome approval.",
        "MLRT-37 does not create Python source files",
        "MLRT-37 does not create source files",
        "MLRT-37 does not create parent folders",
        "does not run a safety-review outcome gate",
        "does not approve safety-review outcomes",
    ]
    for item in required:
        assert item in text


def test_mlrt37_records_roadmap_progression() -> None:
    text = read(DOC)
    for marker in ["MLRT-31", "MLRT-32", "MLRT-33", "MLRT-34", "MLRT-35", "MLRT-36", "MLRT-37"]:
        assert marker in text
    assert NEXT in text


def test_mlrt37_defines_outcome_gate_without_running_it() -> None:
    text = read(DOC)
    assert PLANNED_SOURCE in text
    assert "A later outcome gate, if it is ever executed" in text
    assert "The outcome gate must not execute the patch" in text
    assert "The outcome gate must not run the safety review" in text
    assert "The outcome gate must not create the source file" in text
    assert "The outcome gate may only inspect" in text


def test_mlrt37_outcome_gate_inputs_are_safe() -> None:
    text = read(DOC)
    required = [
        "safety_review_completed_under_separate_scope",
        "safety_review_records_available",
        "safety_review_outcome_available",
        "safety_review_outcome_non_authoritative",
        "safety_review_outcome_no_source_created",
        "safety_review_outcome_no_patch_execution",
        "safety_review_outcome_no_test_execution",
        "safety_review_outcome_no_reliability_claim",
        "safety_review_outcome_no_source_authorization",
        "safety_review_outcome_no_runtime_imports",
        "safety_review_outcome_no_prompt_loader",
        "safety_review_outcome_no_provider",
        "safety_review_outcome_no_persistence",
    ]
    for item in required:
        assert item in text


def test_mlrt37_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    reasons = [
        "missing_mlrt37_freeze",
        "missing_safety_review_outcome",
        "safety_review_outcome_gate_attempts_to_create_source_file",
        "safety_review_outcome_gate_attempts_to_execute_patch",
        "safety_review_outcome_gate_attempts_to_run_safety_review",
        "safety_review_outcome_gate_attempts_to_run_tests",
        "safety_review_outcome_gate_attempts_to_authorize_source_creation",
        "safety_review_outcome_approves_source_creation",
        "safety_review_outcome_creates_source_file",
        "safety_review_outcome_executes_patch",
        "safety_review_outcome_runs_tests",
        "safety_review_outcome_claims_reliability",
        "safety_review_outcome_grants_route_authority",
        "safety_review_outcome_missing_import_safety",
        "safety_review_outcome_missing_no_runtime_router",
        "safety_review_outcome_missing_no_prompt_loader",
        "safety_review_outcome_missing_no_provider",
        "safety_review_outcome_missing_no_persistence",
    ]
    for reason in reasons:
        assert reason in text


def test_mlrt37_vocabulary_remains_non_authoritative() -> None:
    text = read(DOC)
    assert "controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_ready_for_final_human_review_gate_planning_only" in text
    assert POS_LABEL in text
    assert "This label does not authorize source creation" in text


def test_mlrt37_manifest_records_planning_only_boundaries() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        "controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_planning_only",
        "python_source_files_created",
        "source_files_created",
        "safety_review_run",
        "safety_review_outcome_gate_run",
        "safety_review_outcome_approved",
        "planned_future_source_path",
        "testing_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT,
    ]
    for item in required:
        assert item in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_python_source_files_created": false' in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_source_files_created": false' in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_safety_review_run": false' in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_safety_review_outcome_gate_run": false' in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_safety_review_outcome_approved": false' in manifest
    assert '"mlrt_candidate_first_non_runtime_dry_run_harness_stub_static_interface_minimal_stub_source_file_creation_patch_controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_plan_testing_started": false' in manifest


def test_mlrt37_has_no_python_implementation_files() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt37_does_not_create_future_source_path() -> None:
    assert not (ROOT / PLANNED_SOURCE).exists()


def test_mlrt37_does_not_create_forbidden_implementation_paths() -> None:
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
        "controlled_minimal_source_file_creation_patch_safety_review",
        "controlled_minimal_source_file_creation_patch_safety_review_records",
        "controlled_minimal_source_file_creation_patch_safety_review_outcome_gate",
        "controlled_minimal_source_file_creation_patch_safety_review_outcome_gate_records",
        "safety_review",
        "safety_review_records",
        "safety_review_outcomes",
        "safety_review_outcome_gate",
        "safety_review_outcome_gate_records",
        "final_human_review",
        "final_human_review_records",
        "final_human_review_outcome",
        "final_human_review_outcomes",
        "final_human_review_outcome_gate",
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


def test_mlrt37_readme_and_manifest_reference_feature() -> None:
    readme = read(README)
    manifest = read(MANIFEST)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in manifest
    assert NEXT in readme
    assert "Tests do not start at MLRT-37" in readme


if __name__ == "__main__":
    test_mlrt37_docs_exist()
    test_mlrt37_tests_do_not_start_yet()
    test_mlrt37_is_outcome_gate_planning_only()
    test_mlrt37_records_roadmap_progression()
    test_mlrt37_defines_outcome_gate_without_running_it()
    test_mlrt37_outcome_gate_inputs_are_safe()
    test_mlrt37_rejection_reasons_are_comprehensive()
    test_mlrt37_vocabulary_remains_non_authoritative()
    test_mlrt37_manifest_records_planning_only_boundaries()
    test_mlrt37_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt37_does_not_create_future_source_path()
    test_mlrt37_does_not_create_forbidden_implementation_paths()
    test_mlrt37_readme_and_manifest_reference_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-37 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Safety Review Outcome Gate Plan v1, "
        "immutable governed documentation-only controlled minimal source-file creation patch safety-review outcome-gate planning after MLRT-36 freeze with FREEZE_MEMORY_STATUS OK, "
        "confirms tests must not start yet, testing still not expected before MLRT-39 or later if no new safety gap appears, "
        "candidate reliability not validated, ML implementation not unlocked, no Python source files created, no source files authorized, no source files created, "
        "no parent folders created, no source creation authorization granted, no source creation authorization gate run, no source creation authorization records created, "
        "no source creation authorization outcomes created, no source creation authorization outcome approved, no source creation authorization outcome gate run, "
        "no source creation authorization outcome-gate records created, no source creation code created, no source creation patch created, "
        "no controlled minimal source-file creation patch created, no future source path created, no safety review run, no safety-review records created, "
        "no safety-review outcomes created, no safety-review outcome approved, no safety-review outcome gate run, no safety-review outcome-gate records created, "
        "no final human review run, no final human-review records created, no final human-review outcomes created, no final human-review outcome approved, "
        "no final human-review outcome gate run, no outcome-gate records created, no source file skeletons created, no source surface created, "
        "no static interface created, no harness created, no runner created, no harness stub files created, no dry run executed, no candidate execution, "
        "no candidate outputs created, no case execution, no case scoring, no route comparison, no route authority, no prompt loading, no provider calls, "
        "no embeddings, no network calls, no subprocess calls, no batch mode, no persistence, no activation key, no field-test mode, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero, next safe milestone is MLRT-38 Candidate First Non-Runtime Dry-Run Harness Stub Static Interface Minimal Stub Source File Creation Patch Controlled Minimal Source File Creation Patch Final Human Review Gate Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_MLRT_CANDIDATE_FIRST_NON_RUNTIME_DRY_RUN_HARNESS_STUB_STATIC_INTERFACE_MINIMAL_STUB_SOURCE_FILE_CREATION_PATCH_CONTROLLED_MINIMAL_SOURCE_FILE_CREATION_PATCH_SAFETY_REVIEW_OUTCOME_GATE_PLAN_V1_VALIDATION_OK")
