from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_patch_skeleton_design import (
    ALLOWED_FUTURE_SKELETON_OUTCOMES,
    GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID,
    GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION,
    REQUIRED_ALLOWED_SKELETON_OUTPUTS,
    REQUIRED_BOUNDARY_DECLARATIONS,
    REQUIRED_CANDIDATE_PATCH_DECLARATIONS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_SKELETON_EFFECT_POLICY,
    REQUIRED_SKELETON_SECTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_SKELETON_OUTPUTS,
    REQUIRED_STOP_CONDITIONS,
    REQUIRED_VALIDATION_DECLARATIONS,
    build_generator_candidate_patch_skeleton_contract,
    classify_generator_candidate_patch_skeleton_request,
    validate_generator_candidate_patch_skeleton_contract,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MODULE = BOX / "generator_candidate_patch_skeleton_design.py"
DESIGN_DOC = BOX / "design" / "routing_signal_scorer_v3_generator_candidate_patch_skeleton_design.md"
MANIFEST = BOX / "box_manifest.json"
CONTRACT = BOX / "contract.py"
INIT = BOX / "__init__.py"
ROOT_HINT = ROOT / "KANDA_FREEZE_HINT.json"


class RoutingSignalScorerV3GeneratorCandidatePatchSkeletonDesignTests(unittest.TestCase):
    def test_contract_validates_and_authorizes_nothing(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        result = validate_generator_candidate_patch_skeleton_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["current_skeleton_state"], "not_skeletoned")
        self.assertFalse(result["real_human_decision_recorded_by_skeleton"])
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
        self.assertTrue(result["requires_prior_generator_candidate_patch_envelope"])
        self.assertTrue(result["requires_future_governed_candidate_patch"])
        self.assertTrue(result["requires_future_governed_generation_patch"])

    def test_contract_identity_and_effect_are_schema_only(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        self.assertEqual(contract["schema_id"], GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID)
        self.assertEqual(contract["schema_version"], GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION)
        self.assertTrue(contract["declared_generator_candidate_patch_skeleton_only"])
        self.assertEqual(contract["skeleton_scope"], "generator_candidate_patch_skeleton_only")
        self.assertEqual(contract["current_skeleton_state"], "not_skeletoned")
        self.assertEqual(contract["current_skeleton_effect"], "no_effect_schema_only_not_skeletoned")

    def test_contract_contains_required_lists(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        checks = [
            ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
            ("required_skeleton_sections", REQUIRED_SKELETON_SECTIONS),
            ("required_candidate_patch_declarations", REQUIRED_CANDIDATE_PATCH_DECLARATIONS),
            ("required_boundary_declarations", REQUIRED_BOUNDARY_DECLARATIONS),
            ("required_validation_declarations", REQUIRED_VALIDATION_DECLARATIONS),
            ("allowed_future_skeleton_outcomes", ALLOWED_FUTURE_SKELETON_OUTCOMES),
            ("allowed_skeleton_outputs", REQUIRED_ALLOWED_SKELETON_OUTPUTS),
            ("prohibited_skeleton_outputs", REQUIRED_PROHIBITED_SKELETON_OUTPUTS),
            ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
            ("skeleton_effect_policy", REQUIRED_SKELETON_EFFECT_POLICY),
            ("stop_conditions", REQUIRED_STOP_CONDITIONS),
        ]
        for field, required in checks:
            self.assertTrue(required.issubset(set(contract[field])), field)

    def test_every_disabled_flag_is_false(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_missing_required_field_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        mutated = dict(contract)
        mutated.pop("required_skeleton_sections")
        result = validate_generator_candidate_patch_skeleton_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing required field" in error for error in result["errors"]))

    def test_forbidden_output_field_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        mutated = dict(contract)
        mutated["generator_candidate_patch"] = "forbidden"
        result = validate_generator_candidate_patch_skeleton_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden skeleton field" in error for error in result["errors"]))

    def test_enabled_flag_fails_validation(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        mutated = dict(contract)
        flags = dict(mutated["disabled_flags"])
        flags["artifact_generation_enabled"] = True
        mutated["disabled_flags"] = flags
        result = validate_generator_candidate_patch_skeleton_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("disabled flag must be false" in error for error in result["errors"]))

    def test_empty_required_lists_fail_validation(self) -> None:
        contract = build_generator_candidate_patch_skeleton_contract()
        mutated = dict(contract)
        mutated["required_skeleton_sections"] = []
        result = validate_generator_candidate_patch_skeleton_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required_skeleton_sections missing" in error for error in result["errors"]))

    def test_classification_allows_schema_view_only(self) -> None:
        allowed = classify_generator_candidate_patch_skeleton_request(
            "show the candidate patch skeleton schema sections declarations"
        )
        self.assertTrue(allowed["allowed_now"])
        self.assertEqual(allowed["permitted_output"], "generator_candidate_patch_skeleton_schema")
        self.assertEqual(allowed["current_skeleton_state"], "not_skeletoned")
        self.assertTrue(allowed["requires_prior_recorded_human_decision"])
        self.assertTrue(allowed["requires_prior_generator_candidate_patch_preflight"])
        self.assertTrue(allowed["requires_prior_generator_candidate_patch_envelope"])
        self.assertFalse(allowed["generator_candidate_patch_authorized"])

    def test_classification_blocks_candidate_patch_and_generation_requests(self) -> None:
        blocked = classify_generator_candidate_patch_skeleton_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_prior_generator_candidate_patch_envelope"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_design_doc_preserves_boundary(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only",
            "schema only",
            "does not create a generator candidate patch",
            "does not authorize a generator candidate",
            "not_skeletoned",
            "another separately governed patch",
        ]:
            self.assertIn(phrase, doc)

    def test_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["generator_candidate_patch_skeleton_design_feature_id"],
            GENERATOR_CANDIDATE_PATCH_SKELETON_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_patch_skeleton_schema_version"],
            GENERATOR_CANDIDATE_PATCH_SKELETON_SCHEMA_VERSION,
        )
        for characteristic in [
            "generator_candidate_patch_skeleton_design",
            "generator_candidate_patch_skeleton_only",
            "no_generator_candidate_patch_from_skeleton",
            "no_generator_authorization_from_skeleton",
            "no_artifact_generation_from_skeleton",
            "no_artifact_writing_from_skeleton",
            "no_artifact_reading_from_skeleton",
            "no_source_scanning_from_skeleton",
            "no_raw_text_materialization_from_skeleton",
            "no_embeddings_from_skeleton",
            "no_vectors_from_skeleton",
            "no_provider_execution_from_skeleton",
            "no_runtime_enablement_from_skeleton",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_generator_candidate_patch_skeleton_contract",
            "validate_generator_candidate_patch_skeleton_contract",
            "classify_generator_candidate_patch_skeleton_request",
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
