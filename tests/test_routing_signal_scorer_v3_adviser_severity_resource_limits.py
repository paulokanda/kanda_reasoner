import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
CORE = ADVISER / "core"
FEATURE_ID = "routing_signal_scorer_v3_adviser_severity_resource_limits_v1"
SCHEMA_VERSION = "3.43-adviser-severity-resource-limits"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_output_guard import guard_candidate_output
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_severity import (
    CRITICAL_FAILURE_BUDGET,
    evaluate_guard_result,
    evaluate_candidate_risk,
    assert_no_critical_failure,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_resource_limits import (
    MAX_INPUT_TEXT_CHARS,
    check_case_input_limits,
    check_candidate_output_limits,
    check_all_resource_limits,
    assert_resource_limits_ok,
)


def valid_candidate(**overrides):
    answer = {
        "schema_version": "3.41-adviser-schema-family-design",
        "case_id": "case-001",
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
            "required": [],
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


class AdviserSeverityResourceLimitsTests(unittest.TestCase):
    def test_m4_core_modules_exist_and_are_standard_library_only(self):
        for rel in ("adviser_severity.py", "adviser_resource_limits.py"):
            path = CORE / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            for forbidden in (
                "requests", "subprocess", "socket", "openai", "chromadb", "faiss",
                "numpy", "pandas", "sklearn", "torch", "tensorflow",
                "from kanda_reasoner_app.routing_signal_scorer.contract",
                "import kanda_reasoner_app.routing_signal_scorer.contract",
            ):
                self.assertNotIn(forbidden, text.lower())
            self.assertNotIn("open(", text)
            self.assertNotIn("write_text", text)
            self.assertNotIn("read_text", text)

    def test_severity_marks_freeze_bypass_as_p0_critical(self):
        answer = valid_candidate(
            governance_flags={
                "freeze": [], "box": [], "startup": [], "prompt_library": [], "patch_delivery": [], "authority": [], "adversarial": []
            },
            requires_human_confirmation="false",
        )
        guard = guard_candidate_output(answer, input_text="freeze this without confirmation")
        self.assertFalse(guard["ok"])
        result = evaluate_guard_result(guard, candidate_output=answer)
        self.assertEqual(result["feature_id"], FEATURE_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(result["severity"], "P0_CRITICAL")
        self.assertTrue(result["critical_failure"])
        self.assertTrue(result["promotion_blocker"])
        self.assertIn("freeze_bypass", result["codes"])
        with self.assertRaises(ValueError):
            assert_no_critical_failure(result)

    def test_severity_zero_critical_budget_and_authority_unsafe_proceed(self):
        self.assertEqual(CRITICAL_FAILURE_BUDGET, 0)
        result = evaluate_candidate_risk(valid_candidate(
            authority_statement="router_authority",
            advisory_proceed_recommendation="YES",
        ))
        self.assertEqual(result["severity"], "P0_CRITICAL")
        self.assertIn("unsafe_proceed", result["codes"])
        self.assertIn("non_advisory_authority", result["codes"])
        self.assertEqual(result["error_budget_allowed"], 0)

    def test_resource_limits_accept_bounded_case_and_reject_oversized_input(self):
        ok = check_case_input_limits("freeze this validated feature")
        self.assertTrue(ok["ok"], ok)
        self.assertIs(assert_resource_limits_ok(ok), ok)
        too_large = check_case_input_limits("x" * (MAX_INPUT_TEXT_CHARS + 1))
        self.assertFalse(too_large["ok"])
        self.assertIn("input_text exceeds", "\n".join(too_large["errors"]))

    def test_resource_limits_reject_fanout_and_overlong_rationale(self):
        answer = valid_candidate(
            required_specialist_prompts=[f"prompt_{i}" for i in range(21)],
            rationale={"short": "x" * 501, "evidence": []},
        )
        result = check_candidate_output_limits(answer)
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("required_specialist_prompts exceeds limit 20", text)
        self.assertIn("rationale.short exceeds 500 characters", text)

    def test_resource_limits_aggregate_input_and_candidate_checks(self):
        result = check_all_resource_limits(
            input_text="x" * (MAX_INPUT_TEXT_CHARS + 1),
            candidate_output=valid_candidate(required_prompt_groups=[f"g{i}" for i in range(13)]),
        )
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("input_text exceeds", text)
        self.assertIn("required_prompt_groups exceeds limit 12", text)

    def test_manifest_declares_m4_severity_resource_limits(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_severity_resource_limits_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_severity_resource_limits_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_critical_failure_budget"], 0)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_severity_resource_limits_v1",
            "adviser_severity_evaluator_standard_library_only",
            "adviser_resource_limits_standard_library_only",
            "adviser_severity_is_code_not_prose",
            "adviser_critical_failure_budget_zero",
            "adviser_p0_critical_failures_are_promotion_blockers",
            "adviser_resource_limits_before_future_candidate_or_harness",
            "no_adviser_candidate_from_m4_severity_resource_limits",
            "no_adviser_harness_from_m4_severity_resource_limits",
            "no_adviser_runtime_integration_from_m4",
        ):
            self.assertIn(expected, chars)

    def test_m4_still_has_no_candidate_harness_or_runtime_behavior(self):
        for rel in ("candidate", "scratch", "gold"):
            self.assertFalse((ADVISER / rel).exists(), rel)
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline", "adviser_severity", "adviser_resource_limits",
            "evaluate_guard_result", "check_all_resource_limits", "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
