
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
REGISTRY = ADVISER / "registry"
FEATURE_ID = "routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1"
SCHEMA_VERSION = "3.45-adviser-gold-manifest-run-registry"

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.hash_utils import (
    canonical_json,
    hash_mapping,
    hash_record_without_field,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.gold_manifest import (
    build_case_manifest_entry,
    build_gold_manifest_record,
    validate_gold_manifest_record,
    assert_gold_manifest_valid,
)
from kanda_reasoner_app.routing_signal_scorer.adviser_offline.registry.run_registry import (
    build_run_registry_record,
    validate_run_registry_record,
    assert_run_registry_record_review_eligible,
)


def reviewed_case(case_id="case-freeze-001", **overrides):
    case = {
        "case_id": case_id,
        "input_hash": "0" * 64,
        "teacher_answer_hash": "1" * 64,
        "human_review_status": "approved_as_gold",
        "expected_severity_if_missed": "critical",
        "supersedes": None,
        "provenance": {"source": "unit-test-fixture"},
    }
    case.update(overrides)
    return case


def reviewed_entry(case_id="case-freeze-001", **overrides):
    return build_case_manifest_entry(reviewed_case(case_id, **overrides))


def gold_manifest(case_count=2):
    entries = [reviewed_entry(f"case-freeze-{i:03d}") for i in range(1, case_count + 1)]
    return build_gold_manifest_record(
        manifest_id="manifest-v1-fixture",
        gold_set_version="gold-v1-fixture",
        case_entries=entries,
        created_by="human-review-fixture",
    )


def safe_run_summary(**overrides):
    summary = {
        "run_id": "run-m6-fixture",
        "candidate_id": "candidate-fixture",
        "candidate_version": "0.0-fixture",
        "candidate_code_hash": "2" * 64,
        "gold_set_version": "gold-v1-fixture",
        "gold_manifest_hash": "3" * 64,
        "cases_run": 2,
        "critical_failures": 0,
        "promotion_blockers": 0,
        "aggregate_severity": "none",
        "status": "eligible_for_review",
        "authority_statement": "advisory_only",
    }
    summary.update(overrides)
    return summary


class AdviserGoldManifestRunRegistryTests(unittest.TestCase):
    def test_m6_registry_modules_exist_and_are_standard_library_only(self):
        for rel in ("__init__.py", "hash_utils.py", "gold_manifest.py", "run_registry.py"):
            path = REGISTRY / rel
            self.assertTrue(path.exists(), rel)
            text = path.read_text(encoding="utf-8")
            text.encode("ascii")
            lowered = text.lower()
            for forbidden in (
                "requests", "subprocess", "socket", "openai", "chromadb", "faiss",
                "numpy", "pandas", "sklearn", "torch", "tensorflow",
                "from kanda_reasoner_app.routing_signal_scorer.contract",
                "import kanda_reasoner_app.routing_signal_scorer.contract",
                "candidate_scorer", "run_candidate", "load_prompt", "auto_load_prompt",
                "pathlib", "glob", "os.walk", "scandir", "listdir",
            ):
                self.assertNotIn(forbidden, lowered)
            self.assertNotIn("open(", text)
            self.assertNotIn("write_text", text)
            self.assertNotIn("read_text", text)

    def test_hash_utils_are_deterministic_for_supplied_values_only(self):
        first = {"b": 2, "a": [1, 2, 3]}
        second = {"a": [1, 2, 3], "b": 2}
        self.assertEqual(canonical_json(first), canonical_json(second))
        self.assertEqual(hash_mapping(first), hash_mapping(second))
        self.assertEqual(len(hash_mapping(first)), 64)

    def test_build_and_validate_gold_manifest_from_reviewed_supplied_entries(self):
        manifest = gold_manifest(case_count=3)
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["feature_id"], FEATURE_ID)
        self.assertEqual(manifest["authority_statement"], "advisory_only")
        self.assertEqual(manifest["case_count"], 3)
        self.assertEqual(len(manifest["case_hashes"]), 3)
        self.assertEqual(manifest["manifest_hash"], hash_record_without_field(manifest, "manifest_hash"))
        result = validate_gold_manifest_record(manifest)
        self.assertTrue(result["ok"], result)
        self.assertIs(assert_gold_manifest_valid(manifest), manifest)

    def test_unreviewed_case_cannot_enter_gold_manifest(self):
        with self.assertRaises(ValueError):
            build_case_manifest_entry(reviewed_case(human_review_status="draft"))
        bad_entry = reviewed_entry()
        bad_entry["human_review_status"] = "draft"
        with self.assertRaises(ValueError):
            build_gold_manifest_record(
                manifest_id="manifest-bad",
                gold_set_version="gold-bad",
                case_entries=[bad_entry],
                created_by="human-review-fixture",
            )

    def test_manifest_hash_tampering_is_detected(self):
        manifest = gold_manifest(case_count=2)
        tampered = dict(manifest)
        tampered["case_count"] = 999
        result = validate_gold_manifest_record(tampered)
        self.assertFalse(result["ok"])
        self.assertIn("case_count mismatch", result["errors"])
        self.assertIn("manifest_hash mismatch", result["errors"])

    def test_build_and_validate_run_registry_record_from_supplied_summary(self):
        manifest = gold_manifest(case_count=2)
        record = build_run_registry_record(
            run_summary=safe_run_summary(gold_manifest_hash=manifest["manifest_hash"]),
            gold_manifest=manifest,
            candidate_metadata={
                "candidate_id": "candidate-fixture",
                "candidate_version": "0.0-fixture",
                "candidate_code_hash": "2" * 64,
            },
            registry_record_id="registry-record-m6-safe",
            recorded_by="human-review-fixture",
        )
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)
        self.assertEqual(record["feature_id"], FEATURE_ID)
        self.assertEqual(record["authority_statement"], "advisory_only")
        self.assertFalse(record["promotion_blocked"])
        self.assertEqual(record["registry_status"], "eligible_for_human_review")
        self.assertEqual(record["record_hash"], hash_record_without_field(record, "record_hash"))
        result = validate_run_registry_record(record)
        self.assertTrue(result["ok"], result)
        self.assertIs(assert_run_registry_record_review_eligible(record), record)

    def test_critical_failures_make_run_registry_record_promotion_blocked(self):
        manifest = gold_manifest(case_count=2)
        record = build_run_registry_record(
            run_summary=safe_run_summary(critical_failures=1, promotion_blockers=1, status="blocked"),
            gold_manifest=manifest,
            candidate_metadata={
                "candidate_id": "candidate-fixture",
                "candidate_version": "0.0-fixture",
                "candidate_code_hash": "2" * 64,
            },
            registry_record_id="registry-record-m6-blocked",
            recorded_by="human-review-fixture",
        )
        self.assertTrue(record["promotion_blocked"])
        self.assertEqual(record["registry_status"], "blocked")
        result = validate_run_registry_record(record)
        self.assertTrue(result["ok"], result)
        with self.assertRaises(ValueError):
            assert_run_registry_record_review_eligible(record)

    def test_manifest_declares_m6_gold_manifest_run_registry(self):
        manifest = json.loads((BOX / "box_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["adviser_gold_manifest_run_registry_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["adviser_gold_manifest_run_registry_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["adviser_gold_manifest_run_registry_status"],
            "standard_library_only_offline_record_builders_no_file_io_no_candidate_no_runtime_behavior_change",
        )
        chars = set(manifest["protected_architecture_characteristics"])
        for expected in (
            "adviser_gold_manifest_run_registry_v1",
            "adviser_registry_standard_library_only",
            "adviser_hash_utils_supplied_values_only",
            "adviser_gold_manifest_supplied_records_only",
            "adviser_run_registry_supplied_summaries_only",
            "adviser_registry_no_file_io",
            "adviser_registry_no_scratch_writer",
            "adviser_registry_no_gold_set_creation",
            "adviser_registry_no_candidate_execution",
            "adviser_registry_no_source_scanning",
            "adviser_registry_requires_human_reviewed_gold_cases",
            "adviser_registry_critical_failures_block_promotion",
            "adviser_registry_records_are_advisory_evidence_only",
            "no_adviser_candidate_from_m6_registry",
            "no_adviser_runtime_integration_from_m6_registry",
        ):
            self.assertIn(expected, chars)

    def test_m6_still_has_no_candidate_gold_test_data_scratch_or_runtime_behavior(self):
        for rel in ("candidate", "scratch", "gold"):
            self.assertFalse((ADVISER / rel).exists(), rel)
        self.assertTrue((REGISTRY / "hash_utils.py").exists())
        self.assertTrue((REGISTRY / "gold_manifest.py").exists())
        self.assertTrue((REGISTRY / "run_registry.py").exists())
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "adviser_offline",
            "gold_manifest",
            "run_registry",
            "build_gold_manifest_record",
            "build_run_registry_record",
            "adviser_candidate",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
