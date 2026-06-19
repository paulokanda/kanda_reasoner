from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
DESIGN = BOX / "design"
FEATURE_ID = "routing_signal_scorer_v3_closure_shield_v1"
FEATURE_TITLE = "Routing Signal Scorer v3 Closure Shield v1"

V3_CHAIN = [
    {
        "feature_id": "routing_signal_scorer_v3_semantic_readiness_canon_registration_v1",
        "test": "tests/test_routing_signal_scorer_v3_semantic_readiness_canon_registration.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/semantic_evidence_contract.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md",
        "test": "tests/test_routing_signal_scorer_v3_structural_contract_semantic_readiness_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_mock_semantic_evidence_contract_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/semantic_evidence_contract.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_mock_semantic_evidence_contract.md",
        "test": "tests/test_routing_signal_scorer_v3_mock_semantic_evidence_contract.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_metadata_vector_manifest_schema_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/metadata_vector_manifest_schema.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_metadata_vector_manifest_schema.md",
        "test": "tests/test_routing_signal_scorer_v3_metadata_vector_manifest_schema.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_offline_corpus_governance_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/offline_corpus_governance.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_corpus_governance_design.md",
        "test": "tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_offline_evaluation_corpus_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/offline_evaluation_corpus_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_corpus_design.md",
        "test": "tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_gold_set_schema.md",
        "test": "tests/test_routing_signal_scorer_v3_offline_evaluation_gold_set_schema.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_disabled_evaluation_runner_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/disabled_evaluation_runner_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_disabled_evaluation_runner_design.md",
        "test": "tests/test_routing_signal_scorer_v3_disabled_evaluation_runner_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_provider_boundary_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/provider_boundary_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_provider_boundary_design.md",
        "test": "tests/test_routing_signal_scorer_v3_provider_boundary_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design.md",
        "test": "tests/test_routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_disabled_artifact_reader_boundary_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/disabled_artifact_reader_boundary_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_disabled_artifact_reader_boundary_design.md",
        "test": "tests/test_routing_signal_scorer_v3_disabled_artifact_reader_boundary_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/advisory_precomputed_artifact_ui_preview_design.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design.md",
        "test": "tests/test_routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design.py",
    },
    {
        "feature_id": "routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1",
        "module": "kanda_reasoner_app/routing_signal_scorer/schema_only_precomputed_artifact_example.py",
        "design": "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.md",
        "test": "tests/test_routing_signal_scorer_v3_schema_only_precomputed_artifact_example.py",
        "fixture": "kanda_reasoner_app/routing_signal_scorer/design/examples/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json",
    },
]

FORBIDDEN_DEPENDENCY_ROOTS = {
    "chromadb",
    "faiss",
    "langchain",
    "llama_index",
    "numpy",
    "onnx",
    "openai",
    "pandas",
    "qdrant_client",
    "requests",
    "scipy",
    "sentence_transformers",
    "sklearn",
    "tensorflow",
    "torch",
    "transformers",
}

FORBIDDEN_RUNTIME_PATHS = [
    "kanda_reasoner_app/routing_signal_scorer/artifact_reader.py",
    "kanda_reasoner_app/routing_signal_scorer/artifact_ui_preview.py",
    "kanda_reasoner_app/routing_signal_scorer/artifact_loader.py",
    "kanda_reasoner_app/routing_signal_scorer/background_artifact_loader.py",
    "kanda_reasoner_app/routing_signal_scorer/evaluation_runner.py",
    "kanda_reasoner_app/routing_signal_scorer/precomputed_artifact_generator.py",
    "kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_generator.py",
    "kanda_reasoner_app/routing_signal_scorer/provider.py",
    "kanda_reasoner_app/routing_signal_scorer/providers",
    "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
    "kanda_reasoner_app/routing_signal_scorer/vector_store.py",
    "kanda_reasoner_app/routing_signal_scorer/indices",
]

FORBIDDEN_TEXT_MARKERS = [
    "sentence_transformers",
    "faiss",
    "qdrant_client",
    "chromadb",
    "torch",
    "openai.api_key",
    "api_key",
    "credential",
    "model_download",
    "artifact_auto_discovery_enabled",
    "runtime_semantic_enablement",
]


