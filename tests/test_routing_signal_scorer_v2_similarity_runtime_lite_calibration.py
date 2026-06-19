from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
    build_similarity_runtime_lite_advisory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_test_corpus.json"
)


class RoutingSignalScorerV2SimilarityRuntimeLiteCalibrationTests(unittest.TestCase):
    """Calibration tests for the frozen runtime-lite similarity advisor.

    These tests deliberately avoid stronger ML behavior. They protect threshold
    behavior, Fast Path safety, and high-risk hook preservation while keeping the
    runtime advisory only.
    """

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
        self.assertNotIn("may_proceed_now", result)
        self.assertNotIn("required_prompts_final", result)
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

    def _families(self, result: dict[str, object]) -> set[str]:
        families = set()
        for item in result["suggested_route_families"]:
            if isinstance(item, dict):
                families.add(str(item.get("family") or ""))
        return families

    def _similarity_promoted_case_ids(self, result: dict[str, object]) -> set[str]:
        case_ids = set()
        for item in result["suggested_route_families"]:
            if not isinstance(item, dict):
                continue
            if item.get("source_signal") != "similarity_runtime_lite":
                continue
            case_ids.add(str(item.get("source_case_id") or ""))
        return case_ids

    def test_ambiguous_go_request_matches_router_check_without_high_risk_hook(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        case = self._case(result, "STC-008")
        self.assertGreaterEqual(float(case["similarity_score"]), 0.85)
        self.assertEqual(case["similarity_level"], "high")
        self.assertIn("ambiguous_request_needs_router_check", self._families(result))
        self.assertEqual(result["recommended_hooks"], [])
        self.assertNotIn("pre_output_contract_gate_recommended", result["caution_flags"])

    def test_fast_path_patch_concept_trap_keeps_contract_hook_absent(self) -> None:
        result = self._runtime(
            "Explain what a patch means conceptually in simple terms. "
            "No code, no ZIP, just explain."
        )
        case = self._case(result, "STC-010")
        self.assertGreaterEqual(float(case["similarity_score"]), 0.85)
        self.assertIn("fast_path_simple_explanation", self._families(result))
        self.assertIn("fast_path_candidate_only", result["caution_flags"])
        self.assertNotIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])
        self.assertNotIn("pre_output_contract_gate_recommended", result["caution_flags"])

    def test_path_sensitive_project_root_anchor_keeps_contract_hook(self) -> None:
        result = self._runtime(
            "Use the selected active project root and project_freeze_after_update. "
            "Do not hardcode E:\\kanda_reasoner because there may be multiple projects."
        )
        case = self._case(result, "STC-011")
        self.assertGreaterEqual(float(case["similarity_score"]), 0.70)
        self.assertIn("multi_project_path_sensitive", self._families(result))
        self.assertIn("multi_project_path_sensitive", result["caution_flags"])
        self.assertIn("pre_output_contract_gate_recommended", result["caution_flags"])
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_low_similarity_matches_are_visible_but_not_promoted(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        low_patch_case = self._case(result, "STC-005")
        self.assertLess(float(low_patch_case["similarity_score"]), 0.30)
        self.assertEqual(low_patch_case["similarity_level"], "low")
        self.assertNotIn("STC-005", self._similarity_promoted_case_ids(result))
        self.assertNotIn("STC-002", self._similarity_promoted_case_ids(result))
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn("freeze_hint_sidecar_or_intake", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_min_similarity_parameter_filters_low_matches_without_muting_rules(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only.",
            min_similarity=0.30,
        )
        self.assertNotIn("STC-005", self._case_ids(result))
        self.assertNotIn("STC-002", self._case_ids(result))
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn("freeze_hint_sidecar_or_intake", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_medium_validation_anchor_remains_medium_calibrated(self) -> None:
        result = self._runtime(
            "The terminal shows VALIDATION OK and CONTRACT_TEST_OK after the "
            "python tests passed. Should I freeze this?"
        )
        case = self._case(result, "STC-003")
        self.assertGreaterEqual(float(case["similarity_score"]), 0.30)
        self.assertLess(float(case["similarity_score"]), 0.70)
        self.assertEqual(case["similarity_level"], "medium")
        self.assertIn("validation_artifact", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_unknown_text_stays_empty_and_non_authoritative(self) -> None:
        result = self._runtime("Please compare tea and coffee flavor preferences for a casual conversation.")
        self.assertEqual(result["similar_cases"], [])
        self.assertEqual(result["suggested_route_families"], [])
        self.assertEqual(result["recommended_hooks"], [])
        self.assertEqual(result["caution_flags"], [])
        self.assertIsNone(result["route_override"])

    def test_calibration_does_not_create_forbidden_runtime_files(self) -> None:
        corpus = CORPUS_PATH.read_text(encoding="utf-8")
        corpus.encode("ascii")
        forbidden_runtime_files = [
            "similarity_runtime.py",
            "tfidf_similarity.py",
            "embedding_similarity.py",
            "vector_store.py",
            "self_learning.py",
        ]
        scorer_dir = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
        for filename in forbidden_runtime_files:
            self.assertFalse((scorer_dir / filename).exists(), filename)


if __name__ == "__main__":
    unittest.main()
