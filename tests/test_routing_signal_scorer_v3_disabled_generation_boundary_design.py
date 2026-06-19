from __future__ import annotations

import ast
import json
import pathlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.disabled_generation_boundary_design import (
    DISABLED_GENERATION_BOUNDARY_FEATURE_ID,
    DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION,
    FORBIDDEN_AUTHORITY_FIELDS,
    FORBIDDEN_GENERATION_RUNTIME_FIELDS,
    FORBIDDEN_RAW_TEXT_FIELDS,
    REQUIRED_ALLOWED_FUTURE_GENERATION_MODES,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_FORBIDDEN_ACTIONS,
    REQUIRED_FUTURE_GENERATION_GATES,
    REQUIRED_FUTURE_GENERATION_INPUTS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PERMITTED_OUTPUTS,
    build_disabled_generation_boundary_contract,
    classify_generation_activation_request,
    validate_disabled_generation_boundary_contract,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "disabled_generation_boundary_design.py"
DESIGN_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_disabled_generation_boundary_design.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class DisabledGenerationBoundaryDesignTests(unittest.TestCase):
    def test_build_contract_uses_expected_identity_and_schema(self):
        contract = build_disabled_generation_boundary_contract()
        self.assertEqual(contract["contract_id"], DISABLED_GENERATION_BOUNDARY_FEATURE_ID)
        self.assertEqual(contract["schema_version"], DISABLED_GENERATION_BOUNDARY_SCHEMA_VERSION)
        self.assertTrue(contract["declared_design_only"])
        self.assertEqual(contract["generation_boundary_status"], "design_only")
        self.assertEqual(contract["default_generation_mode"], "disabled_no_generation")

    def test_contract_contains_future_modes_inputs_and_gates(self):
        contract = build_disabled_generation_boundary_contract()
        self.assertTrue(REQUIRED_ALLOWED_FUTURE_GENERATION_MODES.issubset(set(contract["allowed_future_generation_modes"])))
        self.assertTrue(REQUIRED_FUTURE_GENERATION_INPUTS.issubset(set(contract["required_future_generation_inputs"])))
        self.assertTrue(REQUIRED_FUTURE_GENERATION_GATES.issubset(set(contract["required_future_generation_gates"])))
        self.assertIn("separate_governed_patch_required", contract["required_future_generation_gates"])
        self.assertIn("freeze_required_before_use", contract["required_future_generation_gates"])

    def test_disabled_flags_are_all_false(self):
        contract = build_disabled_generation_boundary_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_forbidden_actions_cover_generation_runtime_and_authority(self):
        contract = build_disabled_generation_boundary_contract()
        actions = set(contract["forbidden_actions"])
        self.assertTrue(REQUIRED_FORBIDDEN_ACTIONS.issubset(actions))
        for action in [
            "implement_generator_now",
            "generate_artifact_now",
            "write_artifact_now",
            "run_generation_at_startup",
            "run_generation_at_runtime",
            "generate_embeddings",
            "create_vector_index",
            "enable_semantic_runtime",
            "produce_final_route",
            "write_freeze_memory",
        ]:
            self.assertIn(action, actions)

    def test_permitted_outputs_are_review_evidence_only(self):
        contract = build_disabled_generation_boundary_contract()
        outputs = set(contract["permitted_outputs"])
        self.assertTrue(REQUIRED_PERMITTED_OUTPUTS.issubset(outputs))
        self.assertIn("generation_denial_report", outputs)
        self.assertIn("review_evidence_only", outputs)
        self.assertIn("no_artifact_written", outputs)
        self.assertNotIn("generated_artifact", outputs)
        self.assertNotIn("final_route", outputs)

    def test_no_authority_assertions_are_explicit(self):
        contract = build_disabled_generation_boundary_contract()
        assertions = set(contract["no_authority_assertions"])
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(assertions))
        self.assertIn("generator_must_not_choose_route", assertions)
        self.assertIn("generator_must_not_write_freeze_memory", assertions)
        self.assertIn("canon_remains_final_authority", assertions)

    def test_valid_contract_validates_without_authority(self):
        result = validate_disabled_generation_boundary_contract(build_disabled_generation_boundary_contract())
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])
        self.assertFalse(result["artifact_generation_authorized"])
        self.assertFalse(result["artifact_writing_authorized"])
        self.assertFalse(result["startup_generation_authorized"])
        self.assertFalse(result["runtime_generation_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_generation_authorized"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["authority_granted"])
        self.assertTrue(result["review_evidence_only"])
        self.assertTrue(result["requires_future_governed_patch"])

    def test_validator_rejects_missing_required_fields(self):
        contract = build_disabled_generation_boundary_contract()
        del contract["required_future_generation_gates"]
        result = validate_disabled_generation_boundary_contract(contract)
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing required fields" in error for error in result["errors"]))

    def test_validator_rejects_enabled_flags(self):
        for flag in [
            "artifact_generation_enabled",
            "artifact_writing_enabled",
            "startup_generation_enabled",
            "runtime_generation_enabled",
            "embedding_generation_enabled",
            "vector_index_generation_enabled",
            "semantic_runtime_enabled",
            "write_freeze_memory_enabled",
        ]:
            contract = build_disabled_generation_boundary_contract()
            contract["disabled_flags"][flag] = True
            result = validate_disabled_generation_boundary_contract(contract)
            self.assertFalse(result["ok"], flag)
            self.assertIn("disabled flag must be false: " + flag, result["errors"])

    def test_validator_rejects_authority_fields(self):
        for field in FORBIDDEN_AUTHORITY_FIELDS:
            contract = build_disabled_generation_boundary_contract()
            contract[field] = True
            result = validate_disabled_generation_boundary_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(any("forbidden authority fields" in error for error in result["errors"]), field)

    def test_validator_rejects_raw_text_fields(self):
        for field in FORBIDDEN_RAW_TEXT_FIELDS:
            contract = build_disabled_generation_boundary_contract()
            contract[field] = "raw text is forbidden"
            result = validate_disabled_generation_boundary_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(any("forbidden raw/private text fields" in error for error in result["errors"]), field)

    def test_validator_rejects_generation_runtime_fields(self):
        for field in FORBIDDEN_GENERATION_RUNTIME_FIELDS:
            contract = build_disabled_generation_boundary_contract()
            contract[field] = {"forbidden": True}
            result = validate_disabled_generation_boundary_contract(contract)
            self.assertFalse(result["ok"], field)
            self.assertTrue(any("forbidden generation/runtime fields" in error for error in result["errors"]), field)

    def test_activation_requests_never_authorize_generation(self):
        for action in [
            "generate artifact now",
            "write artifact",
            "build artifact at startup",
            "run generation at runtime",
            "generate embeddings",
            "create vector index",
            "enable semantic runtime",
            "auto load prompts",
        ]:
            result = classify_generation_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_generation_authorized"], action)
            self.assertFalse(result["artifact_writing_authorized"], action)
            self.assertFalse(result["startup_generation_authorized"], action)
            self.assertFalse(result["runtime_generation_authorized"], action)
            self.assertFalse(result["embedding_generation_authorized"], action)
            self.assertFalse(result["vector_index_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_disabled_generation_boundary(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Disabled Generation Boundary Design v1",
            "The boundary is intentionally disabled.",
            "This milestone does not authorize any of the following:",
            "artifact generation",
            "embedding generation",
            "Generation is not a runtime capability.",
            "It may never provide authority.",
            "separate governed, validated, and frozen patch",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["disabled_generation_boundary_design_feature_id"],
            "routing_signal_scorer_v3_disabled_generation_boundary_design_v1",
        )
        self.assertEqual(
            manifest["disabled_generation_boundary_design_status"],
            "standard_library_only_disabled_generation_boundary_no_generator_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["disabled_generation_boundary_schema_version"],
            "3.12-disabled-generation-boundary-design",
        )
        self.assertEqual(
            manifest["disabled_generation_boundary_policy"],
            "disabled_generation_only_no_artifact_write_no_embeddings_no_vectors_no_runtime_enablement",
        )
        for characteristic in [
            "disabled_generation_boundary_design",
            "generation_boundary_disabled_only",
            "no_artifact_generator_added",
            "no_artifact_writing_enabled",
            "no_artifact_overwrite_enabled",
            "no_startup_generation_enabled",
            "no_runtime_generation_enabled",
            "no_background_generation_enabled",
            "no_file_watcher_generation_enabled",
            "no_raw_text_materialization_enabled",
            "no_embedding_generation_enabled",
            "no_vector_index_generation_enabled",
            "future_generation_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("build_disabled_generation_boundary_contract", provides)
        self.assertNotIn("validate_disabled_generation_boundary_contract", provides)
        self.assertNotIn("classify_generation_activation_request", provides)
        self.assertNotIn("build_disabled_generation_boundary_contract", CONTRACT.read_text(encoding="utf-8"))
        self.assertNotIn("build_disabled_generation_boundary_contract", INIT.read_text(encoding="utf-8"))

    def test_module_is_standard_library_only_and_has_no_side_effect_calls(self):
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
            "write",
            "read_text",
            "write_text",
            "mkdir",
            "remove",
            "unlink",
            "replace",
            "rename",
            "run",
            "Popen",
            "urlopen",
        ]:
            self.assertNotIn(forbidden_call, calls)

    def test_no_forbidden_runtime_generation_files_exist(self):
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
        for rel_path in forbidden_paths:
            self.assertFalse((ROOT / rel_path).exists(), rel_path)


if __name__ == "__main__":
    unittest.main()
