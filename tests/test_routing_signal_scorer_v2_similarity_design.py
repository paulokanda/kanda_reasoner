from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    ADVISORY_AUTHORITY,
    build_routing_advisory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_design.md"
)


class RoutingSignalScorerV2SimilarityDesignTests(unittest.TestCase):
    """Design-only tests for a possible future similarity layer.

    These tests intentionally do not validate a runtime similarity function,
    because runtime similarity is not implemented in this milestone.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DESIGN_PATH.read_text(encoding="utf-8")

    def test_design_document_exists_and_declares_design_only_scope(self) -> None:
        self.assertTrue(DESIGN_PATH.exists())
        self.assertIn("Feature ID: routing_signal_scorer_v2_similarity_design", self.text)
        self.assertIn("Implementation status: DESIGN_ONLY", self.text)
        self.assertIn("Runtime status: NOT_IMPLEMENTED", self.text)
        self.assertIn("Authority status: NON_AUTHORITATIVE_DESIGN", self.text)

    def test_design_preserves_canon_authority(self) -> None:
        required = [
            "The scorer may suggest. The canon decides.",
            "authority: advisory_only",
            "canon_decides_final_route: true",
            "does_not_override_router: true",
            "may_proceed_now_decision: not_provided_by_similarity",
            "route_override: null",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_design_forbids_runtime_similarity_in_this_milestone(self) -> None:
        required = [
            "implement TF-IDF runtime scoring",
            "implement embedding runtime scoring",
            "add self-learning behavior",
            "auto-load prompts",
            "decide May proceed now",
            "override the deterministic router",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_design_defines_conservative_thresholds_and_false_positive_risks(self) -> None:
        required = [
            "0.00 to 0.29",
            "0.30 to 0.69",
            "0.70 to 0.84",
            "0.85 to 1.00",
            "Fast Path protection must remain a first-class regression test.",
            "Even a high score must not become a route override.",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_design_keeps_next_milestone_as_test_corpus_not_runtime(self) -> None:
        self.assertIn("routing_signal_scorer_v2_similarity_test_corpus", self.text)
        self.assertIn("Do not implement runtime similarity immediately.", self.text)
        self.assertIn("It should still avoid runtime TF-IDF, embeddings, or self-learning.", self.text)

    def test_existing_advisory_runtime_still_stays_non_authoritative(self) -> None:
        advisory = build_routing_advisory(
            "Create a patch ZIP and give me the PowerShell install block."
        )
        self.assertEqual(advisory["authority"], ADVISORY_AUTHORITY)
        self.assertIs(advisory["does_not_override_router"], True)
        self.assertIs(advisory["canon_decides_final_route"], True)
        self.assertEqual(
            advisory["may_proceed_now_decision"],
            "not_provided_by_advisory",
        )
        self.assertIsNone(advisory["route_override"])

    def test_patch_does_not_add_runtime_similarity_source_files(self) -> None:
        scorer_dir = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
        forbidden_names = {
            "similarity_runtime.py",
            "tfidf_similarity.py",
            "embedding_similarity.py",
            "vector_store.py",
            "self_learning.py",
        }
        existing = {path.name for path in scorer_dir.glob("*.py")}
        self.assertTrue(forbidden_names.isdisjoint(existing))

    def test_design_text_is_ascii_for_windows_terminal_stability(self) -> None:
        self.text.encode("ascii")


if __name__ == "__main__":
    unittest.main()
