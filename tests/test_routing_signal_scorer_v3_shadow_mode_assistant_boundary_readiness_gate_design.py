import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_observation_review_evidence_design import (
    NEXT_ALLOWED_MILESTONE as M24_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_assistant_boundary_readiness_gate_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_assistant_boundary_readiness_gate_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_assistant_boundary_readiness_gate_design.py"
NOTES = TRANSITION / "shadow_mode_assistant_boundary_readiness_gate_notes.md"
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
    "run_readiness_gate",
    "execute_readiness_gate",
    "calculate_readiness",
    "evaluate_readiness",
    "build_review_evidence",
    "transform_observation",
    "validate_live_observation",
    "compare_routes",
    "persist_evidence",
    "write_report",
    "write_review_queue",
    "record_human_decision",
    "approve_observation",
    "reject_observation",
    "override_route",
    "run_shadow_mode",
    "activate_shadow_mode",
    "start_assistant",
    "start_auxiliar",
    "start_copilot",
    "integrate_runtime_router",
    "load_prompt",
    "write_gold",
    "write_registry",
    "promote_candidate",
)

FORBIDDEN_AUTHORITY_TERMS = (
    "final_route",
    "route_override",
    "selected_route",
    "selected_prompt",
    "prompt_to_load",
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


class ShadowModeAssistantBoundaryReadinessGateDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m25_readiness_gate_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_assistant_boundary_readiness_gate_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_assistant_boundary_readiness_gate_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_assistant_boundary_readiness_gate_design_status"],
            "immutable_design_only_readiness_gate_prerequisite_design_no_live_gate_no_assistant_behavior_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_assistant_boundary_readiness_gate_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m18_boundary"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m19_io_contract"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m20_contract_validator_design"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m21_observation_skeleton_design"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m22_implementation_gate_design"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m23_non_runtime_observation"])
        self.assertTrue(manifest["shadow_mode_assistant_boundary_readiness_gate_design_requires_m24_review_evidence_design"])
        for key in (
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_live_readiness_gate",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_readiness_evaluation_execution",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_review_evidence_builder",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_observation_transformation_execution",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_route_comparison",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_runtime_integration",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_router_authority",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_prompt_loading",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_file_io",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_persistence",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_report_writer",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_review_queue_writer",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_human_decision_recording",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_gold_or_registry_mutation",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_candidate_promotion",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_shadow_activation",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_assistant_behavior",
            "shadow_mode_assistant_boundary_readiness_gate_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m24_points_to_m25_and_m25_points_to_m26(self):
        self.assertEqual(
            M24_NEXT_ALLOWED_MILESTONE,
            "M25 - Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M26 - Routing Signal Scorer v3 Auxiliar/Assistant Boundary Design v1",
        )

    def test_design_record_is_immutable_static_and_design_only(self):
        design = build_shadow_mode_assistant_boundary_readiness_gate_design()
        second = build_shadow_mode_assistant_boundary_readiness_gate_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M25")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_live_readiness_gate")
        self.assertEqual(design.readiness_gate_design_status, "static_prerequisite_design_only")
        self.assertEqual(design.live_gate_execution_status, "not_implemented")
        self.assertEqual(
            design.assistant_boundary_status,
            "not_started_design_review_only_after_m25_freeze_and_confirmation",
        )
        self.assertEqual(design.runtime_authority_status, "not_granted")
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_prerequisites_are_blocking_and_do_not_grant_authority(self):
        design = build_shadow_mode_assistant_boundary_readiness_gate_design()
        self.assertIn("m24_shadow_observation_review_evidence_design_frozen", design.required_prior_milestones)
        criterion_ids = {item.criterion_id for item in design.future_boundary_review_prerequisites}
        self.assertEqual(
            criterion_ids,
            {
                "m24_review_evidence_design_frozen",
                "shadow_mode_remains_inactive",
                "auxiliar_assistant_remains_not_started",
                "runtime_authority_remains_not_granted",
                "m26_scope_requires_explicit_human_confirmation",
                "no_persistence_or_review_decision_bridge",
            },
        )
        for item in design.future_boundary_review_prerequisites:
            self.assertTrue(item.blocked_status.startswith("blocked_if"), item)
            text = " ".join((item.criterion_id, item.evidence_source, item.required_status, item.blocked_status))
            for forbidden in FORBIDDEN_AUTHORITY_TERMS:
                self.assertNotIn(forbidden, text)

    def test_boundary_rules_preserve_assistant_and_runtime_separation(self):
        design = build_shadow_mode_assistant_boundary_readiness_gate_design()
        boundary_ids = {rule.boundary_id for rule in design.boundary_review_safety_rules}
        self.assertEqual(
            boundary_ids,
            {
                "readiness_gate_is_not_live_gate",
                "assistant_boundary_review_is_not_assistant_behavior",
                "readiness_gate_is_not_promotion",
                "readiness_gate_is_not_router_integration",
            },
        )
        by_id = {rule.boundary_id: rule for rule in design.boundary_review_safety_rules}
        self.assertEqual(by_id["readiness_gate_is_not_live_gate"].required_state, "static_design_record_only")
        self.assertEqual(by_id["readiness_gate_is_not_promotion"].required_state, "candidate_promotion_blocked")
        self.assertEqual(by_id["readiness_gate_is_not_router_integration"].required_state, "runtime_router_authority_not_granted")

    def test_forbidden_behaviors_and_invariants_preserve_boundaries(self):
        design = build_shadow_mode_assistant_boundary_readiness_gate_design()
        for forbidden in (
            "live_readiness_gate",
            "readiness_evaluation_execution",
            "review_evidence_building",
            "observation_transformation_execution",
            "route_comparison",
            "persistence",
            "report_writing",
            "review_queue_writing",
            "human_decision_recording",
            "runtime_router_import",
            "prompt_loading",
            "candidate_promotion",
            "shadow_mode_activation",
            "assistant_behavior",
            "auxiliar_behavior",
            "copilot_behavior",
        ):
            self.assertIn(forbidden, design.forbidden_readiness_gate_behaviors)
        for invariant in (
            "m25_is_design_only",
            "m25_has_no_live_readiness_gate",
            "m25_does_not_evaluate_live_observations_or_review_evidence",
            "m25_does_not_start_auxiliar_assistant_or_copilot_behavior",
            "m25_does_not_grant_runtime_router_or_prompt_loader_authority",
            "m26_requires_separate_human_scope_confirmation",
        ):
            self.assertIn(invariant, design.readiness_gate_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_assistant_boundary_readiness_gate_design"])
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
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    self.assertFalse(module == prefix or module.startswith(prefix + "."), module)
            elif isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                self.assertNotIn(name, FORBIDDEN_CALLS)

    def test_design_builder_has_no_console_or_filesystem_side_effects(self):
        before = sorted(path.name for path in ROOT.iterdir())
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            design = build_shadow_mode_assistant_boundary_readiness_gate_design()
        after = sorted(path.name for path in ROOT.iterdir())
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(design.live_gate_execution_status, "not_implemented")

    def test_notes_and_runtime_exports_preserve_non_runtime_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        for expected in (
            "M25 is a design-only post-Adviser milestone",
            "does not execute a live readiness gate",
            "Shadow mode is not active",
            "Auxiliar/Assistant has not started",
            "Runtime router authority is not granted",
            "M26 - Routing Signal Scorer v3 Auxiliar/Assistant Boundary Design v1",
        ):
            self.assertIn(expected, notes)
        runtime_init = RUNTIME_INIT.read_text(encoding="utf-8")
        runtime_contract = RUNTIME_CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn("shadow_mode_assistant_boundary_readiness_gate", runtime_init)
        self.assertNotIn("shadow_mode_assistant_boundary_readiness_gate", runtime_contract)


if __name__ == "__main__":
    unittest.main()
