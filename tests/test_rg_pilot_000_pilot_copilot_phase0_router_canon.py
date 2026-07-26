from __future__ import annotations

import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
PROMPT_ID = "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon"
PROMPT_FILE = "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md"
FEATURE_ID = "rg_pilot_000_pilot_copilot_phase0_router_canon_v1"

CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / PROMPT_FILE
META = PROMPT_ROOT / "METADATA" / f"{PROMPT_ID}.meta.json"
ACTIVE_NAV = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
PROMPT_ROUTER = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md"
AI_PROMPT_REQUEST_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md"
FOLDER_CARD = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "_FOLDER_ASSIMILATION.md"
ROUTING_NAV = PROMPT_ROOT / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md"
PROMPT_NAV_JSON = PROMPT_ROOT / "ROUTING" / "prompt_navigation_index.json"
GROUP_JSON = PROMPT_ROOT / "ROUTING" / "group_assimilation_index.json"
FOLDER_JSON = PROMPT_ROOT / "ROUTING" / "folder_assimilation_cards_index.json"
SOURCE_MAP = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"


class RgPilot000PilotCopilotPhase0RouterCanonTests(unittest.TestCase):
    def test_canon_prompt_exists_and_contains_hard_rules(self) -> None:
        text = CANON.read_text(encoding="utf-8")
        required = [
            "# RG-PILOT-000 - Pilot/Copilot Phase 0 Router Canon",
            "P0 - Routing Signal Scorer v3 Pilot/Copilot Scope Charter and Entry Gate Design v1",
            "P0 first-position hard override",
            "Projection-not-recommendation rule",
            "Prompt-loading leakage rule",
            "human_review_mandatory = True",
            "ROUTING_EFFECT = \"none\"",
            "Opt-in, ephemeral, no-training, no-batch rules",
            "Reproduction-before-disagreement rule",
            "The phrase \"Limited Shadow Runtime\" must not appear in P0-P12 as an implementation target.",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_metadata_registers_on_request_not_startup_canon(self) -> None:
        data = json.loads(META.read_text(encoding="utf-8"))
        self.assertEqual(data["prompt_id"], PROMPT_ID)
        self.assertEqual(data["category"], "02_prompt_routing_and_indexing")
        self.assertEqual(data["load_type"], "on_request")
        self.assertTrue(data["on_request_not_startup_always_loaded"])
        self.assertTrue(data["requires_p0_before_pilot_implementation"])
        self.assertIn("Pilot/Copilot Phase 0", data["trigger_phrases"])
        self.assertIn("Limited Shadow Runtime", data["trigger_phrases"])
        self.assertIn("kanda_routing_system_canon", data["required_companion_prompts"])
        self.assertIn("kanda_box_shielding_canon", data["required_companion_prompts"])
        self.assertIn("runtime_integration", data["forbidden_authority"])
        self.assertIn("training_data_use", data["forbidden_authority"])
        self.assertIn("Limited Shadow Runtime", data["forbidden_in_next_design_phase"])

    def test_human_routing_assets_register_rg_pilot_000(self) -> None:
        for path in [ACTIVE_NAV, PROMPT_ROUTER, AI_PROMPT_REQUEST_CANON, FOLDER_CARD, ROUTING_NAV]:
            text = path.read_text(encoding="utf-8")
            self.assertIn(PROMPT_ID, text, msg=str(path))
            self.assertIn("Pilot/Copilot Phase 0", text, msg=str(path))
        text = ACTIVE_NAV.read_text(encoding="utf-8")
        self.assertIn("## RG-PILOT-000 Pilot/Copilot Phase 0 routing hook", text)
        self.assertIn("P0 only", text)
        self.assertIn("reproduce frozen router/canon outcomes before disagreement evidence is trusted", text)

    def test_machine_prompt_navigation_registers_single_entry(self) -> None:
        data = json.loads(PROMPT_NAV_JSON.read_text(encoding="utf-8"))
        self.assertEqual(data["prompt_count"], len(data["entries"]))
        matches = [entry for entry in data["entries"] if entry.get("prompt_id") == PROMPT_ID]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["relative_path"], f"ACTIVE_PROMPTS/02_prompt_routing_and_indexing/{PROMPT_FILE}")
        self.assertEqual(entry["priority"], 1)
        self.assertIn("create P0", entry["trigger_phrases"])
        self.assertIn("reproduction-before-disagreement", entry["trigger_phrases"])
        self.assertIn("GROUP_ASSIMILATION_INDEX", entry["required_companion_prompts"])

    def test_group_and_folder_indexes_route_pilot_phase0(self) -> None:
        group_data = json.loads(GROUP_JSON.read_text(encoding="utf-8"))
        group = next(item for item in group_data["groups"] if item["group_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(group["prompt_count"], len(group["main_prompts"]))
        self.assertIn(PROMPT_FILE, group["main_prompts"])
        self.assertIn("P0 scope charter routing", group["required_for"])
        route = next(item for item in group_data["task_routes"] if item.get("route_id") == "routing_signal_scorer_v3_pilot_copilot_phase0_route")
        self.assertIn(PROMPT_ID, route["required_prompts"])
        self.assertIn("kanda_box_shielding_canon", route["required_prompts"])

        folder_data = json.loads(FOLDER_JSON.read_text(encoding="utf-8"))
        folder = next(item for item in folder_data["folders"] if item["folder_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(folder["prompt_count"], len(folder["main_prompt_ids"]))
        self.assertIn(PROMPT_ID, folder["main_prompt_ids"])
        self.assertIn(PROMPT_ID, folder["minimum_viable_context"])
        self.assertIn("P0 scope charter", folder["common_task_triggers"])

    def test_ai_prompt_request_canon_has_exact_rg_pilot_package(self) -> None:
        text = AI_PROMPT_REQUEST_CANON.read_text(encoding="utf-8")
        self.assertIn("### RG-PILOT-000 Pilot/Copilot Phase 0 exact context package", text)
        self.assertIn("routing_signal_scorer_v3_pilot_copilot_phase0_router_canon - required", text)
        self.assertIn("If P0 is not yet validated and frozen, the next implementation milestone is P0 only.", text)
        self.assertIn("Do not implement Pilot before P0-P6 gates allow it.", text)
        self.assertIn("Limited Shadow Runtime", text)

    def test_startup_source_map_does_not_autoload_full_rg_pilot_canon(self) -> None:
        source_map = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
        sources = {entry["canonical_source"] for entry in source_map["startup_sources"]}
        self.assertNotIn(
            f"prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/{PROMPT_FILE}",
            sources,
        )

    def test_no_runtime_or_pilot_implementation_files_added_by_registration(self) -> None:
        forbidden = [
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "pilot_copilot",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "pilot_runtime",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "copilot_runtime",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "prompt_loader",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers",
            PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "embeddings",
        ]
        for path in forbidden:
            self.assertFalse(path.exists(), f"Forbidden Pilot/Copilot implementation artifact exists: {path}")

    def test_freeze_hint_documents_router_canon_registration(self) -> None:
        hint_path = PROJECT_ROOT / "KANDA_FREEZE_HINT.json"
        if not hint_path.exists():
            self.skipTest("KANDA_FREEZE_HINT.json is ZIP delivery metadata and may not be installed in project root")
        hint = json.loads(hint_path.read_text(encoding="utf-8"))
        self.assertEqual(hint["feature_id"], FEATURE_ID)
        self.assertIn("no_pilot_implementation_added", hint["protected_architecture_characteristics"])
        self.assertIn("no_runtime_authority_added", hint["protected_architecture_characteristics"])
        self.assertIn("VALIDATION OK: rg_pilot_000_pilot_copilot_phase0_router_canon_v1", hint["validation_evidence_summary"])


if __name__ == "__main__":
    unittest.main()
