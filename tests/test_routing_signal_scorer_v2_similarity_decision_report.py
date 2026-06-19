from __future__ import annotations

from pathlib import Path
import unittest

import kanda_reasoner_app.routing_signal_scorer as scorer_package
from kanda_reasoner_app.routing_signal_scorer.contract import (
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_PROMOTION_THRESHOLD,
    build_similarity_runtime_lite_advisory,
    summarize_similarity_runtime_lite_advisory,
)

SCORER_DIR = Path(__file__).resolve().parents[1] / "kanda_reasoner_app" / "routing_signal_scorer"


class SimilarityDecisionReportTests(unittest.TestCase):
    def _runtime(self, text: str) -> dict[str, object]:
        return build_similarity_runtime_lite_advisory(text, max_matches=3)

    def _report_map(self, result: dict[str, object]) -> dict[str, str]:
        report = result.get("similarity_decision_report")
        self.assertIsInstance(report, list)
        mapped: dict[str, str] = {}
        for line in report:
            self.assertIsInstance(line, str)
            if "=" in line:
                key, value = line.split("=", 1)
                mapped[key] = value
        return mapped

    def test_decision_report_feature_id_is_public(self) -> None:
        self.assertEqual(
            SIMILARITY_DECISION_REPORT_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_decision_report_v1",
        )
        self.assertEqual(
            scorer_package.SIMILARITY_DECISION_REPORT_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_decision_report_v1",
        )

    def test_top_level_decision_report_summary_lists_required_fields(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        self.assertEqual(result["decision_report_feature_id"], SIMILARITY_DECISION_REPORT_FEATURE_ID)
        summary = result["similarity_decision_report_summary"]
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary["feature_id"], SIMILARITY_DECISION_REPORT_FEATURE_ID)
        self.assertEqual(summary["authority"], "advisory_only")
        self.assertIs(summary["does_not_override_router"], True)
        self.assertEqual(summary["format"], "compact_human_readable_lines")
        for field in [
            "top_match",
            "top_match_score",
            "top_match_threshold_level",
            "route_family_suggestion_eligible",
            "matched_route_families",
            "advisory_only_reason",
            "rule_hook_independence",
        ]:
            self.assertIn(field, summary["fields"])

    def test_report_names_top_match_score_threshold_and_eligibility(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        mapped = self._report_map(result)
        self.assertEqual(mapped["feature_id"], SIMILARITY_DECISION_REPORT_FEATURE_ID)
        self.assertEqual(mapped["authority"], "advisory_only")
        self.assertEqual(mapped["does_not_override_router"], "True")
        self.assertEqual(mapped["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(mapped["route_override"], "None")
        self.assertEqual(mapped["top_match"], "STC-008")
        self.assertEqual(mapped["top_match_score"], "1.000")
        self.assertEqual(mapped["top_match_threshold_level"], "high")
        self.assertEqual(mapped["route_family_suggestion_eligible"], "True")
        self.assertEqual(mapped["matched_route_families"], "ambiguous_request_needs_router_check")

    def test_report_explains_advisory_only_and_rule_hook_independence(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        mapped = self._report_map(result)
        self.assertIn("canon decides final route", mapped["advisory_only_reason"])
        self.assertIn("Rule-based diagnostic hooks remain independent", mapped["rule_hook_independence"])

    def test_visible_low_report_does_not_claim_route_suggestion_eligibility(self) -> None:
        result = self._runtime(
            "Create an installable patch ZIP for the routing scorer. Include "
            "PowerShell install and validation blocks, and keep "
            "KANDA_FREEZE_HINT.json as sidecar only."
        )
        top = result["similar_cases"][0]
        self.assertLess(float(top["similarity_score"]), SIMILARITY_PROMOTION_THRESHOLD)
        mapped = self._report_map(result)
        self.assertEqual(mapped["top_match"], "STC-005")
        self.assertEqual(mapped["top_match_threshold_level"], "visible_low")
        self.assertEqual(mapped["route_family_suggestion_eligible"], "False")

    def test_no_match_report_stays_non_authoritative(self) -> None:
        result = self._runtime("zzzz yyyyy xxxxxx")
        self.assertEqual(result["similar_cases"], [])
        mapped = self._report_map(result)
        self.assertEqual(mapped["top_match"], "none")
        self.assertEqual(mapped["top_match_score"], "0.000")
        self.assertEqual(mapped["top_match_threshold_level"], "hidden")
        self.assertEqual(mapped["route_family_suggestion_eligible"], "False")
        self.assertEqual(mapped["authority"], "advisory_only")
        self.assertEqual(mapped["route_override"], "None")

    def test_summary_mentions_decision_report_without_adding_authority(self) -> None:
        result = self._runtime("Go continue and update logic if needed.")
        summary = summarize_similarity_runtime_lite_advisory(result)
        self.assertIn("decision_report=present", summary)
        self.assertIn("authority=advisory_only", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn("may_proceed_now_decision=not_provided_by_similarity", summary)
        self.assertIn("route_override=None", summary)

    def test_decision_report_does_not_create_stronger_ml_files(self) -> None:
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
