import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_copilot_scope_charter_entry_gate_design import (
    AUTHORITY_STATEMENT,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    PilotCopilotScopeCharterEntryGateDesign,
    ScopeAssertionDesign,
    ScopeMilestoneDesign,
    ScopeRuleDesign,
    build_pilot_copilot_scope_charter_entry_gate_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_post_adviser_pilot_copilot_handoff_closure_design import (
    FEATURE_ID as M35_FEATURE_ID,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "pilot_copilot_scope_charter_entry_gate_design.py"
NOTES = TRANSITION / "pilot_copilot_scope_charter_entry_gate_notes.md"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_INIT = BOX / "__init__.py"
RUNTIME_CONTRACT = BOX / "contract.py"
RG_CANON = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md"

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
    "runtime_authority_granted_true",
    "human_review_mandatory_false",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "human_review_completed",
    "promotion_ready",
    "runtime_enabled",
) + tuple(['candidate_prompt_groups', 'simulated_required_prompt_groups'])


class PilotCopilotScopeCharterEntryGateDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_rg_pilot_000_canon_is_present_before_p0(self):
        self.assertTrue(RG_CANON.exists())
        text = RG_CANON.read_text(encoding="utf-8")
        self.assertIn("RG-PILOT-000", text)
        self.assertIn("P0 - Routing Signal Scorer v3 Pilot/Copilot Scope Charter and Entry Gate Design v1", text)
        self.assertIn("Pilot/Copilot P-series", text)

    def test_manifest_declares_p0_scope_charter_entry_gate(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "pilot_copilot_scope_charter_entry_gate_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest[f"{prefix}_status"],
            "immutable_design_only_pilot_copilot_scope_charter_entry_gate_no_activation_no_runtime_authority",
        )
        self.assertEqual(manifest[f"{prefix}_module"], str(MODULE.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_notes_doc"], str(NOTES.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        self.assertIs(manifest[f"{prefix}_requires_m35_handoff_closure"], True)
        self.assertIs(manifest[f"{prefix}_requires_rg_pilot_000_router_canon"], True)
        self.assertEqual(manifest[f"{prefix}_bridge_roadmap_done_count"], 18)
        self.assertEqual(manifest[f"{prefix}_bridge_roadmap_remaining_count"], 0)
        self.assertEqual(manifest[f"{prefix}_p_series_done_before_p0"], 0)
        self.assertEqual(manifest[f"{prefix}_p_series_remaining_before_p0"], 13)
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

    def test_p0_returns_static_immutable_design_record(self):
        first = build_pilot_copilot_scope_charter_entry_gate_design()
        second = build_pilot_copilot_scope_charter_entry_gate_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertIsInstance(first, PilotCopilotScopeCharterEntryGateDesign)
        with self.assertRaises(FrozenInstanceError):
            first.milestone = "changed"
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "P0")
        self.assertEqual(first.title, "Routing Signal Scorer v3 Pilot/Copilot Scope Charter and Entry Gate Design v1")
        self.assertEqual(first.authority_statement, AUTHORITY_STATEMENT)
        self.assertEqual(first.design_status, "design_only")
        self.assertEqual(first.adviser_phase, "closed_through_m16")
        self.assertEqual(first.bridge_phase, "closed_through_m35_18_done_0_to_go")
        self.assertEqual(first.auxiliar_assistant_phase, "design_complete_not_activated")
        self.assertEqual(first.pilot_phase, "scope_charter_only")
        self.assertEqual(first.copilot_phase, "not_started")
        self.assertIs(first.shadow_mode_active, False)
        self.assertIs(first.pilot_active, False)
        self.assertIs(first.copilot_active, False)
        self.assertIs(first.runtime_authority_granted, False)
        self.assertIs(first.prompt_loading_authority_granted, False)
        self.assertIs(first.persistence_authority_granted, False)
        self.assertEqual(first.candidate_promotion_status, "blocked")
        self.assertIs(first.implementation_blocked_by_default, True)
        self.assertIs(first.pilot_outputs_ephemeral, True)
        self.assertIs(first.pilot_opt_in_per_invocation, True)
        self.assertIs(first.pilot_training_data_use_allowed, False)
        self.assertIs(first.pilot_batch_mode_allowed, False)
        self.assertEqual(first.critical_boundary_error_budget, "zero")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_current_state_and_lifecycle_are_design_only(self):
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        assertion_ids = {item.assertion_id for item in design.current_state_assertions}
        self.assertEqual(
            assertion_ids,
            {
                "adviser_phase_closed",
                "bridge_closed_through_m35",
                "rg_pilot_000_frozen",
                "pilot_not_started",
                "copilot_not_started",
            },
        )
        for item in design.current_state_assertions:
            self.assertIsInstance(item, ScopeAssertionDesign)
            self.assertIn("must_not", item.prohibited_interpretation)
        lifecycle_ids = {item.rule_id for item in design.lifecycle_status}
        self.assertEqual(
            lifecycle_ids,
            {
                "govern_allowed",
                "map_allowed",
                "measure_design_only",
                "manage_gate_decisions_only",
                "deploy_forbidden",
                "operate_forbidden",
            },
        )
        for rule in design.lifecycle_status:
            self.assertIsInstance(rule, ScopeRuleDesign)
            self.assertIn("must_not", rule.blocked_interpretation)

    def test_preconditions_and_evidence_ladder_enforce_ordering(self):
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        self.assertIn("m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen", design.required_preconditions)
        self.assertIn("rg_pilot_000_pilot_copilot_phase0_router_canon_frozen", design.required_preconditions)
        self.assertIn("freeze_memory_status_ok_after_rg_pilot_000", design.required_preconditions)
        self.assertIn("p3_divergence_taxonomy_frozen_before_any_projection_implementation", design.evidence_ladder)
        self.assertIn("p6_implementation_gate_frozen_before_callable_projection", design.evidence_ladder)
        self.assertIn("p8_reproduction_comparison_passes_critical_cases_before_readiness_gate", design.evidence_ladder)

    def test_ladder_has_thirteen_steps_and_no_runtime_shadow_target(self):
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        self.assertEqual(len(design.revised_p_series_ladder), 13)
        ids = tuple(item.milestone_id for item in design.revised_p_series_ladder)
        self.assertEqual(ids, tuple(f"P{i}" for i in range(13)))
        for item in design.revised_p_series_ladder:
            self.assertIsInstance(item, ScopeMilestoneDesign)
            joined = " ".join((item.title, item.safety_pattern, item.milestone_status, item.forbidden_interpretation)).lower()
            self.assertNotIn("limited shadow runtime", joined)
            self.assertNotIn("runtime shadow", joined)
        p3 = design.revised_p_series_ladder[3]
        p6 = design.revised_p_series_ladder[6]
        p8 = design.revised_p_series_ladder[8]
        self.assertIn("Taxonomy", p3.title)
        self.assertIn("Implementation Gate", p6.title)
        self.assertIn("Reproduction", p8.title)

    def test_forbidden_operations_include_audit_assimilations(self):
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        for item in (
            "live_pilot_behavior",
            "live_copilot_behavior",
            "limited_shadow_runtime",
            "projection_implementation",
            "route_comparison_execution",
            "prompt_loading",
            "runtime_authority",
            "persistence",
            "human_decision_recording",
            "gold_mutation",
            "registry_mutation",
            "training_data_use",
            "batch_mode",
            "candidate_promotion",
        ):
            self.assertIn(item, design.forbidden_operations)
        self.assertIn("human_overtrust_of_polished_projection_text", design.surrounding_process_risks)
        self.assertIn("input_attempts_to_request_training_data_use", design.red_team_seed_cases)
        self.assertIn("input_attempts_to_request_batch_mode", design.red_team_seed_cases)

    def test_authority_statement_is_exact_and_non_authorizing(self):
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        self.assertEqual(design.authority_statement, AUTHORITY_STATEMENT)
        for expected in (
            "does not start Pilot",
            "does not start Copilot",
            "does not route",
            "does not load prompts",
            "does not persist output",
            "does not mutate gold or registry data",
            "does not promote candidates",
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
            design = build_pilot_copilot_scope_charter_entry_gate_design()
        after = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if "__pycache__" not in p.parts}
        self.assertIsInstance(design, PilotCopilotScopeCharterEntryGateDesign)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(before, after)

    def test_runtime_contract_and_init_remain_unmodified_by_p0_exports(self):
        contract_text = RUNTIME_CONTRACT.read_text(encoding="utf-8")
        init_text = RUNTIME_INIT.read_text(encoding="utf-8")
        for forbidden in (
            "pilot_copilot_scope_charter_entry_gate_design",
            "build_pilot_copilot_scope_charter_entry_gate_design",
            "adviser_offline",
            "run_pilot",
            "activate_pilot",
            "run_copilot",
            "activate_copilot",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_m35_remains_closed_and_p0_does_not_reopen_bridge(self):
        self.assertEqual(M35_FEATURE_ID, "routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design_v1")
        design = build_pilot_copilot_scope_charter_entry_gate_design()
        self.assertEqual(design.bridge_phase, "closed_through_m35_18_done_0_to_go")
        self.assertEqual(design.pilot_phase, "scope_charter_only")
        self.assertEqual(design.copilot_phase, "not_started")


if __name__ == "__main__":
    unittest.main()
