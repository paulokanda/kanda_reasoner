import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_boundary_design import (
    AUTHORITY_STATEMENT,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    PilotBoundaryDesign,
    PilotBoundaryEvidenceRuleDesign,
    PilotBoundaryRoleDesign,
    PilotBoundaryRuleDesign,
    build_pilot_boundary_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_copilot_scope_charter_entry_gate_design import (
    FEATURE_ID as P0_FEATURE_ID,
    NEXT_ALLOWED_MILESTONE as P0_NEXT_ALLOWED_MILESTONE,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "pilot_boundary_design.py"
NOTES = TRANSITION / "pilot_boundary_notes.md"
P0_MODULE = TRANSITION / "pilot_copilot_scope_charter_entry_gate_design.py"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_INIT = BOX / "__init__.py"
RUNTIME_CONTRACT = BOX / "contract.py"

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
    "logging",
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
    "run_pilot",
    "start_pilot",
    "activate_pilot",
    "run_copilot",
    "start_copilot",
    "activate_copilot",
    "execute_route",
    "compare_routes",
    "select_route",
    "override_route",
    "select_prompt",
    "load_prompt",
    "integrate_runtime_router",
    "persist_evidence",
    "write_report",
    "write_review_queue",
    "record_human_decision",
    "run_shadow_mode",
    "activate_shadow_mode",
    "write_gold",
    "write_registry",
    "promote_candidate",
    "run_batch",
    "train_on_pilot_output",
)

FORBIDDEN_FIELD_TEXT = (
    "candidate_prompt_groups",
    "simulated_required_prompt_groups",
    "approved_route",
    "final_route",
    "execute_route",
    "load_prompt",
    "activate_pilot",
    "activate_copilot",
    "promote_candidate",
    "write_gold",
    "write_registry",
    "record_human_decision",
    "persist_report",
    "human_review_mandatory_false",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "human_review_completed",
    "promotion_ready",
    "runtime_enabled",
)


class PilotBoundaryDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_p0_is_present_and_points_to_p1_before_p1(self):
        self.assertTrue(P0_MODULE.exists())
        self.assertEqual(P0_FEATURE_ID, "routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design_v1")
        self.assertIn("P1 - Routing Signal Scorer v3 Pilot Boundary Design v1", P0_NEXT_ALLOWED_MILESTONE)

    def test_manifest_declares_p1_pilot_boundary_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "pilot_boundary_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest[f"{prefix}_status"], "immutable_design_only_pilot_boundary_no_activation_no_runtime_authority")
        self.assertEqual(manifest[f"{prefix}_module"], str(MODULE.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_notes_doc"], str(NOTES.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        self.assertIs(manifest[f"{prefix}_requires_p0_scope_charter_entry_gate_design"], True)
        self.assertIs(manifest[f"{prefix}_requires_rg_pilot_000_router_canon"], True)
        for key in (
            f"{prefix}_contains_live_pilot_behavior",
            f"{prefix}_contains_live_copilot_behavior",
            f"{prefix}_contains_callable_pilot_runner",
            f"{prefix}_contains_callable_copilot_runner",
            f"{prefix}_contains_projection_implementation",
            f"{prefix}_contains_route_comparison_execution",
            f"{prefix}_contains_route_selection",
            f"{prefix}_contains_route_execution",
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
            f"{prefix}_contains_training_data_use",
            f"{prefix}_contains_batch_mode",
            f"{prefix}_contains_limited_shadow_runtime",
            f"{prefix}_contains_candidate_promotion",
            f"{prefix}_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_p1_returns_static_immutable_design_record(self):
        first = build_pilot_boundary_design()
        second = build_pilot_boundary_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertIsInstance(first, PilotBoundaryDesign)
        with self.assertRaises(FrozenInstanceError):
            first.milestone = "changed"
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "P1")
        self.assertEqual(first.title, "Routing Signal Scorer v3 Pilot Boundary Design v1")
        self.assertEqual(first.authority_statement, AUTHORITY_STATEMENT)
        self.assertEqual(first.design_status, "design_only")
        self.assertEqual(first.pilot_status, "boundary_design_only_not_started")
        self.assertEqual(first.copilot_status, "not_started_deferred_to_p11_boundary_charter")
        self.assertEqual(first.projection_status, "not_implemented_blocked_until_p7_after_p6_gate")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.prompt_loading_authority_status, "not_granted")
        self.assertEqual(first.persistence_authority_status, "not_granted")
        self.assertEqual(first.training_data_use_status, "forbidden")
        self.assertEqual(first.batch_mode_status, "forbidden")
        self.assertEqual(first.limited_shadow_runtime_status, "out_of_scope_separate_future_governed_scope_required")
        self.assertEqual(first.human_review_status, "mandatory_not_approval_not_decision_recording")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_preconditions_require_p0_and_freeze_status_before_p1(self):
        design = build_pilot_boundary_design()
        for item in (
            "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
            "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
            "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
            "startup_freeze_context_refreshed_after_p0",
            "freeze_memory_status_ok_after_p0",
        ):
            self.assertIn(item, design.required_preconditions)

    def test_allowed_future_roles_are_non_authoritative_and_gated(self):
        design = build_pilot_boundary_design()
        role_ids = {role.role_id for role in design.allowed_future_pilot_roles}
        self.assertEqual(
            role_ids,
            {
                "future_descriptive_projection_analyst",
                "future_frozen_router_reproduction_candidate",
                "future_boundary_flag_explainer",
                "future_in_memory_review_note_preparer",
            },
        )
        for role in design.allowed_future_pilot_roles:
            self.assertIsInstance(role, PilotBoundaryRoleDesign)
            self.assertIn("p", role.required_prior_gate)
            self.assertIn("must_not", role.prohibited_interpretation)
        by_id = {role.role_id: role for role in design.allowed_future_pilot_roles}
        self.assertIn("p6_implementation_gate", by_id["future_descriptive_projection_analyst"].required_prior_gate)
        self.assertIn("must_not_trust_divergence_before_reproduction_success", by_id["future_frozen_router_reproduction_candidate"].prohibited_interpretation)

    def test_hard_rules_block_authority_creep(self):
        design = build_pilot_boundary_design()
        rule_ids = {rule.rule_id for rule in design.hard_blocked_authority_rules}
        self.assertEqual(
            rule_ids,
            {
                "pilot_is_not_active",
                "pilot_is_not_copilot",
                "pilot_is_not_router_authority",
                "pilot_is_not_prompt_loader",
                "pilot_is_not_state_writer",
                "pilot_is_not_training_data_source",
                "pilot_is_not_batch_engine",
                "human_review_is_mandatory_not_approval",
            },
        )
        for rule in design.hard_blocked_authority_rules:
            self.assertIsInstance(rule, PilotBoundaryRuleDesign)
            self.assertIn("must_not", rule.blocked_interpretation)
        required_states = {rule.required_state for rule in design.hard_blocked_authority_rules}
        self.assertIn("router_authority_not_granted", required_states)
        self.assertIn("prompt_loading_authority_not_granted", required_states)
        self.assertIn("training_data_use_forbidden", required_states)
        self.assertIn("batch_mode_forbidden", required_states)

    def test_evidence_constraints_preserve_safe_order(self):
        design = build_pilot_boundary_design()
        ids = {rule.evidence_rule_id for rule in design.evidence_constraints}
        self.assertEqual(
            ids,
            {
                "contracts_before_fields",
                "taxonomy_before_projection",
                "implementation_gate_before_callable_projection",
                "reproduction_before_divergence_trust",
            },
        )
        for rule in design.evidence_constraints:
            self.assertIsInstance(rule, PilotBoundaryEvidenceRuleDesign)
        by_id = {rule.evidence_rule_id: rule for rule in design.evidence_constraints}
        self.assertIn("p3_divergence_taxonomy_design_frozen", by_id["taxonomy_before_projection"].required_evidence)
        self.assertIn("p6_implementation_gate_design_frozen", by_id["implementation_gate_before_callable_projection"].required_evidence)
        self.assertIn("zero_critical_deviations", by_id["reproduction_before_divergence_trust"].required_evidence)

    def test_boundary_invariants_and_forbidden_operations_are_complete(self):
        design = build_pilot_boundary_design()
        for item in (
            "p1_is_design_only",
            "p1_does_not_start_or_enable_pilot",
            "p1_does_not_define_copilot_behavior",
            "p1_does_not_implement_projection_or_comparison",
            "p1_does_not_select_load_or_scan_prompts",
            "p1_does_not_cache_log_serialize_persist_or_write_outputs",
            "p1_does_not_use_outputs_for_training_or_gold_expansion",
            "p1_does_not_run_batch_mode",
        ):
            self.assertIn(item, design.pilot_boundary_invariants)
        for item in (
            "live_pilot_behavior",
            "projection_implementation",
            "route_comparison_execution",
            "prompt_loading",
            "runtime_authority",
            "persistence",
            "training_data_use",
            "batch_mode",
            "limited_shadow_runtime",
            "candidate_promotion",
        ):
            self.assertIn(item, design.forbidden_operations)

    def test_safe_language_policy_avoids_prompt_and_route_leakage(self):
        design = build_pilot_boundary_design()
        for safe in (
            "routing_context_public_summary",
            "task_classification_hints_summary",
            "projection_analysis_summary",
            "boundary_flags_for_human_review",
            "human_review_mandatory",
            "storage_status_in_memory_only_constant",
        ):
            self.assertIn(safe, design.safe_future_contract_language)
        for policy in (
            "route_like_output_names_remain_forbidden",
            "prompt_group_field_names_remain_forbidden",
            "approval_or_completion_state_names_remain_forbidden",
            "activation_enablement_promotion_names_remain_forbidden",
        ):
            self.assertIn(policy, design.unsafe_contract_language_policy)

    def test_authority_statement_is_exact_and_non_authorizing(self):
        design = build_pilot_boundary_design()
        self.assertEqual(design.authority_statement, AUTHORITY_STATEMENT)
        for expected in (
            "does not start Pilot",
            "does not implement projection",
            "does not compare routes",
            "does not load prompts",
            "does not persist output",
            "does not use output as training data",
            "does not run batch mode",
            "does not activate Copilot or limited shadow runtime",
            "does not grant runtime authority",
            "Human governance and the real router remain authoritative",
        ):
            self.assertIn(expected, design.authority_statement)

    def test_module_uses_only_safe_static_imports(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertFalse(alias.name.startswith(FORBIDDEN_IMPORT_PREFIXES), alias.name)
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                self.assertFalse(mod.startswith(FORBIDDEN_IMPORT_PREFIXES), mod)
        imports = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        self.assertEqual(imports, {"__future__", "dataclasses", "typing"})

    def test_module_contains_no_runtime_calls_or_functions(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.assertNotIn(node.name, FORBIDDEN_RUNTIME_BEHAVIOR_DEFS)
            if isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                self.assertNotIn(name, FORBIDDEN_CALLS)
            if isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, FORBIDDEN_CALLS)

    def test_module_and_notes_avoid_unsafe_field_names(self):
        source = MODULE.read_text(encoding="utf-8")
        notes = NOTES.read_text(encoding="utf-8")
        combined = source + "\n" + notes
        for token in FORBIDDEN_FIELD_TEXT:
            self.assertNotIn(token, combined)

    def test_builder_has_no_stdout_stderr_and_no_file_side_effects(self):
        before = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if "__pycache__" not in p.parts}
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            design = build_pilot_boundary_design()
        after = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if "__pycache__" not in p.parts}
        self.assertIsInstance(design, PilotBoundaryDesign)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(before, after)

    def test_runtime_contract_and_init_remain_unmodified_by_p1_exports(self):
        contract_text = RUNTIME_CONTRACT.read_text(encoding="utf-8")
        init_text = RUNTIME_INIT.read_text(encoding="utf-8")
        for forbidden in (
            "pilot_boundary_design",
            "build_pilot_boundary_design",
            "PilotBoundaryDesign",
            "pilot_projection",
            "pilot_runner",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
