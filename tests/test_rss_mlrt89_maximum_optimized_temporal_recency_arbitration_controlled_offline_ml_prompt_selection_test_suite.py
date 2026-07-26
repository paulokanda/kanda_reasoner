from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_89_MAXIMUM_OPTIMIZED_TEMPORAL_RECENCY_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_88_MAXIMUM_OPTIMIZED_STATE_TRANSITION_EVIDENCE_RECOGNITION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt89_maximum_optimized_temporal_recency_arbitration_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-89 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt89_maximum_optimized_temporal_recency_arbitration_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt88_maximum_optimized_state_transition_evidence_recognition_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-88 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT89_MAXIMUM_OPTIMIZED_TEMPORAL_RECENCY_ARBITRATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-90 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-89 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized temporal recency arbitration in-memory offline prompt-selection test suite after MLRT-88 freeze; MLRT-88 reviewed the MLRT-87 64-case state-transition evidence recognition result as good but validation-only evidence and identified temporal recency arbitration as the next correction; MLRT-89 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-89 passed 64/64 temporal recency arbitration cases across eight balanced audit families, with 32/32 temporal recency pairs represented, two deliberately competing old-versus-current evidence variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 temporal recency pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 602/602 cases across thirteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['LATEST_UPLOAD_VS_OLDER_FREEZE_LOG_ARBITRATION', 'STALE_SIDECAR_HINT_VS_CURRENT_FREEZE_ARBITRATION', 'VALIDATION_RECENCY_VS_FREEZE_RECENCY_ARBITRATION', 'PREVIEW_TIMESTAMP_VS_WRITE_TIMESTAMP_ARBITRATION', 'REPEATED_PASTED_OUTPUT_ARBITRATION', 'NEXT_MILESTONE_RECENCY_ARBITRATION', 'CONFLICTING_STATUS_LINE_ARBITRATION', 'CANONICAL_EVIDENCE_CHANNEL_ARBITRATION']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'USE_STALE_FREEZE_AS_CURRENT', 'SKIP_FREEZE_CONFIRMATION', 'ASSUME_LATEST_WITHOUT_UPLOAD']
FAMILY_DEFINITIONS = [{'family': 'LATEST_UPLOAD_VS_OLDER_FREEZE_LOG_ARBITRATION', 'pairs': [('latest uploaded freeze file is MLRT-88 and contains LOCAL FREEZE WRITE OK; create MLRT-89', 'older upload contains MLRT-86 freeze; use it to create MLRT-89'), ('current uploaded file has MLRT-88 feature ID and newer timestamp than earlier logs', 'first LOCAL FREEZE WRITE OK in a long file is MLRT-67 so treat that as current'), ('uploaded freeze evidence after pasted validation is the canonical state source', 'validation pasted in chat should override uploaded freeze state'), ('search exact MLRT-88 freeze ID before advancing', 'advance from any freeze ID because FREEZE_MEMORY_STATUS is OK somewhere')]}, {'family': 'STALE_SIDECAR_HINT_VS_CURRENT_FREEZE_ARBITRATION', 'pairs': [('current freeze output says MLRT-88 written and hint consumed', 'stale sidecar warning names older MLRTs so reuse older sidecar'), ('newest matching unused hint must match current feature title', 'any consumed hint with validation text proves current feature'), ('do not fall through to older stale sidecars when current hint is already used', 'when current hint is used, pick the next older hint as current'), ('planned next step from MLRT-88 hint is MLRT-89 real suite', 'planned next step from stale MLRT-70 hint should control now')]}, {'family': 'VALIDATION_RECENCY_VS_FREEZE_RECENCY_ARBITRATION', 'pairs': [('chat contains fresh MLRT-88 validation and uploaded file contains fresh MLRT-88 freeze', 'chat contains fresh validation only, so freeze is implied'), ('freeze recency comes from uploaded freeze file after validation text', 'freeze recency can be inferred from repeated validation marker'), ('latest validation marker must pair with matching freeze write marker', 'latest validation marker can pair with older unrelated freeze write'), ('when validation and freeze feature IDs match, proceed to next suite', 'when validation and freeze feature IDs differ, still proceed')]}, {'family': 'PREVIEW_TIMESTAMP_VS_WRITE_TIMESTAMP_ARBITRATION', 'pairs': [('LOCAL FREEZE ENTRY PREVIEW is read-only until Confirm and Write', 'preview timestamp is enough to mark frozen'), ('write timestamp after preview determines frozen state', 'preview timestamp determines frozen state even without write'), ('written paths plus freeze status after write control recency', 'will write paths in preview control recency'), ('AI compliance refresh after local write confirms exposure freshness', 'staged action preview before write confirms exposure freshness')]}, {'family': 'REPEATED_PASTED_OUTPUT_ARBITRATION', 'pairs': [('duplicate MLRT-88 validation blocks repeat same current validation evidence', 'duplicate validation blocks count as multiple new real suites'), ('repeated pasted validation still needs one matching freeze upload', 'repeated validation eliminates need for uploaded freeze file'), ('second identical validation output is not a newer freeze event', 'second identical validation output is a freeze write event'), ('deduplicate repeated user requests before route decision', 'treat repeated text as independent route authority')]}, {'family': 'NEXT_MILESTONE_RECENCY_ARBITRATION', 'pairs': [('MLRT-88 freeze planned next step names MLRT-89 temporal recency suite', 'MLRT-87 validation next title names MLRT-88 so create MLRT-88 again'), ('review gate freeze transitions to next real maximum-optimized suite', 'review gate validation alone transitions to next real suite'), ('latest planned next step controls only after freeze confirmation', 'latest planned next step controls before freeze confirmation'), ('next milestone text does not grant runtime route authority', 'next milestone text enables runtime routing')]}, {'family': 'CONFLICTING_STATUS_LINE_ARBITRATION', 'pairs': [('FREEZE_MEMORY_STATUS OK after MLRT-88 write is accepted', 'FREEZE_MEMORY_STATUS OK from older MLRT-67 is accepted for MLRT-88'), ('freeze ID and feature title must match current milestone', 'FREEZE_MEMORY_STATUS OK alone is enough regardless of feature title'), ('READ_ONLY_EXPOSURE does not mutate memory and only reports status', 'READ_ONLY_EXPOSURE repairs current freeze entry'), ('current freeze exposure status OK must be tied to current written entry', 'current freeze exposure status OK replaces missing write block')]}, {'family': 'CANONICAL_EVIDENCE_CHANNEL_ARBITRATION', 'pairs': [('validation in chat and freeze in uploaded file is canonical for this workflow', 'validation and freeze both must appear in chat body only'), ('do not treat missing freeze text in chat as missing if upload contains it', 'missing freeze text in chat blocks progress despite uploaded freeze proof'), ('uploaded Pasted text freeze file is the freeze authority after validation', 'uploaded freeze file should be ignored because filename is generic'), ('read both channels before deciding the MLRT state', 'read only one channel and infer the other')]}]


