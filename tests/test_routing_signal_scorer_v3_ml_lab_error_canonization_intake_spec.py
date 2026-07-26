from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation"
DOC = LAB_BOX / "LAB_ERROR_CANONIZATION_INTAKE_SPEC.md"
README = LAB_BOX / "README.md"
PHASE = LAB_BOX / "LAB_PHASE_BOUNDARY.md"
ALLOWED = LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_error_canonization_intake_spec_v1"
ALLOWED_LAB_PYTHON_FILES = [
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py",
]
FORBIDDEN_NEW_ARTIFACTS = [
    LAB_BOX / "error_library",
    LAB_BOX / "error_canonization",
    LAB_BOX / "regression_cases",
    LAB_BOX / "regression_corpus",
]
FORBIDDEN_DOC_PHRASES = [
    "automatic canonization is allowed",
    "mutation_allowed_by_this_record` is always `true`",
    "LAB-12 provides ML/router reliability evidence",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _lab_python_files() -> list[str]:
    return sorted(
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in LAB_BOX.rglob("*.py")
        if "__pycache__" not in path.parts
    )


def test_lab12_files_exist_and_python_surface_is_unchanged() -> None:
    assert DOC.is_file()
    assert README.is_file()
    assert PHASE.is_file()
    assert ALLOWED.is_file()
    assert _lab_python_files() == ALLOWED_LAB_PYTHON_FILES
    for path in FORBIDDEN_NEW_ARTIFACTS:
        assert not path.exists(), path


def test_lab12_doc_defines_intake_spec_without_mutation_or_execution() -> None:
    text = _read(DOC)
    assert FEATURE_ID in text
    for phrase in (
        "documentation-only error canonization intake specification",
        "not automatic canonization",
        "mutation_allowed_by_this_record` is always `false`",
        "separate governed patch required",
        "human review required",
        "FROZEN_AS_REGRESSION",
        "does not create an error library",
        "does not write regression cases",
        "does not mutate LAB-11 corpus files",
        "does not execute test cases",
        "does not evaluate candidates",
        "does not compare routes",
        "does not grant route authority",
        "does not load prompts",
        "Critical boundary error budget remains `0`",
        "LAB-13 - Lab Closure / Next-Phase Readiness Review",
        "LAB-12 provides no ML/router reliability evidence",
    ):
        assert phrase in text, phrase
    for phrase in FORBIDDEN_DOC_PHRASES:
        assert phrase not in text, phrase


def test_lab12_intake_lifecycle_and_record_fields_are_declared() -> None:
    text = _read(DOC)
    for field in (
        "intake_id",
        "source_lab_run_id",
        "source_case_id",
        "observed_outcome",
        "failure_codes",
        "critical_boundary_flag",
        "lab_invalid_flag",
        "proposed_regression_category",
        "human_review_status",
        "requires_separate_governed_patch",
        "requires_freeze_after_patch",
    ):
        assert f"`{field}`" in text, field
    for state in (
        "PROPOSED",
        "NEEDS_HUMAN_REVIEW",
        "REJECTED",
        "ACCEPTED_FOR_GOVERNED_PATCH",
        "PATCH_CREATED",
        "VALIDATED",
        "FROZEN_AS_REGRESSION",
    ):
        assert f"`{state}`" in text, state


def test_lab12_readme_phase_and_allowed_artifacts_point_to_lab13() -> None:
    for path in (README, PHASE, ALLOWED):
        text = _read(path)
        assert FEATURE_ID in text or path == ALLOWED
        assert "LAB-12" in text
        assert "LAB-13" in text
        assert "must not" in text


def test_lab12_manifest_declares_intake_spec_without_authority() -> None:
    data = _manifest()
    assert data["ml_lab_error_canonization_intake_spec_feature_id"] == FEATURE_ID
    assert data["ml_lab_error_canonization_intake_spec_schema_version"] == "lab-12-error-canonization-intake-spec"
    assert data["ml_lab_error_canonization_intake_spec_documentation_only"] is True
    assert data["ml_lab_error_canonization_intake_spec_intake_records_created"] is False
    assert data["ml_lab_error_canonization_intake_spec_error_library_created"] is False
    assert data["ml_lab_error_canonization_intake_spec_automatic_canonization"] is False
    assert data["ml_lab_error_canonization_intake_spec_corpus_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_fixture_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_router_canon_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_prompt_library_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_freeze_memory_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_gold_registry_mutation"] is False
    assert data["ml_lab_error_canonization_intake_spec_candidate_evaluation_executed"] is False
    assert data["ml_lab_error_canonization_intake_spec_cases_executed"] is False
    assert data["ml_lab_error_canonization_intake_spec_cases_scored"] is False
    assert data["ml_lab_error_canonization_intake_spec_route_authority"] is False
    assert data["ml_lab_error_canonization_intake_spec_prompt_loading"] is False
    assert data["ml_lab_error_canonization_intake_spec_provider_calls"] is False
    assert data["ml_lab_error_canonization_intake_spec_embeddings"] is False
    assert data["ml_lab_error_canonization_intake_spec_persistence"] is False
    assert data["ml_lab_error_canonization_intake_spec_activation_key"] is False
    assert data["ml_lab_error_canonization_intake_spec_field_test_mode"] is False
    assert data["ml_lab_error_canonization_intake_spec_runtime_pilot"] is False
    assert data["ml_lab_error_canonization_intake_spec_copilot_behavior"] is False
    assert data["ml_lab_error_canonization_intake_spec_critical_boundary_error_budget"] == 0
    assert data["ml_lab_error_canonization_intake_spec_allowed_lab_python_files"] == ALLOWED_LAB_PYTHON_FILES
    assert "LAB-13 Lab Closure / Next-Phase Readiness Review" in data["ml_lab_error_canonization_intake_spec_next_safe_milestone"]


if __name__ == "__main__":
    test_lab12_files_exist_and_python_surface_is_unchanged()
    test_lab12_doc_defines_intake_spec_without_mutation_or_execution()
    test_lab12_intake_lifecycle_and_record_fields_are_declared()
    test_lab12_readme_phase_and_allowed_artifacts_point_to_lab13()
    test_lab12_manifest_declares_intake_spec_without_authority()
    print(
        "CONTRACT_TEST_OK: LAB-12 ML LAB Error Canonization Intake Spec v1, "
        "immutable governed documentation-only error canonization intake specification after LAB-11 freeze with "
        "FREEZE_MEMORY_STATUS OK, defines future non-authoritative human-reviewed error intake proposal doctrine, "
        "no error library, no automatic canonization, no intake records created, no regression cases written, "
        "no corpus mutation, no fixture mutation, no router-canon mutation, no prompt-library mutation, "
        "no freeze-memory mutation, no gold-registry mutation, no candidate evaluation, no case execution, "
        "no case scoring, no route comparison, no route authority, no prompt loading, no live prompt-library reads, "
        "no live freeze-memory reads, no live router-canon reads, no runtime router imports, no scoring engine, "
        "no metrics engine, no executable candidate harness, no report generation, no report persistence, "
        "no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, "
        "no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, "
        "critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine "
        "preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router "
        "prompt logic reliability is validated, LAB-13 Lab Closure / Next-Phase Readiness Review next"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_ERROR_CANONIZATION_INTAKE_SPEC_V1_VALIDATION_OK")
