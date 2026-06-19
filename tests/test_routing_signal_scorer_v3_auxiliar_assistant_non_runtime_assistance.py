import ast
import contextlib
import io
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_implementation_gate_design import (
    build_auxiliar_assistant_implementation_gate_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_auxiliar_assistant_non_runtime_assistance import (
    ASSISTANCE_RECORD_KIND,
    AUTHORITY_NOTICE,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    AuxiliarAssistantAssistanceContractError,
    build_non_runtime_auxiliar_assistant_assistance,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_auxiliar_assistant_non_runtime_assistance.py"
NOTES = TRANSITION / "shadow_mode_auxiliar_assistant_non_runtime_assistance_notes.md"
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
    "persist_assistance",
    "record_human_decision",
    "write_gold",
    "write_registry",
    "promote_candidate",
)

FORBIDDEN_AUTHORITY_OUTPUT_FIELDS = (
    "final_route",
    "route_override",
    "route_to_use",
    "selected_route",
    "selected_prompt",
    "prompt_to_load",
    "prompts_to_load",
    "approved",
    "rejected",
    "overridden",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "auxiliar_ready",
    "candidate_promoted",
    "promotion_ready",
    "human_review_completed",
    "human_decision",
    "human_decision_recorded",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_registry",
    "write_review_queue",
    "write_freeze",
    "confirm_and_write",
    "persist_record",
    "router_authority_granted",
    "runtime_effect",
)


class AuxiliarAssistantNonRuntimeAssistanceTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _valid_input(self):
        return {
            "assistant_case_id": "assistant-case-001",
            "boundary_context_summary": "M26-M30 boundaries are frozen and Assistant remains inactive.",
            "validated_shadow_observation_summary": "M23 observation is non-runtime and in-memory only.",
            "review_evidence_summary": "M24 review evidence design remains design-only.",
            "current_router_outcome_summary": "Current router outcome remains governed routed work path.",
            "requested_support_kind": "boundary_review",
            "known_boundary_flags_summary": "no_runtime_authority; no_prompt_loading",
            "caller_generated_timestamp_utc": "2026-06-18T21:40:00Z",
        }

    def test_manifest_declares_m31_non_runtime_assistance_implementation(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["auxiliar_assistant_non_runtime_assistance_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["auxiliar_assistant_non_runtime_assistance_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["auxiliar_assistant_non_runtime_assistance_status"],
            "standard_library_only_non_runtime_in_memory_assistance_builder_no_runtime_authority",
        )
        self.assertEqual(
            manifest["auxiliar_assistant_non_runtime_assistance_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        for key in (
            "auxiliar_assistant_non_runtime_assistance_requires_m18_boundary",
            "auxiliar_assistant_non_runtime_assistance_requires_m19_io_contract",
            "auxiliar_assistant_non_runtime_assistance_requires_m20_contract_validator_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m21_observation_skeleton_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m22_implementation_gate_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m23_non_runtime_observation",
            "auxiliar_assistant_non_runtime_assistance_requires_m24_review_evidence_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m25_readiness_gate_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m26_auxiliar_assistant_boundary_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m27_auxiliar_assistant_io_contract_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m28_auxiliar_assistant_contract_validator_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m29_auxiliar_assistant_assistance_skeleton_design",
            "auxiliar_assistant_non_runtime_assistance_requires_m30_auxiliar_assistant_implementation_gate_design",
            "auxiliar_assistant_non_runtime_assistance_contains_callable_assistance_builder",
            "auxiliar_assistant_non_runtime_assistance_contains_fail_closed_local_contract_checks",
            "auxiliar_assistant_non_runtime_assistance_contains_input_processing",
            "auxiliar_assistant_non_runtime_assistance_contains_output_generation",
        ):
            self.assertIs(manifest[key], True, key)
        for key in (
            "auxiliar_assistant_non_runtime_assistance_contains_live_assistant",
            "auxiliar_assistant_non_runtime_assistance_contains_assistant_behavior",
            "auxiliar_assistant_non_runtime_assistance_contains_auxiliar_behavior",
            "auxiliar_assistant_non_runtime_assistance_contains_copilot_behavior",
            "auxiliar_assistant_non_runtime_assistance_contains_assistant_activation",
            "auxiliar_assistant_non_runtime_assistance_contains_shadow_activation",
            "auxiliar_assistant_non_runtime_assistance_contains_route_comparison",
            "auxiliar_assistant_non_runtime_assistance_contains_route_selection",
            "auxiliar_assistant_non_runtime_assistance_contains_prompt_selection",
            "auxiliar_assistant_non_runtime_assistance_contains_prompt_loading",
            "auxiliar_assistant_non_runtime_assistance_contains_runtime_integration",
            "auxiliar_assistant_non_runtime_assistance_contains_router_authority",
            "auxiliar_assistant_non_runtime_assistance_contains_file_io",
            "auxiliar_assistant_non_runtime_assistance_contains_persistence",
            "auxiliar_assistant_non_runtime_assistance_contains_report_writer",
            "auxiliar_assistant_non_runtime_assistance_contains_review_queue_writer",
            "auxiliar_assistant_non_runtime_assistance_contains_human_decision_recording",
            "auxiliar_assistant_non_runtime_assistance_contains_gold_or_registry_mutation",
            "auxiliar_assistant_non_runtime_assistance_contains_candidate_promotion",
            "auxiliar_assistant_non_runtime_assistance_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m30_points_to_m31_and_m31_points_to_m32(self):
        m30 = build_auxiliar_assistant_implementation_gate_design()
        self.assertEqual(
            m30.next_allowed_milestone,
            "M31 - Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M32 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1",
        )

    def test_builds_non_runtime_in_memory_assistance_from_caller_supplied_primitives(self):
        assistance = build_non_runtime_auxiliar_assistant_assistance(self._valid_input())
        self.assertEqual(assistance["assistance_record_kind"], ASSISTANCE_RECORD_KIND)
        self.assertEqual(assistance["assistant_case_id"], "assistant-case-001")
        self.assertEqual(assistance["contract_schema_version"], SCHEMA_VERSION)
        self.assertEqual(assistance["authority_notice"], AUTHORITY_NOTICE)
        self.assertIn("human review only", assistance["human_review_context_summary"])
        self.assertIn("assistant-case-001", assistance["human_review_context_summary"])
        self.assertIsInstance(assistance["boundary_questions_for_human_review"], tuple)
        self.assertGreaterEqual(len(assistance["boundary_questions_for_human_review"]), 3)
        self.assertIn("no_runtime_authority", assistance["safety_flags_for_human_review"])
        self.assertIn("caller_supplied_boundary_flags_present_for_human_review", assistance["safety_flags_for_human_review"])
        self.assertEqual(assistance["requires_separate_human_review"], True)
        self.assertEqual(assistance["storage_status"], "not_persisted_by_auxiliar_assistant_assistance")
        self.assertEqual(assistance["routing_effect"], "none")
        self.assertEqual(assistance["prompt_loading_effect"], "none")
        self.assertEqual(assistance["assistant_activation_effect"], "none")
        for forbidden in FORBIDDEN_AUTHORITY_OUTPUT_FIELDS:
            self.assertNotIn(forbidden, assistance)

    def test_output_is_independent_and_does_not_mutate_input(self):
        source = self._valid_input()
        assistance = build_non_runtime_auxiliar_assistant_assistance(source)
        assistance["safety_flags_for_human_review"] += ("changed",)
        self.assertEqual(source["known_boundary_flags_summary"], "no_runtime_authority; no_prompt_loading")

    def test_all_allowed_support_kinds_build_non_authoritative_records(self):
        for support_kind in (
            "boundary_review",
            "evidence_summary",
            "safety_question_generation",
            "missing_information_review",
        ):
            payload = self._valid_input()
            payload["requested_support_kind"] = support_kind
            assistance = build_non_runtime_auxiliar_assistant_assistance(payload)
            self.assertEqual(assistance["assistance_record_kind"], ASSISTANCE_RECORD_KIND)
            self.assertEqual(assistance["requires_separate_human_review"], True)
            self.assertEqual(assistance["routing_effect"], "none")
            self.assertEqual(assistance["assistant_activation_effect"], "none")

    def test_fails_closed_on_unknown_authority_missing_blank_non_string_and_unsupported_inputs(self):
        bad_unknown = self._valid_input()
        bad_unknown["unknown"] = "x"
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "unknown_input_field"):
            build_non_runtime_auxiliar_assistant_assistance(bad_unknown)

        bad_authority = self._valid_input()
        bad_authority["selected_prompt"] = "load_this"
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "authority_field_is_forbidden"):
            build_non_runtime_auxiliar_assistant_assistance(bad_authority)

        bad_missing = self._valid_input()
        del bad_missing["assistant_case_id"]
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "missing_required_input_field"):
            build_non_runtime_auxiliar_assistant_assistance(bad_missing)

        bad_blank = self._valid_input()
        bad_blank["assistant_case_id"] = "   "
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "required_input_field_must_not_be_blank"):
            build_non_runtime_auxiliar_assistant_assistance(bad_blank)

        bad_live_object = self._valid_input()
        bad_live_object["current_router_outcome_summary"] = object()
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "input_field_must_be_string"):
            build_non_runtime_auxiliar_assistant_assistance(bad_live_object)

        bad_support = self._valid_input()
        bad_support["requested_support_kind"] = "recommend_route"
        with self.assertRaisesRegex(AuxiliarAssistantAssistanceContractError, "unsupported_non_authoritative_support_kind"):
            build_non_runtime_auxiliar_assistant_assistance(bad_support)

    def test_public_exports_are_limited_to_assistance_builder_and_error(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(
            namespace["__all__"],
            [
                "AuxiliarAssistantAssistanceContractError",
                "build_non_runtime_auxiliar_assistant_assistance",
            ],
        )
        text = MODULE.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_RUNTIME_BEHAVIOR_DEFS:
            self.assertNotIn("def " + forbidden, text)

    def test_ast_rejects_forbidden_imports_and_side_effect_calls(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prefix in FORBIDDEN_IMPORT_PREFIXES:
                        self.assertFalse(alias.name == prefix or alias.name.startswith(prefix + "."), alias.name)
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    self.assertFalse(module == prefix or module.startswith(prefix + "."), module)
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                self.assertNotIn(name, FORBIDDEN_CALLS)

    def test_builder_has_no_file_console_or_runtime_side_effects(self):
        before = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            assistance = build_non_runtime_auxiliar_assistant_assistance(self._valid_input())
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(assistance["storage_status"], "not_persisted_by_auxiliar_assistant_assistance")
        self.assertEqual(assistance["routing_effect"], "none")
        self.assertEqual(assistance["assistant_activation_effect"], "none")

    def test_notes_exist_and_preserve_m31_safety_stop_boundaries(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M31 is the first narrow implementation milestone",
            "pure in-memory helper",
            "M31 does not activate Assistant behavior.",
            "M31 does not start Auxiliar behavior.",
            "fails closed on unknown input fields",
            "The next allowed milestone is M32",
        )
        for snippet in required:
            self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
