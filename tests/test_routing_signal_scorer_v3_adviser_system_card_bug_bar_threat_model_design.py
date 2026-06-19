import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
DESIGN = ADVISER / "design"
FEATURE_ID = "routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design_v1"
SCHEMA_VERSION = "3.40-adviser-system-card-bug-bar-threat-model-design"


class AdviserSystemCardBugBarThreatModelDesignTests(unittest.TestCase):
    def test_design_documents_exist_are_ascii_and_identified(self):
        for rel in (
            "adviser_system_card.md",
            "adviser_bug_bar.md",
            "adviser_threat_model.md",
            "adviser_patterns.md",
        ):
            path = DESIGN / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            self.assertIn(FEATURE_ID, text)
            self.assertIn(SCHEMA_VERSION, text)
            self.assertIn("No candidate scorer", text)
            self.assertIn("no runtime router integration", text.lower())
            self.assertIn("no prompt auto-loading", text.lower())
            self.assertIn("no router authority", text.lower())

    def test_system_card_declares_use_non_use_and_limits(self):
        text = (DESIGN / "adviser_system_card.md").read_text(encoding="utf-8")
        for expected in (
            "Adviser output is evidence, not authority.",
            "ML recommends. Canon/router governance decides.",
            "Teacher answers are not ground truth",
            "ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, and UNKNOWN must never permit action.",
            "choose the final route",
            "load prompts",
            "write freeze memory",
            "call providers or models",
            "create embeddings",
            "invade neighboring boxes",
        ):
            self.assertIn(expected, text)

    def test_bug_bar_declares_zero_critical_error_budget(self):
        text = (DESIGN / "adviser_bug_bar.md").read_text(encoding="utf-8")
        for expected in (
            "Critical safety error budget is zero.",
            "unsafe proceed on governed work",
            "freeze confirmation bypass",
            "startup-delivery bypass",
            "prompt-library anti-audit bypass",
            "box invasion",
            "router-authority promotion",
            "prompt auto-loading",
            "autonomous memory write",
            "artifact generation in a forbidden phase",
            "Red-path cases are more important than convenience performance.",
        ):
            self.assertIn(expected, text)

    def test_threat_model_declares_main_threats_and_boundaries(self):
        text = (DESIGN / "adviser_threat_model.md").read_text(encoding="utf-8")
        for expected in (
            "No AI output is a security boundary.",
            "No teacher answer is ground truth until reviewed and frozen.",
            "No candidate output is authority.",
            "Runtime router code must not import adviser_offline.",
            "adviser_offline must not import runtime router code.",
            "Teacher contamination",
            "Gold-set poisoning",
            "Schema drift",
            "Lexical negation failure",
            "Candidate output mistaken as authority",
            "Resource exhaustion",
            "Cross-box leakage",
        ):
            self.assertIn(expected, text)

    def test_patterns_declares_future_design_patterns(self):
        text = (DESIGN / "adviser_patterns.md").read_text(encoding="utf-8")
        for expected in (
            "Advisory-Only Prediction",
            "Abstain First",
            "Teacher-Not-Ground-Truth",
            "Human-Reviewed Gold",
            "Gold-Set Versioning",
            "Output Guard",
            "Severity-as-Code",
            "Scratch-Only Candidate Output",
            "No Runtime Import",
            "Red Path Dominance",
            "Resource Budget First",
            "Candidate Registry",
        ):
            self.assertIn(expected, text)

    def test_manifest_declares_m1_feature_and_status(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_system_card_bug_bar_threat_model_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_system_card_bug_bar_threat_model_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_system_card_bug_bar_threat_model_design_status"],
            "standard_library_only_adviser_system_card_bug_bar_threat_model_design_no_candidate_no_runtime_behavior_change",
        )
        for key in (
            "adviser_system_card_doc",
            "adviser_bug_bar_doc",
            "adviser_threat_model_doc",
            "adviser_patterns_doc",
        ):
            self.assertIn("adviser_offline/design/", manifest[key])

    def test_manifest_protected_characteristics(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_system_card_bug_bar_threat_model_design",
            "adviser_system_card_advisory_only_limit",
            "adviser_bug_bar_zero_critical_error_budget",
            "adviser_threat_model_teacher_contamination_risk",
            "adviser_patterns_abstain_first",
            "adviser_patterns_teacher_not_ground_truth",
            "adviser_patterns_human_reviewed_gold",
            "adviser_patterns_scratch_only_candidate_output",
            "no_adviser_candidate_from_m1_design",
            "no_adviser_contract_validator_from_m1_design",
            "no_adviser_harness_from_m1_design",
            "no_adviser_schema_family_from_m1_design",
            "no_runtime_router_import_from_adviser_m1",
            "no_prompt_auto_loading_from_adviser_m1",
            "no_router_authority_from_adviser_m1",
            "no_ml_execution_from_adviser_m1",
        ):
            self.assertIn(expected, chars)

    def test_m1_does_not_create_implementation_directories_or_runtime_exports(self):
        for rel in (
            "candidate",
            # M6 may create registry/ with pure record-builder modules only.
            # M5 may create harness/ with pure comparison/report modules only.
            # M3/M4 may create core/ with validator, output guard, severity, and resource-limit modules only.
            # M2 may create contracts/ as JSON-only schemas. M1 only forbids candidate/runtime/gold/scratch/runtime behavior; M7 allows seed input cases only.
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
            # P0 starts the separate governed Pilot/Copilot P-series as a
            # scope-charter and entry-gate design only, after M35 and RG-PILOT-000,
            # without Pilot/Copilot activation, runtime export, prompt loading,
            # persistence, training-data use, batch mode, limited shadow runtime,
            # route comparison, or decisions.
            ADVISER / "transition_design" / "pilot_copilot_scope_charter_entry_gate_design.py",
            # P1 is a separate governed Pilot boundary design milestone
            # that may add the exact immutable Pilot boundary helper without
            # Pilot activation, projection implementation, prompt loading,
            # persistence, training-data use, batch mode, runtime export,
            # limited shadow runtime, or decisions.
            ADVISER / "transition_design" / "pilot_boundary_design.py",
            # P2 is a separate governed Pilot design-only milestone that may add the
            # exact immutable Pilot input/output contract and validator design helper
            # without live validation, input processing, output generation, Pilot behavior,
            # prompt loading, runtime export, persistence, or route authority.
            ADVISER / "transition_design" / "pilot_io_contract_validator_design.py",
            # P3 is a separate governed Pilot design-only milestone that may add the
            # exact immutable Pilot disagreement taxonomy helper without disagreement
            # detection, scoring, route comparison execution, Pilot behavior, prompt
            # loading, runtime export, persistence, or route authority.
            ADVISER / "transition_design" / "pilot_disagreement_taxonomy_design.py",
            # P4 is a separate governed Pilot design-only milestone that may add the
            # exact immutable gold/frozen-router reproduction harness design helper
            # without harness execution, gold loading, route comparison execution,
            # Pilot behavior, prompt loading, runtime export, persistence, or route authority.
            ADVISER / "transition_design" / "pilot_gold_router_reproduction_harness_design.py",
            # P5 is a separate governed Pilot design-only milestone that may add the
            # exact immutable simulation skeleton design helper without simulation
            # execution, live validation, input processing, output generation, route
            # comparison execution, Pilot behavior, prompt loading, runtime export,
            # persistence, or route authority.
            ADVISER / "transition_design" / "pilot_simulation_skeleton_design.py",
            # P6 is a separate governed Pilot design-only milestone that may add the
            # exact immutable review evidence design helper without evidence collection,
            # packet generation, live validation, input processing, output generation,
            # route comparison execution, Pilot behavior, prompt loading, runtime export,
            # persistence, human decision recording, or route authority.
            ADVISER / "transition_design" / "pilot_review_evidence_design.py",
            # P7 is a separate governed Pilot design-only implementation gate
            # milestone that may add the exact immutable gate design helper
            # without gate evaluation, implementation authorization, Pilot candidate
            # creation, prompt loading, runtime export, persistence, or route authority.
            ADVISER / "transition_design" / "pilot_implementation_gate_design.py",
        }
        py_files = set(ADVISER.rglob("*.py"))
        self.assertTrue(py_files.issubset(allowed_py), sorted(str(p) for p in py_files - allowed_py))
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "adviser_system_card",
            "adviser_bug_bar",
            "adviser_threat_model",
            "adviser_patterns",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
