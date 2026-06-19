from __future__ import annotations

import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ID = "routing_signal_scorer_v3_semantic_readiness_canon"
PROMPT_FILE = "routing_signal_scorer_v3_semantic_readiness_canon.md"
FEATURE_ID = "routing_signal_scorer_v3_semantic_readiness_canon_registration_v1"

class RoutingSignalScorerV3SemanticReadinessCanonRegistrationTests(unittest.TestCase):
    def test_prompt_asset_exists_and_is_on_request_semantic_canon(self) -> None:
        prompt = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / PROMPT_FILE
        self.assertTrue(prompt.exists(), prompt)
        text = prompt.read_text(encoding="utf-8")
        for phrase in ["# Routing Signal Scorer v3 Semantic Readiness Canon", "The semantic layer is an untrusted evidence witness.", "It may provide evidence.", "It may never provide authority.", "Metadata Vector Manifest", "Metadata eligibility gate", "Generated vector index policy", "External building block adoption policy", "Retrieval evaluation plan", "Fitness-function test matrix"]:
            self.assertIn(phrase, text)

    def test_metadata_registers_canon_without_startup_autoload(self) -> None:
        meta_path = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "METADATA" / f"{PROMPT_ID}.meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        self.assertEqual(meta["prompt_id"], PROMPT_ID)
        self.assertEqual(meta["load_type"], "on_request")
        self.assertTrue(meta["on_request_not_startup_always_loaded"])
        self.assertEqual(meta["semantic_layer_role"], "untrusted_evidence_witness")
        self.assertTrue(meta["requires_design_before_implementation"])
        self.assertIn("embeddings", meta["trigger_phrases"])
        self.assertIn("semantic retrieval", meta["trigger_phrases"])
        self.assertIn("vector index", meta["trigger_phrases"])
        self.assertIn("kanda_routing_system_canon", meta["required_companion_prompts"])
        self.assertIn("kanda_box_shielding_canon", meta["required_companion_prompts"])
        self.assertIn("router_override", meta["forbidden_authority"])
        self.assertIn("provider implementation", meta["forbidden_in_next_design_phase"])

    def test_human_and_machine_routing_indexes_include_the_canon(self) -> None:
        active_text = (PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md").read_text(encoding="utf-8")
        self.assertIn("## Routing Signal Scorer v3 semantic-readiness routing hook", active_text)
        self.assertIn(PROMPT_ID, active_text)
        self.assertIn("Metadata Vector Manifest", active_text)
        generated_text = (PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md").read_text(encoding="utf-8")
        self.assertIn(f"### `{PROMPT_ID}`", generated_text)
        self.assertIn("routing_signal_scorer v3", generated_text)
        machine = json.loads((PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ROUTING" / "prompt_navigation_index.json").read_text(encoding="utf-8"))
        matches = [entry for entry in machine["entries"] if entry.get("prompt_id") == PROMPT_ID]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["relative_path"], f"ACTIVE_PROMPTS/02_prompt_routing_and_indexing/{PROMPT_FILE}")
        self.assertEqual(entry["priority"], 2)
        self.assertIn("sentence-transformers", entry["trigger_phrases"])
        self.assertIn("GROUP_ASSIMILATION_INDEX", entry["required_companion_prompts"])

    def test_group_and_folder_indexes_route_semantic_readiness_work(self) -> None:
        group_index = json.loads((PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ROUTING" / "group_assimilation_index.json").read_text(encoding="utf-8"))
        group = next(item for item in group_index["groups"] if item["group_id"] == "02_prompt_routing_and_indexing")
        self.assertIn(PROMPT_FILE, group["main_prompts"])
        self.assertIn("semantic-readiness canonization", group["required_for"])
        self.assertIn("routing_signal_scorer v3", group["required_for"])
        route = next(item for item in group_index["task_routes"] if item.get("route_id") == "routing_signal_scorer_v3_semantic_readiness_route")
        self.assertIn(PROMPT_ID, route["required_prompts"])
        self.assertIn("kanda_box_shielding_canon", route["required_prompts"])
        folder_index = json.loads((PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ROUTING" / "folder_assimilation_cards_index.json").read_text(encoding="utf-8"))
        folder = next(item for item in folder_index["folders"] if item["folder_id"] == "02_prompt_routing_and_indexing")
        self.assertIn(PROMPT_ID, folder["main_prompt_ids"])
        self.assertIn(PROMPT_ID, folder["minimum_viable_context"])
        self.assertIn("embedding readiness", folder["common_task_triggers"])

    def test_ai_prompt_request_canon_has_exact_semantic_readiness_package(self) -> None:
        path = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("### Routing Signal Scorer v3 semantic-readiness exact context package", text)
        self.assertIn("routing_signal_scorer_v3_semantic_readiness_canon - required", text)
        self.assertIn("The semantic layer is an untrusted evidence witness", text)
        self.assertIn("Do not add embeddings, ML dependencies, provider code, vector indexes", text)
        self.assertIn("May proceed now: PARTIAL for read-only discussion", text)

    def test_startup_source_map_does_not_autoload_full_semantic_canon(self) -> None:
        source_map_path = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
        source_map = json.loads(source_map_path.read_text(encoding="utf-8"))
        sources = {entry["canonical_source"] for entry in source_map["startup_sources"]}
        self.assertNotIn(f"prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/{PROMPT_FILE}", sources)

    def test_no_runtime_ml_or_cross_box_files_were_added_by_registration(self) -> None:
        forbidden = [PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contracts" / "embedding_interfaces.py", PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "schemas" / "corpus_schema.json", PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "indices", PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "providers"]
        for path in forbidden:
            self.assertFalse(path.exists(), f"Forbidden semantic implementation artifact exists: {path}")

    def test_freeze_hint_documents_design_only_semantic_readiness_registration(self) -> None:
        hint_path = PROJECT_ROOT / "KANDA_FREEZE_HINT.json"
        if not hint_path.exists():
            self.skipTest("KANDA_FREEZE_HINT.json is ZIP delivery metadata and may not be installed in project root")
        hint = json.loads(hint_path.read_text(encoding="utf-8"))
        self.assertEqual(hint["feature_id"], FEATURE_ID)
        self.assertIn("no_ml_dependency_added", hint["protected_architecture_characteristics"])
        self.assertIn("no_embedding_provider_added", hint["protected_architecture_characteristics"])
        self.assertIn("kanda_reasoner_app/routing_signal_scorer", hint["patch_boundary"]["forbidden_paths"])
        self.assertIn("VALIDATION OK: routing_signal_scorer_v3_semantic_readiness_canon_registration_v1", hint["validation_evidence_summary"])

if __name__ == "__main__":
    unittest.main()
