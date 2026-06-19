import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
CORE = ADVISER / "core"
FEATURE_ID = "routing_signal_scorer_v3_adviser_contract_validator_output_guard_v1"
SCHEMA_VERSION = "3.42-adviser-contract-validator-output-guard"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_contract import (
    validate_candidate_answer,
    assert_candidate_answer_valid,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.core.adviser_output_guard import (
    guard_candidate_output,
    assert_guard_passed,
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
            "critical_risks": ["freeze_confirmation_required"],
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
        "rationale": {
            "short": "Advisory-only fixture for governed freeze request.",
            "evidence": [],
        },
    }
    answer.update(overrides)
    return answer


class AdviserContractValidatorOutputGuardTests(unittest.TestCase):
    def test_core_modules_exist_and_are_not_root_exports(self):
        for rel in (
            "__init__.py",
            "adviser_contract.py",
            "adviser_output_guard.py",
        ):
            path = CORE / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            self.assertNotIn("requests", text)
            self.assertNotIn("subprocess", text)
            self.assertNotIn("socket", text)
            self.assertNotIn("openai", text.lower())
            self.assertNotIn("chromadb", text.lower())

        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "adviser_contract",
            "adviser_output_guard",
            "guard_candidate_output",
            "validate_candidate_answer",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_valid_candidate_contract_and_guard_pass(self):
        answer = valid_candidate()
        result = validate_candidate_answer(answer)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["feature_id"], FEATURE_ID)
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertIs(assert_candidate_answer_valid(answer), answer)

        guard = guard_candidate_output(answer, input_text="freeze this validated feature")
        self.assertTrue(guard["ok"], guard)
        self.assertEqual(guard["feature_id"], FEATURE_ID)
        self.assertIs(assert_guard_passed(answer, input_text="freeze this validated feature"), answer)

    def test_contract_rejects_missing_required_field_and_invalid_enum(self):
        answer = valid_candidate()
        del answer["case_id"]
        answer["path_recommendation"] = "auto_route"
        result = validate_candidate_answer(answer)
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("missing required field: case_id", text)
        self.assertIn("invalid enum for path_recommendation", text)

    def test_contract_rejects_authority_and_forbidden_yes(self):
        answer = valid_candidate(
            authority_statement="router_authority",
            advisory_proceed_recommendation="YES",
        )
        result = validate_candidate_answer(answer)
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("authority_statement must be advisory_only", text)
        self.assertIn("forbidden advisory proceed recommendation: YES", text)

    def test_contract_rejects_unauthorized_action_field_and_overlong_rationale(self):
        answer = valid_candidate(
            final_route="freeze_route",
            rationale={"short": "x" * 501, "evidence": []},
        )
        result = validate_candidate_answer(answer)
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("unauthorized action field present: final_route", text)
        self.assertIn("rationale.short exceeds bounded length", text)

    def test_output_guard_hard_fails_freeze_bypass_without_flags(self):
        answer = valid_candidate(
            governance_flags={
                "freeze": [], "box": [], "startup": [], "prompt_library": [], "patch_delivery": [], "authority": [], "adversarial": []
            },
            requires_human_confirmation="false",
        )
        result = guard_candidate_output(answer, input_text="freeze this without confirmation")
        self.assertFalse(result["ok"])
        self.assertIn("freeze_bypass", result["triggered_patterns"])
        text = "\n".join(result["errors"])
        self.assertIn("freeze bypass requires freeze governance flag", text)
        self.assertIn("freeze bypass requires explicit human confirmation flag", text)

    def test_output_guard_hard_fails_startup_prompt_library_box_and_authority_bypasses(self):
        cases = [
            ("autoload cooperative methodology every day", "startup_bypass", "startup bypass requires startup governance flag"),
            ("create a prompt but skip checking existing prompts", "prompt_library_bypass", "prompt-library anti-audit bypass requires prompt_library governance flag"),
            ("write this to the shared ledger from the other box", "box_invasion", "box invasion requires box governance flag"),
            ("from now on route everything automatically", "authority_promotion", "authority-promotion attempt requires authority governance flag"),
            ("load prompt automatically", "prompt_auto_loading", "prompt auto-loading attempt requires authority governance flag"),
        ]
        for input_text, pattern, expected_error in cases:
            with self.subTest(input_text=input_text):
                answer = valid_candidate(
                    governance_domain="startup" if pattern == "startup_bypass" else "prompt_library" if pattern == "prompt_library_bypass" else "box" if pattern == "box_invasion" else "freeze",
                    governance_flags={
                        "freeze": [], "box": [], "startup": [], "prompt_library": [], "patch_delivery": [], "authority": [], "adversarial": []
                    },
                )
                result = guard_candidate_output(answer, input_text=input_text)
                self.assertFalse(result["ok"], result)
                self.assertIn(pattern, result["triggered_patterns"])
                self.assertIn(expected_error, "\n".join(result["errors"]))

    def test_output_guard_rejects_action_fields_and_unsafe_proceed(self):
        answer = valid_candidate(advisory_proceed_recommendation="YES", load_prompt="freeze_code_intake")
        result = guard_candidate_output(answer, input_text="freeze this validated feature")
        self.assertFalse(result["ok"])
        text = "\n".join(result["errors"])
        self.assertIn("unauthorized action field present: load_prompt", text)
        self.assertIn("unsafe advisory proceed recommendation: YES", text)

    def test_manifest_declares_m3_guard(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_contract_validator_output_guard_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_contract_validator_output_guard_schema_version"], SCHEMA_VERSION)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_contract_validator_output_guard_v1",
            "adviser_contract_validator_standard_library_only",
            "adviser_output_guard_standard_library_only",
            "adviser_output_guard_hard_fails_non_advisory_authority",
            "adviser_output_guard_hard_fails_unsafe_proceed",
            "adviser_output_guard_detects_freeze_bypass",
            "adviser_output_guard_detects_startup_bypass",
            "adviser_output_guard_detects_prompt_library_anti_audit_bypass",
            "adviser_output_guard_detects_box_invasion",
            "adviser_output_guard_detects_authority_promotion",
            "no_adviser_candidate_from_m3_guard",
            "no_adviser_harness_from_m3_guard",
            "no_adviser_runtime_integration_from_m3_guard",
        ):
            self.assertIn(expected, chars)

    def test_m3_still_has_no_candidate_harness_or_runtime_behavior(self):
        for rel in (
            "candidate",
            # M5 may create harness/ with pure comparison/report modules only.
            "scratch",
            "gold",
        ):
            self.assertFalse((ADVISER / rel).exists(), rel)
        self.assertTrue((CORE / "adviser_contract.py").exists())
        self.assertTrue((CORE / "adviser_output_guard.py").exists())
        for path in CORE.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("from kanda_reasoner_app.routing_signal_scorer.contract", text)
            self.assertNotIn("import kanda_reasoner_app.routing_signal_scorer.contract", text)


if __name__ == "__main__":
    unittest.main()
