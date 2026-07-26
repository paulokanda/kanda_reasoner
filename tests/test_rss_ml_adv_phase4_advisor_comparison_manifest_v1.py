from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
ML_DIR = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal"


def test_phase4_comparison_manifest_and_docs_preserve_boundaries() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["ml_advisory_phase4_advisor_comparison_feature_id"] == (
        "rss_ml_adv_phase4_offline_advisor_comparison_contract_v1"
    )
    assert manifest["ml_advisory_phase4_advisor_comparison_real_ml_enabled"] is False
    assert manifest["ml_advisory_phase4_advisor_comparison_runtime_enabled"] is False
    assert manifest["ml_advisory_phase4_advisor_comparison_route_authority_enabled"] is False
    assert manifest["ml_advisory_phase4_advisor_comparison_router_prompt_logic_modified"] is False
    assert manifest["ml_advisory_phase4_advisor_comparison_mlrt113_created"] is False

    contract_doc = ML_DIR / "ML_ADVISORY_PHASE4_OFFLINE_ADVISOR_COMPARISON_CONTRACT_V1.md"
    boundary_doc = ML_DIR / "ML_ADVISORY_PHASE4_OFFLINE_ADVISOR_COMPARISON_BOUNDARY_MODEL_V1.md"
    readiness_doc = ML_DIR / "ML_ADVISORY_PHASE4_RESULT_REVIEW_READINESS_V1.md"
    for path in (contract_doc, boundary_doc, readiness_doc):
        text = path.read_text(encoding="utf-8")
        assert "No real ML" in text or "not runtime ML" in text or "not add real ML" in text
        assert "No route authority" in text or "no route authority" in text
        assert "No MLRT-113" in text or "no MLRT-113" in text


if __name__ == "__main__":
    test_phase4_comparison_manifest_and_docs_preserve_boundaries()
