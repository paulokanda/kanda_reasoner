import ast
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_boundary_design import (
    FEATURE_ID as P1_FEATURE_ID,
    NEXT_ALLOWED_MILESTONE as P1_NEXT_ALLOWED_MILESTONE,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.pilot_io_contract_validator_design import (
    ACTIVATION_EFFECT,
    AUTHORITY_STATEMENT,
    DESIGN_KIND,
    FEATURE_ID,
    HUMAN_REVIEW_MANDATORY,
    NEXT_ALLOWED_MILESTONE,
    PROMPT_LOADING_EFFECT,
    ROUTING_EFFECT,
    RUNTIME_EFFECT,
    SCHEMA_VERSION,
    STORAGE_STATUS,
    PilotIOContractValidatorDesign,
    build_pilot_io_contract_validator_design,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_io_contract_validator_design.py"
NOTES = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "adviser_offline" / "transition_design" / "pilot_io_contract_validator_notes.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

ALLOWED_IMPORTS = {"__future__", "dataclasses", "typing"}
FORBIDDEN_IMPORT_FRAGMENTS = (
    "runtime",
    "router",
    "prompt_loader",
    "freeze_after_update",
    "project_freeze_ledger",
    "gold",
    "registry",
    "openai",
    "anthropic",
    "cohere",
    "embedding",
    "subprocess",
    "socket",
    "threading",
    "multiprocessing",
    "asyncio",
    "pathlib",
    "os",
    "sys",
    "importlib",
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
    "validate_pilot_input",
    "validate_pilot_output",
    "process_pilot_input",
    "generate_pilot_output",
    "run_pilot",
    "start_pilot",
    "activate_pilot",
    "run_copilot",
    "start_copilot",
    "activate_copilot",
    "project_route",
    "compare_routes",
    "select_route",
    "override_route",
    "execute_route",
    "select_prompt",
    "load_prompt",
    "persist_output",
    "write_report",
    "write_review_queue",
    "record_human_decision",
    "run_batch",
    "train_on_pilot_output",
)
UNSAFE_ALLOWED_FIELD_NAMES = {
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
    "runtime_authority",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "human_review_completed",
    "promotion_ready",
    "route_override",
    "prompt_to_load",
    "copilot_ready",
    "runtime_enabled",
    "requires_human_review",
}


class PilotIOContractValidatorDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def test_p1_is_present_and_points_to_p2_before_p2(self):
        self.assertEqual(P1_FEATURE_ID, "routing_signal_scorer_v3_pilot_boundary_design_v1")
        self.assertIn("P2 - Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1", P1_NEXT_ALLOWED_MILESTONE)

    def test_manifest_declares_p2_contract_validator_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        prefix = "pilot_io_contract_validator_design"
        self.assertEqual(manifest[f"{prefix}_feature_id"], FEATURE_ID)
        self.assertEqual(manifest[f"{prefix}_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest[f"{prefix}_status"], "immutable_design_only_pilot_io_contract_validator_no_live_validation_no_runtime_authority")
        self.assertEqual(manifest[f"{prefix}_module"], str(MODULE.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_notes_doc"], str(NOTES.relative_to(ROOT)).replace("\\", "/"))
        self.assertEqual(manifest[f"{prefix}_next_allowed_milestone"], NEXT_ALLOWED_MILESTONE)
        self.assertIs(manifest[f"{prefix}_requires_p1_pilot_boundary_design"], True)
        self.assertIs(manifest[f"{prefix}_requires_p0_scope_charter_entry_gate_design"], True)
        self.assertIs(manifest[f"{prefix}_requires_rg_pilot_000_router_canon"], True)
        for key in (
            f"{prefix}_contains_live_validator",
            f"{prefix}_contains_input_processing",
            f"{prefix}_contains_output_generation",
            f"{prefix}_contains_live_pilot_behavior",
            f"{prefix}_contains_live_copilot_behavior",
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

    def test_p2_returns_static_immutable_design_record(self):
        first = build_pilot_io_contract_validator_design()
        second = build_pilot_io_contract_validator_design()
        self.assertIs(first, second)
        self.assertTrue(is_dataclass(first))
        self.assertIsInstance(first, PilotIOContractValidatorDesign)
        with self.assertRaises(FrozenInstanceError):
            first.milestone = "changed"
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.milestone, "P2")
        self.assertEqual(first.title, "Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1")
        self.assertEqual(first.authority_statement, AUTHORITY_STATEMENT)
        self.assertEqual(first.design_status, "design_only")
        self.assertEqual(first.validator_status, "design_only_no_live_validator")
        self.assertEqual(first.pilot_status, "not_started_not_active")
        self.assertEqual(first.copilot_status, "not_started_deferred")
        self.assertEqual(first.runtime_authority_status, "not_granted")
        self.assertEqual(first.prompt_loading_authority_status, "not_granted")
        self.assertEqual(first.persistence_authority_status, "not_granted")
        self.assertEqual(first.training_data_use_status, "forbidden")
        self.assertEqual(first.batch_mode_status, "forbidden")
        self.assertEqual(first.limited_shadow_runtime_status, "out_of_scope_separate_future_governed_scope_required")
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)

    def test_preconditions_require_p1_and_freeze_status_before_p2(self):
        design = build_pilot_io_contract_validator_design()
        for item in (
            "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
            "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
            "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
            "p1_pilot_boundary_design_frozen",
            "startup_freeze_context_refreshed_after_p1",
            "freeze_memory_status_ok_after_p1",
        ):
            self.assertIn(item, design.required_preconditions)

    def test_allowed_input_fields_are_exact_and_avoid_prompt_group_language(self):
        design = build_pilot_io_contract_validator_design()
        names = tuple(field.field_name for field in design.allowed_input_fields)
        self.assertEqual(
            names,
            (
                "case_id",
                "schema_version",
                "user_request_summary",
                "routing_context_public_summary",
                "task_classification_hints_summary",
                "current_router_outcome_summary",
                "frozen_canon_constraints_summary",
                "known_boundary_flags",
                "caller_generated_timestamp_utc",
            ),
        )
        self.assertNotIn("candidate_prompt_groups", names)
        self.assertTrue(set(names).isdisjoint(UNSAFE_ALLOWED_FIELD_NAMES))
        shapes = {field.field_name: field.value_shape for field in design.allowed_input_fields}
        self.assertEqual(shapes["known_boundary_flags"], "tuple[str, ...]")
        for name, shape in shapes.items():
            if name != "known_boundary_flags":
                self.assertEqual(shape, "str")

    def test_allowed_output_fields_are_exact_non_authoritative_and_fixed_effects(self):
        design = build_pilot_io_contract_validator_design()
        names = tuple(field.field_name for field in design.allowed_output_fields)
        self.assertEqual(
            names,
            (
                "pilot_record_kind",
                "case_id",
                "schema_version",
                "authority_notice",
                "projection_analysis_summary",
                "task_classification_projection_summary",
                "reasoning_summary_for_human_review",
                "boundary_flags_for_human_review",
                "divergence_summary_for_human_review",
                "divergence_type",
                "missing_information_summary",
                "human_review_mandatory",
                "advisory_review_priority",
                "routing_effect",
                "prompt_loading_effect",
                "runtime_effect",
                "activation_effect",
                "storage_status",
            ),
        )
        self.assertTrue(set(names).isdisjoint(UNSAFE_ALLOWED_FIELD_NAMES))
        self.assertIn("projection_analysis_summary", names)
        self.assertNotIn("recommendation", names)
        self.assertNotIn("requires_human_review", names)

    def test_fixed_output_invariants_use_module_level_constants(self):
        self.assertEqual(ROUTING_EFFECT, "none")
        self.assertEqual(PROMPT_LOADING_EFFECT, "none")
        self.assertEqual(RUNTIME_EFFECT, "none")
        self.assertEqual(ACTIVATION_EFFECT, "none")
        self.assertEqual(STORAGE_STATUS, "in_memory_only")
        self.assertIs(HUMAN_REVIEW_MANDATORY, True)
        design = build_pilot_io_contract_validator_design()
        invariants = {item.invariant_id: item for item in design.fixed_output_invariants}
        self.assertEqual(invariants["routing_effect_none"].required_value, "none")
        self.assertEqual(invariants["prompt_loading_effect_none"].required_value, "none")
        self.assertEqual(invariants["runtime_effect_none"].required_value, "none")
        self.assertEqual(invariants["activation_effect_none"].required_value, "none")
        self.assertEqual(invariants["storage_status_in_memory_only"].required_value, "in_memory_only")
        self.assertEqual(invariants["human_review_mandatory_true"].required_value, "True")
        for item in invariants.values():
            self.assertEqual(item.value_source, "module_level_constant")

    def test_validator_rules_are_fail_closed_design_not_live_validator(self):
        design = build_pilot_io_contract_validator_design()
        input_rule_ids = {rule.rule_id for rule in design.input_validator_rules}
        for expected in (
            "reject_unknown_input_keys",
            "reject_missing_required_input_keys",
            "reject_blank_required_strings",
            "reject_callable_values",
            "reject_file_handles",
            "reject_runtime_objects",
            "reject_prompt_loading_instructions",
            "reject_route_execution_instructions",
            "reject_gold_registry_mutation_instructions",
            "reject_persistence_training_batch_activation_instructions",
        ):
            self.assertIn(expected, input_rule_ids)
        output_rule_ids = {rule.rule_id for rule in design.output_validator_rules}
        for expected in (
            "reject_unknown_output_keys",
            "reject_forbidden_output_names",
            "require_exact_authority_notice",
            "require_human_review_mandatory_true",
            "require_fixed_no_effect_constants",
            "require_storage_status_in_memory_only",
            "require_divergence_type_from_p3_taxonomy",
        ):
            self.assertIn(expected, output_rule_ids)
        for rule in design.input_validator_rules + design.output_validator_rules:
            self.assertEqual(rule.required_failure_mode, "reject_fail_closed")

    def test_forbidden_names_are_recorded_but_not_allowed(self):
        design = build_pilot_io_contract_validator_design()
        forbidden = {item.name for item in design.forbidden_field_names}
        for expected in UNSAFE_ALLOWED_FIELD_NAMES:
            self.assertIn(expected, forbidden)
        allowed = {field.field_name for field in design.allowed_input_fields + design.allowed_output_fields}
        self.assertTrue(allowed.isdisjoint(forbidden))
        replacement_by_name = {item.name: item.replacement_policy for item in design.forbidden_field_names}
        self.assertEqual(replacement_by_name["candidate_prompt_groups"], "use_task_classification_hints_summary")
        self.assertEqual(replacement_by_name["simulated_required_prompt_groups"], "use_task_classification_projection_summary")
        self.assertEqual(replacement_by_name["requires_human_review"], "use_human_review_mandatory")

    def test_contract_design_invariants_and_forbidden_operations_block_runtime(self):
        design = build_pilot_io_contract_validator_design()
        for expected in (
            "p2_is_design_only",
            "p2_does_not_implement_live_validation",
            "p2_does_not_process_input_payloads",
            "p2_does_not_generate_output_payloads",
            "human_review_mandatory_is_fixed_true",
            "effect_fields_are_fixed_module_level_constants",
            "prompt_group_field_names_are_forbidden",
            "training_data_use_is_forbidden",
            "batch_mode_is_forbidden",
            "p3_taxonomy_required_before_divergence_type_use",
            "p6_gate_required_before_callable_projection",
        ):
            self.assertIn(expected, design.contract_design_invariants)
        for expected in (
            "implement_live_validator",
            "process_input_payloads",
            "generate_output_payloads",
            "run_pilot",
            "run_copilot",
            "implement_projection_logic",
            "execute_route_comparison",
            "load_prompt",
            "persist_output",
            "use_output_as_training_data",
            "run_batch_mode",
            "activate_limited_shadow_runtime",
            "grant_runtime_authority",
        ):
            self.assertIn(expected, design.forbidden_operations)

    def test_module_has_only_safe_imports_and_no_forbidden_calls(self):
        tree = self._module_ast()
        imports = []
        calls = []
        defs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defs.append(node.name)
        for item in imports:
            root = item.split(".")[0]
            self.assertIn(root, ALLOWED_IMPORTS, item)
            self.assertFalse(any(fragment in item for fragment in FORBIDDEN_IMPORT_FRAGMENTS), item)
        for name in FORBIDDEN_CALLS:
            self.assertNotIn(name, calls)
        for name in FORBIDDEN_RUNTIME_BEHAVIOR_DEFS:
            self.assertNotIn(name, defs)

    def test_public_exports_are_design_only(self):
        tree = self._module_ast()
        text = MODULE.read_text(encoding="utf-8")
        self.assertIn("build_pilot_io_contract_validator_design", text)
        for name in FORBIDDEN_RUNTIME_BEHAVIOR_DEFS:
            self.assertNotIn(f"def {name}", text)
        self.assertNotIn("def validate_", text)
        self.assertNotIn("def process_", text)
        self.assertNotIn("def generate_", text)
        self.assertGreater(len(tree.body), 1)

    def test_notes_and_source_are_ascii_and_restate_no_runtime_boundary(self):
        source = MODULE.read_text(encoding="utf-8")
        notes = NOTES.read_text(encoding="utf-8")
        source.encode("ascii")
        notes.encode("ascii")
        combined = source + "\n" + notes
        for expected in (
            "does not implement a live validator",
            "does not process inputs",
            "does not generate outputs",
            "does not implement Pilot",
            "does not implement Copilot",
            "does not implement projection logic",
            "does not load prompts",
            "does not persist output",
            "does not use output as training data",
            "does not run batch mode",
            "does not grant runtime authority",
            "P3 - Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1",
        ):
            self.assertIn(expected, combined)


if __name__ == "__main__":
    unittest.main()
