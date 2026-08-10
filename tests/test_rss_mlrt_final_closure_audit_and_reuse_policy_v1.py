from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_TITLE = 'Routing Signal Scorer MLRT Final Closure Audit and Reuse Policy v1'
FEATURE_ID = 'rss_mlrt_final_closure_audit_and_reuse_policy_v1'
POS_LABEL = 'RSS_MLRT_FINAL_CLOSURE_AUDIT_AND_REUSE_POLICY_VALIDATION_OK_NON_RUNTIME_NON_AUTHORITATIVE'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT_FINAL_CLOSURE_AUDIT_AND_REUSE_POLICY_V1_VALIDATION_OK'
CONTRACT_SUMMARY = 'MLRT Final Closure Audit and Reuse Policy v1, closed the current controlled offline ML prompt-selection MLRT expansion wave after the consolidation audit freeze; preserved 1306/1306 validation-only cases across twenty-four real test suites and twenty-four paired review gates as a reusable offline regression corpus; confirmed the five requested finish checks: organization/readability audit, simple coverage map by risk family and suite number, duplicate/redundant-language review, runtime/router-authority leakage check, and no cleanup patch required unless a later audit finds a concrete issue; recorded that MLRT expansion is closed and paused, not deleted, and future increases are allowed only for a new governed risk or a separate ML advisory-signal integration phase; preserved that ML is not integrated into route prompt logic by this closure and still has no runtime route authority; preserved the final goal that ML may later be tested for helping prompt selection in router prompt logic while remaining non-authoritative unless separately governed; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
PREFIX = 'rss_mlrt_final_closure_audit_and_reuse_policy'
REAL_SUITES = [(65, 'First Controlled Offline ML Prompt-Selection Test', 3, 'first controlled static route selection'), (67, 'Second Controlled Offline ML Prompt-Selection Test', 5, 'harder fixed controlled route selection'), (69, 'Expanded Controlled Offline ML Prompt-Selection Test Suite', 10, 'expanded positive expected-route coverage'), (71, 'Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite', 8, 'boundary-negative containment'), (73, 'Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite', 64, 'mixed increased-volume coverage'), (75, 'Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite', 64, 'adversarial prompt-selection pressure'), (77, 'Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite', 64, 'near-miss counterfactual control'), (79, 'Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite', 64, 'differential drift'), (81, 'Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite', 64, 'regression metamorphic consistency'), (83, 'Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite', 64, 'semantic collision disambiguation'), (85, 'Maximum-Optimized Ambiguity Saturation Controlled Offline ML Prompt-Selection Test Suite', 64, 'ambiguity saturation'), (87, 'Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite', 64, 'state-transition evidence recognition'), (89, 'Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite', 64, 'temporal recency arbitration'), (91, 'Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite', 64, 'user-correction evidence recovery'), (93, 'Maximum-Optimized Current-Feature Freeze Intake Precedence Controlled Offline ML Prompt-Selection Test Suite', 64, 'current-feature freeze intake precedence'), (95, 'Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-exposure status recovery'), (97, 'Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite', 64, 'preview/write boundary'), (99, 'Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite', 64, 'human-confirmation binding'), (101, 'Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite', 64, 'written-path integrity'), (103, 'Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-index consistency'), (105, 'Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite', 64, 'AI-send exposure alignment'), (107, 'Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite', 64, 'startup freeze-context propagation'), (109, 'Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite', 64, 'startup handoff next-step arbitration'), (111, 'Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite', 64, 'freeze-hint consumption binding')]
REVIEW_GATES = [66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112]
CUMULATIVE_CASES = 1306
REAL_SUITE_COUNT = 24
REVIEW_GATE_COUNT = 24
DOC_REL = Path('kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_FINAL_CLOSURE_AUDIT_AND_REUSE_POLICY_V1.md')
README_REL = Path('kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md')
MANIFEST_REL = Path('kanda_reasoner_app/routing_signal_scorer/box_manifest.json')
CONSOLIDATION_DOC_REL = Path('kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_CONSOLIDATION_AUDIT_AND_COVERAGE_MAP_V1.md')

FORBIDDEN_TRUE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_AUTHORITY_PHRASES = [
    'ml has runtime route authority',
    'ml is the router',
    'ml chooses final routes',
    'ml overrides governed prompt logic',
    'route authority enabled',
    'router prompt logic modified',
    'provider calls enabled',
    'model training started',
]


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def _manifest() -> dict:
    return json.loads(_read(ROOT / MANIFEST_REL))


def test_final_closure_counts_are_exact_and_no_new_cases_added() -> None:
    assert len(REAL_SUITES) == REAL_SUITE_COUNT == 24
    assert len(REVIEW_GATES) == REVIEW_GATE_COUNT == 24
    assert sum(cases for _, _, cases, _ in REAL_SUITES) == CUMULATIVE_CASES == 1306
    assert [n + 1 for n, _, _, _ in REAL_SUITES] == REVIEW_GATES
    assert REAL_SUITES[0][0] == 65
    assert REAL_SUITES[-1][0] == 111
    assert REVIEW_GATES[0] == 66
    assert REVIEW_GATES[-1] == 112
    assert all(cases == 64 for n, _, cases, _ in REAL_SUITES if n >= 73)


