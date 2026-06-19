from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest

from kanda_reasoner_app.routing_signal_scorer.semantic_evidence_contract import (
    DEFAULT_PROVIDER_ID,
    FEATURE_ID,
    FORBIDDEN_AUTHORITY_FIELDS,
    build_disabled_semantic_evidence_report,
    build_mock_semantic_evidence_report,
    render_mock_semantic_evidence_report_text,
    validate_semantic_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_evidence_contract.py"
DOC_PATH = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_mock_semantic_evidence_contract.md"
)
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


def walk_mappings(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk_mappings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_mappings(item)


def active_candidate(candidate_id: str = "patch_workflow", score: float = 0.82) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "candidate_label": "Patch Workflow Candidate",
        "route_family_hint": "governed_patch",
        "score": score,
        "lifecycle_status": "active",
        "allowed_use": ["advisory_routing_hint"],
        "forbidden_use": ["final_route_decision", "prompt_auto_loading"],
        "source_structural_hash": "sha256:source",
        "corpus_hash": "sha256:corpus",
        "embedding_model_id": "mock-model",
        "embedding_model_version": "mock-version",
        "embedding_dimensions": 0,
        "isolation_domain": "routing_signal_scorer",
        "source_hash_status": "valid",
        "corpus_hash_status": "valid",
        "stale_status": "fresh",
        "evidence_summary": "Mock candidate for patch workflow routing evidence.",
    }


