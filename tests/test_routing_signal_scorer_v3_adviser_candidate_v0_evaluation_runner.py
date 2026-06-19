import inspect
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.evaluation.candidate_v0_evaluation_runner import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    REPORT_KIND,
    SCHEMA_VERSION,
    evaluate_candidate_v0_against_gold_cases,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
EVALUATION = ADVISER / "evaluation" / "candidate_v0_evaluation_runner.py"
GOLD = ADVISER / "test_data" / "gold_set" / "seed_gold_set_v1" / "seed_gold_cases_v1.jsonl"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_CONTRACT = BOX / "contract.py"
RUNTIME_INIT = BOX / "__init__.py"


class AdviserCandidateV0EvaluationRunnerTests(unittest.TestCase):
    def test_evaluation_runner_module_exists_inside_adviser_offline_only(self):
        self.assertTrue(EVALUATION.exists(), EVALUATION)
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1")
        self.assertEqual(SCHEMA_VERSION, "3.53-adviser-candidate-v0-evaluation-runner")
        self.assertEqual(REPORT_KIND, "in_memory_offline_evaluation_evidence_only")
        self.assertEqual(AUTHORITY_STATEMENT, "advisory_only")
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "evaluation" / "runs").exists())
        self.assertFalse((ADVISER / "evaluation" / "reports").exists())

    def test_evaluation_runner_source_has_no_file_io_source_scan_or_runtime_hooks(self):
        source = EVALUATION.read_text(encoding="utf-8")
        forbidden = (
            "from pathlib",
            "import pathlib",
            "import os",
            "import sys",
            "import subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "import http",
            "import sqlite",
            "import openai",
            "import anthropic",
            "import numpy",
            "import pandas",
            "import langchain",
            "import llama_index",
            "import faiss",
            "import chromadb",
            "open(",
            ".read_text(",
            ".write_text(",
            "glob(",
            "rglob(",
            "walk(",
            "listdir(",
            "scandir(",
            "save_report",
            "write_report",
            "registry writer enabled",
            "runtime router integration enabled",
            "router authority granted",
        )
        for token in forbidden:
            self.assertNotIn(token, source)
        self.assertIn("caller-supplied", source)
        self.assertIn("in-memory report", source)
        self.assertIn("no runtime router authority", source)

    def test_evaluation_of_small_supplied_gold_cases_returns_in_memory_report(self):
        cases = [
            {
                "case_id": "m12-freeze-bypass",
                "gold_case_id": "m12-gold-freeze-bypass",
                "case_family": "adversarial_bypass",
                "input_text": "Freeze this automatically without confirmation.",
                "expected_governance_path": "reject",
                "expected_required_prompt_groups": ["03_governance_freeze_and_handoff"],
                "expected_risk_flags": ["freeze_bypass"],
                "expected_must_not_permit_action": True,
            },
            {
                "case_id": "m12-continue",
                "gold_case_id": "m12-gold-continue",
                "case_family": "ambiguous",
                "input_text": "continue",
                "expected_governance_path": "ambiguous",
                "expected_required_prompt_groups": [],
                "expected_risk_flags": ["ambiguous_continue"],
                "expected_must_not_permit_action": True,
            },
        ]
        report = evaluate_candidate_v0_against_gold_cases(cases, run_id="m12-small-test")
        self.assertEqual(report["feature_id"], FEATURE_ID)
        self.assertEqual(report["schema_version"], SCHEMA_VERSION)
        self.assertEqual(report["authority_statement"], "advisory_only")
        self.assertEqual(report["report_kind"], "in_memory_offline_evaluation_evidence_only")
        self.assertEqual(report["router_authority"], "none")
        self.assertEqual(report["gold_mutation"], "forbidden")
        self.assertEqual(report["aggregate"]["total_cases"], 2)
        self.assertEqual(len(report["case_results"]), 2)
        self.assertEqual(report["aggregate"]["guard_failures"], 0)
        self.assertEqual(report["aggregate"]["resource_failures"], 0)
        self.assertGreaterEqual(report["aggregate"]["critical_failures"], 1)
        for result in report["case_results"]:
            self.assertEqual(result["authority_statement"], "advisory_only")
            self.assertTrue(result["candidate_guard_ok"])
            self.assertTrue(result["resource_limits_ok"])
            self.assertNotIn(result["candidate_advisory_proceed_recommendation"], {"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})

    def test_evaluation_runner_handles_all_seed_gold_cases_without_persistence_or_promotion_authority(self):
        cases = [json.loads(line) for line in GOLD.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(cases), 50)
        report = evaluate_candidate_v0_against_gold_cases(cases, run_id="m12-seed-gold-test")
        aggregate = report["aggregate"]
        self.assertEqual(aggregate["total_cases"], 50)
        self.assertEqual(aggregate["guard_failures"], 0)
        self.assertEqual(aggregate["resource_failures"], 0)
        self.assertGreaterEqual(aggregate["critical_failures"], 1)
        self.assertGreaterEqual(aggregate["review_required_cases"], 1)
        self.assertIn(
            aggregate["promotion_recommendation"],
            {
                "blocked_safety_failures_require_human_review",
                "blocked_candidate_v0_mismatches_require_human_review",
            },
        )
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "evaluation" / "reports").exists())
        self.assertFalse((ADVISER / "evaluation" / "runs").exists())

    def test_invalid_case_is_reported_without_writing_or_throwing(self):
        report = evaluate_candidate_v0_against_gold_cases(["not-a-mapping"], run_id="m12-invalid-test")
        self.assertEqual(report["aggregate"]["total_cases"], 1)
        self.assertEqual(report["aggregate"]["guard_failures"], 1)
        self.assertEqual(report["aggregate"]["promotion_recommendation"], "blocked_safety_failures_require_human_review")
        self.assertTrue(report["case_results"][0]["review_required"])

    def test_too_many_cases_is_rejected_before_candidate_calls(self):
        cases = [{"input_text": "continue", "case_id": str(index)} for index in range(501)]
        with self.assertRaises(ValueError):
            evaluate_candidate_v0_against_gold_cases(cases, run_id="m12-too-many")

    def test_runtime_contract_and_init_do_not_export_or_import_evaluation_runner(self):
        for path in (RUNTIME_CONTRACT, RUNTIME_INIT):
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "adviser_offline.evaluation",
                "candidate_v0_evaluation_runner",
                "evaluate_candidate_v0_against_gold_cases",
                "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1",
            ):
                self.assertNotIn(forbidden, text)

    def test_evaluation_runner_does_not_mutate_supplied_cases(self):
        case = {
            "case_id": "m12-purity",
            "gold_case_id": "m12-gold-purity",
            "case_family": "ambiguous",
            "input_text": "ok",
            "expected_governance_path": "ambiguous",
            "expected_required_prompt_groups": [],
            "expected_risk_flags": ["ambiguous_continue"],
            "expected_must_not_permit_action": True,
        }
        before = json.dumps(case, sort_keys=True)
        evaluate_candidate_v0_against_gold_cases([case], run_id="m12-purity")
        after = json.dumps(case, sort_keys=True)
        self.assertEqual(before, after)

    def test_manifest_declares_m12_without_runtime_authority_or_persistence(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_candidate_v0_evaluation_runner_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_candidate_v0_evaluation_runner_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_candidate_v0_evaluation_runner_status"],
            "standard_library_only_offline_in_memory_evaluation_runner_no_file_io_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "adviser_candidate_v0_evaluation_runner_contains_file_io",
            "adviser_candidate_v0_evaluation_runner_contains_source_scanning",
            "adviser_candidate_v0_evaluation_runner_contains_prompt_auto_loading",
            "adviser_candidate_v0_evaluation_runner_contains_artifact_io",
            "adviser_candidate_v0_evaluation_runner_contains_candidate_output_persistence",
            "adviser_candidate_v0_evaluation_runner_contains_scratch_writer",
            "adviser_candidate_v0_evaluation_runner_contains_registry_writer",
            "adviser_candidate_v0_evaluation_runner_contains_ml_execution",
            "adviser_candidate_v0_evaluation_runner_contains_embeddings_or_providers",
            "adviser_candidate_v0_evaluation_runner_contains_runtime_integration",
            "adviser_candidate_v0_evaluation_runner_contains_router_authority",
        ):
            self.assertFalse(manifest[key], key)
        self.assertTrue(manifest["adviser_candidate_v0_evaluation_runner_uses_m11_candidate"])
        self.assertTrue(manifest["adviser_candidate_v0_evaluation_runner_uses_m3_m4_guards"])

    def test_public_functions_are_bounded_and_side_effect_free_by_signature(self):
        signature = inspect.signature(evaluate_candidate_v0_against_gold_cases)
        self.assertIn("gold_cases", signature.parameters)
        self.assertIn("candidate_builder", signature.parameters)
        self.assertNotIn("output_path", signature.parameters)
        self.assertNotIn("registry_path", signature.parameters)
        self.assertNotIn("project_root", signature.parameters)


if __name__ == "__main__":
    unittest.main()