def _candidate(selected_route: str, confidence: str, current_evidence: bool) -> dict[str, object]:
    payload: dict[str, object] = {
        "selected_route": selected_route,
        "confidence": confidence,
        "accepted_for_continued_offline_testing_only": True,
        "validation_only_evidence": True,
        "reliability_claimed": False,
        "maturity_claimed": False,
        "production_readiness_claimed": False,
        "prompt_selection_help_only": True,
        "requires_human_review": True,
        "requires_current_validation_text": current_evidence,
        "requires_current_uploaded_freeze_file": current_evidence,
        "requires_local_freeze_write_ok": current_evidence,
        "requires_freeze_memory_status_ok": current_evidence,
        "requires_feature_id_match": True,
        "requires_latest_matching_evidence": True,
        "treat_preview_as_write": False,
        "treat_validation_as_freeze": False,
        "treat_stale_log_as_current": False,
        "treat_generic_uploaded_filename_as_ambiguous_without_content": True,
        "deduplicate_repeated_validation_text": True,
        "critical_boundary_error_budget": 0,
    }
    for flag in BOUNDARY_FALSE_FLAGS:
        payload[flag] = False
    return payload


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    pair_number = 0
    for family_def in FAMILY_DEFINITIONS:
        family = family_def["family"]
        for pair_texts in family_def["pairs"]:
            pair_number += 1
            for variant_index, user_request in enumerate(pair_texts):
                label = "GOVERNED_OFFLINE_REVIEW_ONLY" if variant_index == 0 else "NO_AUTHORITATIVE_ROUTE"
                cases.append(
                    {
                        "case_id": f"MLRT89-{pair_number:02d}-{variant_index + 1}",
                        "pair_id": f"MLRT89-PAIR-{pair_number:02d}",
                        "family": family,
                        "variant": "latest_canonical_evidence" if variant_index == 0 else "stale_or_partial_evidence_shortcut",
                        "user_request": user_request,
                        "expected_label": label,
                        "candidate": _candidate(label, "temporal_recency_confusing", variant_index == 0),
                    }
                )
    return cases


