from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.non_runtime_pilot_phase_closure_copilot_boundary_entry_gate import (
    ACTIVATION_EFFECT,
    AUTO_MATURITY_STATUS,
    COPILOT_BOUNDARY_ENTRY_GATE_STATUS,
    COPILOT_IMPLEMENTATION_STATUS,
    COPILOT_SCOPE_DESIGN_STATUS,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    DEFINITIVE_ENABLEMENT_STATUS,
    DESIGN_KIND,
    FEATURE_ID,
    FIELD_TEST_STATUS,
    FORBIDDEN_CLOSURE_CLAIMS,
    FORBIDDEN_OPERATIONS,
    GOLD_REGISTRY_MUTATION_STATUS,
    HUMAN_REVIEW_MANDATORY,
    LAB_TEST_CODING_STATUS,
    LAB_TEST_STATUS,
    OPT_IN_PER_INVOCATION_REQUIRED,
    P_SERIES_COMPLETION_STATUS,
    PILOT_PHASE_CLOSURE_STATUS,
    PILOT_RUNTIME_STATUS,
    POST_P12_STATUS,
    PROMPT_LOADING_EFFECT,
    REQUIRED_CLOSURE_SOURCE_FREEZES,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STATIC_CLOSURE_DECLARATIONS,
    STORAGE_STATUS,
    get_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class NonRuntimePilotPhaseClosureCopilotBoundaryEntryGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = get_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_record()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_static_closure_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1")
        self.assertEqual(SCHEMA_VERSION, "3.89-non-runtime-pilot-phase-closure-copilot-boundary-entry-gate")
        self.assertEqual(DESIGN_KIND, "non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_only")
        self.assertEqual(PILOT_PHASE_CLOSURE_STATUS, "static_closure_declaration_only")
        self.assertEqual(COPILOT_BOUNDARY_ENTRY_GATE_STATUS, "static_entry_gate_declaration_only")
        self.assertEqual(P_SERIES_COMPLETION_STATUS, "current_p_series_closes_only_after_p12_freeze")
        self.assertEqual(POST_P12_STATUS, "stop_before_test_lab_or_copilot_boundary_work")
        self.assertEqual(COPILOT_IMPLEMENTATION_STATUS, "not_started_in_p12")
        self.assertEqual(COPILOT_SCOPE_DESIGN_STATUS, "not_started_in_p12")
        self.assertEqual(PILOT_RUNTIME_STATUS, "not_started_in_p12")
        self.assertEqual(LAB_TEST_STATUS, "not_started_in_p12")
        self.assertEqual(self.record.feature_id, FEATURE_ID)
        self.assertEqual(self.record.pilot_phase_closure_status, PILOT_PHASE_CLOSURE_STATUS)

    def test_effects_closure_and_activation_boundaries_are_fixed(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(FIELD_TEST_STATUS, "not_allowed_in_p12")
        self.assertEqual(DEFINITIVE_ENABLEMENT_STATUS, "not_allowed_in_p12")
        self.assertEqual(LAB_TEST_CODING_STATUS, "not_started_in_p12")
        self.assertEqual(AUTO_MATURITY_STATUS, "not_allowed_in_p12")
        self.assertEqual(GOLD_REGISTRY_MUTATION_STATUS, "not_allowed_in_p12")

    def test_static_closure_declarations_are_declared_but_not_executed(self) -> None:
        expected = {
            "freeze_lineage_rg_pilot_000_m35_p0_through_p11_required",
            "p12_validation_and_freeze_required_before_closure",
            "p_series_closure_is_static_declaration_only",
            "copilot_boundary_entry_requires_separate_governed_scope",
            "test_lab_requires_explicit_warning_and_confirmation",
            "activation_gate_deferred_after_lab_testing",
            "no_runtime_authority_after_closure",
            "no_ml_maturity_claim_after_closure",
            "no_field_test_or_definitive_enablement_after_closure",
        }
        self.assertEqual(set(STATIC_CLOSURE_DECLARATIONS), expected)
        self.assertEqual({item.declaration_id for item in self.record.declarations}, expected)
        for item in self.record.declarations:
            self.assertEqual(item.status, "declared_only_not_executed_in_p12")
            self.assertEqual(item.failure_policy, "block_progression")

    def test_required_source_freezes_cover_p0_through_p11(self) -> None:
        text = "\n".join(REQUIRED_CLOSURE_SOURCE_FREEZES)
        for phrase in (
            "RG-PILOT-000 router canon freeze",
            "M35 bridge closure freeze",
            "P0 scope charter and entry gate freeze",
            "P1 Pilot boundary freeze",
            "P2 input/output contract design freeze",
            "P3 disagreement taxonomy freeze",
            "P4 reproduction harness design freeze",
            "P5 simulation skeleton design freeze",
            "P6 review evidence design freeze",
            "P7 implementation gate design freeze",
            "P8 non-runtime Pilot candidate freeze",
            "P9 contract conformance freeze",
            "P10 readiness gate freeze",
            "P11 review evidence packet freeze",
        ):
            self.assertIn(phrase, text)
        self.assertEqual(self.record.required_source_freezes, REQUIRED_CLOSURE_SOURCE_FREEZES)

    def test_forbidden_claims_and_operations_block_authority(self) -> None:
        claims = set(FORBIDDEN_CLOSURE_CLAIMS)
        for item in (
            "p_series_closed_without_p12_freeze",
            "pilot_runtime_ready",
            "pilot_runtime_enabled",
            "copilot_boundary_approved",
            "copilot_scope_defined",
            "copilot_implemented",
            "test_lab_started",
            "field_test_enabled",
            "mature_enabled",
            "auto_maturity_jump",
            "candidate_promoted",
            "router_authority_granted",
            "prompt_loading_enabled",
            "persistence_enabled",
            "training_data_enabled",
            "batch_mode_enabled",
            "gold_registry_mutated",
            "human_review_approved",
        ):
            self.assertIn(item, claims)
        self.assertEqual(set(self.record.boundary.forbidden_claims), claims)
        forbidden = set(FORBIDDEN_OPERATIONS)
        expected = {
            "close_without_freeze",
            "execute_phase_closure",
            "approve_pilot_readiness",
            "mark_candidate_ready",
            "record_human_decision",
            "record_approval",
            "enter_copilot_implementation",
            "define_copilot_scope",
            "approve_copilot_boundary",
            "implement_copilot",
            "start_test_lab",
            "design_test_lab",
            "code_test_lab",
            "create_lab_cases",
            "run_lab_test",
            "activate_field_test",
            "activate_definitive_enablement",
            "activate_maturity_key",
            "compare_routes",
            "read_prompt_library",
            "load_prompt",
            "write_gold",
            "write_registry",
            "call_provider",
            "use_embeddings",
            "train_from_output",
            "run_batch_mode",
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
            "evaluate",
            "approve",
            "enable",
            "close",
            "start_lab",
            "design_test_lab",
            "code_test_lab",
            "collect_evidence",
            "build_review_packet",
            "assemble_packet",
            "generate_packet",
            "write_packet",
            "validate_live",
            "process_input",
            "generate_output",
            "transform_payload",
            "compare_routes",
            "score",
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
        self.assertEqual(function_names, {"get_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_record"})

    def test_text_preserves_stop_rule_and_no_lab_or_copilot_implementation(self) -> None:
        required_phrases = [
            "Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1",
            "static closure and entry-gate declaration only",
            "does not mean ML maturity",
            "does not implement Copilot",
            "start the test lab",
            "Before any test-lab design or coding begins",
            "Activation Gate Box after lab testing and maturity evidence",
            "STOP after P12 freeze",
            "Any Copilot boundary design requires a separate governed",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_manifest_records_no_closure_execution_lab_or_runtime_features(self) -> None:
        prefix = "non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_"
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
        self.assertEqual(self.manifest[prefix + "field_test_status"], "not_allowed_in_p12")
        self.assertEqual(self.manifest[prefix + "definitive_enablement_status"], "not_allowed_in_p12")
        self.assertEqual(self.manifest[prefix + "copilot_status"], "not_started_in_p12")
        self.assertEqual(self.manifest[prefix + "copilot_scope_design_status"], "not_started_in_p12")
        self.assertEqual(self.manifest[prefix + "pilot_runtime_status"], "not_started_in_p12")
        self.assertEqual(self.manifest[prefix + "lab_test_coding_status"], "not_started_in_p12")
        self.assertEqual(self.manifest[prefix + "auto_maturity_status"], "not_allowed_in_p12")
        self.assertEqual(self.manifest[prefix + "gold_registry_mutation_status"], "not_allowed_in_p12")
        forbidden_flags = [
            "contains_phase_closure_execution",
            "contains_copilot_boundary_approval",
            "contains_copilot_scope_design",
            "contains_copilot_implementation",
            "contains_test_lab_design",
            "contains_test_lab_coding",
            "contains_lab_case_creation",
            "contains_evidence_collection",
            "contains_packet_builder",
            "contains_packet_population",
            "contains_packet_persistence",
            "contains_report_writer",
            "contains_review_queue_writer",
            "contains_human_decision_recording",
            "contains_readiness_approval",
            "contains_live_gate_evaluation",
            "contains_field_test_activation",
            "contains_definitive_enablement",
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
            "contains_approval_recording",
            "contains_embeddings_or_providers",
            "contains_training_data_use",
            "contains_batch_mode",
            "contains_limited_shadow_runtime",
            "contains_runtime_integration",
            "contains_router_authority",
            "contains_candidate_promotion",
            "contains_gold_or_registry_mutation",
            "contains_auto_maturity_jump",
            "contains_activation_key",
            "contains_maturity_on_off_switch",
        ]
        for flag in forbidden_flags:
            self.assertFalse(self.manifest[prefix + flag], flag)
        chars = set(self.manifest["protected_architecture_characteristics"])
        self.assertIn("non_runtime_pilot_phase_closure_copilot_boundary_entry_gate", chars)
        self.assertIn("p12_static_closure_entry_gate_only", chars)
        self.assertIn("test_lab_requires_explicit_warning_after_p12", chars)
        self.assertIn("no_copilot_implementation_from_p12", chars)
        self.assertIn("no_ml_maturity_claim_from_p12", chars)


if __name__ == "__main__":
    unittest.main()
