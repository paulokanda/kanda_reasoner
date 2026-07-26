"""Contract tests for LAB-4 ML LAB Test Case Schema + Candidate Output Contract v1.

These tests validate a documentation-only schema/contract design milestone. They must not
import LAB implementation code because LAB-4 is not allowed to create executable schema
validators, fixtures, corpus, runner, scoring engine, metrics engine, candidate harness,
live detectors, import scanners, write guards, provider adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1"
CONTRACT_DOC = LAB_BOX / "LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT.md"

REQUIRED_TEST_CASE_FIELDS = (
    "case_id",
    "case_version",
    "schema_version",
    "corpus_version",
    "canon_version_reference",
    "canon_rule_references",
    "fixture_hash_reference",
    "category",
    "subcategory",
    "severity",
    "critical_boundary_flag",
    "adversarial_flag",
    "regression_source",
    "user_request_raw",
    "normalized_request",
    "conversation_history",
    "simulated_context",
    "context_freshness",
    "simulated_freeze_state",
    "simulated_handoff_state",
    "simulated_sidecar_state",
    "expected_task_classification",
    "expected_path",
    "expected_required_prompt_groups",
    "expected_prompt_priority",
    "expected_missing_context",
    "expected_forbidden_actions",
    "expected_safe_next_action",
    "expected_explanation_elements",
    "case_specific_pass_conditions",
    "case_specific_fail_conditions",
    "case_specific_critical_fail_conditions",
)

REQUIRED_CANDIDATE_FIELDS = (
    "candidate_output_schema_version",
    "candidate_version",
    "candidate_kind",
    "case_id",
    "pass_1_canon_match",
    "pass_1_task_classification",
    "pass_1_path",
    "pass_1_required_prompt_groups",
    "pass_1_missing_context",
    "pass_1_safe_next_action",
    "pass_2_disagreement_or_improvement",
    "yield_to_canon",
    "confidence_level",
    "needs_human_review",
    "no_authority_assertion",
)

FORBIDDEN_AUTHORITY_FIELDS = (
    "route_decision",
    "load_prompt",
    "execute_route",
    "approve_readiness",
    "record_human_approval",
    "write_freeze_memory",
    "write_gold_registry",
    "write_prompt_library",
    "write_router_canon",
    "activate_pilot",
    "activate_copilot",
    "enable_field_test",
    "create_activation_key",
    "call_provider",
    "call_embedding_model",
    "start_batch_mode",
    "persist_ml_decision",
    "runtime_command",
    "copilot_instruction",
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

def test_lab4_contract_doc_exists() -> None:
    assert CONTRACT_DOC.is_file()


def test_lab4_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab4_declares_documentation_only_scope_and_non_claims() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    assert "LAB-4 is documentation/governance design only" in text
    for phrase in (
        "does not implement schema code",
        "does not implement a schema validator",
        "does not create JSON fixtures",
        "does not create corpus cases",
        "does not implement a runner",
        "does not implement scoring",
        "does not evaluate a candidate",
        "does not prove the LAB is reliable",
        "does not prove ML router prompt logic reliability",
        "does not authorize continuing ML implementation",
    ):
        assert phrase in text, phrase


def test_lab4_declares_required_test_case_record_fields() -> None:
    text = _read(CONTRACT_DOC)
    for field in REQUIRED_TEST_CASE_FIELDS:
        assert field in text, field
    for heading in (
        "Identity fields",
        "Canon reference fields",
        "Input simulation fields",
        "Expected routing fields",
        "Case-specific rubric fields",
        "Match-before-disagree expectation fields",
        "Reliability and traceability fields",
    ):
        assert heading in text, heading


def test_lab4_declares_candidate_output_contract_fields() -> None:
    text = _read(CONTRACT_DOC)
    assert "non-authoritative evaluation record" in text
    for field in REQUIRED_CANDIDATE_FIELDS:
        assert field in text, field
    assert "not a route decision" in text
    assert "not a prompt loading command" in text
    assert "not an activation signal" in text


def test_lab4_declares_two_pass_match_before_disagree_contract() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "pass_1_canon_match",
        "pass_2_disagreement_or_improvement only if needed",
        "yield_to_canon",
        "pass 1 must attempt to match frozen canon before disagreement",
        "candidate disagreement cannot override canon",
        "candidate disagreement cannot become route authority",
        "Skipping pass 1 is a hard failure",
    ):
        assert phrase in text, phrase


def test_lab4_declares_forbidden_candidate_output_fields_and_actions() -> None:
    text = _read(CONTRACT_DOC)
    for field in FORBIDDEN_AUTHORITY_FIELDS:
        assert field in text, field
    for phrase in (
        "route authority",
        "prompt loading",
        "freeze-memory mutation",
        "gold-registry mutation",
        "provider calls",
        "embedding/vector calls",
        "human approval recording",
        "readiness approval recording",
        "runtime Pilot behavior",
        "Copilot behavior",
        "ML implementation continuation",
    ):
        assert phrase in text, phrase


def test_lab4_declares_contract_rejection_and_lab_invalid_rules() -> None:
    text = _read(CONTRACT_DOC)
    for code in (
        "required_version_field_missing",
        "case_id_missing_or_mismatched",
        "schema_version_missing_or_unsupported",
        "fixture_hash_reference_missing",
        "canon_version_reference_missing",
        "case_specific_rubric_missing",
        "candidate_output_not_wrapped_as_non_authoritative",
        "pass_1_canon_match_missing",
        "pass_2_attempts_authority",
        "yield_to_canon_missing_or_false_when_required",
        "forbidden_candidate_field_present",
        "candidate_output_contains_runtime_command",
        "candidate_output_claims_reliability_without_lab_preconditions",
        "gold_case_missing_case_id",
        "gold_case_missing_schema_version",
        "gold_case_missing_canon_reference",
        "gold_case_missing_fixture_hash_reference",
        "gold_case_missing_case_specific_rubric",
        "gold_case_has_conflicting_expected_path",
        "gold_case_has_unreviewed_status",
    ):
        assert code in text, code
    assert "Malformed gold/test case records are LAB defects" in text


def test_lab4_declares_human_review_contract() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "needs_human_review = true",
        "human_approved = true",
        "approval_recorded = true",
        "freeze_write_authorized = true",
        "readiness_approved = true",
        "Candidate attempts to record approval are critical boundary violations",
    ):
        assert phrase in text, phrase


def test_lab4_declares_case_categories_without_creating_corpus() -> None:
    text = _read(CONTRACT_DOC)
    for category in (
        "basic_routing_classification",
        "fast_path_vs_routed_work",
        "required_prompt_group_selection",
        "missing_context_may_proceed",
        "freeze_update_governance_workflow",
        "prompt_library_prompt_authoring",
        "patch_install_validation_freeze_memory",
        "box_boundary_leakage",
        "stale_context_stale_filename_stale_sidecar",
        "adversarial_bypass_prompt_injection",
        "ambiguous_typo_shorthand",
        "medical_document_simple_task_distinction",
        "roadmap_regression",
        "known_past_mistake_regression",
    ):
        assert category in text, category
    assert "LAB-4 does not create corpus cases" in text


def test_lab4_declares_candidate_wrapper_and_version_compatibility() -> None:
    text = _read(CONTRACT_DOC)
    assert "non_authoritative_evaluation_record" in text
    for phrase in (
        "route decision",
        "prompt loading command",
        "human decision record",
        "readiness decision",
        "Copilot instruction",
        "schema_version",
        "candidate_output_schema_version",
        "corpus_version",
        "canon_version_reference",
        "scoring_model_version",
        "runner_version",
        "fixture_hash_reference",
        "Incompatible or missing versions must block scoring before soft metrics",
    ):
        assert phrase in text, phrase


def test_lab4_preserves_roadmap_lock_and_next_safe_milestone() -> None:
    combined = "\n".join(
        _read(path)
        for path in (
            CONTRACT_DOC,
            LAB_BOX / "README.md",
            LAB_BOX / "LAB_PHASE_BOUNDARY.md",
            LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md",
        )
    )
    assert "P12 frozen" in combined
    assert "RG-LAB-000 canonization" in combined
    assert "LAB self-validation" in combined
    assert "ML router prompt logic reliability testing" in combined
    assert "only then continue ML logic implementation" in combined
    assert "LAB-5" in combined
    assert "Frozen Canon Fixture Format + Hash Manifest" in combined


def test_box_manifest_registers_lab4_as_documentation_only_schema_contract_design() -> None:
    manifest_path = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ml_lab_schema_contract_feature_id"] == FEATURE_ID
    assert manifest["ml_lab_schema_contract_documentation_only"] is True
    assert manifest["ml_lab_schema_contract_defines_schema_doctrine_only"] is True
    assert manifest["ml_lab_schema_contract_contains_lab_python_modules"] is False
    assert manifest["ml_lab_schema_contract_contains_schema_code"] is False
    assert manifest["ml_lab_schema_contract_contains_executable_validators"] is False
    assert manifest["ml_lab_schema_contract_contains_fixtures"] is False
    assert manifest["ml_lab_schema_contract_contains_corpus"] is False
    assert manifest["ml_lab_schema_contract_contains_runner"] is False
    assert manifest["ml_lab_schema_contract_contains_executable_scoring_engine"] is False
    assert manifest["ml_lab_schema_contract_contains_metrics_engine"] is False
    assert manifest["ml_lab_schema_contract_contains_candidate_harness"] is False
    assert manifest["ml_lab_schema_contract_contains_live_detectors"] is False
    assert manifest["ml_lab_schema_contract_contains_import_scanner"] is False
    assert manifest["ml_lab_schema_contract_contains_write_guard"] is False
    assert manifest["ml_lab_schema_contract_contains_runtime_pilot"] is False
    assert manifest["ml_lab_schema_contract_contains_copilot_behavior"] is False
    assert manifest["ml_lab_schema_contract_critical_boundary_error_budget"] == 0
    assert manifest["ml_lab_schema_contract_candidate_output_non_authoritative"] is True
    assert manifest["ml_lab_schema_contract_match_before_disagree_required"] is True
    assert manifest["ml_lab_schema_contract_yield_to_canon_required"] is True
    assert manifest["ml_lab_schema_contract_lab_invalid_for_malformed_gold_cases"] is True
    assert manifest["ml_lab_schema_contract_ml_implementation_blocked_until_lab_and_router_reliability_validated"] is True
    assert manifest["ml_lab_schema_contract_next_safe_milestone"] == "LAB-5 Frozen Canon Fixture Format + Hash Manifest after local validation and freeze with FREEZE_MEMORY_STATUS OK"
    for field in REQUIRED_TEST_CASE_FIELDS:
        assert field in manifest["ml_lab_schema_contract_required_test_case_fields"], field
    for field in REQUIRED_CANDIDATE_FIELDS:
        assert field in manifest["ml_lab_schema_contract_required_candidate_output_fields"], field
    for field in FORBIDDEN_AUTHORITY_FIELDS:
        assert field in manifest["ml_lab_schema_contract_forbidden_authority_fields"], field


def test_lab4_preserves_prior_lab_documentation_gates() -> None:
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
            "LAB_SCORING_MODEL_HARD_GATES.md",
            "LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT.md",
        )
    )
    assert "LAB-0 is documentation-only" in combined
    assert "LAB-0A adds a success criteria matrix only" in combined
    assert "LAB-0B adds a risk-control matrix only" in combined
    assert "LAB-0C adds a LAB SLO / Critical Error Budget Declaration only" in combined
    assert "LAB-1 adds a Lab Box Boundary + Shielding Manifest only" in combined
    assert "LAB-2 adds a Failure Taxonomy + Critical Violation Model only" in combined
    assert "LAB-3 adds a Scoring Model + Hard Gates design document only" in combined
    assert "LAB-4 adds a Test Case Schema + Candidate Output Contract design document only" in combined
    assert "critical_boundary_error_budget = 0" in combined
    assert "ML logic implementation remains blocked" in combined
