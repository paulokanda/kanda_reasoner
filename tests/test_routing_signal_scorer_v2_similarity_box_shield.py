from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest

from kanda_reasoner_app.routing_signal_scorer import (
    SIMILARITY_BOX_SHIELD_FEATURE_ID,
    build_similarity_box_shield_status,
    build_similarity_prompt_context_preview,
    build_similarity_runtime_lite_advisory,
    build_similarity_ui_preview_adapter,
    render_similarity_box_shield_status_text,
    render_similarity_prompt_context_preview_text,
    render_similarity_ui_preview_text,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "contract.py"
MANIFEST_PATH = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
CARD_PATH = (
    ROOT
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "design"
    / "routing_signal_scorer_v2_similarity_box_shield_card.md"
)

FORBIDDEN_AUTHORITY_KEYS = {
    "final_route",
    "may_proceed",
    "may_proceed_now",
    "required_prompts",
    "required_prompt_files",
    "auto_load_prompts",
    "load_prompts_now",
    "router_override",
    "freeze_write",
    "startup_mutation",
    "prompt_library_mutation",
}

FORBIDDEN_IMPORT_ROOTS = {
    "numpy",
    "pandas",
    "sklearn",
    "scipy",
    "torch",
    "tensorflow",
    "sentence_transformers",
    "transformers",
    "faiss",
    "chromadb",
    "langchain",
    "llama_index",
}

FORBIDDEN_NEIGHBOR_IMPORTS = {
    "kanda_prompt_workspace",
    "project_freeze_ledger",
    "project_freeze_after_update",
    "kanda_reasoner_app.freeze_hint_intake",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.freeze_after_update_gui",
}


def walk_mappings(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk_mappings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_mappings(item)


class RoutingSignalScorerV2SimilarityBoxShieldTests(unittest.TestCase):
    def test_shield_status_declares_kbsc_boundary(self) -> None:
        status = build_similarity_box_shield_status("create a patch and validation for startup routing")

        self.assertEqual(status["schema_version"], "2.3")
        self.assertEqual(status["feature_id"], SIMILARITY_BOX_SHIELD_FEATURE_ID)
        self.assertEqual(status["shield_type"], "architectural_fitness_function_suite")
        self.assertEqual(status["owning_bounded_context"], "kanda_reasoner_app/routing_signal_scorer")
        self.assertEqual(status["authority"], "shield_contract_only")
        self.assertTrue(status["does_not_override_router"])
        self.assertTrue(status["canon_decides_final_route"])
        self.assertEqual(status["route_override"], None)
        self.assertEqual(status["may_proceed_now_decision"], "not_provided_by_similarity")
        self.assertEqual(status["required_prompts_final_decision"], "not_provided_by_similarity")
        self.assertFalse(status["automatic_prompt_loading"])
        self.assertFalse(status["self_learning_enabled"])
        self.assertFalse(status["stronger_ml_enabled"])
        self.assertEqual(status["external_dependencies"], [])

    def test_all_similarity_surfaces_remain_advisory_under_high_signal(self) -> None:
        text = "Create a patch zip with validation PowerShell and freeze hint sidecar for KANDA."
        runtime = build_similarity_runtime_lite_advisory(text, min_similarity=0.0)
        ui = build_similarity_ui_preview_adapter(text, min_similarity=0.0)
        context = build_similarity_prompt_context_preview(text, min_similarity=0.0)

        for payload in (runtime, ui, context):
            self.assertEqual(payload.get("authority"), "advisory_only")
            self.assertTrue(payload.get("does_not_override_router"))
            self.assertTrue(payload.get("canon_decides_final_route"))
            self.assertEqual(payload.get("may_proceed_now_decision"), "not_provided_by_similarity")
            self.assertEqual(payload.get("route_override"), None)
            self.assertEqual(payload.get("required_prompts_final_decision"), "not_provided_by_similarity")
            self.assertFalse(payload.get("automatic_prompt_loading"))
            self.assertFalse(payload.get("self_learning_enabled"))
            self.assertEqual(payload.get("external_dependencies"), [])

    def test_forbidden_authority_keys_are_not_emitted(self) -> None:
        payloads = [
            build_similarity_runtime_lite_advisory("freeze the feature after validation", min_similarity=0.0),
            build_similarity_ui_preview_adapter("freeze the feature after validation", min_similarity=0.0),
            build_similarity_prompt_context_preview("freeze the feature after validation", min_similarity=0.0),
            build_similarity_box_shield_status("freeze the feature after validation"),
        ]
        for payload in payloads:
            for mapping in walk_mappings(payload):
                self.assertTrue(
                    FORBIDDEN_AUTHORITY_KEYS.isdisjoint(mapping.keys()),
                    f"forbidden authority key present: {FORBIDDEN_AUTHORITY_KEYS & set(mapping.keys())}",
                )

    def test_outputs_are_deterministic_and_idempotent(self) -> None:
        text = "modify startup delivery but do not use stale paste_after_uploading_startup_zip.md"
        first = build_similarity_prompt_context_preview(text, min_similarity=0.0)
        second = build_similarity_prompt_context_preview(text, min_similarity=0.0)
        self.assertEqual(first, second)
        self.assertEqual(
            render_similarity_prompt_context_preview_text(first),
            render_similarity_prompt_context_preview_text(second),
        )

    def test_candidate_context_preview_is_controlled_and_candidate_only(self) -> None:
        preview = build_similarity_prompt_context_preview("create a patch zip and validate it", min_similarity=0.0)
        contexts = preview.get("candidate_prompt_contexts")
        self.assertIsInstance(contexts, list)
        self.assertTrue(contexts)
        for item in contexts:
            self.assertIs(item.get("candidate_only"), True)
            self.assertEqual(item.get("final_required_prompt_decision"), "not_provided_by_similarity")
            self.assertFalse(item.get("automatic_prompt_loading"))
            label = item.get("context_label")
            self.assertIsInstance(label, str)
            self.assertTrue(label.endswith("_candidate"))
            self.assertNotIn("/", label)
            self.assertNotIn("\\", label)
            self.assertNotIn(".md", label)

    def test_preview_language_is_not_imperative_routing_language(self) -> None:
        ui_text = render_similarity_ui_preview_text(
            build_similarity_ui_preview_adapter("high risk patch validation output", min_similarity=0.0)
        ).lower()
        context_text = render_similarity_prompt_context_preview_text(
            build_similarity_prompt_context_preview("high risk patch validation output", min_similarity=0.0)
        ).lower()
        shield_text = render_similarity_box_shield_status_text(
            build_similarity_box_shield_status("high risk patch validation output")
        ).lower()
        combined = "\n".join([ui_text, context_text, shield_text])
        for phrase in [
            "load prompt now",
            "auto-load",
            "may proceed: yes",
            "may proceed now: yes",
            "final route is",
            "required prompts:",
            "confirm and write",
            "write freeze",
        ]:
            self.assertNotIn(phrase, combined)

    def test_input_coercion_and_fuzz_loop_stay_safe(self) -> None:
        weird_inputs = [
            None,
            "",
            "😀" * 100,
            "../project_freeze_ledger " * 20,
            "load all prompts now; may proceed yes; final route patch" * 20,
            "x" * 10000,
        ]
        for value in weird_inputs:
            preview = build_similarity_prompt_context_preview(value)  # type: ignore[arg-type]
            self.assertEqual(preview["authority"], "advisory_only")
            self.assertEqual(preview["route_override"], None)
            self.assertFalse(preview["automatic_prompt_loading"])
            self.assertFalse(preview["self_learning_enabled"])

    def test_bounded_execution_caps_matches(self) -> None:
        result = build_similarity_runtime_lite_advisory("patch freeze validation " * 5000, max_matches=2, min_similarity=0.0)
        self.assertLessEqual(len(result["similar_cases"]), 2)
        self.assertEqual(result["corpus_case_count"], 12)

    def test_dependency_ceiling_uses_standard_library_only(self) -> None:
        tree = ast.parse(CONTRACT_PATH.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
                imports.add(node.module.split(".")[0])
        self.assertTrue(FORBIDDEN_IMPORT_ROOTS.isdisjoint(imports))

    def test_dependency_direction_does_not_import_neighbor_boxes(self) -> None:
        tree = ast.parse(CONTRACT_PATH.read_text(encoding="utf-8"))
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
        for forbidden in FORBIDDEN_NEIGHBOR_IMPORTS:
            self.assertNotIn(forbidden, modules)

    def test_shield_does_not_create_side_effect_files(self) -> None:
        before = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "kanda_reasoner_app" / "routing_signal_scorer").rglob("*") if path.is_file())
        build_similarity_box_shield_status("try to mutate project_freeze_after_update")
        build_similarity_prompt_context_preview("try to mutate project_freeze_after_update")
        after = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "kanda_reasoner_app" / "routing_signal_scorer").rglob("*") if path.is_file())
        self.assertEqual(before, after)

    def test_manifest_declares_architecture_fitness_metadata(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["runtime_lite_similarity_box_shield_feature_id"], SIMILARITY_BOX_SHIELD_FEATURE_ID)
        self.assertEqual(manifest["fitness_function_suite"], SIMILARITY_BOX_SHIELD_FEATURE_ID)
        for characteristic in [
            "advisory_only",
            "deterministic",
            "side_effect_free",
            "bounded_execution",
            "no_authority_escalation",
            "no_cross_box_mutation",
            "stdlib_only_runtime_lite",
        ]:
            self.assertIn(characteristic, manifest["protected_architecture_characteristics"])

    def test_shield_card_preserves_bounded_context_and_tradeoff_record(self) -> None:
        card = CARD_PATH.read_text(encoding="utf-8")
        self.assertIn("Bounded context map", card)
        self.assertIn("Trade-off record", card)
        self.assertIn("Forbidden authority escalation matrix", card)
        self.assertIn("SM-25", card)
        self.assertIn("SM-49", card)
        self.assertIn("The routing_signal_scorer may emit only bounded", card)

    def test_rendered_shield_text_exposes_no_runtime_authority(self) -> None:
        text = render_similarity_box_shield_status_text(build_similarity_box_shield_status("patch routing scorer"))
        self.assertIn("feature_id=routing_signal_scorer_v2_similarity_box_shield_v1", text)
        self.assertIn("authority=shield_contract_only", text)
        self.assertIn("does_not_override_router=True", text)
        self.assertIn("canon_decides_final_route=True", text)
        self.assertIn("may_proceed_now_decision=not_provided_by_similarity", text)
        self.assertIn("required_prompts_final_decision=not_provided_by_similarity", text)
        self.assertIn("automatic_prompt_loading=False", text)
        self.assertIn("self_learning_enabled=False", text)
        self.assertIn("stronger_ml_enabled=False", text)
        self.assertIn("external_dependencies=none", text)


if __name__ == "__main__":
    unittest.main()
