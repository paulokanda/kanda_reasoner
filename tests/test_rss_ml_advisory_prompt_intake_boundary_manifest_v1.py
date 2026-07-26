from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"
FEATURE_TITLE = "Routing Signal Scorer ML Advisory-Signal and Governed Prompt Intake Boundary Contract v1"
PREFIX = "ml_advisory_prompt_intake_boundary_v1"


def test_manifest_records_phase1a_boundaries() -> None:
    manifest_path = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_phase"] == "phase_1a_boundary_contract"
    assert manifest[f"{PREFIX}_mlrt_status"] == "closed_and_paused"
    assert manifest[f"{PREFIX}_mlrt_113_created"] is False
    assert manifest[f"{PREFIX}_new_real_mlrt_cases_added"] == 0
    assert manifest[f"{PREFIX}_route_authority_enabled"] is False
    assert manifest[f"{PREFIX}_real_ml_enabled"] is False
    assert manifest[f"{PREFIX}_provider_calls_enabled"] is False
    assert manifest[f"{PREFIX}_embeddings_enabled"] is False
    assert manifest[f"{PREFIX}_persistence_enabled"] is False
    assert manifest[f"{PREFIX}_router_prompt_logic_modified"] is False
    assert manifest[f"{PREFIX}_prompt_registry_mutation_enabled"] is False
    assert manifest[f"{PREFIX}_manual_code_is_authority"] is False
    assert manifest[f"{PREFIX}_prompt_intake_is_only_prompt_creation_door"] is True


if __name__ == "__main__":
    test_manifest_records_phase1a_boundaries()
    print(f"VALIDATION OK: {FEATURE_ID}")
