import ast
import contextlib
import io
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_implementation_gate_design import (
    build_shadow_mode_implementation_gate_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_non_runtime_observation import (
    AUTHORITY_NOTICE,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    OBSERVATION_RECORD_KIND,
    SCHEMA_VERSION,
    ShadowObservationContractError,
    build_non_runtime_shadow_observation,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_non_runtime_observation.py"
NOTES = TRANSITION / "shadow_mode_non_runtime_observation_notes.md"
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
    "run_shadow_mode",
    "activate_shadow_mode",
    "start_assistant",
    "start_auxiliar",
    "integrate_runtime_router",
    "load_prompt",
    "write_report",
    "persist_observation",
    "write_gold",
    "write_registry",
    "promote_candidate",
    "compare_routes",
    "select_route",
    "select_prompt",
)

FORBIDDEN_AUTHORITY_OUTPUT_FIELDS = (
    "final_route",
    "route_override",
    "route_to_use",
    "selected_route",
    "selected_prompt",
    "prompt_to_load",
    "approved",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "auxiliar_ready",
    "candidate_promoted",
    "promotion_ready",
    "human_review_completed",
    "confidence",
    "score",
    "probability",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_registry",
    "write_freeze",
    "confirm_and_write",
)


class ShadowModeNonRuntimeObservationTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _valid_input(self):
        return {
            "routing_case_id": "case-001",
            "user_request_summary": "User asks for governed project routing guidance.",
            "current_router_summary": "Current prompt router chooses governed routed work path.",
            "current_router_path_summary": "routed_work_path",
            "current_prompt_group_summary": ["routing", "freeze_guardrails"],
            "scorer_candidate_summary": "Candidate proposes same governed path as non-authoritative evidence.",
            "scorer_constraint_flags_summary": ["requires_freeze_context", "no_runtime_authority"],
            "boundary_context_summary": "Post-Adviser shadow observation remains isolated.",
            "caller_generated_timestamp_utc": "2026-06-18T20:00:00Z",
        }

    def test_manifest_declares_m23_non_runtime_observation_implementation(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_non_runtime_observation_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_non_runtime_observation_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_non_runtime_observation_status"],
            "standard_library_only_non_runtime_in_memory_observation_builder_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_non_runtime_observation_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_requires_m18_boundary"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_requires_m19_io_contract"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_requires_m20_contract_validator_design"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_requires_m21_observation_skeleton_design"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_requires_m22_implementation_gate_design"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_contains_callable_observation_builder"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_contains_fail_closed_local_contract_checks"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_contains_input_processing"])
        self.assertTrue(manifest["shadow_mode_non_runtime_observation_contains_output_generation"])
        for key in (
            "shadow_mode_non_runtime_observation_contains_route_comparison",
            "shadow_mode_non_runtime_observation_contains_runtime_observation_execution",
            "shadow_mode_non_runtime_observation_contains_shadow_activation",
            "shadow_mode_non_runtime_observation_contains_assistant_behavior",
            "shadow_mode_non_runtime_observation_contains_runtime_integration",
            "shadow_mode_non_runtime_observation_contains_router_authority",
            "shadow_mode_non_runtime_observation_contains_prompt_loading",
            "shadow_mode_non_runtime_observation_contains_file_io",
            "shadow_mode_non_runtime_observation_contains_persistence",
            "shadow_mode_non_runtime_observation_contains_report_writer",
            "shadow_mode_non_runtime_observation_contains_gold_or_registry_mutation",
            "shadow_mode_non_runtime_observation_contains_candidate_promotion",
            "shadow_mode_non_runtime_observation_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m22_points_to_m23_and_m23_points_to_m24(self):
        m22 = build_shadow_mode_implementation_gate_design()
        self.assertEqual(
            m22.next_allowed_milestone,
            "M23 - Routing Signal Scorer v3 Non Runtime Shadow Observation Implementation v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M24 - Routing Signal Scorer v3 Shadow Observation Review Evidence Design v1",
        )

    def test_builds_non_runtime_in_memory_observation_from_caller_supplied_primitives(self):
        source = self._valid_input()
        observation = build_non_runtime_shadow_observation(source)
        self.assertEqual(observation["observation_record_kind"], OBSERVATION_RECORD_KIND)
        self.assertEqual(observation["routing_case_id"], "case-001")
        self.assertEqual(observation["contract_schema_version"], SCHEMA_VERSION)
        self.assertEqual(observation["authority_notice"], AUTHORITY_NOTICE)
        self.assertEqual(observation["route_path_difference_observed"], False)
        self.assertEqual(
            observation["constraint_flags_observed"],
            ["requires_freeze_context", "no_runtime_authority"],
        )
        self.assertEqual(observation["requires_separate_human_review"], True)
        self.assertIn(
            "non_runtime_shadow_observation_requires_separate_human_review",
            observation["human_review_reason_summary"],
        )
        self.assertEqual(observation["storage_status"], "not_persisted_by_shadow_observation")
        self.assertEqual(observation["routing_effect"], "none")
        self.assertEqual(observation["prompt_loading_effect"], "none")
        self.assertEqual(observation["candidate_promotion_effect"], "none")
        self.assertEqual(observation["runtime_authority"], "not_granted")
        self.assertEqual(observation["shadow_mode_status"], "not_active")
        self.assertEqual(observation["assistant_status"], "not_started")
        for forbidden in FORBIDDEN_AUTHORITY_OUTPUT_FIELDS:
            self.assertNotIn(forbidden, observation)

    def test_output_copies_lists_and_does_not_mutate_input(self):
        source = self._valid_input()
        original_flags = list(source["scorer_constraint_flags_summary"])
        observation = build_non_runtime_shadow_observation(source)
        observation["constraint_flags_observed"].append("changed")
        self.assertEqual(source["scorer_constraint_flags_summary"], original_flags)

    def test_fails_closed_on_unknown_authority_missing_and_non_primitive_inputs(self):
        bad_unknown = self._valid_input()
        bad_unknown["unknown"] = "x"
        with self.assertRaisesRegex(ShadowObservationContractError, "unknown_input_field"):
            build_non_runtime_shadow_observation(bad_unknown)

        bad_authority = self._valid_input()
        bad_authority["selected_prompt"] = "load_this"
        with self.assertRaisesRegex(ShadowObservationContractError, "authority_field_is_forbidden"):
            build_non_runtime_shadow_observation(bad_authority)

        bad_missing = self._valid_input()
        del bad_missing["routing_case_id"]
        with self.assertRaisesRegex(ShadowObservationContractError, "missing_required_input_field"):
            build_non_runtime_shadow_observation(bad_missing)

        bad_blank = self._valid_input()
        bad_blank["routing_case_id"] = "   "
        with self.assertRaisesRegex(ShadowObservationContractError, "required_input_field_must_not_be_blank"):
            build_non_runtime_shadow_observation(bad_blank)

        bad_live_object = self._valid_input()
        bad_live_object["current_router_summary"] = object()
        with self.assertRaisesRegex(ShadowObservationContractError, "input_field_must_be_string"):
            build_non_runtime_shadow_observation(bad_live_object)

        bad_list = self._valid_input()
        bad_list["scorer_constraint_flags_summary"] = ["ok", object()]
        with self.assertRaisesRegex(ShadowObservationContractError, "input_list_items_must_be_strings"):
            build_non_runtime_shadow_observation(bad_list)

    def test_public_exports_are_limited_to_observation_builder_and_error(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(
            namespace["__all__"],
            ["ShadowObservationContractError", "build_non_runtime_shadow_observation"],
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
            observation = build_non_runtime_shadow_observation(self._valid_input())
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(observation["storage_status"], "not_persisted_by_shadow_observation")
        self.assertEqual(observation["routing_effect"], "none")
        self.assertEqual(observation["runtime_authority"], "not_granted")

    def test_notes_exist_and_preserve_m23_safety_stop_boundaries(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M23 is the first implementation milestone",
            "pure in-memory helper",
            "M23 does not activate shadow mode.",
            "M23 does not start Auxiliar/Assistant behavior.",
            "fails closed on unknown input fields",
            "The next allowed milestone is M24",
        )
        for snippet in required:
            self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
