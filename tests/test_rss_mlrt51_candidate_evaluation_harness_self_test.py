from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_51_CANDIDATE_EVALUATION_HARNESS_SELF_TEST.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
FEATURE_ID = "rss_mlrt51_candidate_evaluation_harness_self_test_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-52 Lab Reliability Test Against Fixed Cases v1"
POS_LABEL = "RSS_MLRT51_CANDIDATE_EVALUATION_HARNESS_SELF_TEST_PASSED_NON_EVALUATING"
PREFIX = "rss_mlrt51_candidate_evaluation_harness_self_test"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_snapshot() -> list[str]:
    ignored_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in ignored_parts for part in p.parts)
    )


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    import sys
    before = file_snapshot()
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    after = file_snapshot()
    assert before == after
    return module


def load_mlrt_stub():
    return load_module(SOURCE, "mlrt51_stub_under_self_test")


def load_lab_harness():
    return load_module(LAB_HARNESS, "mlrt51_lab_harness_under_self_test")


def build_safe_envelope(module):
    return module.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="mlrt51-safe-self-test",
        candidate_id="candidate-placeholder",
        candidate_version="0.0.0-non-runtime",
        candidate_output_reference="in-memory-placeholder-only",
        candidate_output_metadata={
            "output_kind": "non_authoritative_evaluation_record",
            "candidate_claim": "placeholder only",
        },
        test_case_reference="fixed-case-placeholder-no-execution",
        corpus_version="static-placeholder-corpus",
        fixture_manifest_hash="0" * 64,
        self_validation_status="caller_supplied_pass_reference_only",
    )


def build_rejected_envelope(module):
    return module.build_not_evaluated_candidate_harness_envelope(
        lab_run_id="mlrt51-rejected-self-test",
        candidate_id="candidate-placeholder",
        candidate_version="0.0.0-non-runtime",
        candidate_output_reference="in-memory-placeholder-only",
        candidate_output_metadata={
            "output_kind": "non_authoritative_evaluation_record",
            "route_decision": "FORBIDDEN_AUTHORITY_FIELD",
            "call_provider": True,
        },
        test_case_reference="fixed-case-placeholder-no-execution",
        corpus_version="static-placeholder-corpus",
        fixture_manifest_hash="1" * 64,
        self_validation_status="caller_supplied_pass_reference_only",
    )


def assert_envelope_has_no_runtime_effects(envelope) -> None:
    assert envelope.non_authoritative is True
    assert envelope.candidate_evaluation_executed is False
    assert envelope.candidate_evaluation_allowed_by_this_interface is False
    assert envelope.case_execution_performed is False
    assert envelope.case_scoring_performed is False
    assert envelope.route_comparison_performed is False
    assert envelope.route_authority_granted is False
    assert envelope.prompt_loading_performed is False
    assert envelope.provider_call_performed is False
    assert envelope.embedding_call_performed is False
    assert envelope.persistence_performed is False
    assert envelope.report_generated is False
    assert envelope.report_persisted is False
    assert envelope.activation_performed is False
    assert envelope.field_test_performed is False
    assert envelope.runtime_pilot_behavior_performed is False
    assert envelope.copilot_behavior_performed is False


def test_mlrt51_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()


def test_mlrt51_documents_self_test_only() -> None:
    text = read(DOC)
    required = [
        "self-tests the existing LAB candidate evaluation harness interface",
        "safe_metadata_case -> NOT_EVALUATED",
        "forbidden_authority_metadata_case -> HARNESS_INTERFACE_REJECTED",
        "does **not** execute a candidate",
        "does **not** run a dry run",
        "does **not** score cases",
        "does **not** compare routes",
        "does **not** validate candidate reliability",
        "does **not** start Item 5 training/learning governance",
        "The critical boundary error budget remains `0`",
        SOURCE_REL,
        LAB_HARNESS_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt51_only_one_mlrt_python_source_file_exists() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]


