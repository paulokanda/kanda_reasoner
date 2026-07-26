from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE1B_RESULT_REVIEW_GATE_V1.md"
READINESS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_OFFLINE_EVALUATION_HARNESS_CONTRACT_READINESS_V1.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase1b_review_gate_records_review_result_and_scope():
    doc = read(DOC)
    required = [
        "Feature ID: rss_ml_adv_phase1b_design_audit_result_review_gate_v1",
        "Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Contract v1",
        "accepted as good and safe only for continued governed implementation",
        "not production-readiness evidence",
        "not runtime ML evidence",
        "not route-authority evidence",
        "adds 0 new real prompt-selection cases",
        "creates no MLRT-113",
        "does not reopen MLRT",
    ]
    for text in required:
        assert text in doc


def test_phase1b_review_gate_preserves_all_runtime_and_authority_denials():
    doc = read(DOC)
    denied = [
        "no real ML",
        "no provider calls",
        "no embeddings",
        "no vector store",
        "no persistence",
        "no prompt loading",
        "no prompt registry mutation",
        "no prompt library read",
        "no freeze-memory read or write",
        "no router-canon read",
        "no runtime shadow mode",
        "no router prompt logic modification",
        "no router final selection modification",
        "no route authority",
        "no advisory rankings",
        "no free-text advisory explanations",
        "no training",
        "no calibration",
        "no model improvement",
        "critical boundary error budget zero",
    ]
    for text in denied:
        assert text in doc


def test_phase2_readiness_does_not_implement_or_authorize_phase2():
    readiness = read(READINESS)
    assert "does not implement Phase 2" in readiness
    assert "Future Phase 2 may only create an offline, in-memory" in readiness
    assert "Final governed route selection must remain unchanged" in readiness
    assert "must not add real ML" in readiness
    assert "runtime shadow mode" in readiness


def test_readme_records_phase1b_review_gate_as_not_phase2():
    readme = read(README)
    assert "Phase 1b result review gate" in readme
    assert "It is not Phase 2" in readme
    assert "not real ML" in readme
    assert "does not authorize provider" in readme
