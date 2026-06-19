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
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_io_contract_design import (
    build_shadow_mode_io_contract_design,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_contract_validator_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_contract_validator_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_contract_validator_design.py"
NOTES = TRANSITION / "shadow_mode_contract_validator_notes.md"
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

FORBIDDEN_LIVE_BEHAVIOR_WORDS = (
    "validate_shadow_mode_input",
    "validate_shadow_mode_output",
    "process_input",
    "generate_output",
    "execute_observation",
    "compare_routes",
    "load_prompt",
    "write_report",
    "persist",
    "promote_candidate",
    "activate_shadow_mode",
    "start_assistant",
)


class ShadowModeContractValidatorDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _rule_ids(self, rules):
        return {rule.rule_id for rule in rules}

    def test_manifest_declares_m20_validator_design_without_live_behavior(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_contract_validator_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_contract_validator_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_contract_validator_design_status"],
            "immutable_design_only_validator_rule_design_no_live_validation_no_observation_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_contract_validator_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        for key in (
            "shadow_mode_contract_validator_design_contains_live_validation_execution",
            "shadow_mode_contract_validator_design_contains_callable_validator_entrypoint",
            "shadow_mode_contract_validator_design_contains_input_processing",
            "shadow_mode_contract_validator_design_contains_output_generation",
            "shadow_mode_contract_validator_design_contains_observation_execution",
            "shadow_mode_contract_validator_design_contains_shadow_activation",
            "shadow_mode_contract_validator_design_contains_assistant_behavior",
            "shadow_mode_contract_validator_design_contains_runtime_integration",
            "shadow_mode_contract_validator_design_contains_router_authority",
            "shadow_mode_contract_validator_design_contains_prompt_loading",
            "shadow_mode_contract_validator_design_contains_file_io",
            "shadow_mode_contract_validator_design_contains_persistence",
            "shadow_mode_contract_validator_design_contains_report_writer",
            "shadow_mode_contract_validator_design_contains_gold_or_registry_mutation",
            "shadow_mode_contract_validator_design_contains_candidate_promotion",
            "shadow_mode_contract_validator_design_contains_embeddings_or_providers",
        ):
            self.assertIs(manifest[key], False, key)

    def test_validator_design_record_is_immutable_static_and_design_only(self):
        m18 = build_shadow_mode_boundary_design()
        m19 = build_shadow_mode_io_contract_design()
        self.assertEqual(m18.next_allowed_milestone, "M19 - Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1")
        self.assertEqual(m19.next_allowed_milestone, "M20 - Routing Signal Scorer v3 Shadow Mode Contract Validator Design v1")
        first = build_shadow_mode_contract_validator_design()
        second = build_shadow_mode_contract_validator_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M20")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "design_only_no_live_validation_execution")
        self.assertEqual(first.validator_design_status, "static_rule_design_only_no_validator_function")
        self.assertEqual(first.live_validation_status, "not_implemented")
        self.assertEqual(first.observation_execution_status, "not_implemented")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        with self.assertRaises(FrozenInstanceError):
            first.feature_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.planned_input_validation_rules[0].rule_id = "changed"

    def test_preconditions_require_m18_m19_and_future_human_review(self):
        record = build_shadow_mode_contract_validator_design()
        for expected in (
            "m18_shadow_mode_boundary_design_frozen",
            "m19_shadow_mode_input_output_contract_design_frozen",
            "freezememory_status_ok_before_later_executable_validation",
            "separate_human_review_required_before_later_executable_validation",
        ):
            self.assertIn(expected, record.required_preconditions)

    def test_validator_rules_define_future_checks_without_live_validation(self):
        record = build_shadow_mode_contract_validator_design()
        input_rule_ids = self._rule_ids(record.planned_input_validation_rules)
        output_rule_ids = self._rule_ids(record.planned_output_validation_rules)
        for expected in (
            "input_unknown_keys_rejected",
            "input_json_safe_primitives_only",
            "input_live_objects_rejected",
            "input_caller_supplied_only",
            "input_required_fields_checked_later",
        ):
            self.assertIn(expected, input_rule_ids)
        for expected in (
            "output_declared_keys_only",
            "output_authority_notice_required",
            "output_no_route_or_prompt_directives",
            "output_no_governed_write_directives",
            "output_no_readiness_metrics",
            "output_in_memory_non_authoritative_only",
        ):
            self.assertIn(expected, output_rule_ids)
        for rule in record.planned_input_validation_rules + record.planned_output_validation_rules:
            self.assertNotEqual(rule.description.strip(), "")
            self.assertIn(rule.default_disposition, ("reject_in_future_validator_design", "block_in_future_validator_design"))

    def test_forbidden_behaviors_block_runtime_authority_and_side_effects(self):
        record = build_shadow_mode_contract_validator_design()
        for forbidden in (
            "live_input_validation_execution",
            "callable_validator_entrypoint",
            "observation_generation",
            "route_comparison",
            "candidate_execution",
            "prompt_loading",
            "source_scanning",
            "case_discovery",
            "file_io",
            "console_io",
            "logging",
            "persistence",
            "report_writing",
            "registry_writing",
            "gold_mutation",
            "freeze_writing",
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
            self.assertIn(forbidden, record.forbidden_validator_behaviors)

    def test_invariants_defer_executable_validation_and_observation_logic(self):
        record = build_shadow_mode_contract_validator_design()
        for invariant in (
            "m20_is_design_only",
            "m20_defines_future_validator_rules_only",
            "m20_does_not_validate_live_input",
            "m20_does_not_generate_or_validate_live_observations",
            "future_validator_must_fail_closed_on_unknown_input_keys",
            "future_validator_must_reject_non_primitive_inputs",
            "future_validator_must_block_authority_fields",
            "future_validator_must_keep_outputs_non_authoritative",
            "future_validator_must_not_persist_or_mutate_project_state",
            "m21_is_required_before_observation_skeleton_design",
        ):
            self.assertIn(invariant, record.validator_invariants)

    def test_public_exports_do_not_add_live_validator_entry_points(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_contract_validator_design"])
        text = MODULE.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_LIVE_BEHAVIOR_WORDS:
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
            record = build_shadow_mode_contract_validator_design()
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(record.live_validation_status, "not_implemented")

    def test_notes_exist_and_keep_m20_design_only(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M20 is design-only.",
            "M20 defines future contract validator behavior",
            "It does not implement a callable validator",
            "Future validation must fail closed on unknown input keys.",
            "The next allowed milestone is M21",
        )
        for item in required:
            self.assertIn(item, text)

    def test_runtime_package_does_not_export_m20_validator_design(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "shadow_mode_contract_validator_design",
            "build_shadow_mode_contract_validator_design",
            "ShadowModeContractValidatorDesign",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
