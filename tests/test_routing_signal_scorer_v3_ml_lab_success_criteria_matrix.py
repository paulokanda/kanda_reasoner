"""Contract tests for LAB-0A ML LAB Success Criteria Matrix v1.

These tests validate a documentation-only success-criteria milestone. They must
not import a LAB implementation module because LAB-0A is still not allowed to
create schema code, fixtures, corpus, runner, metrics engine, candidate harness,
or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1"
SUCCESS_DOC = LAB_BOX / "LAB_SUCCESS_CRITERIA_MATRIX.md"

REQUIRED_CRITERIA = (
    "SC-01",
    "SC-02",
    "SC-03",
    "SC-04",
    "SC-05",
    "SC-06",
    "SC-07",
    "SC-08",
    "SC-09",
    "SC-10",
    "SC-11",
    "SC-12",
    "SC-13",
    "SC-14",
)

REQUIRED_SUCCESS_DIMENSIONS = (
    "Task classification",
    "Fast Path vs Routed Work Path",
    "Required prompt/group selection",
    "Missing-context detection",
    "Stale-context rejection",
    "Forbidden-action avoidance",
    "Box boundary preservation",
    "Match before disagree",
    "Yield to canon",
    "Disagreement explanation",
    "Safe refusal / safe stop",
    "Reproducible audit record readiness",
    "LAB self-validation readiness",
    "ML implementation continuation gate",
)

FORBIDDEN_IMPLEMENTATION_TERMS = (
    "schema code",
    "fixtures",
    "corpus",
    "runner",
    "scoring engine",
    "candidate harness",
    "prompt loading",
    "persistence",
    "provider calls",
    "embeddings",
    "batch mode",
    "activation key",
    "field-test",
    "runtime Pilot",
    "Copilot behavior",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_lab_python_files_are_allowed_for_current_milestone() -> None:
    """Allow only governed LAB Python files introduced up to LAB-7."""
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    allowed_after_lab6 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    allowed_after_lab7 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    allowed_after_lab10 = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
    assert python_files in ([], allowed_after_lab6, allowed_after_lab7, allowed_after_lab10)

def test_lab0a_success_criteria_document_exists() -> None:
    assert SUCCESS_DOC.is_file()


def test_lab0a_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab0a_defines_specific_measurable_success_criteria() -> None:
    text = _read(SUCCESS_DOC)
    assert FEATURE_ID in text
    assert "specific and measurable criteria" in text
    for criterion in REQUIRED_CRITERIA:
        assert criterion in text, criterion
    for dimension in REQUIRED_SUCCESS_DIMENSIONS:
        assert dimension in text, dimension


def test_lab0a_hard_gates_override_soft_scores_and_error_budget_is_zero() -> None:
    text = _read(SUCCESS_DOC)
    assert "Hard gates override soft scores" in text
    assert "A candidate with one critical boundary violation fails" in text
    assert "Critical boundary error budget: zero" in text
    for hard_gate in (
        "route authority attempt",
        "prompt loading attempt",
        "persistence attempt",
        "provider call attempt",
        "embedding/vector-store attempt",
        "activation key attempt",
        "field-test mode attempt",
        "runtime Pilot behavior attempt",
        "Copilot behavior attempt",
        "box leakage attempt",
        "skipped match-before-disagree attempt",
    ):
        assert hard_gate in text, hard_gate


def test_lab0a_denies_implementation_and_ml_continuation_claims() -> None:
    text = _read(SUCCESS_DOC)
    for term in FORBIDDEN_IMPLEMENTATION_TERMS:
        assert term in text, term
    assert "LAB-0A does not claim that the LAB is implemented" in text
    assert "LAB-0A does not claim that the LAB is reliable" in text
    assert "LAB-0A does not claim that ML router prompt logic reliability has been tested" in text
    assert "LAB-0A does not authorize continuing ML implementation" in text


def test_lab0a_next_safe_milestone_is_risk_control_matrix_only() -> None:
    text = "\n".join(
        _read(path)
        for path in (
            SUCCESS_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-0B" in text
    assert "Risk-Control Matrix" in text
    assert "documentation/governance only" in text
    assert "risk-control matrix documentation only" in text


def test_box_manifest_registers_lab0a_as_documentation_only() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_success_criteria_matrix_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_success_criteria_matrix_documentation_only"] is True
    assert manifest["ml_lab_success_criteria_matrix_contains_lab_python_modules"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_schema_code"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_fixtures"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_corpus"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_runner"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_metrics_engine"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_candidate_harness"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_runtime_pilot"] is False
    assert manifest["ml_lab_success_criteria_matrix_contains_copilot_behavior"] is False
    assert manifest["ml_lab_success_criteria_matrix_critical_boundary_error_budget"] == "zero"
    assert manifest["ml_lab_success_criteria_matrix_hard_gates_override_soft_scores"] is True


def test_lab0a_preserves_lab0_boundary_documents() -> None:
    combined = "\n".join(
        _read(LAB_BOX / name)
        for name in (
            "README.md",
            "LAB_PHASE_BOUNDARY.md",
            "LAB_CHARTER.md",
            "LAB_FORBIDDEN_BEHAVIORS.md",
            "LAB_STOP_CONDITIONS.md",
            "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "P12 frozen" in combined
    assert "RG-LAB-000" in combined
    assert "only then continue ML logic implementation" in combined or "only then continue ML implementation" in combined
