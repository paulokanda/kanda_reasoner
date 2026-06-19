import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
GATE = ADVISER / "test_data" / "gold_set" / "blocked_pending_review"
TEACHER = ADVISER / "test_data" / "teacher_answers" / "draft"
REVIEWS = ADVISER / "test_data" / "human_review_records" / "draft"
FEATURE_ID = "routing_signal_scorer_v3_adviser_seed_gold_set_gate_v1"
SCHEMA_VERSION = "3.48-adviser-seed-gold-set-gate"


class AdviserSeedGoldSetGateTests(unittest.TestCase):
    def load_jsonl(self, path):
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def test_m9_gate_files_exist_without_gold_cases(self):
        for path in (
            GATE / "README.md",
            GATE / "seed_gold_set_gate_manifest.json",
            GATE / "seed_gold_set_promotion_requirements.json",
            GATE / "blocked_gold_promotion_records_v1.jsonl",
        ):
            self.assertTrue(path.exists(), path)
        for forbidden in (
            GATE / "gold_cases_v1.jsonl",
            GATE / "seed_gold_manifest_v1.json",
            ADVISER / "gold",
            ADVISER / "test_data" / "gold_set" / "approved",
            ADVISER / "test_data" / "gold_set" / "reviewed",
        ):
            self.assertFalse(forbidden.exists(), forbidden)

    def test_manifest_declares_blocked_gate_not_gold_set(self):
        manifest = json.loads((GATE / "seed_gold_set_gate_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["feature_id"], FEATURE_ID)
        self.assertEqual(manifest["dataset_kind"], "seed_gold_set_gate_blocked_pending_review")
        self.assertEqual(manifest["record_count"], 50)
        self.assertEqual(manifest["blocked_promotion_count"], 50)
        self.assertEqual(manifest["gold_case_count"], 0)
        self.assertFalse(manifest["is_gold_set"])
        self.assertFalse(manifest["contains_gold_cases"])
        self.assertFalse(manifest["contains_approved_reviews"])
        self.assertFalse(manifest["contains_candidate_outputs"])
        self.assertFalse(manifest["contains_candidate_scorer"])
        self.assertFalse(manifest["contains_ml_execution"])
        self.assertFalse(manifest["contains_runtime_integration"])
        self.assertFalse(manifest["contains_prompt_auto_loading"])
        self.assertFalse(manifest["contains_artifact_io"])
        self.assertFalse(manifest["contains_embeddings_or_providers"])
        self.assertEqual(manifest["gold_promotion_status"], "blocked_pending_explicit_human_review")
        self.assertTrue(manifest["future_gold_set_requires_separate_patch"])
        self.assertTrue(manifest["all_source_reviews_pending"])
        self.assertTrue(manifest["all_source_records_non_gold"])

    def test_blocked_records_cover_all_pending_review_records_and_do_not_permit_gold(self):
        teacher_answers = self.load_jsonl(TEACHER / "draft_teacher_answers_v1.jsonl")
        pending_reviews = self.load_jsonl(REVIEWS / "pending_human_review_records_v1.jsonl")
        blocked = self.load_jsonl(GATE / "blocked_gold_promotion_records_v1.jsonl")
        self.assertEqual(len(teacher_answers), 50)
        self.assertEqual(len(pending_reviews), 50)
        self.assertEqual(len(blocked), 50)
        pending_review_ids = {row["review_id"] for row in pending_reviews}
        blocked_review_ids = {row["review_id"] for row in blocked}
        self.assertEqual(pending_review_ids, blocked_review_ids)
        for row in blocked:
            self.assertEqual(row["schema_version"], SCHEMA_VERSION)
            self.assertEqual(row["feature_id"], FEATURE_ID)
            self.assertTrue(row["gate_record_id"].startswith("m9-gold-block-m7-"))
            self.assertEqual(row["source_teacher_review_status"], "draft")
            self.assertEqual(row["source_human_review_status"], "pending")
            self.assertEqual(row["source_review_decision"], "unresolved")
            self.assertEqual(row["source_next_action"], "defer")
            self.assertFalse(row["may_be_used_as_gold"])
            self.assertEqual(row["gold_status"], "blocked_not_gold_pending_human_review")
            self.assertEqual(row["required_action_before_gold"], "explicit_human_review_and_approval_record_required")
            self.assertEqual(row["authority_statement"], "gate_blocks_gold_promotion_no_router_authority")
            self.assertIn(row["expected_severity_if_missed"], {"P0_CRITICAL", "P1_HIGH", "P2_MEDIUM", "P3_LOW"})

    def test_promotion_requirements_explain_why_gold_is_blocked(self):
        req = json.loads((GATE / "seed_gold_set_promotion_requirements.json").read_text(encoding="utf-8"))
        self.assertEqual(req["schema_version"], SCHEMA_VERSION)
        self.assertEqual(req["feature_id"], FEATURE_ID)
        self.assertEqual(req["authority_statement"], "requirements_only_no_gold_creation")
        self.assertEqual(req["gold_case_count_created_by_this_patch"], 0)
        self.assertTrue(req["requires_explicit_human_review_before_gold"])
        joined = "\n".join(req["blocked_now_because"] + req["minimum_requirements_before_seed_gold_set"]).lower()
        self.assertIn("pending", joined)
        self.assertIn("draft", joined)
        self.assertIn("explicit human", joined)
        self.assertIn("separate governed patch", joined)

    def test_gate_files_contain_no_current_gold_approval_or_runtime_authority(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in GATE.rglob("*")
            if path.is_file()
        ).lower()
        for forbidden in (
            "gold cases created",
            '"contains_gold_cases": true',
            '"contains_approved_reviews": true',
            '"may_be_used_as_gold": true',
            "runtime router integration enabled",
            "prompt auto-loading enabled",
            "candidate_output_text",
            "candidate scorer enabled",
            "openai_secret_key",
            "embedding vector",
            "faiss_index_file",
            "router authority granted",
            "may_proceed yes",
            "unconditional_yes_allowed",
        ):
            self.assertNotIn(forbidden, text)

    def test_manifest_declares_m9_seed_gold_set_gate(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_seed_gold_set_gate_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_seed_gold_set_gate_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_seed_gold_set_gate_blocked_record_count"], 50)
        self.assertEqual(manifest["adviser_seed_gold_set_gate_gold_case_count"], 0)
        self.assertEqual(manifest["adviser_seed_gold_set_gate_source_review_status"], "pending_only")
        self.assertEqual(
            manifest["adviser_seed_gold_set_gate_status"],
            "blocked_pending_human_review_no_gold_set_created_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_seed_gold_set_gate_v1",
            "adviser_seed_gold_set_blocked_pending_human_review",
            "adviser_seed_gold_set_gate_no_gold_cases_created",
            "adviser_seed_gold_set_gate_no_gold_manifest_written",
            "adviser_seed_gold_set_gate_no_candidate_outputs",
            "adviser_seed_gold_set_gate_no_candidate_scorer",
            "adviser_seed_gold_set_gate_no_ml_execution",
            "adviser_seed_gold_set_gate_no_runtime_integration",
            "adviser_seed_gold_set_gate_no_prompt_auto_loading",
            "adviser_seed_gold_set_gate_no_artifact_io",
            "adviser_seed_gold_set_gate_no_embeddings_or_providers",
            "adviser_seed_gold_set_gate_no_router_authority",
            "teacher_answers_not_ground_truth_without_human_review",
            "pending_human_review_records_cannot_be_gold",
        ):
            self.assertIn(expected, chars)

    def test_runtime_contract_and_init_still_do_not_export_adviser_offline(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "seed_gold_set_gate",
            "blocked_gold_promotion_records",
            "gold_set",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
