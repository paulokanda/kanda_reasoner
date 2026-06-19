import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
TRANSITION = BOX / "adviser_offline" / "transition_design"
MANIFEST = BOX / "box_manifest.json"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_io_contract_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_io_contract_notes.md"

FEATURE_ID = "routing_signal_scorer_v3_auxiliar_assistant_io_contract_design_v1"
SCHEMA_VERSION = "3.68-auxiliar-assistant-io-contract-design"
NEXT_ALLOWED_MILESTONE = "M28 - Routing Signal Scorer v3 Auxiliar/Assistant Contract Validator Design v1"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_boundary_design import (  # noqa: E402
    NEXT_ALLOWED_MILESTONE as M26_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_io_contract_design import (  # noqa: E402
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    build_auxiliar_assistant_io_contract_design,
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

FORBIDDEN_AUTHORITY_FIELD_NAMES = (
    "final_route",
    "route_override",
    "selected_route",
    "selected_prompt",
    "prompt_to_load",
    "approved",
    "rejected",
    "overridden",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "auxiliar_ready",
    "candidate_promoted",
    "promotion_ready",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_registry",
    "write_freeze",
    "confirm_and_write",
    "router_authority_granted",
    "runtime_effect",
)


class AuxiliarAssistantIOContractDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _field_names(self, fields):
        return {field.name for field in fields}

    def test_manifest_declares_m27_auxiliar_assistant_io_contract_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_io_contract_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_io_contract_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_io_contract_design_status"],
            "immutable_design_only_io_contract_no_processing_no_generation_no_assistant_behavior_no_runtime_authority",
        )
        self.assertEqual(manifest["auxiliar_assistant_io_contract_design_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        self.assertTrue(manifest["auxiliar_assistant_io_contract_design_requires_m26_auxiliar_assistant_boundary_design"])
        for key in (
            "auxiliar_assistant_io_contract_design_contains_input_processing",
            "auxiliar_assistant_io_contract_design_contains_output_generation",
            "auxiliar_assistant_io_contract_design_contains_live_contract_validation",
            "auxiliar_assistant_io_contract_design_contains_live_assistant",
            "auxiliar_assistant_io_contract_design_contains_assistant_behavior",
            "auxiliar_assistant_io_contract_design_contains_auxiliar_behavior",
            "auxiliar_assistant_io_contract_design_contains_copilot_behavior",
            "auxiliar_assistant_io_contract_design_contains_assistant_activation",
            "auxiliar_assistant_io_contract_design_contains_shadow_activation",
            "auxiliar_assistant_io_contract_design_contains_review_evidence_builder",
            "auxiliar_assistant_io_contract_design_contains_observation_transformation_execution",
            "auxiliar_assistant_io_contract_design_contains_route_comparison",
            "auxiliar_assistant_io_contract_design_contains_runtime_integration",
            "auxiliar_assistant_io_contract_design_contains_router_authority",
            "auxiliar_assistant_io_contract_design_contains_prompt_loading",
            "auxiliar_assistant_io_contract_design_contains_file_io",
            "auxiliar_assistant_io_contract_design_contains_persistence",
            "auxiliar_assistant_io_contract_design_contains_report_writer",
            "auxiliar_assistant_io_contract_design_contains_review_queue_writer",
            "auxiliar_assistant_io_contract_design_contains_human_decision_recording",
            "auxiliar_assistant_io_contract_design_contains_gold_or_registry_mutation",
            "auxiliar_assistant_io_contract_design_contains_candidate_promotion",
            "auxiliar_assistant_io_contract_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m26_points_to_m27_and_m27_points_to_m28_validator_design(self):
        self.assertEqual(
            M26_NEXT_ALLOWED_MILESTONE,
            "M27 - Routing Signal Scorer v3 Auxiliar/Assistant Input Output Contract Design v1",
        )
        design = build_auxiliar_assistant_io_contract_design()
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_contract_record_is_immutable_static_and_design_only(self):
        design = build_auxiliar_assistant_io_contract_design()
        second = build_auxiliar_assistant_io_contract_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        with self.assertRaises(FrozenInstanceError):
            design.allowed_input_fields[0].name = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M27")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_assistant_behavior")
        self.assertEqual(design.input_contract_status, "static_schema_design_only_no_input_processing")
        self.assertEqual(design.output_contract_status, "static_schema_design_only_no_output_generation")
        self.assertEqual(design.validator_status, "not_implemented_deferred_to_m28")
        self.assertEqual(design.assistant_behavior_status, "not_started")
        self.assertEqual(design.shadow_mode_status, "not_active")
        self.assertEqual(design.runtime_authority_status, "not_granted")

    def test_contract_fields_define_future_schema_without_processing_or_authority(self):
        design = build_auxiliar_assistant_io_contract_design()
        input_names = self._field_names(design.allowed_input_fields)
        output_names = self._field_names(design.allowed_output_fields)
        for expected in (
            "assistant_case_id",
            "boundary_context_summary",
            "validated_shadow_observation_summary",
            "review_evidence_summary",
            "current_router_outcome_summary",
            "requested_support_kind",
            "caller_generated_timestamp_utc",
        ):
            self.assertIn(expected, input_names)
        for expected in (
            "assistance_record_kind",
            "assistant_case_id",
            "contract_schema_version",
            "authority_notice",
            "human_review_context_summary",
            "boundary_questions_for_human_review",
            "safety_flags_for_human_review",
            "missing_information_summary",
            "requires_separate_human_review",
            "storage_status",
            "routing_effect",
            "prompt_loading_effect",
            "assistant_activation_effect",
        ):
            self.assertIn(expected, output_names)
        for forbidden in FORBIDDEN_AUTHORITY_FIELD_NAMES:
            self.assertNotIn(forbidden, input_names)
            self.assertNotIn(forbidden, output_names)
        self.assertTrue(set(FORBIDDEN_AUTHORITY_FIELD_NAMES).issubset(set(design.forbidden_output_fields)))
        for field in design.allowed_input_fields:
            self.assertIn("caller_supplied", field.allowed_status)
            self.assertIn("must_not", field.forbidden_use)
        for field in design.allowed_output_fields:
            self.assertIn("must_not", field.forbidden_use)

    def test_required_prior_milestones_and_guardrails_preserve_m26_boundary(self):
        design = build_auxiliar_assistant_io_contract_design()
        self.assertIn("m26_auxiliar_assistant_boundary_design_frozen", design.required_prior_milestones)
        for guardrail in (
            "guardrail_contract_is_not_assistant_behavior",
            "guardrail_contract_is_not_shadow_activation",
            "guardrail_contract_is_not_router_authority",
            "guardrail_contract_is_not_prompt_loading",
            "guardrail_contract_is_not_persistence_or_report_writing",
            "guardrail_contract_requires_separate_human_review",
            "guardrail_contract_blocks_decision_recording_fields",
            "guardrail_contract_blocks_candidate_promotion_fields",
        ):
            self.assertIn(guardrail, design.required_future_contract_guardrails)

    def test_forbidden_behaviors_and_invariants_preserve_design_only_contract(self):
        design = build_auxiliar_assistant_io_contract_design()
        for forbidden in (
            "live_input_processing",
            "live_output_generation",
            "live_contract_validation",
            "assistant_behavior",
            "auxiliar_behavior",
            "copilot_behavior",
            "assistant_activation",
            "shadow_mode_activation",
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
            self.assertIn(forbidden, design.forbidden_contract_behaviors)
        for invariant in (
            "m27_is_design_only",
            "m27_defines_auxiliar_assistant_io_contract_limits_only",
            "m27_does_not_process_input_or_generate_output",
            "m27_does_not_validate_live_payloads",
            "m27_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m27_does_not_activate_shadow_mode",
            "m27_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m27_does_not_record_human_decisions",
            "m28_requires_separate_governed_contract_validator_design",
        ):
            self.assertIn(invariant, design.contract_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_auxiliar_assistant_io_contract_design"])
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

    def test_notes_document_preserves_no_activation_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("M27 is design-only", notes)
        self.assertIn("does not implement live input processing", notes)
        self.assertIn("does not activate", notes)
        self.assertIn("M28", notes)


if __name__ == "__main__":
    unittest.main()
