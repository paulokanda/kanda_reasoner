from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.non_runtime_pilot_candidate_contract_conformance import (
    ACTIVATION_EFFECT,
    ALLOWED_INPUT_FIELDS,
    ALLOWED_OUTPUT_FIELDS,
    CONFORMANCE_STATUS,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    DEFINITIVE_ENABLEMENT_STATUS,
    DESIGN_KIND,
    FEATURE_ID,
    FIELD_TEST_STATUS,
    FORBIDDEN_INPUT_CONCEPTS,
    FORBIDDEN_OPERATIONS,
    FORBIDDEN_OUTPUT_FIELDS,
    HUMAN_REVIEW_MANDATORY,
    INPUT_PROCESSING_STATUS,
    LIVE_VALIDATOR_STATUS,
    OPT_IN_PER_INVOCATION_REQUIRED,
    OUTPUT_GENERATION_STATUS,
    PILOT_CANDIDATE_SOURCE_MILESTONE,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STORAGE_STATUS,
    get_non_runtime_pilot_candidate_contract_conformance_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_contract_conformance.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_contract_conformance_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class NonRuntimePilotCandidateContractConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = get_non_runtime_pilot_candidate_contract_conformance_record()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_static_conformance_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1")
        self.assertEqual(SCHEMA_VERSION, "3.86-non-runtime-pilot-candidate-contract-conformance")
        self.assertEqual(DESIGN_KIND, "non_runtime_pilot_candidate_contract_conformance_only")
        self.assertEqual(PILOT_CANDIDATE_SOURCE_MILESTONE, "P8")
        self.assertEqual(CONFORMANCE_STATUS, "static_conformance_declaration_only")
        self.assertEqual(LIVE_VALIDATOR_STATUS, "not_present_in_p9")
        self.assertEqual(INPUT_PROCESSING_STATUS, "not_allowed_in_p9")
        self.assertEqual(OUTPUT_GENERATION_STATUS, "not_allowed_in_p9")
        self.assertEqual(self.record.feature_id, FEATURE_ID)
        self.assertEqual(self.record.schema_version, SCHEMA_VERSION)
        self.assertEqual(self.record.pilot_candidate_source_milestone, "P8")
        self.assertEqual(self.record.conformance_status, "static_conformance_declaration_only")

    def test_effects_and_review_invariants_are_fixed(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(FIELD_TEST_STATUS, "not_allowed_in_p9")
        self.assertEqual(DEFINITIVE_ENABLEMENT_STATUS, "not_allowed_in_p9")
        invariants = {item.invariant_id: item for item in self.record.invariants}
        self.assertEqual(invariants["routing_effect"].expected_value, "none")
        self.assertEqual(invariants["prompt_loading_effect"].expected_value, "none")
        self.assertEqual(invariants["runtime_effect"].expected_value, "none")
        self.assertEqual(invariants["activation_effect"].expected_value, "none")
        self.assertEqual(invariants["storage_status"].expected_value, "in_memory_only")
        self.assertEqual(invariants["human_review_mandatory"].expected_value, "true")
        self.assertEqual(invariants["critical_boundary_error_budget"].expected_value, "zero")
        for item in invariants.values():
            self.assertEqual(item.failure_policy, "block_progression")

    def test_input_field_set_is_declarative_and_primitive_only(self) -> None:
        expected = {
            "case_id",
            "schema_version",
            "user_request_summary",
            "routing_context_public_summary",
            "task_classification_hints_summary",
            "current_router_outcome_summary",
            "frozen_canon_constraints_summary",
            "known_boundary_flags",
            "caller_generated_timestamp_utc",
        }
        self.assertEqual(set(ALLOWED_INPUT_FIELDS), expected)
        self.assertEqual(set(self.record.input_field_set.allowed_fields), expected)
        self.assertEqual(self.record.input_field_set.status, "static_declared_only_no_live_validation")
        forbidden = set(FORBIDDEN_INPUT_CONCEPTS)
        for item in (
            "raw_prompt_text",
            "prompt_file_path",
            "prompt_group_object",
            "prompt_library_handle",
            "live_router_object",
            "runtime_state_object",
            "callback",
            "callable",
            "training_data_request",
            "batch_mode_request",
            "activation_request",
        ):
            self.assertIn(item, forbidden)

    def test_output_field_set_is_non_authoritative_only(self) -> None:
        expected = {
            "pilot_record_kind",
            "case_id",
            "schema_version",
            "authority_notice",
            "projection_analysis_summary",
            "task_classification_projection_summary",
            "reasoning_summary_for_human_review",
            "boundary_flags_for_human_review",
            "divergence_summary_for_human_review",
            "divergence_type",
            "missing_information_summary",
            "human_review_mandatory",
            "advisory_review_priority",
            "routing_effect",
            "prompt_loading_effect",
            "runtime_effect",
            "activation_effect",
            "storage_status",
        }
        self.assertEqual(set(ALLOWED_OUTPUT_FIELDS), expected)
        self.assertEqual(set(self.record.output_field_set.allowed_fields), expected)
        self.assertEqual(self.record.output_field_set.status, "static_declared_only_no_output_generation")
        forbidden = set(FORBIDDEN_OUTPUT_FIELDS)
        for item in (
            "approved_route",
            "final_route",
            "execute_route",
            "load_prompt",
            "activate_pilot",
            "activate_copilot",
            "confidence",
            "score",
            "probability",
            "recommendation",
            "suggested_route",
            "suggested_prompts",
            "human_review_completed",
            "runtime_enabled",
        ):
            self.assertIn(item, forbidden)
        self.assertNotIn("candidate_prompt_groups", ALLOWED_INPUT_FIELDS)
        self.assertNotIn("candidate_prompt_groups", ALLOWED_OUTPUT_FIELDS)

    def test_required_preconditions_include_p8_and_contract_design(self) -> None:
        ids = {item.precondition_id for item in self.record.required_preconditions}
        self.assertEqual(
            ids,
            {
                "p8_non_runtime_candidate_frozen",
                "p2_contract_design_frozen",
                "p3_taxonomy_design_frozen",
                "p4_reproduction_harness_design_frozen",
                "root_drive_staging_installer_canon_frozen",
            },
        )
        self.assertIn("P8 Non-Runtime Pilot Candidate Implementation v1 frozen", self.record.required_preconditions[0].required_state)
        self.assertIn("P10 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness Gate v1", self.record.next_allowed_milestone)

    def test_forbidden_operations_cover_execution_and_authority_boundaries(self) -> None:
        forbidden = set(FORBIDDEN_OPERATIONS)
        expected = {
            "validate_live_payload",
            "process_input",
            "generate_output",
            "transform_payload",
            "project_route",
            "recommend_route",
            "select_route",
            "override_route",
            "execute_route",
            "compare_routes",
            "inspect_runtime_router",
            "load_gold_set",
            "read_freeze_memory",
            "read_prompt_library",
            "select_prompt",
            "load_prompt",
            "collect_evidence",
            "build_evidence_packet",
            "record_human_decision",
            "record_approval",
            "persist_record",
            "write_report",
            "write_review_queue",
            "write_gold",
            "write_registry",
            "write_freeze_memory",
            "call_provider",
            "use_embeddings",
            "train_from_output",
            "run_batch_mode",
            "activate_field_test",
            "activate_definitive_enablement",
            "activate_pilot",
            "activate_copilot",
            "activate_limited_shadow_runtime",
            "promote_candidate",
        }
        self.assertTrue(expected.issubset(forbidden))
        self.assertEqual(set(self.record.forbidden_operations), forbidden)

    def test_source_has_no_runtime_io_imports_or_dynamic_execution(self) -> None:
        tree = ast.parse(self.source)
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        imported_names = "\n".join(ast.get_source_segment(self.source, node) or "" for node in imports)
        for forbidden_import in (
            "os",
            "sys",
            "pathlib",
            "json",
            "pickle",
            "sqlite",
            "requests",
            "subprocess",
            "importlib",
            "threading",
            "multiprocessing",
            "socket",
            "logging",
        ):
            self.assertNotIn(forbidden_import, imported_names)
        for forbidden_source_pattern in (
            "open(",
            "Path(",
            ".read_text(",
            ".write_text(",
            "eval(",
            "exec(",
            "compile(",
            "__import__",
            "entry_points",
        ):
            self.assertNotIn(forbidden_source_pattern, self.source)

    def test_no_runtime_function_names_are_defined(self) -> None:
        tree = ast.parse(self.source)
        function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        forbidden_names = {
            "run",
            "execute",
            "simulate",
            "validate_live",
            "process_input",
            "generate_output",
            "transform_payload",
            "compare_routes",
            "score",
            "approve",
            "select_route",
            "load_prompt",
            "persist",
            "record_decision",
            "call_provider",
            "use_embeddings",
            "batch",
            "activate_runtime",
            "activate_pilot",
            "activate_copilot",
        }
        self.assertTrue(function_names.isdisjoint(forbidden_names), sorted(function_names & forbidden_names))
        self.assertEqual(function_names, {"get_non_runtime_pilot_candidate_contract_conformance_record"})

    def test_text_preserves_static_conformance_and_activation_boundary(self) -> None:
        required_phrases = [
            "Non-Runtime Pilot Candidate Contract Conformance v1",
            "static conformance declaration only",
            "not a live validator",
            "Human governance and the real router remain authoritative",
            "Field-test activation and definitive enablement remain deferred",
            "Activation Gate Box after lab testing and maturity evidence",
            "P10 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness Gate v1",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_manifest_records_no_live_validator_or_runtime_features(self) -> None:
        prefix = "non_runtime_pilot_candidate_contract_conformance_"
        self.assertEqual(self.manifest[prefix + "feature_id"], FEATURE_ID)
        self.assertEqual(self.manifest[prefix + "schema_version"], SCHEMA_VERSION)
        self.assertEqual(self.manifest[prefix + "routing_effect"], "none")
        self.assertEqual(self.manifest[prefix + "prompt_loading_effect"], "none")
        self.assertEqual(self.manifest[prefix + "runtime_effect"], "none")
        self.assertEqual(self.manifest[prefix + "activation_effect"], "none")
        self.assertEqual(self.manifest[prefix + "storage_status"], "in_memory_only")
        self.assertTrue(self.manifest[prefix + "human_review_mandatory"])
        self.assertTrue(self.manifest[prefix + "opt_in_per_invocation_required"])
        self.assertEqual(self.manifest[prefix + "critical_boundary_error_budget"], 0)
        self.assertEqual(self.manifest[prefix + "field_test_status"], "not_allowed_in_p9")
        self.assertEqual(self.manifest[prefix + "definitive_enablement_status"], "not_allowed_in_p9")
        self.assertEqual(self.manifest[prefix + "live_validator_status"], "not_present_in_p9")
        self.assertEqual(self.manifest[prefix + "input_processing_status"], "not_allowed_in_p9")
        self.assertEqual(self.manifest[prefix + "output_generation_status"], "not_allowed_in_p9")
        forbidden_flags = [
            "contains_live_validator",
            "contains_live_validation",
            "contains_input_processing",
            "contains_output_generation",
            "contains_payload_transformation",
            "contains_callable_pilot",
            "contains_callable_pilot_runner",
            "contains_callable_copilot_runner",
            "contains_callable_simulator",
            "contains_projection_implementation",
            "contains_route_comparison_execution",
            "contains_runtime_router_inspection",
            "contains_prompt_loading",
            "contains_prompt_library_read",
            "contains_gold_loading",
            "contains_freeze_memory_read",
            "contains_persistence",
            "contains_report_writer",
            "contains_review_queue_writer",
            "contains_human_decision_recording",
            "contains_approval_recording",
            "contains_embeddings_or_providers",
            "contains_training_data_use",
            "contains_batch_mode",
            "contains_limited_shadow_runtime",
            "contains_runtime_integration",
            "contains_router_authority",
            "contains_candidate_promotion",
            "contains_field_test_activation",
            "contains_definitive_enablement",
        ]
        for flag in forbidden_flags:
            self.assertFalse(self.manifest[prefix + flag], flag)


if __name__ == "__main__":
    unittest.main()
