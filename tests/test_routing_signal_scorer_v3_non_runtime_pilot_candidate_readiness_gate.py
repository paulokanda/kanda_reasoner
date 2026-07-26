from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.non_runtime_pilot_candidate_readiness_gate import (
    ACTIVATION_EFFECT,
    ALLOWED_GATE_OUTCOMES,
    BLOCKER_CLASSES,
    COPILOT_STATUS,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    DEFINITIVE_ENABLEMENT_STATUS,
    DESIGN_KIND,
    FEATURE_ID,
    FIELD_TEST_STATUS,
    FORBIDDEN_GATE_OUTCOMES,
    FORBIDDEN_OPERATIONS,
    HUMAN_REVIEW_MANDATORY,
    LAB_TEST_CODING_STATUS,
    LAB_TEST_STATUS,
    LIVE_GATE_EVALUATION_STATUS,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PILOT_CANDIDATE_SOURCE_MILESTONE,
    CONTRACT_CONFORMANCE_SOURCE_MILESTONE,
    PROMPT_LOADING_EFFECT,
    READINESS_GATE_STATUS,
    REVIEW_PACKET_STATUS,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STORAGE_STATUS,
    get_non_runtime_pilot_candidate_readiness_gate_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_readiness_gate.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_readiness_gate_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class NonRuntimePilotCandidateReadinessGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = get_non_runtime_pilot_candidate_readiness_gate_record()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_static_gate_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1")
        self.assertEqual(SCHEMA_VERSION, "3.87-non-runtime-pilot-candidate-readiness-gate")
        self.assertEqual(DESIGN_KIND, "non_runtime_pilot_candidate_readiness_gate_only")
        self.assertEqual(PILOT_CANDIDATE_SOURCE_MILESTONE, "P8")
        self.assertEqual(CONTRACT_CONFORMANCE_SOURCE_MILESTONE, "P9")
        self.assertEqual(READINESS_GATE_STATUS, "static_gate_criteria_declaration_only")
        self.assertEqual(LIVE_GATE_EVALUATION_STATUS, "not_present_in_p10")
        self.assertEqual(REVIEW_PACKET_STATUS, "not_created_in_p10")
        self.assertEqual(LAB_TEST_STATUS, "not_started_in_p10")
        self.assertEqual(self.record.feature_id, FEATURE_ID)
        self.assertEqual(self.record.readiness_gate_status, READINESS_GATE_STATUS)

    def test_effects_review_and_activation_boundaries_are_fixed(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(FIELD_TEST_STATUS, "not_allowed_in_p10")
        self.assertEqual(DEFINITIVE_ENABLEMENT_STATUS, "not_allowed_in_p10")
        self.assertEqual(COPILOT_STATUS, "not_started_in_p10")
        self.assertEqual(LAB_TEST_CODING_STATUS, "not_started_in_p10")

    def test_outcome_names_do_not_grant_authority(self) -> None:
        self.assertEqual(
            set(ALLOWED_GATE_OUTCOMES),
            {"blocked", "not_blocked_for_separate_governed_review_packet_design"},
        )
        forbidden = set(FORBIDDEN_GATE_OUTCOMES)
        for item in (
            "approved",
            "ready",
            "enabled",
            "activated",
            "promoted",
            "runtime_permitted",
            "field_test_enabled",
            "definitive_enablement",
            "copilot_started",
            "lab_test_started",
        ):
            self.assertIn(item, forbidden)
        self.assertEqual({item.outcome_id for item in self.record.allowed_outcomes}, set(ALLOWED_GATE_OUTCOMES))
        self.assertEqual({item.outcome_id for item in self.record.forbidden_outcomes}, forbidden)

    def test_prerequisites_cover_p0_through_p9_and_installer_canon(self) -> None:
        text = "\n".join(item.required_state for item in self.record.prerequisites)
        for phrase in (
            "RG-PILOT-000 router canon frozen",
            "M35 bridge closure frozen",
            "P0 scope charter and entry gate frozen",
            "P1 Pilot boundary frozen",
            "P2 input/output contract design frozen",
            "P3 disagreement taxonomy frozen",
            "P4 reproduction harness design frozen",
            "P5 simulation skeleton design frozen",
            "P6 review evidence design frozen",
            "P7 implementation gate design frozen",
            "P8 non-runtime Pilot candidate frozen",
            "P9 contract conformance frozen",
            "KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 frozen",
        ):
            self.assertIn(phrase, text)
        for item in self.record.prerequisites:
            self.assertEqual(item.failure_policy, "block_progression")

    def test_blocker_classes_include_critical_boundary_and_lab_warning(self) -> None:
        blockers = set(BLOCKER_CLASSES)
        for item in (
            "runtime_authority_leak",
            "prompt_loading_leak",
            "persistence_leak",
            "route_authority_leak",
            "copilot_scope_leak",
            "activation_or_field_test_leak",
            "batch_mode_or_training_data_leak",
            "gold_or_registry_mutation_leak",
            "review_or_human_decision_recording_leak",
            "private_reach_in_or_box_boundary_leak",
            "missing_freeze_or_freeze_memory_status_not_ok",
            "missing_future_review_evidence_packet",
            "missing_future_lab_warning_confirmation",
        ):
            self.assertIn(item, blockers)
        self.assertEqual({item.blocker_id for item in self.record.blockers}, blockers)
        for item in self.record.blockers:
            self.assertEqual(item.effect, "block_progression")

    def test_forbidden_operations_cover_runtime_activation_lab_and_authority(self) -> None:
        forbidden = set(FORBIDDEN_OPERATIONS)
        expected = {
            "evaluate_live_readiness",
            "approve_readiness",
            "mark_ready",
            "enable_candidate",
            "activate_field_test",
            "activate_definitive_enablement",
            "start_lab_test",
            "create_lab_cases",
            "run_lab_test",
            "build_review_packet",
            "collect_evidence",
            "record_human_decision",
            "record_approval",
            "validate_live_payload",
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
            "load_prompt",
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
            "start_lab",
            "build_review_packet",
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
        self.assertEqual(function_names, {"get_non_runtime_pilot_candidate_readiness_gate_record"})

    def test_text_preserves_no_lab_activation_and_future_warning(self) -> None:
        required_phrases = [
            "Non-Runtime Pilot Candidate Readiness Gate v1",
            "static gate criteria declaration only",
            "not a live gate evaluator",
            "not a readiness approval",
            "The test lab is not started in P10",
            "Before any test-lab coding begins, the AI must warn the user",
            "Activation Gate Box after lab testing and maturity evidence",
            "P11 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Review Evidence Packet v1",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_manifest_records_no_live_gate_or_runtime_features(self) -> None:
        prefix = "non_runtime_pilot_candidate_readiness_gate_"
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
        self.assertEqual(self.manifest[prefix + "field_test_status"], "not_allowed_in_p10")
        self.assertEqual(self.manifest[prefix + "definitive_enablement_status"], "not_allowed_in_p10")
        self.assertEqual(self.manifest[prefix + "copilot_status"], "not_started_in_p10")
        self.assertEqual(self.manifest[prefix + "lab_test_coding_status"], "not_started_in_p10")
        forbidden_flags = [
            "contains_live_gate_evaluation",
            "contains_readiness_approval",
            "contains_review_packet_builder",
            "contains_lab_test_coding",
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
            "contains_gold_or_registry_mutation",
            "contains_auto_maturity_jump",
        ]
        for flag in forbidden_flags:
            self.assertFalse(self.manifest[prefix + flag], flag)
        chars = set(self.manifest["protected_architecture_characteristics"])
        self.assertIn("non_runtime_pilot_candidate_readiness_gate", chars)
        self.assertIn("no_lab_test_coding_from_p10", chars)
        self.assertIn("activation_gate_box_deferred_after_lab_testing", chars)


if __name__ == "__main__":
    unittest.main()
