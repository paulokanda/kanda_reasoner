import ast
import contextlib
import io
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_assistance_review_evidence_design import (
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    AssistanceReviewEvidenceBoundaryDesign,
    AssistanceReviewEvidenceFieldDesign,
    AuxiliarAssistantAssistanceReviewEvidenceDesign,
    build_auxiliar_assistant_assistance_review_evidence_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_non_runtime_assistance import (
    NEXT_ALLOWED_MILESTONE as M31_NEXT_ALLOWED_MILESTONE,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_review_evidence_design.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_assistance_review_evidence_notes.md"
MANIFEST = BOX / "box_manifest.json"

FORBIDDEN_IMPORT_PREFIXES = (
    "os",
    "sys",
    "pathlib",
    "subprocess",
    "socket",
    "threading",
    "multiprocessing",
    "tempfile",
    "importlib",
    "pickle",
    "shelve",
    "sqlite3",
    "requests",
    "httpx",
    "aiohttp",
    "kanda_reasoner_app.routing_signal_scorer.contract",
    "kanda_reasoner_app.routing_signal_scorer.runtime",
    "kanda_reasoner_app.routing_signal_scorer.router",
    "kanda_reasoner_app.prompt_loader",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.project_freeze_ledger",
)

FORBIDDEN_CALLS = (
    "open",
    "print",
    "eval",
    "exec",
    "compile",
    "__import__",
    "getenv",
    "putenv",
    "system",
    "popen",
    "import_module",
)

FORBIDDEN_RUNTIME_BEHAVIOR_DEFS = (
    "build_review_evidence",
    "validate_review_evidence",
    "transform_assistance",
    "run_assistant",
    "activate_assistant",
    "start_assistant",
    "start_auxiliar",
    "run_shadow_mode",
    "activate_shadow_mode",
    "integrate_runtime_router",
    "load_prompt",
    "select_prompt",
    "select_route",
    "compare_routes",
    "write_report",
    "persist_evidence",
    "write_review_queue",
    "record_human_decision",
    "write_gold",
    "write_registry",
    "promote_candidate",
)

FORBIDDEN_BEHAVIOR_MARKERS = (
    "live_review_evidence_builder",
    "assistance_transformation_execution",
    "live_input_validation_execution",
    "live_assistance_execution",
    "route_comparison",
    "route_selection",
    "runtime_state_inspection",
    "runtime_router_import",
    "runtime_router_export",
    "prompt_selection",
    "prompt_loading",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "review_queue_writing",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "human_decision_recording",
    "approval_recording",
    "rejection_recording",
    "override_recording",
    "patch_execution",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
    "shadow_mode_activation",
    "assistant_activation",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
    "pilot_behavior",
)


class AuxiliarAssistantAssistanceReviewEvidenceDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m32_assistance_review_evidence_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "auxiliar_assistant_assistance_review_evidence_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest[f"{prefix}_status"],
            "immutable_design_only_assistance_review_evidence_field_design_no_live_builder_no_persistence_no_runtime_authority",
        )
        self.assertEqual(manifest[f"{prefix}_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        for key in (
            f"{prefix}_requires_m18_boundary",
            f"{prefix}_requires_m19_io_contract",
            f"{prefix}_requires_m20_contract_validator_design",
            f"{prefix}_requires_m21_observation_skeleton_design",
            f"{prefix}_requires_m22_implementation_gate_design",
            f"{prefix}_requires_m23_non_runtime_observation",
            f"{prefix}_requires_m24_review_evidence_design",
            f"{prefix}_requires_m25_readiness_gate_design",
            f"{prefix}_requires_m26_auxiliar_assistant_boundary_design",
            f"{prefix}_requires_m27_auxiliar_assistant_io_contract_design",
            f"{prefix}_requires_m28_auxiliar_assistant_contract_validator_design",
            f"{prefix}_requires_m29_auxiliar_assistant_assistance_skeleton_design",
            f"{prefix}_requires_m30_auxiliar_assistant_implementation_gate_design",
            f"{prefix}_requires_m31_non_runtime_auxiliar_assistant_assistance",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            f"{prefix}_contains_callable_review_evidence_builder",
            f"{prefix}_contains_live_review_evidence_builder",
            f"{prefix}_contains_live_input_validation_execution",
            f"{prefix}_contains_live_assistance_execution",
            f"{prefix}_contains_assistance_transformation_execution",
            f"{prefix}_contains_route_comparison",
            f"{prefix}_contains_route_selection",
            f"{prefix}_contains_prompt_selection",
            f"{prefix}_contains_prompt_loading",
            f"{prefix}_contains_runtime_integration",
            f"{prefix}_contains_router_authority",
            f"{prefix}_contains_file_io",
            f"{prefix}_contains_persistence",
            f"{prefix}_contains_report_writer",
            f"{prefix}_contains_review_queue_writer",
            f"{prefix}_contains_human_decision_recording",
            f"{prefix}_contains_gold_or_registry_mutation",
            f"{prefix}_contains_candidate_promotion",
            f"{prefix}_contains_embeddings_or_providers",
            f"{prefix}_contains_shadow_activation",
            f"{prefix}_contains_assistant_activation",
            f"{prefix}_contains_assistant_behavior",
            f"{prefix}_contains_auxiliar_behavior",
            f"{prefix}_contains_copilot_behavior",
            f"{prefix}_contains_pilot_behavior",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m31_points_to_m32_and_m32_points_to_m33(self):
        self.assertEqual(
            M31_NEXT_ALLOWED_MILESTONE,
            "M32 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M33 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review v1",
        )

    def test_returns_static_immutable_design_record(self):
        first = build_auxiliar_assistant_assistance_review_evidence_design()
        second = build_auxiliar_assistant_assistance_review_evidence_design()
        self.assertIs(first, second)
        self.assertIsInstance(first, AuxiliarAssistantAssistanceReviewEvidenceDesign)
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, "post_adviser_auxiliar_assistant_assistance_review_evidence_design_only")
        self.assertEqual(first.milestone, "M32")
        self.assertEqual(first.live_evidence_builder_status, "not_implemented")
        self.assertEqual(first.persistence_status, "not_implemented_no_storage_target")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        self.assertEqual(
            first.implementation_gate,
            "blocked_until_separate_m33_scope_confirmation_validation_and_freeze",
        )

    def test_design_fields_are_for_m31_source_assistance_and_non_authoritative_effects(self):
        design = build_auxiliar_assistant_assistance_review_evidence_design()
        self.assertIn("assistance_record_kind", design.allowed_source_assistance_fields)
        self.assertIn("assistant_case_id", design.allowed_source_assistance_fields)
        self.assertIn("boundary_questions_for_human_review", design.allowed_source_assistance_fields)
        self.assertIn("safety_flags_for_human_review", design.allowed_source_assistance_fields)
        self.assertIn("assistant_activation_effect", design.allowed_source_assistance_fields)
        field_names = {field.name for field in design.future_review_evidence_fields}
        for required in (
            "assistance_review_evidence_record_kind",
            "assistant_case_id",
            "source_assistance_schema_version",
            "human_review_context_summary",
            "boundary_questions_for_review",
            "safety_flags_for_review",
            "missing_information_summary",
            "authority_notice",
            "review_storage_design_status",
            "requires_separate_human_review",
            "routing_effect",
            "prompt_loading_effect",
            "assistant_activation_effect",
        ):
            self.assertIn(required, field_names)
        for field in design.future_review_evidence_fields:
            self.assertIsInstance(field, AssistanceReviewEvidenceFieldDesign)
        for boundary in design.review_boundary_rules:
            self.assertIsInstance(boundary, AssistanceReviewEvidenceBoundaryDesign)
        boundary_ids = {boundary.boundary_id for boundary in design.review_boundary_rules}
        self.assertIn("source_must_be_m31_non_runtime_assistance", boundary_ids)
        self.assertIn("assistance_review_evidence_is_not_human_decision", boundary_ids)
        self.assertIn("assistance_review_evidence_is_not_persistence", boundary_ids)
        self.assertIn("assistance_review_evidence_is_not_assistant_activation", boundary_ids)

    def test_design_requires_m18_through_m31_and_keeps_m33_separate(self):
        design = build_auxiliar_assistant_assistance_review_evidence_design()
        for prior in (
            "m18_shadow_mode_boundary_design_frozen",
            "m19_shadow_mode_input_output_contract_design_frozen",
            "m20_shadow_mode_contract_validator_design_frozen",
            "m21_shadow_mode_observation_skeleton_design_frozen",
            "m22_shadow_mode_implementation_gate_design_frozen",
            "m23_non_runtime_shadow_observation_implementation_frozen",
            "m24_shadow_observation_review_evidence_design_frozen",
            "m25_shadow_mode_assistant_boundary_readiness_gate_design_frozen",
            "m26_auxiliar_assistant_boundary_design_frozen",
            "m27_auxiliar_assistant_input_output_contract_design_frozen",
            "m28_auxiliar_assistant_contract_validator_design_frozen",
            "m29_auxiliar_assistant_assistance_skeleton_design_frozen",
            "m30_auxiliar_assistant_implementation_gate_design_frozen",
            "m31_non_runtime_auxiliar_assistant_assistance_implementation_frozen",
        ):
            self.assertIn(prior, design.required_prior_milestones)
        self.assertIn("m33_requires_separate_human_scope_confirmation", design.review_evidence_invariants)

    def test_forbidden_behaviors_are_explicitly_blocked(self):
        design = build_auxiliar_assistant_assistance_review_evidence_design()
        for forbidden in FORBIDDEN_BEHAVIOR_MARKERS:
            self.assertIn(forbidden, design.forbidden_review_evidence_behaviors)
        for invariant in (
            "m32_is_design_only",
            "m32_has_no_live_review_evidence_builder",
            "m32_does_not_transform_or_validate_live_m31_assistance_records",
            "m32_does_not_persist_write_enqueue_or_report_review_evidence",
            "m32_does_not_record_human_decisions_or_decision_outcomes",
            "m32_does_not_select_routes_or_prompts",
            "m32_does_not_start_auxiliar_assistant_or_pilot_copilot_behavior",
            "m32_does_not_activate_shadow_mode_or_assistant_behavior",
            "m32_does_not_grant_runtime_router_or_prompt_loader_authority",
            "candidate_promotion_remains_blocked",
            "shadow_mode_remains_inactive",
            "assistant_auxiliar_pilot_copilot_remain_not_started",
        ):
            self.assertIn(invariant, design.review_evidence_invariants)

    def test_module_has_no_runtime_imports_or_forbidden_calls(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertFalse(
                        alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES),
                        f"forbidden import: {alias.name}",
                    )
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self.assertFalse(
                    module.startswith(FORBIDDEN_IMPORT_PREFIXES),
                    f"forbidden import-from: {module}",
                )
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                self.assertNotIn(name, FORBIDDEN_CALLS)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.assertNotIn(node.name, FORBIDDEN_RUNTIME_BEHAVIOR_DEFS)

    def test_no_stdout_side_effects_and_notes_state_design_only(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            design = build_auxiliar_assistant_assistance_review_evidence_design()
        self.assertEqual(buffer.getvalue(), "")
        self.assertEqual(design.live_evidence_builder_status, "not_implemented")
        notes = NOTES.read_text(encoding="utf-8")
        self.assertIn("design-only", notes)
        self.assertIn("does not", notes)
        self.assertIn("M33 requires", notes)


if __name__ == "__main__":
    unittest.main()
