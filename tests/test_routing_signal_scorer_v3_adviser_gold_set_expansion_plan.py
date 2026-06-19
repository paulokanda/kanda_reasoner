import copy
import inspect
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.gold_expansion.gold_set_expansion_plan import (
    FEATURE_ID,
    SCHEMA_VERSION,
    assert_gold_set_expansion_plan_valid,
    build_gold_set_expansion_plan,
    validate_gold_set_expansion_plan,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_CONTRACT = BOX / "contract.py"
RUNTIME_INIT = BOX / "__init__.py"
MODULE = ADVISER / "gold_expansion" / "gold_set_expansion_plan.py"
README = ADVISER / "gold_expansion" / "README.md"


class AdviserGoldSetExpansionPlanV1Tests(unittest.TestCase):
    def _gold_summary(self):
        return {
            "gold_set_version": "seed_gold_set_v1",
            "current_case_count": 50,
            "family_counts": {
                "adversarial_bypass": 8,
                "freeze_workflow": 5,
                "out_of_scope": 5,
            },
        }

    def _evaluation_report(self):
        return {
            "feature_id": "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1",
            "aggregate": {
                "total_cases": 50,
                "exact_matches": 35,
                "mismatches": 15,
                "guard_failures": 0,
                "resource_failures": 0,
                "critical_failures": 0,
                "promotion_recommendation": "blocked_review_required",
            },
        }

    def _review_queue(self):
        return {
            "feature_id": "routing_signal_scorer_v3_adviser_active_review_queue_v1",
            "aggregate": {
                "queued_review_items": 15,
                "p0_items": 0,
                "p1_items": 4,
                "queue_recommendation": "human_review_required",
            },
        }

    def _registry_record(self):
        return {
            "feature_id": "routing_signal_scorer_v3_adviser_candidate_registry_v1",
            "candidate_id": "candidate-v0-offline-lexical",
            "candidate_version": "v1",
            "promotion_blocked": True,
            "promotion_blockers": ["m16_promotion_gate_not_yet_run", "human_review_queue_not_empty"],
        }

    def test_builds_valid_in_memory_plan_without_gold_mutation(self):
        plan = build_gold_set_expansion_plan(
            current_gold_summary=self._gold_summary(),
            evaluation_report=self._evaluation_report(),
            review_queue=self._review_queue(),
            registry_record=self._registry_record(),
        )
        self.assertEqual(plan["feature_id"], FEATURE_ID)
        self.assertEqual(plan["schema_version"], SCHEMA_VERSION)
        self.assertEqual(plan["authority_statement"], "advisory_only")
        self.assertEqual(plan["plan_kind"], "in_memory_gold_set_expansion_plan_only")
        self.assertEqual(plan["router_authority"], "none")
        self.assertIs(plan["may_add_gold_cases"], False)
        self.assertIs(plan["may_mutate_gold"], False)
        self.assertIs(plan["may_promote_candidate"], False)
        self.assertIs(plan["may_persist_plan"], False)
        self.assertIs(plan["promotion_blocked"], True)
        self.assertIn("future_governed_gold_patch_required", plan["promotion_blockers"])
        self.assertIn("m16_promotion_gate_not_yet_run", plan["promotion_blockers"])
        self.assertTrue(plan["plan_items"])
        self.assertGreaterEqual(plan["expansion_targets"]["planned_new_case_count"], 50)
        self.assertIs(plan["expansion_targets"]["requires_separate_reviewed_gold_patch"], True)
        assert_gold_set_expansion_plan_valid(plan)

    def test_every_item_is_planned_only_and_future_review_required(self):
        plan = build_gold_set_expansion_plan(current_gold_summary=self._gold_summary())
        for item in plan["plan_items"]:
            self.assertEqual(item["review_status"], "planned_requires_human_review")
            self.assertIs(item["may_create_gold_case_now"], False)
            self.assertIs(item["may_mutate_gold_now"], False)
            self.assertIs(item["requires_future_governed_patch"], True)
            self.assertEqual(item["future_case_source"], "future_human_reviewed_records_only")

    def test_policy_can_limit_target_families_without_discovering_cases(self):
        plan = build_gold_set_expansion_plan(
            current_gold_summary=self._gold_summary(),
            expansion_policy={"target_families": ["freeze_workflow", "box_boundary"], "target_new_cases_per_family": 3},
        )
        self.assertEqual(plan["expansion_targets"]["target_families"], ["freeze_workflow", "box_boundary"])
        self.assertEqual(plan["expansion_targets"]["planned_new_case_count"], 6)
        self.assertEqual([item["family"] for item in plan["plan_items"]], ["freeze_workflow", "box_boundary"])

    def test_rejects_invalid_plan_hash_or_authority(self):
        plan = build_gold_set_expansion_plan(current_gold_summary=self._gold_summary())
        tampered = dict(plan)
        tampered["router_authority"] = "final_route"
        result = validate_gold_set_expansion_plan(tampered)
        self.assertFalse(result["ok"])
        self.assertIn("router_authority must be none", result["errors"])
        tampered_hash = dict(plan)
        tampered_hash["plan_hash"] = "bad"
        self.assertFalse(validate_gold_set_expansion_plan(tampered_hash)["ok"])

    def test_does_not_mutate_inputs(self):
        gold = self._gold_summary()
        evaluation = self._evaluation_report()
        queue = self._review_queue()
        registry = self._registry_record()
        before = copy.deepcopy([gold, evaluation, queue, registry])
        build_gold_set_expansion_plan(
            current_gold_summary=gold,
            evaluation_report=evaluation,
            review_queue=queue,
            registry_record=registry,
        )
        self.assertEqual(before, [gold, evaluation, queue, registry])

    def test_module_source_has_no_file_io_or_runtime_authority_terms(self):
        source = inspect.getsource(build_gold_set_expansion_plan)
        for forbidden in ("open(", "read_text", "write_text", "Path(", "glob(", "router_authority_change"):
            self.assertNotIn(forbidden, source)

    def test_runtime_contract_and_init_do_not_export_or_import_gold_expansion(self):
        for path in (RUNTIME_CONTRACT, RUNTIME_INIT):
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "adviser_offline.gold_expansion.gold_set_expansion_plan",
                "build_gold_set_expansion_plan",
                "routing_signal_scorer_v3_adviser_gold_set_expansion_plan_v1",
            ):
                self.assertNotIn(forbidden, text)

    def test_manifest_declares_m15_without_gold_mutation_or_persistence(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_gold_set_expansion_plan_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_gold_set_expansion_plan_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_gold_set_expansion_plan_status"],
            "standard_library_only_offline_in_memory_gold_expansion_plan_no_file_io_no_gold_mutation_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "adviser_gold_set_expansion_plan_contains_file_io",
            "adviser_gold_set_expansion_plan_contains_case_discovery",
            "adviser_gold_set_expansion_plan_contains_source_scanning",
            "adviser_gold_set_expansion_plan_contains_prompt_auto_loading",
            "adviser_gold_set_expansion_plan_contains_artifact_io",
            "adviser_gold_set_expansion_plan_contains_plan_persistence",
            "adviser_gold_set_expansion_plan_contains_registry_writer",
            "adviser_gold_set_expansion_plan_contains_candidate_output_persistence",
            "adviser_gold_set_expansion_plan_contains_scratch_writer",
            "adviser_gold_set_expansion_plan_contains_gold_mutation",
            "adviser_gold_set_expansion_plan_contains_ml_execution",
            "adviser_gold_set_expansion_plan_contains_embeddings_or_providers",
            "adviser_gold_set_expansion_plan_contains_runtime_integration",
            "adviser_gold_set_expansion_plan_contains_router_authority",
        ):
            self.assertIs(manifest[key], False, key)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_gold_set_expansion_plan_v1",
            "adviser_gold_expansion_plan_in_memory_only",
            "adviser_gold_expansion_plan_no_gold_mutation",
            "adviser_gold_expansion_plan_no_plan_persistence",
            "adviser_gold_expansion_plan_future_governed_patch_required",
            "adviser_gold_expansion_plan_promotion_blocked_until_m16_gate",
            "adviser_gold_expansion_plan_no_router_authority",
        ):
            self.assertIn(expected, chars)

    def test_readme_says_no_gold_cases_are_added(self):
        text = README.read_text(encoding="utf-8")
        for phrase in (
            "does **not** add gold cases",
            "no gold mutation",
            "no automatic approvals",
            "no runtime router authority",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
