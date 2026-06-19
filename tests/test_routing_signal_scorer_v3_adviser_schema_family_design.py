import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
CONTRACTS = ADVISER / "contracts"
FEATURE_ID = "routing_signal_scorer_v3_adviser_schema_family_design_v1"
SCHEMA_VERSION = "3.41-adviser-schema-family-design"


class AdviserSchemaFamilyDesignTests(unittest.TestCase):
    def _load(self, name):
        path = CONTRACTS / name
        self.assertTrue(path.exists(), name)
        text = path.read_text(encoding="utf-8")
        text.encode("ascii")
        data = json.loads(text)
        self.assertEqual(data["feature_id"], FEATURE_ID)
        self.assertEqual(data["schema_version"], SCHEMA_VERSION)
        self.assertIn("design_only_json_contract", data["design_status"])
        return data

    def test_all_schema_files_exist_and_are_json_design_contracts(self):
        for name in (
            "adviser_case_schema.json",
            "adviser_candidate_answer_schema.json",
            "teacher_answer_schema.json",
            "disagreement_report_schema.json",
            "human_review_record_schema.json",
            "harness_run_record_schema.json",
            "gold_manifest_schema.json",
            "candidate_registry_schema.json",
        ):
            self._load(name)

    def test_candidate_answer_schema_has_safe_enums_and_no_unconditional_yes(self):
        data = self._load("adviser_candidate_answer_schema.json")
        enums = data["enums"]
        self.assertIn("ambiguous", enums["governance_domain"])
        self.assertIn("out_of_scope", enums["governance_domain"])
        self.assertIn("unknown", enums["governance_domain"])
        self.assertIn("abstain", enums["path_recommendation"])
        self.assertIn("ABSTAIN", enums["advisory_proceed_recommendation"])
        self.assertIn("UNKNOWN", enums["advisory_proceed_recommendation"])
        self.assertNotIn("YES", enums["advisory_proceed_recommendation"])
        self.assertNotIn("YES_UNCONDITIONAL", enums["advisory_proceed_recommendation"])
        self.assertEqual(enums["authority_statement"], ["advisory_only"])
        forbidden = set(data["explicitly_forbidden_values"]["advisory_proceed_recommendation"])
        self.assertIn("YES", forbidden)
        self.assertIn("AUTO_PROCEED", forbidden)

    def test_candidate_answer_schema_required_fields(self):
        data = self._load("adviser_candidate_answer_schema.json")
        required = set(data["required_fields"])
        for field in (
            "case_id",
            "candidate_id",
            "candidate_version",
            "run_id",
            "input_hash",
            "governance_domain",
            "path_recommendation",
            "required_prompt_groups",
            "required_specialist_prompts",
            "context_requirements",
            "risk_assessment",
            "governance_flags",
            "advisory_proceed_recommendation",
            "requires_human_confirmation",
            "authority_statement",
            "rationale",
        ):
            self.assertIn(field, required)

    def test_teacher_answer_schema_preserves_teacher_not_ground_truth_rule(self):
        data = self._load("teacher_answer_schema.json")
        required = set(data["required_fields"])
        for field in (
            "teacher_id",
            "teacher_version",
            "review_status",
            "reviewed_by",
            "reviewed_at",
            "supersedes",
            "expected_severity_if_missed",
            "provenance",
        ):
            self.assertIn(field, required)
        rules = "\n".join(data["safety_rules"])
        self.assertIn("teacher answers are not ground truth automatically", rules)
        self.assertIn("corrections supersede", rules)

    def test_gold_manifest_and_human_review_are_governed(self):
        gold = self._load("gold_manifest_schema.json")
        review = self._load("human_review_record_schema.json")
        self.assertIn("manifest_hash", gold["required_fields"])
        self.assertIn("case_hashes", gold["required_fields"])
        self.assertIn("review_status_summary", gold["required_fields"])
        self.assertIn("review_decision", review["required_fields"])
        self.assertIn("safety_impact", review["required_fields"])
        self.assertIn("approve_gold", review["enums"]["review_decision"])
        self.assertIn("critical", review["enums"]["safety_impact"])

    def test_disagreement_run_and_registry_schemas_are_provenance_only(self):
        disagreement = self._load("disagreement_report_schema.json")
        run = self._load("harness_run_record_schema.json")
        registry = self._load("candidate_registry_schema.json")
        self.assertIn("promotion_blocker", disagreement["required_fields"])
        self.assertIn("critical_failures", run["required_fields"])
        self.assertIn("candidate_code_hash", run["required_fields"])
        self.assertIn("code_hash", registry["required_fields"])
        self.assertIn("critical_failures", registry["required_fields"])
        for data in (disagreement, run, registry):
            self.assertIn("runtime_router_integration", data["forbidden_runtime_behaviors"])
            self.assertIn("provider_calls", data["forbidden_runtime_behaviors"])

    def test_manifest_declares_m2_schema_family(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_schema_family_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_schema_family_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_schema_family_design_status"],
            "standard_library_only_adviser_schema_family_design_no_validator_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_schema_family_design",
            "adviser_contracts_json_design_only",
            "adviser_candidate_answer_schema_no_unconditional_yes",
            "adviser_teacher_answer_schema_teacher_not_ground_truth",
            "adviser_gold_manifest_schema_hash_and_review_required",
            "no_adviser_contract_validator_from_m2_design",
            "no_adviser_candidate_from_m2_design",
            "no_adviser_harness_from_m2_design",
            "no_runtime_router_import_from_adviser_m2",
            "no_router_authority_from_adviser_m2",
        ):
            self.assertIn(expected, chars)

    def test_m2_has_no_executable_adviser_logic_or_runtime_exports(self):
        for rel in (
            "candidate",
            # M5 may create harness/ with pure comparison/report modules only.
            # M3/M4 may create core/ with validator, output guard, severity, and resource-limit modules only.
            "scratch",
            "gold",
        ):
            self.assertFalse((ADVISER / rel).exists(), rel)
        allowed_py = {
            ADVISER / "core" / "__init__.py",
            ADVISER / "core" / "adviser_contract.py",
            ADVISER / "core" / "adviser_output_guard.py",
            ADVISER / "core" / "adviser_severity.py",
            ADVISER / "core" / "adviser_resource_limits.py",
            ADVISER / "harness" / "__init__.py",
            ADVISER / "harness" / "comparison_engine.py",
            ADVISER / "harness" / "report_builder.py",
            ADVISER / "registry" / "__init__.py",
            ADVISER / "registry" / "hash_utils.py",
            ADVISER / "registry" / "gold_manifest.py",
            ADVISER / "registry" / "run_registry.py",
            # M14 may add the exact pure in-memory candidate registry record builder.
            ADVISER / "registry" / "candidate_registry.py",
            # M11 is a separate governed Adviser milestone that may add the
            # exact offline lexical candidate while preserving no runtime export.
            ADVISER / "candidate_v0" / "__init__.py",
            ADVISER / "candidate_v0" / "offline_lexical_scorer.py",
            # M12 is a separate governed Adviser milestone that may add the
            # exact in-memory evaluation runner while preserving no runtime export.
            ADVISER / "evaluation" / "__init__.py",
            ADVISER / "evaluation" / "candidate_v0_evaluation_runner.py",
            # M13 is a separate governed Adviser milestone that may add the
            # exact in-memory active review queue while preserving no runtime export.
            ADVISER / "review_queue" / "__init__.py",
            ADVISER / "review_queue" / "active_review_queue.py",
            # M15 is a separate governed Adviser milestone that may add the
            # exact in-memory gold expansion plan while preserving no runtime export.
            ADVISER / "gold_expansion" / "__init__.py",
            ADVISER / "gold_expansion" / "gold_set_expansion_plan.py",
            # M16 is the final Adviser-phase gate milestone that may add the
            # exact in-memory promotion criteria gate while preserving no runtime export.
            ADVISER / "promotion_gate" / "__init__.py",
            ADVISER / "promotion_gate" / "promotion_criteria_gate.py",
            # M17 is a separate governed post-Adviser design-only milestone
            # that may add exact transition design helpers without runtime export.
            ADVISER / "transition_design" / "__init__.py",
            ADVISER / "transition_design" / "shadow_mode_assistant_transition_design.py",
            # M18 is a separate governed post-Adviser boundary design milestone
            # that may add the exact immutable shadow-mode boundary design helper
            # without runtime export, shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_boundary_design.py",
            # M19 is a separate governed post-Adviser contract design milestone
            # that may add the exact immutable shadow-mode input/output contract
            # design helper without validation logic, observation execution,
            # runtime export, shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_io_contract_design.py",
            # M20 is a separate governed post-Adviser validator design milestone
            # that may add the exact immutable shadow-mode contract validator
            # design helper without live validation logic, observation execution,
            # runtime export, shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_contract_validator_design.py",
            # M21 is a separate governed post-Adviser skeleton design milestone
            # that may add the exact immutable shadow-mode observation skeleton
            # design helper without a callable observation builder, runtime export,
            # shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_observation_skeleton_design.py",
            # M22 is a separate governed post-Adviser implementation gate design
            # milestone that may add the exact immutable shadow-mode implementation
            # gate design helper without a live gate, runtime export, shadow
            # activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_implementation_gate_design.py",
            ADVISER / "transition_design" / "shadow_mode_non_runtime_observation.py",
            # M24 is a separate governed post-Adviser review evidence design
            # milestone that may add the exact immutable shadow observation
            # review evidence design helper without a live builder, persistence,
            # runtime export, shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_observation_review_evidence_design.py",
            # M25 is a separate governed post-Adviser readiness gate design
            # milestone that may add the exact immutable Assistant boundary
            # review prerequisite design helper without a live gate, runtime
            # export, shadow activation, or Assistant behavior.
            ADVISER / "transition_design" / "shadow_mode_assistant_boundary_readiness_gate_design.py",
            # M26 is a separate governed post-Adviser Auxiliar/Assistant boundary
            # design milestone that may add the exact immutable boundary design
            # helper without Assistant activation, runtime export, prompt loading,
            # shadow activation, or human decision recording.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_boundary_design.py",
            # M27 is a separate governed post-Adviser Auxiliar/Assistant contract
            # design milestone that may add the exact immutable input/output
            # contract design helper without input processing, output generation,
            # Assistant activation, runtime export, prompt loading, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_io_contract_design.py",
            # M28 is a separate governed post-Adviser Auxiliar/Assistant validator
            # design milestone that may add the exact immutable contract-validator
            # design helper without live validation, input/output execution,
            # Assistant activation, runtime export, prompt loading, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_contract_validator_design.py",
            # M29 is a separate governed post-Adviser Auxiliar/Assistant assistance
            # skeleton design milestone that may add the exact immutable skeleton
            # design helper without live assistance, Assistant activation, runtime
            # export, prompt loading, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_assistance_skeleton_design.py",
            # M30 is a separate governed post-Adviser Auxiliar/Assistant
            # implementation gate design milestone that may add the exact immutable
            # implementation gate design helper without a live gate, Assistant
            # activation, runtime export, prompt loading, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_implementation_gate_design.py",
            # M31 is a separate governed post-Adviser non-runtime Auxiliar/Assistant
            # assistance implementation milestone that may add the exact fail-closed
            # in-memory assistance helper without Assistant activation, runtime
            # export, prompt loading, persistence, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_non_runtime_assistance.py",
            # M32 is a separate governed post-Adviser Auxiliar/Assistant
            # assistance review evidence design milestone that may add the exact
            # immutable evidence field design helper without a live builder,
            # persistence, Assistant activation, runtime export, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_assistance_review_evidence_design.py",
            # M33 is a separate governed post-Adviser Auxiliar/Assistant
            # readiness gate design milestone for future Pilot boundary review
            # prerequisites only, without a live gate, Pilot/Copilot activation,
            # runtime export, prompt loading, persistence, or decisions.
            ADVISER / "transition_design" / "shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design.py",
            # M34 is a separate governed post-Adviser Pilot/Copilot boundary
            # design milestone that may add the exact immutable boundary design
            # helper without Pilot/Copilot activation, runtime export, prompt
            # loading, persistence, route execution, or decisions.
            ADVISER / "transition_design" / "shadow_mode_pilot_copilot_boundary_design.py",
            # M35 is a separate governed post-Adviser bridge-closure design
            # milestone that may add the exact immutable handoff closure design
            # helper without Pilot/Copilot activation, runtime export, prompt
            # loading, persistence, route execution, or decisions.
            ADVISER / "transition_design" / "shadow_mode_post_adviser_pilot_copilot_handoff_closure_design.py",
        }
        py_files = set(ADVISER.rglob("*.py"))
        self.assertTrue(py_files.issubset(allowed_py), sorted(str(p) for p in py_files - allowed_py))
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "adviser_candidate",
            "adviser_contract",
            "adviser_output_guard",
            "comparison_engine",
            "gold_loader",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
