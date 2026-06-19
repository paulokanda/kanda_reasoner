import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.precomputed_semantic_evidence_artifact_design import (
    PRECOMPUTED_ARTIFACT_FEATURE_ID,
    build_minimal_valid_precomputed_artifact_contract,
    build_precomputed_artifact_design_status,
    classify_precomputed_artifact_activation_request,
    validate_precomputed_artifact_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "precomputed_semantic_evidence_artifact_design.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class PrecomputedSemanticEvidenceArtifactDesignTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            PRECOMPUTED_ARTIFACT_FEATURE_ID,
            "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1",
        )
        status = build_precomputed_artifact_design_status()
        self.assertFalse(status["artifact_generation_enabled"])
        self.assertFalse(status["precomputed_artifact_written"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["embedding_values_allowed"])
        self.assertFalse(status["vector_values_allowed"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["provider_execution_enabled"])
        self.assertFalse(status["evaluation_runner_enabled"])
        self.assertFalse(status["threshold_auto_tuning_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertTrue(status["advisory_only"])
        self.assertTrue(status["review_evidence_only"])
        self.assertTrue(status["lexical_fallback_primary"])

    def test_minimal_valid_contract_is_valid_but_authorizes_nothing(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        result = validate_precomputed_artifact_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_values_authorized"])
        self.assertFalse(result["vector_index_authorized"])
        self.assertFalse(result["provider_execution_authorized"])
        self.assertFalse(result["evaluation_execution_authorized"])
        self.assertFalse(result["threshold_tuning_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["prompt_router_mutation_authorized"])
        self.assertFalse(result["freeze_memory_write_authorized"])
        self.assertTrue(result["advisory_only"])
        self.assertTrue(result["review_evidence_only"])
        self.assertTrue(result["requires_future_governed_patch"])

    def test_missing_source_manifest_requirements_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["source_manifest_requirements"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("source manifest requirements" in error for error in result["errors"]))

    def test_missing_source_gold_set_requirements_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["source_gold_set_requirements"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("source gold-set requirements" in error for error in result["errors"]))

    def test_missing_required_artifact_sections_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["required_artifact_sections"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required artifact sections" in error for error in result["errors"]))

    def test_missing_forbidden_artifact_sections_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["forbidden_artifact_sections"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden artifact sections" in error for error in result["errors"]))

    def test_missing_validation_gates_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["required_validation_gates"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("artifact validation gates" in error for error in result["errors"]))

    def test_all_artifact_flags_must_be_false(self):
        for flag in [
            "artifact_generation_enabled",
            "precomputed_artifact_written",
            "embedding_generation_enabled",
            "embedding_values_allowed",
            "vector_values_allowed",
            "vector_index_generation_enabled",
            "provider_execution_enabled",
            "model_load_enabled",
            "external_api_enabled",
            "network_access_enabled",
            "evaluation_runner_enabled",
            "threshold_auto_tuning_enabled",
            "semantic_runtime_enabled",
            "startup_artifact_loading_enabled",
            "runtime_artifact_loading_enabled",
            "background_artifact_rebuild_enabled",
            "file_watcher_artifact_rebuild_enabled",
            "prompt_router_mutation_enabled",
            "write_freeze_memory_enabled",
        ]:
            contract = build_minimal_valid_precomputed_artifact_contract()
            contract["disabled_flags"][flag] = True
            result = validate_precomputed_artifact_contract(contract)
            self.assertFalse(result["ok"], flag)
            self.assertTrue(any("artifact flags must be false" in error for error in result["errors"]), result["errors"])

    def test_missing_forbidden_actions_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["forbidden_actions"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden precomputed artifact actions" in error for error in result["errors"]))

    def test_missing_permitted_outputs_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["permitted_outputs"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("permitted precomputed artifact outputs" in error for error in result["errors"]))

    def test_missing_no_authority_assertions_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["no_authority_assertions"] = []
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("no-authority assertions" in error for error in result["errors"]))

    def test_authority_fields_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["final_route"] = "governed_patch"
        contract["required_prompts"] = ["anything"]
        contract["may_proceed_now"] = True
        contract["threshold_override"] = 0.1
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden authority fields" in error for error in result["errors"]))

    def test_raw_text_fields_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["raw_user_query_text"] = "do not store raw query"
        contract["prompt_body_text"] = "do not store prompt body"
        contract["freeze_entry_text"] = "do not store freeze entry"
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden raw/private text fields" in error for error in result["errors"]))

    def test_vector_provider_runtime_fields_are_rejected(self):
        contract = build_minimal_valid_precomputed_artifact_contract()
        contract["embedding_values"] = [0.1, 0.2]
        contract["vector_values"] = [0.3, 0.4]
        contract["artifact_path"] = "forbidden"
        contract["provider_name"] = "forbidden"
        result = validate_precomputed_artifact_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden vector/provider/runtime fields" in error for error in result["errors"]))

    def test_activation_requests_never_authorize_artifact_use(self):
        for action in [
            "generate artifact",
            "write artifact",
            "precompute",
            "generate embeddings",
            "store vectors",
            "create vector index",
            "load provider",
            "run evaluation",
            "enable semantic runtime",
            "load artifact at startup",
        ]:
            result = classify_precomputed_artifact_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_generation_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_values_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["evaluation_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_precomputed_artifact_rules(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Precomputed Semantic Evidence Artifact Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "This design does not authorize artifact generation.",
            "This design does not authorize storing embedding values.",
            "This design does not authorize storing vector values.",
            "The precomputed artifact can only produce review evidence.",
            "It may never enable semantic runtime behavior.",
            "This phase adds no external dependency.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["precomputed_semantic_evidence_artifact_design_feature_id"],
            "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1",
        )
        self.assertEqual(
            manifest["precomputed_semantic_evidence_artifact_design_status"],
            "standard_library_only_artifact_design_no_generator_no_ml_behavior_change",
        )
        self.assertEqual(
            manifest["precomputed_semantic_evidence_artifact_schema_version"],
            "3.8-precomputed-semantic-evidence-artifact-design",
        )
        self.assertEqual(
            manifest["precomputed_semantic_evidence_artifact_policy"],
            "schema_only_no_generation_no_embeddings_no_vectors_no_index_no_runtime_loading_review_evidence_only",
        )
        for characteristic in [
            "precomputed_semantic_evidence_artifact_design",
            "precomputed_artifact_design_schema_only",
            "no_precomputed_artifact_generator_added",
            "no_precomputed_artifact_generated",
            "no_embedding_values_in_artifact",
            "no_vector_values_in_artifact",
            "no_vector_index_in_artifact",
            "precomputed_artifact_identifiers_only",
            "precomputed_artifact_no_raw_text",
            "precomputed_artifact_review_evidence_only",
            "precomputed_artifact_no_runtime_enablement",
            "precomputed_artifact_no_threshold_auto_tuning",
            "precomputed_artifact_requires_frozen_manifest_and_gold_set",
            "precomputed_artifact_requires_separate_governed_generation_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("validate_precomputed_artifact_contract", provides)
        self.assertNotIn("build_precomputed_artifact_design_status", provides)

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
        self.assertTrue(forbidden_roots.isdisjoint(imported_roots))
        for forbidden in [
            "kanda_prompt_workspace",
            "project_freeze_ledger",
            "project_freeze_after_update",
            "kanda_reasoner_app.freeze_hint_intake",
            "kanda_reasoner_app.freeze_after_update",
            "kanda_reasoner_app.freeze_after_update_gui",
        ]:
            self.assertNotIn(forbidden, imported_modules)

    def test_forbidden_runtime_artifacts_were_not_created(self):
        forbidden_paths = [
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "precomputed_artifact_generator.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "evaluation_runner.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "corpus_generator.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), str(path))

    def test_prior_provider_boundary_regression_still_registered(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["provider_boundary_design_feature_id"],
            "routing_signal_scorer_v3_provider_boundary_design_v1",
        )
        self.assertIn("disabled_null_provider_only_default", manifest["protected_architecture_characteristics"])
        self.assertIn("no_provider_implementation_added", manifest["protected_architecture_characteristics"])


if __name__ == "__main__":
    unittest.main()
