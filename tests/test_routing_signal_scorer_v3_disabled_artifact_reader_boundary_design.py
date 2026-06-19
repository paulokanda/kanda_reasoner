from __future__ import annotations

import ast
import json
import pathlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.disabled_artifact_reader_boundary_design import (
    DISABLED_ARTIFACT_READER_FEATURE_ID,
    DISABLED_ARTIFACT_READER_SCHEMA_VERSION,
    FORBIDDEN_AUTHORITY_FIELDS,
    FORBIDDEN_RAW_TEXT_FIELDS,
    FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS,
    REQUIRED_ARTIFACT_SOURCE_REQUIREMENTS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_FORBIDDEN_ACTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PERMITTED_OUTPUTS,
    REQUIRED_READER_GATES,
    build_disabled_artifact_reader_boundary_contract,
    classify_artifact_reader_activation_request,
    validate_disabled_artifact_reader_boundary_contract,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "disabled_artifact_reader_boundary_design.py"
DESIGN_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_disabled_artifact_reader_boundary_design.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class DisabledArtifactReaderBoundaryDesignTests(unittest.TestCase):
    def test_build_contract_uses_expected_identity_and_schema(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        self.assertEqual(contract["contract_id"], DISABLED_ARTIFACT_READER_FEATURE_ID)
        self.assertEqual(contract["schema_version"], DISABLED_ARTIFACT_READER_SCHEMA_VERSION)
        self.assertTrue(contract["declared_design_only"])
        self.assertEqual(contract["reader_design_status"], "design_only")

    def test_contract_contains_required_source_requirements_and_gates(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        self.assertTrue(REQUIRED_ARTIFACT_SOURCE_REQUIREMENTS.issubset(set(contract["artifact_source_requirements"])))
        self.assertTrue(REQUIRED_READER_GATES.issubset(set(contract["required_reader_gates"])))
        self.assertIn("artifact_must_exclude_raw_text", contract["artifact_source_requirements"])
        self.assertIn("manual_invocation_required", contract["required_reader_gates"])
        self.assertIn("no_runtime_enablement_check_required", contract["required_reader_gates"])

    def test_disabled_flags_are_all_false(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_forbidden_actions_cover_runtime_loading_and_authority(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        actions = set(contract["forbidden_actions"])
        self.assertTrue(REQUIRED_FORBIDDEN_ACTIONS.issubset(actions))
        for action in [
            "implement_artifact_reader",
            "load_artifact_at_startup",
            "load_artifact_at_runtime",
            "materialize_raw_text",
            "materialize_vector_values",
            "enable_semantic_runtime",
            "produce_final_route",
            "write_freeze_memory",
        ]:
            self.assertIn(action, actions)

    def test_permitted_outputs_are_review_evidence_only(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        outputs = set(contract["permitted_outputs"])
        self.assertTrue(REQUIRED_PERMITTED_OUTPUTS.issubset(outputs))
        self.assertIn("review_evidence_only", outputs)
        self.assertIn("no_runtime_enablement", outputs)
        self.assertNotIn("final_route", outputs)
        self.assertNotIn("required_prompts", outputs)

    def test_no_authority_assertions_are_explicit(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        assertions = set(contract["no_authority_assertions"])
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(assertions))
        self.assertIn("reader_must_not_choose_route", assertions)
        self.assertIn("reader_must_not_write_freeze_memory", assertions)
        self.assertIn("canon_remains_final_authority", assertions)

    def test_valid_contract_validates_without_authority(self):
        result = validate_disabled_artifact_reader_boundary_contract(build_disabled_artifact_reader_boundary_contract())
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["advisory_only"])
        self.assertTrue(result["review_evidence_only"])
        self.assertFalse(result["artifact_reader_enabled"])
        self.assertFalse(result["startup_loading_enabled"])
        self.assertFalse(result["runtime_loading_enabled"])
        self.assertFalse(result["semantic_runtime_enabled"])
        self.assertFalse(result["authority_granted"])
        self.assertTrue(result["requires_future_governed_patch"])

    def test_validator_rejects_missing_required_fields(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        del contract["required_reader_gates"]
        result = validate_disabled_artifact_reader_boundary_contract(contract)
        self.assertFalse(result["valid"])
        self.assertTrue(any("missing required fields" in err for err in result["errors"]))

    def test_validator_rejects_enabled_flags(self):
        contract = build_disabled_artifact_reader_boundary_contract()
        contract["disabled_flags"]["runtime_artifact_loading_enabled"] = True
        result = validate_disabled_artifact_reader_boundary_contract(contract)
        self.assertFalse(result["valid"])
        self.assertIn("disabled flag must be false: runtime_artifact_loading_enabled", result["errors"])

    def test_validator_rejects_authority_fields(self):
        for field in FORBIDDEN_AUTHORITY_FIELDS:
            contract = build_disabled_artifact_reader_boundary_contract()
            contract[field] = True
            result = validate_disabled_artifact_reader_boundary_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_validator_rejects_raw_text_fields(self):
        for field in FORBIDDEN_RAW_TEXT_FIELDS:
            contract = build_disabled_artifact_reader_boundary_contract()
            contract[field] = "secret text"
            result = validate_disabled_artifact_reader_boundary_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_validator_rejects_vector_provider_runtime_fields(self):
        for field in FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS:
            contract = build_disabled_artifact_reader_boundary_contract()
            contract[field] = {"forbidden": True}
            result = validate_disabled_artifact_reader_boundary_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_activation_requests_are_denied(self):
        for action in [
            "enable artifact reader",
            "load artifact at startup",
            "load artifact at runtime",
            "read artifact automatically",
            "materialize vector values",
            "enable semantic runtime",
            "produce route",
        ]:
            result = classify_artifact_reader_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["artifact_reader_authorized"], action)
            self.assertFalse(result["artifact_loading_authorized"], action)
            self.assertFalse(result["raw_text_materialization_authorized"], action)
            self.assertFalse(result["vector_materialization_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["authority_granted"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_reader_boundary_rules(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Disabled Artifact Reader Boundary Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "This design does not authorize artifact reader implementation.",
            "This design does not authorize artifact loading at startup.",
            "This design does not authorize artifact loading at runtime.",
            "This design does not authorize raw text materialization.",
            "This design does not authorize vector materialization.",
            "This design does not authorize semantic runtime enablement.",
            "This phase adds no external dependency.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["disabled_artifact_reader_boundary_design_feature_id"],
            "routing_signal_scorer_v3_disabled_artifact_reader_boundary_design_v1",
        )
        self.assertEqual(
            manifest["disabled_artifact_reader_boundary_design_status"],
            "standard_library_only_disabled_reader_boundary_no_reader_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["disabled_artifact_reader_boundary_schema_version"],
            "3.9-disabled-artifact-reader-boundary-design",
        )
        self.assertEqual(
            manifest["disabled_artifact_reader_boundary_policy"],
            "disabled_boundary_only_no_startup_loading_no_runtime_loading_no_raw_text_no_vectors_no_runtime_enablement",
        )
        for characteristic in [
            "disabled_artifact_reader_boundary_design",
            "artifact_reader_design_disabled_only",
            "no_artifact_reader_implementation_added",
            "no_artifact_reader_enabled",
            "no_startup_artifact_loading",
            "no_runtime_artifact_loading",
            "no_background_artifact_loading",
            "no_file_watcher_artifact_loading",
            "no_artifact_auto_discovery",
            "no_artifact_auto_refresh",
            "artifact_reader_schema_validation_only",
            "artifact_reader_no_raw_text_materialization",
            "artifact_reader_no_vector_materialization",
            "artifact_reader_review_evidence_only",
            "artifact_reader_no_runtime_enablement",
            "artifact_reader_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])
        provides = manifest["public_contract"]["provides_functions"]
        self.assertNotIn("validate_disabled_artifact_reader_boundary_contract", provides)
        self.assertNotIn("build_disabled_artifact_reader_boundary_contract", provides)

    def test_module_is_stdlib_only_and_does_not_import_neighbor_boxes(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_roots = set()
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name)
                    imported_roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
                imported_roots.add(node.module.split(".")[0])
        forbidden_roots = {
            "numpy", "pandas", "sklearn", "scipy", "torch", "tensorflow",
            "sentence_transformers", "transformers", "faiss", "chromadb",
            "qdrant_client", "langchain", "llama_index",
        }
        self.assertTrue(forbidden_roots.isdisjoint(imported_roots))
        for forbidden in [
            "kanda_prompt_workspace",
            "project_freeze_ledger",
            "project_freeze_after_update",
            "kanda_reasoner_app.freeze_hint_intake",
            "kanda_reasoner_app.freeze_after_update",
            "kanda_reasoner_app.freeze_after_update_gui",
        ]:
            self.assertNotIn(forbidden, imported_modules)

    def test_no_forbidden_runtime_artifacts_are_added(self):
        forbidden_paths = [
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "artifact_reader.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "precomputed_artifact_generator.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "evaluation_runner.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "semantic_provider.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), str(path))

    def test_contract_and_init_are_not_exporting_design_helpers(self):
        contract_text = CONTRACT.read_text(encoding="utf-8") if CONTRACT.exists() else ""
        init_text = INIT.read_text(encoding="utf-8") if INIT.exists() else ""
        self.assertNotIn("disabled_artifact_reader_boundary_design", contract_text)
        self.assertNotIn("disabled_artifact_reader_boundary_design", init_text)
        self.assertNotIn("validate_disabled_artifact_reader_boundary_contract", contract_text)
        self.assertNotIn("validate_disabled_artifact_reader_boundary_contract", init_text)


if __name__ == "__main__":
    unittest.main()
