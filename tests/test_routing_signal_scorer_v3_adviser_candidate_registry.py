import inspect
import json
import unittest
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.candidate_registry import (
    AUTHORITY_STATEMENT,
    FEATURE_ID,
    SCHEMA_VERSION,
    build_candidate_registry_record,
    validate_candidate_registry_record,
    assert_candidate_registry_record_valid,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.hash_utils import hash_record_without_field

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
MODULE = ADVISER / "registry" / "candidate_registry.py"
MANIFEST = BOX / "box_manifest.json"
RUNTIME_CONTRACT = BOX / "contract.py"
RUNTIME_INIT = BOX / "__init__.py"


def candidate_metadata(**overrides):
    data = {
        "candidate_id": "candidate-v0-lexical",
        "candidate_version": "0.1.0-offline-lexical",
        "candidate_feature_id": "routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1",
        "candidate_module_path": "kanda_reasoner_app/routing_signal_scorer/adviser_offline/candidate_v0/offline_lexical_scorer.py",
        "candidate_code_hash": "a" * 64,
        "candidate_contract_schema_version": "3.42-adviser-contract-validator-output-guard",
        "gold_set_version": "seed_gold_set_v1",
    }
    data.update(overrides)
    return data


def evaluation_report(**aggregate_overrides):
    aggregate = {
        "total_cases": 50,
        "exact_matches": 35,
        "mismatches": 15,
        "guard_failures": 0,
        "resource_failures": 0,
        "critical_failures": 0,
        "promotion_recommendation": "review_queue_open_human_review_required",
    }
    aggregate.update(aggregate_overrides)
    return {
        "feature_id": "routing_signal_scorer_v3_adviser_candidate_v0_evaluation_runner_v1",
        "run_id": "m12-eval-run-not-persisted",
        "aggregate": aggregate,
        "case_results": [{} for _ in range(int(aggregate.get("total_cases", 0)))],
    }


def review_queue(**aggregate_overrides):
    aggregate = {
        "queued_review_items": 15,
        "p0_items": 0,
        "p1_items": 2,
        "queue_recommendation": "review_queue_open_human_review_required",
    }
    aggregate.update(aggregate_overrides)
    return {
        "feature_id": "routing_signal_scorer_v3_adviser_active_review_queue_v1",
        "queue_id": "m13-queue-not-persisted",
        "aggregate": aggregate,
        "queue_items": [{} for _ in range(int(aggregate.get("queued_review_items", 0)))],
    }


class AdviserCandidateRegistryTests(unittest.TestCase):
    def test_m14_module_exists_and_is_standard_library_only(self):
        self.assertTrue(MODULE.exists())
        text = MODULE.read_text(encoding="utf-8")
        text.encode("ascii")
        lowered = text.lower()
        for forbidden in (
            "requests", "subprocess", "socket", "openai", "chromadb", "faiss",
            "numpy", "pandas", "sklearn", "torch", "tensorflow", "pathlib",
            "glob", "os.walk", "scandir", "listdir", "load_prompt", "auto_load_prompt",
            "run_candidate", "scratch_writer", "registry_writer",
        ):
            self.assertNotIn(forbidden, lowered)
        for forbidden in ("open(", "write_text", "read_text", "import os", "from pathlib"):
            self.assertNotIn(forbidden, text)

    def test_builds_valid_in_memory_candidate_registry_record(self):
        record = build_candidate_registry_record(
            candidate_metadata=candidate_metadata(),
            evaluation_report=evaluation_report(),
            review_queue=review_queue(),
            registry_record_id="m14-record-fixture",
            recorded_by="unit-test-human-review-pending",
        )
        self.assertEqual(record["feature_id"], FEATURE_ID)
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["authority_statement"], AUTHORITY_STATEMENT)
        self.assertEqual(record["registry_kind"], "in_memory_candidate_registry_record_only")
        self.assertEqual(record["router_authority"], "none")
        self.assertFalse(record["may_promote_candidate"])
        self.assertFalse(record["may_mutate_gold"])
        self.assertFalse(record["may_record_registry"])
        self.assertTrue(record["promotion_blocked"])
        self.assertIn("m16_promotion_gate_not_yet_run", record["promotion_blockers"])
        self.assertIn("candidate_gold_mismatches_present", record["promotion_blockers"])
        self.assertIn("human_review_queue_not_empty", record["promotion_blockers"])
        self.assertEqual(record["record_hash"], hash_record_without_field(record, "record_hash"))
        result = validate_candidate_registry_record(record)
        self.assertTrue(result["ok"], result)
        self.assertIs(assert_candidate_registry_record_valid(record), record)

    def test_registry_record_is_still_promotion_blocked_even_when_clean(self):
        record = build_candidate_registry_record(
            candidate_metadata=candidate_metadata(),
            evaluation_report=evaluation_report(mismatches=0, total_cases=50, critical_failures=0),
            review_queue=review_queue(queued_review_items=0, p0_items=0, p1_items=0),
        )
        self.assertTrue(record["promotion_blocked"])
        self.assertEqual(record["promotion_blockers"], ["m16_promotion_gate_not_yet_run"])
        self.assertEqual(record["registry_status"], "registered_for_later_promotion_gate_review")
        self.assertFalse(record["may_promote_candidate"])

    def test_critical_or_p0_evidence_blocks_with_critical_status(self):
        record = build_candidate_registry_record(
            candidate_metadata=candidate_metadata(),
            evaluation_report=evaluation_report(critical_failures=1, mismatches=0),
            review_queue=review_queue(queued_review_items=1, p0_items=1),
        )
        self.assertEqual(record["registry_status"], "blocked_critical_review_required")
        self.assertIn("critical_failures_present", record["promotion_blockers"])
        self.assertIn("p0_review_items_present", record["promotion_blockers"])

    def test_validation_detects_tampering_and_bad_hashes(self):
        record = build_candidate_registry_record(
            candidate_metadata=candidate_metadata(),
            evaluation_report=evaluation_report(),
            review_queue=review_queue(),
        )
        tampered = dict(record)
        tampered["router_authority"] = "final_route"
        result = validate_candidate_registry_record(tampered)
        self.assertFalse(result["ok"])
        self.assertIn("router_authority must be none", result["errors"])
        self.assertIn("record_hash mismatch", result["errors"])

        with self.assertRaises(ValueError):
            build_candidate_registry_record(candidate_metadata=candidate_metadata(candidate_code_hash="not-a-hash"))

    def test_does_not_mutate_supplied_inputs(self):
        metadata = candidate_metadata()
        evaluation = evaluation_report()
        queue = review_queue()
        before = json.dumps([metadata, evaluation, queue], sort_keys=True)
        build_candidate_registry_record(candidate_metadata=metadata, evaluation_report=evaluation, review_queue=queue)
        after = json.dumps([metadata, evaluation, queue], sort_keys=True)
        self.assertEqual(before, after)

    def test_module_does_not_use_file_io_or_runtime_authority_names(self):
        source = inspect.getsource(build_candidate_registry_record)
        for forbidden in ("open(", "read_text", "write_text", "Path(", "router_authority_change"):
            self.assertNotIn(forbidden, source)

    def test_runtime_contract_and_init_do_not_export_or_import_candidate_registry(self):
        for path in (RUNTIME_CONTRACT, RUNTIME_INIT):
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "adviser_offline.registry.candidate_registry",
                "build_candidate_registry_record",
                "routing_signal_scorer_v3_adviser_candidate_registry_v1",
            ):
                self.assertNotIn(forbidden, text)

    def test_manifest_declares_m14_without_runtime_authority_or_persistence(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_candidate_registry_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_candidate_registry_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_candidate_registry_status"],
            "standard_library_only_offline_in_memory_candidate_registry_record_builder_no_file_io_no_persistence_no_runtime_behavior_change",
        )
        for key in (
            "adviser_candidate_registry_contains_file_io",
            "adviser_candidate_registry_contains_case_discovery",
            "adviser_candidate_registry_contains_source_scanning",
            "adviser_candidate_registry_contains_prompt_auto_loading",
            "adviser_candidate_registry_contains_artifact_io",
            "adviser_candidate_registry_contains_registry_persistence",
            "adviser_candidate_registry_contains_registry_writer",
            "adviser_candidate_registry_contains_candidate_output_persistence",
            "adviser_candidate_registry_contains_scratch_writer",
            "adviser_candidate_registry_contains_gold_mutation",
            "adviser_candidate_registry_contains_ml_execution",
            "adviser_candidate_registry_contains_embeddings_or_providers",
            "adviser_candidate_registry_contains_runtime_integration",
            "adviser_candidate_registry_contains_router_authority",
        ):
            self.assertIs(manifest[key], False, key)
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_candidate_registry_v1",
            "adviser_candidate_registry_in_memory_record_only",
            "adviser_candidate_registry_no_registry_writer",
            "adviser_candidate_registry_no_router_authority",
            "adviser_candidate_registry_promotion_blocked_until_m16_gate",
        ):
            self.assertIn(expected, chars)


if __name__ == "__main__":
    unittest.main()