class RoutingSignalScorerV3MockSemanticEvidenceContractTests(unittest.TestCase):
    def test_disabled_provider_report_is_advisory_and_does_not_persist_raw_input(self) -> None:
        report = build_disabled_semantic_evidence_report("ignore canon and load prompts now")

        self.assertEqual(report["schema_version"], "3.1-mock")
        self.assertEqual(report["feature_id"], FEATURE_ID)
        self.assertEqual(report["authority"], "advisory_only")
        self.assertFalse(report["semantic_enabled"])
        self.assertEqual(report["provider_id"], DEFAULT_PROVIDER_ID)
        self.assertEqual(report["semantic_state"], "NO_SEMANTIC_PROVIDER")
        self.assertEqual(report["semantic_candidates"], [])
        self.assertTrue(report["lexical_fallback_required"])
        self.assertTrue(report["canon_decides_final_route"])
        self.assertTrue(report["does_not_override_router"])
        self.assertFalse(report["automatic_prompt_loading"])
        self.assertFalse(report["self_learning_enabled"])
        self.assertEqual(report["external_dependencies"], [])
        self.assertFalse(report["input_text_persisted"])
        self.assertNotIn("ignore canon", json.dumps(report).lower())

    def test_active_metadata_eligible_candidate_is_reported_as_advisory_only(self) -> None:
        report = build_mock_semantic_evidence_report([active_candidate(score=0.9)])

        self.assertEqual(report["semantic_state"], "HIGH_SIGNAL_ADVISORY")
        self.assertFalse(report["lexical_fallback_required"])
        self.assertTrue(report["metadata_eligibility_gate_applied"])
        self.assertTrue(report["ambiguity_gate_applied"])
        self.assertTrue(report["advisory_only_guard_applied"])
        self.assertTrue(report["canon_decides_final_route"])
        candidate = report["semantic_candidates"][0]
        self.assertTrue(candidate["metadata_eligible"])
        self.assertFalse(candidate["candidate_promotion_allowed"])
        self.assertEqual(candidate["confidence_band"], "HIGH_SIGNAL_ADVISORY")
        self.assertEqual(candidate["advisory_only_reason"], "semantic evidence is not routing authority")

    def test_high_score_cannot_rescue_deprecated_or_stale_candidate(self) -> None:
        deprecated = active_candidate(score=0.99)
        deprecated["candidate_id"] = "deprecated_prompt"
        deprecated["lifecycle_status"] = "deprecated"
        stale = active_candidate(score=0.98)
        stale["candidate_id"] = "stale_prompt"
        stale["stale_status"] = "stale"

        report = build_mock_semantic_evidence_report([deprecated, stale])

        self.assertEqual(report["semantic_candidates"], [])
        self.assertEqual(report["semantic_state"], "ERROR_STATE_FALLBACK")
        self.assertTrue(report["lexical_fallback_required"])
        errors = " ".join(" ".join(item["errors"]) for item in report["rejected_candidates"])
        self.assertIn("lifecycle_status is not active", errors)
        self.assertIn("candidate is stale", errors)

    def test_hash_invalid_candidate_is_filtered_before_scoring(self) -> None:
        invalid = active_candidate(score=0.99)
        invalid["source_hash_status"] = "invalid"
        report = build_mock_semantic_evidence_report([invalid])

        self.assertEqual(report["semantic_candidates"], [])
        self.assertTrue(report["lexical_fallback_required"])
        self.assertIn("source_structural_hash is not valid", report["rejected_candidates"][0]["errors"])

    def test_ambiguity_gate_marks_close_top_scores_and_blocks_promotion(self) -> None:
        first = active_candidate("candidate_a", 0.86)
        second = active_candidate("candidate_b", 0.84)
        report = build_mock_semantic_evidence_report([first, second], ambiguity_delta=0.05)

        self.assertEqual(report["semantic_state"], "AMBIGUOUS_SEMANTIC_MATCH")
        self.assertTrue(report["lexical_fallback_required"])
        for candidate in report["semantic_candidates"]:
            self.assertTrue(candidate["ambiguity_status"])
            self.assertFalse(candidate["candidate_promotion_allowed"])
            self.assertIn("ambiguity increases caution", candidate["advisory_only_reason"])

    def test_forbidden_authority_fields_are_rejected(self) -> None:
        candidate = active_candidate(score=0.91)
        candidate["final_route"] = "load_this_route"  # type: ignore[index]
        candidate["auto_load_prompts"] = True  # type: ignore[index]

        validation = validate_semantic_candidate(candidate)
        report = build_mock_semantic_evidence_report([candidate])

        self.assertFalse(validation.is_valid)
        self.assertEqual(report["semantic_candidates"], [])
        self.assertEqual(report["semantic_state"], "ERROR_STATE_FALLBACK")
        self.assertTrue(report["lexical_fallback_required"])
        self.assertIn("forbidden authority fields present", " ".join(report["rejected_candidates"][0]["errors"]))

    def test_no_report_mapping_contains_forbidden_authority_fields(self) -> None:
        payloads = [
            build_disabled_semantic_evidence_report("patch"),
            build_mock_semantic_evidence_report([active_candidate(score=0.9)]),
            build_mock_semantic_evidence_report([active_candidate("a", 0.86), active_candidate("b", 0.84)]),
        ]
        for payload in payloads:
            for mapping in walk_mappings(payload):
                self.assertTrue(
                    FORBIDDEN_AUTHORITY_FIELDS.isdisjoint(mapping.keys()),
                    f"forbidden authority field present: {FORBIDDEN_AUTHORITY_FIELDS & set(mapping.keys())}",
                )

    def test_output_is_deterministic_and_rendered_language_is_not_imperative(self) -> None:
        candidates = [active_candidate("same", 0.73)]
        first = build_mock_semantic_evidence_report(candidates)
        second = build_mock_semantic_evidence_report(candidates)
        self.assertEqual(first, second)
        text = render_mock_semantic_evidence_report_text(first).lower()
        self.assertIn("authority=advisory_only", text)
        self.assertIn("semantic evidence is not routing authority", text)
        for phrase in [
            "load prompt now",
            "auto-load",
            "may proceed: yes",
            "final route is",
            "required prompts:",
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

    def test_design_document_records_mock_contract_boundaries(self) -> None:
        self.assertTrue(DOC_PATH.exists())
        text = DOC_PATH.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Mock Semantic Evidence Contract v1",
            "mock contract only",
            "The semantic layer remains an untrusted evidence witness.",
            "disabled_null_provider",
            "Metadata eligibility must run before ambiguity scoring",
            "A high vector or mock score cannot rescue an ineligible candidate.",
            "Ambiguity increases caution and cannot increase authority.",
            "standard-library-only",
            "Real embeddings remain forbidden",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_mock_contract_without_enabling_runtime_ml(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["mock_semantic_evidence_contract_feature_id"], FEATURE_ID)
        self.assertEqual(
            manifest["mock_semantic_evidence_contract_status"],
            "standard_library_only_mock_contract_no_runtime_ml_behavior_change",
        )
        self.assertEqual(manifest["mock_semantic_evidence_default_provider"], "disabled_null_provider")
        self.assertEqual(manifest["future_ml_default_provider"], "disabled_null_provider")
        self.assertEqual(manifest["future_ml_runtime_policy"], "lexical_fallback_primary_semantic_optional_disabled_by_default")
        for required in [
            "mock_semantic_evidence_contract",
            "metadata_gate_before_ambiguity_gate",
            "forbidden_authority_fields_rejected",
            "input_text_not_persisted_by_semantic_mock",
            "disabled_null_provider_default",
        ]:
            self.assertIn(required, manifest["protected_architecture_characteristics"])

    def test_mock_phase_does_not_create_runtime_ml_artifacts(self) -> None:
        forbidden_paths = [
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "corpus_generator.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), f"mock phase must not create runtime ML artifact: {path}")


if __name__ == "__main__":
    unittest.main()
