from __future__ import annotations

import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    AUTHORITY,
    FEATURE_ID,
    PRE_OUTPUT_HOOK,
    score_routing_signals,
    summarize_signal_result,
)


class RoutingSignalScorerDiagnosticTests(unittest.TestCase):
    def _score(self, text: str) -> dict[str, object]:
        result = score_routing_signals(text)
        self.assertEqual(result["schema_version"], "1.0")
        self.assertEqual(result["feature_id"], FEATURE_ID)
        self.assertEqual(result["authority"], AUTHORITY)
        self.assertIs(result["does_not_override_router"], True)
        self.assertNotIn("may_proceed_now", result)
        self.assertNotIn("route_override", result)
        return result

    def _signal(self, result: dict[str, object], name: str) -> float:
        signals = result["signals"]
        self.assertIsInstance(signals, dict)
        return float(signals[name])

    def test_simple_explanation_is_fast_path_signal_without_contract_gate(self) -> None:
        result = self._score(
            "Explain in simple terms what Phase 2 Prompt-Call Accuracy means in KANDA. "
            "No patch, no code, just explain."
        )

        self.assertGreaterEqual(self._signal(result, "fast_path_simple_explanation"), 0.7)
        self.assertLess(self._signal(result, "patch_delivery"), 0.3)
        self.assertLess(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertEqual(result["recommended_hooks"], [])

    def test_patch_zip_install_request_recommends_pre_output_contract_gate(self) -> None:
        result = self._score(
            "Create a patch ZIP and give me the PowerShell install block. The installer "
            "must move the ZIP to delete_after_daily_work and extract fresh."
        )

        self.assertGreaterEqual(self._signal(result, "patch_delivery"), 0.7)
        self.assertGreaterEqual(self._signal(result, "terminal_install_output"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_validation_command_request_recommends_contract_gate(self) -> None:
        result = self._score(
            "Give me a validation block that runs python tests and prints "
            "VALIDATION OK: routing_signal_scorer_v1_diagnostic with STATUS: IN_SYNC."
        )

        self.assertGreaterEqual(self._signal(result, "terminal_validation_output"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_freeze_form_json_request_is_detected(self) -> None:
        result = self._score(
            "Return KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END for the "
            "freeze form JSON. Include validation_evidence_summary."
        )

        self.assertGreaterEqual(self._signal(result, "freeze_form_json"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)
        self.assertIn(PRE_OUTPUT_HOOK, result["recommended_hooks"])

    def test_freeze_hint_sidecar_and_memory_write_are_detected(self) -> None:
        result = self._score(
            "The patch ZIP must include KANDA_FREEZE_HINT.json. Then Freeze Feature After "
            "Update uses Confirm and Write to create a local freeze entry under "
            "project_freeze_after_update/frozen_features_memory."
        )

        self.assertGreaterEqual(self._signal(result, "freeze_hint_sidecar"), 0.7)
        self.assertGreaterEqual(self._signal(result, "freeze_memory_write"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)

    def test_external_project_root_sensitive_request_is_detected(self) -> None:
        result = self._score(
            "KANDA works with multiple projects. Do not hardcode E:\\kanda_reasoner; use the "
            "selected active project root and <any_project>/project_freeze_after_update."
        )

        self.assertGreaterEqual(self._signal(result, "external_project_root_sensitive"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)

    def test_prompt_library_update_is_detected_without_final_routing_authority(self) -> None:
        result = self._score(
            "Create a prompt and register it in the prompt library metadata and "
            "prompt_navigation_index."
        )

        self.assertGreaterEqual(self._signal(result, "governed_prompt_library_update"), 0.7)
        self.assertEqual(result["authority"], "diagnostic_only")
        self.assertIs(result["does_not_override_router"], True)

    def test_rg028_confirmation_bypass_scenario_is_high_risk(self) -> None:
        result = self._score(
            "Create a patch to improve the Freeze Feature After Update tab. I want the GUI "
            "to automatically write local freeze entries without asking me to confirm. "
            "Remove Confirm and Write."
        )

        self.assertGreaterEqual(self._signal(result, "confirmation_gate_bypass_risk"), 0.7)
        self.assertGreaterEqual(self._signal(result, "freeze_memory_write"), 0.7)
        self.assertGreaterEqual(self._signal(result, "pre_output_contract_gate_required"), 0.7)

    def test_startup_delivery_change_is_detected(self) -> None:
        result = self._score(
            "Modify paste_after_first_prompts_to_ai.md and sync_startup_routing_kernel_pack.py "
            "so the startup ZIP changes."
        )

        self.assertGreaterEqual(self._signal(result, "startup_delivery_change"), 0.7)
        self.assertGreaterEqual(self._signal(result, "governed_prompt_library_update"), 0.7)

    def test_summary_is_plain_and_reiterates_diagnostic_only_authority(self) -> None:
        result = self._score("Create a patch ZIP and include KANDA_FREEZE_HINT.json.")
        summary = summarize_signal_result(result)

        self.assertIn("authority=diagnostic_only", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn(PRE_OUTPUT_HOOK, summary)


if __name__ == "__main__":
    unittest.main()
