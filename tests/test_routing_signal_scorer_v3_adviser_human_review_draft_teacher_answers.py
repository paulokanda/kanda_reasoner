import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
INPUT_CASES = ADVISER / "test_data" / "input_cases"
TEACHER = ADVISER / "test_data" / "teacher_answers" / "draft"
REVIEWS = ADVISER / "test_data" / "human_review_records" / "draft"
FEATURE_ID = "routing_signal_scorer_v3_adviser_human_review_draft_teacher_answers_v1"
SCHEMA_VERSION = "3.47-adviser-human-review-draft-teacher-answers"


class AdviserHumanReviewDraftTeacherAnswersTests(unittest.TestCase):
    def load_jsonl(self, path):
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def test_m8_files_exist(self):
        for path in (
            TEACHER / "README.md",
            TEACHER / "draft_teacher_answer_manifest.json",
            TEACHER / "draft_teacher_answers_v1.jsonl",
            REVIEWS / "README.md",
            REVIEWS / "pending_review_manifest.json",
            REVIEWS / "pending_human_review_records_v1.jsonl",
        ):
            self.assertTrue(path.exists(), path)

    def test_manifests_declare_draft_only_not_gold(self):
        teacher_manifest = json.loads((TEACHER / "draft_teacher_answer_manifest.json").read_text(encoding="utf-8"))
        review_manifest = json.loads((REVIEWS / "pending_review_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(teacher_manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(teacher_manifest["feature_id"], FEATURE_ID)
        self.assertEqual(teacher_manifest["record_count"], 50)
        self.assertEqual(teacher_manifest["case_count"], 50)
        self.assertEqual(teacher_manifest["review_status"], "draft_unreviewed")
        self.assertFalse(teacher_manifest["is_gold_set"])
        self.assertFalse(teacher_manifest["contains_gold_cases"])
        self.assertFalse(teacher_manifest["contains_candidate_outputs"])
        self.assertFalse(teacher_manifest["contains_candidate_scorer"])
        self.assertFalse(teacher_manifest["contains_runtime_integration"])
        self.assertFalse(teacher_manifest["contains_ml_execution"])
        self.assertFalse(teacher_manifest["contains_artifact_io"])
        self.assertTrue(teacher_manifest["human_review_required_before_gold"])
        self.assertEqual(review_manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(review_manifest["feature_id"], FEATURE_ID)
        self.assertEqual(review_manifest["record_count"], 50)
        self.assertEqual(review_manifest["review_status"], "pending")
        self.assertFalse(review_manifest["is_gold_set"])
        self.assertFalse(review_manifest["contains_completed_human_reviews"])
        self.assertFalse(review_manifest["contains_gold_approvals"])
        self.assertFalse(review_manifest["contains_candidate_outputs"])
        self.assertFalse(review_manifest["contains_runtime_integration"])

    def test_teacher_answers_cover_all_seed_cases_and_remain_draft(self):
        seed_cases = self.load_jsonl(INPUT_CASES / "seed_cases_v1.jsonl")
        teacher_answers = self.load_jsonl(TEACHER / "draft_teacher_answers_v1.jsonl")
        self.assertEqual(len(seed_cases), 50)
        self.assertEqual(len(teacher_answers), 50)
        seed_ids = {case["case_id"] for case in seed_cases}
        answer_case_ids = {answer["case_id"] for answer in teacher_answers}
        self.assertEqual(seed_ids, answer_case_ids)
        for answer in teacher_answers:
            self.assertEqual(answer["schema_version"], SCHEMA_VERSION)
            self.assertEqual(answer["feature_id"], FEATURE_ID)
            self.assertTrue(answer["teacher_answer_id"].startswith("m8-teacher-m7-"))
            self.assertEqual(answer["authority_statement"], "advisory_only_evidence_not_authority")
            self.assertEqual(answer["teacher_version"], "draft_v1_unreviewed")
            self.assertEqual(answer["review_status"], "draft")
            self.assertIsNone(answer["reviewed_by"])
            self.assertIsNone(answer["reviewed_at"])
            self.assertIsNone(answer["supersedes"])
            self.assertTrue(answer["human_review_required_before_gold"])
            self.assertIn(answer["expected_severity_if_missed"], {"P0_CRITICAL", "P1_HIGH", "P2_MEDIUM", "P3_LOW"})
            draft = answer["answer"]
            self.assertIn(draft["draft_advisory_recommendation"], {
                "ABSTAIN_OUT_OF_SCOPE",
                "ABSTAIN_AMBIGUOUS",
                "DO_NOT_PROCEED_BLOCK_UNSAFE_REQUEST",
                "SAFE_EXPLANATION_ONLY_NO_GOVERNED_ACTION",
                "ROUTED_WORK_REQUIRED_BEFORE_ACTION",
            })
            self.assertIsInstance(draft["draft_required_prompt_groups"], list)
            self.assertIsInstance(draft["draft_risk_flags"], list)
            self.assertIsInstance(draft["draft_forbidden_behaviors"], list)

    def test_pending_review_records_cover_all_teacher_answers_without_approval(self):
        teacher_answers = self.load_jsonl(TEACHER / "draft_teacher_answers_v1.jsonl")
        reviews = self.load_jsonl(REVIEWS / "pending_human_review_records_v1.jsonl")
        teacher_ids = {answer["teacher_answer_id"] for answer in teacher_answers}
        review_teacher_ids = {review["teacher_answer_id"] for review in reviews}
        self.assertEqual(len(reviews), 50)
        self.assertEqual(teacher_ids, review_teacher_ids)
        for review in reviews:
            self.assertEqual(review["schema_version"], SCHEMA_VERSION)
            self.assertEqual(review["feature_id"], FEATURE_ID)
            self.assertTrue(review["review_id"].startswith("m8-review-m7-"))
            self.assertIsNone(review["reviewer_id"])
            self.assertEqual(review["review_status"], "pending")
            self.assertEqual(review["review_decision"], "unresolved")
            self.assertIsNone(review["reviewed_at"])
            self.assertEqual(review["next_action"], "defer")
            self.assertFalse(review["may_be_used_as_gold"])
            self.assertTrue(review["requires_explicit_human_review"])
            self.assertIn(review["safety_impact"], {"critical", "high", "medium", "low"})

    def test_m8_does_not_create_gold_candidate_outputs_scratch_or_runtime_behavior(self):
        self.assertFalse((ADVISER / "candidate").exists())
        self.assertFalse((ADVISER / "gold").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        all_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in list(TEACHER.rglob("*")) + list(REVIEWS.rglob("*"))
            if path.is_file()
        ).lower()
        for forbidden in (
            "approved_as_gold",
            "gold_reviewed",
            "candidate_output_text",
            "candidate scorer",
            "runtime router integration enabled",
            "prompt auto-loading enabled",
            "openai_secret_key",
            "embedding vector",
            "faiss_index_file",
            "may_proceed yes allowed",
            "unconditional_yes_allowed",
        ):
            self.assertNotIn(forbidden, all_text)

    def test_manifest_declares_m8_draft_teacher_answers(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_human_review_draft_teacher_answers_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_human_review_draft_teacher_answers_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_human_review_draft_teacher_answers_count"], 50)
        self.assertEqual(manifest["adviser_pending_human_review_record_count"], 50)
        self.assertEqual(
            manifest["adviser_human_review_draft_teacher_answers_status"],
            "draft_teacher_answers_and_pending_review_records_only_no_gold_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_human_review_draft_teacher_answers_v1",
            "adviser_teacher_answers_are_draft_only",
            "adviser_teacher_answers_not_gold",
            "adviser_teacher_answers_require_human_review_before_gold",
            "adviser_human_review_records_pending_only",
            "adviser_human_review_records_no_gold_approval",
            "adviser_m8_no_candidate_outputs",
            "adviser_m8_no_candidate_scorer",
            "adviser_m8_no_gold_set",
            "adviser_m8_no_runtime_integration",
            "adviser_m8_no_prompt_auto_loading",
            "adviser_m8_no_artifact_io",
            "adviser_m8_no_embeddings_or_providers",
            "no_adviser_router_authority_from_m8_teacher_answers",
        ):
            self.assertIn(expected, chars)

    def test_runtime_contract_and_init_still_do_not_export_adviser_offline(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "draft_teacher_answers_v1",
            "pending_human_review_records_v1",
            "teacher_answers",
            "human_review_records",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
