from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_TITLE = 'Routing Signal Scorer MLRT Consolidation Audit and Coverage Map v1'
FEATURE_ID = 'rss_mlrt_consolidation_audit_and_coverage_map_v1'
POS_LABEL = 'RSS_MLRT_CONSOLIDATION_AUDIT_AND_COVERAGE_MAP_VALIDATION_OK_NON_RUNTIME_NON_AUTHORITATIVE'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT_CONSOLIDATION_AUDIT_AND_COVERAGE_MAP_V1_VALIDATION_OK'
CONTRACT_SUMMARY = 'MLRT Consolidation Audit and Coverage Map v1, consolidated the completed controlled offline ML prompt-selection validation wave after MLRT-112 freeze; recorded 1306/1306 validation-only cases across twenty-four real test suites and twenty-four paired review gates; preserved that MLRT-112 reviewed MLRT-111 as good but validation-only evidence and identified consolidation/audit rather than further real MLRT expansion as the next safe milestone; preserved the decision to pause new MLRT growth and audit organization, readability, non-duplication, maintainability, and coverage traceability before any future suite; preserved the standing rule that future real ML prompt-selection suites, if resumed later, must use the maximum optimized number of coherent non-duplicate cases; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
PREFIX = 'rss_mlrt_consolidation_audit_and_coverage_map'
REAL_SUITES = [(65, 'First Controlled Offline ML Prompt-Selection Test', 3, 'first controlled static route selection'), (67, 'Second Controlled Offline ML Prompt-Selection Test', 5, 'harder fixed controlled route selection'), (69, 'Expanded Controlled Offline ML Prompt-Selection Test Suite', 10, 'expanded positive expected-route coverage'), (71, 'Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite', 8, 'boundary-negative containment'), (73, 'Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite', 64, 'mixed increased-volume coverage'), (75, 'Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite', 64, 'adversarial prompt-selection pressure'), (77, 'Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite', 64, 'near-miss counterfactual control'), (79, 'Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite', 64, 'differential drift'), (81, 'Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite', 64, 'regression metamorphic consistency'), (83, 'Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite', 64, 'semantic collision disambiguation'), (85, 'Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite', 64, 'ambiguity saturation'), (87, 'Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite', 64, 'state-transition evidence recognition'), (89, 'Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite', 64, 'temporal recency arbitration'), (91, 'Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite', 64, 'user-correction evidence recovery'), (93, 'Maximum-Optimized Current-Feature Freeze Intake Precedence Controlled Offline ML Prompt-Selection Test Suite', 64, 'current-feature freeze intake precedence'), (95, 'Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-exposure status recovery'), (97, 'Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite', 64, 'preview/write boundary'), (99, 'Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite', 64, 'human-confirmation binding'), (101, 'Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite', 64, 'written-path integrity'), (103, 'Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-index consistency'), (105, 'Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite', 64, 'AI-send exposure alignment'), (107, 'Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite', 64, 'startup freeze-context propagation'), (109, 'Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite', 64, 'startup handoff next-step arbitration'), (111, 'Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-hint consumption binding')]
REVIEW_GATES = [66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112]
CUMULATIVE_CASES = 1306
REAL_SUITE_COUNT = 24
REVIEW_GATE_COUNT = 24
DOC_REL = Path('kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_CONSOLIDATION_AUDIT_AND_COVERAGE_MAP_V1.md')
README_REL = Path('kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md')
MANIFEST_REL = Path('kanda_reasoner_app/routing_signal_scorer/box_manifest.json')

FORBIDDEN_TRUE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def test_consolidation_map_counts_and_pairs_are_exact() -> None:
    assert len(REAL_SUITES) == REAL_SUITE_COUNT == 24
    assert len(REVIEW_GATES) == REVIEW_GATE_COUNT == 24
    assert sum(cases for _, _, cases, _ in REAL_SUITES) == CUMULATIVE_CASES == 1306
    assert [n + 1 for n, _, _, _ in REAL_SUITES] == REVIEW_GATES
    assert REAL_SUITES[0][0] == 65
    assert REAL_SUITES[-1][0] == 111
    assert REVIEW_GATES[0] == 66
    assert REVIEW_GATES[-1] == 112
    assert all(cases > 0 for _, _, cases, _ in REAL_SUITES)
    assert all(cases == 64 for n, _, cases, _ in REAL_SUITES if n >= 73)


