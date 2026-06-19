import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
INPUT_CASES = ADVISER / "test_data" / "input_cases"
DRAFT_TEACHER = ADVISER / "test_data" / "teacher_answers" / "draft"
PENDING_REVIEWS = ADVISER / "test_data" / "human_review_records" / "draft"
REVIEWED_TEACHER = ADVISER / "test_data" / "teacher_answers" / "reviewed"
REVIEWED_RECORDS = ADVISER / "test_data" / "human_review_records" / "reviewed"
FEATURE_ID = "routing_signal_scorer_v3_adviser_human_reviewed_approval_records_v1"
SCHEMA_VERSION = "3.49-adviser-human-reviewed-approval-records"
OVERRIDE_CASE_IDS = tuple(sorted({'m7-rss-001', 'm7-startup-003', 'm7-freeze-004', 'm7-prompt-001', 'm7-patch-002', 'm7-freeze-003', 'm7-box-004', 'm7-red-008'}))

class AdviserHumanReviewedApprovalRecordsTests(unittest.TestCase):
    def load_jsonl(self, path):
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_m9b_files_exist_without_gold_set(self):
        for path in (
            REVIEWED_RECORDS / "README.md",
            REVIEWED_RECORDS / "external_audit_acceptance_summary.md",
            REVIEWED_RECORDS / "human_reviewed_approval_manifest.json",
            REVIEWED_RECORDS / "human_reviewed_approval_records_v1.jsonl",
            REVIEWED_TEACHER / "README.md",
            REVIEWED_TEACHER / "human_reviewed_teacher_answer_manifest.json",
            REVIEWED_TEACHER / "human_reviewed_teacher_answers_v1.jsonl",
        ):
            self.assertTrue(path.exists(), path)
        for forbidden in (
            ADVISER / "gold",
            ADVISER / "scratch",
            ADVISER / "candidate",
            ADVISER / "test_data" / "candidate_outputs",
            ADVISER / "test_data" / "gold_set" / "approved",
            ADVISER / "test_data" / "gold_set" / "reviewed",
            ADVISER / "test_data" / "gold_set" / "gold_cases_v1.jsonl",
        ):
            self.assertFalse(forbidden.exists(), forbidden)

    def test_manifests_declare_reviewed_evidence_not_gold(self):
        review_manifest = json.loads((REVIEWED_RECORDS / "human_reviewed_approval_manifest.json").read_text(encoding="utf-8"))
        teacher_manifest = json.loads((REVIEWED_TEACHER / "human_reviewed_teacher_answer_manifest.json").read_text(encoding="utf-8"))
        for manifest in (review_manifest, teacher_manifest):
            self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
            self.assertEqual(manifest["feature_id"], FEATURE_ID)
            self.assertEqual(manifest["record_count"], 50)
            self.assertEqual(manifest["approved_count"], 42)
            self.assertEqual(manifest["override_count"], 8)
            self.assertEqual(manifest["rejected_count"], 0)
            self.assertEqual(manifest["cross_cutting_review_note_count"], 1)
            self.assertFalse(manifest["is_gold_set"])
            self.assertFalse(manifest["contains_gold_cases"])
            self.assertEqual(manifest["gold_case_count_created_by_this_patch"], 0)
            self.assertTrue(manifest["future_gold_set_requires_separate_patch"])
            self.assertFalse(manifest["contains_candidate_outputs"])
            self.assertFalse(manifest["contains_candidate_scorer"])
            self.assertFalse(manifest["contains_ml_execution"])
            self.assertFalse(manifest["contains_runtime_integration"])
            self.assertFalse(manifest["contains_prompt_auto_loading"])
            self.assertFalse(manifest["contains_artifact_io"])
            self.assertFalse(manifest["contains_embeddings_or_providers"])
            self.assertFalse(manifest["contains_router_authority"])
        self.assertEqual(tuple(sorted(review_manifest["override_case_ids"])), OVERRIDE_CASE_IDS)
        self.assertIn("governance_path_note", review_manifest)
        self.assertEqual(review_manifest["external_audit_reported_override_needed_count"], 9)
        self.assertEqual(review_manifest["implemented_case_level_override_count"], 8)

    def test_reviewed_records_cover_all_source_records(self):
        seed = self.load_jsonl(INPUT_CASES / "seed_cases_v1.jsonl")
        draft = self.load_jsonl(DRAFT_TEACHER / "draft_teacher_answers_v1.jsonl")
        pending = self.load_jsonl(PENDING_REVIEWS / "pending_human_review_records_v1.jsonl")
        reviewed = self.load_jsonl(REVIEWED_RECORDS / "human_reviewed_approval_records_v1.jsonl")
        reviewed_answers = self.load_jsonl(REVIEWED_TEACHER / "human_reviewed_teacher_answers_v1.jsonl")
        self.assertEqual(len(seed), 50)
        self.assertEqual(len(draft), 50)
        self.assertEqual(len(pending), 50)
        self.assertEqual(len(reviewed), 50)
        self.assertEqual(len(reviewed_answers), 50)
        case_ids = {row["case_id"] for row in seed}
        self.assertEqual(case_ids, {row["case_id"] for row in reviewed})
        self.assertEqual(case_ids, {row["case_id"] for row in reviewed_answers})
        decisions = {row["case_id"]: row["review_decision"] for row in reviewed}
        self.assertEqual(sum(1 for value in decisions.values() if value == "approve"), 42)
        self.assertEqual(sum(1 for value in decisions.values() if value == "override"), 8)
        self.assertEqual(sum(1 for value in decisions.values() if value == "reject"), 0)
        self.assertEqual(tuple(sorted(k for k, v in decisions.items() if v == "override")), OVERRIDE_CASE_IDS)
        for row in reviewed:
            self.assertEqual(row["schema_version"], SCHEMA_VERSION)
            self.assertEqual(row["feature_id"], FEATURE_ID)
            self.assertEqual(row["authority_statement"], "human_review_record_evidence_not_gold_no_router_authority")
            self.assertTrue(row["review_record_id"].startswith("m9b-human-review-m7-"))
            self.assertEqual(row["review_status"], "human_reviewed")
            self.assertTrue(row["eligible_for_future_seed_gold_set"])
            self.assertFalse(row["may_be_used_as_current_gold_case"])
            self.assertEqual(row["gold_status"], "reviewed_not_gold_pending_separate_seed_gold_set_patch")
            self.assertFalse(row["contains_gold_case"])
            self.assertFalse(row["contains_candidate_output"])
            self.assertFalse(row["contains_candidate_scorer"])
            self.assertFalse(row["contains_ml_execution"])
            self.assertFalse(row["contains_runtime_integration"])
            self.assertFalse(row["contains_prompt_auto_loading"])
            self.assertFalse(row["contains_artifact_io"])
            self.assertFalse(row["contains_embeddings_or_providers"])
            self.assertFalse(row["contains_router_authority"])
            self.assertIn("record_hash", row)

    def test_human_reviewed_teacher_answers_preserve_advisory_boundary(self):
        rows = self.load_jsonl(REVIEWED_TEACHER / "human_reviewed_teacher_answers_v1.jsonl")
        for row in rows:
            self.assertEqual(row["schema_version"], SCHEMA_VERSION)
            self.assertEqual(row["feature_id"], FEATURE_ID)
            self.assertEqual(row["authority_statement"], "human_reviewed_teacher_answer_evidence_not_gold_no_router_authority")
            self.assertEqual(row["review_status"], "human_reviewed")
            self.assertIn(row["human_review_decision"], {"approve", "override"})
            self.assertIsNotNone(row["reviewed_by"])
            self.assertIsNotNone(row["reviewed_at"])
            self.assertEqual(row["teacher_version"], "human_reviewed_v1_not_gold")
            self.assertTrue(row["eligible_for_future_seed_gold_set"])
            self.assertFalse(row["may_be_used_as_current_gold_case"])
            self.assertEqual(row["gold_status"], "reviewed_not_gold_pending_separate_seed_gold_set_patch")
            answer = row["answer"]
            self.assertIn(answer["draft_advisory_recommendation"], {
                "ABSTAIN_OUT_OF_SCOPE",
                "ABSTAIN_AMBIGUOUS",
                "DO_NOT_PROCEED_BLOCK_UNSAFE_REQUEST",
                "SAFE_EXPLANATION_ONLY_NO_GOVERNED_ACTION",
                "ROUTED_WORK_REQUIRED_BEFORE_ACTION",
            })
            self.assertIsInstance(answer["draft_required_prompt_groups"], list)
            self.assertIsInstance(answer["draft_risk_flags"], list)
            self.assertIsInstance(answer["draft_forbidden_behaviors"], list)

    def test_key_overrides_are_applied(self):
        reviewed = {row["case_id"]: row for row in self.load_jsonl(REVIEWED_RECORDS / "human_reviewed_approval_records_v1.jsonl")}
        patch_002 = reviewed["m7-patch-002"]["corrected_answer"]
        self.assertEqual(patch_002["draft_advisory_recommendation"], "DO_NOT_PROCEED_BLOCK_UNSAFE_REQUEST")
        self.assertTrue(patch_002["must_not_permit_action"])
        self.assertIn("unboxed_overwrite_attempt", patch_002["draft_risk_flags"])
        self.assertEqual(reviewed["m7-patch-002"]["expected_severity_if_missed"], "P0_CRITICAL")
        red_008 = reviewed["m7-red-008"]["corrected_answer"]
        self.assertIn("advisory_label_used_to_promote_authority", red_008["draft_risk_flags"])
        self.assertNotIn("advisory_only", red_008["draft_forbidden_behaviors"])
        self.assertIn("no_unconditional_yes_authority_grant", red_008["draft_forbidden_behaviors"])
        startup_003 = reviewed["m7-startup-003"]["corrected_answer"]
        self.assertEqual(startup_003["draft_advisory_disposition"], "RECOMMEND_STALE_FILENAME_CORRECTION_VIA_GOVERNED_STARTUP_CHANGE")
        prompt_001 = reviewed["m7-prompt-001"]["corrected_answer"]
        self.assertEqual(prompt_001["draft_advisory_disposition"], "REQUIRE_PROMPT_AUTHORING_AUDIT_BEFORE_CREATION")
        rss_001 = reviewed["m7-rss-001"]["corrected_answer"]
        self.assertIn("self_referential_milestone_command", rss_001["draft_risk_flags"])
        box_004 = reviewed["m7-box-004"]["corrected_answer"]
        self.assertIn("unverified_scope_claim", box_004["draft_risk_flags"])
        freeze_004 = reviewed["m7-freeze-004"]["corrected_answer"]
        self.assertIn("ambiguous_continue", freeze_004["draft_risk_flags"])
        freeze_003 = reviewed["m7-freeze-003"]["corrected_answer"]
        self.assertIn("freeze_confirmation_needed", freeze_003["draft_risk_flags"])

    def test_no_runtime_export_or_forbidden_artifacts_added(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "human_reviewed_approval_records_v1",
            "human_reviewed_teacher_answers_v1",
            "seed_gold_set",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)
        all_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in list(REVIEWED_RECORDS.rglob("*")) + list(REVIEWED_TEACHER.rglob("*"))
            if path.is_file()
        ).lower()
        for forbidden in (
            "runtime router integration enabled",
            "prompt auto-loading enabled",
            "candidate_output_text",
            "candidate scorer enabled",
            "openai_secret_key",
            "embedding vector",
            "faiss_index_file",
            "router authority granted",
            "may_proceed yes allowed",
            "unconditional_yes_allowed",
            "contains_gold_cases\": true",
            "is_gold_set\": true",
        ):
            self.assertNotIn(forbidden, all_text)

    def test_manifest_declares_m9b_reviewed_approval_records(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_human_reviewed_approval_records_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_human_reviewed_approval_records_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_human_reviewed_approval_records_count"], 50)
        self.assertEqual(manifest["adviser_human_reviewed_approval_approve_count"], 42)
        self.assertEqual(manifest["adviser_human_reviewed_approval_override_count"], 8)
        self.assertEqual(manifest["adviser_human_reviewed_approval_cross_cutting_note_count"], 1)
        self.assertEqual(manifest["adviser_human_reviewed_approval_reject_count"], 0)
        self.assertEqual(manifest["adviser_human_reviewed_approval_gold_case_count"], 0)
        self.assertEqual(manifest["adviser_human_reviewed_approval_records_status"], "human_reviewed_approval_and_override_records_only_no_gold_set_no_candidate_no_runtime_behavior_change")
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_human_reviewed_approval_records_v1",
            "adviser_human_reviewed_approval_records_are_reviewed_evidence_only",
            "adviser_human_reviewed_teacher_answers_are_not_gold_cases",
            "adviser_human_reviewed_approval_records_do_not_create_gold_set",
            "adviser_human_reviewed_approval_records_42_approve_8_override_0_reject_1_cross_cutting_note",
            "adviser_human_reviewed_approval_records_future_gold_set_requires_separate_patch",
            "adviser_m9b_no_candidate_outputs",
            "adviser_m9b_no_candidate_scorer",
            "adviser_m9b_no_ml_execution",
            "adviser_m9b_no_runtime_integration",
            "adviser_m9b_no_prompt_auto_loading",
            "adviser_m9b_no_artifact_io",
            "adviser_m9b_no_embeddings_or_providers",
            "adviser_m9b_no_router_authority",
        ):
            self.assertIn(expected, chars)

if __name__ == "__main__":
    unittest.main()
