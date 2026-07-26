from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_disagreement_taxonomy_design import (
    ACTIVATION_EFFECT,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    FEATURE_ID,
    HUMAN_REVIEW_MANDATORY,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    STORAGE_STATUS,
    get_pilot_disagreement_taxonomy_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_disagreement_taxonomy_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_disagreement_taxonomy_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PilotDisagreementTaxonomyDesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.design = get_pilot_disagreement_taxonomy_design()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_design_only_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_pilot_disagreement_taxonomy_design_v1")
        self.assertEqual(self.design.feature_id, FEATURE_ID)
        self.assertEqual(self.design.schema_version, "3.80-pilot-disagreement-taxonomy-design")
        self.assertEqual(self.design.design_kind, "pilot_disagreement_taxonomy_design_only")
        self.assertEqual(self.design.milestone, "P3")
        self.assertEqual(self.design.design_status, "design_only")
        self.assertEqual(self.design.taxonomy_status, "descriptive_categories_only_not_a_classifier")
        self.assertEqual(self.design.detector_status, "not_implemented")
        self.assertEqual(self.design.scoring_status, "not_implemented")
        self.assertEqual(self.design.pilot_status, "not_implemented")
        self.assertEqual(self.design.copilot_status, "not_implemented")
        self.assertEqual(self.design.projection_status, "not_implemented")
        self.assertEqual(self.design.route_comparison_status, "not_implemented")

    def test_fixed_non_authority_invariants(self) -> None:
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(self.design.critical_boundary_error_budget, 0)
        invariant_map = {item.invariant_id: item.required_value for item in self.design.invariants}
        self.assertEqual(invariant_map["human_review_mandatory"], "True")
        self.assertEqual(invariant_map["routing_effect"], "none")
        self.assertEqual(invariant_map["prompt_loading_effect"], "none")
        self.assertEqual(invariant_map["runtime_effect"], "none")
        self.assertEqual(invariant_map["activation_effect"], "none")
        self.assertEqual(invariant_map["storage_status"], "in_memory_only")
        self.assertEqual(invariant_map["critical_boundary_error_budget"], "0")

    def test_required_preconditions_and_next_milestone(self) -> None:
        required = set(self.design.required_preconditions)
        for item in (
            "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
            "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
            "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
            "p1_pilot_boundary_design_frozen",
            "p2_pilot_input_output_contract_validator_design_frozen",
            "startup_freeze_context_refreshed_after_p2",
            "freeze_memory_status_ok_after_p2",
        ):
            self.assertIn(item, required)
        self.assertIn("P4", self.design.next_allowed_milestone)
        self.assertIn("FREEZE_MEMORY_STATUS OK", self.design.next_allowed_milestone)

    def test_categories_are_unique_review_only_and_cover_critical_cases(self) -> None:
        categories = self.design.categories
        self.assertGreaterEqual(len(categories), 10)
        ids = [category.category_id for category in categories]
        self.assertEqual(len(ids), len(set(ids)))
        for expected in (
            "no_observable_difference",
            "missing_or_insufficient_evidence",
            "task_classification_difference",
            "boundary_condition_difference",
            "supporting_material_hint_difference",
            "freeze_constraint_conflict",
            "safety_governance_boundary_conflict",
            "maturity_path_conflict",
            "authority_drift_attempt",
            "unresolved_ambiguity",
        ):
            self.assertIn(expected, ids)
        critical = [category for category in categories if category.severity == "critical_review"]
        self.assertGreaterEqual(len(critical), 3)
        for category in categories:
            self.assertIn("Human reviewer", category.required_human_review_action)
            self.assertNotIn("automatically route", category.required_human_review_action.lower())
            self.assertNotIn("select prompt", category.required_human_review_action.lower())

    def test_evidence_rules_are_primitive_descriptive_and_fail_closed(self) -> None:
        rule_ids = {rule.rule_id for rule in self.design.evidence_rules}
        self.assertIn("evidence_from_caller_supplied_primitives_only", rule_ids)
        self.assertIn("taxonomy_is_not_recommendation", rule_ids)
        self.assertIn("match_before_disagree_required", rule_ids)
        self.assertIn("critical_boundary_error_budget_zero", rule_ids)
        for rule in self.design.evidence_rules:
            self.assertTrue(rule.fail_closed_result)
            self.assertIn("No ", rule.forbidden_source_or_action)

    def test_match_before_disagree_is_explicit(self) -> None:
        self.assertIn("No taxonomy label is trusted", self.design.match_before_disagree_rule)
        self.assertIn("reproduce frozen router/canon outcomes", self.design.match_before_disagree_rule)
        self.assertIn("match-before-disagree", self.notes.lower())
        self.assertIn("future reproduction", self.readme.lower())

    def test_forbidden_operations_include_all_runtime_authority_paths(self) -> None:
        forbidden = set(self.design.forbidden_operations)
        for op in (
            "detect_disagreement",
            "score_disagreement",
            "compare_routes",
            "execute_route_comparison",
            "project_route",
            "recommend_route",
            "select_route",
            "select_prompt",
            "load_prompt",
            "read_prompt_library",
            "read_freeze_memory",
            "mutate_freeze_memory",
            "persist_disagreement_record",
            "record_human_decision",
            "train_from_disagreement",
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
        p3_only = "\n".join([self.source, self.notes])
        for forbidden in (
            "candidate_prompt_groups",
            "simulated_required_prompt_groups",
            "required_prompt_groups",
            "requires_human_review",
        ):
            self.assertNotIn(forbidden, p3_only)
        self.assertIn("supporting_material_hint_difference", self.combined)
        self.assertIn("human_review_mandatory", self.combined)

    def test_manifest_records_p3_without_authority(self) -> None:
        prefix = "pilot_disagreement_taxonomy_design"
        self.assertEqual(self.manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertTrue(self.manifest[f"{prefix}_requires_p2_pilot_io_contract_validator_design"])
        self.assertIn("P4", self.manifest[f"{prefix}_next_allowed_milestone"])
        for flag in (
            "contains_disagreement_detector",
            "contains_disagreement_scoring",
            "contains_live_pilot_behavior",
            "contains_live_copilot_behavior",
            "contains_projection_implementation",
            "contains_route_comparison_execution",
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
            "pilot_disagreement_taxonomy_design",
            "pilot_p3_design_only_no_detector",
            "pilot_p3_taxonomy_not_recommendation",
            "pilot_p3_match_before_disagree_required",
            "pilot_p3_critical_boundary_error_budget_zero",
            "pilot_no_projection_from_p3",
            "pilot_no_prompt_loading_from_p3",
            "pilot_no_runtime_authority_from_p3",
        ):
            self.assertIn(expected, chars)

    def test_readme_and_notes_document_boundary(self) -> None:
        self.assertIn("## P3 - Pilot Disagreement Taxonomy Design v1", self.readme)
        self.assertIn("P3 - Pilot Disagreement Taxonomy Design v1", self.notes)
        for text in (self.readme, self.notes):
            self.assertIn("design-only", text)
            self.assertIn("no", text.lower())
            self.assertIn("P4", text)
            self.assertIn("FREEZE_MEMORY_STATUS", text)


if __name__ == "__main__":
    unittest.main()
