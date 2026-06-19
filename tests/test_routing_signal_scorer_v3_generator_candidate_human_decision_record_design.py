from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_human_decision_record_design import (
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
    GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
    REQUIRED_ALLOWED_RECORD_OUTPUTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_FUTURE_RECORDING_INPUTS,
    REQUIRED_HUMAN_DECISION_RECORD_FIELDS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_RECORD_OUTPUTS,
    REQUIRED_RECORD_EFFECT_POLICY,
    REQUIRED_STOP_CONDITIONS,
    build_generator_candidate_human_decision_record_contract,
    classify_generator_candidate_human_decision_record_request,
    validate_generator_candidate_human_decision_record_contract,
)

MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_generator_candidate_human_decision_record_design.md"
CONTRACT = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class GeneratorCandidateHumanDecisionRecordDesignTests(unittest.TestCase):
    def test_contract_validates(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        result = validate_generator_candidate_human_decision_record_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["schema_id"], GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID)
        self.assertEqual(result["schema_version"], GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION)
        self.assertEqual(result["current_human_decision_record_state"], "human_decision_record_not_recorded")
        self.assertEqual(result["current_recorded_decision_value"], "not_recorded")
        self.assertTrue(result["requires_prior_generator_candidate_human_decision_gate"])
        self.assertTrue(result["requires_future_governed_decision_recording_patch"])
        self.assertTrue(result["requires_future_governed_candidate_patch"])
        self.assertTrue(result["requires_future_governed_generation_patch"])

    def test_contract_has_required_schema_sections(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        for field in REQUIRED_HUMAN_DECISION_RECORD_FIELDS:
            self.assertIn(field, contract)

    def test_required_prior_and_record_input_sets_are_present(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        self.assertTrue(REQUIRED_PRIOR_MILESTONES.issubset(set(contract["required_prior_milestones"])))
        self.assertTrue(REQUIRED_FUTURE_RECORDING_INPUTS.issubset(set(contract["required_future_recording_inputs"])))
        self.assertTrue(REQUIRED_ALLOWED_RECORD_OUTPUTS.issubset(set(contract["allowed_record_outputs"])))
        self.assertTrue(REQUIRED_PROHIBITED_RECORD_OUTPUTS.issubset(set(contract["prohibited_record_outputs"])))
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(set(contract["no_authority_assertions"])))
        self.assertTrue(REQUIRED_RECORD_EFFECT_POLICY.issubset(set(contract["record_effect_policy"])))
        self.assertTrue(REQUIRED_STOP_CONDITIONS.issubset(set(contract["stop_conditions"])))

    def test_all_disabled_flags_are_false(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        flags = contract["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, flags)
            self.assertIs(flags[flag], False)

    def test_record_does_not_record_or_infer_approval(self) -> None:
        result = validate_generator_candidate_human_decision_record_contract(
            build_generator_candidate_human_decision_record_contract()
        )
        self.assertFalse(result["real_human_decision_recorded_by_human_decision_record"])
        self.assertFalse(result["human_approval_inferred_from_preparation_chain"])
        self.assertFalse(result["candidate_patch_approval_recorded"])

    def test_no_candidate_patch_or_generator_authority(self) -> None:
        result = validate_generator_candidate_human_decision_record_contract(
            build_generator_candidate_human_decision_record_contract()
        )
        self.assertFalse(result["generator_candidate_patch_created"])
        self.assertFalse(result["generator_candidate_patch_authorized"])
        self.assertFalse(result["generator_implementation_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["router_authority_authorized"])

    def test_no_artifact_io_source_scanning_or_embeddings(self) -> None:
        result = validate_generator_candidate_human_decision_record_contract(
            build_generator_candidate_human_decision_record_contract()
        )
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["artifact_writing_authorized"])
        self.assertFalse(result["artifact_reading_authorized"])
        self.assertFalse(result["source_scanning_authorized"])
        self.assertFalse(result["raw_text_materialization_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_generation_authorized"])
        self.assertFalse(result["provider_execution_authorized"])

    def test_schema_view_allowed_but_activation_denied(self) -> None:
        allowed = classify_generator_candidate_human_decision_record_request(
            "show the human decision record schema checklist"
        )
        self.assertTrue(allowed["allowed_now"])
        blocked = classify_generator_candidate_human_decision_record_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded_by_human_decision_record"])
        self.assertFalse(blocked["human_approval_inferred_from_preparation_chain"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertTrue(blocked["requires_future_governed_decision_recording_patch"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_manifest_registers_design_only_boundary(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["generator_candidate_human_decision_record_design_feature_id"],
            GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_human_decision_record_schema_version"],
            GENERATOR_CANDIDATE_HUMAN_DECISION_RECORD_SCHEMA_VERSION,
        )
        self.assertEqual(
            manifest["generator_candidate_human_decision_record_design_status"],
            "standard_library_only_generator_candidate_human_decision_record_no_decision_recorded_no_candidate_patch_no_generator_no_runtime_behavior_change",
        )
        protected = set(manifest["protected_architecture_characteristics"])
        for value in [
            "generator_candidate_human_decision_record_design",
            "generator_candidate_human_decision_record_only",
            "no_real_human_decision_from_human_decision_record",
            "no_approval_inference_from_human_decision_record",
            "no_candidate_patch_from_human_decision_record",
            "no_generator_authorization_from_human_decision_record",
            "future_decision_recording_after_human_decision_record_requires_separate_governed_patch",
        ]:
            self.assertIn(value, protected)

    def test_design_doc_records_non_goals(self) -> None:
        text = DESIGN_DOC.read_text(encoding="utf-8")
        self.assertIn("schema only", text)
        self.assertIn("human_decision_record_not_recorded", text)
        self.assertIn("does not record a human decision", text)
        self.assertIn("does not infer approval", text)
        self.assertIn("does not create or authorize a generator candidate patch", text)
        self.assertIn("does not authorize generation", text)

    def test_no_public_contract_export(self) -> None:
        forbidden = [
            "build_generator_candidate_human_decision_record_contract",
            "validate_generator_candidate_human_decision_record_contract",
            "classify_generator_candidate_human_decision_record_request",
        ]
        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for name in forbidden:
            self.assertNotIn(name, contract_text)
            self.assertNotIn(name, init_text)

    def test_contract_rejects_forbidden_output_fields(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        contract["recorded_human_decision"] = "approved"
        result = validate_generator_candidate_human_decision_record_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden record field" in error for error in result["errors"]))

    def test_contract_rejects_enabled_disabled_flag(self) -> None:
        contract = build_generator_candidate_human_decision_record_contract()
        contract["disabled_flags"]["generator_candidate_patch_creation_enabled"] = True
        result = validate_generator_candidate_human_decision_record_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("disabled flag must be false" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