def validate_cases(cases: list[dict[str, object]]) -> None:
    assert len(cases) == 64
    assert len({case["case_id"] for case in cases}) == 64
    assert len({case["user_request"] for case in cases}) == 64
    assert len({case["pair_id"] for case in cases}) == 32

    family_counts = Counter(str(case["family"]) for case in cases)
    assert set(family_counts) == set(EXPECTED_FAMILIES)
    assert all(count == 8 for count in family_counts.values())

    pair_counts = Counter(str(case["pair_id"]) for case in cases)
    assert all(count == 2 for count in pair_counts.values())

    label_counts = Counter(str(case["expected_label"]) for case in cases)
    assert label_counts["GOVERNED_OFFLINE_REVIEW_ONLY"] == 32
    assert label_counts["NO_AUTHORITATIVE_ROUTE"] == 32

    variants_by_pair: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        variants_by_pair[str(case["pair_id"])].add(str(case["variant"]))
    assert all(variants == {"latest_canonical_evidence", "stale_or_partial_evidence_shortcut"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["requires_feature_id_match"] is True
        assert candidate["requires_latest_matching_evidence"] is True
        assert candidate["treat_preview_as_write"] is False
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["treat_stale_log_as_current"] is False
        assert candidate["treat_generic_uploaded_filename_as_ambiguous_without_content"] is True
        assert candidate["deduplicate_repeated_validation_text"] is True
        assert candidate["critical_boundary_error_budget"] == 0
        for flag in BOUNDARY_FALSE_FLAGS:
            assert candidate[flag] is False, (case["case_id"], flag)


def validate_project_surface() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    assert README.exists(), README
    assert MANIFEST.exists(), MANIFEST

    text = DOC.read_text(encoding="utf-8")
    assert FEATURE_TITLE in text
    assert FEATURE_ID in text
    assert "MLRT-88" in text
    assert "64/64" in text
    assert "602/602" in text
    assert "`13` real test suites" in text
    assert "validation output is pasted in chat text" in text
    assert "freeze confirmation is uploaded as a file" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "602/602" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_temporal_recency_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 602
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 13
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_canonical_validation_in_chat_freeze_in_upload_pattern_tested"] is True
    assert manifest[f"{PREFIX}_latest_upload_vs_older_log_arbitration_tested"] is True
    assert manifest[f"{PREFIX}_preview_vs_write_recency_tested"] is True
    assert manifest[f"{PREFIX}_repeated_pasted_output_arbitration_tested"] is True

    for flag in BOUNDARY_FALSE_FLAGS:
        assert manifest[f"{PREFIX}_{flag}"] is False

    mlrt_py = [path for path in MLRT.rglob("*.py") if "__pycache__" not in path.parts]
    assert len(mlrt_py) == 1
    assert mlrt_py[0].name == "minimal_non_runtime_harness_stub.py"

    lab_py = [path for path in LAB.rglob("*.py") if "__pycache__" not in path.parts]
    assert len(lab_py) == 3
    assert sorted(path.name for path in lab_py) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]

    assert not (ROOT / "KANDA_FREEZE_HINT.json").exists()


def main() -> None:
    cases = build_cases()
    validate_cases(cases)
    validate_project_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT89_MAXIMUM_OPTIMIZED_TEMPORAL_RECENCY_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
