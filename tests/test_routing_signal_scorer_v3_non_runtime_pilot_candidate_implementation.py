from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.non_runtime_pilot_candidate import (
    ACTIVATION_EFFECT,
    CANDIDATE_AUTHORITY_STATUS,
    CANDIDATE_MATURITY_STATUS,
    CANDIDATE_RUNTIME_STATUS,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    DEFINITIVE_ENABLEMENT_STATUS,
    DESIGN_KIND,
    FEATURE_ID,
    FIELD_TEST_STATUS,
    HUMAN_REVIEW_MANDATORY,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STORAGE_STATUS,
    get_non_runtime_pilot_candidate_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class NonRuntimePilotCandidateImplementationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = get_non_runtime_pilot_candidate_record()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_static_candidate_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1")
        self.assertEqual(SCHEMA_VERSION, "3.85-non-runtime-pilot-candidate-implementation")
        self.assertEqual(DESIGN_KIND, "non_runtime_pilot_candidate_implementation_only")
        self.assertEqual(self.record.feature_id, FEATURE_ID)
        self.assertEqual(self.record.schema_version, SCHEMA_VERSION)
        self.assertEqual(self.record.identity.milestone, "P8")
        self.assertEqual(self.record.identity.candidate_id, "pilot_candidate_non_runtime_v1")
        self.assertEqual(self.record.identity.implementation_scope, "static_metadata_record_only")
        self.assertEqual(self.record.identity.maturity_status, "immature_non_runtime_candidate")

    def test_effects_and_boundary_state_are_no_authority(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(CANDIDATE_RUNTIME_STATUS, "not_runtime")
        self.assertEqual(CANDIDATE_AUTHORITY_STATUS, "not_authoritative")
        self.assertEqual(CANDIDATE_MATURITY_STATUS, "immature_non_runtime_candidate")
        self.assertEqual(FIELD_TEST_STATUS, "not_allowed_in_p8")
        self.assertEqual(DEFINITIVE_ENABLEMENT_STATUS, "not_allowed_in_p8")
        state = self.record.boundary_state
        self.assertEqual(state.routing_effect, "none")
        self.assertEqual(state.prompt_loading_effect, "none")
        self.assertEqual(state.runtime_effect, "none")
        self.assertEqual(state.activation_effect, "none")
        self.assertEqual(state.storage_status, "in_memory_only")
        self.assertTrue(state.human_review_mandatory)
        self.assertTrue(state.opt_in_per_invocation_required)
        self.assertEqual(state.critical_boundary_error_budget, 0)
        self.assertEqual(state.field_test_status, "not_allowed_in_p8")
        self.assertEqual(state.definitive_enablement_status, "not_allowed_in_p8")

    def test_allowed_declarations_are_static_metadata_only(self) -> None:
        ids = {item.capability_id for item in self.record.allowed_declarations}
        self.assertEqual(
            ids,
            {
                "static_identity_declaration",
                "static_boundary_declaration",
                "static_capability_map_declaration",
                "static_precondition_declaration",
            },
        )
        for item in self.record.allowed_declarations:
            self.assertEqual(item.capability_kind, "allowed_static_metadata")
            self.assertEqual(item.status, "available_in_p8")
            self.assertIn("p8 may", item.reason.lower())

    def test_forbidden_declarations_block_runtime_and_activation(self) -> None:
        ids = {item.capability_id for item in self.record.forbidden_declarations}
        expected = {
            "runtime_routing",
            "prompt_loading",
            "persistent_recording",
            "provider_or_embedding_use",
            "training_or_batch_use",
            "field_test_or_definitive_enablement",
        }
        self.assertEqual(ids, expected)
        for item in self.record.forbidden_declarations:
            self.assertEqual(item.capability_kind, "forbidden_behavior")
            self.assertEqual(item.status, "blocked_in_p8")

    def test_required_preconditions_include_p7_and_installer_canon(self) -> None:
        ids = {item.precondition_id for item in self.record.required_preconditions}
        self.assertEqual(
            ids,
            {
                "m35_bridge_closed_and_frozen",
                "rg_pilot_000_router_canon_frozen",
                "p0_through_p7_frozen",
                "root_drive_staging_installer_canon_frozen",
            },
        )
        self.assertIn("P0 through P7 frozen", self.record.required_preconditions[2].required_state)
        self.assertIn("P9 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1", self.record.next_allowed_milestone)

    def test_forbidden_operations_cover_unsafe_boundaries(self) -> None:
        forbidden = set(self.record.forbidden_operations)
        expected = {
            "evaluate_user_request",
            "process_input",
            "generate_output",
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
            "validate_live_payload",
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
        self.assertEqual(function_names, {"get_non_runtime_pilot_candidate_record"})

    def test_text_preserves_non_runtime_activation_gate_boundary(self) -> None:
        required_phrases = [
            "Non-Runtime Pilot Candidate Implementation v1",
            "inert, static candidate record",
            "not a Pilot runtime",
            "Human governance and the real router remain authoritative",
            "field-test and definitive enablement are not allowed in this milestone",
            "Activation Gate Box after lab testing and maturity evidence",
            "P9 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_manifest_records_no_runtime_or_persistence_features(self) -> None:
        prefix = "non_runtime_pilot_candidate_implementation_"
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
        self.assertEqual(self.manifest[prefix + "field_test_status"], "not_allowed_in_p8")
        self.assertEqual(self.manifest[prefix + "definitive_enablement_status"], "not_allowed_in_p8")
        forbidden_flags = [
            "contains_callable_pilot",
            "contains_callable_pilot_runner",
            "contains_callable_copilot_runner",
            "contains_callable_simulator",
            "contains_live_validation",
            "contains_input_processing",
            "contains_output_generation",
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
