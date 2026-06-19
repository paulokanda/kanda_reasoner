import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
TRANSITION = BOX / "adviser_offline" / "transition_design"
MANIFEST = BOX / "box_manifest.json"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_implementation_gate_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_implementation_gate_notes.md"

FEATURE_ID = "routing_signal_scorer_v3_auxiliar_assistant_implementation_gate_design_v1"
SCHEMA_VERSION = "3.71-auxiliar-assistant-implementation-gate-design"
NEXT_ALLOWED_MILESTONE = "M31 - Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_assistance_skeleton_design import (  # noqa: E402
    NEXT_ALLOWED_MILESTONE as M29_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_implementation_gate_design import (  # noqa: E402
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    build_auxiliar_assistant_implementation_gate_design,
)

FORBIDDEN_IMPORTS = {
    "os",
    "sys",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "pathlib",
    "json",
    "openai",
}

FORBIDDEN_CALLS = {
    "open",
    "print",
    "eval",
    "exec",
    "compile",
    "input",
    "__import__",
}

FORBIDDEN_RUNTIME_BEHAVIOR_DEFS = (
    "run_gate",
    "evaluate_gate",
    "activate_shadow_mode",
    "start_assistant",
    "start_auxiliar",
    "start_copilot",
    "compare_routes",
    "select_route",
    "load_prompt",
    "write_report",
    "record_human_decision",
    "promote_candidate",
    "process_input",
    "generate_output",
    "validate_contract",
    "build_assistance",
)


class AuxiliarAssistantImplementationGateDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _criterion_ids(self, criteria):
        return {criterion.criterion_id for criterion in criteria}

    def test_manifest_declares_m30_auxiliar_assistant_implementation_gate_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_implementation_gate_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_implementation_gate_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_implementation_gate_design_status"],
            "immutable_design_only_implementation_gate_no_live_gate_no_assistant_behavior_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_implementation_gate_design_policy"],
            "future_non_runtime_auxiliar_assistant_assistance_implementation_gate_design_only_no_assistant_activation_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_implementation_gate_design_module"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_implementation_gate_design.py",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_implementation_gate_design_notes_doc"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_implementation_gate_notes.md",
        )
        self.assertEqual(manifest["auxiliar_assistant_implementation_gate_design_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        for key in (
            "auxiliar_assistant_implementation_gate_design_requires_m18_boundary",
            "auxiliar_assistant_implementation_gate_design_requires_m19_io_contract",
            "auxiliar_assistant_implementation_gate_design_requires_m20_contract_validator_design",
            "auxiliar_assistant_implementation_gate_design_requires_m21_observation_skeleton_design",
            "auxiliar_assistant_implementation_gate_design_requires_m22_implementation_gate_design",
            "auxiliar_assistant_implementation_gate_design_requires_m23_non_runtime_observation",
            "auxiliar_assistant_implementation_gate_design_requires_m24_review_evidence_design",
            "auxiliar_assistant_implementation_gate_design_requires_m25_readiness_gate_design",
            "auxiliar_assistant_implementation_gate_design_requires_m26_auxiliar_assistant_boundary_design",
            "auxiliar_assistant_implementation_gate_design_requires_m27_auxiliar_assistant_io_contract_design",
            "auxiliar_assistant_implementation_gate_design_requires_m28_auxiliar_assistant_contract_validator_design",
            "auxiliar_assistant_implementation_gate_design_requires_m29_auxiliar_assistant_assistance_skeleton_design",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            "auxiliar_assistant_implementation_gate_design_contains_live_implementation_gate",
            "auxiliar_assistant_implementation_gate_design_contains_callable_gate_entrypoint",
            "auxiliar_assistant_implementation_gate_design_contains_implementation_permission_grant",
            "auxiliar_assistant_implementation_gate_design_contains_runtime_state_inspection",
            "auxiliar_assistant_implementation_gate_design_contains_live_assistance_execution",
            "auxiliar_assistant_implementation_gate_design_contains_callable_assistance_builder",
            "auxiliar_assistant_implementation_gate_design_contains_live_contract_validation",
            "auxiliar_assistant_implementation_gate_design_contains_input_processing",
            "auxiliar_assistant_implementation_gate_design_contains_output_generation",
            "auxiliar_assistant_implementation_gate_design_contains_live_assistant",
            "auxiliar_assistant_implementation_gate_design_contains_assistant_behavior",
            "auxiliar_assistant_implementation_gate_design_contains_auxiliar_behavior",
            "auxiliar_assistant_implementation_gate_design_contains_copilot_behavior",
            "auxiliar_assistant_implementation_gate_design_contains_assistant_activation",
            "auxiliar_assistant_implementation_gate_design_contains_shadow_activation",
            "auxiliar_assistant_implementation_gate_design_contains_review_evidence_builder",
            "auxiliar_assistant_implementation_gate_design_contains_observation_transformation_execution",
            "auxiliar_assistant_implementation_gate_design_contains_route_comparison",
            "auxiliar_assistant_implementation_gate_design_contains_route_selection",
            "auxiliar_assistant_implementation_gate_design_contains_runtime_integration",
            "auxiliar_assistant_implementation_gate_design_contains_router_authority",
            "auxiliar_assistant_implementation_gate_design_contains_prompt_loading",
            "auxiliar_assistant_implementation_gate_design_contains_file_io",
            "auxiliar_assistant_implementation_gate_design_contains_persistence",
            "auxiliar_assistant_implementation_gate_design_contains_report_writer",
            "auxiliar_assistant_implementation_gate_design_contains_review_queue_writer",
            "auxiliar_assistant_implementation_gate_design_contains_human_decision_recording",
            "auxiliar_assistant_implementation_gate_design_contains_gold_or_registry_mutation",
            "auxiliar_assistant_implementation_gate_design_contains_candidate_promotion",
            "auxiliar_assistant_implementation_gate_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m29_points_to_m30_and_m30_points_to_m31_non_runtime_implementation(self):
        self.assertEqual(
            M29_NEXT_ALLOWED_MILESTONE,
            "M30 - Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1",
        )
        design = build_auxiliar_assistant_implementation_gate_design()
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_gate_record_is_immutable_static_and_design_only(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        second = build_auxiliar_assistant_implementation_gate_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        with self.assertRaises(FrozenInstanceError):
            design.allowed_gate_outcomes[0].outcome_id = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M30")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_live_implementation_gate_execution")
        self.assertEqual(design.gate_design_status, "static_gate_design_only_no_callable_gate_entrypoint")
        self.assertEqual(design.live_gate_execution_status, "not_implemented")
        self.assertEqual(design.assistance_implementation_status, "not_implemented")
        self.assertEqual(design.assistant_behavior_status, "not_started")
        self.assertEqual(design.shadow_mode_status, "not_active")
        self.assertEqual(design.runtime_authority_status, "not_granted")

    def test_allowed_gate_outcomes_do_not_grant_implementation_authority(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        outcome_ids = {outcome.outcome_id for outcome in design.allowed_gate_outcomes}
        self.assertEqual(outcome_ids, {"blocked", "not_blocked_for_separate_human_review"})
        for outcome in design.allowed_gate_outcomes:
            self.assertIn("human", outcome.allowed_use)
            self.assertIn("Must not", outcome.blocked_interpretation)
            self.assertNotIn("permission to implement automatically", outcome.allowed_use)

    def test_required_prior_milestones_and_gate_criteria_preserve_m29_skeleton(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        self.assertIn("m29_auxiliar_assistant_assistance_skeleton_design_frozen", design.required_preconditions)
        criterion_ids = self._criterion_ids(design.required_frozen_milestone_criteria)
        for expected in (
            "m18_to_m22_shadow_design_chain_confirmed",
            "m23_to_m25_shadow_transition_chain_confirmed",
            "m26_auxiliar_assistant_boundary_freeze_confirmed",
            "m27_auxiliar_assistant_io_contract_freeze_confirmed",
            "m28_auxiliar_assistant_contract_validator_freeze_confirmed",
            "m29_auxiliar_assistant_assistance_skeleton_freeze_confirmed",
        ):
            self.assertIn(expected, criterion_ids)

    def test_boundary_failure_and_human_review_criteria_block_authority_leaks(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        critical_ids = self._criterion_ids(design.critical_boundary_failure_criteria)
        for expected in (
            "runtime_import_boundary_clean",
            "side_effect_boundary_clean",
            "authority_boundary_clean",
            "assistant_activation_boundary_clean",
            "future_assistance_scope_boundary_clean",
        ):
            self.assertIn(expected, critical_ids)
        human_ids = self._criterion_ids(design.human_review_criteria)
        for expected in (
            "human_confirms_m31_scope_separately",
            "validation_evidence_reviewed",
            "freeze_context_reviewed",
        ):
            self.assertIn(expected, human_ids)

    def test_later_m31_constraints_remain_non_runtime_in_memory_only(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        later_ids = self._criterion_ids(design.later_m31_constraints)
        for expected in (
            "m31_may_be_non_runtime_only",
            "m31_may_use_validated_primitives_only",
            "m31_must_follow_m29_skeleton_slots",
            "m31_may_return_one_non_authoritative_assistance_record",
        ):
            self.assertIn(expected, later_ids)
        for criterion in design.later_m31_constraints:
            self.assertNotIn("authority granted", criterion.required_status)

    def test_forbidden_behaviors_and_invariants_preserve_design_only_gate(self):
        design = build_auxiliar_assistant_implementation_gate_design()
        for forbidden in (
            "live_implementation_gate_execution",
            "callable_gate_entrypoint",
            "implementation_permission_grant",
            "runtime_state_inspection",
            "freeze_memory_reading",
            "live_assistance_execution",
            "callable_assistance_builder",
            "live_contract_validation_execution",
            "input_processing",
            "output_generation",
            "assistant_behavior",
            "auxiliar_behavior",
            "copilot_behavior",
            "pilot_behavior",
            "assistant_activation",
            "shadow_mode_activation",
            "route_comparison",
            "route_selection",
            "prompt_loading",
            "runtime_integration",
            "router_authority",
            "file_io",
            "persistence",
            "report_writing",
            "review_queue_writing",
            "human_decision_recording",
            "candidate_promotion",
        ):
            self.assertIn(forbidden, design.forbidden_gate_behaviors)
        for invariant in (
            "m30_is_design_only",
            "m30_defines_auxiliar_assistant_implementation_gate_limits_only",
            "m30_has_no_callable_gate_entrypoint",
            "m30_does_not_evaluate_live_project_state",
            "m30_does_not_read_freeze_memory_or_source_files",
            "m30_does_not_authorize_m31_by_itself",
            "m30_does_not_implement_assistance_logic",
            "m30_does_not_process_input_or_generate_output",
            "m30_does_not_compare_or_select_routes",
            "m30_does_not_select_or_load_prompts",
            "m30_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m30_does_not_activate_shadow_mode",
            "m30_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m30_does_not_record_human_decisions",
            "m30_does_not_persist_or_mutate_project_state",
            "future_m31_requires_separate_human_confirmation_after_m30_freeze",
        ):
            self.assertIn(invariant, design.gate_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_auxiliar_assistant_implementation_gate_design"])
        text = MODULE.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_RUNTIME_BEHAVIOR_DEFS:
            self.assertNotIn("def " + forbidden, text)

    def test_module_imports_only_dataclasses_and_typing(self):
        tree = self._module_ast()
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append((node.module or "").split(".")[0])
        self.assertEqual(set(imports), {"__future__", "dataclasses", "typing"})
        self.assertTrue(FORBIDDEN_IMPORTS.isdisjoint(imports))

    def test_module_has_no_side_effect_calls_or_runtime_terms(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, FORBIDDEN_CALLS)
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, FORBIDDEN_CALLS)
        text = MODULE.read_text(encoding="utf-8")
        for forbidden in (
            "requests.",
            "subprocess.",
            "Path(",
            ".write_text(",
            ".read_text(",
            "open(",
            "print(",
        ):
            self.assertNotIn(forbidden, text)

    def test_notes_document_preserves_no_live_gate_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("M30 is design-only", notes)
        self.assertIn("does not implement a live gate", notes)
        self.assertIn("does not activate", notes)
        self.assertIn("M31", notes)


if __name__ == "__main__":
    unittest.main()