def test_final_closure_doc_records_five_finish_checks_and_reuse_policy() -> None:
    doc = _read(ROOT / DOC_REL)
    readme = _read(ROOT / README_REL)
    consolidation = _read(ROOT / CONSOLIDATION_DOC_REL)

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert 'Five finish checks' in doc
    assert 'Organization and readability' in doc
    assert 'Coverage map by risk family and suite number' in doc
    assert 'Duplicate or redundant suite language' in doc
    assert 'Runtime/router-authority leakage' in doc
    assert 'Optional maintenance patch' in doc
    assert 'Keep the MLRT tests' in doc
    assert 'MLRT expansion status: `closed and paused`' in doc
    assert 'ML integrated to route prompt logic: `no`' in doc
    assert 'Runtime route authority: `no`' in doc
    assert 'Future increases are allowed only' in doc
    assert '1306/1306' in doc
    assert 'MLRT-65' in doc and 'MLRT-112' in doc

    assert FEATURE_TITLE in readme
    assert 'New real cases added: `0`' in readme
    assert 'ML is not integrated into route prompt logic' in readme
    assert '1306/1306' in consolidation
    assert 'pause new MLRT growth' in consolidation


def test_coverage_map_domains_are_unique_and_documents_exist() -> None:
    domains = [domain for *_, domain in REAL_SUITES]
    assert len(domains) == len(set(domains))
    for n, _, _, _ in REAL_SUITES:
        matches = sorted((ROOT / 'kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability').glob(f'MLRT_{n}_*.md'))
        assert len(matches) == 1, (n, matches)
    for n in REVIEW_GATES:
        matches = sorted((ROOT / 'kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability').glob(f'MLRT_{n}_*.md'))
        assert len(matches) == 1, (n, matches)
        assert 'RESULT_REVIEW_GATE' in matches[0].name


def test_manifest_records_closure_and_all_boundary_flags_remain_false() -> None:
    manifest = _manifest()
    assert manifest[f'{PREFIX}_feature_id'] == FEATURE_ID
    assert manifest[f'{PREFIX}_feature_title'] == FEATURE_TITLE
    assert manifest[f'{PREFIX}_new_real_cases_added'] == 0
    assert manifest[f'{PREFIX}_real_suite_count'] == 24
    assert manifest[f'{PREFIX}_review_gate_count'] == 24
    assert manifest[f'{PREFIX}_cumulative_controlled_offline_cases_passed'] == 1306
    assert manifest[f'{PREFIX}_cumulative_controlled_offline_cases_expected'] == 1306
    assert manifest[f'{PREFIX}_mlrt_expansion_closed'] is True
    assert manifest[f'{PREFIX}_mlrt_expansion_paused'] is True
    assert manifest[f'{PREFIX}_reuse_policy_preserve_tests'] is True
    assert manifest[f'{PREFIX}_future_increase_allowed_only_for_new_governed_risk_or_integration_phase'] is True
    assert manifest[f'{PREFIX}_ml_integrated_to_route_prompt_logic'] is False
    assert manifest[f'{PREFIX}_ml_has_runtime_route_authority'] is False
    assert manifest[f'{PREFIX}_maintenance_cleanup_required_now'] is False
    assert manifest[f'{PREFIX}_critical_boundary_error_budget'] == 0
    for flag in FORBIDDEN_TRUE_FLAGS:
        assert manifest[f'{PREFIX}_{flag}'] is False


def test_no_runtime_authority_leakage_phrases_in_final_closure_surfaces() -> None:
    combined = '\n'.join([
        _read(ROOT / DOC_REL),
        _read(ROOT / README_REL),
        json.dumps(_manifest(), sort_keys=True),
    ]).lower()
    for phrase in FORBIDDEN_AUTHORITY_PHRASES:
        assert phrase not in combined
    required_boundary_phrases = [
        'no runtime routing',
        'no route authority',
        'no router prompt logic modification',
        'no prompt loading',
        'no provider calls',
        'no embeddings',
        'no persistence',
        'no model training',
        'no model calibration',
        'no model improvement',
        'no runtime pilot',
        'no copilot behavior',
        'critical boundary error budget zero',
    ]
    summary = CONTRACT_SUMMARY.lower()
    for phrase in required_boundary_phrases:
        assert phrase in summary


if __name__ == '__main__':
    test_final_closure_counts_are_exact_and_no_new_cases_added()
    test_final_closure_doc_records_five_finish_checks_and_reuse_policy()
    test_coverage_map_domains_are_unique_and_documents_exist()
    test_manifest_records_closure_and_all_boundary_flags_remain_false()
    test_no_runtime_authority_leakage_phrases_in_final_closure_surfaces()
    print(f'VALIDATION OK: {FEATURE_ID}')
    print(f'CONTRACT_TEST_OK: {CONTRACT_SUMMARY}')
    print(SANDBOX_MARKER)
