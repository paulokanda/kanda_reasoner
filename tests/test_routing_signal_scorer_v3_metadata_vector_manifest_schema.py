from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.metadata_vector_manifest_schema import (
    AUTHORITY,
    FEATURE_ID,
    SCHEMA_VERSION,
    build_empty_metadata_vector_manifest,
    metadata_manifest_item_eligibility_reasons,
    render_metadata_vector_manifest_validation_text,
    validate_metadata_vector_manifest,
    validate_metadata_vector_manifest_item,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "metadata_vector_manifest_schema.py"
DOC_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_metadata_vector_manifest_schema.md"
MANIFEST_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

FORBIDDEN_IMPORT_ROOTS = {
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
}

FORBIDDEN_NEIGHBOR_IMPORTS = {
    "kanda_prompt_workspace",
    "project_freeze_ledger",
    "project_freeze_after_update",
    "kanda_reasoner_app.freeze_hint_intake",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.freeze_after_update_gui",
}


def valid_item(item_id: str = "patch_workflow") -> dict[str, object]:
    return {
        "id": item_id,
        "label": "Patch Workflow",
        "route_family": "governed_patch",
        "isolation_domain": "routing_signal_scorer",
        "lifecycle_status": "active",
        "source_path": "prompt_library/ACTIVE_PROMPTS/example.md",
        "source_version": "freeze-20260617-example",
        "source_structural_hash": "sha256:sourcehash",
        "corpus_generation_run_id": "run-20260617-example",
        "embedding_model_id": "schema_only_no_model",
        "embedding_model_version": "schema-only",
        "embedding_dimensions": 0,
        "corpus_hash": "sha256:corpushash",
        "last_validated": "2026-06-17T00:00:00Z",
        "allowed_use": ["advisory_routing_hint"],
        "forbidden_use": [
            "final_route_decision",
            "required_prompt_decision",
            "may_proceed_now_decision",
            "prompt_auto_loading",
            "freeze_write",
        ],
        "semantic_summary": "Curated semantic routing evidence for governed patch workflow.",
        "canonical_terms": ["create patch", "install block", "validation command"],
        "keywords": ["patch", "zip", "validation"],
        "negative_examples": ["explain concept", "summarize text"],
        "min_score_threshold": 0.72,
    }


def valid_manifest() -> dict[str, object]:
    manifest = build_empty_metadata_vector_manifest(
        manifest_id="routing-corpus-schema-test",
        manifest_version="0.1.0-schema-only",
        generated_at="2026-06-17T00:00:00Z",
    )
    manifest["corpus_hash"] = "sha256:corpushash"
    manifest["items"] = [valid_item()]
    return manifest


class MetadataVectorManifestSchemaTests(unittest.TestCase):
    def test_empty_manifest_is_schema_only_and_advisory(self) -> None:
        manifest = build_empty_metadata_vector_manifest()
        validation = validate_metadata_vector_manifest(manifest)

        self.assertTrue(validation.is_valid, validation.errors)
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["authority"], AUTHORITY)
        self.assertFalse(manifest["contains_embeddings"])
        self.assertFalse(manifest["contains_vectors"])
        self.assertFalse(manifest["contains_raw_prompt_text"])
        self.assertFalse(manifest["contains_user_queries"])
        self.assertFalse(manifest["contains_freeze_entries"])
        self.assertFalse(manifest["runtime_rebuild_allowed"])
        self.assertFalse(manifest["startup_rebuild_allowed"])
        self.assertFalse(manifest["external_api_allowed"])

    def test_valid_manifest_item_is_eligible_for_future_semantic_evidence(self) -> None:
        item = valid_item()
        item_validation = validate_metadata_vector_manifest_item(item)
        eligible, reasons = metadata_manifest_item_eligibility_reasons(item)

        self.assertTrue(item_validation.is_valid, item_validation.errors)
        self.assertTrue(eligible, reasons)
        self.assertEqual(reasons, ())

    def test_valid_manifest_with_one_item_passes(self) -> None:
        validation = validate_metadata_vector_manifest(valid_manifest())
        self.assertTrue(validation.is_valid, validation.errors)
        self.assertEqual(validation.errors, ())

    def test_forbidden_authority_fields_are_rejected(self) -> None:
        item = valid_item()
        item["final_route"] = "load_patch_route"  # type: ignore[index]
        item["may_proceed_now"] = True  # type: ignore[index]
        manifest = valid_manifest()
        manifest["items"] = [item]

        validation = validate_metadata_vector_manifest(manifest)

        self.assertFalse(validation.is_valid)
        self.assertIn("forbidden fields", " ".join(validation.errors))

    def test_raw_prompt_user_query_and_freeze_text_fields_are_rejected(self) -> None:
        for field in ["raw_prompt_text", "user_query_text", "freeze_entry_text", "terminal_log_text"]:
            item = valid_item(field)
            item[field] = "unsafe raw content"  # type: ignore[index]
            validation = validate_metadata_vector_manifest_item(item)
            self.assertFalse(validation.is_valid, field)
            self.assertIn(field, " ".join(validation.errors))

    def test_vector_and_index_fields_are_rejected(self) -> None:
        for field in ["embedding", "vector", "dense_vector", "vector_index_path", "faiss_index_path"]:
            item = valid_item(field)
            item[field] = [0.1, 0.2]  # type: ignore[index]
            validation = validate_metadata_vector_manifest_item(item)
            self.assertFalse(validation.is_valid, field)
            self.assertIn(field, " ".join(validation.errors))

    def test_non_active_items_are_valid_but_not_eligible(self) -> None:
        item = valid_item()
        item["lifecycle_status"] = "deprecated"
        validation = validate_metadata_vector_manifest_item(item)
        eligible, reasons = metadata_manifest_item_eligibility_reasons(item)

        self.assertTrue(validation.is_valid, validation.errors)
        self.assertIn("non-active lifecycle_status", " ".join(validation.warnings))
        self.assertFalse(eligible)
        self.assertIn("lifecycle_status is not active", reasons)

    def test_duplicate_ids_are_rejected_at_manifest_level(self) -> None:
        manifest = valid_manifest()
        manifest["items"] = [valid_item("same"), valid_item("same")]
        validation = validate_metadata_vector_manifest(manifest)

        self.assertFalse(validation.is_valid)
        self.assertIn("duplicate id same", " ".join(validation.errors))

    def test_external_api_and_runtime_rebuild_are_rejected(self) -> None:
        manifest = valid_manifest()
        manifest["external_api_allowed"] = True
        manifest["startup_rebuild_allowed"] = True
        item = valid_item()
        item["embedding_model_id"] = "external_api_openai"
        manifest["items"] = [item]

        validation = validate_metadata_vector_manifest(manifest)

        self.assertFalse(validation.is_valid)
        combined = " ".join(validation.errors)
        self.assertIn("external_api_allowed must be False", combined)
        self.assertIn("startup_rebuild_allowed must be False", combined)
        self.assertIn("external API embedding model ids are forbidden", combined)

    def test_validation_rendering_is_advisory_and_not_imperative(self) -> None:
        text = render_metadata_vector_manifest_validation_text(validate_metadata_vector_manifest(valid_manifest())).lower()
        self.assertIn("authority=advisory_schema_only", text)
        self.assertIn("manifest evidence is not routing authority", text)
        for phrase in [
            "final route is",
            "required prompts:",
            "may proceed: yes",
            "load prompt now",
            "confirm and write",
        ]:
            self.assertNotIn(phrase, text)

    def test_module_uses_standard_library_only_and_no_neighbor_imports(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        root_imports = set()
        full_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    full_imports.add(alias.name)
                    root_imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                full_imports.add(node.module)
                root_imports.add(node.module.split(".")[0])
        self.assertTrue(FORBIDDEN_IMPORT_ROOTS.isdisjoint(root_imports))
        for forbidden in FORBIDDEN_NEIGHBOR_IMPORTS:
            self.assertNotIn(forbidden, full_imports)

    def test_design_doc_records_schema_boundaries(self) -> None:
        self.assertTrue(DOC_PATH.exists())
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Metadata Vector Manifest Schema v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "Metadata Vector Manifest is the only future embeddable source",
            "Forbidden raw content fields",
            "Only `active` manifest items may be eligible",
            "A high vector or mock score cannot rescue an ineligible manifest item.",
            "This schema phase must not store actual vectors.",
            "No automatic rebuild",
            "External building block adoption boundary",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_schema_without_enabling_runtime_ml(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["metadata_vector_manifest_schema_feature_id"], FEATURE_ID)
        self.assertEqual(
            manifest["metadata_vector_manifest_schema_status"],
            "standard_library_only_schema_contract_no_embeddings_no_vectors_no_runtime_behavior_change",
        )
        self.assertEqual(manifest["metadata_vector_manifest_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["metadata_vector_manifest_policy"],
            "curated_manifest_only_no_raw_prompt_freeze_user_query_or_vector_fields",
        )
        self.assertEqual(manifest["future_ml_default_provider"], "disabled_null_provider")
        self.assertEqual(manifest["contract_version"], "1.8")
        for characteristic in [
            "metadata_vector_manifest_schema",
            "manifest_schema_no_vectors",
            "manifest_schema_no_raw_prompt_text",
            "manifest_schema_no_user_queries",
            "manifest_schema_no_freeze_entries",
            "manifest_schema_no_runtime_rebuild",
            "manifest_schema_no_startup_rebuild",
            "manifest_items_active_only_for_eligibility",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])


if __name__ == "__main__":
    unittest.main()
