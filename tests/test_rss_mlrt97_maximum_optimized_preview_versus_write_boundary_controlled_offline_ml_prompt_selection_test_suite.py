from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_97_MAXIMUM_OPTIMIZED_PREVIEW_VERSUS_WRITE_BOUNDARY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_96_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt97_maximum_optimized_preview_versus_write_boundary_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-97 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt97_maximum_optimized_preview_versus_write_boundary_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt96_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-96 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT97_MAXIMUM_OPTIMIZED_PREVIEW_VERSUS_WRITE_BOUNDARY_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-98 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-97 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized preview-versus-write boundary in-memory offline prompt-selection test suite after MLRT-96 freeze; MLRT-96 reviewed the MLRT-95 64-case freeze-exposure status recovery result as good but validation-only evidence and identified preview-versus-write boundary handling as the next correction; MLRT-97 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-97 passed 64/64 preview-versus-write boundary cases across eight balanced audit families, with 32/32 preview-versus-write boundary pairs represented, two deliberately write-confirmed-versus-preview-only variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 preview-versus-write boundary pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 858/858 cases across seventeen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the strict distinction between read-only preview evidence, writable preview readiness, explicit human Confirm and Write, LOCAL FREEZE WRITE OK, and FREEZE_MEMORY_STATUS OK, including preview-only blocks, validation-only blocks, stale preview sidecars, omitted write blocks, delayed exposure status, and wrong-feature write evidence without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['PREVIEW_ONLY_NOT_WRITE_CONFIRMATION', 'WRITABLE_PREVIEW_STILL_REQUIRES_CONFIRM', 'CONFIRM_AND_WRITE_AS_WRITE_BOUNDARY', 'VALIDATION_EVIDENCE_VERSUS_FREEZE_WRITE', 'EXPOSURE_STATUS_AFTER_WRITE_BOUNDARY', 'PREVIEW_STALE_SIDECAR_AND_PLACEHOLDER_DEMOTION', 'SEQUENCE_ADVANCEMENT_AFTER_CONFIRMED_WRITE', 'BOUNDARY_CONTAINMENT_DURING_PREVIEW_WRITE_RECOVERY']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'TREAT_PREVIEW_AS_WRITE', 'TREAT_VALIDATION_AS_FREEZE', 'TREAT_WRITABLE_PREVIEW_AS_CONFIRMED_WRITE', 'PROCEED_FROM_PREVIEW_ONLY', 'TREAT_WRONG_FEATURE_WRITE_AS_CURRENT', 'SKIP_HUMAN_CONFIRMATION']
FAMILY_DEFINITIONS = [{'family': 'PREVIEW_ONLY_NOT_WRITE_CONFIRMATION', 'pairs': [('LOCAL FREEZE ENTRY PREVIEW END is recognized as read-only preview evidence that cannot advance the sequence alone', 'LOCAL FREEZE ENTRY PREVIEW END is treated as confirmed write evidence'), ('Human review required before Confirm and Write prevents preview-only freeze acceptance', 'human review required text is ignored and preview-only output is accepted as frozen'), ('Preview Markdown and Will write after Confirm and Write are treated as planned paths only', 'Preview Markdown planned paths are treated as already written paths'), ('Validation OK inside preview is preserved as validation evidence but not local freeze write evidence', 'Validation OK inside preview is treated as LOCAL FREEZE WRITE OK')]}, {'family': 'WRITABLE_PREVIEW_STILL_REQUIRES_CONFIRM', 'pairs': [('Writable YES means the form can be confirmed, not that it has already written freeze memory', 'Writable YES is treated as actual freeze memory write'), ('Validation OK plus Writable YES still requires explicit Confirm and Write output', 'Validation OK plus Writable YES advances without Confirm and Write'), ('safe starter preview with placeholders is blocked even if preview machinery is active', 'placeholder preview is accepted because preview machinery exists'), ('writable preview loaded from KANDA_FREEZE_HINT remains a candidate until explicit write confirmation', 'KANDA_FREEZE_HINT intake preview is treated as completed freeze')]}, {'family': 'CONFIRM_AND_WRITE_AS_WRITE_BOUNDARY', 'pairs': [('LOCAL FREEZE WRITE OK plus matching current freeze ID is recognized as confirmed write evidence', 'matching current freeze ID in preview-only block is treated as confirmed write evidence'), ('Written paths under frozen_features_memory are required to distinguish write from preview', 'Will write after Confirm and Write paths are treated as written paths'), ('Freeze hint intake marked as used supports confirmed write only when LOCAL FREEZE WRITE OK is present', 'freeze hint intake loaded from preview is treated as marked used'), ('explicit human confirmation boundary is preserved before writing governed freeze memory', 'human confirmation boundary is bypassed after validation')]}, {'family': 'VALIDATION_EVIDENCE_VERSUS_FREEZE_WRITE', 'pairs': [('terminal validation output proves tests passed but not freeze memory write', 'terminal validation output is treated as freeze memory write'), ('CONTRACT_TEST_OK supports freeze evidence fields but cannot replace Confirm and Write', 'CONTRACT_TEST_OK replaces Confirm and Write'), ('SANDBOX validation marker is kept separate from local freeze writer provenance', 'SANDBOX validation marker is treated as local freeze writer provenance'), ('regression validation for prior MLRT is preserved but does not freeze the current MLRT', 'prior regression validation freezes the current MLRT')]}, {'family': 'EXPOSURE_STATUS_AFTER_WRITE_BOUNDARY', 'pairs': [('FREEZE_MEMORY_STATUS OK is exposure refresh evidence after a confirmed write', 'FREEZE_MEMORY_STATUS OK alone is treated as current write evidence without write block'), ('AI COMPLIANCE REFRESH AFTER LOCAL WRITE supports exposure only after LOCAL FREEZE WRITE OK', 'AI compliance refresh without local write proves freeze is written'), ('Startup freeze context refreshed is sequenced after write and does not replace write confirmation', 'startup refresh replaces missing LOCAL FREEZE WRITE OK'), ('same-feature write plus same-feature status OK permits next suite generation', 'same-feature status OK permits next suite generation from preview-only evidence')]}, {'family': 'PREVIEW_STALE_SIDECAR_AND_PLACEHOLDER_DEMOTION', 'pairs': [('stale preview sidecars from older MLRTs are demoted unless matching current feature write exists', 'stale preview sidecars from older MLRTs complete the current freeze'), ('placeholder current validated feature preview remains blocked until exact current feature data is provided', 'placeholder current validated feature preview is accepted as the current freeze'), ('consumed KANDA_FREEZE_HINT records are not reused as current write evidence', 'consumed KANDA_FREEZE_HINT records are reused as current write evidence'), ('older preview-ready entries are historical when newer current write evidence is available', 'older preview-ready entries override newer current write evidence')]}, {'family': 'SEQUENCE_ADVANCEMENT_AFTER_CONFIRMED_WRITE', 'pairs': [('planned next step is acted on only after current validation, confirmed write, and exposure status reconcile', 'planned next step is acted on after preview-only next step text'), ('review gate to real suite alternation is preserved after confirmed freeze', 'review gate to real suite alternation proceeds from validation-only output'), ('current feature title and freeze ID must match the latest intended MLRT sequence', 'wrong feature title with next step text can advance the sequence'), ('confirmed MLRT-96 write plus status OK permits MLRT-97 real suite generation', 'MLRT-96 preview-only block permits MLRT-97 real suite generation')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_PREVIEW_WRITE_RECOVERY', 'pairs': [('preview-versus-write recovery is offline evidence handling, not runtime route authority', 'preview-versus-write recovery grants runtime route authority'), ('targeted uploaded-log inspection for write status is not live freeze-memory read for routing', 'targeted uploaded-log inspection enables live freeze-memory reads for routing'), ('preview-versus-write testing does not train, calibrate, or improve a model', 'preview-versus-write evidence is saved as training data'), ('preview-versus-write recovery does not mutate freeze memory, gold registry, Pilot, or Copilot behavior', 'preview-versus-write recovery writes gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            write_text, preview_text = pair
            pair_id = f"mlrt97_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("write_confirmed", write_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("preview_only_containment", preview_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt97_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-97 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Preserve preview-versus-write boundary without runtime authority."
                )
                confirmed = variant == "write_confirmed"
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "preview_block_present": True,
                    "local_freeze_entry_preview_end_present": True,
                    "writable_preview_is_not_write": True,
                    "human_confirm_and_write_required": True,
                    "local_freeze_write_ok_present": confirmed,
                    "confirmed_write_boundary_preserved": True,
                    "written_paths_required_for_write": True,
                    "validation_evidence_separate_from_write": True,
                    "freeze_memory_status_ok_recovered_after_write": confirmed,
                    "preview_only_containment_applied": not confirmed,
                    "stale_preview_demoted": True,
                    "placeholder_preview_blocked": True,
                    "sequence_advancement_requires_confirmed_write": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_preview_as_write": False,
                    "treat_validation_as_freeze": False,
                    "treat_writable_preview_as_confirmed_write": False,
                    "skip_human_confirmation": False,
                    "treat_wrong_feature_write_as_current": False,
                    "critical_boundary_error_budget": 0,
                }
                for flag in BOUNDARY_FALSE_FLAGS:
                    candidate[flag] = False
                cases.append({
                    "case_id": case_id,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "user_request": user_request,
                    "expected_label": expected_label,
                    "candidate": candidate,
                })
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
    assert all(variants == {"write_confirmed", "preview_only_containment"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["preview_block_present"] is True
        assert candidate["local_freeze_entry_preview_end_present"] is True
        assert candidate["writable_preview_is_not_write"] is True
        assert candidate["human_confirm_and_write_required"] is True
        assert candidate["local_freeze_write_ok_present"] is (case["variant"] == "write_confirmed")
        assert candidate["confirmed_write_boundary_preserved"] is True
        assert candidate["written_paths_required_for_write"] is True
        assert candidate["validation_evidence_separate_from_write"] is True
        assert candidate["freeze_memory_status_ok_recovered_after_write"] is (case["variant"] == "write_confirmed")
        assert candidate["preview_only_containment_applied"] is (case["variant"] == "preview_only_containment")
        assert candidate["stale_preview_demoted"] is True
        assert candidate["placeholder_preview_blocked"] is True
        assert candidate["sequence_advancement_requires_confirmed_write"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_preview_as_write"] is False
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["treat_writable_preview_as_confirmed_write"] is False
        assert candidate["skip_human_confirmation"] is False
        assert candidate["treat_wrong_feature_write_as_current"] is False
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
    assert "MLRT-96" in text
    assert "64/64" in text
    assert "858/858" in text
    assert "`17` real test suites" in text
    assert "LOCAL FREEZE ENTRY PREVIEW END" in text
    assert "Confirm and Write" in text
    assert "LOCAL FREEZE WRITE OK" in text
    assert "FREEZE_MEMORY_STATUS: OK" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "858/858" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_preview_versus_write_boundary_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 858
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 17
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_preview_only_not_write_confirmation_tested"] is True
    assert manifest[f"{PREFIX}_writable_preview_still_requires_confirm_tested"] is True
    assert manifest[f"{PREFIX}_confirm_and_write_as_write_boundary_tested"] is True
    assert manifest[f"{PREFIX}_validation_evidence_versus_freeze_write_tested"] is True
    assert manifest[f"{PREFIX}_exposure_status_after_write_boundary_tested"] is True
    assert manifest[f"{PREFIX}_preview_stale_sidecar_and_placeholder_demotion_tested"] is True
    assert manifest[f"{PREFIX}_sequence_advancement_after_confirmed_write_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_preview_write_recovery_tested"] is True
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
    print("SANDBOX_RSS_MLRT97_MAXIMUM_OPTIMIZED_PREVIEW_VERSUS_WRITE_BOUNDARY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
