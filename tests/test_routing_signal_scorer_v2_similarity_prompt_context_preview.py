from __future__ import annotations

from pathlib import Path
import unittest

import kanda_reasoner_app.routing_signal_scorer as scorer_package
from kanda_reasoner_app.routing_signal_scorer.contract import (
    SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
    build_similarity_prompt_context_preview,
    render_similarity_prompt_context_preview_text,
)

SCORER_DIR = Path(__file__).resolve().parents[1] / "kanda_reasoner_app" / "routing_signal_scorer"


class SimilarityPromptContextPreviewTests(unittest.TestCase):
    def _preview(self, text: str) -> dict[str, object]:
        return build_similarity_prompt_context_preview(text, max_matches=3)

    def _mapped_lines(self, preview: dict[str, object]) -> dict[str, str]:
        text = render_similarity_prompt_context_preview_text(preview)
        mapped: dict[str, str] = {}
        for line in text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                mapped[key] = value
        return mapped

    def _context_labels(self, preview: dict[str, object]) -> list[str]:
        contexts = preview.get("candidate_prompt_contexts", [])
        self.assertIsInstance(contexts, list)
        labels = []
        for item in contexts:
            self.assertIsInstance(item, dict)
            labels.append(str(item.get("context_label") or ""))
        return labels

    def test_feature_id_and_exports_are_public(self) -> None:
        self.assertEqual(
            SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_prompt_context_preview_v1",
        )
        self.assertEqual(
            scorer_package.SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
            "routing_signal_scorer_v2_similarity_prompt_context_preview_v1",
        )
        self.assertIs(scorer_package.build_similarity_prompt_context_preview, build_similarity_prompt_context_preview)
        self.assertIs(
            scorer_package.render_similarity_prompt_context_preview_text,
            render_similarity_prompt_context_preview_text,
        )

    def test_prompt_context_preview_is_candidate_only(self) -> None:
        preview = self._preview("Create a patch ZIP with install and validation blocks.")
        self.assertEqual(preview["feature_id"], SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID)
        self.assertEqual(preview["source_feature_id"], SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID)
        self.assertEqual(preview["authority"], "advisory_only")
        self.assertEqual(preview["adapter_scope"], "candidate_prompt_context_preview_only")
        self.assertIs(preview["candidate_contexts_only"], True)
        self.assertIs(preview["does_not_override_router"], True)
        self.assertIs(preview["canon_decides_final_route"], True)

    def test_patch_request_shows_patch_candidates_without_final_prompt_decision(self) -> None:
        preview = self._preview("Create a patch ZIP with PowerShell install and validation blocks.")
        labels = self._context_labels(preview)
        mapped = self._mapped_lines(preview)
        self.assertIn("05_patch_delivery_and_validation_candidate", labels)
        self.assertIn("08_python_engineering_core_candidate", labels)
        self.assertIn("09_python_quality_security_observability_candidate", labels)
        self.assertIn("pre_output_contract_gates_candidate", labels)
        self.assertEqual(mapped["required_prompts_final_decision"], "not_provided_by_similarity")
        self.assertEqual(mapped["automatic_prompt_loading"], "False")

    def test_freeze_form_request_shows_freeze_candidates_and_hook(self) -> None:
        preview = self._preview(
            "Return KANDA_FREEZE_FORM_JSON_BEGIN freeze form JSON with validation_evidence_summary."
        )
        labels = self._context_labels(preview)
        mapped = self._mapped_lines(preview)
        self.assertIn("freeze_code_intake_and_form_protocol_candidate", labels)
        self.assertIn("pre_output_contract_gates_candidate", labels)
        self.assertIn("pre_output_contract_gates", mapped["recommended_hooks"])
        self.assertEqual(mapped["may_proceed_now_decision"], "not_provided_by_similarity")

    def test_startup_delivery_request_surfaces_startup_candidate(self) -> None:
        preview = self._preview(
            "Modify paste_after_first_prompts_to_ai.md and sync_startup_routing_kernel_pack.py."
        )
        labels = self._context_labels(preview)
        mapped = self._mapped_lines(preview)
        self.assertIn("paste_if_modify_startup_delivery_candidate", labels)
        self.assertIn("startup_delivery_maintenance_protocol_candidate", labels)
        self.assertIn("startup_delivery_update", mapped["route_family_candidates"])
        self.assertIn("startup_delivery_governance_needed", mapped["caution_flags"])

    def test_ambiguous_go_next_request_shows_router_context_candidate(self) -> None:
        preview = self._preview("go next")
        labels = self._context_labels(preview)
        mapped = self._mapped_lines(preview)
        self.assertIn("router_context_check_candidate", labels)
        self.assertIn("ask_for_or_inspect_required_context_candidate", labels)
        self.assertIn("ambiguous_request_needs_router_check", mapped["route_family_candidates"])
        self.assertEqual(mapped["route_override"], "None")

    def test_fast_path_simple_explanation_stays_candidate_only(self) -> None:
        preview = self._preview("Just explain what this means in simple terms, no patch and no code.")
        labels = self._context_labels(preview)
        mapped = self._mapped_lines(preview)
        self.assertIn("fast_path_explanation_only_candidate", labels)
        self.assertEqual(mapped["candidate_contexts_only"], "True")
        self.assertEqual(mapped["automatic_prompt_loading"], "False")

    def test_render_function_returns_plain_text(self) -> None:
        preview = self._preview("Create a patch ZIP with install and validation blocks.")
        text = render_similarity_prompt_context_preview_text(preview)
        self.assertIsInstance(text, str)
        self.assertIn("Routing Signal Scorer v2 Prompt Context Preview", text)
        self.assertIn("candidate_prompt_contexts=", text)
        self.assertIn("preview_note=the canon decides required prompts", text)

    def test_prompt_context_preview_does_not_create_stronger_ml_files(self) -> None:
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
