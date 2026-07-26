from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_47_SOURCE_CREATION_FINAL_HUMAN_REVIEW_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "rss_mlrt47_source_creation_final_review_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-47 Source Creation Final Human Review Plan v1"
PLANNED_SOURCE = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-48 Controlled Minimal Source Creation v1"
POS_LABEL = "RSS_MLRT47_READY_FOR_CONTROLLED_MINIMAL_SOURCE_CREATION_ONLY"
PREFIX = "rss_mlrt47_source_creation_final_human_review_plan"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mlrt47_docs_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()


def test_mlrt47_uses_compact_freeze_safe_name() -> None:
    text = read(DOC)
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "Compact freeze-safe naming" in text
    assert "Windows and Freeze Feature form filename limits" in text


def test_mlrt47_is_final_human_review_only() -> None:
    text = read(DOC)
    required = [
        "Status: governed documentation-only final human-review / go-no-go planning milestone.",
        "MLRT-47 is the final human-review planning gate before the first controlled minimal source creation milestone.",
        "the documentation-only chain must stop before it becomes wasteful",
        "MLRT-47 is still not source code.",
        "It is not source creation.",
        "MLRT-47 does not create the source file",
        "does not create the parent folder",
        "does not unlock training or runtime behavior",
    ]
    for item in required:
        assert item in text


def test_mlrt47_boundaries_prevent_source_runtime_and_item5() -> None:
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
        "does not start Item 5 training/learning governance",
        "Item 5 remains blocked until the non-runtime harness/source surface has been created and tested",
    ]:
        assert item in text


def test_mlrt47_planned_source_path_remains_absent() -> None:
    assert PLANNED_SOURCE in read(DOC)
    assert not (ROOT / PLANNED_SOURCE).exists()


def test_mlrt47_go_no_go_checklist_is_specific() -> None:
    text = read(DOC)
    required = [
        "mlrt_46_freeze_confirmed",
        "freeze_memory_status_ok",
        "planned_future_source_path_absent_before_mlrt48",
        "planned_future_parent_folder_absent_before_mlrt48",
        "mlrt48_scope_limited_to_one_python_file",
        "mlrt48_creates_only_minimal_non_runtime_harness_stub",
        "mlrt48_source_file_inert_contract_confirmed",
        "mlrt48_no_import_time_side_effects_confirmed",
        "mlrt48_no_runtime_router_imports_confirmed",
        "mlrt48_no_prompt_loader_imports_confirmed",
        "mlrt48_no_provider_imports_confirmed",
        "mlrt48_no_training_data_use_confirmed",
        "mlrt48_no_route_authority_confirmed",
        "mlrt48_freeze_required_after_validation",
    ]
    for item in required:
        assert item in text


def test_mlrt47_rejection_reasons_are_comprehensive() -> None:
    text = read(DOC)
    reasons = [
        "missing_mlrt46_freeze",
        "planned_future_source_path_already_exists",
        "planned_future_parent_folder_already_exists",
        "mlrt48_attempts_to_create_more_than_one_source_file",
        "mlrt48_attempts_to_create_runtime_router_behavior",
        "mlrt48_attempts_to_load_prompts",
        "mlrt48_attempts_to_call_providers",
        "mlrt48_attempts_to_use_embeddings",
        "mlrt48_attempts_to_persist",
        "mlrt48_attempts_training_data_use",
        "mlrt48_attempts_route_authority",
        "mlrt48_attempts_candidate_execution",
        "mlrt48_attempts_dry_run_execution",
        "mlrt48_attempts_item5_training_or_learning_governance",
        "mlrt48_exceeds_controlled_minimal_source_creation_scope",
    ]
    for reason in reasons:
        assert reason in text


def test_mlrt47_stop_condition_prevents_more_plan_only_drift() -> None:
    text = read(DOC)
    assert "MLRT-47 is the final planned documentation-only milestone before source creation" in text
    assert "the next safe milestone must be MLRT-48 controlled minimal source creation" in text
    assert "continuing with additional source-creation planning documents after MLRT-47 is considered scope drift" in text
    assert POS_LABEL in text
    assert NEXT_TITLE in text


def test_mlrt47_manifest_records_final_review_boundaries() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        "final_human_review_go_no_go_planning_only",
        "last_plan_only_before_source_creation",
        "python_source_files_created",
        "source_files_created",
        "source_creation_executed",
        "item5_training_governance_started",
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
    assert f'"{PREFIX}_source_creation_executed": false' in manifest
    assert f'"{PREFIX}_testing_started": false' in manifest
    assert f'"{PREFIX}_item5_training_governance_started": false' in manifest
    assert f'"{PREFIX}_last_plan_only_before_source_creation": true' in manifest


def test_mlrt47_has_no_python_implementation_files() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == []


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt47_readme_references_feature() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "final planned documentation-only milestone before source creation" in readme


if __name__ == "__main__":
    test_mlrt47_docs_exist()
    test_mlrt47_uses_compact_freeze_safe_name()
    test_mlrt47_is_final_human_review_only()
    test_mlrt47_boundaries_prevent_source_runtime_and_item5()
    test_mlrt47_planned_source_path_remains_absent()
    test_mlrt47_go_no_go_checklist_is_specific()
    test_mlrt47_rejection_reasons_are_comprehensive()
    test_mlrt47_stop_condition_prevents_more_plan_only_drift()
    test_mlrt47_manifest_records_final_review_boundaries()
    test_mlrt47_has_no_python_implementation_files()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt47_readme_references_feature()
    print(
        "CONTRACT_TEST_OK: MLRT-47 Source Creation Final Human Review Plan v1, "
        "final documentation-only go/no-go before MLRT-48 controlled minimal source creation, "
        "compact freeze-safe name, no Python source files created, no parent folders created, no source creation executed, "
        "no dry run, no candidate execution, no testing start, no Item 5 training governance start, no route authority, "
        "no prompt loading, no provider calls, no embeddings, no persistence, no runtime Pilot, no Copilot behavior, "
        f"critical boundary error budget zero, next safe milestone is {NEXT_TITLE}"
    )
    print("SANDBOX_RSS_MLRT47_SOURCE_CREATION_FINAL_REVIEW_PLAN_V1_VALIDATION_OK")
