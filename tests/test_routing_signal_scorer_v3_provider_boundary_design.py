import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.provider_boundary_design import (
    PROVIDER_BOUNDARY_FEATURE_ID,
    build_minimal_valid_provider_boundary_contract,
    build_provider_boundary_status,
    classify_provider_activation_request,
    validate_provider_boundary_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "provider_boundary_design.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_provider_boundary_design.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class ProviderBoundaryDesignTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            PROVIDER_BOUNDARY_FEATURE_ID,
            "routing_signal_scorer_v3_provider_boundary_design_v1",
        )
        status = build_provider_boundary_status()
        self.assertEqual(status["default_provider"], "disabled_null_provider")
        self.assertFalse(status["provider_execution_enabled"])
        self.assertFalse(status["local_embedding_provider_enabled"])
        self.assertFalse(status["external_api_provider_enabled"])
        self.assertFalse(status["network_access_enabled"])
        self.assertFalse(status["credential_loading_enabled"])
        self.assertFalse(status["model_download_enabled"])
        self.assertFalse(status["model_load_enabled"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertFalse(status["automatic_provider_selection_enabled"])
        self.assertFalse(status["startup_provider_initialization_enabled"])
        self.assertFalse(status["runtime_provider_initialization_enabled"])
        self.assertFalse(status["background_provider_initialization_enabled"])
        self.assertTrue(status["advisory_only"])
        self.assertTrue(status["lexical_fallback_primary"])

    def test_minimal_valid_contract_is_valid_but_authorizes_nothing(self):
        contract = build_minimal_valid_provider_boundary_contract()
        result = validate_provider_boundary_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["provider_execution_authorized"])
        self.assertFalse(result["local_embedding_provider_authorized"])
        self.assertFalse(result["external_api_provider_authorized"])
        self.assertFalse(result["network_access_authorized"])
        self.assertFalse(result["credential_loading_authorized"])
        self.assertFalse(result["model_download_authorized"])
        self.assertFalse(result["model_load_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["prompt_router_mutation_authorized"])
        self.assertFalse(result["freeze_memory_write_authorized"])
        self.assertTrue(result["advisory_only"])

    def test_default_provider_must_remain_disabled_null_provider(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["default_provider"] = "local_embedding_provider"
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("disabled_null_provider" in error for error in result["errors"]))

    def test_all_provider_flags_must_be_false(self):
        for flag in [
            "provider_execution_enabled",
            "local_embedding_provider_enabled",
            "external_api_provider_enabled",
            "network_access_enabled",
            "credential_loading_enabled",
            "model_download_enabled",
            "model_load_enabled",
            "embedding_generation_enabled",
            "vector_index_generation_enabled",
            "semantic_runtime_enabled",
            "automatic_provider_selection_enabled",
            "startup_provider_initialization_enabled",
            "runtime_provider_initialization_enabled",
            "background_provider_initialization_enabled",
            "file_watcher_provider_initialization_enabled",
            "prompt_router_mutation_enabled",
        ]:
            contract = build_minimal_valid_provider_boundary_contract()
            contract["disabled_flags"][flag] = True
            result = validate_provider_boundary_contract(contract)
            self.assertFalse(result["ok"], flag)
            self.assertTrue(any("provider flags must be false" in error for error in result["errors"]), result["errors"])

    def test_missing_allowed_future_provider_classes_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["allowed_future_provider_classes"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("allowed future provider classes" in error for error in result["errors"]))

    def test_missing_forbidden_provider_classes_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["forbidden_provider_classes_now"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden provider classes now" in error for error in result["errors"]))

    def test_missing_future_adoption_gates_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["required_future_adoption_gates"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("future provider adoption gates" in error for error in result["errors"]))

    def test_missing_forbidden_actions_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["forbidden_actions"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden provider actions" in error for error in result["errors"]))

    def test_missing_permitted_outputs_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["permitted_outputs"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("permitted provider-boundary outputs" in error for error in result["errors"]))

    def test_missing_no_authority_assertions_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["no_authority_assertions"] = []
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("no-authority assertions" in error for error in result["errors"]))

    def test_authority_fields_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["final_route"] = "governed_patch"
        contract["required_prompts"] = ["anything"]
        contract["may_proceed_now"] = True
        contract["provider_override"] = "local_embedding_provider"
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden authority fields" in error for error in result["errors"]))

    def test_raw_text_fields_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["raw_user_query"] = "do not store raw query"
        contract["prompt_body_text"] = "do not store prompt body"
        contract["freeze_entry_text"] = "do not store freeze entry"
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden raw/private text fields" in error for error in result["errors"]))

    def test_vector_provider_runtime_fields_are_rejected(self):
        contract = build_minimal_valid_provider_boundary_contract()
        contract["embedding"] = [0.1, 0.2]
        contract["provider_name"] = "forbidden"
        contract["external_api_key"] = "forbidden"
        contract["model_path"] = "forbidden"
        result = validate_provider_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden vector/provider runtime fields" in error for error in result["errors"]))

    def test_activation_requests_never_authorize_provider_use(self):
        for action in [
            "enable local provider",
            "download model",
            "load model",
            "call external api",
            "generate embeddings",
            "create vector index",
            "enable semantic runtime",
            "select provider automatically",
        ]:
            result = classify_provider_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["model_load_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_index_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["external_api_authorized"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_provider_boundary_rules(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Provider Boundary Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "disabled_null_provider",
            "Required future adoption gates",
            "This design does not authorize provider execution.",
            "This design does not authorize semantic runtime enablement.",
            "This design does not authorize model loading.",
            "This design does not authorize external API use.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["provider_boundary_design_feature_id"],
            "routing_signal_scorer_v3_provider_boundary_design_v1",
        )
        self.assertEqual(
            manifest["provider_boundary_design_status"],
            "standard_library_only_provider_boundary_design_no_provider_no_ml_behavior_change",
        )
        self.assertEqual(
            manifest["provider_boundary_schema_version"],
            "3.7-provider-boundary-design",
        )
        self.assertEqual(
            manifest["provider_boundary_policy"],
            "disabled_null_provider_only_no_execution_no_model_load_no_download_no_external_api_no_runtime_enablement",
        )
        for characteristic in [
            "provider_boundary_design",
            "provider_boundary_design_disabled_only",
            "disabled_null_provider_only_default",
            "no_provider_implementation_added",
            "no_provider_execution_enabled",
            "no_model_download_enabled",
            "no_model_load_enabled",
            "no_external_api_provider_enabled",
            "no_network_access_enabled",
            "no_credential_loading_enabled",
            "no_automatic_provider_selection",
            "future_provider_requires_separate_governed_patch",
            "provider_outputs_review_evidence_only",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("validate_provider_boundary_contract", provides)
        self.assertNotIn("build_provider_boundary_status", provides)

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

    def test_forbidden_runtime_provider_artifacts_absent(self):
        for path in [
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "evaluation_runner.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "corpus_generator.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "provider.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]:
            self.assertFalse(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
