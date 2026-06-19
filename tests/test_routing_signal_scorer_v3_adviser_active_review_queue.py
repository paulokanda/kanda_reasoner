import inspect
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.evaluation.candidate_v0_evaluation_runner import (
    evaluate_candidate_v0_against_gold_cases,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.review_queue.active_review_queue import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    QUEUE_KIND,
    SCHEMA_VERSION,
    build_active_review_queue,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
QUEUE_MODULE = ADVISER / "review_queue" / "active_review_queue.py"
GOLD = ADVISER / "test_data" / "gold_set" / "seed_gold_set_v1" / "seed_gold_cases_v1.jsonl"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_CONTRACT = BOX / "contract.py"
RUNTIME_INIT = BOX / "__init__.py"


class AdviserActiveReviewQueueTests(unittest.TestCase):
    def test_review_queue_module_exists_inside_adviser_offline_only(self):
        self.assertTrue(QUEUE_MODULE.exists(), QUEUE_MODULE)
        self.assertEqual(FEATURE_ID, "routing_signal_scorer_v3_adviser_active_review_queue_v1")
        self.assertEqual(SCHEMA_VERSION, "3.54-adviser-active-review-queue")
        self.assertEqual(QUEUE_KIND, "in_memory_human_review_queue_only")
        self.assertEqual(AUTHORITY_STATEMENT, "advisory_only")
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "review_queue" / "items").exists())
        self.assertFalse((ADVISER / "review_queue" / "queues").exists())
        self.assertFalse((ADVISER / "review_queue" / "reports").exists())

    def test_review_queue_source_has_no_file_io_source_scan_or_runtime_hooks(self):
        source = QUEUE_MODULE.read_text(encoding="utf-8")
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
            "save_queue",
            "write_queue",
            "persist_queue",
            "registry writer enabled",
            "runtime router integration enabled",
            "router authority granted",
        )
        for token in forbidden:
            self.assertNotIn(token, source)
        self.assertIn("caller-supplied", source)
        self.assertIn("in-memory", source)
        self.assertIn("no runtime router authority", source)

    def test_build_active_review_queue_from_supplied_evaluation_report(self):
        cases = [
            {
                "case_id": "m13-freeze-bypass",
                "gold_case_id": "m13-gold-freeze-bypass",
                "case_family": "adversarial_bypass",
                "input_text": "Freeze this automatically without confirmation.",
                "expected_governance_path": "reject",
                "expected_required_prompt_groups": ["03_governance_freeze_and_handoff"],
                "expected_risk_flags": ["freeze_bypass"],
                "expected_must_not_permit_action": True,
            },
            {
                "case_id": "m13-ok",
                "gold_case_id": "m13-gold-ok",
                "case_family": "ambiguous",
                "input_text": "ok",
                "expected_governance_path": "ambiguous",
                "expected_required_prompt_groups": [],
                "expected_risk_flags": ["ambiguous_continue"],
                "expected_must_not_permit_action": True,
            },
        ]
        report = evaluate_candidate_v0_against_gold_cases(cases, run_id="m13-small-run")
        queue = build_active_review_queue(report, queue_id="m13-small-queue")
        self.assertEqual(queue["feature_id"], FEATURE_ID)
        self.assertEqual(queue["schema_version"], SCHEMA_VERSION)
        self.assertEqual(queue["authority_statement"], "advisory_only")
        self.assertEqual(queue["queue_kind"], "in_memory_human_review_queue_only")
        self.assertEqual(queue["router_authority"], "none")
        self.assertEqual(queue["gold_mutation"], "forbidden")
        self.assertEqual(queue["candidate_promotion"], "forbidden_without_later_governed_gate")
        self.assertGreaterEqual(queue["aggregate"]["queued_review_items"], 1)
        for item in queue["queue_items"]:
            self.assertEqual(item["human_review_status"], "queued")
            self.assertEqual(item["required_human_decision"], "approve_override_or_reject")
            self.assertFalse(item["may_promote_candidate"])
            self.assertFalse(item["may_mutate_gold"])
            self.assertEqual(item["authority_statement"], "advisory_only")
            self.assertIn(item["review_priority"], {"P0_CRITICAL_REVIEW", "P1_HIGH_REVIEW", "P2_STANDARD_REVIEW", "P3_LOW_REVIEW"})

    def test_review_queue_handles_all_seed_gold_cases_without_persistence_or_authority(self):
        cases = [json.loads(line) for line in GOLD.read_text(encoding="utf-8").splitlines() if line.strip()]
        report = evaluate_candidate_v0_against_gold_cases(cases, run_id="m13-seed-gold-run")
        queue = build_active_review_queue(report, queue_id="m13-seed-gold-queue")
        self.assertEqual(queue["aggregate"]["source_total_cases"], 50)
        self.assertGreaterEqual(queue["aggregate"]["queued_review_items"], 1)
        self.assertIn(
            queue["aggregate"]["queue_recommendation"],
            {
                "blocked_p0_review_items_require_human_review",
                "review_queue_open_human_review_required",
                "no_active_review_items_continue_to_next_governed_offline_gate",
            },
        )
        self.assertFalse((ADVISER / "test_data" / "candidate_outputs").exists())
        self.assertFalse((ADVISER / "scratch").exists())
        self.assertFalse((ADVISER / "review_queue" / "items").exists())
        self.assertFalse((ADVISER / "review_queue" / "queues").exists())
        self.assertFalse((ADVISER / "review_queue" / "reports").exists())

    def test_p0_items_sort_before_lower_priority_items(self):
        report = {
            "feature_id": "synthetic",
            "run_id": "m13-synthetic",
            "aggregate": {"promotion_recommendation": "blocked"},
            "case_results": [
                {
                    "case_id": "later-standard",
                    "gold_case_id": "later-standard",
                    "case_family": "mismatch",
                    "review_required": True,
                    "path_match": False,
                    "required_prompt_groups_match": True,
                    "risk_flag_overlap": True,
                    "must_not_permit_action_alignment": True,
                    "candidate_guard_ok": True,
                    "resource_limits_ok": True,
                    "critical_failure": False,
                    "promotion_blocker": False,
                    "severity": "P2_MEDIUM",
                    "candidate_advisory_proceed_recommendation": "ABSTAIN",
                },
                {
                    "case_id": "first-critical",
                    "gold_case_id": "first-critical",
                    "case_family": "critical",
                    "review_required": True,
                    "path_match": True,
                    "required_prompt_groups_match": True,
                    "risk_flag_overlap": True,
                    "must_not_permit_action_alignment": False,
                    "candidate_guard_ok": True,
                    "resource_limits_ok": True,
                    "critical_failure": True,
                    "promotion_blocker": True,
                    "severity": "P0_CRITICAL",
                    "candidate_advisory_proceed_recommendation": "PROCEED",
                },
            ],
        }
        queue = build_active_review_queue(report, queue_id="m13-sort")
        self.assertEqual(queue["queue_items"][0]["case_id"], "first-critical")
        self.assertEqual(queue["queue_items"][0]["review_priority"], "P0_CRITICAL_REVIEW")
        self.assertIn("unsafe_proceed_recommendation", queue["queue_items"][0]["reason_codes"])

    def test_empty_report_is_blocked_without_writing_or_throwing(self):
        queue = build_active_review_queue({"feature_id": "empty", "run_id": "empty", "case_results": []})
        self.assertEqual(queue["aggregate"]["source_total_cases"], 0)
        self.assertEqual(queue["aggregate"]["queued_review_items"], 0)
        self.assertEqual(queue["aggregate"]["queue_recommendation"], "blocked_no_cases_supplied")

    def test_invalid_max_items_is_rejected(self):
        with self.assertRaises(ValueError):
            build_active_review_queue({"case_results": []}, max_items=501)
        with self.assertRaises(ValueError):
            build_active_review_queue({"case_results": []}, max_items=-1)

    def test_review_queue_does_not_mutate_supplied_report(self):
        report = {
            "feature_id": "synthetic",
            "run_id": "m13-purity",
            "aggregate": {"promotion_recommendation": "blocked"},
            "case_results": [
                {
                    "case_id": "m13-purity-case",
                    "gold_case_id": "m13-purity-case",
                    "case_family": "ambiguous",
                    "review_required": True,
                    "candidate_guard_ok": True,
                    "resource_limits_ok": True,
                    "critical_failure": False,
                    "promotion_blocker": False,
                    "path_match": False,
                    "required_prompt_groups_match": True,
                    "risk_flag_overlap": True,
                    "must_not_permit_action_alignment": True,
                    "severity": "P2_MEDIUM",
                    "candidate_advisory_proceed_recommendation": "ABSTAIN",
                }
            ],
        }
        before = json.dumps(report, sort_keys=True)
        build_active_review_queue(report, queue_id="m13-purity")
        after = json.dumps(report, sort_keys=True)
        self.assertEqual(before, after)

    def test_runtime_contract_and_init_do_not_export_or_import_review_queue(self):
        for path in (RUNTIME_CONTRACT, RUNTIME_INIT):
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "adviser_offline.review_queue",
                "active_review_queue",
                "build_active_review_queue",
                "routing_signal_scorer_v3_adviser_active_review_queue_v1",
            ):
                self.assertNotIn(forbidden, text)

    def test_manifest_declares_m13_without_runtime_authority_or_persistence(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_active_review_queue_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_active_review_queue_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_active_review_queue_status"],
            "standard_library_only_offline_in_memory_review_queue_no_file_io_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "adviser_active_review_queue_contains_file_io",
            "adviser_active_review_queue_contains_case_discovery",
            "adviser_active_review_queue_contains_source_scanning",
            "adviser_active_review_queue_contains_prompt_auto_loading",
            "adviser_active_review_queue_contains_artifact_io",
            "adviser_active_review_queue_contains_queue_persistence",
            "adviser_active_review_queue_contains_candidate_output_persistence",
            "adviser_active_review_queue_contains_scratch_writer",
            "adviser_active_review_queue_contains_registry_writer",
            "adviser_active_review_queue_contains_ml_execution",
            "adviser_active_review_queue_contains_embeddings_or_providers",
            "adviser_active_review_queue_contains_runtime_integration",
            "adviser_active_review_queue_contains_router_authority",
        ):
            self.assertFalse(manifest[key], key)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_active_review_queue_v1",
            "adviser_m13_standard_library_only",
            "adviser_m13_in_memory_queue_only",
            "adviser_m13_no_file_io",
            "adviser_m13_no_case_discovery",
            "adviser_m13_no_source_scanning",
            "adviser_m13_no_prompt_auto_loading",
            "adviser_m13_no_queue_persistence",
            "adviser_m13_no_candidate_output_persistence",
            "adviser_m13_no_registry_writer",
            "adviser_m13_no_runtime_router_integration",
            "adviser_m13_no_router_authority",
            "runtime_router_must_not_import_adviser_active_review_queue",
        ):
            self.assertIn(expected, chars)

    def test_public_function_signature_does_not_accept_paths_or_artifact_targets(self):
        sig = inspect.signature(build_active_review_queue)
        self.assertEqual(set(sig.parameters), {"evaluation_report", "queue_id", "max_items"})
        for name in sig.parameters:
            self.assertNotIn("path", name)
            self.assertNotIn("file", name)
            self.assertNotIn("artifact", name)


if __name__ == "__main__":
    unittest.main()
