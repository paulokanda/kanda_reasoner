import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
DESIGN = ADVISER / "design" / "candidate_v0_offline_lexical_scorer"
FEATURE_ID = "routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_design_v1"
SCHEMA_VERSION = "3.51-adviser-candidate-v0-offline-lexical-scorer-design"


class AdviserCandidateV0OfflineLexicalScorerDesignTests(unittest.TestCase):
    def test_m10_design_files_remain_and_m11_may_add_exact_offline_candidate(self):
        for path in (
            DESIGN / "README.md",
            DESIGN / "candidate_v0_offline_lexical_scorer_design.md",
            DESIGN / "candidate_v0_offline_lexical_scorer_design_spec.json",
        ):
            self.assertTrue(path.exists(), path)

        # M10 froze a design-only boundary. M11 is the separate governed milestone
        # that may add the exact offline candidate module, but still no candidate
        # outputs, scratch space, generic scorer package, or runtime behavior.
        allowed_m11_candidate = ADVISER / "candidate_v0" / "offline_lexical_scorer.py"
        if allowed_m11_candidate.exists():
            self.assertTrue(allowed_m11_candidate.read_text(encoding="utf-8").startswith(
                '"""Offline deterministic lexical Adviser Candidate v0.'
            ))

        for forbidden in (
            ADVISER / "candidate",
            ADVISER / "scorers",
            ADVISER / "test_data" / "candidate_outputs",
            ADVISER / "scratch",
        ):
            self.assertFalse(forbidden.exists(), forbidden)

    def test_design_spec_declares_future_lexical_baseline_only(self):
        spec = json.loads((DESIGN / "candidate_v0_offline_lexical_scorer_design_spec.json").read_text(encoding="utf-8"))
        self.assertEqual(spec["schema_version"], SCHEMA_VERSION)
        self.assertEqual(spec["feature_id"], FEATURE_ID)
        self.assertEqual(spec["status"], "design_only_not_implemented")
        self.assertEqual(spec["authority_statement"], "candidate_v0_design_only_no_candidate_execution_no_router_authority")
        self.assertFalse(spec["roadmap_position"]["candidate_exists_after_m10"])
        self.assertFalse(spec["roadmap_position"]["candidate_outputs_exist_after_m10"])
        self.assertEqual(spec["designed_future_candidate"]["candidate_kind"], "offline_deterministic_lexical_baseline")
        self.assertEqual(spec["designed_future_candidate"]["implementation_status"], "not_implemented_in_m10")
        self.assertIn("YES", spec["designed_future_candidate"]["forbidden_advisory_proceed_values"])
        self.assertIn("AUTO_PROCEED", spec["designed_future_candidate"]["forbidden_advisory_proceed_values"])
        self.assertIn("ABSTAIN", spec["designed_future_candidate"]["default_safe_outputs_future"])
        self.assertIn("OUT_OF_SCOPE", spec["designed_future_candidate"]["default_safe_outputs_future"])

    def test_design_spec_covers_seed_gold_case_families_and_priority_order(self):
        spec = json.loads((DESIGN / "candidate_v0_offline_lexical_scorer_design_spec.json").read_text(encoding="utf-8"))
        self.assertEqual(set(spec["future_lexical_families"]), {
            "freeze_workflow",
            "patch_delivery",
            "box_boundary",
            "startup_delivery",
            "prompt_library",
            "routing_signal_scorer",
            "adversarial_bypass",
            "ambiguous",
            "false_positive",
            "out_of_scope",
        })
        priority = spec["future_priority_order"]
        self.assertEqual(priority[0], "critical_bypass_or_authority_promotion")
        self.assertLess(priority.index("freeze_confirmation_or_freeze_bypass_risk"), priority.index("ambiguous_short_command"))
        self.assertLess(priority.index("patch_delivery_or_manual_overwrite_risk"), priority.index("explanation_only_false_positive"))
        self.assertIn("m9c_seed_gold_set_static_offline_cases", spec["required_existing_guards_before_future_use"])
        self.assertIn("adviser_output_guard", spec["required_existing_guards_before_future_use"])
        self.assertIn("adviser_resource_limits", spec["required_existing_guards_before_future_use"])
        self.assertIn("adviser_severity", spec["required_existing_guards_before_future_use"])

    def test_m10_forbids_candidate_execution_runtime_and_io(self):
        spec = json.loads((DESIGN / "candidate_v0_offline_lexical_scorer_design_spec.json").read_text(encoding="utf-8"))
        for key, value in spec["explicitly_forbidden_in_m10"].items():
            self.assertIs(value, True, key)
        for key in (
            "m10_contains_candidate_outputs",
            "m10_contains_candidate_scorer",
            "m10_contains_ml_execution",
            "m10_contains_runtime_integration",
            "m10_contains_prompt_auto_loading",
            "m10_contains_artifact_io",
            "m10_contains_embeddings_or_providers",
            "m10_contains_router_authority",
            "runtime_router_may_import_candidate_design",
            "prompt_loader_may_auto_load_candidate_design",
        ):
            self.assertIs(spec[key], False, key)

    def test_design_text_preserves_no_runtime_no_provider_no_router_authority_boundary(self):
        text = "\n".join(path.read_text(encoding="utf-8") for path in DESIGN.rglob("*") if path.is_file()).lower()
        for required in (
            "design-only",
            "not the candidate implementation",
            "standard library only",
            "pure function",
            "no model call",
            "no embedding",
            "no vector index",
            "no provider",
            "no router authority",
            "unconditional `yes`",
            "m11",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "runtime router integration enabled",
            "prompt auto-loading enabled",
            "candidate outputs created",
            "candidate implementation complete",
            "openai_secret_key",
            "faiss_index_file",
            "router authority granted",
            "unconditional_yes_allowed",
            "may_proceed yes allowed",
            "provider call enabled",
            "embedding vector created",
        ):
            self.assertNotIn(forbidden, text)

    def test_runtime_contract_and_init_do_not_export_candidate_design(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "candidate_v0_offline_lexical_scorer",
            "adviser_candidate",
            "seed_gold_set_v1",
            "adviser_offline",
            "lexical_scorer",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)

    def test_manifest_declares_m10_design_only_boundary(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_candidate_v0_offline_lexical_scorer_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_candidate_v0_offline_lexical_scorer_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_candidate_v0_offline_lexical_scorer_design_status"],
            "design_only_no_candidate_module_no_candidate_outputs_no_runtime_behavior_change",
        )
        self.assertFalse(manifest["adviser_candidate_v0_offline_lexical_scorer_design_contains_candidate_module"])
        self.assertFalse(manifest["adviser_candidate_v0_offline_lexical_scorer_design_contains_candidate_outputs"])
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_candidate_v0_offline_lexical_scorer_design_v1",
            "adviser_candidate_v0_design_only_not_implemented",
            "adviser_candidate_v0_no_candidate_module_in_m10",
            "adviser_candidate_v0_no_candidate_outputs_in_m10",
            "adviser_candidate_v0_future_standard_library_only",
            "adviser_candidate_v0_future_pure_function_only",
            "adviser_candidate_v0_future_no_file_io",
            "adviser_candidate_v0_future_no_source_scanning",
            "adviser_candidate_v0_future_no_prompt_auto_loading",
            "adviser_candidate_v0_future_no_embeddings_vectors_or_providers",
            "adviser_candidate_v0_future_no_runtime_router_authority",
            "adviser_candidate_v0_output_must_pass_m3_m4_guards",
            "adviser_candidate_v0_evaluation_against_m9c_gold_is_future_offline_only",
            "runtime_router_must_not_import_adviser_candidate_design",
        ):
            self.assertIn(expected, chars)


if __name__ == "__main__":
    unittest.main()
