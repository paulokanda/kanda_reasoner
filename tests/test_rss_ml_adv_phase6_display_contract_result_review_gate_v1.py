from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'ml_advisory_signal' / 'ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_CONTRACT_RESULT_REVIEW_GATE_V1.md'
READY = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'ml_advisory_signal' / 'ML_ADVISORY_PHASE6_GUARDED_RUNTIME_ADVISORY_DISPLAY_IMPLEMENTATION_READINESS_V1.md'
README = ROOT / 'kanda_reasoner_app' / 'routing_signal_scorer' / 'ml_advisory_signal' / 'README.md'

FEATURE_ID = 'rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_result_review_gate_v1'
REVIEWED_FEATURE_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1'
NEXT_TITLE = 'Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation v1'


def test_phase6_display_contract_review_gate_doc_exists_and_reviews_frozen_feature():
    text = DOC.read_text(encoding='utf-8')
    assert FEATURE_ID in text
    assert REVIEWED_FEATURE_TITLE in text
    assert 'Phase 6 display contract is accepted as good and safe only for continued' in text
    assert 'governed implementation' in text
    assert 'runtime display' in text
    assert 'implementation evidence' in text
    assert 'advisory panel evidence' in text
    assert 'runtime telemetry' in text
    assert 'surface evidence' in text
    assert NEXT_TITLE in text


def test_phase6_display_contract_review_gate_preserves_zero_authority_boundaries():
    text = DOC.read_text(encoding='utf-8')
    required = [
        'ML Advisory Signal remains telemetry only',
        'the governed router remains the final selector',
        'no real ML',
        'no adapter execution',
        'no candidate execution',
        'no provider calls',
        'no network calls',
        'no API keys',
        'no embeddings',
        'no prompt loading',
        'no prompt library read',
        'no freeze-memory read or write',
        'no router-canon read',
        'no runtime shadow mode',
        'no runtime display implementation',
        'no runtime advisory panel',
        'no runtime telemetry surface',
        'no runtime UI mutation',
        'no router prompt logic modification',
        'no route authority',
        'no advisory rankings',
        'no free-text advisory explanations',
        'no runtime Copilot behavior',
        'no MLRT-113',
        'critical boundary error budget zero',
        'adds 0 new real prompt-selection cases',
    ]
    for marker in required:
        assert marker in text


def test_phase6_implementation_readiness_blocks_authority_and_state_leaks():
    text = READY.read_text(encoding='utf-8')
    assert NEXT_TITLE in text
    assert 'It is not an implementation' in text
    assert 'does not authorize runtime display' in text
    assert 'route-invariant' in text
    assert 'final-selection-invisible' in text
    assert 'removable without changing router output' in text
    assert 'fail open' in text
    assert 'never show advisory rankings' in text
    assert 'never show free-text advisory explanations' in text
    assert 'never call providers' in text
    assert 'never create MLRT-113' in text
    assert 'turning the display on' in text
    assert 'identical governed router decisions' in text


def test_readme_mentions_phase6_display_contract_review_gate():
    text = README.read_text(encoding='utf-8')
    assert 'Phase 6 guarded runtime advisory display contract result review gate' in text
    assert 'does not implement runtime display' in text


if __name__ == '__main__':
    test_phase6_display_contract_review_gate_doc_exists_and_reviews_frozen_feature()
    test_phase6_display_contract_review_gate_preserves_zero_authority_boundaries()
    test_phase6_implementation_readiness_blocks_authority_and_state_leaks()
    test_readme_mentions_phase6_display_contract_review_gate()
    print('VALIDATION OK: rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_result_review_gate_v1')
