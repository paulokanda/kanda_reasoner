from __future__ import annotations

from pathlib import Path
import unittest

import kanda_reasoner_app.routing_signal_scorer as scorer_package
from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    build_similarity_runtime_lite_advisory,
    summarize_similarity_runtime_lite_advisory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCORER_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer"


class RoutingSignalScorerV2SimilarityExplainabilityTests(unittest.TestCase):
    """Explainability tests for runtime-lite similarity output."""

    def _runtime(self, text: str, *, max_matches: int = 6) -> dict[str, object]:
        result = build_similarity_runtime_lite_advisory(text, max_matches=max_matches)
        self.assertEqual(result["authority"], SIMILARITY_RUNTIME_LITE_AUTHORITY)
        self.assertIs(result["does_not_override_router"], True)
        self.assertIs(result["canon_decides_final_route"], True)
        self.assertEqual(result["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertIsNone(result["route_override"])
        self.assertEqual(result["required_prompts_final_decision"], "not_provided_by_similarity")
        self.assertIs(result["automatic_prompt_loading"], False)
        self.assertIs(result["self_learning_enabled"], False)
        self.assertEqual(result["external_dependencies"], [])
        return result

    def _case(self, result: dict[str, object], case_id: str) -> dict[str, object]:
        for item in result["similar_cases"]:
            if isinstance(item, dict) and item.get("case_id") == case_id:
                return item
        self.fail("Expected similar case not found: " + case_id)

    def test_explainability_feature_id_is_public(self) -> None:
        self.assertEqual(
            SIMILARITY_EXPLAINABILITY_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_explainability_v1",
        )
        self.assertEqual(
            scorer_package.SIMILARITY_EXPLAINABILITY_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_explainability_v1",
        )

    def test_top_level_explainability_summary_lists_required_fields(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        self.assertEqual(result["explainability_feature_id"], SIMILARITY_EXPLAINABILITY_FEATURE_ID)
        summary = result["similarity_explainability"]
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary["feature_id"], SIMILARITY_EXPLAINABILITY_FEATURE_ID)
        self.assertEqual(summary["threshold_policy_feature_id"], SIMILARITY_THRESHOLD_POLICY_FEATURE_ID)
        self.assertEqual(summary["authority"], "advisory_only")
        self.assertIs(summary["does_not_override_router"], True)
        self.assertIn("hidden", summary["threshold_levels"])
        self.assertIn("visible_low", summary["threshold_levels"])
        self.assertIn("promoted_medium", summary["threshold_levels"])
        self.assertIn("high", summary["threshold_levels"])
        for field in [
            "matched_corpus_item_id",
            "matched_route_families",
            "similarity_score",
            "threshold_level",
            "route_family_suggestion_eligible",
            "advisory_only_reason",
            "rule_hook_independence",
        ]:
            self.assertIn(field, summary["match_fields"])

    def test_each_visible_match_carries_explainability_payload(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        match = self._case(result, "STC-008")
        self.assertEqual(match["matched_corpus_item_id"], "STC-008")
        self.assertEqual(match["matched_route_families"], ["ambiguous_request_needs_router_check"])
        self.assertEqual(match["threshold_level"], "high")
        self.assertIs(match["route_family_suggestion_eligible"], True)
        explanation = match["explainability"]
        self.assertEqual(explanation["feature_id"], SIMILARITY_EXPLAINABILITY_FEATURE_ID)
        self.assertEqual(explanation["matched_corpus_item_id"], "STC-008")
        self.assertEqual(explanation["matched_route_families"], ["ambiguous_request_needs_router_check"])
        self.assertEqual(explanation["similarity_score"], match["similarity_score"])
        self.assertEqual(explanation["threshold_level"], "high")
        self.assertIs(explanation["route_family_suggestion_eligible"], True)
        self.assertEqual(explanation["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(explanation["final_route_decision"], "not_provided_by_similarity")
        self.assertIs(explanation["does_not_override_router"], True)
        self.assertIn("canon decides final route", explanation["advisory_only_reason"])
        self.assertIn("Rule-based diagnostic hooks remain independent", explanation["rule_hook_independence"])

    def test_visible_low_match_explains_non_promotion(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        match = self._case(result, "STC-005")
        self.assertLess(float(match["similarity_score"]), SIMILARITY_PROMOTION_THRESHOLD)
        self.assertEqual(match["threshold_level"], "visible_low")
        self.assertIs(match["route_family_suggestion_eligible"], False)
        explanation = match["explainability"]
        self.assertEqual(explanation["threshold_level"], "visible_low")
        self.assertIs(explanation["route_family_suggestion_eligible"], False)
        self.assertEqual(explanation["matched_corpus_item_id"], "STC-005")
        self.assertEqual(explanation["matched_route_families"], match["matched_route_families"])
        similarity_case_ids = {
            str(item.get("source_case_id") or "")
            for item in result["suggested_route_families"]
            if isinstance(item, dict) and item.get("source_signal") == "similarity_runtime_lite"
        }
        self.assertNotIn("STC-005", similarity_case_ids)
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_similarity_route_suggestion_explains_advisory_status(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        # Rule suggestions may deduplicate the same family first, so inspect all
        # similarity-derived suggestions when they exist and require explanation.
        for item in result["suggested_route_families"]:
            if not isinstance(item, dict):
                continue
            if item.get("source_signal") != "similarity_runtime_lite":
                continue
            self.assertIn("matched_corpus_item_id", item)
            self.assertIn(item["threshold_level"], {"promoted_medium", "high"})
            self.assertIn("canon decides final route", item["advisory_only_reason"])
            self.assertIn("Rule-based diagnostic hooks remain independent", item["rule_hook_independence"])
            self.assertEqual(item["reason"], "Similar frozen corpus scenario detected. Advisory only.")

    def test_summary_includes_threshold_level_without_adding_authority(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        summary = summarize_similarity_runtime_lite_advisory(result)
        self.assertIn("STC-008(1.0)[high]", summary)
        self.assertIn("authority=advisory_only", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn("may_proceed_now_decision=not_provided_by_similarity", summary)
        self.assertIn("route_override=None", summary)

    def test_explainability_does_not_create_stronger_ml_files(self) -> None:
        forbidden_runtime_files = [
            "similarity_runtime.py",
            "tfidf_similarity.py",
            "embedding_similarity.py",
            "vector_store.py",
            "self_learning.py",
        ]
        for filename in forbidden_runtime_files:
            self.assertFalse((SCORER_DIR / filename).exists(), filename)


if __name__ == "__main__":
    unittest.main()
