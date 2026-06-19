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
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_io_contract_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_io_contract_design.py"
NOTES = TRANSITION / "shadow_mode_io_contract_notes.md"
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

FORBIDDEN_OUTPUT_FIELD_NAMES = (
    "final_route",
    "route_override",
    "selected_prompt",
    "prompt_to_load",
    "approved",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "candidate_promoted",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_freeze",
    "confirm_and_write",
    "router_authority_granted",
    "runtime_effect",
)


class ShadowModeIOContractDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _field_names(self, fields):
        return {field.name for field in fields}

    def test_manifest_declares_m19_contract_design_without_runtime_behavior(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_io_contract_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_io_contract_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_io_contract_design_status"],
            "immutable_design_only_io_contract_no_validation_no_observation_no_runtime_authority",
        )
        self.assertEqual(
            manifest["shadow_mode_io_contract_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )
        for key in (
            "shadow_mode_io_contract_design_contains_input_processing",
            "shadow_mode_io_contract_design_contains_output_generation",
            "shadow_mode_io_contract_design_contains_validator_logic",
            "shadow_mode_io_contract_design_contains_observation_execution",
            "shadow_mode_io_contract_design_contains_file_io",
            "shadow_mode_io_contract_design_contains_persistence",
            "shadow_mode_io_contract_design_contains_prompt_loading",
            "shadow_mode_io_contract_design_contains_runtime_integration",
            "shadow_mode_io_contract_design_contains_router_authority",
            "shadow_mode_io_contract_design_contains_candidate_promotion",
            "shadow_mode_io_contract_design_contains_shadow_activation",
            "shadow_mode_io_contract_design_contains_assistant_behavior",
            "shadow_mode_io_contract_design_contains_embeddings_or_providers",
            "shadow_mode_io_contract_design_contains_report_writer",
            "shadow_mode_io_contract_design_contains_gold_or_registry_mutation",
        ):
            self.assertIs(manifest[key], False, key)

    def test_contract_record_is_immutable_static_and_design_only(self):
        m18 = build_shadow_mode_boundary_design()
        self.assertEqual(m18.next_allowed_milestone, "M19 - Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1")
        first = build_shadow_mode_io_contract_design()
        second = build_shadow_mode_io_contract_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "M19")
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.lifecycle_status, "design_only_no_shadow_observation_execution")
        self.assertEqual(first.input_contract_status, "static_schema_design_only_no_input_processing")
        self.assertEqual(first.output_contract_status, "static_schema_design_only_no_output_generation")
        self.assertEqual(first.validator_status, "not_implemented_deferred_to_m20")
        self.assertEqual(first.observation_execution_status, "not_implemented")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        with self.assertRaises(FrozenInstanceError):
            first.feature_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.allowed_input_fields[0].name = "changed"

    def test_contract_fields_define_schema_without_processing(self):
        record = build_shadow_mode_io_contract_design()
        input_names = self._field_names(record.allowed_input_fields)
        output_names = self._field_names(record.allowed_output_fields)
        for expected in (
            "routing_case_id",
            "user_request_summary",
            "current_router_summary",
            "current_router_path_summary",
            "current_prompt_group_summary",
            "scorer_candidate_summary",
            "scorer_constraint_flags_summary",
            "boundary_context_summary",
            "caller_generated_timestamp_utc",
        ):
            self.assertIn(expected, input_names)
        for expected in (
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
        ):
            self.assertIn(expected, output_names)
        for field in record.allowed_input_fields + record.allowed_output_fields:
            self.assertNotEqual(field.description.strip(), "")
            self.assertNotEqual(field.source_rule.strip(), "")

    def test_contract_forbids_live_objects_unknown_keys_and_authority_fields(self):
        record = build_shadow_mode_io_contract_design()
        self.assertIn("unknown_keys", record.forbidden_input_kinds)
        for forbidden in (
            "live_router_object",
            "prompt_object",
            "file_handle",
            "path_object",
            "callable_object",
            "module_object",
            "registry_object",
            "gold_mutation_object",
            "freeze_writer_object",
            "provider_client_object",
            "embedding_index_object",
        ):
            self.assertIn(forbidden, record.forbidden_input_kinds)
        output_names = self._field_names(record.allowed_output_fields)
        for forbidden in FORBIDDEN_OUTPUT_FIELD_NAMES:
            self.assertIn(forbidden, record.forbidden_output_fields)
            self.assertNotIn(forbidden, output_names)

    def test_contract_invariants_preserve_m18_boundary_and_defer_m20_logic(self):
        record = build_shadow_mode_io_contract_design()
        for invariant in (
            "m19_is_design_only",
            "schemas_are_static_contracts_not_validators",
            "future_inputs_must_be_caller_supplied_json_safe_primitives",
            "future_inputs_must_reject_unknown_keys",
            "future_outputs_must_remain_in_memory_non_authoritative_evidence",
            "future_outputs_must_not_direct_routes_or_prompt_loading",
            "future_outputs_must_not_persist_or_mutate_gold_registry_or_freeze_memory",
            "future_outputs_must_require_separate_human_review_by_default",
            "m20_is_required_before_contract_validation_logic",
        ):
            self.assertIn(invariant, record.contract_invariants)
        for primitive in (
            "string",
            "integer",
            "float",
            "boolean",
            "null",
            "list_of_primitives",
            "object_with_declared_keys_only",
        ):
            self.assertIn(primitive, record.json_safe_primitive_kinds)

    def test_public_exports_do_not_add_side_effect_entry_points(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_io_contract_design"])

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

    def test_contract_builder_has_no_file_or_console_side_effects(self):
        before = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            record = build_shadow_mode_io_contract_design()
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(record.observation_execution_status, "not_implemented")

    def test_notes_exist_and_keep_m19_design_only(self):
        text = NOTES.read_text(encoding="utf-8")
        required = (
            "M19 is design-only.",
            "M19 may define static contract shapes only.",
            "Future inputs must be caller-supplied, serialized, JSON-safe primitives.",
            "Future outputs must remain in-memory non-authoritative evidence.",
            "The next allowed milestone is M20",
        )
        for item in required:
            self.assertIn(item, text)

    def test_runtime_package_does_not_export_m19_contract_design(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "shadow_mode_io_contract_design",
            "build_shadow_mode_io_contract_design",
            "ShadowModeIOContractDesign",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
