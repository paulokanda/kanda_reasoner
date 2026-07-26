from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_review_evidence_design import (
    ACTIVATION_EFFECT,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    FEATURE_ID,
    HUMAN_REVIEW_MANDATORY,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    STORAGE_STATUS,
    get_pilot_review_evidence_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_review_evidence_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_review_evidence_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PilotReviewEvidenceDesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = get_pilot_review_evidence_design()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_design_only_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_pilot_review_evidence_design_v1")
        self.assertEqual(self.design.feature_id, FEATURE_ID)
        self.assertEqual(self.design.schema_version, "3.83-pilot-review-evidence-design")
        self.assertEqual(self.design.design_kind, "pilot_review_evidence_design_only")
        self.assertEqual(self.design.milestone, "P6")
        self.assertEqual(self.design.design_status, "design_only")
        self.assertEqual(self.design.evidence_collection_status, "not_implemented_design_only")
        self.assertEqual(self.design.evidence_packet_generation_status, "not_implemented")
        self.assertEqual(self.design.live_validation_status, "not_implemented")
        self.assertEqual(self.design.input_processing_status, "not_implemented")
        self.assertEqual(self.design.output_generation_status, "not_implemented")
        self.assertEqual(self.design.route_comparison_status, "not_implemented")
        self.assertEqual(self.design.report_generation_status, "not_implemented")
        self.assertEqual(self.design.review_queue_status, "not_implemented")
        self.assertEqual(self.design.human_decision_recording_status, "not_implemented")
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
        self.assertEqual(self.design.storage_status, "in_memory_only")
        self.assertTrue(self.design.human_review_mandatory)
        self.assertTrue(self.design.opt_in_per_invocation_required)
        self.assertEqual(self.design.critical_boundary_error_budget, 0)
        self.assertIn("not approval", self.design.human_review_rule)
        self.assertIn("not a decision record", self.design.human_review_rule)
        self.assertIn("fail-closed", self.design.match_before_disagree_rule)

    def test_preconditions_include_complete_p_chain_before_p6(self) -> None:
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
            "kanda_patch_delivery_root_drive_staging_canon_frozen",
            "startup_freeze_context_refreshed_after_p5",
            "freeze_memory_status_ok_after_p5",
        }
        self.assertTrue(expected.issubset(required))
        self.assertIn("P7 - Routing Signal Scorer v3 Pilot Implementation Gate Design v1", self.design.next_allowed_milestone)

    def test_review_evidence_fields_are_descriptive_and_inert(self) -> None:
        ids = [field.field_id for field in self.design.evidence_fields]
        self.assertEqual(
            ids,
            [
                "case_local_opt_in_trace",
                "contract_boundary_trace",
                "frozen_router_reproduction_trace",
                "taxonomy_language_trace",
                "simulation_skeleton_trace",
                "critical_boundary_blocker_trace",
                "human_review_note_trace",
            ],
        )
        for field in self.design.evidence_fields:
            self.assertIn("field design only", field.inert_p6_status)
            self.assertTrue(field.forbidden_interpretation.startswith("Not") or field.forbidden_interpretation.startswith("No"))
        reproduction = next(field for field in self.design.evidence_fields if field.field_id == "frozen_router_reproduction_trace")
        self.assertIn("match-before-disagree", reproduction.design_purpose)
        self.assertIn("Not a harness run", reproduction.forbidden_interpretation)
        human = next(field for field in self.design.evidence_fields if field.field_id == "human_review_note_trace")
        self.assertIn("No note is written", human.inert_p6_status)
        self.assertIn("Not approval", human.forbidden_interpretation)

    def test_review_evidence_sections_require_order_and_fail_closed_language(self) -> None:
        ids = [section.section_id for section in self.design.evidence_sections]
        self.assertEqual(
            ids,
            [
                "section_1_scope_and_opt_in",
                "section_2_reproduction_before_taxonomy",
                "section_3_simulation_skeleton_traceability",
                "section_4_boundary_and_human_review",
            ],
        )
        sequences = [section.sequence_label for section in self.design.evidence_sections]
        self.assertEqual(sequences, ["1", "2", "3", "4"])
        for section in self.design.evidence_sections:
            self.assertIn("block", section.fail_closed_condition)
            self.assertIn("Human reviewer", section.human_review_visibility)
        taxonomy_section = self.design.evidence_sections[1]
        self.assertEqual(taxonomy_section.required_fields, ("frozen_router_reproduction_trace", "taxonomy_language_trace"))
        self.assertIn("Reproduction before taxonomy", taxonomy_section.design_purpose)

    def test_forbidden_operations_capture_no_runtime_or_storage_behavior(self) -> None:
        forbidden = set(self.design.forbidden_operations)
        expected = {
            "collect_evidence",
            "build_evidence_packet",
            "generate_review_packet",
            "validate_live_payload",
            "process_input",
            "generate_output",
            "run_simulation",
            "load_gold_set",
            "read_freeze_memory",
            "read_prompt_library",
            "inspect_runtime_router",
            "compare_routes",
            "calculate_metric",
            "detect_disagreement",
            "score_disagreement",
            "project_route",
            "recommend_route",
            "select_prompt",
            "load_prompt",
            "write_report",
            "write_review_queue",
            "persist_evidence_packet",
            "record_human_decision",
            "approve_route",
            "train_from_review_evidence",
            "run_batch_mode",
            "activate_limited_shadow_runtime",
            "promote_candidate",
            "call_provider",
            "use_embeddings",
        }
        self.assertTrue(expected.issubset(forbidden))

    def test_source_and_notes_explicitly_forbid_implementation_effects(self) -> None:
        required_phrases = [
            "P6 defines static review-evidence vocabulary",
            "It does not collect evidence",
            "No opt-in evidence is collected in P6; field design only.",
            "No note is written, persisted, queued, or recorded in P6; field design only.",
            "no evidence collection",
            "no evidence packet generation",
            "no human decision recording",
            "no runtime authority",
            "P7 - Routing Signal Scorer v3 Pilot Implementation Gate Design v1",
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
            "def collect_",
            "def build_evidence",
            "def generate_",
            "def validate_",
            "def process_",
            "def run_",
            "def execute_",
            "def load_",
            "def read_",
            "def inspect_",
            "def compare_",
            "def calculate_",
            "def detect_",
            "def score_",
            "def project_",
            "def recommend_",
            "def select_",
            "def write_",
            "def persist_",
            "def record_",
            "def approve_",
            "class PilotRunner",
            "class CopilotRunner",
            "class PilotSimulator",
            "class ReviewQueue",
        ]
        for pattern in forbidden_defs:
            self.assertNotIn(pattern, self.source)

    def test_manifest_records_p6_and_false_runtime_flags(self) -> None:
        prefix = "pilot_review_evidence_design"
        self.assertEqual(self.manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(self.manifest[f"{prefix}_schema_version"], "3.83-pilot-review-evidence-design")
        self.assertTrue(self.manifest[f"{prefix}_requires_p5_simulation_skeleton_design"])
        self.assertTrue(self.manifest[f"{prefix}_requires_root_drive_staging_canon"])
        self.assertEqual(self.manifest[f"{prefix}_routing_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_prompt_loading_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_runtime_effect"], "none")
        self.assertEqual(self.manifest[f"{prefix}_activation_effect"], "none")
        self.assertTrue(self.manifest[f"{prefix}_human_review_mandatory"])
        self.assertTrue(self.manifest[f"{prefix}_opt_in_per_invocation_required"])
        self.assertEqual(self.manifest[f"{prefix}_critical_boundary_error_budget"], 0)
        false_flags = [
            "contains_evidence_collection",
            "contains_evidence_packet_generation",
            "contains_review_packet_generation",
            "contains_live_validation",
            "contains_input_processing",
            "contains_output_generation",
            "contains_route_comparison_execution",
            "contains_metric_calculation",
            "contains_report_writer",
            "contains_review_queue_writer",
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

    def test_protected_architecture_characteristics_include_p6(self) -> None:
        chars = set(self.manifest["protected_architecture_characteristics"])
        expected = {
            "pilot_review_evidence_design",
            "pilot_p6_design_only_no_evidence_collection",
            "pilot_p6_no_packet_generation",
            "pilot_p6_match_before_disagree_preserved",
            "pilot_p6_no_human_decision_recording",
            "pilot_p6_critical_boundary_error_budget_zero",
            "pilot_no_projection_from_p6",
            "pilot_no_prompt_loading_from_p6",
            "pilot_no_runtime_authority_from_p6",
        }
        self.assertTrue(expected.issubset(chars))

    def test_p6_is_not_copilot_or_runtime_shadow(self) -> None:
        forbidden_claims = [
            "activate Copilot",
            "Limited Shadow Runtime implementation",
            "runtime authority granted",
            "auto-approve",
            "automatic approval",
            "training dataset",
            "batch execution",
        ]
        for phrase in forbidden_claims:
            self.assertNotIn(phrase, self.combined)


if __name__ == "__main__":
    unittest.main()
