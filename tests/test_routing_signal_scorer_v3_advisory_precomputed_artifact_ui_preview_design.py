from __future__ import annotations

import ast
import json
import pathlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.advisory_precomputed_artifact_ui_preview_design import (
    ADVISORY_ARTIFACT_UI_PREVIEW_FEATURE_ID,
    ADVISORY_ARTIFACT_UI_PREVIEW_SCHEMA_VERSION,
    FORBIDDEN_AUTHORITY_FIELDS,
    FORBIDDEN_RAW_TEXT_FIELDS,
    FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS,
    REQUIRED_DISABLED_FLAGS_FALSE,
    REQUIRED_DISPLAY_GATES,
    REQUIRED_DISPLAY_SECTIONS,
    REQUIRED_FORBIDDEN_ACTIONS,
    REQUIRED_NO_AUTHORITY_ASSERTIONS,
    REQUIRED_PERMITTED_OUTPUTS,
    REQUIRED_SOURCE_REQUIREMENTS,
    build_advisory_artifact_ui_preview_contract,
    classify_artifact_ui_preview_activation_request,
    validate_advisory_artifact_ui_preview_contract,
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "advisory_precomputed_artifact_ui_preview_design.py"
DESIGN_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
CONTRACT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
INIT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "__init__.py"


class AdvisoryPrecomputedArtifactUiPreviewDesignTests(unittest.TestCase):
    def test_build_contract_uses_expected_identity_and_schema(self):
        contract = build_advisory_artifact_ui_preview_contract()
        self.assertEqual(contract["contract_id"], ADVISORY_ARTIFACT_UI_PREVIEW_FEATURE_ID)
        self.assertEqual(contract["schema_version"], ADVISORY_ARTIFACT_UI_PREVIEW_SCHEMA_VERSION)
        self.assertTrue(contract["declared_design_only"])
        self.assertEqual(contract["preview_design_status"], "design_only")

    def test_contract_contains_required_source_requirements(self):
        contract = build_advisory_artifact_ui_preview_contract()
        self.assertTrue(REQUIRED_SOURCE_REQUIREMENTS.issubset(set(contract["source_requirements"])))
        self.assertIn("disabled_artifact_reader_boundary_must_be_frozen", contract["source_requirements"])
        self.assertIn("artifact_must_exclude_raw_text", contract["source_requirements"])
        self.assertIn("artifact_must_exclude_vector_values", contract["source_requirements"])

    def test_contract_contains_required_display_sections_and_gates(self):
        contract = build_advisory_artifact_ui_preview_contract()
        self.assertTrue(REQUIRED_DISPLAY_SECTIONS.issubset(set(contract["display_sections"])))
        self.assertTrue(REQUIRED_DISPLAY_GATES.issubset(set(contract["display_gates"])))
        self.assertIn("no_authority_banner", contract["display_sections"])
        self.assertIn("disabled_runtime_banner", contract["display_sections"])
        self.assertIn("manual_preview_invocation_required", contract["display_gates"])
        self.assertIn("display_redaction_check_required", contract["display_gates"])

    def test_disabled_flags_are_all_false(self):
        contract = build_advisory_artifact_ui_preview_contract()
        for flag in REQUIRED_DISABLED_FLAGS_FALSE:
            self.assertIn(flag, contract["disabled_flags"])
            self.assertFalse(contract["disabled_flags"][flag], flag)

    def test_forbidden_actions_cover_ui_artifact_loading_and_authority(self):
        contract = build_advisory_artifact_ui_preview_contract()
        actions = set(contract["forbidden_actions"])
        self.assertTrue(REQUIRED_FORBIDDEN_ACTIONS.issubset(actions))
        for action in [
            "implement_ui_preview",
            "read_artifact_for_display",
            "load_artifact_at_startup",
            "display_raw_text",
            "display_vector_values",
            "enable_semantic_runtime",
            "produce_final_route",
            "write_freeze_memory",
        ]:
            self.assertIn(action, actions)

    def test_permitted_outputs_are_review_evidence_only(self):
        contract = build_advisory_artifact_ui_preview_contract()
        outputs = set(contract["permitted_outputs"])
        self.assertTrue(REQUIRED_PERMITTED_OUTPUTS.issubset(outputs))
        self.assertIn("redacted_metadata_summary_only", outputs)
        self.assertIn("review_evidence_only", outputs)
        self.assertIn("no_runtime_enablement", outputs)
        self.assertNotIn("final_route", outputs)
        self.assertNotIn("required_prompts", outputs)

    def test_no_authority_assertions_are_explicit(self):
        contract = build_advisory_artifact_ui_preview_contract()
        assertions = set(contract["no_authority_assertions"])
        self.assertTrue(REQUIRED_NO_AUTHORITY_ASSERTIONS.issubset(assertions))
        self.assertIn("preview_must_not_choose_route", assertions)
        self.assertIn("preview_must_not_write_freeze_memory", assertions)
        self.assertIn("canon_remains_final_authority", assertions)

    def test_valid_contract_validates_without_authority(self):
        result = validate_advisory_artifact_ui_preview_contract(build_advisory_artifact_ui_preview_contract())
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["advisory_only"])
        self.assertTrue(result["review_evidence_only"])
        self.assertFalse(result["ui_preview_enabled"])
        self.assertFalse(result["artifact_reader_enabled"])
        self.assertFalse(result["artifact_loading_enabled"])
        self.assertFalse(result["raw_text_materialization_enabled"])
        self.assertFalse(result["vector_materialization_enabled"])
        self.assertFalse(result["semantic_runtime_enabled"])
        self.assertFalse(result["authority_granted"])
        self.assertTrue(result["requires_future_governed_patch"])

    def test_validator_rejects_missing_required_fields(self):
        contract = build_advisory_artifact_ui_preview_contract()
        del contract["display_gates"]
        result = validate_advisory_artifact_ui_preview_contract(contract)
        self.assertFalse(result["valid"])
        self.assertTrue(any("missing required fields" in err for err in result["errors"]))

    def test_validator_rejects_enabled_flags(self):
        contract = build_advisory_artifact_ui_preview_contract()
        contract["disabled_flags"]["ui_preview_enabled"] = True
        result = validate_advisory_artifact_ui_preview_contract(contract)
        self.assertFalse(result["valid"])
        self.assertIn("disabled flag must be false: ui_preview_enabled", result["errors"])

    def test_validator_rejects_authority_fields(self):
        for field in FORBIDDEN_AUTHORITY_FIELDS:
            contract = build_advisory_artifact_ui_preview_contract()
            contract[field] = True
            result = validate_advisory_artifact_ui_preview_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_validator_rejects_raw_text_fields(self):
        for field in FORBIDDEN_RAW_TEXT_FIELDS:
            contract = build_advisory_artifact_ui_preview_contract()
            contract[field] = "secret text"
            result = validate_advisory_artifact_ui_preview_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_validator_rejects_vector_provider_runtime_fields(self):
        for field in FORBIDDEN_VECTOR_PROVIDER_RUNTIME_FIELDS:
            contract = build_advisory_artifact_ui_preview_contract()
            contract[field] = {"forbidden": True}
            result = validate_advisory_artifact_ui_preview_contract(contract)
            self.assertFalse(result["valid"], field)
            self.assertTrue(any("forbidden field present" in err for err in result["errors"]), field)

    def test_activation_requests_are_denied(self):
        for action in [
            "enable UI preview",
            "display artifact summary",
            "read artifact for display",
            "load artifact at startup",
            "display raw text",
            "display vector values",
            "enable semantic runtime",
            "produce route",
        ]:
            result = classify_artifact_ui_preview_activation_request(action)
            self.assertFalse(result["allowed_now"], action)
            self.assertFalse(result["ui_preview_authorized"], action)
            self.assertFalse(result["artifact_reader_authorized"], action)
            self.assertFalse(result["artifact_loading_authorized"], action)
            self.assertFalse(result["raw_text_materialization_authorized"], action)
            self.assertFalse(result["vector_materialization_authorized"], action)
            self.assertFalse(result["provider_execution_authorized"], action)
            self.assertFalse(result["semantic_runtime_authorized"], action)
            self.assertFalse(result["authority_granted"], action)
            self.assertTrue(result["requires_future_governed_patch"], action)
            self.assertTrue(result["advisory_only"], action)

    def test_design_document_preserves_ui_preview_boundary_rules(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Advisory Precomputed Artifact UI Preview Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "This design does not authorize UI preview implementation.",
            "This design does not authorize artifact reading for display.",
            "This design does not authorize artifact loading at startup.",
            "This design does not authorize artifact loading at runtime.",
            "This design does not authorize raw text display.",
            "This design does not authorize vector display.",
            "This design does not authorize semantic runtime enablement.",
            "This phase adds no external dependency.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registration_and_no_public_contract_export(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["advisory_precomputed_artifact_ui_preview_design_feature_id"],
            "routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design_v1",
        )
        self.assertEqual(
            manifest["advisory_precomputed_artifact_ui_preview_design_status"],
            "standard_library_only_ui_preview_design_no_ui_no_reader_no_runtime_behavior_change",
        )
        self.assertEqual(
            manifest["advisory_precomputed_artifact_ui_preview_schema_version"],
            "3.10-advisory-precomputed-artifact-ui-preview-design",
        )
        self.assertEqual(
            manifest["advisory_precomputed_artifact_ui_preview_policy"],
            "design_only_no_ui_no_artifact_reading_no_loading_no_raw_text_no_vectors_no_runtime_enablement",
        )
        for characteristic in [
            "advisory_precomputed_artifact_ui_preview_design",
            "artifact_ui_preview_design_only",
            "no_artifact_ui_preview_implementation_added",
            "no_artifact_ui_preview_enabled",
            "no_artifact_reading_for_preview",
            "no_startup_artifact_loading_for_preview",
            "no_runtime_artifact_loading_for_preview",
            "artifact_ui_preview_no_raw_text_display",
            "artifact_ui_preview_no_vector_display",
            "artifact_ui_preview_review_evidence_only",
            "artifact_ui_preview_no_runtime_enablement",
            "artifact_ui_preview_requires_separate_governed_patch",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_module_is_stdlib_only_and_avoids_neighboring_boxes(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        forbidden = {
            "numpy",
            "pandas",
            "sklearn",
            "scipy",
            "torch",
            "tensorflow",
            "sentence_transformers",
            "transformers",
            "faiss",
            "chromadb",
            "qdrant_client",
            "langchain",
            "llama_index",
            "kanda_prompt_workspace",
            "project_freeze_ledger",
            "project_freeze_after_update",
        }
        self.assertFalse(forbidden.intersection(imports))

    def test_forbidden_runtime_artifacts_are_not_created(self):
        forbidden_paths = [
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "artifact_ui_preview.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "artifact_reader.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "precomputed_artifact_generator.py",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices",
            ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "vector_index.py",
        ]
        for path in forbidden_paths:
            self.assertFalse(path.exists(), str(path))

    def test_contract_and_init_exports_are_not_modified(self):
        contract_text = CONTRACT.read_text(encoding="utf-8")
        init_text = INIT.read_text(encoding="utf-8")
        self.assertNotIn("advisory_precomputed_artifact_ui_preview_design", contract_text)
        self.assertNotIn("advisory_precomputed_artifact_ui_preview_design", init_text)
        self.assertNotIn("validate_advisory_artifact_ui_preview_contract", contract_text)
        self.assertNotIn("validate_advisory_artifact_ui_preview_contract", init_text)


if __name__ == "__main__":
    unittest.main()
