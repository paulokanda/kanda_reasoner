import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
TRANSITION = BOX / "adviser_offline" / "transition_design"
MANIFEST = BOX / "box_manifest.json"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_contract_validator_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_contract_validator_notes.md"

FEATURE_ID = "routing_signal_scorer_v3_auxiliar_assistant_contract_validator_design_v1"
SCHEMA_VERSION = "3.69-auxiliar-assistant-contract-validator-design"
NEXT_ALLOWED_MILESTONE = "M29 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Skeleton Design v1"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_io_contract_design import (  # noqa: E402
    NEXT_ALLOWED_MILESTONE as M27_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_contract_validator_design import (  # noqa: E402
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    build_auxiliar_assistant_contract_validator_design,
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
)


class AuxiliarAssistantContractValidatorDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _rule_ids(self, rules):
        return {rule.rule_id for rule in rules}

    def test_manifest_declares_m28_auxiliar_assistant_contract_validator_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_contract_validator_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_contract_validator_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_contract_validator_design_status"],
            "immutable_design_only_contract_validator_no_live_validation_no_assistant_behavior_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_contract_validator_design_policy"],
            "future_fail_closed_contract_validator_design_only_no_live_validation_no_assistant_activation_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_contract_validator_design_module"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_contract_validator_design.py",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_contract_validator_design_notes_doc"],
            "kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_contract_validator_notes.md",
        )
        self.assertEqual(manifest["auxiliar_assistant_contract_validator_design_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        for key in (
            "auxiliar_assistant_contract_validator_design_requires_m18_boundary",
            "auxiliar_assistant_contract_validator_design_requires_m19_io_contract",
            "auxiliar_assistant_contract_validator_design_requires_m20_contract_validator_design",
            "auxiliar_assistant_contract_validator_design_requires_m21_observation_skeleton_design",
            "auxiliar_assistant_contract_validator_design_requires_m22_implementation_gate_design",
            "auxiliar_assistant_contract_validator_design_requires_m23_non_runtime_observation",
            "auxiliar_assistant_contract_validator_design_requires_m24_review_evidence_design",
            "auxiliar_assistant_contract_validator_design_requires_m25_readiness_gate_design",
            "auxiliar_assistant_contract_validator_design_requires_m26_auxiliar_assistant_boundary_design",
            "auxiliar_assistant_contract_validator_design_requires_m27_auxiliar_assistant_io_contract_design",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            "auxiliar_assistant_contract_validator_design_contains_live_contract_validation",
            "auxiliar_assistant_contract_validator_design_contains_callable_validator_entrypoint",
            "auxiliar_assistant_contract_validator_design_contains_input_processing",
            "auxiliar_assistant_contract_validator_design_contains_output_generation",
            "auxiliar_assistant_contract_validator_design_contains_live_assistant",
            "auxiliar_assistant_contract_validator_design_contains_assistant_behavior",
            "auxiliar_assistant_contract_validator_design_contains_auxiliar_behavior",
            "auxiliar_assistant_contract_validator_design_contains_copilot_behavior",
            "auxiliar_assistant_contract_validator_design_contains_assistant_activation",
            "auxiliar_assistant_contract_validator_design_contains_shadow_activation",
            "auxiliar_assistant_contract_validator_design_contains_review_evidence_builder",
            "auxiliar_assistant_contract_validator_design_contains_observation_transformation_execution",
            "auxiliar_assistant_contract_validator_design_contains_route_comparison",
            "auxiliar_assistant_contract_validator_design_contains_runtime_integration",
            "auxiliar_assistant_contract_validator_design_contains_router_authority",
            "auxiliar_assistant_contract_validator_design_contains_prompt_loading",
            "auxiliar_assistant_contract_validator_design_contains_file_io",
            "auxiliar_assistant_contract_validator_design_contains_persistence",
            "auxiliar_assistant_contract_validator_design_contains_report_writer",
            "auxiliar_assistant_contract_validator_design_contains_review_queue_writer",
            "auxiliar_assistant_contract_validator_design_contains_human_decision_recording",
            "auxiliar_assistant_contract_validator_design_contains_gold_or_registry_mutation",
            "auxiliar_assistant_contract_validator_design_contains_candidate_promotion",
            "auxiliar_assistant_contract_validator_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m27_points_to_m28_and_m28_points_to_m29_skeleton_design(self):
        self.assertEqual(
            M27_NEXT_ALLOWED_MILESTONE,
            "M28 - Routing Signal Scorer v3 Auxiliar/Assistant Contract Validator Design v1",
        )
        design = build_auxiliar_assistant_contract_validator_design()
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_validator_record_is_immutable_static_and_design_only(self):
        design = build_auxiliar_assistant_contract_validator_design()
        second = build_auxiliar_assistant_contract_validator_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        with self.assertRaises(FrozenInstanceError):
            design.planned_input_validation_rules[0].rule_id = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M28")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_live_contract_validation")
        self.assertEqual(design.validator_design_status, "static_rule_design_only_no_validator_function")
        self.assertEqual(design.live_validation_status, "not_implemented")
        self.assertEqual(design.input_processing_status, "not_implemented")
        self.assertEqual(design.output_generation_status, "not_implemented")
        self.assertEqual(design.assistant_behavior_status, "not_started")
        self.assertEqual(design.shadow_mode_status, "not_active")
        self.assertEqual(design.runtime_authority_status, "not_granted")

    def test_planned_validation_rules_fail_closed_without_executing_validation(self):
        design = build_auxiliar_assistant_contract_validator_design()
        input_rules = self._rule_ids(design.planned_input_validation_rules)
        output_rules = self._rule_ids(design.planned_output_validation_rules)
        for expected in (
            "assistant_input_declared_keys_only",
            "assistant_input_required_fields_present",
            "assistant_input_json_safe_primitives_only",
            "assistant_input_live_objects_rejected",
            "assistant_input_caller_supplied_only",
        ):
            self.assertIn(expected, input_rules)
        for expected in (
            "assistant_output_declared_keys_only",
            "assistant_output_authority_notice_required",
            "assistant_output_no_route_or_prompt_directives",
            "assistant_output_no_activation_or_readiness_claims",
            "assistant_output_no_governed_write_directives",
            "assistant_output_in_memory_non_authoritative_only",
        ):
            self.assertIn(expected, output_rules)
        for rule in design.planned_input_validation_rules + design.planned_output_validation_rules:
            self.assertIn("future_validator_design", rule.default_disposition)
            self.assertTrue(rule.description.startswith("Future"))

    def test_required_prior_milestones_and_fail_closed_boundaries_preserve_m27_contract(self):
        design = build_auxiliar_assistant_contract_validator_design()
        self.assertIn("m27_auxiliar_assistant_input_output_contract_design_frozen", design.required_prior_milestones)
        for boundary_rule in (
            "unknown_input_keys_reject",
            "unknown_output_keys_block",
            "missing_required_input_fields_reject",
            "non_primitive_inputs_reject",
            "live_object_inputs_reject",
            "authority_or_activation_fields_block",
            "governed_write_fields_block",
            "persistence_fields_block",
            "human_decision_recording_fields_block",
            "candidate_promotion_fields_block",
        ):
            self.assertIn(boundary_rule, design.fail_closed_boundary_rules)

    def test_forbidden_behaviors_and_invariants_preserve_design_only_validator(self):
        design = build_auxiliar_assistant_contract_validator_design()
        for forbidden in (
            "live_contract_validation_execution",
            "callable_validator_entrypoint",
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
            self.assertIn(forbidden, design.forbidden_validator_behaviors)
        for invariant in (
            "m28_is_design_only",
            "m28_defines_auxiliar_assistant_contract_validator_limits_only",
            "m28_has_no_callable_validator_entrypoint",
            "m28_does_not_validate_live_payloads",
            "m28_does_not_process_input_or_generate_output",
            "m28_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m28_does_not_activate_shadow_mode",
            "m28_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m28_does_not_record_human_decisions",
            "m28_does_not_persist_or_mutate_project_state",
            "future_validator_must_fail_closed_on_unknown_keys_and_authority_fields",
            "m29_requires_separate_governed_assistance_skeleton_design",
        ):
            self.assertIn(invariant, design.validator_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_auxiliar_assistant_contract_validator_design"])
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

    def test_notes_document_preserves_no_live_validator_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("M28 is design-only", notes)
        self.assertIn("does not implement a live validator", notes)
        self.assertIn("does not activate", notes)
        self.assertIn("M29", notes)


if __name__ == "__main__":
    unittest.main()
