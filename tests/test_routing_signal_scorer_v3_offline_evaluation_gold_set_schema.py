import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.offline_evaluation_gold_set_schema import (
    OFFLINE_EVALUATION_GOLD_SET_FEATURE_ID,
    build_disabled_gold_set_schema_status,
    build_minimal_valid_gold_set_case,
    build_minimal_valid_gold_set_template,
    classify_gold_set_case_category,
    validate_gold_set_case,
    validate_offline_evaluation_gold_set,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "offline_evaluation_gold_set_schema.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_offline_evaluation_gold_set_schema.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class OfflineEvaluationGoldSetSchemaTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            OFFLINE_EVALUATION_GOLD_SET_FEATURE_ID,
            "routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1",
        )
        status = build_disabled_gold_set_schema_status()
        self.assertFalse(status["evaluation_runner_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertFalse(status["threshold_auto_tuning_enabled"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["raw_user_query_storage_enabled"])
        self.assertFalse(status["external_api_enabled"])
        self.assertTrue(status["advisory_only"])

    def test_minimal_valid_gold_set_is_valid_but_not_authorizing_runtime(self):
        gold_set = build_minimal_valid_gold_set_template()
        result = validate_offline_evaluation_gold_set(gold_set)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["evaluation_runner_authorized"])
        self.assertFalse(result["threshold_changes_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_authorized"])
        self.assertTrue(result["advisory_only"])

    def test_all_required_categories_have_case_coverage(self):
        gold_set = build_minimal_valid_gold_set_template()
        categories = {case["category"] for case in gold_set["case_records"]}
        for category in [
            "positive_routing_cases",
            "near_miss_cases",
            "ambiguous_cases",
            "adversarial_instruction_cases",
            "stale_context_cases",
            "out_of_domain_cases",
            "freeze_shield_boundary_cases",
            "fast_path_false_positive_cases",
        ]:
            self.assertIn(category, categories)

    def test_unknown_category_is_rejected(self):
        case = build_minimal_valid_gold_set_case("positive_routing_cases")
        case["category"] = "unknown_category"
        result = validate_gold_set_case(case)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unknown" in error for error in result["errors"]))
        classified = classify_gold_set_case_category("unknown_category")
        self.assertFalse(classified["known_category"])
        self.assertFalse(classified["semantic_runtime_authorized"])

    def test_ambiguous_cases_must_mark_ambiguity(self):
        case = build_minimal_valid_gold_set_case("ambiguous_cases")
        self.assertTrue(validate_gold_set_case(case)["ok"])
        case["must_mark_ambiguity"] = False
        result = validate_gold_set_case(case)
        self.assertFalse(result["ok"])
        self.assertTrue(any("ambiguity" in error for error in result["errors"]))

    def test_stale_cases_must_declare_forbidden_candidate_ids(self):
        case = build_minimal_valid_gold_set_case("stale_context_cases")
        self.assertTrue(validate_gold_set_case(case)["ok"])
        case["forbidden_candidate_ids"] = []
        result = validate_gold_set_case(case)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden_candidate_ids" in error for error in result["errors"]))

    def test_raw_and_private_text_fields_are_rejected(self):
        case = build_minimal_valid_gold_set_case("positive_routing_cases")
        case["request_text"] = "do not store raw request text"
        case["prompt_file_text"] = "do not store prompt body"
        result = validate_gold_set_case(case)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden raw/private text fields", joined)

    def test_privacy_flags_must_be_false(self):
        case = build_minimal_valid_gold_set_case("positive_routing_cases")
        case["contains_raw_user_text"] = True
        case["contains_private_project_text"] = True
        case["contains_prompt_body_text"] = True
        case["contains_freeze_entry_text"] = True
        result = validate_gold_set_case(case)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("raw user text", joined)
        self.assertIn("private project text", joined)
        self.assertIn("prompt body text", joined)
        self.assertIn("freeze entry text", joined)

    def test_authority_fields_rejected_in_gold_set_and_cases(self):
        gold_set = build_minimal_valid_gold_set_template()
        gold_set["may_proceed_now"] = True
        gold_set["case_records"][0]["final_route"] = "governed_patch"
        result = validate_offline_evaluation_gold_set(gold_set)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden", joined)

    def test_gold_set_must_be_declared_before_run(self):
        gold_set = build_minimal_valid_gold_set_template()
        gold_set["declared_before_run"] = False
        result = validate_offline_evaluation_gold_set(gold_set)
        self.assertFalse(result["ok"])
        self.assertTrue(any("before any evaluation run" in error for error in result["errors"]))

    def test_missing_category_coverage_invalidates_gold_set(self):
        gold_set = build_minimal_valid_gold_set_template()
        gold_set["case_records"] = [case for case in gold_set["case_records"] if case["category"] != "near_miss_cases"]
        result = validate_offline_evaluation_gold_set(gold_set)
        self.assertFalse(result["ok"])
        self.assertTrue(any("near_miss_cases" in error for error in result["errors"]))

    def test_forbidden_actions_include_no_runner_no_runtime_no_tuning(self):
        gold_set = build_minimal_valid_gold_set_template()
        forbidden = set(gold_set["forbidden_actions"])
        for action in [
            "run_evaluation",
            "enable_semantic_runtime",
            "install_ml_dependency",
            "generate_embeddings",
            "create_vector_index",
            "auto_adjust_thresholds_after_results",
            "produce_final_route",
        ]:
            self.assertIn(action, forbidden)

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

    def test_design_document_declares_gold_set_boundaries(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "Metrics and thresholds must be declared before the evaluation run.",
            "zero authority leakage",
            "zero privacy leakage",
            "Synthetic or curated cases only.",
            "This schema phase does not authorize",
            "The gold set can only produce review evidence.",
            "It may never enable semantic runtime behavior",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_offline_evaluation_gold_set_schema(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["offline_evaluation_gold_set_schema_feature_id"],
            "routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1",
        )
        self.assertEqual(
            manifest["offline_evaluation_gold_set_schema_status"],
            "standard_library_only_gold_set_schema_contract_no_runner_no_ml_behavior_change",
        )
        for characteristic in [
            "offline_evaluation_gold_set_schema",
            "gold_set_schema_validation_only",
            "no_evaluation_runner_added",
            "gold_set_cases_synthetic_or_curated_only",
            "gold_set_zero_authority_leakage_required",
            "gold_set_no_runtime_enablement",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_forbidden_runtime_artifacts_absent(self):
        for rel in [
            "kanda_reasoner_app/routing_signal_scorer/providers",
            "kanda_reasoner_app/routing_signal_scorer/indices",
            "kanda_reasoner_app/routing_signal_scorer/evaluation_runner.py",
            "kanda_reasoner_app/routing_signal_scorer/corpus_generator.py",
            "kanda_reasoner_app/routing_signal_scorer/semantic_provider.py",
            "kanda_reasoner_app/routing_signal_scorer/vector_index.py",
        ]:
            self.assertFalse((PROJECT_ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
