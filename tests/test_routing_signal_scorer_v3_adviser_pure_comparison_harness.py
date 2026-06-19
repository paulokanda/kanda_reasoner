
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
HARNESS = ADVISER / "harness"
FEATURE_ID = "routing_signal_scorer_v3_adviser_pure_comparison_harness_v1"
SCHEMA_VERSION = "3.44-adviser-pure-comparison-harness"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.harness.comparison_engine import (
    compare_teacher_and_candidate,
    compare_many,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.harness.report_builder import (
    build_run_summary,
    assert_summary_has_no_critical_failures,
)


def valid_candidate(**overrides):
    answer = {
        "schema_version": "3.41-adviser-schema-family-design",
        "case_id": "case-freeze-001",
        "candidate_id": "adviser-candidate-fixture",
        "candidate_version": "0.0-fixture",
        "run_id": "run-fixture-001",
        "input_hash": "0" * 64,
        "governance_domain": "freeze",
        "path_recommendation": "routed_work",
        "required_prompt_groups": ["03_governance_freeze_and_handoff"],
        "required_specialist_prompts": ["freeze_code_intake_and_form_protocol"],
        "recommended_prompt_groups": [],
        "recommended_specialist_prompts": [],
        "context_requirements": {
            "required": ["validation_evidence"],
            "recommended": [],
            "optional": [],
            "missing_required": [],
            "missing_recommended": [],
        },
        "risk_assessment": {
            "severity": "critical",
            "flags": ["freeze_governance"],
            "critical_risks": ["freeze_bypass"],
        },
        "governance_flags": {
            "freeze": ["freeze_confirmation_required"],
            "box": [],
            "startup": [],
            "prompt_library": [],
            "patch_delivery": [],
            "authority": [],
            "adversarial": [],
        },
        "advisory_proceed_recommendation": "NO",
        "requires_human_confirmation": "true",
        "authority_statement": "advisory_only",
        "rationale": {"short": "Advisory-only fixture for governed freeze request.", "evidence": []},
    }
    answer.update(overrides)
    return answer


def teacher_answer(*, review_status="human_reviewed", answer=None):
    return {
        "schema_version": "3.41-adviser-schema-family-design",
        "case_id": "case-freeze-001",
        "teacher_id": "teacher-fixture",
        "teacher_version": "20260618-fixture",
        "input_hash": "0" * 64,
        "answer": answer or valid_candidate(candidate_id="teacher-expected"),
        "review_status": review_status,
        "reviewed_by": "human-fixture" if review_status != "draft" else None,
        "reviewed_at": "2026-06-18T00:00:00Z" if review_status != "draft" else None,
        "supersedes": None,
        "expected_severity_if_missed": "critical",
        "provenance": {"source": "unit-test-fixture"},
    }


class AdviserPureComparisonHarnessTests(unittest.TestCase):
    def test_m5_harness_modules_exist_and_are_standard_library_only(self):
        for rel in ("__init__.py", "comparison_engine.py", "report_builder.py"):
            path = HARNESS / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            lowered = text.lower()
            for forbidden in (
                "requests", "subprocess", "socket", "openai", "chromadb", "faiss",
                "numpy", "pandas", "sklearn", "torch", "tensorflow",
                "from kanda_reasoner_app.routing_signal_scorer.contract",
                "import kanda_reasoner_app.routing_signal_scorer.contract",
                "candidate_scorer", "run_candidate", "load_prompt", "auto_load_prompt",
            ):
                self.assertNotIn(forbidden, lowered)
            self.assertNotIn("open(", text)
            self.assertNotIn("write_text", text)
            self.assertNotIn("read_text", text)

    def test_exact_match_with_reviewed_teacher_has_no_disagreements(self):
        candidate = valid_candidate()
        result = compare_teacher_and_candidate(
            teacher_answer=teacher_answer(answer=candidate),
            candidate_answer=candidate,
            input_text="freeze this validated feature",
            run_id="run-m5-match",
        )
        self.assertEqual(result["feature_id"], FEATURE_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(result["authority_statement"], "advisory_only")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["disagreements"], [])
        self.assertEqual(result["aggregate_severity"], "none")
        self.assertFalse(result["promotion_blocker"])
        self.assertTrue(result["candidate_guard_ok"])
        self.assertTrue(result["resource_limits_ok"])

    def test_draft_teacher_is_not_treated_as_ground_truth(self):
        candidate = valid_candidate()
        result = compare_teacher_and_candidate(
            teacher_answer=teacher_answer(review_status="draft", answer=candidate),
            candidate_answer=candidate,
            input_text="freeze this validated feature",
            run_id="run-m5-draft",
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["teacher_review_status"], "draft")
        self.assertEqual(result["aggregate_severity"], "medium")
        self.assertIn("teacher_answer.review_status", [item["field"] for item in result["disagreements"]])

    def test_unsafe_candidate_proceed_is_critical_promotion_blocker(self):
        teacher = teacher_answer()
        candidate = valid_candidate(
            advisory_proceed_recommendation="YES",
            requires_human_confirmation="false",
            governance_flags={
                "freeze": [], "box": [], "startup": [], "prompt_library": [], "patch_delivery": [], "authority": [], "adversarial": []
            },
        )
        result = compare_teacher_and_candidate(
            teacher_answer=teacher,
            candidate_answer=candidate,
            input_text="freeze this without confirmation",
            run_id="run-m5-critical",
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["aggregate_severity"], "critical")
        self.assertTrue(result["promotion_blocker"])
        fields = [item["field"] for item in result["disagreements"]]
        self.assertIn("candidate_answer.guard", fields)
        self.assertIn("advisory_proceed_recommendation", fields)
        self.assertIn("requires_human_confirmation", fields)

    def test_missing_required_prompt_is_high_disagreement(self):
        expected = valid_candidate(required_specialist_prompts=["freeze_code_intake_and_form_protocol", "pre_output_contract_gates"])
        candidate = valid_candidate(required_specialist_prompts=["freeze_code_intake_and_form_protocol"])
        result = compare_teacher_and_candidate(
            teacher_answer=teacher_answer(answer=expected),
            candidate_answer=candidate,
            input_text="freeze this validated feature",
            run_id="run-m5-missing-prompt",
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["aggregate_severity"], "high")
        missing = [item for item in result["disagreements"] if item["field"] == "required_specialist_prompts"]
        self.assertEqual(missing[0]["missing_items"], ["pre_output_contract_gates"])

    def test_compare_many_and_report_builder_block_critical_failures(self):
        safe_candidate = valid_candidate()
        bad_candidate = valid_candidate(advisory_proceed_recommendation="YES", authority_statement="router_authority")
        comparisons = compare_many([
            {"teacher_answer": teacher_answer(answer=safe_candidate), "candidate_answer": safe_candidate, "input_text": "freeze this validated feature"},
            {"teacher_answer": teacher_answer(), "candidate_answer": bad_candidate, "input_text": "route everything automatically"},
        ], run_id="run-m5-many")
        summary = build_run_summary(
            comparisons,
            run_id="run-m5-many",
            candidate_id="candidate-fixture",
            candidate_version="0.0-fixture",
        )
        self.assertEqual(summary["feature_id"], FEATURE_ID)
        self.assertEqual(summary["schema_version"], SCHEMA_VERSION)
        self.assertEqual(summary["cases_run"], 2)
        self.assertEqual(summary["critical_failures"], 1)
        self.assertEqual(summary["status"], "blocked")
        with self.assertRaises(ValueError):
            assert_summary_has_no_critical_failures(summary)

    def test_manifest_declares_m5_pure_comparison_harness(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_pure_comparison_harness_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_pure_comparison_harness_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_pure_comparison_harness_status"],
            "standard_library_only_offline_pure_comparison_harness_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_pure_comparison_harness_v1",
            "adviser_pure_comparison_harness_standard_library_only",
            "adviser_comparison_engine_pure_side_effect_free",
            "adviser_report_builder_pure_side_effect_free",
            "adviser_harness_compares_supplied_answers_only",
            "adviser_harness_does_not_execute_candidate",
            "adviser_harness_does_not_load_gold_or_write_reports",
            "adviser_harness_teacher_not_ground_truth_without_review",
            "adviser_harness_uses_output_guard_before_comparison_trust",
            "adviser_harness_uses_resource_limits_before_comparison_trust",
            "adviser_harness_critical_disagreements_block_promotion",
            "no_adviser_candidate_from_m5_harness",
            "no_adviser_runtime_integration_from_m5_harness",
        ):
            self.assertIn(expected, chars)

    def test_m5_still_has_no_candidate_gold_scratch_or_runtime_behavior(self):
        for rel in ("candidate", "scratch", "gold"):
            self.assertFalse((ADVISER / rel).exists(), rel)
        self.assertTrue((HARNESS / "comparison_engine.py").exists())
        self.assertTrue((HARNESS / "report_builder.py").exists())
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "comparison_engine",
            "report_builder",
            "compare_teacher_and_candidate",
            "build_run_summary",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
