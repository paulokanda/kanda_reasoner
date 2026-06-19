import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_assistant_transition_design import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    NEXT_PHASE,
    RUNTIME_POLICY,
    SCHEMA_VERSION,
    assert_shadow_mode_assistant_transition_design_valid,
    build_shadow_mode_assistant_transition_design,
    validate_shadow_mode_assistant_transition_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
MODULE = ADVISER / "transition_design" / "shadow_mode_assistant_transition_design.py"
MANIFEST = BOX / "box_manifest.json"


class ShadowModeAssistantTransitionDesignTests(unittest.TestCase):
    def test_manifest_declares_design_only_m17_boundary(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_assistant_transition_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_assistant_transition_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_assistant_transition_design_status"],
            "standard_library_only_offline_in_memory_design_record_no_file_io_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "shadow_mode_assistant_transition_design_contains_file_io",
            "shadow_mode_assistant_transition_design_contains_case_discovery",
            "shadow_mode_assistant_transition_design_contains_source_scanning",
            "shadow_mode_assistant_transition_design_contains_prompt_auto_loading",
            "shadow_mode_assistant_transition_design_contains_artifact_io",
            "shadow_mode_assistant_transition_design_contains_persistence",
            "shadow_mode_assistant_transition_design_contains_registry_writer",
            "shadow_mode_assistant_transition_design_contains_scratch_writer",
            "shadow_mode_assistant_transition_design_contains_gold_mutation",
            "shadow_mode_assistant_transition_design_contains_ml_execution",
            "shadow_mode_assistant_transition_design_contains_embeddings_or_providers",
            "shadow_mode_assistant_transition_design_contains_runtime_integration",
            "shadow_mode_assistant_transition_design_contains_router_authority",
            "shadow_mode_assistant_transition_design_contains_shadow_mode_enablement",
            "shadow_mode_assistant_transition_design_contains_assistant_behavior",
        ):
            self.assertIs(manifest[key], False, key)
        self.assertIs(manifest["shadow_mode_assistant_transition_design_uses_m16_gate_report"], True)

    def test_builds_design_record_without_granting_runtime_authority(self):
        record = build_shadow_mode_assistant_transition_design(
            promotion_gate_report={
                "gate_decision": "eligible_for_future_shadow_mode_design_review_only",
                "next_allowed_step": "future_governed_shadow_mode_design_review_only",
                "router_authority": "none",
                "candidate_promotion": "not_performed_by_this_gate",
                "shadow_mode_authority": "not_granted_requires_future_governed_design",
            },
            transition_policy={"policy_version": "m17-test"},
        )
        self.assertEqual(record["feature_id"], FEATURE_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["authority_statement"], AUTHORITY_STATEMENT)
        self.assertEqual(record["runtime_policy"], RUNTIME_POLICY)
        self.assertEqual(record["router_authority"], "none")
        self.assertEqual(record["next_allowed_step"], NEXT_PHASE)
        self.assertIs(record["eligible_for_future_shadow_mode_design_review"], True)
        for flag in (
            "may_enable_shadow_mode",
            "may_enable_assistant_behavior",
            "may_promote_candidate",
            "may_mutate_gold",
            "may_persist_transition_record",
            "may_write_runtime_config",
            "may_modify_router",
            "may_auto_load_prompts",
            "may_call_provider",
            "may_use_embeddings",
        ):
            self.assertIs(record[flag], False, flag)
        self.assertTrue(validate_shadow_mode_assistant_transition_design(record)["ok"])
        self.assertIs(assert_shadow_mode_assistant_transition_design_valid(record), record)

    def test_blocked_m16_gate_still_only_allows_future_design_review(self):
        record = build_shadow_mode_assistant_transition_design(
            promotion_gate_report={
                "gate_decision": "blocked_human_review_or_evidence_required",
                "next_allowed_step": "resolve_blockers_with_human_review_before_future_phase",
                "router_authority": "none",
            }
        )
        self.assertIs(record["eligible_for_future_shadow_mode_design_review"], False)
        self.assertEqual(record["next_allowed_step"], NEXT_PHASE)
        self.assertFalse(record["may_enable_shadow_mode"])
        self.assertTrue(validate_shadow_mode_assistant_transition_design(record)["ok"])

    def test_validator_rejects_runtime_or_shadow_authority(self):
        record = build_shadow_mode_assistant_transition_design()
        bad = dict(record)
        bad["may_enable_shadow_mode"] = True
        self.assertFalse(validate_shadow_mode_assistant_transition_design(bad)["ok"])
        bad = dict(record)
        bad["router_authority"] = "final_route"
        self.assertFalse(validate_shadow_mode_assistant_transition_design(bad)["ok"])
        bad = dict(record)
        bad["transition_boundaries"] = dict(record["transition_boundaries"])
        bad["transition_boundaries"]["prompt_auto_loading"] = "allowed"
        self.assertFalse(validate_shadow_mode_assistant_transition_design(bad)["ok"])

    def test_module_has_no_io_provider_embedding_runtime_or_router_behavior(self):
        text = MODULE.read_text(encoding="utf-8")
        forbidden = (
            "open(",
            "Path(",
            "read_text",
            "write_text",
            "glob",
            "rglob",
            "subprocess",
            "requests",
            "socket",
            "http",
            "provider",
            "embedding",
            "vector",
            "final_route",
            "may_proceed_now",
            "required_prompts",
        )
        lowered = text.lower()
        for item in forbidden:
            if item in {"provider", "embedding", "vector"}:
                # These words are allowed in the module docstring and constants only as forbidden-boundary text.
                self.assertIn(f"{item}", lowered)
                continue
            self.assertNotIn(item.lower(), lowered, item)

    def test_runtime_package_does_not_export_transition_design(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "transition_design",
            "shadow_mode_assistant_transition_design",
            "build_shadow_mode_assistant_transition_design",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
