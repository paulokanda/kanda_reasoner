from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_gold_router_reproduction_harness_design import (
    ACTIVATION_EFFECT,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    FEATURE_ID,
    HUMAN_REVIEW_MANDATORY,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    STORAGE_STATUS,
    get_pilot_gold_router_reproduction_harness_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_gold_router_reproduction_harness_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_gold_router_reproduction_harness_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PilotGoldRouterReproductionHarnessDesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = get_pilot_gold_router_reproduction_harness_design()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_design_only_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_pilot_gold_frozen_router_reproduction_harness_design_v1")
        self.assertEqual(self.design.feature_id, FEATURE_ID)
        self.assertEqual(self.design.schema_version, "3.81-pilot-gold-frozen-router-reproduction-harness-design")
        self.assertEqual(self.design.design_kind, "pilot_gold_frozen_router_reproduction_harness_design_only")
        self.assertEqual(self.design.milestone, "P4")
        self.assertEqual(self.design.design_status, "design_only")
        self.assertEqual(self.design.harness_status, "not_implemented_design_only")
        self.assertEqual(self.design.gold_loading_status, "not_implemented")
        self.assertEqual(self.design.frozen_router_access_status, "not_implemented")
        self.assertEqual(self.design.route_comparison_status, "not_implemented")
        self.assertEqual(self.design.metric_calculation_status, "not_implemented")
        self.assertEqual(self.design.report_generation_status, "not_implemented")

    def test_fixed_non_authority_invariants(self) -> None:
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
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
            "kanda_patch_delivery_root_drive_staging_canon_frozen",
            "startup_freeze_context_refreshed_after_p3_and_installer_canon",
            "freeze_memory_status_ok_after_p3_and_installer_canon",
        ):
            self.assertIn(item, required)
        self.assertIn("P5", self.design.next_allowed_milestone)
        self.assertIn("FREEZE_MEMORY_STATUS OK", self.design.next_allowed_milestone)

    def test_reference_designs_are_provenance_only_and_no_direct_access(self) -> None:
        refs = self.design.reference_designs
        self.assertEqual(len(refs), 3)
        ids = {ref.reference_id for ref in refs}
        self.assertEqual(ids, {"frozen_router_canon_reference", "governed_case_reference", "expected_output_reference"})
        for ref in refs:
            self.assertIn("No ", ref.forbidden_access)
            self.assertIn("provenance", ref.required_provenance.lower())
            self.assertIn("blocks", ref.fail_closed_condition.lower())

    def test_harness_phase_designs_are_non_executable_and_human_reviewed(self) -> None:
        phases = self.design.harness_phase_designs
        self.assertEqual(len(phases), 3)
        ids = {phase.phase_id for phase in phases}
        self.assertIn("preflight_provenance_check_design", ids)
        self.assertIn("frozen_outcome_alignment_design", ids)
        self.assertIn("critical_failure_blocker_design", ids)
        for phase in phases:
            self.assertIn("Human reviewer", phase.human_review_requirement)
            self.assertIn("No ", phase.forbidden_operation)

    def test_metric_designs_preserve_match_before_disagree_and_zero_critical_budget(self) -> None:
        metrics = {metric.metric_id: metric for metric in self.design.metric_designs}
        self.assertEqual(metrics["exact_frozen_outcome_match_required"].required_result, "required_for_trust")
        self.assertEqual(metrics["critical_boundary_error_count_zero"].required_result, "0")
        self.assertEqual(metrics["human_review_mandatory_true"].required_result, "True")
        self.assertIn("routing_effect=none", metrics["effect_fields_none"].required_result)
        for metric in metrics.values():
            self.assertTrue(metric.failure_effect)

    def test_forbidden_operations_include_all_runtime_authority_paths(self) -> None:
        forbidden = set(self.design.forbidden_operations)
        for op in (
            "run_reproduction_harness",
            "execute_harness_case",
            "load_gold_set",
            "read_gold_manifest",
            "read_freeze_memory",
            "read_prompt_library",
            "inspect_runtime_router",
            "import_runtime_router",
            "compare_routes",
            "calculate_reproduction_score",
            "rank_candidate",
            "certify_candidate",
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
            "persist_harness_record",
            "record_human_decision",
            "mutate_gold_registry",
            "mutate_freeze_memory",
            "train_from_harness_result",
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
        p4_only = "\n".join([self.source, self.notes])
        for forbidden in (
            "candidate_prompt_groups",
            "simulated_required_prompt_groups",
            "required_prompt_groups",
            "requires_human_review",
        ):
            self.assertNotIn(forbidden, p4_only)
        self.assertIn("human_review_mandatory", self.combined)
        self.assertIn("effect fields", self.notes.lower())

    def test_manifest_records_p4_without_authority(self) -> None:
        prefix = "pilot_gold_router_reproduction_harness_design"
        self.assertEqual(self.manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertTrue(self.manifest[f"{prefix}_requires_p3_pilot_disagreement_taxonomy_design"])
        self.assertTrue(self.manifest[f"{prefix}_requires_root_drive_staging_canon"])
        self.assertIn("P5", self.manifest[f"{prefix}_next_allowed_milestone"])
        for flag in (
            "contains_live_harness",
            "contains_harness_execution",
            "contains_gold_loading",
            "contains_freeze_memory_read",
            "contains_prompt_library_read",
            "contains_runtime_router_inspection",
            "contains_route_comparison_execution",
            "contains_metric_calculation",
            "contains_report_writer",
            "contains_disagreement_trust",
            "contains_live_pilot_behavior",
            "contains_live_copilot_behavior",
            "contains_projection_implementation",
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
            "pilot_gold_router_reproduction_harness_design",
            "pilot_p4_design_only_no_harness_execution",
            "pilot_p4_match_before_disagree_preserved",
            "pilot_p4_no_gold_loading",
            "pilot_p4_no_freeze_memory_read",
            "pilot_p4_no_route_comparison_execution",
            "pilot_p4_critical_boundary_error_budget_zero",
            "pilot_p4_human_review_mandatory_true",
            "pilot_no_projection_from_p4",
            "pilot_no_prompt_loading_from_p4",
            "pilot_no_runtime_authority_from_p4",
        ):
            self.assertIn(expected, chars)

    def test_readme_and_notes_document_boundary(self) -> None:
        self.assertIn("## P4 - Pilot Gold/Frozen Router Reproduction Harness Design v1", self.readme)
        self.assertIn("P4 - Pilot Gold/Frozen Router Reproduction Harness Design v1", self.notes)
        for text in (self.readme, self.notes):
            self.assertIn("match-before-disagree", text.lower())
            self.assertIn("no Pilot implementation".lower(), text.lower())
            self.assertIn("no Copilot implementation".lower(), text.lower())
            self.assertIn("no runtime authority".lower(), text.lower())
        self.assertIn("P5 - Routing Signal Scorer v3 Pilot Simulation Skeleton Design v1", self.readme)


if __name__ == "__main__":
    unittest.main()
