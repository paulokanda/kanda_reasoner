import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.gold_expansion.gold_set_expansion_plan import (
    build_gold_set_expansion_plan,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.promotion_gate.promotion_criteria_gate import (
    BLOCKED,
    ELIGIBLE_REVIEW_ONLY,
    FEATURE_ID,
    SCHEMA_VERSION,
    assert_promotion_criteria_gate_report_valid,
    build_promotion_criteria_gate_report,
    validate_promotion_criteria_gate_report,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.candidate_registry import (
    AUTHORITY_STATEMENT,
    build_candidate_registry_record,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MODULE = BOX / "adviser_offline" / "promotion_gate" / "promotion_criteria_gate.py"
README = BOX / "adviser_offline" / "promotion_gate" / "README.md"
MANIFEST = BOX / "box_manifest.json"

ZERO_HASH = "0" * 64


def clean_evaluation_report():
    return {
        "feature_id": "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1",
        "run_id": "eval-clean-not-persisted",
        "aggregate": {
            "total_cases": 50,
            "exact_matches": 50,
            "mismatches": 0,
            "guard_failures": 0,
            "resource_failures": 0,
            "critical_failures": 0,
            "promotion_recommendation": "review_gate_possible",
        },
        "case_results": [{"case_id": f"case-{i:02d}"} for i in range(50)],
    }


def empty_review_queue():
    return {
        "feature_id": "routing_signal_scorer_v3_adviser_active_review_queue_v1",
        "queue_id": "queue-clean-not-persisted",
        "aggregate": {
            "queued_review_items": 0,
            "p0_items": 0,
            "p1_items": 0,
            "queue_recommendation": "no_active_review_items",
        },
        "queue_items": [],
    }


def candidate_metadata():
    return {
        "candidate_id": "candidate-v0-offline-lexical",
        "candidate_version": "v1",
        "candidate_feature_id": "routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1",
        "candidate_module_path": "kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/offline_lexical_scorer.py",
        "candidate_code_hash": ZERO_HASH,
        "candidate_contract_schema_version": "3.52-adviser-candidate-v0-offline-lexical-scorer",
        "gold_set_version": "seed_gold_set_v1",
    }


def registry_record(evaluation=None, queue=None):
    return build_candidate_registry_record(
        candidate_metadata=candidate_metadata(),
        evaluation_report=evaluation or clean_evaluation_report(),
        review_queue=queue or empty_review_queue(),
    )


def expansion_plan():
    return build_gold_set_expansion_plan(
        current_gold_summary={
            "gold_set_version": "seed_gold_set_v1",
            "case_count": 50,
            "families": {"freeze_workflow": 5, "adversarial_bypass": 8},
        },
        evaluation_report=clean_evaluation_report(),
        review_queue=empty_review_queue(),
        registry_record=registry_record(),
    )


class PromotionCriteriaGateTests(unittest.TestCase):
    def test_clean_inputs_are_only_eligible_for_future_shadow_mode_design_review(self):
        report = build_promotion_criteria_gate_report(
            candidate_registry_record=registry_record(),
            evaluation_report=clean_evaluation_report(),
            review_queue=empty_review_queue(),
            gold_expansion_plan=expansion_plan(),
        )
        self.assertEqual(report["feature_id"], FEATURE_ID)
        self.assertEqual(report["schema_version"], SCHEMA_VERSION)
        self.assertEqual(report["authority_statement"], AUTHORITY_STATEMENT)
        self.assertEqual(report["gate_decision"], ELIGIBLE_REVIEW_ONLY)
        self.assertEqual(report["next_allowed_step"], "future_governed_shadow_mode_design_review_only")
        self.assertEqual(report["promotion_blockers"], ["future_shadow_mode_design_review_required"])
        self.assertIs(report["promotion_blocked"], True)
        self.assertIs(report["may_promote_candidate"], False)
        self.assertIs(report["may_enable_shadow_mode"], False)
        self.assertIs(report["may_mutate_gold"], False)
        self.assertEqual(report["router_authority"], "none")
        self.assertEqual(report["runtime_integration"], "forbidden")
        self.assertTrue(validate_promotion_criteria_gate_report(report)["ok"])
        self.assertIs(assert_promotion_criteria_gate_report_valid(report), report)

    def test_mismatches_and_review_queue_items_block_gate(self):
        evaluation = clean_evaluation_report()
        evaluation["aggregate"]["mismatches"] = 2
        queue = empty_review_queue()
        queue["aggregate"]["queued_review_items"] = 1
        queue["aggregate"]["p1_items"] = 1
        queue["queue_items"] = [{"case_id": "case-needs-review", "priority": "P1"}]
        report = build_promotion_criteria_gate_report(
            candidate_registry_record=registry_record(evaluation=evaluation, queue=queue),
            evaluation_report=evaluation,
            review_queue=queue,
            gold_expansion_plan=expansion_plan(),
        )
        self.assertEqual(report["gate_decision"], BLOCKED)
        self.assertIn("candidate_gold_mismatches_present", report["promotion_blockers"])
        self.assertIn("human_review_queue_not_empty", report["promotion_blockers"])
        self.assertIn("p1_review_items_present", report["promotion_blockers"])
        self.assertEqual(report["next_allowed_step"], "resolve_blockers_with_human_review_before_future_phase")
        self.assertTrue(validate_promotion_criteria_gate_report(report)["ok"])

    def test_missing_expansion_plan_blocks_gate(self):
        report = build_promotion_criteria_gate_report(
            candidate_registry_record=registry_record(),
            evaluation_report=clean_evaluation_report(),
            review_queue=empty_review_queue(),
        )
        self.assertEqual(report["gate_decision"], BLOCKED)
        self.assertIn("gold_expansion_plan_missing", report["promotion_blockers"])
        self.assertTrue(validate_promotion_criteria_gate_report(report)["ok"])

    def test_report_hash_detects_mutation(self):
        report = build_promotion_criteria_gate_report(
            candidate_registry_record=registry_record(),
            evaluation_report=clean_evaluation_report(),
            review_queue=empty_review_queue(),
            gold_expansion_plan=expansion_plan(),
        )
        mutated = dict(report)
        mutated["gate_decision"] = BLOCKED
        result = validate_promotion_criteria_gate_report(mutated)
        self.assertFalse(result["ok"])
        self.assertIn("gate_hash mismatch", result["errors"])

    def test_type_errors_are_strict(self):
        with self.assertRaises(TypeError):
            build_promotion_criteria_gate_report(candidate_registry_record=[])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_promotion_criteria_gate_report(candidate_registry_record=registry_record(), evaluation_report=[])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_promotion_criteria_gate_report(candidate_registry_record=registry_record(), review_queue=[])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_promotion_criteria_gate_report(candidate_registry_record=registry_record(), gold_expansion_plan=[])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_promotion_criteria_gate_report(candidate_registry_record=registry_record(), gate_policy=[])  # type: ignore[arg-type]

    def test_module_uses_no_forbidden_runtime_or_io_imports(self):
        tree = ast.parse(MODULE.read_text(encoding="utf-8"))
        imports = set()
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    calls.add(func.id)
                elif isinstance(func, ast.Attribute):
                    calls.add(func.attr)
        for forbidden in (
            "os",
            "pathlib",
            "glob",
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "openai",
            "numpy",
            "sklearn",
            "pickle",
        ):
            self.assertNotIn(forbidden, imports)
        for forbidden_call in ("open", "write", "mkdir", "rglob", "glob", "scandir", "walk"):
            self.assertNotIn(forbidden_call, calls)

    def test_manifest_records_non_authority_characteristics(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_promotion_criteria_gate_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_promotion_criteria_gate_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_promotion_criteria_gate_status"],
            "standard_library_only_offline_in_memory_promotion_criteria_gate_no_file_io_no_promotion_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "adviser_promotion_criteria_gate_contains_file_io",
            "adviser_promotion_criteria_gate_contains_case_discovery",
            "adviser_promotion_criteria_gate_contains_source_scanning",
            "adviser_promotion_criteria_gate_contains_prompt_auto_loading",
            "adviser_promotion_criteria_gate_contains_artifact_io",
            "adviser_promotion_criteria_gate_contains_gate_persistence",
            "adviser_promotion_criteria_gate_contains_registry_writer",
            "adviser_promotion_criteria_gate_contains_candidate_output_persistence",
            "adviser_promotion_criteria_gate_contains_scratch_writer",
            "adviser_promotion_criteria_gate_contains_gold_mutation",
            "adviser_promotion_criteria_gate_contains_actual_promotion",
            "adviser_promotion_criteria_gate_contains_ml_execution",
            "adviser_promotion_criteria_gate_contains_embeddings_or_providers",
            "adviser_promotion_criteria_gate_contains_runtime_integration",
            "adviser_promotion_criteria_gate_contains_router_authority",
        ):
            self.assertIs(manifest[key], False, key)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_promotion_criteria_gate_v1",
            "adviser_promotion_gate_in_memory_only",
            "adviser_promotion_gate_no_actual_promotion",
            "adviser_promotion_gate_no_gate_persistence",
            "adviser_promotion_gate_shadow_mode_design_review_only",
            "adviser_phase_closure_gate_no_runtime_enablement",
        ):
            self.assertIn(expected, chars)

    def test_readme_says_no_promotion_or_runtime_authority(self):
        text = README.read_text(encoding="utf-8")
        for phrase in (
            "does **not** promote the candidate",
            "no actual promotion",
            "no runtime integration",
            "no router authority",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
