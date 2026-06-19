import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.offline_corpus_governance import (
    ALLOWED_HUMAN_GOVERNED_TRIGGERS,
    FORBIDDEN_AUTOMATIC_TRIGGERS,
    OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID,
    build_disabled_offline_corpus_governance_status,
    build_minimal_valid_governance_plan_template,
    classify_corpus_governance_trigger,
    validate_offline_corpus_governance_plan,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "offline_corpus_governance.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_offline_corpus_governance_design.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class OfflineCorpusGovernanceDesignTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            OFFLINE_CORPUS_GOVERNANCE_FEATURE_ID,
            "routing_signal_scorer_v3_offline_corpus_governance_design_v1",
        )
        status = build_disabled_offline_corpus_governance_status()
        self.assertFalse(status["corpus_generation_enabled"])
        self.assertFalse(status["runtime_manifest_use_enabled"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["external_api_enabled"])
        self.assertTrue(status["advisory_only"])

    def test_minimal_valid_template_is_valid_but_not_authorized_to_generate(self):
        plan = build_minimal_valid_governance_plan_template()
        result = validate_offline_corpus_governance_plan(plan)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["generation_authorized"])
        self.assertFalse(result["runtime_use_authorized"])
        self.assertTrue(result["advisory_only"])
        self.assertIn("future governed freeze", result["reason"])

    def test_missing_required_fields_invalid(self):
        result = validate_offline_corpus_governance_plan({"schema_version": "3.3-offline-corpus-governance"})
        self.assertFalse(result["ok"])
        self.assertTrue(any("missing required" in error for error in result["errors"]))
        self.assertFalse(result["generation_authorized"])

    def test_forbidden_automatic_trigger_rejected(self):
        plan = build_minimal_valid_governance_plan_template()
        plan["trigger"] = "startup"
        result = validate_offline_corpus_governance_plan(plan)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden automatic trigger" in error for error in result["errors"]))

    def test_human_governed_triggers_are_not_automatic_generation(self):
        for trigger in sorted(ALLOWED_HUMAN_GOVERNED_TRIGGERS):
            result = classify_corpus_governance_trigger(trigger)
            self.assertTrue(result["allowed_for_governance_review"])
            self.assertFalse(result["automatic_generation_allowed"])

    def test_forbidden_triggers_are_blocked(self):
        for trigger in sorted(FORBIDDEN_AUTOMATIC_TRIGGERS):
            result = classify_corpus_governance_trigger(trigger)
            self.assertFalse(result["allowed_for_governance_review"])
            self.assertFalse(result["automatic_generation_allowed"])

    def test_forbidden_source_types_rejected(self):
        for source_type in ["raw_prompt_text", "freeze_entry_text", "user_query_text", "vector_values"]:
            plan = build_minimal_valid_governance_plan_template()
            plan["source_layers"][0]["source_type"] = source_type
            result = validate_offline_corpus_governance_plan(plan)
            self.assertFalse(result["ok"], source_type)
            self.assertTrue(any("forbidden source_type" in error for error in result["errors"]), result["errors"])

    def test_forbidden_output_artifacts_rejected(self):
        for artifact_type in ["embedding_vector_file", "vector_index", "freeze_memory_entry", "startup_delivery_mutation"]:
            plan = build_minimal_valid_governance_plan_template()
            plan["output_artifacts"][0]["artifact_type"] = artifact_type
            result = validate_offline_corpus_governance_plan(plan)
            self.assertFalse(result["ok"], artifact_type)
            self.assertTrue(any("forbidden artifact_type" in error for error in result["errors"]), result["errors"])

    def test_authority_fields_rejected_everywhere(self):
        plan = build_minimal_valid_governance_plan_template()
        plan["final_route"] = "governed_patch"
        plan["source_layers"][0]["required_prompts"] = ["x"]
        plan["output_artifacts"][0]["may_proceed_now"] = True
        result = validate_offline_corpus_governance_plan(plan)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden authority fields", joined)

    def test_validation_gates_are_required(self):
        plan = build_minimal_valid_governance_plan_template()
        plan["validation_gates"] = ["human_review_required"]
        result = validate_offline_corpus_governance_plan(plan)
        self.assertFalse(result["ok"])
        self.assertTrue(any("validation_gates missing required values" in error for error in result["errors"]))

    def test_module_is_standard_library_only_and_does_not_import_neighbor_boxes(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        roots = set()
        full = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    full.add(alias.name)
                    roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                full.add(node.module)
                roots.add(node.module.split(".")[0])

        forbidden_roots = {
            "numpy", "pandas", "sklearn", "scipy", "torch", "tensorflow",
            "sentence_transformers", "transformers", "faiss", "chromadb",
            "qdrant_client", "langchain", "llama_index",
        }
        forbidden_full = {
            "kanda_prompt_workspace",
            "project_freeze_ledger",
            "project_freeze_after_update",
            "kanda_reasoner_app.freeze_hint_intake",
            "kanda_reasoner_app.freeze_after_update",
            "kanda_reasoner_app.freeze_after_update_gui",
        }
        self.assertTrue(forbidden_roots.isdisjoint(roots), forbidden_roots & roots)
        self.assertTrue(forbidden_full.isdisjoint(full), forbidden_full & full)

    def test_design_document_declares_governance_boundaries(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Offline Corpus Governance Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "Corpus generation must be offline, human-governed, diff-reviewed, schema-validated, and frozen before runtime use.",
            "No startup rebuild. No runtime rebuild. No background rebuild. No file-watcher rebuild.",
            "Future source layers must use curated metadata records only.",
            "Output artifacts must not contain raw text or vector values.",
            "freeze required before runtime use",
            "This phase adds no external dependency.",
            "does not authorize generation",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_offline_corpus_governance_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["offline_corpus_governance_design_feature_id"],
            "routing_signal_scorer_v3_offline_corpus_governance_design_v1",
        )
        self.assertEqual(
            manifest["offline_corpus_governance_design_status"],
            "standard_library_only_governance_contract_no_generator_no_runtime_behavior_change",
        )
        for characteristic in [
            "offline_corpus_governance_design",
            "governance_plan_validation_only",
            "no_corpus_generator_added",
            "no_runtime_corpus_generation",
            "no_startup_corpus_generation",
            "human_governed_corpus_review_required",
            "diff_review_required_before_manifest_use",
            "freeze_required_before_runtime_manifest_use",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_forbidden_runtime_artifacts_absent(self):
        for rel in [
            "kanda_reasoner_app/routing_signal_scorer/providers",
            "kanda_reasoner_app/routing_signal_scorer/indices",
            "kanda_reasoner_app/routing_signal_scorer/corpus_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/semantic_provider.py",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
        ]:
            self.assertFalse((PROJECT_ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
