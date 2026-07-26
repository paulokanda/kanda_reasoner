"""Contract tests for LAB-2 ML LAB Failure Taxonomy + Critical Violation Model v1.

These tests validate a documentation-only taxonomy/design milestone. They must not
import LAB implementation code because LAB-2 is not allowed to create schema code,
fixtures, corpus, runner, scoring engine, metrics engine, candidate harness, live
risk detectors, import scanners, write guards, provider adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1"
TAXONOMY_DOC = LAB_BOX / "LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL.md"

OUTCOMES = (
    "PASS",
    "SOFT_FAIL",
    "HARD_FAIL",
    "CRITICAL_FAIL",
    "LAB_INVALID",
    "NEEDS_HUMAN_REVIEW",
    "NOT_EVALUATED",
)

FAILURE_FAMILIES = (
    "ROUTING_CLASSIFICATION_FAILURE",
    "PROMPT_SELECTION_FAILURE",
    "MISSING_CONTEXT_FAILURE",
    "STALE_OR_CONFLICTING_CONTEXT_FAILURE",
    "GOVERNANCE_WORKFLOW_FAILURE",
    "PATCH_INSTALL_FREEZE_FAILURE",
    "BOX_BOUNDARY_FAILURE",
    "SECURITY_INJECTION_FAILURE",
    "AUTHORITY_ESCALATION_FAILURE",
    "MATCH_BEFORE_DISAGREE_FAILURE",
    "EXPLANATION_AND_EVIDENCE_FAILURE",
    "SCHEMA_AND_CONTRACT_FAILURE",
    "FIXTURE_AND_CORPUS_FAILURE",
    "LAB_INTEGRITY_FAILURE",
    "HUMAN_REVIEW_FAILURE",
    "RELIABILITY_CLAIM_FAILURE",
    "ACTIVATION_AND_RUNTIME_DRIFT_FAILURE",
)

CRITICAL_CODES = (
    "ROUTE_AUTHORITY_OVERRIDE",
    "UNAUTHORIZED_PROMPT_LOAD",
    "RUNTIME_ACTION",
    "PERSISTENCE_ATTEMPT",
    "PROVIDER_CALL_ATTEMPT",
    "EMBEDDING_ATTEMPT",
    "TRAINING_DATA_USE_ATTEMPT",
    "BATCH_MODE_ATTEMPT",
    "CANON_MUTATION",
    "FREEZE_MEMORY_MUTATION",
    "GOLD_REGISTRY_MUTATION",
    "PROMPT_LIBRARY_MUTATION",
    "FIELD_TEST_MODE_ATTEMPT",
    "ACTIVATION_KEY_ATTEMPT",
    "COPILOT_BEHAVIOR_ATTEMPT",
    "HUMAN_APPROVAL_RECORDING_ATTEMPT",
    "READINESS_APPROVAL_ATTEMPT",
    "PRODUCTION_IMPORTS_LAB",
    "LAB_IMPORTS_RUNTIME_ROUTER",
    "LAB_IMPORTS_PROMPT_LOADER",
    "LAB_IMPORTS_PROVIDER_OR_EMBEDDING",
    "LAB_WRITES_OUTSIDE_AUTHORIZED_PATHS",
    "LIVE_CANON_COUPLING",
    "LIVE_FREEZE_MEMORY_COUPLING",
    "LIVE_GOLD_REGISTRY_COUPLING",
    "PROMPT_INJECTION_BYPASS",
    "SYSTEM_PROMPT_OR_PROMPT_FILE_LEAK_ATTEMPT",
    "INSECURE_OUTPUT_TO_DOWNSTREAM",
    "LAB_INVALID_RESULT_REPORTED_AS_PASS",
    "RELIABILITY_CLAIM_WITH_CRITICAL_FAILURE",
    "ML_IMPLEMENTATION_CONTINUED_PREMATURELY",
)

LAB_INVALID_CODES = (
    "LAB_SELF_VALIDATION_BYPASSED",
    "LAB_SELF_VALIDATION_FAILED",
    "FIXTURE_HASH_MISMATCH",
    "SCHEMA_VIOLATION_IN_GOLD_FIXTURE",
    "RUNNER_VERSION_MISSING",
    "SCORING_MODEL_VERSION_MISSING",
    "CORPUS_VERSION_MISSING",
    "CANON_VERSION_REFERENCE_MISSING",
    "LAB_REPORT_INCOMPLETE",
    "LAB_RUN_NOT_REPRODUCIBLE",
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

def test_lab2_taxonomy_doc_exists() -> None:
    assert TAXONOMY_DOC.is_file()


def test_lab2_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab2_declares_documentation_only_scope_and_non_claims() -> None:
    text = _read(TAXONOMY_DOC)
    assert FEATURE_ID in text
    assert "LAB-2 is documentation/governance design only" in text
    for phrase in (
        "does not implement scoring",
        "does not implement schema validation",
        "does not implement a runner",
        "does not create fixtures or corpus cases",
        "does not evaluate a candidate",
        "does not prove the LAB is reliable",
        "does not prove ML router prompt logic reliability",
        "does not authorize continuing ML implementation",
    ):
        assert phrase in text, phrase


def test_lab2_declares_outcomes_and_hard_gate_principle() -> None:
    text = _read(TAXONOMY_DOC)
    for outcome in OUTCOMES:
        assert outcome in text, outcome
    assert "Hard gates are evaluated before soft scores" in text
    assert "Aggregate accuracy" in text
    assert "cannot compensate for a hard or critical failure" in text
    assert "critical failure count > 0 → reliability claim blocked" in text
    assert "LAB_INVALID → candidate evaluation not trusted" in text


def test_lab2_declares_failure_families() -> None:
    text = _read(TAXONOMY_DOC)
    for family in FAILURE_FAMILIES:
        assert family in text, family


def test_lab2_declares_key_project_specific_failure_codes() -> None:
    text = _read(TAXONOMY_DOC)
    for code in (
        "FALSE_FAST_PATH",
        "MISSED_ROUTED_WORK",
        "PROMPT_OMISSION",
        "MISSING_VALIDATION_EVIDENCE_FAILURE",
        "STALE_FREEZE_SIDECAR_ACCEPTANCE",
        "HANDOFF_CORRUPTION",
        "SKIPPED_BOX_BOUNDARY_AUDIT",
        "SKIPPED_FREEZE_MEMORY_STATUS_CHECK",
        "PATCH_INSTALLS_KANDA_FREEZE_HINT_TO_PROJECT_ROOT",
        "PROJECT_FREEZE_LEDGER_USED_AS_ACTIVE_MEMORY",
        "BOX_LEAKAGE",
        "FIXTURE_CONTAMINATION",
        "PROMPT_INJECTION_BYPASS",
        "UNTRUSTED_TEXT_TREATED_AS_INSTRUCTION",
        "MATCH_BEFORE_DISAGREE_VIOLATION",
        "CANDIDATE_TREATED_AS_GROUND_TRUTH",
        "FALSE_CERTAINTY",
        "CONFIDENCE_MISCALIBRATION",
        "NON_AUTHORITATIVE_WRAPPER_MISSING",
        "CANON_VERSION_REFERENCE_MISSING",
        "CORPUS_OVERFITS_KNOWN_CASES",
        "LAB_INVALID_RESULT_REPORTED_AS_PASS",
        "HUMAN_REVIEW_RECORDED_BY_CANDIDATE",
        "ML_IMPLEMENTATION_CONTINUED_PREMATURELY",
        "ACTIVATION_GATE_BYPASSED",
        "MATURITY_LEVEL_OVERCLAIMED",
    ):
        assert code in text, code


def test_lab2_declares_critical_violation_model() -> None:
    text = _read(TAXONOMY_DOC)
    assert "Any one of them must be treated as `CRITICAL_FAIL`" in text
    for code in CRITICAL_CODES:
        assert code in text, code
    assert "critical boundary error budget equals zero" in text or "critical_boundary_error_budget = 0" in text


def test_lab2_declares_lab_invalid_classes() -> None:
    text = _read(TAXONOMY_DOC)
    for code in LAB_INVALID_CODES:
        assert code in text, code
    assert "blocks candidate evaluation" in text
    assert "not a candidate pass or fail" in text


def test_lab2_preserves_multiturn_and_roadmap_lock() -> None:
    text = _read(TAXONOMY_DOC)
    for phrase in (
        "continue",
        "after LAB-1 freeze → LAB-2 taxonomy/design only",
        "after P12 → RG-LAB-000 before LAB work",
        "RG-LAB-000 → LAB-0 through LAB reliability gates",
        "LAB self-validation passes",
        "ML router prompt logic reliability testing",
        "only then continue ML logic implementation",
    ):
        assert phrase in text, phrase


def test_lab2_next_safe_milestone_is_scoring_model_hard_gates() -> None:
    combined = "\n".join(
        _read(path)
        for path in (
            TAXONOMY_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "LAB-3" in combined
    assert "Scoring Model + Hard Gates" in combined
    assert "later lab implementation only after documentation, shielding, taxonomy, scoring, and schema gates are frozen" in combined


def test_box_manifest_registers_lab2_as_documentation_only_taxonomy() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_failure_taxonomy_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_failure_taxonomy_documentation_only"] is True
    assert manifest["ml_lab_failure_taxonomy_contains_lab_python_modules"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_schema_code"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_fixtures"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_corpus"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_runner"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_scoring_engine"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_metrics_engine"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_candidate_harness"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_live_detectors"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_import_scanner"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_write_guard"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_runtime_pilot"] is False
    assert manifest["ml_lab_failure_taxonomy_contains_copilot_behavior"] is False
    assert manifest["ml_lab_failure_taxonomy_critical_boundary_error_budget"] == 0
    assert manifest["ml_lab_failure_taxonomy_lab_invalid_blocks_candidate_evaluation"] is True
    assert manifest["ml_lab_failure_taxonomy_critical_fail_blocks_reliability_claims"] is True
    assert manifest["ml_lab_failure_taxonomy_ml_implementation_blocked_until_lab_and_router_reliability_validated"] is True
    assert manifest["ml_lab_failure_taxonomy_next_safe_milestone"] == "LAB-3 Scoring Model + Hard Gates after local validation and freeze with FREEZE_MEMORY_STATUS OK"


def test_lab2_preserves_prior_lab_documentation_gates() -> None:
    combined = "\n".join(
        _read(LAB_BOX / name)
        for name in (
            "README.md",
            "LAB_PHASE_BOUNDARY.md",
            "LAB_CHARTER.md",
            "LAB_FORBIDDEN_BEHAVIORS.md",
            "LAB_STOP_CONDITIONS.md",
            "LAB_ALLOWED_ARTIFACTS.md",
            "LAB_SUCCESS_CRITERIA_MATRIX.md",
            "LAB_RISK_CONTROL_MATRIX.md",
            "LAB_SLO_CRITICAL_ERROR_BUDGET.md",
            "LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md",
            "LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "LAB-0A adds a success criteria matrix only" in combined
    assert "LAB-0B adds a risk-control matrix only" in combined
    assert "LAB-0C adds a LAB SLO / Critical Error Budget Declaration only" in combined
    assert "LAB-1 adds a Lab Box Boundary + Shielding Manifest only" in combined
    assert "critical_boundary_error_budget = 0" in combined
    assert "ML logic implementation remains blocked" in combined
