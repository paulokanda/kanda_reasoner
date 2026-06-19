from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md"
)
MANIFEST_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1"


class RoutingSignalScorerV3StructuralContractSemanticReadinessDesignTests(unittest.TestCase):
    def test_design_document_exists_and_declares_design_only_scope(self) -> None:
        self.assertTrue(DOC_PATH.exists())
        text = DOC_PATH.read_text(encoding="utf-8")
        self.assertIn("Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design", text)
        self.assertIn(FEATURE_ID, text)
        self.assertIn("Status: design-only architecture contract. No runtime behavior change.", text)
        self.assertIn("This phase changes documentation and manifest registration only.", text)
        self.assertIn("This design does not authorize implementation.", text)

    def test_design_preserves_semantic_evidence_not_authority_law(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "The semantic layer is an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "It may never output authority fields.",
            "It may never bypass lexical fallback.",
            "It may never override the routing canon.",
            "Disagreement cannot increase authority.",
            "Disagreement can only increase caution.",
        ]:
            self.assertIn(phrase, text)

    def test_design_forbids_runtime_ml_and_dependency_installation_in_this_phase(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "This phase does not add:",
            "sentence-transformers",
            "FAISS",
            "Qdrant",
            "Chroma",
            "provider implementation",
            "runtime evidence aggregator",
            "semantic scoring runtime logic",
            "dependency installation in design phase",
        ]:
            self.assertIn(phrase, text)

    def test_design_defines_metadata_vector_manifest_and_corpus_lifecycle(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Metadata Vector Manifest",
            "Future embeddings must not be generated from raw prompt files.",
            "source_structural_hash",
            "corpus_generation_run_id",
            "embedding_model_id",
            "embedding_model_version",
            "corpus_hash",
            "proposed -> validated -> active -> deprecated -> superseded -> archived",
            "Only `active` items may be surfaced",
        ]:
            self.assertIn(phrase, text)

    def test_design_requires_metadata_eligibility_before_semantic_scoring(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Metadata filtering must happen before semantic scoring",
            "metadata eligibility gate",
            "A high vector score cannot rescue an ineligible candidate.",
            "lifecycle_status == active",
            "allowed_use` contains `advisory_routing_hint",
        ]:
            self.assertIn(phrase, text)

    def test_design_declares_vector_index_disposable_and_no_startup_rebuild(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "The vector index is disposable generated evidence.",
            "It is not canonical memory.",
            "It is not freeze memory.",
            "No automatic rebuild at startup",
            "mark semantic provider unavailable",
            "fall back to lexical scorer",
            "require explicit human-governed rebuild",
        ]:
            self.assertIn(phrase, text)

    def test_design_defines_provider_boundary_and_forbidden_output_fields(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "disabled_null_provider",
            "offline_precomputed_provider",
            "external_api_provider",
            "forbidden in v3",
            "final_route",
            "required_prompts",
            "may_proceed_now",
            "route_override",
            "auto_load_prompts",
        ]:
            self.assertIn(phrase, text)

    def test_design_defines_evaluation_metrics_and_threat_model(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Precision@1",
            "Recall@3",
            "MRR",
            "NDCG@10",
            "stale candidate suppression rate",
            "authority leakage rate",
            "Threat model",
            "authority creep",
            "index poisoning",
            "user-query persistence",
        ]:
            self.assertIn(phrase, text)

    def test_design_defines_external_building_block_adoption_policy(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "External building block adoption policy",
            "KANDA should not reinvent the wheel",
            "sentence-transformers",
            "all-MiniLM-L6-v2",
            "license review",
            "Windows/PyCharm install review",
            "No external ML or vector dependency may become core runtime behavior",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_semantic_readiness_design_without_contract_change(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["semantic_readiness_architecture_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["semantic_readiness_architecture_status"], "design_only_no_runtime_behavior_change")
        self.assertEqual(
            manifest["semantic_readiness_architecture_doc"],
            "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md",
        )
        self.assertEqual(manifest["semantic_readiness_policy"], "semantic_layer_is_untrusted_evidence_witness_not_authority")
        self.assertEqual(manifest["future_ml_default_provider"], "disabled_null_provider")
        self.assertEqual(manifest["future_ml_runtime_policy"], "lexical_fallback_primary_semantic_optional_disabled_by_default")
        self.assertEqual(manifest["contract_version"], "1.8")

    def test_manifest_preserves_v2_shield_and_adds_future_ml_gates(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["runtime_lite_similarity_box_shield_feature_id"], "routing_signal_scorer_v2_similarity_box_shield_v1")
        for required in [
            "semantic_evidence_only",
            "lexical_fallback_primary",
            "metadata_eligibility_before_scoring",
            "no_user_query_persistence",
            "no_external_api_provider_v3",
            "no_runtime_ml_dependency_in_design",
        ]:
            self.assertIn(required, manifest["protected_architecture_characteristics"])
        for required in [
            "semantic_provider_runtime",
            "metadata_vector_manifest_generator",
            "offline_embedding_generation",
            "vector_index_adapter",
            "semantic_ui_display",
        ]:
            self.assertIn(required, manifest["shield_required_before"])

    def test_design_phase_does_not_create_runtime_artifacts(self) -> None:
        forbidden_paths = [
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "corpus_generator.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), f"design-only phase must not create runtime artifact: {path}")


if __name__ == "__main__":
    unittest.main()
