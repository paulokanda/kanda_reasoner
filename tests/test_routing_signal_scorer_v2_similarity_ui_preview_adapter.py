from __future__ import annotations

from pathlib import Path
import unittest

import kanda_reasoner_app.routing_signal_scorer as scorer_package
from kanda_reasoner_app.routing_signal_scorer.contract import (
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
    build_similarity_ui_preview_adapter,
    render_similarity_ui_preview_text,
)

SCORER_DIR = Path(__file__).resolve().parents[1] / "kanda_reasoner_app" / "routing_signal_scorer"


class SimilarityUiPreviewAdapterTests(unittest.TestCase):
    def _preview(self, text: str) -> dict[str, object]:
        return build_similarity_ui_preview_adapter(text, max_matches=3)

    def _mapped_lines(self, preview: dict[str, object]) -> dict[str, str]:
        text = render_similarity_ui_preview_text(preview)
        mapped: dict[str, str] = {}
        for line in text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                mapped[key] = value
        return mapped

    def test_ui_preview_feature_id_is_public(self) -> None:
        self.assertEqual(
            SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_ui_preview_adapter_v1",
        )
        self.assertEqual(
            scorer_package.SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_ui_preview_adapter_v1",
        )

    def test_preview_payload_is_gui_log_preview_only(self) -> None:
        preview = self._preview("Go continue and update logic if needed.")
        self.assertEqual(preview["feature_id"], SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID)
        self.assertEqual(preview["decision_report_feature_id"], SIMILARITY_DECISION_REPORT_FEATURE_ID)
        self.assertEqual(preview["authority"], "advisory_only")
        self.assertEqual(preview["adapter_scope"], "gui_log_preview_only")
        self.assertEqual(preview["preview_format"], "plain_text_lines")
        self.assertIs(preview["does_not_override_router"], True)
        self.assertIs(preview["canon_decides_final_route"], True)

    def test_preview_lines_show_decision_report_boundaries(self) -> None:
        preview = self._preview("Go continue and update logic if needed.")
        lines = preview["preview_lines"]
        self.assertIsInstance(lines, list)
        self.assertEqual(lines[0], "Routing Signal Scorer v2 Similarity Preview")
        self.assertIn("decision_report_begin", lines)
        self.assertIn("decision_report_end", lines)
        self.assertIn("Similarity decision report", lines)

    def test_preview_exposes_top_match_score_threshold_and_eligibility(self) -> None:
        preview = self._preview("Go continue and update logic if needed.")
        mapped = self._mapped_lines(preview)
        self.assertEqual(mapped["top_match"], "STC-008")
        self.assertEqual(mapped["top_match_score"], "1.000")
        self.assertEqual(mapped["top_match_threshold_level"], "high")
        self.assertEqual(mapped["route_family_suggestion_eligible"], "True")
        self.assertEqual(mapped["matched_route_families"], "ambiguous_request_needs_router_check")

    def test_preview_repeats_non_authority_guardrails(self) -> None:
        preview = self._preview("Create a patch ZIP with install and validation blocks.")
        mapped = self._mapped_lines(preview)
        self.assertEqual(mapped["authority"], "advisory_only")
        self.assertEqual(mapped["does_not_override_router"], "True")
        self.assertEqual(mapped["canon_decides_final_route"], "True")
        self.assertEqual(mapped["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(mapped["route_override"], "None")
        self.assertEqual(mapped["automatic_prompt_loading"], "False")
        self.assertEqual(mapped["self_learning_enabled"], "False")

    def test_preview_preserves_high_risk_hook_visibility(self) -> None:
        preview = self._preview(
            "Create a patch ZIP and include PowerShell install and validation blocks. "
            "Keep KANDA_FREEZE_HINT.json as sidecar metadata only."
        )
        mapped = self._mapped_lines(preview)
        self.assertIn("pre_output_contract_gates", mapped["recommended_hooks"])
        self.assertIn("Rule-based diagnostic hooks remain independent", mapped["rule_hook_independence"])

    def test_no_match_preview_stays_non_authoritative(self) -> None:
        preview = self._preview("zzzz yyyyy xxxxxx")
        mapped = self._mapped_lines(preview)
        self.assertEqual(mapped["top_match"], "none")
        self.assertEqual(mapped["top_match_score"], "0.000")
        self.assertEqual(mapped["top_match_threshold_level"], "hidden")
        self.assertEqual(mapped["route_family_suggestion_eligible"], "False")
        self.assertEqual(mapped["route_override"], "None")

    def test_render_function_returns_plain_text(self) -> None:
        preview = self._preview("Go continue and update logic if needed.")
        text = render_similarity_ui_preview_text(preview)
        self.assertIsInstance(text, str)
        self.assertIn("Routing Signal Scorer v2 Similarity Preview", text)
        self.assertIn("decision_report_begin", text)
        self.assertIn("decision_report_end", text)

    def test_preview_does_not_create_stronger_ml_files(self) -> None:
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
