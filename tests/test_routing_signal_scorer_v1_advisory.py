from __future__ import annotations

import unittest

from kanda_reasoner_app.routing_signal_scorer.contract import (
    ADVISORY_AUTHORITY,
    ADVISORY_FEATURE_ID,
    PRE_OUTPUT_HOOK,
    build_routing_advisory,
    score_routing_signals,
    summarize_advisory,
)


class RoutingSignalScorerAdvisoryTests(unittest.TestCase):
    """Advisory-mode tests for the routing signal scorer.

    Advisory mode may suggest likely route families, hooks, and caution flags.
    It must not become the final KANDA router.
    """

    def _advisory(self, text: str) -> dict[str, object]:
        advisory = build_routing_advisory(text)
        self.assertEqual(advisory["schema_version"], "1.1")
        self.assertEqual(advisory["feature_id"], ADVISORY_FEATURE_ID)
        self.assertEqual(advisory["authority"], ADVISORY_AUTHORITY)
        self.assertIs(advisory["does_not_override_router"], True)
        self.assertIs(advisory["canon_decides_final_route"], True)
        self.assertEqual(advisory["may_proceed_now_decision"], "not_provided_by_advisory")
        self.assertIsNone(advisory["route_override"])
        self.assertNotIn("may_proceed_now", advisory)
        self.assertNotIn("required_prompts_final", advisory)
        return advisory

    def _families(self, advisory: dict[str, object]) -> set[str]:
        suggestions = advisory["suggested_route_families"]
        self.assertIsInstance(suggestions, list)
        return {str(item["family"]) for item in suggestions if isinstance(item, dict)}

    def _flags(self, advisory: dict[str, object]) -> set[str]:
        flags = advisory["caution_flags"]
        self.assertIsInstance(flags, list)
        return {str(item) for item in flags}

    def test_advisory_fast_path_candidate_stays_non_authoritative(self) -> None:
        advisory = self._advisory(
            "Explain in simple terms what Phase 2 Prompt-Call Accuracy means in KANDA. "
            "No patch, no code, just explain."
        )

        self.assertIn("fast_path_simple_explanation", self._families(advisory))
        self.assertIn("fast_path_candidate_only", self._flags(advisory))
        self.assertEqual(advisory["recommended_hooks"], [])

    def test_advisory_patch_delivery_recommends_contract_gate(self) -> None:
        advisory = self._advisory(
            "Create a patch ZIP and give me the PowerShell install block. The installer "
            "must move the ZIP to delete_after_daily_work and extract fresh."
        )

        families = self._families(advisory)
        self.assertIn("patch_delivery_or_code_update", families)
        self.assertIn("terminal_install_artifact", families)
        self.assertIn(PRE_OUTPUT_HOOK, advisory["recommended_hooks"])
        self.assertIn("pre_output_contract_gate_recommended", self._flags(advisory))

    def test_advisory_freeze_form_json_recommends_contract_gate(self) -> None:
        advisory = self._advisory(
            "Return KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END for "
            "the freeze form JSON. Include validation_evidence_summary."
        )

        self.assertIn("freeze_form_json_artifact", self._families(advisory))
        self.assertIn(PRE_OUTPUT_HOOK, advisory["recommended_hooks"])

    def test_advisory_confirmation_gate_bypass_is_flagged(self) -> None:
        advisory = self._advisory(
            "Create a patch to improve Freeze Feature After Update. Automatically write "
            "local freeze entries without asking me to confirm and remove Confirm and Write."
        )

        families = self._families(advisory)
        flags = self._flags(advisory)
        self.assertIn("protected_confirmation_gate_risk", families)
        self.assertIn("freeze_memory_workflow", families)
        self.assertIn("confirmation_gate_bypass_risk", flags)
        self.assertIn(PRE_OUTPUT_HOOK, advisory["recommended_hooks"])

    def test_advisory_startup_delivery_and_prompt_library_are_governed_hints(self) -> None:
        advisory = self._advisory(
            "Modify paste_after_first_prompts_to_ai.md and sync_startup_routing_kernel_pack.py "
            "to add a prompt to the prompt library and startup ZIP."
        )

        families = self._families(advisory)
        flags = self._flags(advisory)
        self.assertIn("startup_delivery_update", families)
        self.assertIn("prompt_library_or_routing_update", families)
        self.assertIn("startup_delivery_governance_needed", flags)
        self.assertIn("prompt_library_governance_needed", flags)

    def test_advisory_multi_project_path_sensitivity_is_flagged(self) -> None:
        advisory = self._advisory(
            "KANDA works with multiple projects. Do not hardcode E:\\kanda_reasoner. "
            "Use the selected active project root and <any_project>/project_freeze_after_update."
        )

        self.assertIn("multi_project_path_sensitive", self._families(advisory))
        self.assertIn("multi_project_path_sensitive", self._flags(advisory))

    def test_advisory_wraps_source_diagnostic_without_changing_it(self) -> None:
        text = "Create a patch ZIP and include KANDA_FREEZE_HINT.json."
        diagnostic = score_routing_signals(text)
        advisory = self._advisory(text)

        self.assertEqual(advisory["source_diagnostic"]["authority"], "diagnostic_only")
        self.assertEqual(advisory["source_diagnostic"]["signals"], diagnostic["signals"])
        self.assertIs(advisory["source_diagnostic"]["does_not_override_router"], True)

    def test_advisory_summary_restates_limits(self) -> None:
        advisory = self._advisory("Create a patch ZIP and include KANDA_FREEZE_HINT.json.")
        summary = summarize_advisory(advisory)

        self.assertIn("authority=advisory_only", summary)
        self.assertIn("does_not_override_router=True", summary)
        self.assertIn("canon_decides_final_route=True", summary)
        self.assertIn("may_proceed_now_decision=not_provided_by_advisory", summary)


if __name__ == "__main__":
    unittest.main()
