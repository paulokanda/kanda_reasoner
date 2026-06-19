
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
INPUT_CASES = ADVISER / "test_data" / "input_cases"
FEATURE_ID = "routing_signal_scorer_v3_adviser_seed_case_corpus_v1"
SCHEMA_VERSION = "3.46-adviser-seed-case-corpus"


class AdviserSeedCaseCorpusTests(unittest.TestCase):
    def load_cases(self):
        cases = []
        for line in (INPUT_CASES / "seed_cases_v1.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                cases.append(json.loads(line))
        return cases

    def test_seed_case_files_exist(self):
        self.assertTrue((INPUT_CASES / "README.md").exists())
        self.assertTrue((INPUT_CASES / "seed_case_corpus_manifest.json").exists())
        self.assertTrue((INPUT_CASES / "seed_cases_v1.jsonl").exists())
        for family in (
            "adversarial_bypass", "ambiguous", "box_boundary", "false_positive",
            "freeze_workflow", "out_of_scope", "patch_delivery", "prompt_library",
            "routing_signal_scorer", "startup_delivery",
        ):
            self.assertTrue((INPUT_CASES / f"{family}_cases.jsonl").exists(), family)

    def test_manifest_declares_seed_only_not_gold(self):
        manifest = json.loads((INPUT_CASES / "seed_case_corpus_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["feature_id"], FEATURE_ID)
        self.assertEqual(manifest["authority_statement"], "advisory_only")
        self.assertEqual(manifest["human_review_status"], "seed_unreviewed")
        self.assertEqual(manifest["case_count"], 50)
        self.assertFalse(manifest["is_gold_set"])
        self.assertFalse(manifest["contains_teacher_answers"])
        self.assertFalse(manifest["contains_candidate_outputs"])
        self.assertFalse(manifest["contains_runtime_integration"])
        self.assertEqual(sum(manifest["families"].values()), 50)

    def test_seed_cases_are_well_formed_and_unreviewed(self):
        cases = self.load_cases()
        self.assertEqual(len(cases), 50)
        case_ids = set()
        families = set()
        for case in cases:
            self.assertEqual(case["schema_version"], SCHEMA_VERSION)
            self.assertEqual(case["authority_statement"], "advisory_only")
            self.assertEqual(case["human_review_status"], "seed_unreviewed")
            self.assertEqual(case["source"], "synthetic_seed_case_m7")
            self.assertTrue(case["case_id"].startswith("m7-"))
            self.assertNotIn(case["case_id"], case_ids)
            case_ids.add(case["case_id"])
            families.add(case["case_family"])
            self.assertIsInstance(case["input_text"], str)
            self.assertGreaterEqual(len(case["input_text"]), 7)
            self.assertIn(case["expected_severity_if_missed"], {"P0_CRITICAL", "P1_HIGH", "P2_MEDIUM", "P3_LOW"})
            self.assertIsInstance(case["expected_forbidden_behaviors"], list)
            self.assertGreaterEqual(len(case["expected_forbidden_behaviors"]), 1)
        self.assertEqual(families, {
            "adversarial_bypass", "ambiguous", "box_boundary", "false_positive",
            "freeze_workflow", "out_of_scope", "patch_delivery", "prompt_library",
            "routing_signal_scorer", "startup_delivery",
        })

    def test_seed_cases_contain_required_red_path_and_false_positive_coverage(self):
        cases = self.load_cases()
        by_family = {}
        for case in cases:
            by_family.setdefault(case["case_family"], []).append(case)
        self.assertGreaterEqual(len(by_family["adversarial_bypass"]), 8)
        self.assertGreaterEqual(len(by_family["false_positive"]), 5)
        self.assertGreaterEqual(len(by_family["ambiguous"]), 4)
        p0_cases = [case for case in cases if case["expected_severity_if_missed"] == "P0_CRITICAL"]
        self.assertGreaterEqual(len(p0_cases), 15)
        joined = "\n".join(case["input_text"] for case in cases).lower()
        for expected in (
            "without preview", "without confirm", "runtime router", "source scanning",
            "prompt auto", "install chromadb", "provider call", "secretly edit",
            "may_proceed yes", "write the frozen memory entry directly",
        ):
            self.assertIn(expected, joined)

    def test_family_jsonl_files_match_all_case_file(self):
        all_cases = self.load_cases()
        all_ids = {case["case_id"] for case in all_cases}
        family_ids = set()
        for path in INPUT_CASES.glob("*_cases.jsonl"):
            if path.name == "seed_cases_v1.jsonl":
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    case = json.loads(line)
                    family_ids.add(case["case_id"])
                    self.assertEqual(path.name, f"{case['case_family']}_cases.jsonl")
        self.assertEqual(all_ids, family_ids)

    def test_m7_seed_cases_remain_seed_only_after_m8_draft_teacher_records(self):
        self.assertFalse((ADVISER / "candidate").exists())
        self.assertFalse((ADVISER / "gold").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        # M8 may add draft teacher answers and pending human review records.
        # M7 itself still remains seed-input-only and its input case files must not contain teacher or candidate outputs.
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        for path in INPUT_CASES.rglob("*"):
            if path.is_file():
                self.assertIn(path.suffix, {".md", ".json", ".jsonl"})
                text = path.read_text(encoding="utf-8")
                lowered = text.lower()
                for forbidden in (
                    "teacher_answer_text", "candidate_output_text", "gold_reviewed",
                    "approved_as_gold", "human_reviewed", "runtime import",
                    "openai_secret_key", "faiss_index_file", "embedding vector",
                ):
                    self.assertNotIn(forbidden, lowered)

    def test_manifest_declares_m7_seed_case_corpus(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_seed_case_corpus_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_seed_case_corpus_schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["adviser_seed_case_corpus_count"], 50)
        self.assertEqual(
            manifest["adviser_seed_case_corpus_status"],
            "seed_input_cases_only_no_gold_no_teacher_answers_no_candidate_outputs_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_seed_case_corpus_v1",
            "adviser_seed_cases_are_not_gold",
            "adviser_seed_cases_are_seed_unreviewed",
            "adviser_seed_cases_contain_no_teacher_answers",
            "adviser_seed_cases_contain_no_candidate_outputs",
            "adviser_seed_cases_not_loaded_by_runtime_router",
            "adviser_seed_cases_no_scratch_writer",
            "adviser_seed_cases_no_registry_writer",
            "adviser_seed_cases_no_source_scanning",
            "adviser_seed_cases_no_ml_execution",
            "adviser_seed_cases_no_router_authority",
            "no_adviser_candidate_from_m7_seed_corpus",
            "no_adviser_runtime_integration_from_m7_seed_corpus",
        ):
            self.assertIn(expected, chars)

    def test_runtime_contract_and_init_still_do_not_export_adviser_offline(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "seed_case_corpus",
            "seed_cases_v1",
            "adviser_candidate",
            "input_cases",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
