from __future__ import annotations

from pathlib import Path
import hashlib
import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_RUNTIME_LITE_FEATURE_ID,
    build_similarity_runtime_lite_advisory,
    summarize_similarity_runtime_lite_advisory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_test_corpus.json"
)
RUNTIME_DESIGN_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_runtime_lite.md"
)


class RoutingSignalScorerV2SimilarityRuntimeLiteTests(unittest.TestCase):
    """Runtime-lite similarity tests.

    Runtime-lite may surface similar frozen corpus cases, but it remains
    advisory only and must not become the KANDA router.
    """

    def _runtime(self, text: str) -> dict[str, object]:
        result = build_similarity_runtime_lite_advisory(text, max_matches=4)
        self.assertEqual(result["schema_version"], "2.0")
        self.assertEqual(result["feature_id"], SIMILARITY_RUNTIME_LITE_FEATURE_ID)
        self.assertEqual(result["authority"], SIMILARITY_RUNTIME_LITE_AUTHORITY)
        self.assertEqual(result["runtime_status"], "RUNTIME_LITE")
        self.assertEqual(result["similarity_method"], "deterministic_token_overlap")
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

    def _families(self, result: dict[str, object]) -> set[str]:
        families = set()
        for item in result["suggested_route_families"]:
            if isinstance(item, dict):
                families.add(str(item.get("family") or ""))
        return families

    def _case_ids(self, result: dict[str, object]) -> set[str]:
        return {str(item.get("case_id") or "") for item in result["similar_cases"] if isinstance(item, dict)}

    def test_runtime_lite_design_doc_declares_advisory_boundary(self) -> None:
        text = RUNTIME_DESIGN_PATH.read_text(encoding="utf-8")
        text.encode("ascii")
        self.assertIn("Feature ID: routing_signal_scorer_v2_similarity_runtime_lite", text)
        self.assertIn("Implementation status: RUNTIME_LITE", text)
        self.assertIn("Authority status: ADVISORY_ONLY", text)
        self.assertIn("may_proceed_now_decision: not_provided_by_similarity", text)
        self.assertIn("self_learning_enabled: false", text)

    def test_patch_delivery_matches_corpus_and_preserves_contract_gate(self) -> None:
        result = self._runtime(
            "Create a patch ZIP and include a PowerShell install block. Move the ZIP "
            "into delete_after_daily_work and extract fresh."
        )
        self.assertIn("STC-002", self._case_ids(result))
        self.assertIn("patch_delivery_or_code_update", self._families(result))
        self.assertIn("terminal_install_artifact", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_freeze_json_matches_corpus_and_stays_advisory_only(self) -> None:
        result = self._runtime(
            "Return KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END "
            "with validation_evidence_summary for the local freeze entry."
        )
        self.assertIn("STC-004", self._case_ids(result))
        self.assertIn("freeze_form_json_artifact", self._families(result))
        self.assertIn("freeze_memory_workflow", self._families(result))
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_false_positive_trap_preserves_fast_path(self) -> None:
        result = self._runtime(
            "Explain what a patch means conceptually in simple terms. No code, no ZIP, just explain."
        )
        self.assertIn("STC-010", self._case_ids(result))
        self.assertIn("fast_path_simple_explanation", self._families(result))
        self.assertNotIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])
        self.assertIn("fast_path_candidate_only", result["caution_flags"])

    def test_unknown_low_similarity_text_has_no_router_authority(self) -> None:
        result = self._runtime("Please compare tea and coffee flavor preferences for a casual conversation.")
        self.assertEqual(result["recommended_hooks"], [])
        self.assertIsNone(result["route_override"])
        self.assertEqual(result["may_proceed_now_decision"], "not_provided_by_similarity")

    def test_runtime_lite_does_not_mutate_corpus_file(self) -> None:
        before = hashlib.sha256(CORPUS_PATH.read_bytes()).hexdigest()
        self._runtime("Create a patch ZIP with KANDA_FREEZE_HINT.json sidecar metadata.")
        after = hashlib.sha256(CORPUS_PATH.read_bytes()).hexdigest()
        self.assertEqual(before, after)

    def test_summary_restates_non_authoritative_runtime_limits(self) -> None:
        result = self._runtime("Create a patch ZIP with KANDA_FREEZE_HINT.json sidecar metadata.")
        summary = summarize_similarity_runtime_lite_advisory(result)
        self.assertIn("authority=advisory_only", summary)
        self.assertIn("runtime_status=RUNTIME_LITE", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn("canon_decides_final_route=True", summary)
        self.assertIn("may_proceed_now_decision=not_provided_by_similarity", summary)
        self.assertIn("self_learning_enabled=False", summary)

    def test_corpus_count_is_loaded_from_frozen_json(self) -> None:
        result = self._runtime("Run validation and include VALIDATION OK plus CONTRACT_TEST_OK.")
        self.assertEqual(result["corpus_feature_id"], "routing_signal_scorer_v2_similarity_test_corpus")
        self.assertEqual(result["corpus_case_count"], 12)


if __name__ == "__main__":
    unittest.main()
