import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_pilot_copilot_boundary_design import (
    NEXT_ALLOWED_MILESTONE as M34_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_post_adviser_pilot_copilot_handoff_closure_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    HandoffClosureCheckpointDesign,
    HandoffClosureRuleDesign,
    PostAdviserPilotCopilotHandoffClosureDesign,
    build_post_adviser_pilot_copilot_handoff_closure_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_post_adviser_pilot_copilot_handoff_closure_design.py"
NOTES = TRANSITION / "shadow_mode_post_adviser_pilot_copilot_handoff_closure_notes.md"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_INIT = BOX / "__init__.py"
RUNTIME_CONTRACT = BOX / "contract.py"

FORBIDDEN_IMPORT_PREFIXES = (
    "os", "sys", "pathlib", "subprocess", "socket", "threading", "multiprocessing",
    "tempfile", "importlib", "pickle", "shelve", "sqlite3", "logging", "requests", "httpx", "aiohttp",
    "kanda_reasoner_app.routing_signal_scorer.contract",
    "kanda_reasoner_app.routing_signal_scorer.runtime",
    "kanda_reasoner_app.routing_signal_scorer.router",
    "kanda_reasoner_app.prompt_loader",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.project_freeze_ledger",
)

FORBIDDEN_CALLS = (
    "open", "print", "eval", "exec", "compile", "__import__", "getenv", "putenv",
    "system", "popen", "import_module",
)

FORBIDDEN_RUNTIME_BEHAVIOR_DEFS = (
    "run_handoff", "execute_handoff", "run_pilot", "start_pilot", "activate_pilot",
    "run_copilot", "start_copilot", "activate_copilot", "execute_route", "compare_routes",
    "select_route", "override_route", "select_prompt", "load_prompt", "integrate_runtime_router",
    "persist_evidence", "write_report", "write_review_queue", "record_human_decision",
    "approve_assistance", "reject_assistance", "run_shadow_mode", "activate_shadow_mode",
    "activate_assistant", "write_gold", "write_registry", "promote_candidate",
)

FORBIDDEN_BEHAVIOR_MARKERS = (
    "live_pilot_behavior", "live_copilot_behavior", "live_assistant_behavior", "auxiliar_behavior",
    "callable_pilot_runner", "callable_copilot_runner", "callable_handoff_runner",
    "pilot_activation", "copilot_activation", "assistant_activation", "auxiliar_activation",
    "shadow_mode_activation", "automatic_next_milestone", "handoff_execution", "production_enablement",
    "runtime_authority", "runtime_integration", "runtime_state_inspection", "runtime_router_import",
    "runtime_router_export", "route_comparison", "route_selection", "route_override", "route_execution",
    "prompt_selection", "prompt_loading", "source_scanning", "case_discovery", "file_io", "console_io",
    "logging", "persistence", "report_writing", "review_queue_writing", "registry_writing",
    "gold_mutation", "freeze_writing", "human_decision_recording", "approval_recording",
    "rejection_recording", "override_recording", "patch_execution", "provider_or_model_call",
    "embedding_or_vector_index", "network_call", "subprocess_call", "dynamic_import", "candidate_promotion",
)


class PostAdviserPilotCopilotHandoffClosureDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m35_handoff_closure_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "post_adviser_pilot_copilot_handoff_closure_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest[f"{prefix}_status"], "immutable_design_only_post_adviser_bridge_closure_no_activation_no_runtime_authority")
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
            f"{prefix}_requires_m33_pilot_boundary_readiness_gate_design",
            f"{prefix}_requires_m34_pilot_copilot_boundary_design",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            f"{prefix}_contains_live_pilot_behavior",
            f"{prefix}_contains_live_copilot_behavior",
            f"{prefix}_contains_live_assistant_behavior",
            f"{prefix}_contains_auxiliar_behavior",
            f"{prefix}_contains_callable_handoff_runner",
            f"{prefix}_contains_pilot_activation",
            f"{prefix}_contains_copilot_activation",
            f"{prefix}_contains_assistant_activation",
            f"{prefix}_contains_shadow_activation",
            f"{prefix}_contains_route_comparison",
            f"{prefix}_contains_route_selection",
            f"{prefix}_contains_route_execution",
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
        ):
            self.assertIs(manifest[key], False, key)

    def test_m34_points_to_m35_and_m35_has_no_automatic_next_milestone(self):
        self.assertEqual(
            M34_NEXT_ALLOWED_MILESTONE,
            "M35 - Routing Signal Scorer v3 Post-Adviser to Pilot/Copilot Handoff Closure Design v1",
        )
        self.assertIn("NO_AUTOMATIC_NEXT_MILESTONE", NEXT_ALLOWED_MILESTONE)
        self.assertIn("separate governed scope", NEXT_ALLOWED_MILESTONE)

    def test_returns_static_immutable_closure_record(self):
        first = build_post_adviser_pilot_copilot_handoff_closure_design()
        second = build_post_adviser_pilot_copilot_handoff_closure_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        with self.assertRaises(FrozenInstanceError):
            first.milestone = "changed"
        self.assertIsInstance(first, PostAdviserPilotCopilotHandoffClosureDesign)
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M35")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "handoff_closure_design_only_no_activation")
        self.assertEqual(first.closure_status, "post_adviser_bridge_closed_for_design_chain")
        self.assertEqual(first.handoff_status, "future_work_requires_separate_governed_scope")
        self.assertEqual(first.pilot_status, "not_started")
        self.assertEqual(first.copilot_status, "not_started")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        self.assertEqual(first.final_bridge_status, "post_adviser_to_pilot_copilot_bridge_closed_after_m35_validation_and_freeze")

    def test_closure_checkpoints_and_rules_are_non_authoritative(self):
        design = build_post_adviser_pilot_copilot_handoff_closure_design()
        checkpoint_ids = {item.checkpoint_id for item in design.closure_checkpoints}
        self.assertEqual(
            checkpoint_ids,
            {
                "adviser_phase_closed",
                "shadow_mode_bridge_closed",
                "auxiliar_assistant_bridge_closed",
                "pilot_copilot_boundary_closed",
                "future_work_requires_new_scope",
            },
        )
        for item in design.closure_checkpoints:
            self.assertIsInstance(item, HandoffClosureCheckpointDesign)
            self.assertIn("must_not", item.prohibited_interpretation)
        rule_ids = {rule.rule_id for rule in design.closure_rules}
        self.assertEqual(
            rule_ids,
            {
                "closure_is_not_activation",
                "closure_is_not_runtime_authority",
                "closure_is_not_handoff_execution",
                "closure_is_not_prompt_or_route_authority",
                "closure_is_not_write_or_decision_authority",
                "closure_is_not_candidate_promotion",
            },
        )
        for rule in design.closure_rules:
            self.assertIsInstance(rule, HandoffClosureRuleDesign)
        by_id = {rule.rule_id: rule for rule in design.closure_rules}
        self.assertEqual(by_id["closure_is_not_activation"].required_state, "all_activation_not_granted")
        self.assertEqual(by_id["closure_is_not_candidate_promotion"].required_state, "candidate_promotion_blocked")

    def test_design_requires_m18_through_m34_and_closes_bridge(self):
        design = build_post_adviser_pilot_copilot_handoff_closure_design()
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
            "m33_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design_frozen",
            "m34_pilot_copilot_boundary_design_frozen",
        ):
            self.assertIn(prior, design.required_prior_milestones)
        for invariant in (
            "m35_is_design_only",
            "m35_closes_post_adviser_bridge_without_activation",
            "m35_does_not_start_assistant_auxiliar_pilot_or_copilot_behavior",
            "m35_does_not_activate_shadow_mode",
            "m35_does_not_compare_select_override_or_execute_routes",
            "m35_does_not_select_or_load_prompts",
            "m35_does_not_integrate_runtime_router_or_grant_authority",
            "m35_does_not_read_or_write_project_state",
            "m35_does_not_persist_or_write_reports_or_queues",
            "m35_does_not_record_human_decisions",
            "candidate_promotion_remains_blocked",
            "pilot_copilot_remain_not_started",
            "future_work_requires_new_governed_scope",
            "no_automatic_next_milestone_after_m35",
        ):
            self.assertIn(invariant, design.closure_invariants)

    def test_forbidden_behaviors_are_explicitly_blocked(self):
        design = build_post_adviser_pilot_copilot_handoff_closure_design()
        for forbidden in FORBIDDEN_BEHAVIOR_MARKERS:
            self.assertIn(forbidden, design.forbidden_handoff_behaviors)

    def test_module_has_no_runtime_imports_or_forbidden_calls(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertFalse(alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES), f"forbidden import: {alias.name}")
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self.assertFalse(module.startswith(FORBIDDEN_IMPORT_PREFIXES), f"forbidden import-from: {module}")
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
        self.assertNotIn("shadow_mode_post_adviser_pilot_copilot_handoff_closure_design", runtime_text)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            design = build_post_adviser_pilot_copilot_handoff_closure_design()
        self.assertEqual(buffer.getvalue(), "")
        self.assertEqual(design.pilot_status, "not_started")
        self.assertEqual(design.copilot_status, "not_started")
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("design-only", notes)
        self.assertIn("does not", notes)
        self.assertIn("no automatic next milestone", notes)


if __name__ == "__main__":
    unittest.main()
