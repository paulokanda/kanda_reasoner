import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
DESIGN = ADVISER / "design"


class AdviserFoundationsReferenceBoxBoundaryDesignTests(unittest.TestCase):
    def test_design_documents_exist_and_are_ascii(self):
        for rel in (
            "adviser_foundations_reference.md",
            "adviser_box_boundary.md",
        ):
            path = DESIGN / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            self.assertIn("routing_signal_scorer_v3_adviser_foundations_reference_and_box_boundary_design_v1", text)
            self.assertIn("3.39-adviser-foundations-reference-and-box-boundary-design", text)

    def test_reference_declares_core_adviser_doctrine(self):
        text = (DESIGN / "adviser_foundations_reference.md").read_text(encoding="utf-8")
        for expected in (
            "ML recommends. Canon/router governance decides.",
            "Adviser output is evidence, not authority.",
            "Teacher answers must remain draft evidence",
            "ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, and UNKNOWN must never permit action.",
            "A future Adviser output guard is mandatory",
            "Disagreement severity must be implemented as code, not prose.",
            "Do not skip directly to candidate implementation.",
        ):
            self.assertIn(expected, text)

    def test_reference_declares_forbidden_runtime_behavior(self):
        text = (DESIGN / "adviser_foundations_reference.md").read_text(encoding="utf-8")
        for forbidden_phrase in (
            "candidate scorer implementation",
            "machine-learning execution",
            "embeddings",
            "vector indexes",
            "provider calls",
            "prompt auto-loading",
            "router authority changes",
            "runtime router integration",
            "source scanning",
            "artifact generation",
            "artifact reading",
            "artifact writing",
            "autonomous freeze writes",
            "autonomous decision recording",
            "dependency installation",
        ):
            self.assertIn(forbidden_phrase, text)

    def test_box_boundary_declares_import_and_file_boundaries(self):
        text = (DESIGN / "adviser_box_boundary.md").read_text(encoding="utf-8")
        for expected in (
            "Runtime router code must not import adviser_offline.",
            "adviser_offline must not import runtime router code.",
            "It must not create candidate, core, harness, contracts, test_data, gold, registry, or scratch implementation folders yet.",
            "No candidate exists yet.",
            "No router behavior changes.",
            "No runtime contract changes.",
            "No public export changes.",
        ):
            self.assertIn(expected, text)

    def test_manifest_declares_feature_and_status(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["adviser_foundations_reference_and_box_boundary_design_feature_id"],
            "routing_signal_scorer_v3_adviser_foundations_reference_and_box_boundary_design_v1",
        )
        self.assertEqual(
            manifest["adviser_foundations_reference_and_box_boundary_design_schema_version"],
            "3.39-adviser-foundations-reference-and-box-boundary-design",
        )
        self.assertEqual(
            manifest["adviser_foundations_reference_and_box_boundary_design_status"],
            "standard_library_only_adviser_foundations_reference_and_box_boundary_design_no_candidate_no_runtime_behavior_change",
        )

    def test_manifest_protected_characteristics(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_foundations_reference_and_box_boundary_design",
            "adviser_offline_sub_box_design_only",
            "no_adviser_candidate_scorer_from_foundations_reference",
            "no_runtime_router_import_from_adviser_offline",
            "no_adviser_offline_import_into_runtime_router",
            "no_prompt_auto_loading_from_adviser_foundations",
            "no_router_authority_from_adviser_foundations",
            "no_artifact_generation_from_adviser_foundations",
            "no_artifact_reading_from_adviser_foundations",
            "no_artifact_writing_from_adviser_foundations",
            "no_embeddings_from_adviser_foundations",
            "no_providers_from_adviser_foundations",
            "teacher_answers_not_ground_truth_without_review",
            "abstain_ambiguous_out_of_scope_must_not_permit_action",
            "future_adviser_requires_output_guard_before_candidate_trust",
            "future_adviser_severity_must_be_code_not_prose",
        ):
            self.assertIn(expected, chars)

    def test_no_candidate_or_runtime_adviser_modules_created(self):
        for rel in (
            "candidate",
            # M6 may create registry/ with pure record-builder modules only.
            # M5 may create harness/ with pure comparison/report modules only.
            # M3/M4 may create core/ with validator, output guard, severity, and resource-limit modules only.
            # M2 may create contracts/ as JSON-only schemas. M0 only forbids candidate/runtime/gold/scratch/runtime behavior; M7 allows seed input cases only.
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

    def test_contract_and_init_do_not_export_adviser_offline(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "adviser_foundations_reference",
            "adviser_box_boundary",
            "teacher_student",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_forbidden_runtime_generation_paths_absent(self):
        for rel in (
            "artifact_generator.py",
            "precomputed_artifact_generator.py",
            "precomputed_semantic_evidence_artifact_generator.py",
            "generated_artifacts",
            "artifacts",
            "vector_index.py",
            "indices",
            "providers",
        ):
            self.assertFalse((BOX / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
