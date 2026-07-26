from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ML_DIR = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'ml_advisory_signal'
DOC = ML_DIR / 'ML_ADVISORY_PHASE4_OFFLINE_ADVISOR_COMPARISON_RESULT_REVIEW_GATE_V1.md'
READY = ML_DIR / 'ML_ADVISORY_PHASE5_OFFLINE_REAL_ADAPTER_BOUNDARY_CONTRACT_READINESS_V1.md'
README = ML_DIR / 'README.md'

FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Result Review Gate v1'
FEATURE_ID = 'rss_ml_adv_phase4_advisor_comparison_result_review_gate_v1'
REVIEWED_FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1'
NEXT_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Contract v1'


def test_phase4_review_gate_doc_exists_and_reviews_frozen_feature():
    text = DOC.read_text(encoding='utf-8')
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert REVIEWED_FEATURE_TITLE in text
    assert 'accepted as good and safe only for continued governed' in text
    assert 'offline, in-memory passive' in text and 'comparison' in text
    assert 'not runtime ML evidence' in text
    assert 'not route-authority evidence' in text
    assert NEXT_TITLE in text


def test_phase4_review_gate_preserves_zero_authority_boundaries():
    text = DOC.read_text(encoding='utf-8')
    required = [
        'ML Advisory Signal remains telemetry only',
        'the governed router remains the final selector',
        'no real ML',
        'no provider calls',
        'no embeddings',
        'no prompt library read',
        'no freeze-memory read or write',
        'no router-canon read',
        'no runtime shadow mode',
        'no router prompt logic modification',
        'no route authority',
        'no advisory rankings',
        'no free-text advisory explanations',
        'no MLRT-113',
        'critical boundary error budget zero',
        'adds 0 new real prompt-selection cases',
    ]
    for marker in required:
        assert marker in text


def test_phase5_readiness_blocks_real_adapter_authority_leaks():
    text = READY.read_text(encoding='utf-8')
    assert NEXT_TITLE in text
    assert 'does not implement Phase 5' in text
    assert 'provider calls' in text
    assert 'embeddings' in text
    assert 'prompt-library reads' in text
    assert 'freeze-memory reads' in text
    assert 'router-canon reads' in text
    assert 'route authority' in text
    assert 'router' in text and 'prompt logic modification' in text
    assert 'must fail' in text


def test_readme_mentions_phase4_review_gate():
    text = README.read_text(encoding='utf-8')
    assert 'Phase 4 offline advisor comparison result review gate' in text
    assert 'does not authorize real ML' in text


if __name__ == '__main__':
    test_phase4_review_gate_doc_exists_and_reviews_frozen_feature()
    test_phase4_review_gate_preserves_zero_authority_boundaries()
    test_phase5_readiness_blocks_real_adapter_authority_leaks()
    test_readme_mentions_phase4_review_gate()
    print('VALIDATION OK: rss_ml_adv_phase4_advisor_comparison_result_review_gate_v1')
