import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
TRANSITION = BOX / "adviser_offline" / "transition_design"
MANIFEST = BOX / "box_manifest.json"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_boundary_design.py"

FEATURE_ID = "routing_signal_scorer_v3_auxiliar_assistant_boundary_design_v1"
SCHEMA_VERSION = "3.67-auxiliar-assistant-boundary-design"
NEXT_ALLOWED_MILESTONE = "M27 - Routing Signal Scorer v3 Auxiliar/Assistant Input Output Contract Design v1"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_assistant_boundary_readiness_gate_design import (  # noqa: E402
    NEXT_ALLOWED_MILESTONE as M25_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_boundary_design import (  # noqa: E402
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    build_auxiliar_assistant_boundary_design,
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
)

FORBIDDEN_AUTHORITY_TERMS = (
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
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_registry",
    "write_freeze",
    "confirm_and_write",
)


class AuxiliarAssistantBoundaryDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m26_auxiliar_assistant_boundary_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_boundary_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_boundary_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_boundary_design_status"],
            "immutable_design_only_assistant_boundary_no_assistant_behavior_no_shadow_activation_no_runtime_authority",
        )
        self.assertEqual(manifest["auxiliar_assistant_boundary_design_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        self.assertTrue(manifest["auxiliar_assistant_boundary_design_requires_m25_readiness_gate_design"])
        for key in (
            "auxiliar_assistant_boundary_design_contains_live_assistant",
            "auxiliar_assistant_boundary_design_contains_assistant_behavior",
            "auxiliar_assistant_boundary_design_contains_auxiliar_behavior",
            "auxiliar_assistant_boundary_design_contains_copilot_behavior",
            "auxiliar_assistant_boundary_design_contains_assistant_activation",
            "auxiliar_assistant_boundary_design_contains_shadow_activation",
            "auxiliar_assistant_boundary_design_contains_readiness_evaluation_execution",
            "auxiliar_assistant_boundary_design_contains_review_evidence_builder",
            "auxiliar_assistant_boundary_design_contains_observation_transformation_execution",
            "auxiliar_assistant_boundary_design_contains_route_comparison",
            "auxiliar_assistant_boundary_design_contains_runtime_integration",
            "auxiliar_assistant_boundary_design_contains_router_authority",
            "auxiliar_assistant_boundary_design_contains_prompt_loading",
            "auxiliar_assistant_boundary_design_contains_file_io",
            "auxiliar_assistant_boundary_design_contains_persistence",
            "auxiliar_assistant_boundary_design_contains_report_writer",
            "auxiliar_assistant_boundary_design_contains_review_queue_writer",
            "auxiliar_assistant_boundary_design_contains_human_decision_recording",
            "auxiliar_assistant_boundary_design_contains_gold_or_registry_mutation",
            "auxiliar_assistant_boundary_design_contains_candidate_promotion",
            "auxiliar_assistant_boundary_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m25_points_to_m26_and_m26_points_to_m27_contract_design(self):
        self.assertEqual(
            M25_NEXT_ALLOWED_MILESTONE,
            "M26 - Routing Signal Scorer v3 Auxiliar/Assistant Boundary Design v1",
        )
        design = build_auxiliar_assistant_boundary_design()
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_design_record_is_immutable_static_and_design_only(self):
        design = build_auxiliar_assistant_boundary_design()
        second = build_auxiliar_assistant_boundary_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M26")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_assistant_behavior")
        self.assertEqual(design.assistant_boundary_design_status, "static_boundary_design_only")
        self.assertEqual(design.assistant_behavior_status, "not_started")
        self.assertEqual(design.shadow_mode_status, "not_active")
        self.assertEqual(design.runtime_authority_status, "not_granted")

    def test_required_prior_milestones_include_m25_and_boundary_roles_are_non_authoritative(self):
        design = build_auxiliar_assistant_boundary_design()
        self.assertIn("m25_assistant_boundary_readiness_gate_design_frozen", design.required_prior_milestones)
        role_ids = {item.role_id for item in design.future_allowed_role_boundaries}
        self.assertEqual(
            role_ids,
            {
                "future_non_authoritative_comparison_reader",
                "future_boundary_question_drafter",
                "future_safety_summary_assistant",
                "future_next_step_clarifier",
            },
        )
        for item in design.future_allowed_role_boundaries:
            text = " ".join((item.role_id, item.allowed_scope, item.required_human_control, item.forbidden_interpretation))
            self.assertIn("human", item.required_human_control)
            for forbidden in FORBIDDEN_AUTHORITY_TERMS:
                self.assertNotIn(forbidden, text)

    def test_authority_rules_keep_assistant_shadow_runtime_and_storage_separate(self):
        design = build_auxiliar_assistant_boundary_design()
        boundary_ids = {rule.boundary_id for rule in design.authority_boundary_rules}
        self.assertEqual(
            boundary_ids,
            {
                "assistant_boundary_is_not_assistant_activation",
                "assistant_boundary_is_not_shadow_activation",
                "assistant_boundary_is_not_router_authority",
                "assistant_boundary_is_not_decision_recording",
                "assistant_boundary_is_not_persistence",
            },
        )
        by_id = {rule.boundary_id: rule for rule in design.authority_boundary_rules}
        self.assertEqual(by_id["assistant_boundary_is_not_assistant_activation"].required_state, "assistant_behavior_not_started")
        self.assertEqual(by_id["assistant_boundary_is_not_shadow_activation"].required_state, "shadow_mode_not_active")
        self.assertEqual(by_id["assistant_boundary_is_not_router_authority"].required_state, "runtime_router_authority_not_granted")

    def test_forbidden_behaviors_and_invariants_preserve_boundaries(self):
        design = build_auxiliar_assistant_boundary_design()
        for forbidden in (
            "live_assistant",
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
            self.assertIn(forbidden, design.forbidden_assistant_boundary_behaviors)
        for invariant in (
            "m26_is_design_only",
            "m26_defines_auxiliar_assistant_boundary_limits_only",
            "m26_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m26_does_not_activate_shadow_mode",
            "m26_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m26_does_not_record_human_decisions",
            "m27_requires_separate_governed_input_output_contract_design",
        ):
            self.assertIn(invariant, design.assistant_boundary_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_auxiliar_assistant_boundary_design"])
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


if __name__ == "__main__":
    unittest.main()
