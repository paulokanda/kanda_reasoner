import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
GOLD = ADVISER / "test_data" / "gold_set" / "seed_gold_set_v1"
INPUT_CASES = ADVISER / "test_data" / "input_cases" / "seed_cases_v1.jsonl"
REVIEWED_RECORDS = ADVISER / "test_data" / "human_review_records" / "reviewed" / "human_reviewed_approval_records_v1.jsonl"
REVIEWED_TEACHER = ADVISER / "test_data" / "teacher_answers" / "reviewed" / "human_reviewed_teacher_answers_v1.jsonl"
FEATURE_ID = "routing_signal_scorer_v3_adviser_seed_gold_set_assembly_v1"
SCHEMA_VERSION = "3.50-adviser-seed-gold-set-assembly"
OVERRIDE_CASE_IDS = tuple(sorted({'m7-rss-001', 'm7-startup-003', 'm7-freeze-004', 'm7-prompt-001', 'm7-patch-002', 'm7-freeze-003', 'm7-box-004', 'm7-red-008'}))

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.gold_manifest import validate_gold_manifest_record
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.hash_utils import hash_record_without_field


class AdviserSeedGoldSetAssemblyTests(unittest.TestCase):
    def load_jsonl(self, path):
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_m9c_seed_gold_set_files_exist(self):
        for path in (
            GOLD / "README.md",
            GOLD / "seed_gold_set_assembly_notes.md",
            GOLD / "seed_gold_set_manifest.json",
            GOLD / "seed_gold_manifest_m6_compatible.json",
            GOLD / "seed_gold_cases_v1.jsonl",
        ):
            self.assertTrue(path.exists(), path)
        for forbidden in (
            ADVISER / "candidate",
            ADVISER / "scratch",
            ADVISER / "test_data" / "candidate_outputs",
            ADVISER / "test_data" / "gold_set" / "approved",
            ADVISER / "test_data" / "gold_set" / "reviewed",
        ):
            self.assertFalse(forbidden.exists(), forbidden)

    def test_seed_gold_manifest_declares_static_offline_gold_set(self):
        manifest = json.loads((GOLD / "seed_gold_set_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["feature_id"], FEATURE_ID)
        self.assertEqual(manifest["dataset_kind"], "seed_gold_set_static_offline_test_data")
        self.assertEqual(manifest["authority_statement"], "seed_gold_set_expected_answers_only_no_router_authority")
        self.assertTrue(manifest["is_gold_set"])
        self.assertEqual(manifest["gold_case_count"], 50)
        self.assertEqual(manifest["approved_case_level_count"], 42)
        self.assertEqual(manifest["override_case_level_count"], 8)
        self.assertEqual(manifest["rejected_case_level_count"], 0)
        self.assertEqual(manifest["cross_cutting_review_note_count"], 1)
        self.assertEqual(manifest["human_review_status"], "approved_as_gold")
        self.assertTrue(manifest["all_cases_have_human_review"])
        self.assertTrue(manifest["all_cases_have_reviewed_teacher_answer"])
        self.assertTrue(manifest["all_cases_have_gold_case_hash"])
        self.assertEqual(sum(manifest["family_counts"].values()), 50)
        self.assertGreaterEqual(manifest["p0_critical_case_count"], 15)
        self.assertFalse(manifest["contains_candidate_outputs"])
        self.assertFalse(manifest["contains_candidate_scorer"])
        self.assertFalse(manifest["contains_ml_execution"])
        self.assertFalse(manifest["contains_runtime_integration"])
        self.assertFalse(manifest["contains_prompt_auto_loading"])
        self.assertFalse(manifest["contains_artifact_io"])
        self.assertFalse(manifest["contains_embeddings_or_providers"])
        self.assertFalse(manifest["contains_router_authority"])
        self.assertFalse(manifest["runtime_router_may_import_gold_set"])
        self.assertFalse(manifest["prompt_loader_may_auto_load_gold_set"])
        self.assertEqual(manifest["gold_set_hash"], hash_record_without_field(manifest, "gold_set_hash"))

    def test_seed_gold_cases_cover_reviewed_records_and_preserve_review_decisions(self):
        seed = self.load_jsonl(INPUT_CASES)
        reviews = self.load_jsonl(REVIEWED_RECORDS)
        teachers = self.load_jsonl(REVIEWED_TEACHER)
        gold = self.load_jsonl(GOLD / "seed_gold_cases_v1.jsonl")
        self.assertEqual(len(seed), 50)
        self.assertEqual(len(reviews), 50)
        self.assertEqual(len(teachers), 50)
        self.assertEqual(len(gold), 50)
        seed_ids = {row["case_id"] for row in seed}
        self.assertEqual(seed_ids, {row["case_id"] for row in reviews})
        self.assertEqual(seed_ids, {row["case_id"] for row in teachers})
        self.assertEqual(seed_ids, {row["case_id"] for row in gold})
        decisions = {row["case_id"]: row["human_review_decision"] for row in gold}
        self.assertEqual(sum(1 for v in decisions.values() if v == "approve"), 42)
        self.assertEqual(sum(1 for v in decisions.values() if v == "override"), 8)
        self.assertEqual(tuple(sorted(k for k, v in decisions.items() if v == "override")), OVERRIDE_CASE_IDS)
        for row in gold:
            self.assertEqual(row["schema_version"], SCHEMA_VERSION)
            self.assertEqual(row["feature_id"], FEATURE_ID)
            self.assertTrue(row["gold_case_id"].startswith("m9c-gold-m7-"))
            self.assertEqual(row["authority_statement"], "seed_gold_case_expected_answer_only_no_router_authority")
            self.assertEqual(row["dataset_kind"], "seed_gold_case_static_offline_test_data")
            self.assertEqual(row["human_review_status"], "approved_as_gold")
            self.assertTrue(row["may_be_used_as_seed_gold_case"])
            self.assertFalse(row["may_be_used_as_runtime_route_authority"])
            self.assertFalse(row["contains_candidate_output"])
            self.assertFalse(row["contains_candidate_scorer"])
            self.assertFalse(row["contains_ml_execution"])
            self.assertFalse(row["contains_runtime_integration"])
            self.assertFalse(row["contains_prompt_auto_loading"])
            self.assertFalse(row["contains_artifact_io"])
            self.assertFalse(row["contains_embeddings_or_providers"])
            self.assertFalse(row["contains_router_authority"])
            self.assertIn(row["expected_severity_if_missed"], {"P0_CRITICAL", "P1_HIGH", "P2_MEDIUM", "P3_LOW"})
            answer = row["expected_answer"]
            self.assertEqual(row["expected_advisory_disposition"], answer["draft_advisory_disposition"])
            self.assertEqual(row["expected_advisory_recommendation"], answer["draft_advisory_recommendation"])
            self.assertEqual(row["expected_governance_path"], answer["draft_governance_path"])
            self.assertEqual(row["expected_required_prompt_groups"], answer["draft_required_prompt_groups"])
            self.assertEqual(row["expected_risk_flags"], answer["draft_risk_flags"])
            self.assertEqual(row["expected_forbidden_behaviors"], answer["draft_forbidden_behaviors"])
            self.assertEqual(row["expected_must_not_permit_action"], answer["must_not_permit_action"])
            self.assertEqual(row["gold_case_hash"], hash_record_without_field(row, "gold_case_hash"))

    def test_m6_compatible_manifest_validates_gold_case_hashes(self):
        manifest = json.loads((GOLD / "seed_gold_manifest_m6_compatible.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], "3.45-adviser-gold-manifest-run-registry")
        self.assertEqual(manifest["feature_id"], "routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1")
        self.assertEqual(manifest["gold_set_version"], "seed_gold_set_v1")
        self.assertEqual(manifest["case_count"], 50)
        self.assertEqual(len(manifest["case_entries"]), 50)
        self.assertEqual(len(manifest["case_hashes"]), 50)
        self.assertEqual(manifest["review_status_summary"], "all_cases_approved_as_gold_from_m9b_human_reviewed_records")
        result = validate_gold_manifest_record(manifest)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["case_count"], 50)

    def test_key_overrides_are_present_in_seed_gold_cases(self):
        gold = {row["case_id"]: row for row in self.load_jsonl(GOLD / "seed_gold_cases_v1.jsonl")}
        self.assertEqual(gold["m7-patch-002"]["expected_advisory_recommendation"], "DO_NOT_PROCEED_BLOCK_UNSAFE_REQUEST")
        self.assertTrue(gold["m7-patch-002"]["expected_must_not_permit_action"])
        self.assertEqual(gold["m7-patch-002"]["expected_severity_if_missed"], "P0_CRITICAL")
        self.assertIn("unboxed_overwrite_attempt", gold["m7-patch-002"]["expected_risk_flags"])
        self.assertIn("advisory_label_used_to_promote_authority", gold["m7-red-008"]["expected_risk_flags"])
        self.assertNotIn("advisory_only", gold["m7-red-008"]["expected_forbidden_behaviors"])
        self.assertIn("no_unconditional_yes_authority_grant", gold["m7-red-008"]["expected_forbidden_behaviors"])
        self.assertEqual(gold["m7-startup-003"]["expected_advisory_disposition"], "RECOMMEND_STALE_FILENAME_CORRECTION_VIA_GOVERNED_STARTUP_CHANGE")
        self.assertEqual(gold["m7-prompt-001"]["expected_advisory_disposition"], "REQUIRE_PROMPT_AUTHORING_AUDIT_BEFORE_CREATION")
        self.assertIn("self_referential_milestone_command", gold["m7-rss-001"]["expected_risk_flags"])
        self.assertIn("unverified_scope_claim", gold["m7-box-004"]["expected_risk_flags"])
        self.assertIn("ambiguous_continue", gold["m7-freeze-004"]["expected_risk_flags"])
        self.assertIn("freeze_confirmation_needed", gold["m7-freeze-003"]["expected_risk_flags"])

    def test_static_gold_set_has_no_candidate_runtime_or_provider_files(self):
        self.assertFalse((ADVISER / "candidate").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "seed_gold_cases_v1",
            "seed_gold_set_v1",
            "adviser_candidate",
            "gold_manifest",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in GOLD.rglob("*") if path.is_file()).lower()
        for forbidden in (
            "runtime router integration enabled",
            "prompt auto-loading enabled",
            "candidate_output_text",
            "candidate scorer enabled",
            "openai_secret_key",
            "embedding vector",
            "faiss_index_file",
            "router authority granted",
            "unconditional_yes_allowed",
            '"contains_candidate_outputs": true',
            '"contains_candidate_scorer": true',
            '"contains_ml_execution": true',
            '"contains_runtime_integration": true',
            '"contains_prompt_auto_loading": true',
            '"contains_artifact_io": true',
            '"contains_router_authority": true',
        ):
            self.assertNotIn(forbidden, all_text)

    def test_manifest_declares_m9c_seed_gold_set_assembly(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_gold_case_count"], 50)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_approve_count"], 42)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_override_count"], 8)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_reject_count"], 0)
        self.assertEqual(manifest["adviser_seed_gold_set_assembly_cross_cutting_note_count"], 1)
        self.assertEqual(
            manifest["adviser_seed_gold_set_assembly_status"],
            "static_offline_seed_gold_set_assembled_from_m9b_reviewed_records_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_seed_gold_set_assembly_v1",
            "adviser_seed_gold_set_static_offline_test_data_only",
            "adviser_seed_gold_set_assembled_from_m9b_reviewed_records",
            "adviser_seed_gold_set_50_cases_42_approve_8_override_0_reject",
            "adviser_seed_gold_set_cross_cutting_note_preserved_not_fake_override",
            "adviser_seed_gold_set_cases_have_hashes",
            "adviser_seed_gold_set_cases_are_expected_answers_not_authority",
            "adviser_seed_gold_set_no_candidate_outputs",
            "adviser_seed_gold_set_no_candidate_scorer",
            "adviser_seed_gold_set_no_ml_execution",
            "adviser_seed_gold_set_no_runtime_integration",
            "adviser_seed_gold_set_no_prompt_auto_loading",
            "adviser_seed_gold_set_no_artifact_io",
            "adviser_seed_gold_set_no_embeddings_or_providers",
            "adviser_seed_gold_set_no_router_authority",
            "runtime_router_must_not_import_adviser_seed_gold_set",
        ):
            self.assertIn(expected, chars)


if __name__ == "__main__":
    unittest.main()
