from __future__ import annotations

import ast
import json
import pathlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.local_generator_candidate_review_gate_design import (
    FORBIDDEN_GATE_FIELDS,
    LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_FEATURE_ID,
    LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_SCHEMA_VERSION,
    REQUIRED_ALLOWED_REVIEW_OUTPUTS,
    REQUIRED_CANDIDATE_SCOPE,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_EVIDENCE_BEFORE_CANDIDATE_PATCH,
    REQUIRED_FORBIDDEN_ACTIONS,
    REQUIRED_HUMAN_DECISIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PERMANENT_BLOCKERS,
    REQUIRED_PREREQUISITES,
    build_local_generator_candidate_review_gate_contract,
    classify_local_generator_candidate_review_request,
    validate_local_generator_candidate_review_gate_contract,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
MODULE_PATH = BOX / "local_generator_candidate_review_gate_design.py"
DESIGN_DOC = BOX / "design" / "routing_signal_scorer_v3_local_generator_candidate_review_gate_design.md"
MANIFEST = BOX / "box_manifest.json"
CONTRACT = BOX / "contract.py"
INIT = BOX / "__init__.py"


class LocalGeneratorCandidateReviewGateDesignTests(unittest.TestCase):
    def test_build_gate_uses_expected_identity_schema_and_scope(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        self.assertEqual(contract["gate_id"], LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_FEATURE_ID)
        self.assertEqual(contract["schema_version"], LOCAL_GENERATOR_CANDIDATE_REVIEW_GATE_SCHEMA_VERSION)
        self.assertEqual(contract["gate_status"], "review_only")
        self.assertTrue(contract["declared_review_only"])
        self.assertEqual(contract["candidate_scope"], REQUIRED_CANDIDATE_SCOPE)

    def test_required_prerequisites_preserve_frozen_prior_boundaries(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        prerequisites = set(contract["required_prerequisites"])
        self.assertTrue(REQUIRED_PREREQUISITES.issubset(prerequisites))
        for item in [
            "v3_closure_shield_frozen",
            "disabled_generation_boundary_frozen",
            "dry_run_artifact_generation_plan_frozen",
            "freeze_hint_state_machine_regressions_passing",
            "runtime_lite_advisory_only_regressions_passing",
        ]:
            self.assertIn(item, prerequisites)

    def test_allowed_outputs_are_review_evidence_only(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        outputs = set(contract["allowed_review_outputs"])
        self.assertTrue(REQUIRED_ALLOWED_REVIEW_OUTPUTS.issubset(outputs))
        self.assertIn("candidate_readiness_summary", outputs)
        self.assertIn("candidate_risk_register", outputs)
        self.assertIn("human_review_queue_only", outputs)
        self.assertIn("review_evidence_only", outputs)
        self.assertIn("no_artifact_generated", outputs)
        self.assertIn("no_artifact_written", outputs)
        self.assertIn("no_runtime_enablement", outputs)

    def test_required_human_decisions_and_evidence_before_candidate_patch(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        self.assertTrue(REQUIRED_HUMAN_DECISIONS.issubset(set(contract["required_human_decisions"])))
        self.assertTrue(
            REQUIRED_EVIDENCE_BEFORE_CANDIDATE_PATCH.issubset(
                set(contract["required_evidence_before_candidate_patch"])
            )
        )
        self.assertIn(
            "decide_whether_generator_candidate_is_allowed_to_be_proposed",
            contract["required_human_decisions"],
        )
        self.assertIn(
            "human_confirmation_of_candidate_scope",
            contract["required_evidence_before_candidate_patch"],
        )

    def test_disabled_flags_forbid_generation_and_runtime_enablement(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        flags = contract["disabled_flags"]
        self.assertTrue(REQUIRED_DISABLED_FLAGS_FALSE.issubset(flags.keys()))
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIs(flags[flag], False, flag)
        for flag in [
            "generator_candidate_patch_authorized",
            "artifact_generation_enabled",
            "artifact_writing_enabled",
            "source_scanning_enabled",
            "raw_text_materialization_enabled",
            "embedding_generation_enabled",
            "provider_execution_enabled",
            "semantic_runtime_enabled",
            "prompt_router_mutation_enabled",
        ]:
            self.assertFalse(flags[flag])

    def test_forbidden_actions_and_no_authority_assertions_are_complete(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        self.assertTrue(REQUIRED_FORBIDDEN_ACTIONS.issubset(set(contract["forbidden_actions"])))
        self.assertTrue(
            REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(set(contract["no_authority_assertions"]))
        )
        self.assertIn("create_generator_candidate_patch_from_review_gate", contract["forbidden_actions"])
        self.assertIn("generate_artifact_from_review_gate", contract["forbidden_actions"])
        self.assertIn("review_gate_must_not_authorize_generator_candidate_patch_by_itself", contract["no_authority_assertions"])
        self.assertIn("canon_remains_final_authority", contract["no_authority_assertions"])

    def test_permanent_blockers_stop_shortcuts_to_generation(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        blockers = set(contract["permanent_blockers"])
        self.assertTrue(REQUIRED_PERMANENT_BLOCKERS.issubset(blockers))
        for blocker in [
            "request_to_generate_now",
            "request_to_write_artifacts_now",
            "request_to_scan_sources_now",
            "request_to_materialize_raw_text_now",
            "request_to_generate_embeddings_now",
            "request_to_enable_runtime_semantics_now",
            "request_to_modify_router_authority_now",
            "request_to_bypass_future_governed_patch",
        ]:
            self.assertIn(blocker, blockers)

    def test_validator_accepts_default_contract_and_denies_authority(self) -> None:
        contract = build_local_generator_candidate_review_gate_contract()
        result = validate_local_generator_candidate_review_gate_contract(contract)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["generator_candidate_patch_authorized"])
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["artifact_writing_authorized"])
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
        contract = build_local_generator_candidate_review_gate_contract()
        del contract["disabled_flags"]["artifact_generation_enabled"]
        result = validate_local_generator_candidate_review_gate_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("required disabled flags must be false" in error for error in result["errors"]))

    def test_validator_rejects_forbidden_fields(self) -> None:
        for field in sorted(FORBIDDEN_GATE_FIELDS):
            contract = build_local_generator_candidate_review_gate_contract()
            contract[field] = "forbidden"
            result = validate_local_generator_candidate_review_gate_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(any("forbidden gate fields present" in error for error in result["errors"]), field)

    def test_request_classifier_allows_review_only_but_denies_generation(self) -> None:
        review = classify_local_generator_candidate_review_request("review candidate risk checklist")
        self.assertTrue(review["allowed_now"])
        self.assertEqual(review["permitted_output"], "candidate_readiness_summary")
        self.assertTrue(review["review_evidence_only"])
        self.assertFalse(review["generator_candidate_patch_authorized"])
        self.assertTrue(review["requires_future_governed_patch_for_generation"])

        for action in [
            "generate artifact now",
            "write artifact from review gate",
            "scan source for generation",
            "materialize raw text",
            "create embeddings",
            "create vector index",
            "enable provider runtime",
            "modify router authority",
            "bypass the future patch",
        ]:
            result = classify_local_generator_candidate_review_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_generation_authorized"], action)
            self.assertFalse(result["artifact_writing_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_index_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["authority_granted"], action)
            self.assertTrue(result["requires_future_governed_patch_for_generation"], action)

    def test_design_doc_preserves_review_gate_only_boundary(self) -> None:
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1",
            "review-only gate",
            "It is not a generator.",
            "The review gate cannot authorize generation.",
            "Future generator work still requires a separate",
            "Do not implement artifact generation",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_runtime_export(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["local_generator_candidate_review_gate_design_feature_id"],
            "routing_signal_scorer_v3_local_generator_candidate_review_gate_design_v1",
        )
        self.assertEqual(
            manifest["local_generator_candidate_review_gate_design_status"],
            "standard_library_only_review_gate_design_no_generator_no_artifact_writing_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["local_generator_candidate_review_gate_schema_version"],
            "3.14-local-generator-candidate-review-gate-design",
        )
        for characteristic in [
            "local_generator_candidate_review_gate_design",
            "review_gate_only_no_generator_candidate_patch_authorized",
            "no_artifact_generation_from_review_gate",
            "no_artifact_writing_from_review_gate",
            "no_source_scanning_from_review_gate",
            "no_raw_text_materialization_from_review_gate",
            "no_embeddings_from_review_gate",
            "no_vectors_from_review_gate",
            "no_provider_execution_from_review_gate",
            "no_runtime_enablement_from_review_gate",
            "future_generator_candidate_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("build_local_generator_candidate_review_gate_contract", provides)
        self.assertNotIn("validate_local_generator_candidate_review_gate_contract", provides)
        self.assertNotIn("classify_local_generator_candidate_review_request", provides)
        self.assertNotIn("build_local_generator_candidate_review_gate_contract", CONTRACT.read_text(encoding="utf-8"))
        self.assertNotIn("build_local_generator_candidate_review_gate_contract", INIT.read_text(encoding="utf-8"))

    def test_module_is_standard_library_only_and_has_no_side_effect_calls(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imports = []
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
                elif isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
        for imported in imports:
            self.assertTrue(
                imported.startswith("__future__")
                or imported.startswith("collections")
                or imported.startswith("typing"),
                imported,
            )
        for forbidden_call in [
            "open",
            "write_text",
            "read_text",
            "mkdir",
            "unlink",
            "replace",
            "rename",
            "rglob",
            "glob",
            "scandir",
            "listdir",
            "system",
            "run",
            "Popen",
        ]:
            self.assertNotIn(forbidden_call, calls)

    def test_no_runtime_generation_paths_or_root_freeze_hint_exist(self) -> None:
        for relative in [
            "artifact_generator.py",
            "precomputed_artifact_generator.py",
            "precomputed_semantic_evidence_artifact_generator.py",
            "generated_artifacts",
            "artifacts",
            "vector_index.py",
            "indices",
            "providers",
        ]:
            self.assertFalse((BOX / relative).exists(), relative)
        self.assertFalse((ROOT / "KANDA_FREEZE_HINT.json").exists())


if __name__ == "__main__":
    unittest.main()
