import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    AuxiliarAssistantAssistanceReadinessGatePilotBoundaryDesign,
    PilotBoundaryReadinessBoundaryDesign,
    PilotBoundaryReadinessCriterionDesign,
    build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_assistance_review_evidence_design import (
    NEXT_ALLOWED_MILESTONE as M32_NEXT_ALLOWED_MILESTONE,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_notes.md"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_INIT = BOX / "__init__.py"
RUNTIME_CONTRACT = BOX / "contract.py"

FORBIDDEN_IMPORT_PREFIXES = (
    "os",
    "sys",
    "pathlib",
    "subprocess",
    "socket",
    "threading",
    "multiprocessing",
    "tempfile",
    "importlib",
    "pickle",
    "shelve",
    "sqlite3",
    "logging",
    "requests",
    "httpx",
    "aiohttp",
    "kanda_reasoner_app.routing_signal_scorer.contract",
    "kanda_reasoner_app.routing_signal_scorer.runtime",
    "kanda_reasoner_app.routing_signal_scorer.router",
    "kanda_reasoner_app.prompt_loader",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.project_freeze_ledger",
)

FORBIDDEN_CALLS = (
    "open",
    "print",
    "eval",
    "exec",
    "compile",
    "__import__",
    "getenv",
    "putenv",
    "system",
    "popen",
    "import_module",
)

FORBIDDEN_RUNTIME_BEHAVIOR_DEFS = (
    "run_readiness_gate",
    "execute_readiness_gate",
    "calculate_readiness",
    "evaluate_readiness",
    "build_review_evidence",
    "transform_assistance",
    "validate_live_assistance",
    "compare_routes",
    "select_route",
    "select_prompt",
    "persist_evidence",
    "write_report",
    "write_review_queue",
    "record_human_decision",
    "approve_assistance",
    "reject_assistance",
    "override_route",
    "run_shadow_mode",
    "activate_shadow_mode",
    "activate_assistant",
    "start_assistant",
    "start_auxiliar",
    "start_pilot",
    "start_copilot",
    "integrate_runtime_router",
    "load_prompt",
    "write_gold",
    "write_registry",
    "promote_candidate",
)

FORBIDDEN_BEHAVIOR_MARKERS = (
    "live_readiness_gate",
    "callable_readiness_gate",
    "readiness_evaluation_execution",
    "assistance_review_evidence_building",
    "assistance_review_evidence_validation",
    "assistance_transformation_execution",
    "live_assistance_execution",
    "live_input_validation_execution",
    "route_comparison",
    "route_selection",
    "runtime_state_inspection",
    "runtime_router_import",
    "runtime_router_export",
    "prompt_selection",
    "prompt_loading",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "review_queue_writing",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "human_decision_recording",
    "approval_recording",
    "rejection_recording",
    "override_recording",
    "patch_execution",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
    "shadow_mode_activation",
    "assistant_activation",
    "pilot_activation",
    "copilot_activation",
    "assistant_behavior",
    "auxiliar_behavior",
    "pilot_behavior",
    "copilot_behavior",
)


class AuxiliarAssistantAssistanceReadinessGatePilotBoundaryDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m33_readiness_gate_for_pilot_boundary_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest[f"{prefix}_status"],
            "immutable_design_only_pilot_boundary_readiness_gate_prerequisite_design_no_live_gate_no_pilot_copilot_behavior_no_runtime_authority",
        )
        self.assertEqual(manifest[f"{prefix}_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        for key in (
            f"{prefix}_requires_m18_boundary",
            f"{prefix}_requires_m19_io_contract",
            f"{prefix}_requires_m20_contract_validator_design",
            f"{prefix}_requires_m21_observation_skeleton_design",
            f"{prefix}_requires_m22_implementation_gate_design",
            f"{prefix}_requires_m23_non_runtime_observation",
            f"{prefix}_requires_m24_review_evidence_design",
            f"{prefix}_requires_m25_readiness_gate_design",
            f"{prefix}_requires_m26_auxiliar_assistant_boundary_design",
            f"{prefix}_requires_m27_auxiliar_assistant_io_contract_design",
            f"{prefix}_requires_m28_auxiliar_assistant_contract_validator_design",
            f"{prefix}_requires_m29_auxiliar_assistant_assistance_skeleton_design",
            f"{prefix}_requires_m30_auxiliar_assistant_implementation_gate_design",
            f"{prefix}_requires_m31_non_runtime_auxiliar_assistant_assistance",
            f"{prefix}_requires_m32_assistance_review_evidence_design",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            f"{prefix}_contains_live_readiness_gate",
            f"{prefix}_contains_callable_readiness_gate",
            f"{prefix}_contains_readiness_evaluation_execution",
            f"{prefix}_contains_review_evidence_builder",
            f"{prefix}_contains_assistance_transformation_execution",
            f"{prefix}_contains_live_assistance_execution",
            f"{prefix}_contains_live_input_validation_execution",
            f"{prefix}_contains_route_comparison",
            f"{prefix}_contains_route_selection",
            f"{prefix}_contains_prompt_selection",
            f"{prefix}_contains_prompt_loading",
            f"{prefix}_contains_runtime_integration",
            f"{prefix}_contains_router_authority",
            f"{prefix}_contains_file_io",
            f"{prefix}_contains_persistence",
            f"{prefix}_contains_report_writer",
            f"{prefix}_contains_review_queue_writer",
            f"{prefix}_contains_human_decision_recording",
            f"{prefix}_contains_gold_or_registry_mutation",
            f"{prefix}_contains_candidate_promotion",
            f"{prefix}_contains_embeddings_or_providers",
            f"{prefix}_contains_shadow_activation",
            f"{prefix}_contains_assistant_activation",
            f"{prefix}_contains_pilot_activation",
            f"{prefix}_contains_copilot_activation",
            f"{prefix}_contains_assistant_behavior",
            f"{prefix}_contains_auxiliar_behavior",
            f"{prefix}_contains_pilot_behavior",
            f"{prefix}_contains_copilot_behavior",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m32_points_to_m33_and_m33_points_to_m34(self):
        self.assertEqual(
            M32_NEXT_ALLOWED_MILESTONE,
            "M33 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M34 - Routing Signal Scorer v3 Pilot/Copilot Boundary Design v1",
        )

    def test_returns_static_immutable_design_record(self):
        first = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        second = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        with self.assertRaises(FrozenInstanceError):
            first.milestone = "changed"
        self.assertIsInstance(first, AuxiliarAssistantAssistanceReadinessGatePilotBoundaryDesign)
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M33")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "design_only_no_live_readiness_gate")
        self.assertEqual(first.readiness_gate_design_status, "static_prerequisite_design_only")
        self.assertEqual(first.live_gate_execution_status, "not_implemented")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        self.assertEqual(
            first.implementation_gate,
            "blocked_until_separate_m34_scope_confirmation_validation_and_freeze",
        )

    def test_prerequisites_are_blocking_and_do_not_grant_pilot_authority(self):
        design = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        criterion_ids = {item.criterion_id for item in design.future_pilot_boundary_review_prerequisites}
        self.assertEqual(
            criterion_ids,
            {
                "m32_review_evidence_design_frozen",
                "assistant_branch_remains_non_authoritative",
                "shadow_mode_remains_inactive",
                "pilot_copilot_remain_not_started",
                "runtime_authority_remains_not_granted",
                "m34_scope_requires_explicit_human_confirmation",
                "no_persistence_or_review_decision_bridge",
                "candidate_promotion_remains_blocked",
            },
        )
        for item in design.future_pilot_boundary_review_prerequisites:
            self.assertIsInstance(item, PilotBoundaryReadinessCriterionDesign)
            self.assertTrue(item.blocked_status.startswith("blocked_if"), item)
        boundary_ids = {rule.boundary_id for rule in design.boundary_review_safety_rules}
        self.assertEqual(
            boundary_ids,
            {
                "readiness_gate_is_not_live_gate",
                "pilot_boundary_review_is_not_pilot_or_copilot_behavior",
                "readiness_gate_is_not_assistant_activation",
                "readiness_gate_is_not_promotion",
                "readiness_gate_is_not_router_integration",
            },
        )
        for rule in design.boundary_review_safety_rules:
            self.assertIsInstance(rule, PilotBoundaryReadinessBoundaryDesign)
        by_id = {rule.boundary_id: rule for rule in design.boundary_review_safety_rules}
        self.assertEqual(by_id["readiness_gate_is_not_live_gate"].required_state, "static_design_record_only")
        self.assertEqual(by_id["readiness_gate_is_not_promotion"].required_state, "candidate_promotion_blocked")

    def test_design_requires_m18_through_m32_and_keeps_m34_separate(self):
        design = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        for prior in (
            "m18_shadow_mode_boundary_design_frozen",
            "m19_shadow_mode_input_output_contract_design_frozen",
            "m20_shadow_mode_contract_validator_design_frozen",
            "m21_shadow_mode_observation_skeleton_design_frozen",
            "m22_shadow_mode_implementation_gate_design_frozen",
            "m23_non_runtime_shadow_observation_implementation_frozen",
            "m24_shadow_observation_review_evidence_design_frozen",
            "m25_shadow_mode_assistant_boundary_readiness_gate_design_frozen",
            "m26_auxiliar_assistant_boundary_design_frozen",
            "m27_auxiliar_assistant_input_output_contract_design_frozen",
            "m28_auxiliar_assistant_contract_validator_design_frozen",
            "m29_auxiliar_assistant_assistance_skeleton_design_frozen",
            "m30_auxiliar_assistant_implementation_gate_design_frozen",
            "m31_non_runtime_auxiliar_assistant_assistance_implementation_frozen",
            "m32_auxiliar_assistant_assistance_review_evidence_design_frozen",
        ):
            self.assertIn(prior, design.required_prior_milestones)
        self.assertIn("m34_requires_separate_human_scope_confirmation", design.readiness_gate_invariants)

    def test_forbidden_behaviors_are_explicitly_blocked(self):
        design = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        for forbidden in FORBIDDEN_BEHAVIOR_MARKERS:
            self.assertIn(forbidden, design.forbidden_readiness_gate_behaviors)
        for invariant in (
            "m33_is_design_only",
            "m33_defines_future_m34_pilot_boundary_review_prerequisites_only",
            "m33_has_no_live_readiness_gate",
            "m33_does_not_evaluate_live_assistance_or_review_evidence",
            "m33_does_not_start_auxiliar_assistant_or_pilot_copilot_behavior",
            "m33_does_not_activate_shadow_mode_assistant_pilot_or_copilot",
            "m33_does_not_select_routes_or_prompts",
            "m33_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m33_does_not_persist_or_write_project_state",
            "m33_does_not_record_human_decisions",
            "candidate_promotion_remains_blocked",
            "shadow_mode_remains_inactive",
            "pilot_copilot_remain_not_started",
        ):
            self.assertIn(invariant, design.readiness_gate_invariants)

    def test_module_has_no_runtime_imports_or_forbidden_calls(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertFalse(
                        alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES),
                        f"forbidden import: {alias.name}",
                    )
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self.assertFalse(
                    module.startswith(FORBIDDEN_IMPORT_PREFIXES),
                    f"forbidden import-from: {module}",
                )
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                self.assertNotIn(name, FORBIDDEN_CALLS)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.assertNotIn(node.name, FORBIDDEN_RUNTIME_BEHAVIOR_DEFS)

    def test_runtime_surface_is_not_exported_and_notes_state_design_only(self):
        runtime_text = RUNTIME_INIT.read_text(encoding="utf-8") + RUNTIME_CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn("shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design", runtime_text)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            design = build_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design()
        self.assertEqual(buffer.getvalue(), "")
        self.assertEqual(design.live_gate_execution_status, "not_implemented")
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("design-only", notes)
        self.assertIn("does not", notes)
        self.assertIn("M34 requires", notes)


if __name__ == "__main__":
    unittest.main()
