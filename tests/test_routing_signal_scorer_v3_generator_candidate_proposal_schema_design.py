from __future__ import annotations

import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_proposal_schema_design import (
    ALLOWED_FUTURE_PROPOSAL_VALUES,
    FORBIDDEN_PROPOSAL_SCHEMA_FIELDS,
    GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID,
    GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION,
    REQUIRED_ALLOWED_SCHEMA_OUTPUTS,
    REQUIRED_CANDIDATE_PATCH_CONSTRAINTS,
    REQUIRED_CANDIDATE_PROPOSAL_SECTIONS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_SCHEMA_OUTPUTS,
    REQUIRED_PROPOSAL_EFFECT_POLICY,
    REQUIRED_RECORDED_DECISION_PREREQUISITES,
    REQUIRED_STOP_CONDITIONS,
    build_generator_candidate_proposal_schema_contract,
    classify_generator_candidate_proposal_schema_request,
    validate_generator_candidate_proposal_schema_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v3_generator_candidate_proposal_schema_design.md"
)
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"
ROOT_HINT = ROOT / "KANDA_FREEZE_HINT.json"
MODULE = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "generator_candidate_proposal_schema_design.py"
)


class RoutingSignalScorerV3GeneratorCandidateProposalSchemaDesignTests(unittest.TestCase):
    def test_contract_validates_and_remains_schema_only(self) -> None:
        schema = build_generator_candidate_proposal_schema_contract()
        result = validate_generator_candidate_proposal_schema_contract(schema)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["current_proposal_state"], "not_proposed")
        self.assertFalse(result["real_human_decision_recorded_by_schema"])
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
        schema = build_generator_candidate_proposal_schema_contract()
        self.assertEqual(schema["schema_id"], GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID)
        self.assertEqual(schema["schema_version"], GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION)
        self.assertEqual(schema["current_proposal_state"], "not_proposed")
        self.assertEqual(schema["current_proposal_effect"], "no_effect_schema_only_not_proposed")
        checks = [
            ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
            ("required_recorded_decision_prerequisites", REQUIRED_RECORDED_DECISION_PREREQUISITES),
            ("allowed_future_proposal_values", ALLOWED_FUTURE_PROPOSAL_VALUES),
            ("required_candidate_proposal_sections", REQUIRED_CANDIDATE_PROPOSAL_SECTIONS),
            ("required_candidate_patch_constraints", REQUIRED_CANDIDATE_PATCH_CONSTRAINTS),
            ("allowed_schema_outputs", REQUIRED_ALLOWED_SCHEMA_OUTPUTS),
            ("prohibited_schema_outputs", REQUIRED_PROHIBITED_SCHEMA_OUTPUTS),
            ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
            ("proposal_effect_policy", REQUIRED_PROPOSAL_EFFECT_POLICY),
            ("stop_conditions", REQUIRED_STOP_CONDITIONS),
        ]
        for field, required in checks:
            self.assertTrue(required.issubset(set(schema[field])), field)

    def test_every_disabled_flag_is_false(self) -> None:
        schema = build_generator_candidate_proposal_schema_contract()
        disabled_flags = schema["disabled_flags"]
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, disabled_flags)
            self.assertFalse(disabled_flags[flag], flag)

    def test_forbidden_fields_fail_validation(self) -> None:
        schema = build_generator_candidate_proposal_schema_contract()
        for field in FORBIDDEN_PROPOSAL_SCHEMA_FIELDS:
            mutated = dict(schema)
            mutated[field] = "forbidden"
            result = validate_generator_candidate_proposal_schema_contract(mutated)
            self.assertFalse(result["ok"], field)

    def test_missing_required_sections_fail_validation(self) -> None:
        schema = build_generator_candidate_proposal_schema_contract()
        mutated = dict(schema)
        mutated["required_candidate_proposal_sections"] = []
        result = validate_generator_candidate_proposal_schema_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required_candidate_proposal_sections missing" in e for e in result["errors"]))

    def test_classification_allows_schema_view_only(self) -> None:
        allowed = classify_generator_candidate_proposal_schema_request(
            "show the generator candidate proposal schema checklist design"
        )
        self.assertTrue(allowed["allowed_now"])
        self.assertEqual(allowed["permitted_output"], "generator_candidate_proposal_schema")
        self.assertEqual(allowed["current_proposal_state"], "not_proposed")
        self.assertTrue(allowed["requires_prior_recorded_human_decision"])
        self.assertFalse(allowed["generator_candidate_patch_authorized"])

    def test_classification_blocks_generation_and_candidate_patch_requests(self) -> None:
        blocked = classify_generator_candidate_proposal_schema_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["real_human_decision_recorded_by_schema"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_prior_recorded_human_decision"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_design_doc_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only, schema only, review evidence only",
            "does not create a generator candidate patch",
            "does not authorize generator candidate implementation",
            "not_proposed",
            "another separately governed",
        ]:
            self.assertIn(phrase, doc)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["generator_candidate_proposal_schema_design_feature_id"],
            GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_proposal_schema_version"],
            GENERATOR_CANDIDATE_PROPOSAL_SCHEMA_VERSION,
        )
        for characteristic in [
            "generator_candidate_proposal_schema_design",
            "generator_candidate_proposal_schema_only",
            "no_generator_candidate_patch_from_proposal_schema",
            "no_generator_authorization_from_proposal_schema",
            "no_artifact_generation_from_proposal_schema",
            "no_artifact_writing_from_proposal_schema",
            "no_artifact_reading_from_proposal_schema",
            "no_source_scanning_from_proposal_schema",
            "no_raw_text_materialization_from_proposal_schema",
            "no_embeddings_from_proposal_schema",
            "no_vectors_from_proposal_schema",
            "no_provider_execution_from_proposal_schema",
            "no_runtime_enablement_from_proposal_schema",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_generator_candidate_proposal_schema_contract",
            "validate_generator_candidate_proposal_schema_contract",
            "classify_generator_candidate_proposal_schema_request",
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
