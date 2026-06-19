from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_patch_envelope_design import (
    ALLOWED_FUTURE_ENVELOPE_OUTCOMES,
    GENERATOR_CANDIDATE_PATCH_ENVELOPE_FEATURE_ID,
    GENERATOR_CANDIDATE_PATCH_ENVELOPE_SCHEMA_VERSION,
    REQUIRED_ALLOWED_ENVELOPE_OUTPUTS,
    REQUIRED_BOUNDARY_DECLARATIONS,
    REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_ENVELOPE_EFFECT_POLICY,
    REQUIRED_ENVELOPE_SECTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_ENVELOPE_OUTPUTS,
    REQUIRED_STOP_CONDITIONS,
    REQUIRED_VALIDATION_DECLARATIONS,
    build_generator_candidate_patch_envelope_contract,
    classify_generator_candidate_patch_envelope_request,
    validate_generator_candidate_patch_envelope_contract,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MODULE = BOX / "generator_candidate_patch_envelope_design.py"
DESIGN_DOC = BOX / "design" / "routing_signal_scorer_v3_generator_candidate_patch_envelope_design.md"
MANIFEST = BOX / "box_manifest.json"
CONTRACT = BOX / "contract.py"
INIT = BOX / "__init__.py"
ROOT_HINT = ROOT / "KANDA_FREEZE_HINT.json"


class RoutingSignalScorerV3GeneratorCandidatePatchEnvelopeDesignTests(unittest.TestCase):
    def test_contract_validates_and_authorizes_nothing(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        result = validate_generator_candidate_patch_envelope_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["current_envelope_state"], "not_enveloped")
        self.assertFalse(result["real_human_decision_recorded_by_envelope"])
        self.assertFalse(result["generator_candidate_patch_created"])
        self.assertFalse(result["generator_candidate_patch_authorized"])
        self.assertFalse(result["generator_implementation_authorized"])
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["artifact_writing_authorized"])
        self.assertFalse(result["artifact_reading_authorized"])
        self.assertFalse(result["source_scanning_authorized"])
        self.assertFalse(result["raw_text_materialization_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_generation_authorized"])
        self.assertFalse(result["provider_execution_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["router_authority_authorized"])
        self.assertTrue(result["requires_prior_recorded_human_decision"])
        self.assertTrue(result["requires_prior_generator_candidate_patch_preflight"])
        self.assertTrue(result["requires_future_governed_candidate_patch"])
        self.assertTrue(result["requires_future_governed_generation_patch"])

    def test_contract_identity_and_effect_are_schema_only(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        self.assertEqual(contract["schema_id"], GENERATOR_CANDIDATE_PATCH_ENVELOPE_FEATURE_ID)
        self.assertEqual(contract["schema_version"], GENERATOR_CANDIDATE_PATCH_ENVELOPE_SCHEMA_VERSION)
        self.assertTrue(contract["declared_generator_candidate_patch_envelope_only"])
        self.assertEqual(contract["envelope_scope"], "generator_candidate_patch_envelope_only")
        self.assertEqual(contract["current_envelope_state"], "not_enveloped")
        self.assertEqual(contract["current_envelope_effect"], "no_effect_schema_only_not_enveloped")

    def test_contract_contains_required_lists(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        checks = [
            ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
            ("required_envelope_sections", REQUIRED_ENVELOPE_SECTIONS),
            ("required_candidate_patch_declarations", REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
            ("required_boundary_declarations", REQUIRED_BOUNDARY_DECLARATIONS),
            ("required_validation_declarations", REQUIRED_VALIDATION_DECLARATIONS),
            ("allowed_future_envelope_outcomes", ALLOWED_FUTURE_ENVELOPE_OUTCOMES),
            ("allowed_envelope_outputs", REQUIRED_ALLOWED_ENVELOPE_OUTPUTS),
            ("prohibited_envelope_outputs", REQUIRED_PROHIBITED_ENVELOPE_OUTPUTS),
            ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
            ("envelope_effect_policy", REQUIRED_ENVELOPE_EFFECT_POLICY),
            ("stop_conditions", REQUIRED_STOP_CONDITIONS),
        ]
        for field, required in checks:
            self.assertTrue(required.issubset(set(contract[field])), field)

    def test_every_disabled_flag_is_false(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_missing_required_field_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        mutated = dict(contract)
        mutated.pop("required_envelope_sections")
        result = validate_generator_candidate_patch_envelope_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing required field" in error for error in result["errors"]))

    def test_forbidden_output_field_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        mutated = dict(contract)
        mutated["generator_candidate_patch"] = "forbidden"
        result = validate_generator_candidate_patch_envelope_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden envelope field" in error for error in result["errors"]))

    def test_enabled_flag_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        mutated = dict(contract)
        flags = dict(mutated["disabled_flags"])
        flags["artifact_generation_enabled"] = True
        mutated["disabled_flags"] = flags
        result = validate_generator_candidate_patch_envelope_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("disabled flag must be false" in error for error in result["errors"]))

    def test_empty_required_lists_fail_validation(self) -> None:
        contract = build_generator_candidate_patch_envelope_contract()
        mutated = dict(contract)
        mutated["required_envelope_sections"] = []
        result = validate_generator_candidate_patch_envelope_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required_envelope_sections missing" in error for error in result["errors"]))

    def test_classification_allows_schema_view_only(self) -> None:
        allowed = classify_generator_candidate_patch_envelope_request(
            "show the candidate patch envelope schema sections declarations"
        )
        self.assertTrue(allowed["allowed_now"])
        self.assertEqual(allowed["permitted_output"], "generator_candidate_patch_envelope_schema")
        self.assertEqual(allowed["current_envelope_state"], "not_enveloped")
        self.assertTrue(allowed["requires_prior_recorded_human_decision"])
        self.assertTrue(allowed["requires_prior_generator_candidate_patch_preflight"])
        self.assertFalse(allowed["generator_candidate_patch_authorized"])

    def test_classification_blocks_candidate_patch_and_generation_requests(self) -> None:
        blocked = classify_generator_candidate_patch_envelope_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_design_doc_preserves_boundary(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only",
            "schema only",
            "does not create a generator candidate patch",
            "does not authorize a generator candidate",
            "not_enveloped",
            "another separately governed patch",
        ]:
            self.assertIn(phrase, doc)

    def test_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["generator_candidate_patch_envelope_design_feature_id"],
            GENERATOR_CANDIDATE_PATCH_ENVELOPE_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_patch_envelope_schema_version"],
            GENERATOR_CANDIDATE_PATCH_ENVELOPE_SCHEMA_VERSION,
        )
        for characteristic in [
            "generator_candidate_patch_envelope_design",
            "generator_candidate_patch_envelope_only",
            "no_generator_candidate_patch_from_envelope",
            "no_generator_authorization_from_envelope",
            "no_artifact_generation_from_envelope",
            "no_artifact_writing_from_envelope",
            "no_artifact_reading_from_envelope",
            "no_source_scanning_from_envelope",
            "no_raw_text_materialization_from_envelope",
            "no_embeddings_from_envelope",
            "no_vectors_from_envelope",
            "no_provider_execution_from_envelope",
            "no_runtime_enablement_from_envelope",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_generator_candidate_patch_envelope_contract",
            "validate_generator_candidate_patch_envelope_contract",
            "classify_generator_candidate_patch_envelope_request",
            "generate_precomputed_artifact",
            "write_precomputed_artifact",
            "run_generation_at_startup",
            "run_generation_at_runtime",
        ]:
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

        for forbidden_path in [
            "kanda_reasoner_app/routing_signal_scorer/artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/generated_artifacts",
            "kanda_reasoner_app/routing_signal_scorer/artifacts",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
            "kanda_reasoner_app/routing_signal_scorer/indices",
            "kanda_reasoner_app/routing_signal_scorer/providers",
        ]:
            self.assertFalse((ROOT / forbidden_path).exists(), forbidden_path)

    def test_ascii_only_and_no_root_freeze_hint(self) -> None:
        for path in [MODULE, DESIGN_DOC, Path(__file__)]:
            path.read_text(encoding="utf-8").encode("ascii")
        self.assertFalse(ROOT_HINT.exists())


if __name__ == "__main__":
    unittest.main()
