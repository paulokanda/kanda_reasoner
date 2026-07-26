from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.non_runtime_pilot_candidate_review_evidence_packet import (
    ACTIVATION_EFFECT,
    COPILOT_STATUS,
    CRITICAL_BOUNDARY_ERROR_BUDGET,
    DEFINITIVE_ENABLEMENT_STATUS,
    DESIGN_KIND,
    EVIDENCE_COLLECTION_STATUS,
    FEATURE_ID,
    FIELD_TEST_STATUS,
    FORBIDDEN_OPERATIONS,
    FORBIDDEN_PACKET_CLAIMS,
    HUMAN_DECISION_RECORDING_STATUS,
    HUMAN_REVIEW_MANDATORY,
    LAB_TEST_CODING_STATUS,
    LAB_TEST_STATUS,
    OPT_IN_PER_INVOCATION_REQUIRED,
    PACKET_BUILDER_STATUS,
    PACKET_PERSISTENCE_STATUS,
    PILOT_CANDIDATE_SOURCE_MILESTONE,
    CONTRACT_CONFORMANCE_SOURCE_MILESTONE,
    READINESS_GATE_SOURCE_MILESTONE,
    PROMPT_LOADING_EFFECT,
    REQUIRED_PACKET_SOURCE_FREEZES,
    REVIEW_EVIDENCE_PACKET_STATUS,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STATIC_EVIDENCE_SECTIONS,
    STORAGE_STATUS,
    get_non_runtime_pilot_candidate_review_evidence_packet_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_review_evidence_packet.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "non_runtime_pilot_candidate_review_evidence_packet_notes.md"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class NonRuntimePilotCandidateReviewEvidencePacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = get_non_runtime_pilot_candidate_review_evidence_packet_record()
        self.source = MODULE.read_text(encoding="utf-8")
        self.notes = NOTES.read_text(encoding="utf-8")
        self.readme = README.read_text(encoding="utf-8")
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.combined = "\\n".join([self.source, self.notes, self.readme, json.dumps(self.manifest, sort_keys=True)])

    def test_identity_and_static_packet_status(self) -> None:
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1")
        self.assertEqual(SCHEMA_VERSION, "3.88-non-runtime-pilot-candidate-review-evidence-packet")
        self.assertEqual(DESIGN_KIND, "non_runtime_pilot_candidate_review_evidence_packet_only")
        self.assertEqual(PILOT_CANDIDATE_SOURCE_MILESTONE, "P8")
        self.assertEqual(CONTRACT_CONFORMANCE_SOURCE_MILESTONE, "P9")
        self.assertEqual(READINESS_GATE_SOURCE_MILESTONE, "P10")
        self.assertEqual(REVIEW_EVIDENCE_PACKET_STATUS, "static_packet_shape_declaration_only")
        self.assertEqual(EVIDENCE_COLLECTION_STATUS, "not_present_in_p11")
        self.assertEqual(PACKET_BUILDER_STATUS, "not_present_in_p11")
        self.assertEqual(PACKET_PERSISTENCE_STATUS, "not_present_in_p11")
        self.assertEqual(HUMAN_DECISION_RECORDING_STATUS, "not_present_in_p11")
        self.assertEqual(LAB_TEST_STATUS, "not_started_in_p11")
        self.assertEqual(self.record.feature_id, FEATURE_ID)
        self.assertEqual(self.record.review_evidence_packet_status, REVIEW_EVIDENCE_PACKET_STATUS)

    def test_effects_review_and_activation_boundaries_are_fixed(self) -> None:
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertTrue(HUMAN_REVIEW_MANDATORY)
        self.assertTrue(OPT_IN_PER_INVOCATION_REQUIRED)
        self.assertEqual(CRITICAL_BOUNDARY_ERROR_BUDGET, 0)
        self.assertEqual(FIELD_TEST_STATUS, "not_allowed_in_p11")
        self.assertEqual(DEFINITIVE_ENABLEMENT_STATUS, "not_allowed_in_p11")
        self.assertEqual(COPILOT_STATUS, "not_started_in_p11")
        self.assertEqual(LAB_TEST_CODING_STATUS, "not_started_in_p11")

    def test_static_sections_are_declared_but_not_populated(self) -> None:
        expected = {
            "freeze_lineage_p0_through_p10",
            "non_runtime_candidate_identity",
            "contract_conformance_declaration",
            "readiness_gate_criteria_snapshot",
            "unsafe_boundary_preservation_checklist",
            "match_before_disagree_requirement",
            "critical_boundary_error_budget_zero",
            "future_human_review_placeholder",
            "future_lab_warning_requirement",
            "activation_gate_deferred_notice",
        }
        self.assertEqual(set(STATIC_EVIDENCE_SECTIONS), expected)
        self.assertEqual({item.section_id for item in self.record.sections}, expected)
        for item in self.record.sections:
            self.assertEqual(item.status, "declared_only_not_populated_in_p11")
            self.assertEqual(item.failure_policy, "block_progression")

    def test_required_source_freezes_cover_p0_through_p10(self) -> None:
        text = "\\n".join(REQUIRED_PACKET_SOURCE_FREEZES)
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
        ):
            self.assertIn(phrase, text)
        self.assertEqual(self.record.required_source_freezes, REQUIRED_PACKET_SOURCE_FREEZES)

    def test_forbidden_claims_and_operations_block_authority(self) -> None:
        claims = set(FORBIDDEN_PACKET_CLAIMS)
        for item in (
            "review_approved",
            "human_decision_recorded",
            "evidence_collected",
            "packet_built_from_live_case",
            "packet_persisted",
            "candidate_ready",
            "field_test_enabled",
            "definitive_enablement",
            "pilot_runtime_enabled",
            "copilot_started",
            "lab_test_started",
        ):
            self.assertIn(item, claims)
        self.assertEqual(set(self.record.boundary.forbidden_claims), claims)
        forbidden = set(FORBIDDEN_OPERATIONS)
        expected = {
            "collect_evidence",
            "build_review_packet",
            "assemble_packet",
            "generate_packet",
            "write_packet",
            "write_report",
            "write_review_queue",
            "persist_record",
            "record_human_decision",
            "record_approval",
            "approve_review",
            "mark_ready",
            "activate_field_test",
            "activate_definitive_enablement",
            "start_lab_test",
            "create_lab_cases",
            "run_lab_test",
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
        imported_names = "\\n".join(ast.get_source_segment(self.source, node) or "" for node in imports)
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
        self.assertEqual(function_names, {"get_non_runtime_pilot_candidate_review_evidence_packet_record"})

    def test_text_preserves_no_packet_builder_lab_or_activation(self) -> None:
        required_phrases = [
            "Non-Runtime Pilot Candidate Review Evidence Packet v1",
            "static packet shape declaration only",
            "not an evidence collector",
            "not a packet builder",
            "The test lab is not started in P11",
            "Before any test-lab coding begins, the AI must warn the user",
            "Activation Gate Box after lab testing and maturity evidence",
            "P12 - Routing Signal Scorer v3 Pilot Phase Closure / Copilot Boundary Entry Gate v1",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.combined)

    def test_manifest_records_no_packet_builder_or_runtime_features(self) -> None:
        prefix = "non_runtime_pilot_candidate_review_evidence_packet_"
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
        self.assertEqual(self.manifest[prefix + "field_test_status"], "not_allowed_in_p11")
        self.assertEqual(self.manifest[prefix + "definitive_enablement_status"], "not_allowed_in_p11")
        self.assertEqual(self.manifest[prefix + "copilot_status"], "not_started_in_p11")
        self.assertEqual(self.manifest[prefix + "lab_test_coding_status"], "not_started_in_p11")
        forbidden_flags = [
            "contains_evidence_collection",
            "contains_packet_builder",
            "contains_packet_population",
            "contains_packet_persistence",
            "contains_report_writer",
            "contains_review_queue_writer",
            "contains_human_decision_recording",
            "contains_readiness_approval",
            "contains_live_gate_evaluation",
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
        self.assertIn("non_runtime_pilot_candidate_review_evidence_packet", chars)
        self.assertIn("no_packet_builder_from_p11", chars)
        self.assertIn("no_lab_test_coding_from_p11", chars)
        self.assertIn("activation_gate_box_deferred_after_lab_testing", chars)


if __name__ == "__main__":
    unittest.main()
