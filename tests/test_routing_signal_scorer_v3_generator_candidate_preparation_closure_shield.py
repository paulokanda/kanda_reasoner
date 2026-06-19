from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.routing_signal_scorer.generator_candidate_preparation_closure_shield import (
    GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID,
    GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION,
    REQUIRED_ALLOWED_CLOSURE_OUTPUTS,
    REQUIRED_CLOSURE_CHECKS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_KBSC_CLOSURE_DIMENSIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PREPARATION_CLOSURE_SHIELD_FIELDS,
    REQUIRED_PRIOR_MILESTONES,
    REQUIRED_PROHIBITED_CLOSURE_OUTPUTS,
    REQUIRED_STOP_CONDITIONS,
    build_generator_candidate_preparation_closure_shield_contract,
    classify_generator_candidate_preparation_closure_shield_request,
    validate_generator_candidate_preparation_closure_shield_contract,
)

MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_generator_candidate_preparation_closure_shield.md"
CONTRACT = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class GeneratorCandidatePreparationClosureShieldTests(unittest.TestCase):
    def test_contract_validates(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        result = validate_generator_candidate_preparation_closure_shield_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(
            result["schema_id"],
            GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID,
        )
        self.assertEqual(
            result["schema_version"],
            GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION,
        )
        self.assertEqual(
            result["current_preparation_closure_state"],
            "preparation_closure_shield_schema_only",
        )
        self.assertTrue(result["kbsc_preparation_chain_closure_declared"])
        self.assertTrue(result["preparation_chain_closed_for_current_phase"])
        self.assertTrue(result["requires_prior_generator_candidate_review_bundle"])
        self.assertTrue(result["requires_future_governed_candidate_patch"])
        self.assertTrue(result["requires_future_governed_generation_patch"])

    def test_contract_has_required_schema_sections(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        for field in REQUIRED_PREPARATION_CLOSURE_SHIELD_FIELDS:
            self.assertIn(field, contract)

    def test_required_prior_and_closure_sets_are_present(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        checks = [
            ("required_prior_milestones", REQUIRED_PRIOR_MILESTONES),
            ("kbsc_closure_dimensions", REQUIRED_KBSC_CLOSURE_DIMENSIONS),
            ("required_closure_checks", REQUIRED_CLOSURE_CHECKS),
            ("allowed_closure_outputs", REQUIRED_ALLOWED_CLOSURE_OUTPUTS),
            ("prohibited_closure_outputs", REQUIRED_PROHIBITED_CLOSURE_OUTPUTS),
            ("no_authority_assertions", REQUIRED_NO_AUTHORITY_ASSERTIONS),
            ("stop_conditions", REQUIRED_STOP_CONDITIONS),
        ]
        for field, required in checks:
            self.assertTrue(required.issubset(set(contract[field])), field)

    def test_every_disabled_flag_is_false(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_missing_required_field_fails_validation(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        mutated = dict(contract)
        mutated.pop("kbsc_closure_dimensions")
        result = validate_generator_candidate_preparation_closure_shield_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing required field" in error for error in result["errors"]))

    def test_forbidden_output_field_fails_validation(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        mutated = dict(contract)
        mutated["generator_candidate_patch"] = "forbidden"
        result = validate_generator_candidate_preparation_closure_shield_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden closure field" in error for error in result["errors"]))

    def test_enabled_flag_fails_validation(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        mutated = dict(contract)
        flags = dict(mutated["disabled_flags"])
        flags["artifact_generation_enabled"] = True
        mutated["disabled_flags"] = flags
        result = validate_generator_candidate_preparation_closure_shield_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("disabled flag must be false" in error for error in result["errors"]))

    def test_empty_required_lists_fail_validation(self) -> None:
        contract = build_generator_candidate_preparation_closure_shield_contract()
        mutated = dict(contract)
        mutated["required_closure_checks"] = []
        result = validate_generator_candidate_preparation_closure_shield_contract(mutated)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required_closure_checks missing" in error for error in result["errors"]))

    def test_classification_allows_schema_view_only(self) -> None:
        allowed = classify_generator_candidate_preparation_closure_shield_request(
            "show the generator candidate preparation closure shield kbsc summary schema"
        )
        self.assertTrue(allowed["allowed_now"])
        self.assertEqual(
            allowed["permitted_output"],
            "generator_candidate_preparation_closure_shield_schema",
        )
        self.assertEqual(
            allowed["current_preparation_closure_state"],
            "preparation_closure_shield_schema_only",
        )
        self.assertTrue(allowed["requires_prior_generator_candidate_review_bundle"])
        self.assertFalse(allowed["generator_candidate_patch_authorized"])

    def test_classification_blocks_candidate_patch_and_generation_requests(self) -> None:
        blocked = classify_generator_candidate_preparation_closure_shield_request(
            "approve now create candidate patch and generate artifact with embeddings"
        )
        self.assertFalse(blocked["allowed_now"])
        self.assertFalse(blocked["generator_candidate_patch_created"])
        self.assertFalse(blocked["generator_candidate_patch_authorized"])
        self.assertFalse(blocked["artifact_generation_authorized"])
        self.assertTrue(blocked["requires_prior_generator_candidate_review_bundle"])
        self.assertTrue(blocked["requires_future_governed_candidate_patch"])
        self.assertTrue(blocked["requires_future_governed_generation_patch"])

    def test_design_doc_preserves_boundary(self) -> None:
        doc = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "design only",
            "schema only",
            "does not create a generator candidate patch",
            "does not authorize a generator candidate",
            "preparation_closure_shield_schema_only",
            "another separately governed patch",
        ]:
            self.assertIn(phrase, doc)

    def test_manifest_public_contract_and_runtime_paths_are_safe(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.20.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["generator_candidate_preparation_closure_shield_feature_id"],
            GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_FEATURE_ID,
        )
        self.assertEqual(
            manifest["generator_candidate_preparation_closure_shield_schema_version"],
            GENERATOR_CANDIDATE_PREPARATION_CLOSURE_SHIELD_SCHEMA_VERSION,
        )
        for characteristic in [
            "generator_candidate_preparation_closure_shield",
            "generator_candidate_preparation_closure_shield_only",
            "kbsc_preparation_chain_closure",
            "no_candidate_patch_from_preparation_closure_shield",
            "no_generator_authorization_from_preparation_closure_shield",
            "no_artifact_generation_from_preparation_closure_shield",
            "no_artifact_writing_from_preparation_closure_shield",
            "no_artifact_reading_from_preparation_closure_shield",
            "no_source_scanning_from_preparation_closure_shield",
            "no_raw_text_materialization_from_preparation_closure_shield",
            "no_embeddings_from_preparation_closure_shield",
            "no_vectors_from_preparation_closure_shield",
            "no_provider_execution_from_preparation_closure_shield",
            "no_runtime_enablement_from_preparation_closure_shield",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        for forbidden in [
            "build_generator_candidate_preparation_closure_shield_contract",
            "validate_generator_candidate_preparation_closure_shield_contract",
            "classify_generator_candidate_preparation_closure_shield_request",
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
            self.assertFalse((PROJECT_ROOT / forbidden_path).exists(), forbidden_path)

    def test_no_runtime_authority_flags_are_false(self) -> None:
        result = validate_generator_candidate_preparation_closure_shield_contract(
            build_generator_candidate_preparation_closure_shield_contract()
        )
        for key in [
            "real_human_decision_recorded_by_preparation_closure_shield",
            "dependency_install_authorized",
            "side_effect_authorized",
            "generator_candidate_patch_created",
            "generator_candidate_patch_authorized",
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
            "public_runtime_export_authorized",
        ]:
            self.assertFalse(result[key], key)


if __name__ == "__main__":
    unittest.main()
