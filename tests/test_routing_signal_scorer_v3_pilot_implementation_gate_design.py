from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_implementation_gate_design import (
    ACTIVATION_EFFECT,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    FEATURE_ID,
    GATE_DEFAULT_STATE,
    HUMAN_REVIEW_MANDATORY,
    IMPLEMENTATION_AUTHORIZATION_STATUS,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    STORAGE_STATUS,
    get_pilot_implementation_gate_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_implementation_gate_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_implementation_gate_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PilotImplementationGateDesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = get_pilot_implementation_gate_design()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_design_only_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_pilot_implementation_gate_design_v1")
        self.assertEqual(self.design.feature_id, FEATURE_ID)
        self.assertEqual(self.design.schema_version, "3.84-pilot-implementation-gate-design")
        self.assertEqual(self.design.design_kind, "pilot_implementation_gate_design_only")
        self.assertEqual(self.design.milestone, "P7")
        self.assertEqual(self.design.design_status, "design_only")
        self.assertEqual(self.design.gate_evaluation_status, "not_implemented_design_only")
        self.assertEqual(self.design.implementation_authorization_status, "not_granted")
        self.assertEqual(self.design.pilot_candidate_creation_status, "not_implemented")
        self.assertEqual(self.design.callable_pilot_status, "not_implemented")
        self.assertEqual(self.design.live_validation_status, "not_implemented")
        self.assertEqual(self.design.input_processing_status, "not_implemented")
        self.assertEqual(self.design.output_generation_status, "not_implemented")
        self.assertEqual(self.design.route_comparison_status, "not_implemented")
        self.assertEqual(self.design.runtime_authority_status, "not_granted")
        self.assertEqual(self.design.prompt_loading_authority_status, "not_granted")
        self.assertEqual(self.design.persistence_authority_status, "not_granted")

    def test_invariants_are_constant_and_fail_closed(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(GATE_DEFAULT_STATE, "closed_design_only")
        self.assertEqual(IMPLEMENTATION_AUTHORIZATION_STATUS, "not_granted")
        self.assertEqual(self.design.gate_default_state, "closed_design_only")
        self.assertTrue(self.design.human_review_mandatory)
        self.assertTrue(self.design.opt_in_per_invocation_required)
        self.assertEqual(self.design.critical_boundary_error_budget, 0)
        self.assertIn("not approval", self.design.human_review_rule)
        self.assertIn("gate remains closed", self.design.match_before_disagree_rule)

    def test_preconditions_include_complete_p_chain_before_p7(self) -> None:
        required = set(self.design.required_preconditions)
        expected = {
            "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
            "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
            "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
            "p1_pilot_boundary_design_frozen",
            "p2_pilot_input_output_contract_validator_design_frozen",
            "p3_pilot_disagreement_taxonomy_design_frozen",
            "p4_pilot_gold_frozen_router_reproduction_harness_design_frozen",
            "p5_pilot_simulation_skeleton_design_frozen",
            "p6_pilot_review_evidence_design_frozen",
            "kanda_patch_delivery_root_drive_staging_canon_frozen",
            "startup_freeze_context_refreshed_after_p6",
            "freeze_memory_status_ok_after_p6",
        }
        self.assertTrue(expected.issubset(required))
        self.assertIn("P8 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1", self.design.next_allowed_milestone)

    def test_gate_conditions_are_static_and_closed(self) -> None:
        ids = [condition.condition_id for condition in self.design.gate_conditions]
        self.assertEqual(
            ids,
            [
                "prior_freeze_chain_complete",
                "root_drive_installer_canon_preserved",
                "scope_is_non_runtime_pilot_candidate_only",
                "match_before_disagree_preserved",
                "critical_boundary_error_budget_zero",
                "human_review_mandatory_not_approval",
            ],
        )
        for condition in self.design.gate_conditions:
            self.assertIn("blocked", condition.blocked_when_missing.lower())
            self.assertIn("Do not", condition.forbidden_shortcut)
        installer = next(condition for condition in self.design.gate_conditions if condition.condition_id == "root_drive_installer_canon_preserved")
        self.assertIn("Root-Drive ZIP Staging Canon", installer.required_evidence)
        scope = next(condition for condition in self.design.gate_conditions if condition.condition_id == "scope_is_non_runtime_pilot_candidate_only")
        self.assertIn("non-runtime", scope.design_purpose)
        self.assertIn("Copilot", scope.blocked_when_missing)

    def test_gate_stages_require_order_and_fail_closed_language(self) -> None:
        ids = [stage.stage_id for stage in self.design.gate_stages]
        self.assertEqual(
            ids,
            [
                "stage_1_freeze_chain_and_delivery_canon",
                "stage_2_scope_boundary",
                "stage_3_safety_invariants",
            ],
        )
        self.assertEqual([stage.sequence_label for stage in self.design.gate_stages], ["1", "2", "3"])
        for stage in self.design.gate_stages:
            self.assertIn("If", stage.fail_closed_rule)
            self.assertTrue(stage.required_conditions)
        final_stage = self.design.gate_stages[-1]
        self.assertIn("P8 may be designed", final_stage.next_stage_if_later_satisfied)

    def test_forbidden_operations_capture_no_gate_or_runtime_behavior(self) -> None:
        forbidden = set(self.design.forbidden_operations)
        expected = {
            "evaluate_gate",
            "approve_implementation",
            "authorize_pilot",
            "create_pilot_candidate",
            "run_pilot_candidate",
            "activate_pilot",
            "activate_copilot",
            "validate_live_payload",
            "process_input",
            "generate_output",
            "collect_evidence",
            "build_evidence_packet",
            "run_simulation",
            "run_reproduction_harness",
            "load_gold_set",
            "read_freeze_memory",
            "read_prompt_library",
            "inspect_runtime_router",
            "compare_routes",
            "calculate_metric",
            "detect_disagreement",
            "score_disagreement",
            "trust_disagreement",
            "project_route",
            "recommend_route",
            "select_prompt",
            "load_prompt",
            "persist_record",
            "record_human_decision",
            "record_approval",
            "train_from_gate",
            "run_batch_mode",
            "activate_limited_shadow_runtime",
            "promote_candidate",
            "call_provider",
            "use_embeddings",
        }
        self.assertTrue(expected.issubset(forbidden))

    def test_source_and_notes_explicitly_forbid_implementation_effects(self) -> None:
        required_phrases = [
            "P7 defines static fail-closed gate conditions",
            "It does not evaluate a gate",
            "P7 is not the Pilot implementation",
            "no gate evaluation",
            "no implementation approval",
            "no Pilot candidate creation",
            "no callable Pilot",
            "no runtime authority",
            "P8 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_no_forbidden_import_or_io_patterns(self) -> None:
        forbidden_source_patterns = [
            "open(",
            "Path(",
            ".read_text(",
            ".write_text(",
            "json.load",
            "json.dump",
            "pickle",
            "sqlite",
            "requests",
            "subprocess",
            "os.environ",
            "importlib",
            "entry_points",
        ]
        for pattern in forbidden_source_patterns:
            self.assertNotIn(pattern, self.source)

    def test_no_callable_runtime_verbs_are_defined(self) -> None:
        forbidden_defs = [
            "def evaluate_",
            "def approve_",
            "def authorize_",
            "def create_pilot",
            "def implement_",
            "def validate_",
            "def process_",
            "def generate_",
            "def collect_",
            "def build_",
            "def run_",
            "def execute_",
            "def load_",
            "def read_",
            "def inspect_",
            "def compare_",
            "def calculate_",
            "def detect_",
            "def score_",
            "def trust_",
            "def project_",
            "def recommend_",
            "def select_",
            "def write_",
            "def persist_",
            "def record_",
            "class PilotRunner",
            "class CopilotRunner",
            "class PilotSimulator",
            "class ImplementationGateRunner",
        ]
        for pattern in forbidden_defs:
            self.assertNotIn(pattern, self.source)

    def test_manifest_records_p7_and_false_runtime_flags(self) -> None:
        prefix = "pilot_implementation_gate_design"
        self.assertEqual(self.manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(self.manifest[f"{prefix}_schema_version"], "3.84-pilot-implementation-gate-design")
        self.assertTrue(self.manifest[f"{prefix}_requires_p6_review_evidence_design"])
        self.assertTrue(self.manifest[f"{prefix}_requires_root_drive_staging_canon"])
        self.assertEqual(self.manifest[f"{prefix}_routing_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_prompt_loading_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_runtime_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_activation_effect"], "none")
        self.assertTrue(self.manifest[f"{prefix}_human_review_mandatory"])
        self.assertTrue(self.manifest[f"{prefix}_opt_in_per_invocation_required"])
        self.assertEqual(self.manifest[f"{prefix}_critical_boundary_error_budget"], 0)
        self.assertEqual(self.manifest[f"{prefix}_gate_default_state"], "closed_design_only")
        self.assertEqual(self.manifest[f"{prefix}_implementation_authorization_status"], "not_granted")
        false_flags = [
            "contains_gate_evaluation",
            "contains_implementation_approval",
            "contains_pilot_candidate_creation",
            "contains_callable_pilot",
            "contains_live_validation",
            "contains_input_processing",
            "contains_output_generation",
            "contains_route_comparison_execution",
            "contains_metric_calculation",
            "contains_human_decision_recording",
            "contains_approval_recording",
            "contains_disagreement_trust",
            "contains_disagreement_detector",
            "contains_projection_implementation",
            "contains_prompt_loading",
            "contains_prompt_selection",
            "contains_persistence",
            "contains_batch_mode",
            "contains_limited_shadow_runtime",
            "contains_router_authority",
        ]
        for flag in false_flags:
            self.assertFalse(self.manifest[f"{prefix}_{flag}"], flag)

    def test_protected_architecture_characteristics_include_p7(self) -> None:
        chars = set(self.manifest["protected_architecture_characteristics"])
        expected = {
            "pilot_implementation_gate_design",
            "pilot_p7_design_only_no_gate_evaluation",
            "pilot_p7_no_implementation_authorization",
            "pilot_p7_no_pilot_candidate_creation",
            "pilot_p7_gate_default_closed",
            "pilot_p7_next_scope_non_runtime_pilot_candidate_only",
            "pilot_p7_match_before_disagree_preserved",
            "pilot_p7_critical_boundary_error_budget_zero",
            "pilot_no_projection_from_p7",
            "pilot_no_prompt_loading_from_p7",
            "pilot_no_runtime_authority_from_p7",
        }
        self.assertTrue(expected.issubset(chars))

    def test_p7_is_not_pilot_implementation_copilot_or_runtime_shadow(self) -> None:
        forbidden_claims = [
            "activate Copilot",
            "Limited Shadow Runtime implementation",
            "runtime authority granted",
            "auto-approve",
            "automatic approval",
            "training dataset",
            "batch execution granted",
            "Pilot implementation is complete",
        ]
        for phrase in forbidden_claims:
            self.assertNotIn(phrase, self.combined)


if __name__ == "__main__":
    unittest.main()
