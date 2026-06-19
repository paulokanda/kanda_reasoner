import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_human_decision_recording_finalization_design import (
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_SCHEMA_VERSION,
    build_generator_candidate_human_decision_recording_finalization_contract,
    classify_generator_candidate_human_decision_recording_finalization_request,
    validate_generator_candidate_human_decision_recording_finalization_contract,
)


ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"


class GeneratorCandidateHumanDecisionRecordingFinalizationDesignTests(unittest.TestCase):
    def test_contract_validates(self):
        contract = build_generator_candidate_human_decision_recording_finalization_contract()
        result = validate_generator_candidate_human_decision_recording_finalization_contract(contract)
        self.assertTrue(result["ok"])
        self.assertEqual(result["schema_id"], GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_FEATURE_ID)
        self.assertEqual(result["schema_version"], GENERATOR_CANDIDATE_HUMAN_DECISION_RECORDING_FINALIZATION_SCHEMA_VERSION)

    def test_current_state_is_not_finalized_and_not_recorded(self):
        result = validate_generator_candidate_human_decision_recording_finalization_contract(
            build_generator_candidate_human_decision_recording_finalization_contract()
        )
        self.assertEqual(result["current_human_decision_recording_finalization_state"], "decision_recording_finalization_not_finalized")
        self.assertEqual(result["current_recorded_decision_value"], "not_recorded")
        self.assertFalse(result["human_decision_recording_finalization_created"])
        self.assertFalse(result["human_decision_recording_write_function_enabled"])

    def test_no_decision_or_approval_authority(self):
        result = validate_generator_candidate_human_decision_recording_finalization_contract(
            build_generator_candidate_human_decision_recording_finalization_contract()
        )
        self.assertFalse(result["real_human_decision_recorded_by_human_decision_recording_finalization"])
        self.assertFalse(result["human_decision_write_performed"])
        self.assertFalse(result["human_approval_inferred_from_preparation_chain"])
        self.assertFalse(result["candidate_patch_approval_recorded"])
        self.assertTrue(result["requires_explicit_human_confirmation_to_prepare_recording_finalization"])
        self.assertTrue(result["requires_future_governed_decision_recording_patch"])

    def test_no_candidate_patch_or_generation_authority(self):
        result = validate_generator_candidate_human_decision_recording_finalization_contract(
            build_generator_candidate_human_decision_recording_finalization_contract()
        )
        for key in (
            "dependency_install_authorized",
            "side_effect_authorized",
            "generator_candidate_patch_created",
            "generator_candidate_patch_authorized",
            "generator_commit_authorized",
            "generator_implementation_authorized",
            "artifact_generation_authorized",
            "artifact_writing_authorized",
            "artifact_reading_authorized",
            "source_scanning_authorized",
            "raw_text_materialization_authorized",
            "embedding_generation_authorized",
            "vector_index_generation_authorized",
            "provider_execution_authorized",
            "semantic_runtime_authorized",
            "router_authority_authorized",
        ):
            self.assertFalse(result[key], key)

    def test_activation_request_is_denied(self):
        result = classify_generator_candidate_human_decision_recording_finalization_request(
            "continue approve now record decision finalize decision create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(result["allowed_now"])
        self.assertEqual(result["current_recorded_decision_value"], "not_recorded")
        self.assertFalse(result["real_human_decision_recorded_by_human_decision_recording_finalization"])
        self.assertFalse(result["human_decision_write_performed"])
        self.assertFalse(result["human_decision_recording_finalization_created"])
        self.assertFalse(result["generator_candidate_patch_created"])
        self.assertFalse(result["generator_candidate_patch_authorized"])

    def test_schema_request_is_review_only(self):
        result = classify_generator_candidate_human_decision_recording_finalization_request(
            "show recording finalization schema and evidence checklist for review only"
        )
        self.assertTrue(result["allowed_now"])
        self.assertEqual(result["permitted_output"], "human_decision_recording_finalization_schema")
        self.assertFalse(result["human_decision_recording_finalization_created"])
        self.assertFalse(result["generator_candidate_patch_authorized"])

    def test_missing_required_field_fails(self):
        contract = build_generator_candidate_human_decision_recording_finalization_contract()
        contract.pop("current_recorded_decision_value")
        result = validate_generator_candidate_human_decision_recording_finalization_contract(contract)
        self.assertFalse(result["ok"])

    def test_enabled_flag_fails_validation(self):
        contract = build_generator_candidate_human_decision_recording_finalization_contract()
        contract["disabled_flags"]["human_decision_write_enabled"] = True
        result = validate_generator_candidate_human_decision_recording_finalization_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("human_decision_write_enabled" in err for err in result["errors"]))

    def test_forbidden_field_fails_validation(self):
        contract = build_generator_candidate_human_decision_recording_finalization_contract()
        contract["decision_write"] = {"unsafe": True}
        result = validate_generator_candidate_human_decision_recording_finalization_contract(contract)
        self.assertFalse(result["ok"])

    def test_manifest_declares_feature(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["generator_candidate_human_decision_recording_finalization_design_feature_id"],
            "routing_signal_scorer_v3_generator_candidate_human_decision_recording_finalization_design_v1",
        )
        self.assertEqual(
            manifest["generator_candidate_human_decision_recording_finalization_schema_version"],
            "3.35-generator-candidate-human-decision-recording-finalization-design",
        )
        self.assertEqual(
            manifest["generator_candidate_human_decision_recording_finalization_design_status"],
            "standard_library_only_generator_candidate_human_decision_recording_finalization_no_decision_write_no_candidate_patch_no_generator_no_runtime_behavior_change",
        )

    def test_manifest_protected_characteristics(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "generator_candidate_human_decision_recording_finalization_design",
            "generator_candidate_human_decision_recording_finalization_only",
            "no_real_human_decision_from_human_decision_recording_finalization",
            "no_decision_write_from_human_decision_recording_finalization",
            "no_recording_finalization_creation_from_human_decision_recording_finalization",
            "no_approval_inference_from_human_decision_recording_finalization",
            "no_candidate_patch_from_human_decision_recording_finalization",
            "no_generator_authorization_from_human_decision_recording_finalization",
            "no_artifact_generation_from_human_decision_recording_finalization",
            "no_source_scanning_from_human_decision_recording_finalization",
            "future_decision_recording_after_human_decision_recording_finalization_requires_separate_governed_patch",
        ):
            self.assertIn(expected, chars)

    def test_contract_and_init_do_not_export_finalization(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "build_generator_candidate_human_decision_recording_finalization_contract",
            "validate_generator_candidate_human_decision_recording_finalization_contract",
            "classify_generator_candidate_human_decision_recording_finalization_request",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_forbidden_runtime_generation_paths_absent(self):
        for rel in (
            "artifact_generator.py",
            "precomputed_artifact_generator.py",
            "precomputed_semantic_evidence_artifact_generator.py",
            "generated_artifacts",
            "artifacts",
            "vector_index.py",
            "indices",
            "providers",
        ):
            self.assertFalse((BOX / rel).exists(), rel)

    def test_design_doc_states_no_decision_write(self):
        text = (
            BOX / "design" / "routing_signal_scorer_v3_generator_candidate_human_decision_recording_finalization_design.md"
        ).read_text(encoding="utf-8")
        self.assertIn("schema-only decision-recording-finalization", text)
        self.assertIn("No decision is written", text)
        self.assertIn("not_recorded", text)
        self.assertIn("does not export public runtime behavior", text)


if __name__ == "__main__":
    unittest.main()
