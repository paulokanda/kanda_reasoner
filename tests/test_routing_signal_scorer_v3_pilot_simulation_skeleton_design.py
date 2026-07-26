from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_simulation_skeleton_design import (
    ACTIVATION_EFFECT,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    FEATURE_ID,
    HUMAN_REVIEW_MANDATORY,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    STORAGE_STATUS,
    get_pilot_simulation_skeleton_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_simulation_skeleton_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_simulation_skeleton_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PilotSimulationSkeletonDesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = get_pilot_simulation_skeleton_design()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_design_only_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_pilot_simulation_skeleton_design_v1")
        self.assertEqual(self.design.feature_id, FEATURE_ID)
        self.assertEqual(self.design.schema_version, "3.82-pilot-simulation-skeleton-design")
        self.assertEqual(self.design.design_kind, "pilot_simulation_skeleton_design_only")
        self.assertEqual(self.design.milestone, "P5")
        self.assertEqual(self.design.design_status, "design_only")
        self.assertEqual(self.design.simulation_status, "not_implemented_design_only")
        self.assertEqual(self.design.callable_simulator_status, "not_implemented")
        self.assertEqual(self.design.live_validation_status, "not_implemented")
        self.assertEqual(self.design.input_processing_status, "not_implemented")
        self.assertEqual(self.design.output_generation_status, "not_implemented")
        self.assertEqual(self.design.route_comparison_status, "not_implemented")
        self.assertEqual(self.design.projection_status, "not_implemented")
        self.assertEqual(self.design.report_generation_status, "not_implemented")

    def test_fixed_non_authority_invariants(self) -> None:
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(self.design.storage_status, "in_memory_only")
        self.assertTrue(self.design.human_review_mandatory)
        self.assertTrue(self.design.opt_in_per_invocation_required)
        self.assertEqual(self.design.critical_boundary_error_budget, 0)
        self.assertEqual(self.design.runtime_authority_status, "not_granted")
        self.assertEqual(self.design.prompt_loading_authority_status, "not_granted")
        self.assertEqual(self.design.persistence_authority_status, "not_granted")
        self.assertEqual(self.design.training_data_use_status, "forbidden")
        self.assertEqual(self.design.batch_mode_status, "forbidden")
        self.assertEqual(self.design.limited_shadow_runtime_status, "forbidden")

    def test_required_preconditions_and_next_milestone(self) -> None:
        required = set(self.design.required_preconditions)
        for item in (
            "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
            "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
            "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
            "p1_pilot_boundary_design_frozen",
            "p2_pilot_input_output_contract_validator_design_frozen",
            "p3_pilot_disagreement_taxonomy_design_frozen",
            "p4_pilot_gold_frozen_router_reproduction_harness_design_frozen",
            "kanda_patch_delivery_root_drive_staging_canon_frozen",
            "startup_freeze_context_refreshed_after_p4",
            "freeze_memory_status_ok_after_p4",
        ):
            self.assertIn(item, required)
        self.assertIn("P6", self.design.next_allowed_milestone)
        self.assertIn("FREEZE_MEMORY_STATUS OK", self.design.next_allowed_milestone)

    def test_skeleton_slots_are_inert_placeholders(self) -> None:
        slots = self.design.skeleton_slots
        self.assertEqual(len(slots), 6)
        ids = {slot.slot_id for slot in slots}
        for expected in (
            "invocation_envelope_placeholder",
            "contract_snapshot_placeholder",
            "reproduction_evidence_placeholder",
            "taxonomy_language_placeholder",
            "human_review_packet_placeholder",
            "critical_boundary_blocker_placeholder",
        ):
            self.assertIn(expected, ids)
        for slot in slots:
            self.assertIn("placeholder", slot.slot_id)
            self.assertIn("No ", slot.forbidden_operation)
            self.assertIn("P5", slot.inert_placeholder_output)
            self.assertIn("gate", slot.required_gate_before_use.lower())

    def test_stage_designs_preserve_order_and_human_review(self) -> None:
        stages = self.design.stage_designs
        self.assertEqual([stage.sequence_label for stage in stages], ["1", "2", "3", "4", "5"])
        ids = {stage.stage_id for stage in stages}
        self.assertIn("stage_1_opt_in_context_design", ids)
        self.assertIn("stage_3_reproduction_gate_design", ids)
        self.assertIn("stage_5_review_packet_design", ids)
        for stage in stages:
            self.assertIn("Human reviewer", stage.human_review_requirement)
            self.assertIn("block", stage.fail_closed_condition.lower())

    def test_forbidden_operations_include_all_simulation_and_authority_paths(self) -> None:
        forbidden = set(self.design.forbidden_operations)
        for op in (
            "run_simulation",
            "execute_simulation_stage",
            "build_simulation_record",
            "validate_live_payload",
            "process_input",
            "generate_output",
            "transform_observation",
            "load_gold_set",
            "read_freeze_memory",
            "read_prompt_library",
            "inspect_runtime_router",
            "compare_routes",
            "calculate_score",
            "certify_reproduction",
            "trust_disagreement_label",
            "detect_disagreement",
            "score_disagreement",
            "project_route",
            "recommend_route",
            "select_route",
            "select_prompt",
            "load_prompt",
            "write_report",
            "write_review_queue",
            "persist_simulation_record",
            "record_human_decision",
            "train_from_simulation",
            "run_batch_mode",
            "activate_limited_shadow_runtime",
            "promote_candidate",
            "call_provider",
            "use_embeddings",
        ):
            self.assertIn(op, forbidden)

    def test_no_callable_runtime_implementation_names_are_added(self) -> None:
        forbidden_snippets = (
            "def validate_",
            "def run_",
            "def execute_",
            "def process_",
            "def generate_",
            "def compare_",
            "def score_",
            "def project_",
            "def select_",
            "open(",
            "Path(",
            "json.dump",
            "write_text(",
            "requests.",
            "subprocess.",
        )
        for snippet in forbidden_snippets:
            self.assertNotIn(snippet, self.source)

    def test_forbidden_prompt_loading_leakage_names_are_absent(self) -> None:
        p5_only = "\n".join([self.source, self.notes])
        for forbidden in (
            "candidate_prompt_groups",
            "simulated_required_prompt_groups",
            "required_prompt_groups",
            "requires_human_review",
        ):
            self.assertNotIn(forbidden, p5_only)
        self.assertIn("human_review_mandatory", self.combined)
        self.assertIn("effect", self.source.lower())

    def test_manifest_records_p5_without_authority(self) -> None:
        prefix = "pilot_simulation_skeleton_design"
        self.assertEqual(self.manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertTrue(self.manifest[f"{prefix}_requires_p4_gold_frozen_router_reproduction_harness_design"])
        self.assertTrue(self.manifest[f"{prefix}_requires_root_drive_staging_canon"])
        self.assertIn("P6", self.manifest[f"{prefix}_next_allowed_milestone"])
        for flag in (
            "contains_live_simulation",
            "contains_callable_simulator",
            "contains_simulation_execution",
            "contains_live_validation",
            "contains_input_processing",
            "contains_output_generation",
            "contains_reproduction_harness_run",
            "contains_gold_loading",
            "contains_freeze_memory_read",
            "contains_prompt_library_read",
            "contains_route_comparison_execution",
            "contains_metric_calculation",
            "contains_report_writer",
            "contains_review_queue_writer",
            "contains_human_decision_recording",
            "contains_disagreement_trust",
            "contains_live_pilot_behavior",
            "contains_live_copilot_behavior",
            "contains_projection_implementation",
            "contains_recommendation_engine",
            "contains_prompt_loading",
            "contains_runtime_integration",
            "contains_file_io",
            "contains_persistence",
            "contains_training_data_use",
            "contains_batch_mode",
            "contains_limited_shadow_runtime",
            "contains_candidate_promotion",
            "contains_embeddings_or_providers",
        ):
            self.assertFalse(self.manifest[f"{prefix}_{flag}"], flag)
        chars = set(self.manifest.get("protected_architecture_characteristics", []))
        for expected in (
            "pilot_simulation_skeleton_design",
            "pilot_p5_design_only_no_simulation_execution",
            "pilot_p5_opt_in_per_invocation_required",
            "pilot_p5_ephemeral_in_memory_only",
            "pilot_p5_match_before_disagree_preserved",
            "pilot_p5_no_live_validation",
            "pilot_p5_no_input_processing",
            "pilot_p5_no_output_generation",
            "pilot_p5_no_route_comparison_execution",
            "pilot_p5_critical_boundary_error_budget_zero",
            "pilot_p5_human_review_mandatory_true",
            "pilot_no_projection_from_p5",
            "pilot_no_prompt_loading_from_p5",
            "pilot_no_runtime_authority_from_p5",
        ):
            self.assertIn(expected, chars)

    def test_readme_and_notes_document_boundary(self) -> None:
        self.assertIn("## P5 - Pilot Simulation Skeleton Design v1", self.readme)
        self.assertIn("P5 - Pilot Simulation Skeleton Design v1", self.notes)
        for text in (self.readme, self.notes):
            self.assertIn("no runtime authority", text.lower())
            self.assertIn("no Pilot implementation".lower(), text.lower())
            self.assertIn("no Copilot implementation".lower(), text.lower())
            self.assertIn("no input processing", text.lower())
            self.assertIn("no output generation", text.lower())
        self.assertIn("P6 - Routing Signal Scorer v3 Pilot Review Evidence Design v1", self.readme)


if __name__ == "__main__":
    unittest.main()
