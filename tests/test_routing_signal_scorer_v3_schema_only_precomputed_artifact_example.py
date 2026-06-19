"""Regression tests for schema-only precomputed artifact example."""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.schema_only_precomputed_artifact_example import (
    FORBIDDEN_FIELD_NAMES,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_EXAMPLE_FIELDS,
    SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID,
    SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION,
    build_disabled_schema_example_status,
    build_minimal_schema_only_precomputed_artifact_example,
    validate_schema_only_precomputed_artifact_example,
)


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "schema_only_precomputed_artifact_example.py"
DOC_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_schema_only_precomputed_artifact_example.md"
FIXTURE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "examples" / "routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json"
MANIFEST_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class SchemaOnlyPrecomputedArtifactExampleTests(unittest.TestCase):
    def test_feature_identity_constants_are_frozen(self) -> None:
        self.assertEqual(
            SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_FEATURE_ID,
            "routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1",
        )
        self.assertEqual(
            SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_SCHEMA_VERSION,
            "3.11-schema-only-precomputed-artifact-example",
        )

    def test_minimal_example_has_required_top_level_fields(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        self.assertTrue(REQUIRED_EXAMPLE_FIELDS.issubset(example))
        self.assertTrue(example["declared_schema_only"])

    def test_minimal_example_validates(self) -> None:
        notes = validate_schema_only_precomputed_artifact_example(
            build_minimal_schema_only_precomputed_artifact_example()
        )
        self.assertIn("schema-only static fixture accepted for human review training only", notes)

    def test_static_json_fixture_exists_and_validates(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            fixture["artifact_example_id"],
            "routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1",
        )
        self.assertIn("candidate_records", fixture)
        validate_schema_only_precomputed_artifact_example(fixture)

    def test_static_json_fixture_contains_no_forbidden_field_names(self) -> None:
        text = FIXTURE_PATH.read_text(encoding="utf-8")
        for forbidden in sorted(FORBIDDEN_FIELD_NAMES):
            self.assertNotIn(f'"{forbidden}"', text)

    def test_static_json_fixture_is_redacted_metadata_only(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        for candidate in fixture["candidate_records"]:
            self.assertEqual(candidate["privacy_status"], "redacted_metadata_only")
            self.assertEqual(candidate["authority_status"], "no_authority_fields_present")

    def test_rejects_forbidden_raw_text_field(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        example["raw_user_query"] = "not allowed"
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_rejects_forbidden_vector_field(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        example["candidate_records"][0]["vector_values"] = [0.1, 0.2]
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_rejects_authority_field(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        example["final_route"] = "not allowed"
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_rejects_runtime_eligible_identity(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        example["artifact_identity"]["runtime_eligible"] = True
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_rejects_non_review_evidence_identity(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        example["artifact_identity"]["review_evidence_only"] = False
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_rejects_enabled_disabled_flag(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        flag = sorted(REQUIRED_DISABLED_FLAGS_FALSE)[0]
        example["disabled_flags"][flag] = True
        with self.assertRaises(ValueError):
            validate_schema_only_precomputed_artifact_example(example)

    def test_disabled_status_has_no_runtime_enablement(self) -> None:
        status = build_disabled_schema_example_status()
        self.assertFalse(status["artifact_example_generation_enabled"])
        self.assertFalse(status["artifact_example_runtime_enabled"])
        self.assertFalse(status["artifact_reader_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertTrue(status["review_evidence_only"])

    def test_doc_freezes_no_authority_and_no_runtime_language(self) -> None:
        doc = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Schema-Only Precomputed Artifact Example v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "The example may never be treated as a generated artifact.",
            "The example may never be loaded at startup or runtime.",
            "The example may never enable semantic runtime behavior.",
            "This phase does not authorize artifact generation.",
            "This phase does not authorize artifact reading.",
            "This phase adds no external dependency.",
        ]:
            self.assertIn(phrase, doc)

    def test_manifest_registration_is_schema_only(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["schema_only_precomputed_artifact_example_feature_id"],
            "routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1",
        )
        self.assertEqual(
            manifest["schema_only_precomputed_artifact_example_policy"],
            "static_redacted_fixture_only_no_generation_no_reader_no_loading_no_vectors_no_runtime_enablement",
        )

    def test_manifest_protected_characteristics_registered(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        characteristics = set(manifest["protected_architecture_characteristics"])
        for item in [
            "schema_only_precomputed_artifact_example",
            "schema_only_artifact_example_static_fixture_only",
            "schema_only_artifact_example_no_generation",
            "schema_only_artifact_example_no_reader",
            "schema_only_artifact_example_no_loading",
            "schema_only_artifact_example_no_raw_text",
            "schema_only_artifact_example_no_embedding_values",
            "schema_only_artifact_example_no_vector_values",
            "schema_only_artifact_example_no_vector_index",
            "schema_only_artifact_example_no_provider_config",
            "schema_only_artifact_example_no_authority_fields",
            "schema_only_artifact_example_review_evidence_only",
            "schema_only_artifact_example_no_runtime_enablement",
            "schema_only_artifact_example_no_threshold_tuning",
            "schema_only_artifact_example_requires_separate_governed_generation_patch",
        ]:
            self.assertIn(item, characteristics)

    def test_no_forbidden_ml_vector_dependencies_imported(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertTrue(
            {
                "numpy",
                "pandas",
                "sklearn",
                "scipy",
                "torch",
                "tensorflow",
                "sentence_transformers",
                "transformers",
                "faiss",
                "chromadb",
                "qdrant_client",
                "langchain",
                "llama_index",
            }.isdisjoint(imported_roots)
        )

    def test_forbidden_runtime_files_not_created(self) -> None:
        for relative in [
            "kanda_reasoner_app/routing_signal_scorer/artifact_reader.py",
            "kanda_reasoner_app/routing_signal_scorer/artifact_ui_preview.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/evaluation_runner.py",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
            "kanda_reasoner_app/routing_signal_scorer/providers",
            "kanda_reasoner_app/routing_signal_scorer/indices",
        ]:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_contract_and_init_are_not_exporting_schema_example(self) -> None:
        contract_text = (ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py").read_text(encoding="utf-8")
        init_text = (ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py").read_text(encoding="utf-8")
        self.assertNotIn("schema_only_precomputed_artifact_example", contract_text)
        self.assertNotIn("schema_only_precomputed_artifact_example", init_text)

    def test_no_authority_assertions_remain_required(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        self.assertIn("canon_remains_final_authority", example["no_authority_assertions"])
        self.assertIn("example_must_not_choose_route", example["no_authority_assertions"])
        self.assertIn("example_must_not_decide_may_proceed", example["no_authority_assertions"])

    def test_permitted_uses_are_review_only(self) -> None:
        example = build_minimal_schema_only_precomputed_artifact_example()
        self.assertIn("review_evidence_only", example["permitted_uses"])
        self.assertIn("no_runtime_enablement", example["permitted_uses"])
        self.assertIn("no_final_route_signal", example["permitted_uses"])
        self.assertIn("no_may_proceed_signal", example["permitted_uses"])


if __name__ == "__main__":
    unittest.main()
