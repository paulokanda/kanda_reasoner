import ast
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.offline_evaluation_corpus_design import (
    OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
    build_disabled_offline_evaluation_corpus_status,
    build_minimal_valid_evaluation_case,
    build_minimal_valid_evaluation_corpus_template,
    classify_evaluation_case_category,
    validate_evaluation_case,
    validate_offline_evaluation_corpus_plan,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "offline_evaluation_corpus_design.py"
DESIGN_DOC = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "design" / "routing_signal_scorer_v3_offline_evaluation_corpus_design.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"


class OfflineEvaluationCorpusDesignTests(unittest.TestCase):
    def test_feature_identity_and_disabled_status(self):
        self.assertEqual(
            OFFLINE_EVALUATION_CORPUS_FEATURE_ID,
            "routing_signal_scorer_v3_offline_evaluation_corpus_design_v1",
        )
        status = build_disabled_offline_evaluation_corpus_status()
        self.assertFalse(status["evaluation_runtime_enabled"])
        self.assertFalse(status["semantic_runtime_enabled"])
        self.assertFalse(status["threshold_auto_tuning_enabled"])
        self.assertFalse(status["embedding_generation_enabled"])
        self.assertFalse(status["vector_index_generation_enabled"])
        self.assertFalse(status["raw_user_query_storage_enabled"])
        self.assertTrue(status["advisory_only"])

    def test_minimal_valid_template_is_valid_but_not_authorizing_runtime(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        result = validate_offline_evaluation_corpus_plan(plan)
        self.assertTrue(result["ok"], result["errors"])
        self.assertFalse(result["semantic_runtime_authorized"])
        self.assertFalse(result["threshold_changes_authorized"])
        self.assertFalse(result["embedding_generation_authorized"])
        self.assertFalse(result["vector_index_authorized"])
        self.assertTrue(result["advisory_only"])

    def test_all_required_categories_are_present(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        categories = set(plan["case_categories"])
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
            self.assertTrue(classify_evaluation_case_category(category)["known_category"])

    def test_metrics_and_thresholds_must_be_declared_before_run(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        plan["declared_before_run"] = False
        result = validate_offline_evaluation_corpus_plan(plan)
        self.assertFalse(result["ok"])
        self.assertTrue(any("declared before" in error for error in result["errors"]))

    def test_required_metrics_present(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        metrics = set(plan["metrics"])
        for metric in ["precision_at_1", "precision_at_3", "recall_at_1", "recall_at_3", "mrr", "ndcg_at_10", "authority_leakage_rate", "p95_latency_overhead_ms"]:
            self.assertIn(metric, metrics)

    def test_zero_tolerance_thresholds_required(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        plan["acceptance_thresholds"]["authority_leakage_rate_must_equal_zero"] = False
        result = validate_offline_evaluation_corpus_plan(plan)
        self.assertFalse(result["ok"])
        self.assertTrue(any("zero leakage" in error for error in result["errors"]))

    def test_evaluation_case_rejects_raw_user_text_and_private_text(self):
        case = build_minimal_valid_evaluation_case("positive_routing_cases")
        case["contains_raw_user_text"] = True
        case["contains_private_project_text"] = True
        result = validate_evaluation_case(case)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("raw user text", joined)
        self.assertIn("private project text", joined)

    def test_raw_text_fields_are_rejected(self):
        case = build_minimal_valid_evaluation_case("positive_routing_cases")
        case["request_text"] = "raw user request must not be stored"
        result = validate_evaluation_case(case)
        self.assertFalse(result["ok"])
        self.assertTrue(any("forbidden raw text fields" in error for error in result["errors"]))

    def test_authority_fields_rejected_in_plan_and_cases(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        plan["may_proceed_now"] = True
        plan["evaluation_cases"][0]["final_route"] = "governed_patch"
        result = validate_offline_evaluation_corpus_plan(plan)
        self.assertFalse(result["ok"])
        joined = "\n".join(result["errors"])
        self.assertIn("forbidden", joined)

    def test_missing_category_case_invalid(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        plan["evaluation_cases"] = [case for case in plan["evaluation_cases"] if case["category"] != "stale_context_cases"]
        result = validate_offline_evaluation_corpus_plan(plan)
        self.assertFalse(result["ok"])
        self.assertTrue(any("stale_context_cases" in error for error in result["errors"]))

    def test_forbidden_actions_include_no_runtime_enablement(self):
        plan = build_minimal_valid_evaluation_corpus_template()
        forbidden = set(plan["forbidden_actions"])
        for action in [
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

    def test_design_document_declares_evaluation_boundaries(self):
        text = DESIGN_DOC.read_text(encoding="utf-8")
        for phrase in [
            "Routing Signal Scorer v3 Offline Evaluation Corpus Design v1",
            "The semantic layer remains an untrusted evidence witness.",
            "It may provide evidence. It may never provide authority.",
            "Metrics must be declared before the evaluation run.",
            "zero authority leakage",
            "synthetic or curated cases only",
            "Evaluation can only produce review evidence.",
            "This design does not authorize evaluation execution.",
            "This design does not authorize semantic runtime enablement.",
            "This design does not authorize threshold changes.",
        ]:
            self.assertIn(phrase, text)

    def test_manifest_registers_offline_evaluation_corpus_design(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.19.0")
        self.assertEqual(manifest["contract_version"], "1.8")
        self.assertEqual(
            manifest["offline_evaluation_corpus_design_feature_id"],
            "routing_signal_scorer_v3_offline_evaluation_corpus_design_v1",
        )
        self.assertEqual(
            manifest["offline_evaluation_corpus_design_status"],
            "standard_library_only_evaluation_contract_no_runtime_evaluation_no_ml_behavior_change",
        )
        for characteristic in [
            "offline_evaluation_corpus_design",
            "gold_set_design_validation_only",
            "thresholds_declared_before_evaluation_run",
            "zero_authority_leakage_required",
            "no_raw_user_query_text_in_evaluation_corpus",
            "no_semantic_runtime_enablement_from_evaluation_alone",
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
