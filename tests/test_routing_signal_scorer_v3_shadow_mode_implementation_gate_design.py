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
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_implementation_gate_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_implementation_gate_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_io_contract_design import (
    build_shadow_mode_io_contract_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_observation_skeleton_design import (
    build_shadow_mode_observation_skeleton_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_implementation_gate_design.py"
NOTES = TRANSITION / "shadow_mode_implementation_gate_notes.md"
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
    "run_shadow_mode_implementation_gate",
    "evaluate_shadow_mode_implementation_gate",
    "evaluate_implementation_readiness",
    "confirm_implementation_scope",
    "start_m23",
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


class ShadowModeImplementationGateDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _criterion_ids(self, criteria):
        return {criterion.criterion_id for criterion in criteria}

    def _outcome_ids(self, outcomes):
        return {outcome.outcome_id for outcome in outcomes}

    def test_manifest_declares_m22_implementation_gate_design_without_live_behavior(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_implementation_gate_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_implementation_gate_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_implementation_gate_design_status"],
            "immutable_design_only_implementation_gate_no_live_gate_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_implementation_gate_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        for key in (
            "shadow_mode_implementation_gate_design_contains_callable_gate_entrypoint",
            "shadow_mode_implementation_gate_design_contains_live_gate_execution",
            "shadow_mode_implementation_gate_design_contains_observation_implementation",
            "shadow_mode_implementation_gate_design_contains_observation_execution",
            "shadow_mode_implementation_gate_design_contains_live_validation_execution",
            "shadow_mode_implementation_gate_design_contains_input_processing",
            "shadow_mode_implementation_gate_design_contains_output_generation",
            "shadow_mode_implementation_gate_design_contains_route_comparison",
            "shadow_mode_implementation_gate_design_contains_shadow_activation",
            "shadow_mode_implementation_gate_design_contains_assistant_behavior",
            "shadow_mode_implementation_gate_design_contains_runtime_integration",
            "shadow_mode_implementation_gate_design_contains_router_authority",
            "shadow_mode_implementation_gate_design_contains_prompt_loading",
            "shadow_mode_implementation_gate_design_contains_file_io",
            "shadow_mode_implementation_gate_design_contains_persistence",
            "shadow_mode_implementation_gate_design_contains_report_writer",
            "shadow_mode_implementation_gate_design_contains_gold_or_registry_mutation",
            "shadow_mode_implementation_gate_design_contains_candidate_promotion",
            "shadow_mode_implementation_gate_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_implementation_gate_record_is_immutable_static_and_design_only(self):
        m18 = build_shadow_mode_boundary_design()
        m19 = build_shadow_mode_io_contract_design()
        m20 = build_shadow_mode_contract_validator_design()
        m21 = build_shadow_mode_observation_skeleton_design()
        self.assertEqual(m18.next_allowed_milestone, "M19 - Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1")
        self.assertEqual(m19.next_allowed_milestone, "M20 - Routing Signal Scorer v3 Shadow Mode Contract Validator Design v1")
        self.assertEqual(m20.next_allowed_milestone, "M21 - Routing Signal Scorer v3 Shadow Mode Observation Skeleton Design v1")
        self.assertEqual(m21.next_allowed_milestone, "M22 - Routing Signal Scorer v3 Shadow Mode Implementation Gate Design v1")
        first = build_shadow_mode_implementation_gate_design()
        second = build_shadow_mode_implementation_gate_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M22")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "design_only_no_live_gate_execution")
        self.assertEqual(first.gate_design_status, "static_gate_design_only_no_gate_function")
        self.assertEqual(first.live_gate_execution_status, "not_implemented")
        self.assertEqual(first.observation_implementation_status, "not_implemented")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        with self.assertRaises(FrozenInstanceError):
            first.feature_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.required_frozen_milestone_criteria[0].criterion_id = "changed"

    def test_preconditions_require_m18_m19_m20_m21_and_human_confirmation(self):
        record = build_shadow_mode_implementation_gate_design()
        for expected in (
            "m18_shadow_mode_boundary_design_frozen",
            "m19_shadow_mode_input_output_contract_design_frozen",
            "m20_shadow_mode_contract_validator_design_frozen",
            "m21_shadow_mode_observation_skeleton_design_frozen",
            "freezememory_status_ok_before_later_m23_implementation",
            "explicit_human_confirmation_required_before_m23_implementation",
        ):
            self.assertIn(expected, record.required_preconditions)

    def test_allowed_outcomes_do_not_grant_authority_or_automatic_implementation(self):
        record = build_shadow_mode_implementation_gate_design()
        self.assertEqual(
            self._outcome_ids(record.allowed_gate_outcomes),
            {"blocked", "not_blocked_for_separate_human_review"},
        )
        for outcome in record.allowed_gate_outcomes:
            self.assertNotIn("approved", outcome.outcome_id)
            self.assertNotIn("ready", outcome.outcome_id)
            self.assertNotIn("enabled", outcome.outcome_id)
            self.assertIn("Must not", outcome.blocked_interpretation)

    def test_gate_criteria_require_frozen_chain_and_block_critical_boundary_failures(self):
        record = build_shadow_mode_implementation_gate_design()
        frozen_ids = self._criterion_ids(record.required_frozen_milestone_criteria)
        critical_ids = self._criterion_ids(record.critical_boundary_failure_criteria)
        human_ids = self._criterion_ids(record.human_review_criteria)
        later_ids = self._criterion_ids(record.later_m23_constraints)
        for expected in (
            "m18_boundary_freeze_confirmed",
            "m19_io_contract_freeze_confirmed",
            "m20_validator_design_freeze_confirmed",
            "m21_observation_skeleton_freeze_confirmed",
        ):
            self.assertIn(expected, frozen_ids)
        for expected in (
            "runtime_import_boundary_clean",
            "side_effect_boundary_clean",
            "authority_boundary_clean",
            "assistant_boundary_clean",
            "schema_fail_closed_boundary_clean",
        ):
            self.assertIn(expected, critical_ids)
        for expected in (
            "human_confirms_m23_scope_separately",
            "validation_evidence_reviewed",
            "freeze_context_reviewed",
        ):
            self.assertIn(expected, human_ids)
        for expected in (
            "m23_may_be_non_runtime_only",
            "m23_may_use_validated_primitives_only",
            "m23_may_return_one_non_authoritative_observation",
        ):
            self.assertIn(expected, later_ids)

    def test_forbidden_behaviors_block_runtime_authority_and_side_effects(self):
        record = build_shadow_mode_implementation_gate_design()
        for forbidden in (
            "live_gate_evaluation_execution",
            "callable_gate_entrypoint",
            "automatic_scope_confirmation",
            "implementation_permission_grant",
            "runtime_state_inspection",
            "freeze_memory_reading",
            "source_scanning",
            "case_discovery",
            "file_io",
            "console_io",
            "logging",
            "persistence",
            "observation_implementation",
            "observation_execution",
            "live_input_validation_execution",
            "input_processing",
            "output_generation",
            "route_comparison",
            "candidate_execution",
            "prompt_selection",
            "prompt_loading",
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
            self.assertIn(forbidden, record.forbidden_gate_behaviors)

    def test_invariants_defer_m23_to_separate_governed_patch(self):
        record = build_shadow_mode_implementation_gate_design()
        for invariant in (
            "m22_is_design_only",
            "m22_defines_future_implementation_gate_limits_only",
            "m22_has_no_callable_gate_entrypoint",
            "m22_does_not_evaluate_live_project_state",
            "m22_does_not_read_freeze_memory_or_source_files",
            "m22_does_not_authorize_m23_by_itself",
            "m22_does_not_implement_observation_logic",
            "m22_keeps_shadow_mode_inactive",
            "m22_keeps_auxiliar_assistant_not_started",
            "future_m23_requires_separate_human_confirmation_after_m22_freeze",
        ):
            self.assertIn(invariant, record.gate_invariants)

    def test_public_exports_do_not_add_gate_or_observation_entry_points(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_implementation_gate_design"])
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
            record = build_shadow_mode_implementation_gate_design()
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(record.live_gate_execution_status, "not_implemented")
        self.assertEqual(record.observation_implementation_status, "not_implemented")

    def test_notes_exist_and_keep_m22_design_only(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M22 is design-only.",
            "M22 defines the future implementation gate boundary",
            "It does not implement a live gate",
            "M22 does not implement observation logic.",
            "The next allowed milestone is M23",
        )
        for snippet in required:
            self.assertIn(snippet, text)


if __name__ == "__main__":
    unittest.main()
