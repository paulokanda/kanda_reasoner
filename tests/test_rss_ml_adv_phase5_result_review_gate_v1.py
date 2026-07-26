from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ML_DIR = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'ml_advisory_signal'
DOC = ML_DIR / 'ML_ADVISORY_PHASE5_OFFLINE_REAL_ADAPTER_BOUNDARY_RESULT_REVIEW_GATE_V1.md'
READY = ML_DIR / 'ML_ADVISORY_PHASE5_OFFLINE_REAL_ADAPTER_CANDIDATE_CONTRACT_READINESS_V1.md'
README = ML_DIR / 'README.md'

FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Result Review Gate v1'
FEATURE_ID = 'rss_ml_adv_phase5_real_adapter_boundary_result_review_gate_v1'
REVIEWED_FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Contract v1'
NEXT_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Contract v1'


def test_phase5_review_gate_doc_exists_and_reviews_frozen_feature():
    text = DOC.read_text(encoding='utf-8')
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert REVIEWED_FEATURE_TITLE in text
    assert 'accepted as good and safe only for continued governed' in text
    assert 'descriptor-only real-adapter' in text
    assert 'not adapter execution evidence' in text
    assert 'not runtime ML evidence' in text
    assert 'not route-authority evidence' in text
    assert NEXT_TITLE in text


def test_phase5_review_gate_preserves_zero_authority_boundaries():
    text = DOC.read_text(encoding='utf-8')
    required = [
        'ML Advisory Signal remains telemetry only',
        'the governed router remains the final selector',
        'no real ML',
        'no adapter execution',
        'no provider calls',
        'no network calls',
        'no API keys',
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


def test_phase5_candidate_readiness_blocks_runtime_and_provider_leaks():
    text = READY.read_text(encoding='utf-8')
    assert NEXT_TITLE in text
    assert 'does not implement an adapter candidate' in text
    assert 'does not authorize runtime ML' in text
    assert 'provider calls' in text
    assert 'network access' in text
    assert 'credentials' in text
    assert 'embeddings' in text
    assert 'persistence' in text
    assert 'route authority' in text
    assert 'router prompt logic modification' in text
    assert 'must fail' in text


def test_readme_mentions_phase5_review_gate():
    text = README.read_text(encoding='utf-8')
    assert 'Phase 5 offline real-adapter boundary result review gate' in text
    assert 'does not authorize adapter execution' in text


if __name__ == '__main__':
    test_phase5_review_gate_doc_exists_and_reviews_frozen_feature()
    test_phase5_review_gate_preserves_zero_authority_boundaries()
    test_phase5_candidate_readiness_blocks_runtime_and_provider_leaks()
    test_readme_mentions_phase5_review_gate()
    print('VALIDATION OK: rss_ml_adv_phase5_real_adapter_boundary_result_review_gate_v1')
