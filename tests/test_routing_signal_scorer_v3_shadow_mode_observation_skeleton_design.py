import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_boundary_design import (
    build_shadow_mode_boundary_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_contract_validator_design import (
    build_shadow_mode_contract_validator_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_io_contract_design import (
    build_shadow_mode_io_contract_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_observation_skeleton_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_observation_skeleton_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_observation_skeleton_design.py"
NOTES = TRANSITION / "shadow_mode_observation_skeleton_notes.md"
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

FORBIDDEN_LIVE_BEHAVIOR_DEFS = (
    "build_shadow_observation",
    "run_shadow_observation",
    "observe_shadow_case",
    "validate_shadow_mode_input",
    "validate_shadow_mode_output",
    "process_input",
    "generate_output",
    "execute_observation",
    "compare_routes",
    "load_prompt",
    "write_report",
    "persist_observation",
    "promote_candidate",
    "activate_shadow_mode",
    "start_assistant",
)


class ShadowModeObservationSkeletonDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _slot_ids(self, slots):
        return {slot.slot_id for slot in slots}

    def test_manifest_declares_m21_skeleton_design_without_live_behavior(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_observation_skeleton_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_observation_skeleton_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_observation_skeleton_design_status"],
            "immutable_design_only_observation_skeleton_no_callable_builder_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_observation_skeleton_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        for key in (
            "shadow_mode_observation_skeleton_design_contains_callable_observation_entrypoint",
            "shadow_mode_observation_skeleton_design_contains_live_validation_execution",
            "shadow_mode_observation_skeleton_design_contains_input_processing",
            "shadow_mode_observation_skeleton_design_contains_output_generation",
            "shadow_mode_observation_skeleton_design_contains_observation_execution",
            "shadow_mode_observation_skeleton_design_contains_route_comparison",
            "shadow_mode_observation_skeleton_design_contains_shadow_activation",
            "shadow_mode_observation_skeleton_design_contains_assistant_behavior",
            "shadow_mode_observation_skeleton_design_contains_runtime_integration",
            "shadow_mode_observation_skeleton_design_contains_router_authority",
            "shadow_mode_observation_skeleton_design_contains_prompt_loading",
            "shadow_mode_observation_skeleton_design_contains_file_io",
            "shadow_mode_observation_skeleton_design_contains_persistence",
            "shadow_mode_observation_skeleton_design_contains_report_writer",
            "shadow_mode_observation_skeleton_design_contains_gold_or_registry_mutation",
            "shadow_mode_observation_skeleton_design_contains_candidate_promotion",
            "shadow_mode_observation_skeleton_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_observation_skeleton_record_is_immutable_static_and_design_only(self):
        m18 = build_shadow_mode_boundary_design()
        m19 = build_shadow_mode_io_contract_design()
        m20 = build_shadow_mode_contract_validator_design()
        self.assertEqual(m18.next_allowed_milestone, "M19 - Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1")
        self.assertEqual(m19.next_allowed_milestone, "M20 - Routing Signal Scorer v3 Shadow Mode Contract Validator Design v1")
        self.assertEqual(m20.next_allowed_milestone, "M21 - Routing Signal Scorer v3 Shadow Mode Observation Skeleton Design v1")
        first = build_shadow_mode_observation_skeleton_design()
        second = build_shadow_mode_observation_skeleton_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M21")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "design_only_no_observation_execution")
        self.assertEqual(first.skeleton_design_status, "static_skeleton_design_only_no_observation_function")
        self.assertEqual(first.live_validation_status, "not_implemented")
        self.assertEqual(first.observation_execution_status, "not_implemented")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        with self.assertRaises(FrozenInstanceError):
            first.feature_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.future_skeleton_slots[0].slot_id = "changed"

    def test_preconditions_require_m18_m19_m20_and_future_human_review(self):
        record = build_shadow_mode_observation_skeleton_design()
        for expected in (
            "m18_shadow_mode_boundary_design_frozen",
            "m19_shadow_mode_input_output_contract_design_frozen",
            "m20_shadow_mode_contract_validator_design_frozen",
            "freezememory_status_ok_before_later_observation_implementation",
            "separate_human_review_required_before_later_observation_implementation",
        ):
            self.assertIn(expected, record.required_preconditions)

    def test_skeleton_slots_define_future_boundaries_without_live_execution(self):
        record = build_shadow_mode_observation_skeleton_design()
        slot_ids = self._slot_ids(record.future_skeleton_slots)
        guardrail_ids = self._slot_ids(record.required_future_guardrails)
        for expected in (
            "future_validated_input_reference",
            "future_contract_version_reference",
            "future_non_authoritative_observation_placeholder",
            "future_separate_human_review_marker",
        ):
            self.assertIn(expected, slot_ids)
        for expected in (
            "guardrail_router_authority_not_granted",
            "guardrail_prompt_loading_not_granted",
            "guardrail_project_mutation_not_granted",
            "guardrail_assistant_not_started",
        ):
            self.assertIn(expected, guardrail_ids)
        for slot in record.future_skeleton_slots + record.required_future_guardrails:
            self.assertNotEqual(slot.description.strip(), "")
            self.assertNotIn("approved", slot.allowed_status)
            self.assertNotIn("enabled", slot.allowed_status)

    def test_forbidden_behaviors_block_runtime_authority_and_side_effects(self):
        record = build_shadow_mode_observation_skeleton_design()
        for forbidden in (
            "callable_observation_entrypoint",
            "live_input_validation_execution",
            "validated_input_processing",
            "observation_generation",
            "route_comparison",
            "candidate_execution",
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
            "patch_execution",
            "runtime_router_import",
            "runtime_router_export",
            "provider_or_model_call",
            "embedding_or_vector_index",
            "network_call",
            "subprocess_call",
            "dynamic_import",
            "candidate_promotion",
            "shadow_mode_activation",
            "assistant_behavior",
        ):
            self.assertIn(forbidden, record.forbidden_skeleton_behaviors)

    def test_invariants_defer_observation_implementation_to_later_gate(self):
        record = build_shadow_mode_observation_skeleton_design()
        for invariant in (
            "m21_is_design_only",
            "m21_defines_future_skeleton_limits_only",
            "m21_has_no_callable_observation_entrypoint",
            "m21_does_not_accept_or_process_input",
            "m21_does_not_generate_observation_output",
            "m21_does_not_compare_routes_or_candidates",
            "m21_does_not_persist_or_mutate_project_state",
            "future_skeleton_must_use_m20_validated_caller_supplied_primitives_only",
            "future_skeleton_output_must_remain_in_memory_non_authoritative_evidence_only",
            "m22_gate_design_is_required_before_later_observation_implementation",
        ):
            self.assertIn(invariant, record.skeleton_invariants)

    def test_public_exports_do_not_add_observation_entry_points(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_observation_skeleton_design"])
        text = MODULE.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_LIVE_BEHAVIOR_DEFS:
            self.assertNotIn("def " + forbidden, text)

    def test_ast_rejects_forbidden_imports_and_calls(self):
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

    def test_builder_has_no_file_or_console_side_effects(self):
        before = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            record = build_shadow_mode_observation_skeleton_design()
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(record.observation_execution_status, "not_implemented")

    def test_notes_exist_and_keep_m21_design_only(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M21 is design-only.",
            "M21 defines the future non-runtime observation skeleton boundary",
            "It does not implement a callable observation",
            "M21 does not implement observation execution.",
            "The next allowed milestone is M22",
        )
        for snippet in required:
            self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
