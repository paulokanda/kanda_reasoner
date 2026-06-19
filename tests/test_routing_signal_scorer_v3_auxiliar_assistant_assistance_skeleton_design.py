import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
TRANSITION = BOX / "adviser_offline" / "transition_design"
MANIFEST = BOX / "box_manifest.json"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_skeleton_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_skeleton_notes.md"

FEATURE_ID = "routing_signal_scorer_v3_auxiliar_assistant_assistance_skeleton_design_v1"
SCHEMA_VERSION = "3.70-auxiliar-assistant-assistance-skeleton-design"
NEXT_ALLOWED_MILESTONE = "M30 - Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_contract_validator_design import (  # noqa: E402
    NEXT_ALLOWED_MILESTONE as M28_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_assistance_skeleton_design import (  # noqa: E402
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    build_auxiliar_assistant_assistance_skeleton_design,
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


class AuxiliarAssistantAssistanceSkeletonDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _slot_ids(self, slots):
        return {slot.slot_id for slot in slots}

    def test_manifest_declares_m29_auxiliar_assistant_assistance_skeleton_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_assistance_skeleton_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_assistance_skeleton_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_assistance_skeleton_design_status"],
            "immutable_design_only_assistance_skeleton_no_live_assistance_no_assistant_behavior_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_assistance_skeleton_design_policy"],
            "future_non_authoritative_assistance_skeleton_design_only_no_assistant_activation_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_assistance_skeleton_design_module"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_assistance_skeleton_design.py",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_assistance_skeleton_design_notes_doc"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_assistance_skeleton_notes.md",
        )
        self.assertEqual(manifest["auxiliar_assistant_assistance_skeleton_design_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        for key in (
            "auxiliar_assistant_assistance_skeleton_design_requires_m18_boundary",
            "auxiliar_assistant_assistance_skeleton_design_requires_m19_io_contract",
            "auxiliar_assistant_assistance_skeleton_design_requires_m20_contract_validator_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m21_observation_skeleton_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m22_implementation_gate_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m23_non_runtime_observation",
            "auxiliar_assistant_assistance_skeleton_design_requires_m24_review_evidence_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m25_readiness_gate_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m26_auxiliar_assistant_boundary_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m27_auxiliar_assistant_io_contract_design",
            "auxiliar_assistant_assistance_skeleton_design_requires_m28_auxiliar_assistant_contract_validator_design",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            "auxiliar_assistant_assistance_skeleton_design_contains_live_assistance_execution",
            "auxiliar_assistant_assistance_skeleton_design_contains_callable_assistance_builder",
            "auxiliar_assistant_assistance_skeleton_design_contains_live_contract_validation",
            "auxiliar_assistant_assistance_skeleton_design_contains_input_processing",
            "auxiliar_assistant_assistance_skeleton_design_contains_output_generation",
            "auxiliar_assistant_assistance_skeleton_design_contains_live_assistant",
            "auxiliar_assistant_assistance_skeleton_design_contains_assistant_behavior",
            "auxiliar_assistant_assistance_skeleton_design_contains_auxiliar_behavior",
            "auxiliar_assistant_assistance_skeleton_design_contains_copilot_behavior",
            "auxiliar_assistant_assistance_skeleton_design_contains_assistant_activation",
            "auxiliar_assistant_assistance_skeleton_design_contains_shadow_activation",
            "auxiliar_assistant_assistance_skeleton_design_contains_review_evidence_builder",
            "auxiliar_assistant_assistance_skeleton_design_contains_observation_transformation_execution",
            "auxiliar_assistant_assistance_skeleton_design_contains_route_comparison",
            "auxiliar_assistant_assistance_skeleton_design_contains_route_selection",
            "auxiliar_assistant_assistance_skeleton_design_contains_runtime_integration",
            "auxiliar_assistant_assistance_skeleton_design_contains_router_authority",
            "auxiliar_assistant_assistance_skeleton_design_contains_prompt_loading",
            "auxiliar_assistant_assistance_skeleton_design_contains_file_io",
            "auxiliar_assistant_assistance_skeleton_design_contains_persistence",
            "auxiliar_assistant_assistance_skeleton_design_contains_report_writer",
            "auxiliar_assistant_assistance_skeleton_design_contains_review_queue_writer",
            "auxiliar_assistant_assistance_skeleton_design_contains_human_decision_recording",
            "auxiliar_assistant_assistance_skeleton_design_contains_gold_or_registry_mutation",
            "auxiliar_assistant_assistance_skeleton_design_contains_candidate_promotion",
            "auxiliar_assistant_assistance_skeleton_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m28_points_to_m29_and_m29_points_to_m30_gate_design(self):
        self.assertEqual(
            M28_NEXT_ALLOWED_MILESTONE,
            "M29 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Skeleton Design v1",
        )
        design = build_auxiliar_assistant_assistance_skeleton_design()
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_skeleton_record_is_immutable_static_and_design_only(self):
        design = build_auxiliar_assistant_assistance_skeleton_design()
        second = build_auxiliar_assistant_assistance_skeleton_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        with self.assertRaises(FrozenInstanceError):
            design.future_assistance_slots[0].slot_id = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M29")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_live_assistance_execution")
        self.assertEqual(design.skeleton_design_status, "static_slot_design_only_no_assistance_builder")
        self.assertEqual(design.live_assistance_status, "not_implemented")
        self.assertEqual(design.input_processing_status, "not_implemented")
        self.assertEqual(design.output_generation_status, "not_implemented")
        self.assertEqual(design.live_validation_status, "not_implemented")
        self.assertEqual(design.assistant_behavior_status, "not_started")
        self.assertEqual(design.shadow_mode_status, "not_active")
        self.assertEqual(design.runtime_authority_status, "not_granted")

    def test_future_assistance_slots_are_non_authoritative_placeholders_only(self):
        design = build_auxiliar_assistant_assistance_skeleton_design()
        slot_ids = self._slot_ids(design.future_assistance_slots)
        for expected in (
            "future_validated_assistant_input_reference",
            "future_validated_assistant_contract_version_reference",
            "future_non_authoritative_assistance_placeholder",
            "future_human_review_required_marker",
            "future_no_action_taken_authority_marker",
        ):
            self.assertIn(expected, slot_ids)
        for slot in design.future_assistance_slots:
            self.assertIn("no_", slot.blocked_use)
            self.assertTrue(slot.description.startswith("Future"))

    def test_required_prior_milestones_and_guardrails_preserve_m28_validator_design(self):
        design = build_auxiliar_assistant_assistance_skeleton_design()
        self.assertIn("m28_auxiliar_assistant_contract_validator_design_frozen", design.required_prior_milestones)
        for guardrail in (
            "guardrail_assistance_is_non_authoritative_human_review_support_only",
            "guardrail_router_authority_not_granted",
            "guardrail_prompt_loading_not_granted",
            "guardrail_runtime_integration_not_granted",
            "guardrail_shadow_mode_activation_not_granted",
            "guardrail_assistant_activation_not_granted",
            "guardrail_no_human_decision_recording",
            "guardrail_no_persistence_or_report_writing",
            "guardrail_no_gold_registry_or_review_queue_mutation",
            "guardrail_no_candidate_promotion",
        ):
            self.assertIn(guardrail, design.required_future_guardrails)

    def test_forbidden_behaviors_and_invariants_preserve_design_only_skeleton(self):
        design = build_auxiliar_assistant_assistance_skeleton_design()
        for forbidden in (
            "live_assistance_execution",
            "callable_assistance_builder",
            "live_contract_validation_execution",
            "live_input_processing",
            "live_output_generation",
            "assistant_behavior",
            "auxiliar_behavior",
            "copilot_behavior",
            "pilot_behavior",
            "assistant_activation",
            "shadow_mode_activation",
            "observation_transformation",
            "review_evidence_builder",
            "route_comparison_execution",
            "route_selection",
            "prompt_loading",
            "runtime_router_import",
            "persistence",
            "report_writing",
            "review_queue_writing",
            "human_decision_recording",
            "candidate_promotion",
        ):
            self.assertIn(forbidden, design.forbidden_skeleton_behaviors)
        for invariant in (
            "m29_is_design_only",
            "m29_defines_auxiliar_assistant_assistance_skeleton_limits_only",
            "m29_has_no_callable_assistance_builder",
            "m29_does_not_validate_live_contracts",
            "m29_does_not_process_input_or_generate_output",
            "m29_does_not_compare_or_select_routes",
            "m29_does_not_select_or_load_prompts",
            "m29_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m29_does_not_activate_shadow_mode",
            "m29_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m29_does_not_record_human_decisions",
            "m29_does_not_persist_or_mutate_project_state",
            "future_assistance_must_remain_non_authoritative_human_review_support_only",
            "m30_requires_separate_governed_implementation_gate_design",
        ):
            self.assertIn(invariant, design.skeleton_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_auxiliar_assistant_assistance_skeleton_design"])
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

    def test_notes_document_preserves_no_live_assistance_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("M29 is design-only", notes)
        self.assertIn("does not implement a live assistance builder", notes)
        self.assertIn("does not activate", notes)
        self.assertIn("M30", notes)


if __name__ == "__main__":
    unittest.main()
