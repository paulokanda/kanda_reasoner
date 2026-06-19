import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.disabled_evaluation_runner_design import (
    DISABLED_EVALUATION_RUNNER_FEATURE_ID,
    build_disabled_evaluation_runner_status,
    build_minimal_valid_disabled_runner_contract,
    classify_runner_activation_request,
    validate_disabled_evaluation_runner_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "disabled_evaluation_runner_design.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_disabled_evaluation_runner_design.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class DisabledEvaluationRunnerDesignTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            DISABLED_EVALUATION_RUNNER_FEATURE_ID,
            "routing_signal_scorer_v3_disabled_evaluation_runner_design_v1",
        )
        status = build_disabled_evaluation_runner_status()
        self.assertFalse(status["evaluation_runner_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertFalse(status["threshold_auto_tuning_enabled"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["corpus_generation_enabled"])
        self.assertFalse(status["external_api_enabled"])
        self.assertFalse(status["startup_run_enabled"])
        self.assertFalse(status["runtime_run_enabled"])
        self.assertFalse(status["background_job_enabled"])
        self.assertFalse(status["file_watcher_enabled"])
        self.assertTrue(status["advisory_only"])
        self.assertTrue(status["lexical_fallback_primary"])

    def test_minimal_valid_contract_is_valid_but_authorizes_nothing(self):
        contract = build_minimal_valid_disabled_runner_contract()
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["evaluation_runner_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["threshold_changes_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_authorized"])
        self.assertFalse(result["external_api_authorized"])
        self.assertFalse(result["freeze_memory_write_authorized"])
        self.assertFalse(result["prompt_router_mutation_authorized"])
        self.assertTrue(result["advisory_only"])

    def test_all_enabled_flags_must_be_false(self):
        contract = build_minimal_valid_disabled_runner_contract()
        for flag in [
            "evaluation_execution_enabled",
            "semantic_runtime_enabled",
            "threshold_auto_tuning_enabled",
            "embedding_generation_enabled",
            "vector_index_generation_enabled",
            "external_api_enabled",
            "startup_run_enabled",
            "runtime_run_enabled",
            "background_job_enabled",
            "file_watcher_enabled",
            "prompt_router_mutation_enabled",
        ]:
            mutated = build_minimal_valid_disabled_runner_contract()
            mutated["enabled_flags"][flag] = True
            result = validate_disabled_evaluation_runner_contract(mutated)
            self.assertFalse(result["ok"], flag)
            self.assertTrue(any("must be false" in error for error in result["errors"]), result["errors"])

    def test_missing_required_preconditions_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["preconditions_before_any_future_runner"] = []
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("future preconditions" in error for error in result["errors"]))

    def test_missing_future_inputs_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["required_inputs_for_future_manual_runner"] = []
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("future manual-runner inputs" in error for error in result["errors"]))

    def test_missing_forbidden_actions_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["forbidden_actions"] = []
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden actions" in error for error in result["errors"]))

    def test_missing_review_gates_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["review_gates"] = []
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("review gates" in error for error in result["errors"]))

    def test_missing_no_authority_assertions_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["no_authority_assertions"] = []
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("no-authority assertions" in error for error in result["errors"]))

    def test_authority_fields_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["final_route"] = "governed_patch"
        contract["required_prompts"] = ["anything"]
        contract["may_proceed_now"] = True
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden authority fields" in error for error in result["errors"]))

    def test_raw_text_fields_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["raw_user_query"] = "do not store raw query"
        contract["prompt_body_text"] = "do not store prompt body"
        contract["freeze_entry_text"] = "do not store freeze entry"
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden raw/private text fields" in error for error in result["errors"]))

    def test_vector_and_provider_fields_are_rejected(self):
        contract = build_minimal_valid_disabled_runner_contract()
        contract["embedding"] = [0.1, 0.2]
        contract["vector_index"] = "forbidden"
        contract["provider_name"] = "forbidden"
        result = validate_disabled_evaluation_runner_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden vector/provider fields" in error for error in result["errors"]))

    def test_activation_requests_never_authorize_execution(self):
        for action in [
            "run evaluation",
            "run_at_startup",
            "enable semantic runtime",
            "adjust thresholds",
            "create vector index",
            "write freeze memory",
            "produce may proceed",
        ]:
            result = classify_runner_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["evaluation_runner_authorized"], action)
            self.assertFalse(result["threshold_changes_authorized"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_disabled_runner_rules(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Disabled Evaluation Runner Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "design/contract only",
            "disabled-by-default contract",
            "No-authority assertions",
            "This design does not authorize evaluation execution.",
            "This design does not authorize semantic runtime enablement.",
            "This design does not authorize threshold changes.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["disabled_evaluation_runner_design_feature_id"],
            "routing_signal_scorer_v3_disabled_evaluation_runner_design_v1",
        )
        self.assertEqual(
            manifest["disabled_evaluation_runner_design_status"],
            "standard_library_only_disabled_runner_design_no_runner_no_ml_behavior_change",
        )
        self.assertEqual(
            manifest["disabled_evaluation_runner_schema_version"],
            "3.6-disabled-evaluation-runner-design",
        )
        self.assertEqual(
            manifest["disabled_evaluation_runner_policy"],
            "disabled_design_only_no_execution_no_startup_no_runtime_no_background_no_threshold_tuning_no_runtime_enablement",
        )
        for characteristic in [
            "disabled_evaluation_runner_design",
            "evaluation_runner_design_disabled_only",
            "no_evaluation_runner_added",
            "no_evaluation_execution_enabled",
            "no_startup_evaluation_run",
            "no_runtime_evaluation_run",
            "no_background_evaluation_run",
            "no_threshold_auto_tuning_from_runner",
            "no_semantic_runtime_enablement_from_runner",
            "runner_outputs_review_evidence_only",
            "future_runner_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("validate_disabled_evaluation_runner_contract", provides)
        self.assertNotIn("build_disabled_evaluation_runner_status", provides)

    def test_module_is_stdlib_only_and_does_not_import_neighbor_boxes(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_roots = set()
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name)
                    imported_roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
                imported_roots.add(node.module.split(".")[0])
        forbidden_roots = {
            "numpy", "pandas", "sklearn", "scipy", "torch", "tensorflow",
            "sentence_transformers", "transformers", "faiss", "chromadb",
            "qdrant_client", "langchain", "llama_index",
        }
        self.assertFalse(forbidden_roots & imported_roots)
        for forbidden_module in [
            "kanda_prompt_workspace",
            "project_freeze_ledger",
            "project_freeze_after_update",
            "kanda_reasoner_app.freeze_hint_intake",
            "kanda_reasoner_app.freeze_after_update",
            "kanda_reasoner_app.freeze_after_update_gui",
        ]:
            self.assertNotIn(forbidden_module, imported_modules)

    def test_forbidden_runtime_artifacts_absent(self):
        for path in [
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "evaluation_runner.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "corpus_generator.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]:
            self.assertFalse(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
