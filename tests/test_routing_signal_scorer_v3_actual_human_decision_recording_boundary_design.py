from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.actual_human_decision_recording_boundary_design import (
    ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID,
    ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION,
    ALLOWED_FUTURE_DECISION_VALUES,
    REQUIRED_ALLOWED_BOUNDARY_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRE_RECORDING_EVIDENCE,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS,
    REQUIRED_RECORDING_EFFECT_POLICY,
    REQUIRED_RECORDING_PATCH_CONSTRAINTS,
    build_actual_human_decision_recording_boundary_contract,
    classify_actual_human_decision_recording_boundary_request,
    validate_actual_human_decision_recording_boundary_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_actual_human_decision_recording_boundary_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class ActualHumanDecisionRecordingBoundaryDesignTests(unittest.TestCase):
    def test_contract_identity_and_state_are_schema_only(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertEqual(boundary["boundary_id"], ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID)
        self.assertEqual(boundary["schema_version"], ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION)
        self.assertTrue(boundary["declared_actual_human_decision_recording_boundary_only"])
        self.assertEqual(boundary["recording_boundary_scope"], "actual_human_decision_recording_boundary_schema_only")
        self.assertEqual(boundary["current_recording_state"], "not_recorded")
        self.assertEqual(boundary["current_recording_effect"], "no_effect_schema_only_not_recorded")

    def test_required_prior_milestones_are_preserved(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_PRIOR_MILESTONES.issubset(set(boundary["required_prior_milestones"])))
        for marker in [
            "actual_human_decision_record_design_frozen",
            "human_decision_intake_frozen",
            "local_generator_candidate_review_gate_frozen",
            "v3_closure_shield_frozen",
        ]:
            self.assertIn(marker, boundary["required_prior_milestones"])

    def test_allowed_future_decisions_are_review_only_values(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(ALLOWED_FUTURE_DECISION_VALUES.issubset(set(boundary["allowed_future_decision_values"])))
        self.assertIn("permit_separate_generator_candidate_proposal_review_only", boundary["allowed_future_decision_values"])
        self.assertNotIn("generate_artifact", boundary["allowed_future_decision_values"])
        self.assertNotIn("enable_semantic_runtime", boundary["allowed_future_decision_values"])

    def test_pre_recording_evidence_is_required_before_any_future_write(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_PRE_RECORDING_EVIDENCE.issubset(set(boundary["required_pre_recording_evidence"])))
        for marker in [
            "explicit_human_request_to_record_actual_decision",
            "explicit_decision_value_selected_from_allowed_vocabulary",
            "written_privacy_review_present",
            "written_authority_boundary_review_present",
        ]:
            self.assertIn(marker, boundary["required_pre_recording_evidence"])

    def test_future_recording_patch_constraints_keep_generation_disabled(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_RECORDING_PATCH_CONSTRAINTS.issubset(set(boundary["required_recording_patch_constraints"])))
        for marker in [
            "must_not_generate_artifacts",
            "must_not_write_semantic_artifacts",
            "must_not_read_semantic_artifacts",
            "must_not_enable_semantic_runtime",
            "must_not_change_router_authority",
        ]:
            self.assertIn(marker, boundary["required_recording_patch_constraints"])

    def test_allowed_outputs_are_review_evidence_only(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_ALLOWED_BOUNDARY_OUTPUTS.issubset(set(boundary["allowed_boundary_outputs"])))
        for allowed in [
            "actual_human_decision_recording_boundary_schema",
            "pre_recording_evidence_checklist",
            "no_real_decision_recorded_by_this_boundary",
            "no_generator_candidate_patch_authorized",
        ]:
            self.assertIn(allowed, boundary["allowed_boundary_outputs"])

    def test_prohibited_outputs_block_decision_write_and_runtime_ml(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_PROHIBITED_BOUNDARY_OUTPUTS.issubset(set(boundary["prohibited_boundary_outputs"])))
        for prohibited in [
            "real_human_decision_recorded",
            "decision_record_written",
            "generator_candidate_authorization",
            "generated_artifact",
            "embedding_values",
            "runtime_semantic_score",
            "may_proceed_now",
        ]:
            self.assertIn(prohibited, boundary["prohibited_boundary_outputs"])

    def test_disabled_flags_remain_false(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        flags = boundary["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, flags)
            self.assertIs(flags[flag], False)

    def test_no_authority_assertions_and_effect_policy_are_present(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(set(boundary["no_authority_assertions"])))
        self.assertTrue(REQUIRED_RECORDING_EFFECT_POLICY.issubset(set(boundary["recording_effect_policy"])))
        self.assertIn("boundary_records_no_real_human_decision", boundary["no_authority_assertions"])
        self.assertIn("boundary_writes_no_decision_record", boundary["no_authority_assertions"])
        self.assertIn("schema_only_boundary_has_no_decision_effect", boundary["recording_effect_policy"])
        self.assertIn("future_recorded_permit_review_only_value_does_not_authorize_generation", boundary["recording_effect_policy"])

    def test_validation_accepts_static_boundary_and_authorizes_nothing(self) -> None:
        result = validate_actual_human_decision_recording_boundary_contract(
            build_actual_human_decision_recording_boundary_contract()
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["current_recording_state"], "not_recorded")
        self.assertFalse(result["real_human_decision_recorded"])
        self.assertFalse(result["decision_recording_authorized"])
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

    def test_validation_rejects_forbidden_fields_and_recording_state_change(self) -> None:
        boundary = build_actual_human_decision_recording_boundary_contract()
        boundary["actual_human_decision"] = "permit_separate_generator_candidate_proposal_review_only"
        boundary["current_recording_state"] = "recorded"
        boundary["current_recording_effect"] = "permit_review_only"
        result = validate_actual_human_decision_recording_boundary_contract(boundary)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden boundary fields present", joined)
        self.assertIn("current_recording_state must remain not_recorded", joined)
        self.assertIn("current_recording_effect must remain", joined)

    def test_classifier_allows_boundary_schema_talk_but_blocks_decision_or_generation(self) -> None:
        schema = classify_actual_human_decision_recording_boundary_request(
            "prepare actual human decision recording boundary schema"
        )
        self.assertTrue(schema["allowed_now"])
        self.assertEqual(schema["permitted_output"], "actual_human_decision_recording_boundary_schema")
        self.assertEqual(schema["current_recording_state"], "not_recorded")
        self.assertFalse(schema["real_human_decision_recorded"])
        self.assertFalse(schema["decision_recording_authorized"])
        self.assertFalse(schema["decision_write_authorized"])
        self.assertFalse(schema["generator_candidate_patch_authorized"])

        blocked = classify_actual_human_decision_recording_boundary_request(
            "approve now record decision and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded"])
        self.assertFalse(blocked["decision_recording_authorized"])
        self.assertFalse(blocked["decision_write_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_future_governed_patch_for_decision_recording"])
        self.assertTrue(blocked["requires_future_governed_patch_for_generation"])

    def test_design_doc_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only, schema only, review evidence only",
            "does not record a real human decision",
            "does not authorize a decision write",
            "not_recorded",
            "separate governed candidate proposal review patch",
        ]:
            self.assertIn(phrase, doc)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["actual_human_decision_recording_boundary_design_feature_id"],
            ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_FEATURE_ID,
        )
        self.assertEqual(
            manifest["actual_human_decision_recording_boundary_schema_version"],
            ACTUAL_HUMAN_DECISION_RECORDING_BOUNDARY_SCHEMA_VERSION,
        )
        for characteristic in [
            "actual_human_decision_recording_boundary_design",
            "actual_human_decision_recording_boundary_schema_only",
            "no_real_decision_recorded_from_recording_boundary",
            "no_decision_write_from_recording_boundary",
            "no_generator_candidate_from_recording_boundary",
            "no_artifact_generation_from_recording_boundary",
            "no_artifact_writing_from_recording_boundary",
            "no_artifact_reading_from_recording_boundary",
            "no_source_scanning_from_recording_boundary",
            "no_raw_text_materialization_from_recording_boundary",
            "no_embeddings_from_recording_boundary",
            "no_vectors_from_recording_boundary",
            "no_provider_execution_from_recording_boundary",
            "no_runtime_enablement_from_recording_boundary",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_actual_human_decision_recording_boundary_contract",
            "validate_actual_human_decision_recording_boundary_contract",
            "classify_actual_human_decision_recording_boundary_request",
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


if __name__ == "__main__":
    unittest.main()
