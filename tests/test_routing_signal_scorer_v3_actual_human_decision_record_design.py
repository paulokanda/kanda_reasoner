from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.actual_human_decision_record_design import (
    ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID,
    ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
    ALLOWED_FUTURE_RECORDED_DECISION_VALUES,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_HUMAN_ATTESTATION_SECTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_RECORD_EFFECT_POLICY,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION,
    build_actual_human_decision_record_contract,
    classify_actual_human_decision_record_request,
    validate_actual_human_decision_record_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_actual_human_decision_record_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class ActualHumanDecisionRecordDesignTests(unittest.TestCase):
    def test_contract_identity_scope_and_decision_are_schema_only(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertEqual(record["record_id"], ACTUAL_HUMAN_DECISION_RECORD_FEATURE_ID)
        self.assertEqual(record["schema_version"], ACTUAL_HUMAN_DECISION_RECORD_SCHEMA_VERSION)
        self.assertEqual(record["record_status"], "schema_only")
        self.assertTrue(record["declared_actual_human_decision_record_schema_only"])
        self.assertEqual(record["decision_record_scope"], "actual_human_decision_record_schema_only")
        self.assertEqual(record["decision_value"], "not_recorded")
        self.assertEqual(record["decision_record_effect"], "no_effect_schema_only_not_recorded")

    def test_required_prior_milestones_preserve_full_review_chain(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertTrue(REQUIRED_PRIOR_MILESTONES.issubset(set(record["required_prior_milestones"])))
        for milestone in [
            "v3_closure_shield_frozen",
            "disabled_generation_boundary_frozen",
            "dry_run_artifact_generation_plan_frozen",
            "local_generator_candidate_review_gate_frozen",
            "human_architectural_review_record_frozen",
            "human_decision_intake_frozen",
        ]:
            self.assertIn(milestone, record["required_prior_milestones"])

    def test_allowed_future_recorded_decisions_are_named_but_not_recorded(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertTrue(
            ALLOWED_FUTURE_RECORDED_DECISION_VALUES.issubset(
                set(record["allowed_future_recorded_decision_values"])
            )
        )
        self.assertEqual(record["decision_value"], "not_recorded")
        self.assertIn(
            "permit_separate_generator_candidate_proposal_review_only",
            record["allowed_future_recorded_decision_values"],
        )

    def test_required_attestation_and_evidence_sections_are_present(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertTrue(
            REQUIRED_HUMAN_ATTESTATION_SECTIONS.issubset(
                set(record["required_human_attestation_sections"])
            )
        )
        self.assertTrue(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_RECORDING_REAL_DECISION.issubset(
                set(record["required_written_evidence_before_recording_real_decision"])
            )
        )
        self.assertTrue(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE.issubset(
                set(record["required_written_evidence_before_any_future_candidate"])
            )
        )
        self.assertIn(
            "explicit_human_decision_recording_patch_requested",
            record["required_written_evidence_before_recording_real_decision"],
        )
        self.assertIn(
            "real_human_decision_recorded_in_separate_frozen_patch",
            record["required_written_evidence_before_any_future_candidate"],
        )

    def test_allowed_and_prohibited_outputs_preserve_non_authority(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertTrue(REQUIRED_ALLOWED_RECORD_OUTPUTS.issubset(set(record["allowed_record_outputs"])))
        self.assertTrue(REQUIRED_PROHIBITED_RECORD_OUTPUTS.issubset(set(record["prohibited_record_outputs"])))
        for prohibited in [
            "real_human_decision_recorded",
            "generator_candidate_authorization",
            "generated_artifact",
            "read_artifact",
            "embedding_values",
            "runtime_semantic_score",
            "may_proceed_now",
        ]:
            self.assertIn(prohibited, record["prohibited_record_outputs"])

    def test_disabled_flags_remain_false(self) -> None:
        record = build_actual_human_decision_record_contract()
        flags = record["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, flags)
            self.assertIs(flags[flag], False)

    def test_no_authority_assertions_and_effect_policy_are_present(self) -> None:
        record = build_actual_human_decision_record_contract()
        self.assertTrue(
            REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(set(record["no_authority_assertions"]))
        )
        self.assertTrue(REQUIRED_RECORD_EFFECT_POLICY.issubset(set(record["record_effect_policy"])))
        for assertion in [
            "record_design_records_no_real_human_decision",
            "future_real_decision_recording_requires_separate_governed_patch",
            "future_generator_candidate_requires_separate_governed_patch_after_recorded_decision",
        ]:
            self.assertIn(assertion, record["no_authority_assertions"])
        self.assertIn("schema_only_record_has_no_decision_effect", record["record_effect_policy"])
        self.assertIn(
            "even_future_permit_review_only_value_does_not_authorize_generation",
            record["record_effect_policy"],
        )

    def test_validation_accepts_static_record_and_authorizes_nothing(self) -> None:
        result = validate_actual_human_decision_record_contract(
            build_actual_human_decision_record_contract()
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["decision_value"], "not_recorded")
        self.assertFalse(result["real_human_decision_recorded"])
        self.assertFalse(result["decision_write_authorized"])
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

    def test_validation_rejects_forbidden_fields_and_recorded_decision(self) -> None:
        record = build_actual_human_decision_record_contract()
        record["actual_human_decision"] = "permit_separate_generator_candidate_proposal_review_only"
        record["decision_value"] = "permit_separate_generator_candidate_proposal_review_only"
        record["decision_record_effect"] = "permit_review_only"
        result = validate_actual_human_decision_record_contract(record)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden record fields present", joined)
        self.assertIn("decision_value must remain not_recorded", joined)
        self.assertIn("decision_record_effect must remain", joined)

    def test_classifier_allows_schema_talk_but_blocks_decision_or_generation(self) -> None:
        schema = classify_actual_human_decision_record_request(
            "prepare actual human decision record schema"
        )
        self.assertTrue(schema["allowed_now"])
        self.assertEqual(schema["permitted_output"], "actual_human_decision_record_schema")
        self.assertEqual(schema["decision_value"], "not_recorded")
        self.assertFalse(schema["real_human_decision_recorded"])
        self.assertFalse(schema["decision_write_authorized"])
        self.assertFalse(schema["generator_candidate_patch_authorized"])

        blocked = classify_actual_human_decision_record_request(
            "approve now and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded"])
        self.assertFalse(blocked["decision_write_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_future_governed_patch_for_decision_recording"])
        self.assertTrue(blocked["requires_future_governed_patch_for_generation"])

    def test_design_doc_and_manifest_register_schema_only_boundary(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Design only. Schema only. Review evidence only.",
            "does not record a real human decision",
            "does not authorize a generator candidate",
            "not_recorded",
            "separate governed, validated, and frozen patch",
        ]:
            self.assertIn(phrase, doc)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["actual_human_decision_record_design_feature_id"],
            "routing_signal_scorer_v3_actual_human_decision_record_design_v1",
        )
        self.assertEqual(
            manifest["actual_human_decision_record_design_status"],
            "standard_library_only_actual_decision_record_schema_no_decision_write_no_generator_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["actual_human_decision_record_schema_version"],
            "3.17-actual-human-decision-record-design",
        )
        for characteristic in [
            "actual_human_decision_record_design",
            "actual_human_decision_record_schema_only",
            "no_real_decision_recorded_from_record_design",
            "no_decision_write_from_record_design",
            "no_generator_candidate_from_decision_record",
            "no_artifact_generation_from_decision_record",
            "no_artifact_writing_from_decision_record",
            "no_artifact_reading_from_decision_record",
            "no_source_scanning_from_decision_record",
            "no_raw_text_materialization_from_decision_record",
            "no_embeddings_from_decision_record",
            "no_vectors_from_decision_record",
            "no_provider_execution_from_decision_record",
            "no_runtime_enablement_from_decision_record",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_public_contract_and_init_are_not_extended_for_schema_only_design(self) -> None:
        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_actual_human_decision_record_contract",
            "validate_actual_human_decision_record_contract",
            "classify_actual_human_decision_record_request",
            "generate_precomputed_artifact",
            "write_precomputed_artifact",
            "run_generation_at_startup",
            "run_generation_at_runtime",
        ]:
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_no_forbidden_runtime_generation_or_provider_paths_exist(self) -> None:
        forbidden_paths = [
            "kanda_reasoner_app/routing_signal_scorer/artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/generated_artifacts",
            "kanda_reasoner_app/routing_signal_scorer/artifacts",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
            "kanda_reasoner_app/routing_signal_scorer/indices",
            "kanda_reasoner_app/routing_signal_scorer/providers",
        ]
        for forbidden_path in forbidden_paths:
            self.assertFalse((ROOT / forbidden_path).exists(), forbidden_path)


if __name__ == "__main__":
    unittest.main()
