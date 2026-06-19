from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.human_decision_intake_design import (
    ALLOWED_FUTURE_DECISION_VALUES,
    FORBIDDEN_INTAKE_FIELDS,
    HUMAN_DECISION_INTAKE_FEATURE_ID,
    HUMAN_DECISION_INTAKE_SCHEMA_VERSION,
    REQUIRED_ALLOWED_INTAKE_OUTPUTS,
    REQUIRED_DECISION_CONTEXT_SECTIONS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_INTAKE_OUTPUTS,
    REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE,
    build_human_decision_intake_contract,
    classify_human_decision_intake_request,
    validate_human_decision_intake_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_human_decision_intake_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class HumanDecisionIntakeDesignTests(unittest.TestCase):
    def test_contract_identity_scope_and_decision_are_schema_only(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertEqual(contract["intake_id"], HUMAN_DECISION_INTAKE_FEATURE_ID)
        self.assertEqual(contract["schema_version"], HUMAN_DECISION_INTAKE_SCHEMA_VERSION)
        self.assertEqual(contract["intake_status"], "schema_only")
        self.assertTrue(contract["declared_human_decision_intake_only"])
        self.assertEqual(contract["decision_scope"], "human_decision_intake_schema_only")
        self.assertEqual(contract["decision_value"], "not_recorded")

    def test_required_prior_milestones_preserve_review_chain(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            REQUIRED_PRIOR_MILESTONES.issubset(set(contract["required_prior_milestones"]))
        )
        for milestone in [
            "v3_closure_shield_frozen",
            "disabled_generation_boundary_frozen",
            "dry_run_artifact_generation_plan_frozen",
            "local_generator_candidate_review_gate_frozen",
            "human_architectural_review_record_frozen",
        ]:
            self.assertIn(milestone, contract["required_prior_milestones"])

    def test_allowed_future_decision_values_do_not_authorize_generation(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            ALLOWED_FUTURE_DECISION_VALUES.issubset(
                set(contract["allowed_future_decision_values"])
            )
        )
        self.assertIn(
            "permit_separate_generator_candidate_proposal_review_only",
            contract["allowed_future_decision_values"],
        )
        self.assertEqual(contract["decision_value"], "not_recorded")

    def test_required_decision_context_sections_are_present(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            REQUIRED_DECISION_CONTEXT_SECTIONS.issubset(
                set(contract["required_decision_context_sections"])
            )
        )
        for section in [
            "privacy_and_redaction_decision_summary",
            "authority_boundary_decision_summary",
            "runtime_boundary_decision_summary",
            "final_decision_placeholder",
        ]:
            self.assertIn(section, contract["required_decision_context_sections"])

    def test_required_evidence_before_future_candidate_is_present(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            REQUIRED_WRITTEN_EVIDENCE_BEFORE_ANY_FUTURE_CANDIDATE.issubset(
                set(contract["required_written_evidence_before_any_future_candidate"])
            )
        )
        self.assertIn(
            "explicit_human_decision_recorded_in_future_governed_patch",
            contract["required_written_evidence_before_any_future_candidate"],
        )
        self.assertIn(
            "human_decision_freeze_entry_written_before_candidate_patch",
            contract["required_written_evidence_before_any_future_candidate"],
        )

    def test_allowed_and_prohibited_outputs_preserve_non_authority(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            REQUIRED_ALLOWED_INTAKE_OUTPUTS.issubset(set(contract["allowed_intake_outputs"]))
        )
        self.assertTrue(
            REQUIRED_PROHIBITED_INTAKE_OUTPUTS.issubset(
                set(contract["prohibited_intake_outputs"])
            )
        )
        for prohibited in [
            "actual_human_decision",
            "generator_candidate_authorization",
            "generated_artifact",
            "embedding_values",
            "runtime_semantic_score",
            "may_proceed_now",
        ]:
            self.assertIn(prohibited, contract["prohibited_intake_outputs"])

    def test_disabled_flags_remain_false(self) -> None:
        contract = build_human_decision_intake_contract()
        flags = contract["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, flags)
            self.assertIs(flags[flag], False)

    def test_no_authority_assertions_and_effect_policy_are_present(self) -> None:
        contract = build_human_decision_intake_contract()
        self.assertTrue(
            REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(
                set(contract["no_authority_assertions"])
            )
        )
        for assertion in [
            "intake_records_no_real_human_decision",
            "intake_must_not_authorize_generator_candidate_patch_by_itself",
            "future_actual_decision_requires_separate_governed_patch",
            "future_generator_candidate_requires_separate_governed_patch_after_decision",
        ]:
            self.assertIn(assertion, contract["no_authority_assertions"])
        self.assertIn(
            "schema_only_intake_has_no_decision_effect",
            contract["decision_effect_policy"],
        )
        self.assertIn(
            "any_request_to_use_intake_as_authority_is_blocked",
            contract["decision_effect_policy"],
        )

    def test_validation_accepts_static_contract_and_authorizes_nothing(self) -> None:
        result = validate_human_decision_intake_contract(
            build_human_decision_intake_contract()
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["decision_value"], "not_recorded")
        self.assertFalse(result["real_human_decision_recorded"])
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

    def test_validation_rejects_forbidden_fields_and_real_decision(self) -> None:
        contract = build_human_decision_intake_contract()
        contract["actual_human_decision"] = "permit_separate_generator_candidate_proposal_review_only"
        contract["decision_value"] = "permit_separate_generator_candidate_proposal_review_only"
        result = validate_human_decision_intake_contract(contract)
        self.assertFalse(result["ok"])
        self.assertIn("forbidden intake fields present", "\n".join(result["errors"]))
        self.assertIn("decision_value must remain not_recorded", "\n".join(result["errors"]))

    def test_classifier_allows_schema_talk_but_blocks_decision_or_generation(self) -> None:
        schema = classify_human_decision_intake_request("prepare human decision intake schema")
        self.assertTrue(schema["allowed_now"])
        self.assertEqual(schema["permitted_output"], "human_decision_intake_schema")
        self.assertEqual(schema["decision_value"], "not_recorded")
        self.assertFalse(schema["real_human_decision_recorded"])
        self.assertFalse(schema["generator_candidate_patch_authorized"])

        blocked = classify_human_decision_intake_request(
            "approve now and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded"])
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
            manifest["human_decision_intake_design_feature_id"],
            "routing_signal_scorer_v3_human_decision_intake_design_v1",
        )
        self.assertEqual(
            manifest["human_decision_intake_design_status"],
            "standard_library_only_decision_intake_schema_no_generator_no_artifact_writing_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["human_decision_intake_schema_version"],
            "3.16-human-decision-intake-design",
        )
        for characteristic in [
            "human_decision_intake_design",
            "human_decision_intake_schema_only",
            "no_actual_human_decision_from_intake",
            "no_generator_candidate_from_decision_intake",
            "no_artifact_generation_from_decision_intake",
            "no_artifact_writing_from_decision_intake",
            "no_artifact_reading_from_decision_intake",
            "no_source_scanning_from_decision_intake",
            "no_raw_text_materialization_from_decision_intake",
            "no_embeddings_from_decision_intake",
            "no_vectors_from_decision_intake",
            "no_provider_execution_from_decision_intake",
            "no_runtime_enablement_from_decision_intake",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_public_contract_and_init_do_not_export_decision_intake(self) -> None:
        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_human_decision_intake_contract",
            "validate_human_decision_intake_contract",
            "classify_human_decision_intake_request",
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

    def test_forbidden_intake_fields_cover_private_and_authority_data(self) -> None:
        for field in [
            "actual_human_decision",
            "approved_generator_candidate",
            "raw_user_query",
            "prompt_text",
            "freeze_entry_text",
            "embedding_values",
            "vector_index",
            "provider_config",
            "final_route",
            "required_prompts",
            "may_proceed_now",
            "authority_granted",
        ]:
            self.assertIn(field, FORBIDDEN_INTAKE_FIELDS)


if __name__ == "__main__":
    unittest.main()