def test_doc_readme_and_manifest_record_pause_not_expansion() -> None:
    doc = _read(ROOT / DOC_REL)
    readme = _read(ROOT / README_REL)
    manifest = json.loads(_read(ROOT / MANIFEST_REL))

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert POS_LABEL in doc
    assert 'pause new MLRT growth' in doc
    assert 'adds `0` new real prompt-selection cases' in doc
    assert '1306/1306' in doc
    assert '24' in doc
    assert 'MLRT-65' in doc
    assert 'MLRT-112' in doc
    assert 'MLRT Consolidation Audit and Coverage Map v1' in readme
    assert 'adds `0` new real cases' in readme

    assert manifest[f'{PREFIX}_feature_id'] == FEATURE_ID
    assert manifest[f'{PREFIX}_feature_title'] == FEATURE_TITLE
    assert manifest[f'{PREFIX}_new_real_cases_added'] == 0
    assert manifest[f'{PREFIX}_real_suite_count'] == 24
    assert manifest[f'{PREFIX}_review_gate_count'] == 24
    assert manifest[f'{PREFIX}_cumulative_controlled_offline_cases_passed'] == 1306
    assert manifest[f'{PREFIX}_cumulative_controlled_offline_cases_expected'] == 1306
    assert manifest[f'{PREFIX}_mlrt_expansion_paused'] is True
    assert manifest[f'{PREFIX}_consolidation_audit_recommended'] is True
    assert manifest[f'{PREFIX}_future_real_suite_maximum_optimized_policy_preserved'] is True
    assert manifest[f'{PREFIX}_ml_signal_ready_for_runtime'] is False
    assert manifest[f'{PREFIX}_ml_signal_ready_for_route_authority'] is False
    assert manifest[f'{PREFIX}_ml_signal_ready_for_training'] is False
    assert manifest[f'{PREFIX}_critical_boundary_error_budget'] == 0

    for flag in FORBIDDEN_TRUE_FLAGS:
        assert manifest[f'{PREFIX}_{flag}'] is False


def test_every_mapped_suite_and_review_gate_document_exists() -> None:
    manifest = json.loads(_read(ROOT / MANIFEST_REL))
    real_docs = manifest[f'{PREFIX}_real_suite_documents']
    gate_docs = manifest[f'{PREFIX}_review_gate_documents']
    assert len(real_docs) == 24
    assert len(gate_docs) == 24
    for n, _, _, _ in REAL_SUITES:
        path = ROOT / real_docs[f'mlrt_{n}_document']
        assert path.exists(), path
        assert f'MLRT_{n}_' in path.name
    for n in REVIEW_GATES:
        path = ROOT / gate_docs[f'mlrt_{n}_review_gate_document']
        assert path.exists(), path
        assert f'MLRT_{n}_' in path.name
        assert 'RESULT_REVIEW_GATE' in path.name


def test_contract_preserves_non_runtime_non_authoritative_boundary() -> None:
    summary = CONTRACT_SUMMARY
    required = [
        'no runtime routing',
        'no route authority',
        'no router prompt logic modification',
        'no prompt loading',
        'no provider calls',
        'no embeddings',
        'no persistence',
        'no training-data intake',
        'no dataset creation',
        'no model training',
        'no model calibration',
        'no model improvement',
        'no gold registry write',
        'no registry mutation',
        'no runtime Pilot',
        'no Copilot behavior',
        'critical boundary error budget zero',
    ]
    for phrase in required:
        assert phrase in summary
    assert 'validation-only' in summary
    assert 'pause new MLRT growth' in summary


if __name__ == '__main__':
    test_consolidation_map_counts_and_pairs_are_exact()
    test_doc_readme_and_manifest_record_pause_not_expansion()
    test_every_mapped_suite_and_review_gate_document_exists()
    test_contract_preserves_non_runtime_non_authoritative_boundary()
    print(f'VALIDATION OK: {FEATURE_ID}')
    print(f'CONTRACT_TEST_OK: {CONTRACT_SUMMARY}')
    print(SANDBOX_MARKER)