class RoutingSignalScorerV3ClosureShieldTests(unittest.TestCase):
    def test_closure_shield_document_exists_and_states_design_only_boundary(self) -> None:
        path = DESIGN / "routing_signal_scorer_v3_closure_shield.md"
        self.assertTrue(path.exists(), path)
        text = path.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Closure Shield v1",
            "does not implement semantic runtime behavior",
            "Semantic evidence remains an untrusted evidence witness",
            "Future real semantic enablement requires a separately governed",
            "real embeddings",
            "No artifact reader",
            "No provider implementation",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_records_closure_without_public_runtime_export(self) -> None:
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["v3_closure_shield_feature_id"], FEATURE_ID)
        self.assertEqual(
            manifest["v3_closure_shield_status"],
            "tests_only_closure_shield_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["v3_closure_shield_doc"],
            "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_closure_shield.md",
        )
        self.assertEqual(
            manifest["v3_closure_shield_test"],
            "tests/test_routing_signal_scorer_v3_closure_shield.py",
        )
        self.assertIn("v3_closure_no_embeddings", manifest["protected_architecture_characteristics"])
        self.assertIn("v3_closure_no_providers", manifest["protected_architecture_characteristics"])
        self.assertIn("v3_closure_no_generators", manifest["protected_architecture_characteristics"])
        self.assertIn("v3_closure_no_readers", manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("build_v3_closure_shield", provides)
        self.assertNotIn("run_semantic_evaluation", provides)
        self.assertNotIn("load_precomputed_artifact", provides)

    def test_every_frozen_v3_milestone_still_has_expected_files(self) -> None:
        for item in V3_CHAIN:
            for key in ["module", "design", "test", "fixture"]:
                if key in item:
                    path = ROOT / item[key]
                    self.assertTrue(path.exists(), f"Missing {key} for {item['feature_id']}: {path}")

    def test_v3_modules_remain_standard_library_only(self) -> None:
        module_paths = sorted(
            {
                ROOT / item["module"]
                for item in V3_CHAIN
                if "module" in item
            }
        )
        self.assertGreaterEqual(len(module_paths), 10)
        for path in module_paths:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported_roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_roots.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_roots.add(node.module.split(".")[0])
            self.assertTrue(
                FORBIDDEN_DEPENDENCY_ROOTS.isdisjoint(imported_roots),
                f"Forbidden import in {path}: {sorted(FORBIDDEN_DEPENDENCY_ROOTS.intersection(imported_roots))}",
            )

    def test_forbidden_runtime_semantic_files_are_still_absent(self) -> None:
        for relative in FORBIDDEN_RUNTIME_PATHS:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_schema_only_fixture_has_no_raw_text_vectors_or_authority_fields(self) -> None:
        fixture = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "examples" / "routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertTrue(data["declared_schema_only"])
        self.assertEqual(data["example_status"], "schema_only_static_fixture")
        for assertion in [
            "contains_no_raw_user_query_text",
            "contains_no_prompt_body_text",
            "contains_no_embedding_values",
            "contains_no_vector_values",
            "contains_no_provider_config",
            "contains_no_authority_fields",
        ]:
            self.assertIn(assertion, data["forbidden_content_assertions"])
        for assertion in [
            "canon_remains_final_authority",
            "example_must_not_choose_route",
            "example_must_not_decide_may_proceed",
            "example_must_not_load_prompts",
        ]:
            self.assertIn(assertion, data["no_authority_assertions"])
        disabled = data["disabled_flags"]
        for flag in [
            "artifact_generation_enabled",
            "artifact_reader_enabled",
            "artifact_loading_enabled",
            "startup_loading_enabled",
            "runtime_loading_enabled",
            "provider_execution_enabled",
            "threshold_auto_tuning_enabled",
            "prompt_router_mutation_enabled",
            "write_freeze_memory_enabled",
        ]:
            self.assertIs(disabled[flag], False, flag)
        for record in data["candidate_records"]:
            self.assertEqual(record["privacy_status"], "redacted_metadata_only")
            self.assertEqual(record["authority_status"], "no_authority_fields_present")
            self.assertIn("metadata", record["redacted_label"].lower())

    def test_contract_and_init_do_not_export_v3_semantic_runtime(self) -> None:
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        forbidden = [
            "semantic_evidence_contract",
            "metadata_vector_manifest_schema",
            "offline_corpus_governance",
            "offline_evaluation_gold_set_schema",
            "provider_boundary_design",
            "precomputed_semantic_evidence_artifact_design",
            "disabled_artifact_reader_boundary_design",
            "schema_only_precomputed_artifact_example",
            "load_precomputed_artifact",
            "generate_precomputed_artifact",
            "run_semantic_evaluation",
            "execute_provider",
        ]
        for marker in forbidden:
            self.assertNotIn(marker, contract_text)
            self.assertNotIn(marker, init_text)

    def test_v3_design_files_preserve_disabled_and_review_only_language(self) -> None:
        design_paths = [ROOT / item["design"] for item in V3_CHAIN if "design" in item]
        self.assertGreaterEqual(len(design_paths), 12)
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in design_paths)
        for phrase in [
            "advisory",
            "disabled",
            "review",
            "no runtime",
            "no embeddings",
            "no vector",
            "no provider",
            "no authority",
        ]:
            self.assertIn(phrase, combined)

    def test_box_manifest_preserves_v3_non_goals(self) -> None:
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        blob = json.dumps(manifest, sort_keys=True).lower()
        for phrase in [
            "no_provider_execution_enabled",
            "no_model_download_enabled",
            "no_network_access_enabled",
            "no_precomputed_artifact_generator_added",
            "no_artifact_reader_implementation_added",
            "no_artifact_reader_enabled",
            "no_artifact_ui_preview_implementation_added",
            "schema_only_artifact_example_no_embedding_values",
            "schema_only_artifact_example_no_vector_values",
            "v3_closure_requires_separate_governed_patch_for_real_semantic_enablement",
        ]:
            self.assertIn(phrase, blob)

    def test_new_closure_artifacts_are_ascii_and_do_not_create_runtime_code(self) -> None:
        for path in [
            DESIGN / "routing_signal_scorer_v3_closure_shield.md",
            ROOT / "tests" / "test_routing_signal_scorer_v3_closure_shield.py",
        ]:
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
        self.assertFalse((BOX / "routing_signal_scorer_v3_closure_shield.py").exists())

    def test_patch_does_not_create_root_freeze_hint_in_project(self) -> None:
        self.assertFalse((ROOT / "KANDA_FREEZE_HINT.json").exists())


if __name__ == "__main__":
    unittest.main()
