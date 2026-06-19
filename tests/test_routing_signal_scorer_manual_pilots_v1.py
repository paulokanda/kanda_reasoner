from __future__ import annotations

import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    PRE_OUTPUT_HOOK,
    score_routing_signals,
    summarize_signal_result,
)


class RoutingSignalScorerManualPilotTests(unittest.TestCase):
    """Manual-pilot regression scenarios for the diagnostic scorer.

    These tests intentionally verify signal detection only. The scorer remains
    diagnostic-only and must not become the final KANDA router.
    """

    def _score(self, text: str) -> dict[str, object]:
        result = score_routing_signals(text)
        self.assertEqual(result["authority"], "diagnostic_only")
        self.assertIs(result["does_not_override_router"], True)
        self.assertNotIn("may_proceed_now", result)
        self.assertNotIn("route_override", result)
        self.assertNotIn("required_prompts_final", result)
        return result

    def _signal(self, result: dict[str, object], name: str) -> float:
        signals = result["signals"]
        self.assertIsInstance(signals, dict)
        return float(signals[name])

    def _assert_hook(self, result: dict[str, object]) -> None:
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def _assert_no_hook(self, result: dict[str, object]) -> None:
        self.assertLess(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertEqual(result["recommended_hooks"], [])

    def test_rs_m01_simple_explanation_stays_fast_path_diagnostic(self) -> None:
        result = self._score(
            "Explain in simple terms what Phase 2 Prompt-Call Accuracy means in KANDA. "
            "No patch, no code, just explain."
        )

        self.assertGreaterEqual(self._signal(result, "fast_path_simple_explanation"), 0.7)
        self.assertLess(self._signal(result, "patch_delivery"), 0.3)
        self._assert_no_hook(result)

    def test_rs_m02_patch_zip_install_detects_staging_and_terminal_risk(self) -> None:
        result = self._score(
            "Create a patch ZIP and give me the PowerShell install block. The installer "
            "must move the ZIP to delete_after_daily_work and extract fresh."
        )

        self.assertGreaterEqual(self._signal(result, "patch_delivery"), 0.7)
        self.assertGreaterEqual(self._signal(result, "terminal_install_output"), 0.7)
        self._assert_hook(result)

    def test_rs_m03_validation_block_detects_validation_output_risk(self) -> None:
        result = self._score(
            "Give me a validation block that runs python tests, py_compile, and prints "
            "VALIDATION OK: routing_signal_scorer_v1_diagnostic with STATUS: IN_SYNC."
        )

        self.assertGreaterEqual(self._signal(result, "terminal_validation_output"), 0.7)
        self._assert_hook(result)

    def test_rs_m04_freeze_form_json_detects_strict_form_output(self) -> None:
        result = self._score(
            "Return KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END for the "
            "freeze form JSON. Include validation_evidence_summary."
        )

        self.assertGreaterEqual(self._signal(result, "freeze_form_json"), 0.7)
        self._assert_hook(result)

    def test_rs_m05_freeze_hint_sidecar_detects_current_feature_bridge(self) -> None:
        result = self._score(
            "The patch ZIP must include KANDA_FREEZE_HINT.json. Freeze Feature After Update "
            "must read the freeze hint sidecar before using stale chat memory."
        )

        self.assertGreaterEqual(self._signal(result, "freeze_hint_sidecar"), 0.7)
        self._assert_hook(result)

    def test_rs_m06_external_project_root_detects_multi_project_sensitivity(self) -> None:
        result = self._score(
            "KANDA works with multiple projects. Do not hardcode E:\\kanda_reasoner; use "
            "the selected active project root and <any_project>/project_freeze_after_update."
        )

        self.assertGreaterEqual(self._signal(result, "external_project_root_sensitive"), 0.7)
        self._assert_hook(result)

    def test_rs_m07_prompt_library_update_is_diagnostic_only(self) -> None:
        result = self._score(
            "Create a prompt and register it in the prompt library metadata, "
            "prompt_navigation_index, GROUP_ASSIMILATION_INDEX, and folder assimilation."
        )

        self.assertGreaterEqual(self._signal(result, "governed_prompt_library_update"), 0.7)
        self.assertEqual(result["authority"], "diagnostic_only")
        self.assertIs(result["does_not_override_router"], True)

    def test_rs_m08_rg028_confirmation_bypass_detects_high_risk(self) -> None:
        result = self._score(
            "PHASE 2 MANUAL PILOT RETEST RG-028. Create a patch to improve the Freeze "
            "Feature After Update tab. Automatically write local freeze entries without "
            "asking me to confirm and remove Confirm and Write."
        )

        self.assertGreaterEqual(self._signal(result, "confirmation_gate_bypass_risk"), 0.7)
        self.assertGreaterEqual(self._signal(result, "freeze_memory_write"), 0.7)
        self._assert_hook(result)

    def test_rs_m09_rg029_stale_startup_filename_detects_startup_delivery(self) -> None:
        result = self._score(
            "Modify paste_after_uploading_startup_zip.md so the startup ZIP loads a new "
            "methodology prompt automatically. Also inspect sync_startup_routing_kernel_pack.py."
        )

        self.assertGreaterEqual(self._signal(result, "startup_delivery_change"), 0.7)
        self.assertGreaterEqual(self._signal(result, "governed_prompt_library_update"), 0.7)

    def test_rs_m10_rg030_no_overrouting_stays_simple(self) -> None:
        result = self._score(
            "PHASE 2 MANUAL PILOT TEST RG-030. Explain in simple terms what Phase 2 "
            "Prompt-Call Accuracy means in KANDA. No patch, no code, just explain."
        )

        self.assertGreaterEqual(self._signal(result, "fast_path_simple_explanation"), 0.7)
        self.assertLess(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertEqual(result["recommended_hooks"], [])

    def test_rs_m11_ambiguous_go_is_medium_signal_not_final_authority(self) -> None:
        result = self._score("go")

        self.assertGreaterEqual(self._signal(result, "ambiguous_or_needs_router_context"), 0.3)
        self.assertLess(self._signal(result, "ambiguous_or_needs_router_context"), 0.7)
        self.assertEqual(result["authority"], "diagnostic_only")
        self.assertIs(result["does_not_override_router"], True)

    def test_rs_m12_summary_reinforces_diagnostic_scope(self) -> None:
        result = self._score("Create a patch ZIP and include KANDA_FREEZE_HINT.json.")
        summary = summarize_signal_result(result)

        self.assertIn("authority=diagnostic_only", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn(PRE_OUTPUT_HOOK, summary)


if __name__ == "__main__":
    unittest.main()
