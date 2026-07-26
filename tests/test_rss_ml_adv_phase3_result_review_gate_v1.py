from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE3_OFFLINE_FIXTURE_CATALOG_RESULT_REVIEW_GATE_V1.md"
READINESS = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE4_OFFLINE_ADVISOR_COMPARISON_CONTRACT_READINESS_V1.md"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    require(DOC.exists(), "Phase 3 result review gate doc is missing")
    require(READINESS.exists(), "Phase 4 readiness doc is missing")

    doc = DOC.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")

    require("Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Result Review Gate v1" in doc, "feature title missing")
    require("Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1" in doc, "reviewed feature title missing")
    require("Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1" in doc, "next safe feature title missing")
    require("synthetic fixture catalog" in doc, "synthetic fixture catalog acceptance missing")
    require("not prompt-selection correctness evidence" in doc, "prompt-selection correctness denial missing")
    require("ML Advisory Signal remains telemetry only" in doc, "telemetry-only invariant missing")
    require("the governed router remains the final selector" in doc, "router final selector invariant missing")
    require("critical boundary error budget zero" in doc, "zero boundary budget missing")
    require("adds 0 new real prompt-selection cases" in doc, "zero real prompt-selection accounting missing")
    require("It creates no MLRT-113" in doc, "MLRT-113 denial missing")

    forbidden_phrases = [
        "no real ML",
        "no provider calls",
        "no embeddings",
        "no vector store",
        "no persistence",
        "no report persistence",
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
        "no runtime Pilot behavior",
        "no runtime Copilot behavior",
        "no MLRT-113",
    ]
    for phrase in forbidden_phrases:
        require(phrase in doc, f"forbidden-scope phrase missing: {phrase}")

    require("Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1" in readiness, "Phase 4 readiness next title missing")
    require("Patch install delivery guard remains active" in readiness, "delivery guard precondition missing")
    require("MLRT remains closed and paused" in readiness, "MLRT closed invariant missing")
    require("NullAdvisor and MockAdvisor-style" in readiness, "offline comparison scope missing")
    require("It may not persist reports" in readiness, "report persistence denial missing")

    print("VALIDATION OK: rss_ml_adv_phase3_fixture_catalog_result_review_gate_v1")


if __name__ == "__main__":
    main()
