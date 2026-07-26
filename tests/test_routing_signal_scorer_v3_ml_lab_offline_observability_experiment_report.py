"""Contract tests for LAB-9 Offline Observability + Experiment Report v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1"
CONTRACT_DOC = LAB_BOX / "LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT.md"
REPORT_TEMPLATE = LAB_BOX / "report_templates" / "offline_experiment_report_template_v1.json"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
ALLOWED_LAB_PYTHON_FILES = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
FORBIDDEN_AUTHORITY_FIELDS = ['route_decision', 'load_prompt', 'execute_route', 'approve_readiness', 'record_human_approval', 'write_freeze_memory', 'write_gold_registry', 'write_prompt_library', 'write_router_canon', 'activate_pilot', 'activate_copilot', 'enable_field_test', 'call_provider', 'call_embedding_model', 'start_batch_mode', 'persist_ml_decision', 'runtime_command', 'copilot_instruction']


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path):
    return json.loads(_read(path))


def test_lab9_files_exist_and_python_surface_is_unchanged() -> None:
    assert CONTRACT_DOC.is_file()
    assert REPORT_TEMPLATE.is_file()
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    assert python_files == ALLOWED_LAB_PYTHON_FILES


def test_lab9_doc_declares_static_non_runtime_observability_contract_only() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    for phrase in (
        "static offline observability and experiment-report contract only",
        "static report template only",
        "not a generated report",
        "not candidate evaluation",
        "not reliability evidence",
        "does not generate experiment reports",
        "does not persist reports",
        "does not evaluate candidates",
        "does not compare routes",
        "does not load prompts",
        "does not read live prompt-library content",
        "Critical boundary error budget: zero",
        "LAB-10 — Candidate Evaluation Harness Interface",
    ):
        assert phrase in text, phrase


def test_lab9_report_template_shape_and_required_sections() -> None:
    template = _load_json(REPORT_TEMPLATE)
    assert template["feature_id"] == FEATURE_ID
    assert template["schema_version"] == "lab-9-offline-observability-experiment-report"
    assert template["template_status"] == "static_template_only_not_generated_not_persisted_not_reliability_evidence"
    assert template["report_generation_status"] == "not_implemented_not_executed"
    assert template["report_persistence_status"] == "not_implemented_not_allowed_by_lab9"
    assert template["candidate_evaluation_status"] == "not_executed"
    assert template["critical_boundary_error_budget"] == 0
    required_sections = set(template["required_sections"])
    for section in (
        "run_identity",
        "lab_version_context",
        "corpus_context",
        "fixture_manifest_context",
        "self_validation_context",
        "candidate_metadata_context",
        "hard_gate_summary",
        "soft_metric_summary",
        "case_outcome_summary",
        "critical_boundary_incidents",
        "lab_invalid_incidents",
        "human_review_queue",
        "reproducibility_metadata",
        "limitations_and_non_claims",
        "freeze_evidence_reference",
    ):
        assert section in required_sections, section
        assert section in template["future_report_record_shape"], section


def test_lab9_template_non_authority_declarations_block_runtime_and_persistence() -> None:
    template = _load_json(REPORT_TEMPLATE)
    declarations = template["non_authority_declarations"]
    for key in (
        "candidate_evaluation_executed",
        "cases_scored",
        "route_comparison_performed",
        "route_authority_granted",
        "prompt_loading_performed",
        "live_prompt_library_read_performed",
        "live_freeze_memory_read_performed",
        "live_router_canon_read_performed",
        "runtime_router_import_performed",
        "actual_fixture_snapshot_created",
        "runner_created",
        "scoring_engine_created",
        "metrics_engine_created",
        "candidate_harness_created",
        "report_generated",
        "report_persisted",
        "ml_decision_persisted",
        "provider_call_performed",
        "embedding_call_performed",
        "network_call_performed",
        "subprocess_call_performed",
        "batch_mode_performed",
        "activation_performed",
        "field_test_performed",
        "runtime_pilot_behavior_performed",
        "copilot_behavior_performed",
    ):
        assert declarations[key] is False, key
    assert template["forbidden_authority_fields"] == FORBIDDEN_AUTHORITY_FIELDS
    assert template["reliability_claim_status"] == "blocked_by_default_until_future_governed_lab_evidence_and_human_review"


def test_lab9_template_reproducibility_and_incident_sections_are_explicit() -> None:
    template = _load_json(REPORT_TEMPLATE)
    record = template["future_report_record_shape"]
    assert record["critical_boundary_incidents"] == []
    assert record["lab_invalid_incidents"] == []
    assert record["human_review_queue"] == []
    assert record["reproducibility_metadata"]["network_allowed"] is False
    assert record["reproducibility_metadata"]["provider_calls_allowed"] is False
    assert record["reproducibility_metadata"]["embedding_calls_allowed"] is False
    assert "Template only; no report generated by LAB-9." in record["limitations_and_non_claims"]
    assert "Template only; no candidate evaluated by LAB-9." in record["limitations_and_non_claims"]
    assert "Template only; no reliability claim authorized by LAB-9." in record["limitations_and_non_claims"]


def test_lab9_manifest_metadata_declares_template_without_report_persistence_or_authority() -> None:
    data = _load_json(MANIFEST)
    assert data["ml_lab_offline_observability_report_feature_id"] == FEATURE_ID
    assert data["ml_lab_offline_observability_report_schema_version"] == "lab-9-offline-observability-experiment-report"
    assert data["ml_lab_offline_observability_report_contains_static_report_template"] is True
    assert data["ml_lab_offline_observability_report_template_sha256"] == hashlib.sha256(REPORT_TEMPLATE.read_bytes()).hexdigest()
    assert data["ml_lab_offline_observability_report_contains_generated_reports"] is False
    assert data["ml_lab_offline_observability_report_contains_report_persistence"] is False
    assert data["ml_lab_offline_observability_report_contains_candidate_evaluation"] is False
    assert data["ml_lab_offline_observability_report_contains_case_execution"] is False
    assert data["ml_lab_offline_observability_report_contains_route_comparison"] is False
    assert data["ml_lab_offline_observability_report_contains_route_authority"] is False
    assert data["ml_lab_offline_observability_report_contains_prompt_loading"] is False
    assert data["ml_lab_offline_observability_report_contains_provider_calls"] is False
    assert data["ml_lab_offline_observability_report_contains_embeddings"] is False
    assert data["ml_lab_offline_observability_report_contains_batch_mode"] is False
    assert data["ml_lab_offline_observability_report_contains_activation_key"] is False
    assert data["ml_lab_offline_observability_report_contains_field_test_mode"] is False
    assert data["ml_lab_offline_observability_report_contains_runtime_pilot"] is False
    assert data["ml_lab_offline_observability_report_contains_copilot_behavior"] is False
    assert data["ml_lab_offline_observability_report_generation_executed"] is False
    assert data["ml_lab_offline_observability_report_persistence_performed"] is False
    assert data["ml_lab_offline_observability_report_candidate_evaluation_executed"] is False
    assert data["ml_lab_offline_observability_report_critical_boundary_error_budget"] == 0
    assert "LAB-10 Candidate Evaluation Harness Interface" in data["ml_lab_offline_observability_report_next_safe_milestone"]


if __name__ == "__main__":
    test_lab9_files_exist_and_python_surface_is_unchanged()
    test_lab9_doc_declares_static_non_runtime_observability_contract_only()
    test_lab9_report_template_shape_and_required_sections()
    test_lab9_template_non_authority_declarations_block_runtime_and_persistence()
    test_lab9_template_reproducibility_and_incident_sections_are_explicit()
    test_lab9_manifest_metadata_declares_template_without_report_persistence_or_authority()
    print(
        "CONTRACT_TEST_OK: LAB-9 ML LAB Offline Observability + Experiment Report v1, "
        "immutable governed static offline observability and experiment-report contract after LAB-8 freeze with FREEZE_MEMORY_STATUS OK, "
        "adds one static report template and declares future report sections for run identity, lab version context, corpus context, fixture manifest context, self-validation context, candidate metadata, hard gates, soft metrics, case outcomes, critical-boundary incidents, LAB_INVALID incidents, human-review queue, reproducibility metadata, limitations, and freeze evidence, "
        "report generation not implemented, report persistence not implemented, candidate evaluation not executed, cases not executed or scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-10 Candidate Evaluation Harness Interface next"
    )
