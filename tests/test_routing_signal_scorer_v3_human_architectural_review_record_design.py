from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.human_architectural_review_record_design import (
    FORBIDDEN_REVIEW_RECORD_FIELDS,
    HUMAN_ARCHITECTURAL_REVIEW_RECORD_FEATURE_ID,
    HUMAN_ARCHITECTURAL_REVIEW_RECORD_SCHEMA_VERSION,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_HUMAN_REVIEW_SECTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_REVIEW_QUESTIONS,
    build_human_architectural_review_record_contract,
    classify_human_architectural_review_request,
    validate_human_architectural_review_record_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_human_architectural_review_record_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class HumanArchitecturalReviewRecordDesignTests(unittest.TestCase):
    def test_contract_identity_and_scope_are_schema_only(self) -> None:
        contract = build_human_architectural_review_record_contract()
        self.assertEqual(contract["record_id"], HUMAN_ARCHITECTURAL_REVIEW_RECORD_FEATURE_ID)
        self.assertEqual(contract["schema_version"], HUMAN_ARCHITECTURAL_REVIEW_RECORD_SCHEMA_VERSION)
        self.assertEqual(contract["record_status"], "schema_only")
        self.assertTrue(contract["declared_human_review_only"])
        self.assertEqual(contract["review_scope"], "human_architectural_review_record_only")

    def test_required_prior_milestones_preserve_frozen_chain(self) -> None:
        contract = build_human_architectural_review_record_contract()
        prior = set(contract["required_prior_milestones"])
        self.assertTrue(REQUIRED_PRIOR_MILESTONES.issubset(prior))
        for item in [
            "v3_closure_shield_frozen",
            "disabled_generation_boundary_frozen",
            "dry_run_artifact_generation_plan_frozen",
            "local_generator_candidate_review_gate_frozen",
        ]:
            self.assertIn(item, prior)

    def test_review_questions_and_sections_are_complete(self) -> None:
        contract = build_human_architectural_review_record_contract()
        self.assertTrue(REQUIRED_REVIEW_QUESTIONS.issubset(set(contract["required_review_questions"])))
        self.assertTrue(
            REQUIRED_HUMAN_REVIEW_SECTIONS.issubset(
                set(contract["required_human_review_sections"])
            )
        )
        self.assertIn(
            "what_exact_future_generator_candidate_would_be_reviewed",
            contract["required_review_questions"],
        )
        self.assertIn("final_human_decision_placeholder", contract["required_human_review_sections"])

    def test_allowed_outputs_are_review_record_only(self) -> None:
        contract = build_human_architectural_review_record_contract()
        outputs = set(contract["allowed_record_outputs"])
        self.assertTrue(REQUIRED_ALLOWED_RECORD_OUTPUTS.issubset(outputs))
        for item in [
            "human_review_record_schema",
            "human_review_decision_placeholder",
            "risk_register_template",
            "review_evidence_only",
            "no_artifact_generated",
            "no_runtime_enablement",
        ]:
            self.assertIn(item, outputs)

    def test_prohibited_outputs_block_generator_and_authority_material(self) -> None:
        contract = build_human_architectural_review_record_contract()
        prohibited = set(contract["prohibited_record_outputs"])
        self.assertTrue(REQUIRED_PROHIBITED_RECORD_OUTPUTS.issubset(prohibited))
        for item in [
            "generator_candidate_patch",
            "generated_artifact",
            "raw_prompt_text",
            "embedding_values",
            "vector_index",
            "provider_config",
            "final_route",
            "may_proceed_now",
            "freeze_memory_write",
        ]:
            self.assertIn(item, prohibited)

    def test_disabled_flags_forbid_generation_and_runtime_enablement(self) -> None:
        contract = build_human_architectural_review_record_contract()
        flags = contract["disabled_flags"]
        self.assertTrue(REQUIRED_DISABLED_FLAGS_FALSE.issubset(flags.keys()))
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIs(flags[flag], False, flag)
        for flag in [
            "generator_candidate_patch_authorized",
            "artifact_generation_enabled",
            "artifact_writing_enabled",
            "artifact_reader_enabled",
            "source_scanning_enabled",
            "raw_text_materialization_enabled",
            "embedding_generation_enabled",
            "semantic_runtime_enabled",
            "prompt_router_mutation_enabled",
        ]:
            self.assertFalse(flags[flag])

    def test_no_authority_and_decision_policy_are_complete(self) -> None:
        contract = build_human_architectural_review_record_contract()
        self.assertTrue(
            REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(set(contract["no_authority_assertions"]))
        )
        self.assertIn("default_decision_is_not_recorded", contract["decision_policy"])
        self.assertIn("only_human_can_record_decision", contract["decision_policy"])
        self.assertIn(
            "permit_proposal_is_not_generation_authorization",
            contract["decision_policy"],
        )
        self.assertIn("canon_remains_final_authority", contract["no_authority_assertions"])

    def test_validator_accepts_default_contract_and_denies_authority(self) -> None:
        contract = build_human_architectural_review_record_contract()
        result = validate_human_architectural_review_record_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["generator_candidate_patch_authorized"])
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
        self.assertTrue(result["requires_future_governed_patch"])
        self.assertTrue(result["review_evidence_only"])

    def test_validator_rejects_missing_disabled_flag(self) -> None:
        contract = build_human_architectural_review_record_contract()
        del contract["disabled_flags"]["artifact_generation_enabled"]
        result = validate_human_architectural_review_record_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required disabled flags must be false" in error for error in result["errors"]))

    def test_validator_rejects_forbidden_fields(self) -> None:
        for field in sorted(FORBIDDEN_REVIEW_RECORD_FIELDS):
            contract = build_human_architectural_review_record_contract()
            contract[field] = "forbidden"
            result = validate_human_architectural_review_record_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(
                any("forbidden review record fields present" in error for error in result["errors"]),
                field,
            )

    def test_request_classifier_allows_review_record_only_but_denies_generation(self) -> None:
        review = classify_human_architectural_review_request("human review record template")
        self.assertTrue(review["allowed_now"])
        self.assertEqual(review["permitted_output"], "human_review_record_schema")
        self.assertTrue(review["review_evidence_only"])
        self.assertFalse(review["generator_candidate_patch_authorized"])
        self.assertTrue(review["requires_future_governed_patch_for_generation"])

        for action in [
            "generate artifact now",
            "write artifact from review record",
            "read artifact",
            "scan source for generation",
            "materialize raw text",
            "create embeddings",
            "create vector index",
            "enable provider runtime",
            "modify router authority",
            "bypass the future patch",
        ]:
            result = classify_human_architectural_review_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_generation_authorized"], action)
            self.assertFalse(result["artifact_writing_authorized"], action)
            self.assertFalse(result["artifact_reading_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_index_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["authority_granted"], action)
            self.assertTrue(result["requires_future_governed_patch_for_generation"], action)

    def test_design_doc_preserves_review_record_only_boundary(self) -> None:
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Human Architectural Review Record Design v1",
            "It is not a generator.",
            "schema-only human architectural review record design",
            "The review record cannot authorize generation by itself.",
            "Future generator candidate work still requires a separate governed patch.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_runtime_export(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["human_architectural_review_record_design_feature_id"],
            "routing_signal_scorer_v3_human_architectural_review_record_design_v1",
        )
        self.assertEqual(
            manifest["human_architectural_review_record_design_status"],
            "standard_library_only_review_record_schema_no_generator_no_artifact_writing_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["human_architectural_review_record_schema_version"],
            "3.15-human-architectural-review-record-design",
        )
        for characteristic in [
            "human_architectural_review_record_design",
            "human_review_record_schema_only",
            "no_generator_candidate_from_review_record",
            "no_artifact_generation_from_review_record",
            "no_artifact_writing_from_review_record",
            "no_artifact_reading_from_review_record",
            "no_source_scanning_from_review_record",
            "no_raw_text_materialization_from_review_record",
            "no_embeddings_from_review_record",
            "no_vectors_from_review_record",
            "no_provider_execution_from_review_record",
            "no_runtime_enablement_from_review_record",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_human_architectural_review_record_contract",
            "validate_human_architectural_review_record_contract",
            "classify_human_architectural_review_request",
            "generate_precomputed_artifact",
            "write_precomputed_artifact",
            "run_generation_at_startup",
            "run_generation_at_runtime",
        ]:
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_forbidden_runtime_generation_paths_absent(self) -> None:
        for relative in [
            "kanda_reasoner_app/routing_signal_scorer/artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/generated_artifacts",
            "kanda_reasoner_app/routing_signal_scorer/artifacts",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
            "kanda_reasoner_app/routing_signal_scorer/indices",
            "kanda_reasoner_app/routing_signal_scorer/providers",
        ]:
            self.assertFalse((ROOT / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
