from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_44_SOURCE_CREATION_AUTHORIZATION_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "rss_mlrt44_source_creation_auth_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-44 Source Creation Authorization Plan v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-45 Source Creation Authorization Outcome Plan v1"
POS_LABEL = "RSS_MLRT44_READY_FOR_SOURCE_CREATION_AUTHORIZATION_OUTCOME_PLANNING_ONLY"
PREFIX = "rss_mlrt44_source_creation_authorization_plan"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt44_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt44_uses_compact_freeze_safe_name() -> None:
    text = read(DOC)
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "Compact freeze-safe naming" in text
    assert "Windows and Freeze Feature form filename limits" in text


def test_mlrt44_is_authorization_planning_only() -> None:
    text = read(DOC)
    required = [
        "Status: governed documentation-only source-creation authorization planning milestone.",
        "MLRT-44 is still not source code.",
        "It is not source-file authorization execution.",
        "It is not an authorization outcome.",
        "MLRT-44 only plans the constraints",
        "does not authorize source creation",
        "does not execute authorization",
        "does not approve the source path",
        "does not create the source file",
        "does not create the parent folder",
    ]
    for item in required:
        assert item in text


def test_mlrt44_boundaries_prevent_source_and_runtime() -> None:
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
        "does not execute authorization",
        "does not approve authorization",
        "does not create an authorization outcome",
    ]:
        assert item in text


def test_mlrt44_planned_source_path_remains_absent() -> None:
    assert PLANNED_SOURCE in read(DOC)
    assert not (ROOT / PLANNED_SOURCE).exists()


def test_mlrt44_required_evidence_is_safe() -> None:
    text = read(DOC)
    required = [
        "mlrt_43_freeze_confirmed",
        "freeze_memory_status_ok",
        "startup_freeze_context_refreshed",
        "mlrt_44_source_creation_authorization_plan_available",
        "planned_future_source_path_exact",
        "planned_future_source_path_absent_before_authorization",
        "single_file_creation_limit_confirmed",
        "source_file_inert_contract_confirmed",
        "source_file_import_safe_contract_confirmed",
        "authorization_plan_non_authoritative",
        "authorization_plan_no_source_created",
        "authorization_plan_no_patch_execution",
        "authorization_plan_no_test_execution",
        "authorization_plan_no_reliability_claim",
        "authorization_plan_only_allows_authorization_outcome_planning",
    ]
    for item in required:
        assert item in text


def test_mlrt44_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    reasons = [
        "missing_mlrt44_freeze",
        "planned_future_source_path_already_exists",
        "source_creation_attempted_during_authorization_plan",
        "source_authorization_executed_during_authorization_plan",
        "authorization_plan_attempts_to_create_source_file",
        "authorization_plan_attempts_to_execute_patch",
        "authorization_plan_attempts_to_run_source_creation",
        "authorization_plan_attempts_to_run_tests",
        "authorization_plan_attempts_to_claim_reliability",
        "authorization_plan_attempts_to_grant_route_authority",
        "authorization_plan_attempts_to_load_prompts",
        "authorization_plan_attempts_to_call_providers",
        "authorization_plan_attempts_to_use_embeddings",
        "authorization_plan_exceeds_next_scope",
    ]
    for reason in reasons:
        assert reason in text


def test_mlrt44_vocabulary_remains_non_authoritative() -> None:
    text = read(DOC)
    assert "source_creation_authorization_ready_for_outcome_planning_only" in text
    assert POS_LABEL in text
    assert "This label does not authorize source creation" in text
    assert "It does not authorize execution" in text
    assert "It does not create an outcome" in text
    assert NEXT_TITLE in text


def test_mlrt44_manifest_records_planning_only_boundaries() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        "source_creation_authorization_planning_only",
        "python_source_files_created",
        "source_files_created",
        "source_authorization_executed",
        "source_authorization_outcome_produced",
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
    assert f'"{PREFIX}_source_authorization_executed": false' in manifest
    assert f'"{PREFIX}_source_authorization_outcome_produced": false' in manifest
    assert f'"{PREFIX}_testing_started": false' in manifest


def test_mlrt44_has_no_python_implementation_files() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt44_readme_references_feature() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "Tests do not start at MLRT-44" in readme


if __name__ == "__main__":
    test_mlrt44_docs_exist()
    test_mlrt44_uses_compact_freeze_safe_name()
    test_mlrt44_is_authorization_planning_only()
    test_mlrt44_boundaries_prevent_source_and_runtime()
    test_mlrt44_planned_source_path_remains_absent()
    test_mlrt44_required_evidence_is_safe()
    test_mlrt44_rejection_reasons_are_comprehensive()
    test_mlrt44_vocabulary_remains_non_authoritative()
    test_mlrt44_manifest_records_planning_only_boundaries()
    test_mlrt44_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt44_readme_references_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-44 Source Creation Authorization Plan v1, "
        "immutable governed documentation-only source-creation authorization planning after MLRT-43 freeze with FREEZE_MEMORY_STATUS OK, "
        "compact freeze-safe name, candidate reliability not validated, ML implementation not unlocked, no Python source files created, "
        "no source files authorized, no source files created, no parent folders created, no source creation authorization executed, "
        "no source creation authorization outcome produced, no source creation records created, no source creation code created, no source creation patch created, "
        "no controlled minimal source-file creation patch created, no future source path created, no execution gate run, no execution-gate outcome produced, "
        "no dry run executed, no candidate execution, no candidate outputs created, no case execution, no case scoring, no route comparison, "
        "no report generation, no route authority, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, "
        f"no batch mode, no persistence, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is {NEXT_TITLE}"
    )
    print("SANDBOX_RSS_MLRT44_SOURCE_CREATION_AUTH_PLAN_V1_VALIDATION_OK")
