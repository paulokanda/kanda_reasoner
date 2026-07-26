from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation"
DOC = LAB_BOX / "LAB_CLOSURE_NEXT_PHASE_READINESS_REVIEW.md"
README = LAB_BOX / "README.md"
PHASE = LAB_BOX / "LAB_PHASE_BOUNDARY.md"
ALLOWED = LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_closure_next_phase_readiness_review_v1"
ALLOWED_LAB_PYTHON_FILES = [
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py",
]
FORBIDDEN_NEW_ARTIFACTS = [
    LAB_BOX / "readiness_approval",
    LAB_BOX / "candidate_reliability_results",
    LAB_BOX / "runtime_activation",
    LAB_BOX / "ml_candidate",
]
FORBIDDEN_DOC_PHRASES = [
    "LAB-13 is ML/router reliability evidence",
    "critical boundary error budget is greater than 0",
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


def test_lab13_files_exist_and_python_surface_is_unchanged() -> None:
    assert DOC.is_file()
    assert README.is_file()
    assert PHASE.is_file()
    assert ALLOWED.is_file()
    assert _lab_python_files() == ALLOWED_LAB_PYTHON_FILES
    for path in FORBIDDEN_NEW_ARTIFACTS:
        assert not path.exists(), path


def test_lab13_doc_defines_closure_without_candidate_execution_or_authority() -> None:
    text = _read(DOC)
    assert FEATURE_ID in text
    for phrase in (
        "documentation-only LAB closure and next-phase readiness review",
        "not a candidate evaluation milestone",
        "does not run cases",
        "evaluate a candidate",
        "does not unlock direct ML implementation",
        "Critical boundary error budget remains `0`",
        "If candidate output can reach runtime, the LAB closure fails.",
        "LAB-13 is not ML/router reliability evidence",
        "MLRT-0 - Controlled Non-Runtime ML/Router Candidate Reliability Test Plan",
        "ML implementation remains blocked",
    ):
        assert phrase in text, phrase
    for phrase in FORBIDDEN_DOC_PHRASES:
        assert phrase not in text, phrase


def test_lab13_review_scope_and_readiness_labels_are_declared() -> None:
    text = _read(DOC)
    for milestone in (
        "RG-LAB-000",
        "LAB-0 Phase Boundary + Lab Charter / Entry Gate",
        "LAB-7 Lab Self-Validation Gate",
        "LAB-10 Candidate Evaluation Harness Interface",
        "LAB-11 Corpus V1 Expansion",
        "LAB-12 Error Canonization Intake Spec",
    ):
        assert milestone in text, milestone
    for label in (
        "NOT_READY_FOR_CANDIDATE_RELIABILITY_TESTING",
        "READY_FOR_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLANNING_ONLY",
        "BLOCKED_BY_LAB_INVALID",
        "BLOCKED_BY_CRITICAL_BOUNDARY_RISK",
        "BLOCKED_BY_MISSING_FREEZE_OR_STARTUP_REFRESH",
        "NEEDS_HUMAN_REVIEW_BEFORE_NEXT_PHASE",
    ):
        assert f"`{label}`" in text, label


def test_lab13_readme_phase_and_allowed_artifacts_point_to_mlrt0() -> None:
    for path in (README, PHASE, ALLOWED):
        text = _read(path)
        assert "LAB-13" in text
        assert "MLRT-0" in text
        assert "must not" in text
        assert "route authority" in text
        assert "Copilot" in text


def test_lab13_manifest_declares_closure_review_without_unlocking_ml() -> None:
    data = _manifest()
    assert data["ml_lab_closure_next_phase_readiness_review_feature_id"] == FEATURE_ID
    assert data["ml_lab_closure_next_phase_readiness_review_schema_version"] == "lab-13-closure-next-phase-readiness-review"
    assert data["ml_lab_closure_next_phase_readiness_review_documentation_only"] is True
    assert data["ml_lab_closure_next_phase_readiness_review_candidate_evaluation_executed"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_cases_executed"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_cases_scored"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_reports_generated"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_reports_persisted"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_route_authority"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_prompt_loading"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_provider_calls"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_embeddings"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_persistence"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_activation_key"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_field_test_mode"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_runtime_pilot"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_copilot_behavior"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_candidate_reliability_validated"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_ml_implementation_unlocked"] is False
    assert data["ml_lab_closure_next_phase_readiness_review_positive_label"] == "READY_FOR_CONTROLLED_NON_RUNTIME_CANDIDATE_RELIABILITY_TEST_PLANNING_ONLY"
    assert data["ml_lab_closure_next_phase_readiness_review_critical_boundary_error_budget"] == 0
    assert data["ml_lab_closure_next_phase_readiness_review_allowed_lab_python_files"] == ALLOWED_LAB_PYTHON_FILES
    assert "MLRT-0" in data["ml_lab_closure_next_phase_readiness_review_next_safe_milestone"]


if __name__ == "__main__":
    test_lab13_files_exist_and_python_surface_is_unchanged()
    test_lab13_doc_defines_closure_without_candidate_execution_or_authority()
    test_lab13_review_scope_and_readiness_labels_are_declared()
    test_lab13_readme_phase_and_allowed_artifacts_point_to_mlrt0()
    test_lab13_manifest_declares_closure_review_without_unlocking_ml()
    print(
        "CONTRACT_TEST_OK: LAB-13 ML LAB Closure / Next-Phase Readiness Review v1, "
        "immutable governed documentation-only lab closure/readiness review after LAB-12 freeze with "
        "FREEZE_MEMORY_STATUS OK, defines closure scope across RG-LAB-000 and LAB-0 through LAB-12, "
        "defines readiness questions, readiness labels, mandatory closure preconditions, critical boundary "
        "closure rules, no candidate evaluation, no case execution, no case scoring, no route comparison, "
        "no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, "
        "no live router-canon reads, no runtime router imports, no corpus mutation, no fixture mutation, "
        "no router-canon mutation, no prompt-library mutation, no freeze-memory mutation, no gold-registry "
        "mutation, no error library, no automatic canonization, no report generation, no report persistence, "
        "no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent "
        "ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, candidate "
        "reliability not validated, ML implementation not unlocked, critical boundary incidents must not be hidden "
        "by aggregate soft metrics, zero critical boundary doctrine preserved, next safe milestone is MLRT-0 "
        "Controlled Non-Runtime ML/Router Candidate Reliability Test Plan"
    )
    print("SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CLOSURE_NEXT_PHASE_READINESS_REVIEW_V1_VALIDATION_OK")
