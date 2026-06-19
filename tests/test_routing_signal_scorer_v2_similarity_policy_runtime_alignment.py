from __future__ import annotations

from pathlib import Path
import unittest

import kanda_reasoner_app.routing_signal_scorer as scorer_package
from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
    SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD,
    build_similarity_runtime_lite_advisory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_threshold_policy.md"
)
SCORER_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer"


class RoutingSignalScorerV2SimilarityPolicyRuntimeAlignmentTests(unittest.TestCase):
    """Runtime alignment tests for the frozen threshold policy."""

    def _runtime(
        self,
        text: str,
        *,
        max_matches: int = 6,
        min_similarity: float | None = None,
    ) -> dict[str, object]:
        kwargs: dict[str, object] = {"max_matches": max_matches}
        if min_similarity is not None:
            kwargs["min_similarity"] = min_similarity
        result = build_similarity_runtime_lite_advisory(text, **kwargs)
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

    def _case_ids(self, result: dict[str, object]) -> set[str]:
        return {
            str(item.get("case_id") or "")
            for item in result["similar_cases"]
            if isinstance(item, dict)
        }

    def _similarity_promoted_case_ids(self, result: dict[str, object]) -> set[str]:
        case_ids = set()
        for item in result["suggested_route_families"]:
            if not isinstance(item, dict):
                continue
            if item.get("source_signal") != "similarity_runtime_lite":
                continue
            case_ids.add(str(item.get("source_case_id") or ""))
        return case_ids

    def _families(self, result: dict[str, object]) -> set[str]:
        families = set()
        for item in result["suggested_route_families"]:
            if isinstance(item, dict):
                families.add(str(item.get("family") or ""))
        return families

    def test_threshold_constants_are_public_and_match_policy_doc(self) -> None:
        self.assertEqual(SIMILARITY_THRESHOLD_POLICY_FEATURE_ID, "routing_signal_scorer_v2_similarity_threshold_policy_v1")
        self.assertEqual(SIMILARITY_VISIBILITY_THRESHOLD, 0.18)
        self.assertEqual(SIMILARITY_PROMOTION_THRESHOLD, 0.30)
        self.assertEqual(SIMILARITY_HIGH_THRESHOLD, 0.55)
        self.assertEqual(scorer_package.SIMILARITY_VISIBILITY_THRESHOLD, 0.18)
        self.assertEqual(scorer_package.SIMILARITY_PROMOTION_THRESHOLD, 0.30)
        self.assertEqual(scorer_package.SIMILARITY_HIGH_THRESHOLD, 0.55)
        policy_text = POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("score below `0.18`", policy_text)
        self.assertIn("`0.18 <= score < 0.30`", policy_text)
        self.assertIn("`0.30 <= score < 0.55`", policy_text)
        self.assertIn("`score >= 0.55`", policy_text)

    def test_runtime_exposes_threshold_policy_metadata(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        policy = result["similarity_threshold_policy"]
        self.assertIsInstance(policy, dict)
        self.assertEqual(result["threshold_policy_feature_id"], SIMILARITY_THRESHOLD_POLICY_FEATURE_ID)
        self.assertEqual(result["similarity_visibility_threshold"], SIMILARITY_VISIBILITY_THRESHOLD)
        self.assertEqual(result["similarity_promotion_threshold"], SIMILARITY_PROMOTION_THRESHOLD)
        self.assertEqual(result["similarity_high_threshold"], SIMILARITY_HIGH_THRESHOLD)
        self.assertEqual(policy["visibility_threshold"], SIMILARITY_VISIBILITY_THRESHOLD)
        self.assertEqual(policy["promotion_threshold"], SIMILARITY_PROMOTION_THRESHOLD)
        self.assertEqual(policy["high_threshold"], SIMILARITY_HIGH_THRESHOLD)
        self.assertEqual(policy["route_family_suggestion_minimum"], SIMILARITY_PROMOTION_THRESHOLD)
        self.assertIs(policy["rule_hooks_independent"], True)
        self.assertEqual(policy["authority"], "advisory_only")
        self.assertIs(policy["does_not_override_router"], True)

    def test_default_visibility_threshold_comes_from_policy_constant(self) -> None:
        text = (
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        default_result = self._runtime(text)
        explicit_result = self._runtime(text, min_similarity=SIMILARITY_VISIBILITY_THRESHOLD)
        self.assertEqual(self._case_ids(default_result), self._case_ids(explicit_result))
        low_case = self._case(default_result, "STC-005")
        self.assertGreaterEqual(float(low_case["similarity_score"]), SIMILARITY_VISIBILITY_THRESHOLD)
        self.assertLess(float(low_case["similarity_score"]), SIMILARITY_PROMOTION_THRESHOLD)
        self.assertEqual(low_case["similarity_level"], "low")

    def test_promotion_threshold_controls_similarity_route_suggestions(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        low_case = self._case(result, "STC-005")
        self.assertLess(float(low_case["similarity_score"]), SIMILARITY_PROMOTION_THRESHOLD)
        self.assertNotIn("STC-005", self._similarity_promoted_case_ids(result))
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_high_similarity_is_aligned_but_not_authoritative(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        case = self._case(result, "STC-008")
        self.assertGreaterEqual(float(case["similarity_score"]), SIMILARITY_HIGH_THRESHOLD)
        self.assertEqual(case["similarity_level"], "high")
        self.assertIn("ambiguous_request_needs_router_check", self._families(result))
        self.assertEqual(result["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(result["required_prompts_final_decision"], "not_provided_by_similarity")
        self.assertIs(result["automatic_prompt_loading"], False)
        self.assertIsNone(result["route_override"])

    def test_policy_runtime_alignment_does_not_create_stronger_ml_files(self) -> None:
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
