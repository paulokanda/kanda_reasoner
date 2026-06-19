from __future__ import annotations

import ast
import json
import pathlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.dry_run_artifact_generation_plan_design import (
    DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID,
    DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION,
    FORBIDDEN_PLAN_FIELDS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_DRY_RUN_MODE,
    REQUIRED_FORBIDDEN_ACTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PERMITTED_PLAN_OUTPUTS,
    REQUIRED_REVIEW_GATES,
    REQUIRED_REVIEW_QUESTIONS,
    REQUIRED_SOURCE_MATERIAL_POLICY,
    build_dry_run_artifact_generation_plan_contract,
    classify_dry_run_artifact_generation_plan_request,
    validate_dry_run_artifact_generation_plan_contract,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MODULE_PATH = BOX / "dry_run_artifact_generation_plan_design.py"
DESIGN_DOC = BOX / "design" / "routing_signal_scorer_v3_dry_run_artifact_generation_plan_design.md"
MANIFEST = BOX / "box_manifest.json"
CONTRACT = BOX / "contract.py"
INIT = BOX / "__init__.py"


class DryRunArtifactGenerationPlanDesignTests(unittest.TestCase):
    def test_build_plan_uses_expected_identity_schema_and_mode(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        self.assertEqual(contract["plan_id"], DRY_RUN_ARTIFACT_GENERATION_PLAN_FEATURE_ID)
        self.assertEqual(contract["schema_version"], DRY_RUN_ARTIFACT_GENERATION_PLAN_SCHEMA_VERSION)
        self.assertEqual(contract["plan_status"], "design_only")
        self.assertTrue(contract["declared_design_only"])
        self.assertEqual(contract["dry_run_mode"], REQUIRED_DRY_RUN_MODE)

    def test_source_material_policy_forbids_scans_and_raw_text(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        policy = set(contract["source_material_policy"])
        self.assertTrue(REQUIRED_SOURCE_MATERIAL_POLICY.issubset(policy))
        self.assertIn("no_prompt_library_scan", policy)
        self.assertIn("no_freeze_entry_scan", policy)
        self.assertIn("no_project_source_scan", policy)
        self.assertIn("no_raw_text_materialization", policy)

    def test_permitted_outputs_are_review_only(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        outputs = set(contract["permitted_plan_outputs"])
        self.assertTrue(REQUIRED_PERMITTED_PLAN_OUTPUTS.issubset(outputs))
        self.assertIn("dry_run_plan_summary", outputs)
        self.assertIn("future_generator_risk_register", outputs)
        self.assertIn("review_evidence_only", outputs)
        self.assertIn("no_artifact_written", outputs)
        self.assertNotIn("generated_artifact", outputs)
        self.assertNotIn("final_route", outputs)

    def test_review_gates_and_human_questions_are_complete(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        gates = set(contract["required_review_gates_before_future_generation"])
        questions = set(contract["planned_human_review_questions"])
        self.assertTrue(REQUIRED_REVIEW_GATES.issubset(gates))
        self.assertTrue(REQUIRED_REVIEW_QUESTIONS.issubset(questions))
        self.assertIn("separate_governed_patch_required", gates)
        self.assertIn("privacy_review_required", gates)
        self.assertIn("authority_leakage_gate_required", gates)
        self.assertIn("which_sources_would_future_generation_use", questions)
        self.assertIn("how_will_router_authority_remain_canonical", questions)

    def test_disabled_flags_remain_false(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        flags = contract["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, flags)
            self.assertIs(flags[flag], False, flag)

    def test_forbidden_actions_cover_generation_authority_and_side_effects(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        actions = set(contract["forbidden_actions"])
        self.assertTrue(REQUIRED_FORBIDDEN_ACTIONS.issubset(actions))
        for action in [
            "generate_artifact_from_plan",
            "write_artifact_from_plan",
            "scan_prompt_library_for_plan",
            "scan_freeze_entries_for_plan",
            "generate_embeddings",
            "create_vector_index",
            "instantiate_provider",
            "enable_semantic_runtime",
            "modify_prompt_router",
            "write_freeze_memory",
            "produce_may_proceed_now",
        ]:
            self.assertIn(action, actions)

    def test_no_authority_assertions_are_explicit(self) -> None:
        contract = build_dry_run_artifact_generation_plan_contract()
        assertions = set(contract["no_authority_assertions"])
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(assertions))
        self.assertIn("dry_run_plan_must_not_generate_artifacts", assertions)
        self.assertIn("dry_run_plan_must_not_choose_route", assertions)
        self.assertIn("dry_run_plan_must_not_write_freeze_memory", assertions)
        self.assertIn("canon_remains_final_authority", assertions)

    def test_valid_plan_validates_without_authority_or_generation(self) -> None:
        result = validate_dry_run_artifact_generation_plan_contract(
            build_dry_run_artifact_generation_plan_contract()
        )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["plan_report_only"])
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["artifact_writing_authorized"])
        self.assertFalse(result["source_scanning_authorized"])
        self.assertFalse(result["raw_text_materialization_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_generation_authorized"])
        self.assertFalse(result["provider_execution_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["prompt_router_mutation_authorized"])
        self.assertFalse(result["freeze_memory_write_authorized"])
        self.assertFalse(result["authority_granted"])
        self.assertTrue(result["review_evidence_only"])
        self.assertTrue(result["requires_future_governed_patch"])

    def test_validator_rejects_enabled_flags_and_forbidden_fields(self) -> None:
        for flag in [
            "artifact_generation_enabled",
            "artifact_writing_enabled",
            "source_scanning_enabled",
            "embedding_generation_enabled",
            "vector_index_generation_enabled",
            "provider_execution_enabled",
            "semantic_runtime_enabled",
            "write_freeze_memory_enabled",
        ]:
            contract = build_dry_run_artifact_generation_plan_contract()
            contract["disabled_flags"][flag] = True
            result = validate_dry_run_artifact_generation_plan_contract(contract)
            self.assertFalse(result["ok"], flag)
            self.assertIn("disabled flag must be false: " + flag, result["errors"])

        for field in FORBIDDEN_PLAN_FIELDS:
            contract = build_dry_run_artifact_generation_plan_contract()
            contract[field] = "forbidden"
            result = validate_dry_run_artifact_generation_plan_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(any("forbidden plan fields present" in error for error in result["errors"]), field)

    def test_request_classifier_allows_plan_review_only_but_denies_activation(self) -> None:
        plan = classify_dry_run_artifact_generation_plan_request("make a dry-run checklist and risk register")
        self.assertTrue(plan["allowed_now"])
        self.assertEqual(plan["permitted_output"], "dry_run_plan_summary")
        self.assertFalse(plan["artifact_generation_authorized"])
        self.assertFalse(plan["artifact_writing_authorized"])
        self.assertTrue(plan["review_evidence_only"])

        for action in [
            "generate artifact now",
            "write artifact from the plan",
            "create embeddings",
            "create vector index",
            "use provider at runtime",
            "run at startup",
            "enable semantic runtime",
            "write freeze memory",
        ]:
            result = classify_dry_run_artifact_generation_plan_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_generation_authorized"], action)
            self.assertFalse(result["artifact_writing_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_index_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["authority_granted"], action)
            self.assertTrue(result["requires_future_governed_patch_for_generation"], action)

    def test_design_doc_preserves_plan_only_boundary(self) -> None:
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1",
            "Design-only dry-run planning contract",
            "The plan is review evidence only.",
            "It is not a generator.",
            "It cannot create files.",
            "It cannot scan project sources.",
            "Real generation remains forbidden",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_runtime_export(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["dry_run_artifact_generation_plan_design_feature_id"],
            "routing_signal_scorer_v3_dry_run_artifact_generation_plan_design_v1",
        )
        self.assertEqual(
            manifest["dry_run_artifact_generation_plan_design_status"],
            "standard_library_only_dry_run_plan_design_no_generation_no_artifact_writing_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["dry_run_artifact_generation_plan_schema_version"],
            "3.13-dry-run-artifact-generation-plan-design",
        )
        for characteristic in [
            "dry_run_artifact_generation_plan_design",
            "dry_run_plan_only_no_generation",
            "no_artifact_generation_from_dry_run_plan",
            "no_artifact_writing_from_dry_run_plan",
            "no_source_scanning_from_dry_run_plan",
            "no_raw_text_materialization_from_dry_run_plan",
            "no_embeddings_from_dry_run_plan",
            "no_vectors_from_dry_run_plan",
            "no_provider_execution_from_dry_run_plan",
            "no_runtime_enablement_from_dry_run_plan",
            "future_generation_after_dry_run_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("build_dry_run_artifact_generation_plan_contract", provides)
        self.assertNotIn("validate_dry_run_artifact_generation_plan_contract", provides)
        self.assertNotIn("classify_dry_run_artifact_generation_plan_request", provides)
        self.assertNotIn("build_dry_run_artifact_generation_plan_contract", CONTRACT.read_text(encoding="utf-8"))
        self.assertNotIn("build_dry_run_artifact_generation_plan_contract", INIT.read_text(encoding="utf-8"))

    def test_module_is_standard_library_only_and_has_no_side_effect_calls(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imports = []
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
                elif isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
        for imported in imports:
            self.assertTrue(
                imported.startswith("__future__")
                or imported.startswith("collections")
                or imported.startswith("typing"),
                imported,
            )
        for forbidden_call in [
            "open",
            "write_text",
            "read_text",
            "mkdir",
            "unlink",
            "replace",
            "rename",
            "rglob",
            "glob",
            "scandir",
            "listdir",
            "system",
            "run",
            "Popen",
        ]:
            self.assertNotIn(forbidden_call, calls)

    def test_no_runtime_generation_paths_or_root_freeze_hint_exist(self) -> None:
        for relative in [
            "artifact_generator.py",
            "precomputed_artifact_generator.py",
            "precomputed_semantic_evidence_artifact_generator.py",
            "generated_artifacts",
            "artifacts",
            "vector_index.py",
            "indices",
            "providers",
        ]:
            self.assertFalse((BOX / relative).exists(), relative)
        self.assertFalse((ROOT / "KANDA_FREEZE_HINT.json").exists())


if __name__ == "__main__":
    unittest.main()
