from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_43_EXECUTION_GATE_OUTCOME_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "rss_mlrt43_execution_gate_outcome_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-43 Execution Gate Outcome Plan v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-44 Source Creation Patch Execution Authorization Plan v1"
POS_LABEL = "RSS_MLRT43_READY_FOR_SOURCE_CREATION_PATCH_EXECUTION_AUTHORIZATION_PLANNING_ONLY"
PREFIX = "rss_mlrt43_execution_gate_outcome_plan"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt43_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt43_uses_compact_freeze_safe_name() -> None:
    text = read(DOC)
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "compact freeze-safe naming" in text
    assert "Windows and Freeze Feature form filename limits" in text


def test_mlrt43_is_execution_gate_outcome_planning_only() -> None:
    text = read(DOC)
    required = [
        "Status: governed documentation-only execution-gate outcome planning milestone.",
        "MLRT-43 is still not source code.",
        "It is not execution-gate execution.",
        "It is not an executed execution-gate outcome.",
        "It is not source creation approval.",
        "MLRT-43 only plans how a later execution-gate outcome would be recorded",
        "does not run the gate",
        "does not produce an actual gate outcome",
        "does not approve execution",
        "does not authorize source creation",
    ]
    for item in required:
        assert item in text


def test_mlrt43_boundaries_prevent_source_and_runtime() -> None:
    text = read(DOC)
    for item in [
        "does not create Python source files",
        "does not create the parent folder",
        "does not write source code",
        "does not execute a dry run",
        "does not execute a candidate",
        "does not validate candidate reliability",
        "does not grant route authority",
        "does not load prompts",
        "does not call providers",
        "does not use embeddings",
        "does not create runtime Pilot behavior",
        "does not create Copilot behavior",
    ]:
        assert item in text


def test_mlrt43_planned_source_path_remains_absent() -> None:
    assert PLANNED_SOURCE in read(DOC)
    assert not (ROOT / PLANNED_SOURCE).exists()


def test_mlrt43_required_evidence_is_safe() -> None:
    text = read(DOC)
    required = [
        "mlrt_42_freeze_confirmed",
        "freeze_memory_status_ok",
        "startup_freeze_context_refreshed",
        "mlrt_42_execution_gate_plan_available",
        "mlrt_43_execution_gate_outcome_plan_available",
        "planned_future_source_path_exact",
        "planned_future_source_path_absent_before_outcome",
        "single_file_creation_limit_confirmed",
        "source_file_inert_contract_confirmed",
        "source_file_import_safe_contract_confirmed",
        "execution_gate_outcome_non_authoritative",
        "execution_gate_outcome_no_source_created",
        "execution_gate_outcome_no_patch_execution",
        "execution_gate_outcome_no_test_execution",
        "execution_gate_outcome_no_reliability_claim",
        "execution_gate_outcome_only_allows_authorization_planning",
    ]
    for item in required:
        assert item in text


def test_mlrt43_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    reasons = [
        "missing_mlrt43_freeze",
        "planned_future_source_path_already_exists",
        "source_creation_attempted_during_execution_gate_outcome_plan",
        "source_authorization_attempted_during_execution_gate_outcome_plan",
        "execution_gate_outcome_attempts_to_create_source_file",
        "execution_gate_outcome_attempts_to_execute_patch",
        "execution_gate_outcome_attempts_to_run_source_creation",
        "execution_gate_outcome_attempts_to_run_tests",
        "execution_gate_outcome_attempts_to_claim_reliability",
        "execution_gate_outcome_attempts_to_grant_route_authority",
        "execution_gate_outcome_attempts_to_load_prompts",
        "execution_gate_outcome_attempts_to_call_providers",
        "execution_gate_outcome_attempts_to_use_embeddings",
        "execution_gate_outcome_exceeds_next_scope",
    ]
    for reason in reasons:
        assert reason in text


def test_mlrt43_vocabulary_remains_non_authoritative() -> None:
    text = read(DOC)
    assert "controlled_minimal_source_file_creation_patch_execution_gate_outcome_ready_for_authorization_planning_only" in text
    assert POS_LABEL in text
    assert "This label does not authorize source creation" in text
    assert "It does not authorize execution" in text
    assert NEXT_TITLE in text


def test_mlrt43_manifest_records_planning_only_boundaries() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        "execution_gate_outcome_planning_only",
        "python_source_files_created",
        "source_files_created",
        "execution_gate_run",
        "execution_gate_outcome_produced",
        "planned_future_source_path",
        "testing_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_python_source_files_created": false' in manifest
    assert f'"{PREFIX}_source_files_created": false' in manifest
    assert f'"{PREFIX}_execution_gate_run": false' in manifest
    assert f'"{PREFIX}_execution_gate_outcome_produced": false' in manifest
    assert f'"{PREFIX}_testing_started": false' in manifest


def test_mlrt43_has_no_python_implementation_files() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt43_readme_references_feature() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "Tests do not start at MLRT-43" in readme


if __name__ == "__main__":
    test_mlrt43_docs_exist()
    test_mlrt43_uses_compact_freeze_safe_name()
    test_mlrt43_is_execution_gate_outcome_planning_only()
    test_mlrt43_boundaries_prevent_source_and_runtime()
    test_mlrt43_planned_source_path_remains_absent()
    test_mlrt43_required_evidence_is_safe()
    test_mlrt43_rejection_reasons_are_comprehensive()
    test_mlrt43_vocabulary_remains_non_authoritative()
    test_mlrt43_manifest_records_planning_only_boundaries()
    test_mlrt43_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt43_readme_references_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-43 Execution Gate Outcome Plan v1, "
        "immutable governed documentation-only execution-gate outcome planning after MLRT-42 freeze with FREEZE_MEMORY_STATUS OK, "
        "compact freeze-safe name, candidate reliability not validated, ML implementation not unlocked, no Python source files created, "
        "no source files authorized, no source files created, no parent folders created, no source creation authorization granted, "
        "no source creation records created, no source creation code created, no source creation patch created, no controlled minimal source-file creation patch created, "
        "no future source path created, no execution gate run, no execution-gate outcome produced, no execution approved, "
        "no dry run executed, no candidate execution, no candidate outputs created, no case execution, no case scoring, no route comparison, "
        "no report generation, no route authority, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, "
        f"no batch mode, no persistence, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is {NEXT_TITLE}"
    )
    print("SANDBOX_RSS_MLRT43_EXECUTION_GATE_OUTCOME_PLAN_V1_VALIDATION_OK")