def test_mlrt51_stub_boundary_still_static_and_false() -> None:
    module = load_mlrt_stub()
    before = file_snapshot()
    contract = dict(module.get_stub_contract())
    assert module.assert_static_non_runtime_boundary() is True
    after = file_snapshot()
    assert before == after
    assert contract["critical_boundary_error_budget"] == 0
    forbidden_flags = [
        "runtime_route_authority_enabled",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "batch_mode_enabled",
        "activation_enabled",
        "field_testing_enabled",
        "dry_run_execution_enabled",
        "candidate_execution_enabled",
        "case_scoring_enabled",
        "report_generation_enabled",
        "reliability_claim_enabled",
        "training_data_use_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in forbidden_flags:
        assert contract[flag] is False


def test_mlrt51_lab_harness_builds_safe_not_evaluated_envelope_without_effects() -> None:
    module = load_lab_harness()
    before = file_snapshot()
    record = module.get_lab10_candidate_harness_interface_record()
    envelope = build_safe_envelope(module)
    mapping = module.as_read_only_mapping(envelope)
    after = file_snapshot()
    assert before == after
    assert record.critical_boundary_error_budget == 0
    assert record.design_kind == "non_runtime_candidate_evaluation_harness_interface_only"
    assert envelope.outcome == module.OUTCOME_NOT_EVALUATED
    assert envelope.forbidden_authority_fields_present == ()
    assert mapping["outcome"] == module.OUTCOME_NOT_EVALUATED
    assert_envelope_has_no_runtime_effects(envelope)


def test_mlrt51_lab_harness_rejects_forbidden_authority_metadata_without_execution() -> None:
    module = load_lab_harness()
    before = file_snapshot()
    envelope = build_rejected_envelope(module)
    mapping = module.as_read_only_mapping(envelope)
    after = file_snapshot()
    assert before == after
    assert envelope.outcome == module.OUTCOME_INTERFACE_REJECTED
    assert envelope.forbidden_authority_fields_present == ("route_decision", "call_provider")
    assert mapping["outcome"] == module.OUTCOME_INTERFACE_REJECTED
    assert_envelope_has_no_runtime_effects(envelope)


def test_mlrt51_no_dry_run_candidate_training_or_item5_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "candidate execution is enabled",
        "case scoring is enabled",
        "route authority is granted",
        "Item 5 has started",
        "reliability is validated",
        "training is started",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not modify the MLRT source file",
        "must not claim validated candidate reliability",
        "does **not** execute a candidate",
        "does **not** start Item 5 training/learning governance",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt51_manifest_records_self_test_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        "candidate_evaluation_harness_self_test",
        "safe_not_evaluated_envelope_built",
        "forbidden_authority_rejected_envelope_built",
        "candidate_evaluation_executed",
        "dry_run_executed",
        "item5_training_governance_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_self_test_executed": true' in manifest
    assert f'"{PREFIX}_safe_not_evaluated_envelope_built": true' in manifest
    assert f'"{PREFIX}_forbidden_authority_rejected_envelope_built": true' in manifest
    assert f'"{PREFIX}_candidate_evaluation_executed": false' in manifest
    assert f'"{PREFIX}_dry_run_executed": false' in manifest
    assert f'"{PREFIX}_case_scoring_started": false' in manifest
    assert f'"{PREFIX}_route_authority_granted": false' in manifest
    assert f'"{PREFIX}_item5_training_governance_started": false' in manifest


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt51_readme_references_self_test_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert LAB_HARNESS_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "candidate evaluation harness self-test" in readme
    assert "Item 5 remains blocked" in readme


if __name__ == "__main__":
    test_mlrt51_files_exist()
    test_mlrt51_documents_self_test_only()
    test_mlrt51_only_one_mlrt_python_source_file_exists()
    test_mlrt51_stub_boundary_still_static_and_false()
    test_mlrt51_lab_harness_builds_safe_not_evaluated_envelope_without_effects()
    test_mlrt51_lab_harness_rejects_forbidden_authority_metadata_without_execution()
    test_mlrt51_no_dry_run_candidate_training_or_item5_claims()
    test_mlrt51_manifest_records_self_test_without_unlocking_runtime()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt51_readme_references_self_test_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-51 Candidate Evaluation Harness Self-Test v1, "
        "self-tested the existing non-runtime LAB candidate evaluation harness interface with safe and forbidden-authority in-memory metadata envelopes only; "
        "no source modification, no dry run, no candidate execution, no case execution, no case scoring, no route comparison, no route authority, "
        "no prompt loading, no provider calls, no embeddings, no persistence, no training-data use, no Item 5 start, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT51_CANDIDATE_EVALUATION_HARNESS_SELF_TEST_V1_VALIDATION_OK")
