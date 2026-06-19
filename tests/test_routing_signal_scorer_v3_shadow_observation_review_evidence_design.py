import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_non_runtime_observation import (
    NEXT_ALLOWED_MILESTONE as M23_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_observation_review_evidence_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_observation_review_evidence_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_observation_review_evidence_design.py"
NOTES = TRANSITION / "shadow_observation_review_evidence_notes.md"
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
    "build_review_evidence",
    "build_live_review_evidence",
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
    "integrate_runtime_router",
    "load_prompt",
    "write_gold",
    "write_registry",
    "promote_candidate",
)

FORBIDDEN_AUTHORITY_FIELDS = (
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


class ShadowObservationReviewEvidenceDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_manifest_declares_m24_review_evidence_design_only(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_observation_review_evidence_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_observation_review_evidence_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_observation_review_evidence_design_status"],
            "immutable_design_only_review_evidence_field_design_no_live_builder_no_persistence_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_observation_review_evidence_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m18_boundary"])
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m19_io_contract"])
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m20_contract_validator_design"])
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m21_observation_skeleton_design"])
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m22_implementation_gate_design"])
        self.assertTrue(manifest["shadow_observation_review_evidence_design_requires_m23_non_runtime_observation"])
        for key in (
            "shadow_observation_review_evidence_design_contains_callable_review_evidence_builder",
            "shadow_observation_review_evidence_design_contains_live_input_validation_execution",
            "shadow_observation_review_evidence_design_contains_observation_transformation_execution",
            "shadow_observation_review_evidence_design_contains_route_comparison",
            "shadow_observation_review_evidence_design_contains_runtime_observation_execution",
            "shadow_observation_review_evidence_design_contains_runtime_integration",
            "shadow_observation_review_evidence_design_contains_router_authority",
            "shadow_observation_review_evidence_design_contains_prompt_loading",
            "shadow_observation_review_evidence_design_contains_file_io",
            "shadow_observation_review_evidence_design_contains_persistence",
            "shadow_observation_review_evidence_design_contains_report_writer",
            "shadow_observation_review_evidence_design_contains_review_queue_writer",
            "shadow_observation_review_evidence_design_contains_human_decision_recording",
            "shadow_observation_review_evidence_design_contains_gold_or_registry_mutation",
            "shadow_observation_review_evidence_design_contains_candidate_promotion",
            "shadow_observation_review_evidence_design_contains_shadow_activation",
            "shadow_observation_review_evidence_design_contains_assistant_behavior",
            "shadow_observation_review_evidence_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_m23_points_to_m24_and_m24_points_to_m25(self):
        self.assertEqual(
            M23_NEXT_ALLOWED_MILESTONE,
            "M24 - Routing Signal Scorer v3 Shadow Observation Review Evidence Design v1",
        )
        self.assertEqual(
            NEXT_ALLOWED_MILESTONE,
            "M25 - Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1",
        )

    def test_design_record_is_immutable_static_and_design_only(self):
        design = build_shadow_observation_review_evidence_design()
        second = build_shadow_observation_review_evidence_design()
        self.assertIs(design, second)
        self.assertTrue(is_dataclass(design))
        with self.assertRaises(FrozenInstanceError):
            design.milestone = "changed"
        self.assertEqual(design.feature_id, FEATURE_ID)
        self.assertEqual(design.schema_version, SCHEMA_VERSION)
        self.assertEqual(design.design_kind, DESIGN_KIND)
        self.assertEqual(design.milestone, "M24")
        self.assertEqual(design.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(design.lifecycle_status, "design_only_no_live_review_evidence_builder")
        self.assertEqual(design.evidence_design_status, "static_review_evidence_field_design_only")
        self.assertEqual(design.live_evidence_builder_status, "not_implemented")
        self.assertEqual(design.persistence_status, "not_implemented")
        self.assertEqual(design.runtime_authority_status, "not_granted")
        self.assertEqual(design.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_review_evidence_fields_are_non_authoritative_and_human_review_focused(self):
        design = build_shadow_observation_review_evidence_design()
        field_names = {field.name for field in design.future_review_evidence_fields}
        self.assertEqual(
            field_names,
            {
                "review_evidence_record_kind",
                "routing_case_id",
                "source_observation_schema_version",
                "review_reason_summary",
                "constraint_flags_for_review",
                "authority_notice",
                "review_storage_design_status",
                "requires_separate_human_review",
                "routing_effect",
                "prompt_loading_effect",
                "candidate_promotion_effect",
            },
        )
        for forbidden in FORBIDDEN_AUTHORITY_FIELDS:
            self.assertNotIn(forbidden, field_names)
        field_by_name = {field.name: field for field in design.future_review_evidence_fields}
        self.assertEqual(field_by_name["requires_separate_human_review"].requirement, "required_true")
        self.assertEqual(field_by_name["routing_effect"].requirement, "required_none")
        self.assertEqual(field_by_name["prompt_loading_effect"].requirement, "required_none")
        self.assertEqual(field_by_name["candidate_promotion_effect"].requirement, "required_none")

    def test_design_references_m23_observation_fields_but_does_not_transform_them(self):
        design = build_shadow_observation_review_evidence_design()
        self.assertIn("m23_non_runtime_shadow_observation_implementation_frozen", design.required_prior_milestones)
        self.assertEqual(
            set(design.allowed_source_observation_fields),
            {
                "observation_record_kind",
                "routing_case_id",
                "contract_schema_version",
                "authority_notice",
                "route_path_difference_observed",
                "constraint_flags_observed",
                "requires_separate_human_review",
                "human_review_reason_summary",
                "storage_status",
                "routing_effect",
                "prompt_loading_effect",
                "candidate_promotion_effect",
                "runtime_authority",
                "shadow_mode_status",
                "assistant_status",
            },
        )
        boundary_ids = {rule.boundary_id for rule in design.review_boundary_rules}
        self.assertIn("source_must_be_m23_non_runtime_observation", boundary_ids)
        self.assertIn("review_evidence_is_not_human_decision", boundary_ids)
        self.assertIn("review_evidence_is_not_persistence", boundary_ids)
        self.assertIn("review_evidence_is_not_shadow_activation", boundary_ids)

    def test_forbidden_behaviors_and_invariants_preserve_boundaries(self):
        design = build_shadow_observation_review_evidence_design()
        for forbidden in (
            "live_review_evidence_builder",
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
        ):
            self.assertIn(forbidden, design.forbidden_review_evidence_behaviors)
        for invariant in (
            "m24_is_design_only",
            "m24_has_no_callable_review_evidence_builder",
            "m24_does_not_transform_live_observations",
            "m24_does_not_persist_or_write_review_evidence",
            "m24_does_not_record_human_decisions",
            "future_review_evidence_must_remain_non_authoritative",
        ):
            self.assertIn(invariant, design.review_evidence_invariants)

    def test_public_exports_are_limited_to_design_builder(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_observation_review_evidence_design"])
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
            design = build_shadow_observation_review_evidence_design()
        after = sorted(path.name for path in ROOT.iterdir())
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(design.persistence_status, "not_implemented")

    def test_notes_and_runtime_exports_preserve_non_runtime_boundary(self):
        notes = NOTES.read_text(encoding="utf-8")
        for expected in (
            "M24 is a design-only post-Adviser milestone",
            "does not persist observations",
            "does not write reports",
            "does not record human approval, rejection, or override decisions",
            "Shadow mode is not active",
            "Auxiliar/Assistant has not started",
            "M25 - Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1",
        ):
            self.assertIn(expected, notes)
        runtime_init = RUNTIME_INIT.read_text(encoding="utf-8")
        runtime_contract = RUNTIME_CONTRACT.read_text(encoding="utf-8")
        self.assertNotIn("shadow_observation_review_evidence", runtime_init)
        self.assertNotIn("shadow_observation_review_evidence", runtime_contract)


if __name__ == "__main__":
    unittest.main()
