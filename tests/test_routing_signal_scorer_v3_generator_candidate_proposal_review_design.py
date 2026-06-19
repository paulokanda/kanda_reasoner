from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_proposal_review_design import (
    ALLOWED_FUTURE_REVIEW_OUTCOMES,
    FORBIDDEN_REVIEW_FIELDS,
    GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID,
    GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION,
    REQUIRED_ALLOWED_REVIEW_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_REVIEW_OUTPUTS,
    REQUIRED_PROPOSAL_INPUTS,
    REQUIRED_REJECTION_REASONS,
    REQUIRED_REVIEW_EFFECT_POLICY,
    REQUIRED_REVIEW_QUESTIONS,
    REQUIRED_STOP_CONDITIONS,
    build_generator_candidate_proposal_review_contract,
    classify_generator_candidate_proposal_review_request,
    validate_generator_candidate_proposal_review_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_generator_candidate_proposal_review_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"
ROOT_HINT = ROOT / "KANDA_FREEZE_HINT.json"
MODULE = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "generator_candidate_proposal_review_design.py"
)


class RoutingSignalScorerV3GeneratorCandidateProposalReviewDesignTests(unittest.TestCase):
    def test_contract_validates_and_remains_review_only(self) -> None:
        review = build_generator_candidate_proposal_review_contract()
        result = validate_generator_candidate_proposal_review_contract(review)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["current_review_state"], "not_reviewed")
        self.assertFalse(result["real_human_decision_recorded_by_review"])
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
        self.assertTrue(result["requires_future_governed_candidate_patch"])
        self.assertTrue(result["requires_future_governed_generation_patch"])

    def test_contract_contains_required_lists(self) -> None:
        review = build_generator_candidate_proposal_review_contract()
        self.assertEqual(review["schema_id"], GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID)
        self.assertEqual(review["schema_version"], GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION)
        self.assertEqual(review["current_review_state"], "not_reviewed")
        self.assertEqual(review["current_review_effect"], "no_effect_schema_only_not_reviewed")
        checks = [
            ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
            ("required_proposal_inputs", REQUIRED_PROPOSAL_INPUTS),
            ("required_review_questions", REQUIRED_REVIEW_QUESTIONS),
            ("required_rejection_reasons", REQUIRED_REJECTION_REASONS),
            ("allowed_future_review_outcomes", ALLOWED_FUTURE_REVIEW_OUTCOMES),
            ("allowed_review_outputs", REQUIRED_ALLOWED_REVIEW_OUTPUTS),
            ("prohibited_review_outputs", REQUIRED_PROHIBITED_REVIEW_OUTPUTS),
            ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
            ("review_effect_policy", REQUIRED_REVIEW_EFFECT_POLICY),
            ("stop_conditions", REQUIRED_STOP_CONDITIONS),
        ]
        for field, required in checks:
            self.assertTrue(required.issubset(set(review[field])), field)

    def test_every_disabled_flag_is_false(self) -> None:
        review = build_generator_candidate_proposal_review_contract()
        disabled_flags = review["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, disabled_flags)
            self.assertFalse(disabled_flags[flag], flag)

    def test_forbidden_fields_fail_validation(self) -> None:
        review = build_generator_candidate_proposal_review_contract()
        for field in FORBIDDEN_REVIEW_FIELDS:
            mutated = dict(review)
            mutated[field] = "forbidden"
            result = validate_generator_candidate_proposal_review_contract(mutated)
            self.assertFalse(result["ok"], field)

    def test_missing_required_questions_fail_validation(self) -> None:
        review = build_generator_candidate_proposal_review_contract()
        mutated = dict(review)
        mutated["required_review_questions"] = []
        result = validate_generator_candidate_proposal_review_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required_review_questions missing" in e for e in result["errors"]))

    def test_classification_allows_review_schema_view_only(self) -> None:
        allowed = classify_generator_candidate_proposal_review_request(
            "show the proposal review schema checklist questions"
        )
        self.assertTrue(allowed["allowed_now"])
        self.assertEqual(allowed["permitted_output"], "generator_candidate_proposal_review_schema")
        self.assertEqual(allowed["current_review_state"], "not_reviewed")
        self.assertTrue(allowed["requires_prior_recorded_human_decision"])
        self.assertFalse(allowed["generator_candidate_patch_authorized"])

    def test_classification_blocks_generation_and_candidate_patch_requests(self) -> None:
        blocked = classify_generator_candidate_proposal_review_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded_by_review"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_prior_recorded_human_decision"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_design_doc_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only, schema only, and review evidence only",
            "does not create a generator candidate patch",
            "does not authorize a generator candidate",
            "not_reviewed",
            "another separately governed patch",
        ]:
            self.assertIn(phrase, doc)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["generator_candidate_proposal_review_design_feature_id"],
            GENERATOR_CANDIDATE_PROPOSAL_REVIEW_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_proposal_review_schema_version"],
            GENERATOR_CANDIDATE_PROPOSAL_REVIEW_SCHEMA_VERSION,
        )
        for characteristic in [
            "generator_candidate_proposal_review_design",
            "generator_candidate_proposal_review_only",
            "no_generator_candidate_patch_from_proposal_review",
            "no_generator_authorization_from_proposal_review",
            "no_artifact_generation_from_proposal_review",
            "no_artifact_writing_from_proposal_review",
            "no_artifact_reading_from_proposal_review",
            "no_source_scanning_from_proposal_review",
            "no_raw_text_materialization_from_proposal_review",
            "no_embeddings_from_proposal_review",
            "no_vectors_from_proposal_review",
            "no_provider_execution_from_proposal_review",
            "no_runtime_enablement_from_proposal_review",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_generator_candidate_proposal_review_contract",
            "validate_generator_candidate_proposal_review_contract",
            "classify_generator_candidate_proposal_review_request",
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
