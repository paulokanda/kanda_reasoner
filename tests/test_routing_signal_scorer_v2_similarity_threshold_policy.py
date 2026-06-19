from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.routing_signal_scorer import contract
from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
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


class RoutingSignalScorerV2SimilarityThresholdPolicyTests(unittest.TestCase):
    """Threshold-policy regression tests for runtime-lite similarity."""

    def _runtime(
        self,
        text: str,
        *,
        max_matches: int = 6,
        min_similarity: float = 0.18,
    ) -> dict[str, object]:
        result = build_similarity_runtime_lite_advisory(
            text,
            max_matches=max_matches,
            min_similarity=min_similarity,
        )
        self.assertEqual(result["authority"], "advisory_only")
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

    def test_policy_document_freezes_numeric_threshold_ladder(self) -> None:
        text = POLICY_PATH.read_text(encoding="utf-8")
        text.encode("ascii")
        required_fragments = [
            "score below `0.18`",
            "`0.18 <= score < 0.30`",
            "`0.30 <= score < 0.55`",
            "`score >= 0.55`",
            "Similarity-derived route families, hooks, and caution flags require a score of",
            "Runtime-lite similarity remains advisory only.",
            "Rule-based diagnostic and advisory signals remain independent",
        ]
        for fragment in required_fragments:
            self.assertIn(fragment, text)

    def test_runtime_similarity_level_boundaries_match_policy(self) -> None:
        self.assertEqual(contract._similarity_level(0.179), "low")
        self.assertEqual(contract._similarity_level(0.18), "low")
        self.assertEqual(contract._similarity_level(0.299), "low")
        self.assertEqual(contract._similarity_level(0.30), "medium")
        self.assertEqual(contract._similarity_level(0.549), "medium")
        self.assertEqual(contract._similarity_level(0.55), "high")

    def test_low_similarity_visibility_does_not_promote_similarity_routes(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        low_case = self._case(result, "STC-005")
        self.assertGreaterEqual(float(low_case["similarity_score"]), 0.18)
        self.assertLess(float(low_case["similarity_score"]), 0.30)
        self.assertEqual(low_case["similarity_level"], "low")
        self.assertNotIn("STC-005", self._similarity_promoted_case_ids(result))
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_min_similarity_filters_similarity_without_muting_rule_hooks(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only.",
            min_similarity=0.30,
        )
        case_ids = {
            str(item.get("case_id") or "")
            for item in result["similar_cases"]
            if isinstance(item, dict)
        }
        self.assertNotIn("STC-005", case_ids)
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_high_similarity_is_still_advisory_not_authority(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        case = self._case(result, "STC-008")
        self.assertEqual(case["similarity_level"], "high")
        self.assertIn("ambiguous_request_needs_router_check", self._families(result))
        self.assertEqual(result["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(result["required_prompts_final_decision"], "not_provided_by_similarity")
        self.assertIs(result["automatic_prompt_loading"], False)
        self.assertIsNone(result["route_override"])

    def test_threshold_policy_does_not_create_stronger_ml_runtime_files(self) -> None:
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
