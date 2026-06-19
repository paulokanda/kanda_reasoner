from __future__ import annotations

from pathlib import Path
import json
import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    ADVISORY_AUTHORITY,
    PRE_OUTPUT_HOOK,
    build_routing_advisory,
    score_routing_signals,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_test_corpus.json"
)
DESIGN_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_design.md"
)


class RoutingSignalScorerV2SimilarityTestCorpusTests(unittest.TestCase):
    """Corpus-only tests for future similarity work.

    These tests validate a curated example corpus. They do not implement
    runtime similarity and do not change deterministic routing behavior.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw_text = CORPUS_PATH.read_text(encoding="utf-8")
        cls.corpus = json.loads(cls.raw_text)
        cls.cases = cls.corpus["cases"]

    def test_corpus_file_exists_and_is_ascii_json(self) -> None:
        self.assertTrue(CORPUS_PATH.exists())
        self.raw_text.encode("ascii")
        self.assertEqual(self.corpus["schema_version"], "1.0")
        self.assertEqual(
            self.corpus["feature_id"],
            "routing_signal_scorer_v2_similarity_test_corpus",
        )

    def test_corpus_declares_corpus_only_non_runtime_scope(self) -> None:
        self.assertEqual(self.corpus["corpus_status"], "CORPUS_ONLY")
        self.assertEqual(self.corpus["runtime_status"], "NOT_IMPLEMENTED")
        self.assertEqual(self.corpus["authority_status"], "NON_AUTHORITATIVE_CORPUS")
        self.assertEqual(
            self.corpus["baseline_design_feature_id"],
            "routing_signal_scorer_v2_similarity_design",
        )
        self.assertIn("The scorer may suggest. The canon decides.", self.corpus["core_rule"])

    def test_similarity_output_limits_preserve_canon_authority(self) -> None:
        limits = self.corpus["similarity_output_limits"]
        self.assertEqual(limits["authority"], "advisory_only")
        self.assertIs(limits["canon_decides_final_route"], True)
        self.assertIs(limits["does_not_override_router"], True)
        self.assertEqual(
            limits["may_proceed_now_decision"],
            "not_provided_by_similarity",
        )
        self.assertIsNone(limits["route_override"])

    def test_required_categories_are_present_and_case_ids_are_unique(self) -> None:
        expected_categories = {
            "fast_path_simple_explanation",
            "patch_delivery",
            "validation_output",
            "freeze_form_json",
            "freeze_hint_sidecar",
            "confirmation_bypass",
            "prompt_library_governed_update",
            "ambiguous_request",
            "startup_delivery_regression_anchor_rg029",
            "similarity_false_positive_trap",
            "external_project_root_sensitive",
            "rg028_regression_anchor",
        }
        categories = {case["category"] for case in self.cases}
        self.assertEqual(categories, expected_categories)
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 12)

    def test_each_case_has_required_structure(self) -> None:
        required_fields = {
            "id",
            "category",
            "text",
            "expected_signals_min",
            "expected_hooks",
            "expected_route_families",
            "expected_caution_flags",
            "notes",
        }
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(required_fields.issubset(case))
                self.assertIsInstance(case["text"], str)
                self.assertGreater(len(case["text"]), 20)
                self.assertIsInstance(case["expected_signals_min"], dict)
                self.assertIsInstance(case["expected_hooks"], list)
                self.assertIsInstance(case["expected_route_families"], list)
                self.assertIsInstance(case["expected_caution_flags"], list)

    def test_current_diagnostic_scorer_matches_expected_minimums(self) -> None:
        for case in self.cases:
            result = score_routing_signals(case["text"])
            signals = result["signals"]
            with self.subTest(case=case["id"]):
                self.assertEqual(result["authority"], "diagnostic_only")
                self.assertIs(result["does_not_override_router"], True)
                for name, minimum in case["expected_signals_min"].items():
                    self.assertGreaterEqual(signals[name], minimum)
                for name, maximum in case.get("expected_signals_max", {}).items():
                    self.assertLessEqual(signals[name], maximum)

    def test_current_hook_recommendations_match_corpus_expectations(self) -> None:
        for case in self.cases:
            result = score_routing_signals(case["text"])
            hooks = set(result["recommended_hooks"])
            with self.subTest(case=case["id"]):
                for hook in case["expected_hooks"]:
                    self.assertIn(hook, hooks)
                for hook in case.get("expected_absent_hooks", []):
                    self.assertNotIn(hook, hooks)

    def test_current_advisory_matches_expected_families_and_flags(self) -> None:
        for case in self.cases:
            advisory = build_routing_advisory(case["text"], max_suggestions=12)
            families = {
                str(item["family"])
                for item in advisory["suggested_route_families"]
                if isinstance(item, dict)
            }
            flags = set(advisory["caution_flags"])
            with self.subTest(case=case["id"]):
                self.assertEqual(advisory["authority"], ADVISORY_AUTHORITY)
                self.assertIs(advisory["does_not_override_router"], True)
                self.assertIs(advisory["canon_decides_final_route"], True)
                self.assertEqual(
                    advisory["may_proceed_now_decision"],
                    "not_provided_by_advisory",
                )
                self.assertIsNone(advisory["route_override"])
                self.assertNotIn("may_proceed_now", advisory)
                for family in case["expected_route_families"]:
                    self.assertIn(family, families)
                for flag in case["expected_caution_flags"]:
                    self.assertIn(flag, flags)

    def test_false_positive_trap_preserves_fast_path_protection(self) -> None:
        traps = [case for case in self.cases if case["category"] == "similarity_false_positive_trap"]
        self.assertEqual(len(traps), 1)
        result = score_routing_signals(traps[0]["text"])
        self.assertGreaterEqual(result["signals"]["fast_path_simple_explanation"], 0.70)
        self.assertLessEqual(result["signals"]["patch_delivery"], 0.29)
        self.assertLessEqual(result["signals"]["pre_output_contract_gate_required"], 0.29)
        self.assertNotIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_rg_regression_anchors_are_present(self) -> None:
        by_id = {case["id"]: case for case in self.cases}
        self.assertIn("STC-009", by_id)
        self.assertIn("STC-012", by_id)
        startup = score_routing_signals(by_id["STC-009"]["text"])
        freeze = score_routing_signals(by_id["STC-012"]["text"])
        self.assertGreaterEqual(startup["signals"]["startup_delivery_change"], 0.70)
        self.assertGreaterEqual(freeze["signals"]["confirmation_gate_bypass_risk"], 0.70)
        self.assertGreaterEqual(freeze["signals"]["freeze_memory_write"], 0.70)

    def test_design_document_names_this_corpus_as_next_milestone(self) -> None:
        design_text = DESIGN_PATH.read_text(encoding="utf-8")
        self.assertIn("routing_signal_scorer_v2_similarity_test_corpus", design_text)
        self.assertIn("Do not implement runtime similarity immediately.", design_text)

    def test_no_runtime_similarity_files_exist(self) -> None:
        for relative in self.corpus["forbidden_runtime_files"]:
            with self.subTest(relative=relative):
                self.assertFalse((PROJECT_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
