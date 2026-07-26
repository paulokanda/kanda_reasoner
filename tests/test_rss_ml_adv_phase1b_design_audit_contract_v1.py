from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE1B_NON_RUNTIME_DESIGN_AUDIT_CONTRACT_V1.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PHASE2 = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_OFFLINE_EVALUATION_READINESS_V1.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase1b_contract_records_required_design_audit_only_scope():
    doc = read(DOC)
    required = [
        "Feature ID: rss_ml_adv_phase1b_design_audit_contract_v1",
        "Phase 1b is an audit contract",
        "not a model adapter",
        "not a runtime shadow mode",
        "not a router integration",
        "not prompt selection logic",
        "Phase 1b creates no MLRT-113",
        "adds 0 new real prompt-selection cases",
    ]
    for text in required:
        assert text in doc


def test_phase1b_contract_preserves_forbidden_authority_and_capabilities():
    doc = read(DOC)
    forbidden_denials = [
        "does not add real ML",
        "does not add provider calls",
        "does not add embeddings",
        "vector stores",
        "persistence",
        "training data",
        "model training",
        "calibration",
        "model improvement",
        "prompt loading",
        "prompt registry mutation",
        "freeze-memory write",
        "router-canon direct access",
        "runtime shadow mode",
        "router prompt logic modification",
        "router final selection modification",
        "route authority",
    ]
    for text in forbidden_denials:
        assert text in doc


def test_phase1b_contract_requires_abstention_and_route_invariance():
    doc = read(DOC)
    required = [
        "Abstention is a safe outcome",
        "final governed route is identical with NullAdvisor and MockAdvisor",
        "no advisory field can change required prompts or groups",
        "disagreement between advisory signal and canon produces audit evidence only",
        "not a route change",
    ]
    for text in required:
        assert text in doc


def test_phase2_readiness_is_not_authorization():
    phase2 = read(PHASE2)
    assert "does not authorize Phase 2" in phase2
    assert "only after Phase 1b is validated, frozen, and reviewed" in phase2
    assert "final governed route must remain unchanged" in phase2
    assert "must not add real ML" in phase2


def test_readme_records_phase1b_as_non_runtime_audit():
    readme = read(README)
    assert "Phase 1b non-runtime design audit" in readme
    assert "It is not real ML integration" in readme
    assert "not a runtime shadow mode" in readme
    assert "Phase 1b result review gate" in readme
