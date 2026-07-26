from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE2_OFFLINE_EVALUATION_HARNESS_RESULT_REVIEW_GATE_V1.md"
READINESS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE3_OFFLINE_FIXTURE_CATALOG_CONTRACT_READINESS_V1.md"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    require(DOC.exists(), "missing Phase 2 result review gate doc")
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Feature ID: rss_ml_adv_phase2_offline_harness_result_review_gate_v1",
        "Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1",
        "offline, in-memory harness",
        "not production-readiness evidence",
        "not runtime ML evidence",
        "not route-authority evidence",
        "not router prompt logic integration evidence",
        "adds 0 new real prompt-selection cases",
        "creates no MLRT-113",
        "does not integrate ML into router prompt logic",
        "critical boundary error budget zero",
        "Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1",
    ]
    for item in required:
        require(item in text, "Phase 2 result review doc missing: " + item)

    forbidden_pairs = [
        "real ML enabled",
        "provider calls enabled",
        "route authority enabled",
        "runtime shadow mode enabled",
        "router prompt logic modification enabled",
    ]
    lower = text.lower()
    for item in forbidden_pairs:
        require(item not in lower, "Phase 2 result review doc contains unsafe phrase: " + item)

    require(READINESS.exists(), "missing Phase 3 readiness doc")
    readiness = READINESS.read_text(encoding="utf-8")
    for item in [
        "does not implement Phase 3",
        "caller-supplied, in-memory",
        "not a prompt library reader",
        "not freeze-memory reader",
        "not router-canon reader",
        "runtime shadow mode",
        "MLRT-113",
        "Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1",
    ]:
        require(item in readiness, "Phase 3 readiness doc missing: " + item)

    print("VALIDATION OK: rss_ml_adv_phase2_result_review_gate_doc_v1")


if __name__ == "__main__":
    main()
