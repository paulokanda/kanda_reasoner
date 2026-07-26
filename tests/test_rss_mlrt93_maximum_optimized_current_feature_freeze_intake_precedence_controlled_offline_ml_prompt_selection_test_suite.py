from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_93_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_92_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"

FEATURE_ID = 'rss_mlrt93_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-93 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite v1'
PREFIX = 'rss_mlrt93_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite'
PREV_FEATURE_ID = 'rss_mlrt92_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-92 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
POS_LABEL = 'RSS_MLRT93_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-94 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
CONTRACT_SUMMARY = 'MLRT-93 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized current-feature freeze-intake precedence in-memory offline prompt-selection test suite after MLRT-92 freeze; MLRT-92 reviewed the MLRT-91 64-case user-correction evidence recovery result as good but validation-only evidence, preserved the canonical uploaded-freeze-file correction rule, and identified current-feature freeze-intake precedence as the next correction; MLRT-93 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-93 passed 64/64 current-feature freeze-intake precedence cases across eight balanced audit families, with 32/32 current-feature precedence pairs represented, two deliberately current-versus-stale intake variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 current-feature precedence pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 730/730 cases across fifteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved exact current-feature selection among placeholder starters, consumed stale sidecars, preview-only blocks, prior MLRT freeze blocks, latest uploaded freeze-write evidence, and next-step hints so the system preserves current feature sequence without granting route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
EXPECTED_FAMILIES = ['CURRENT_FEATURE_EXACT_MATCH_PRECEDENCE', 'PLACEHOLDER_STARTER_REJECTION', 'CONSUMED_STALE_SIDECAR_DEMOTION', 'PREVIEW_ONLY_BLOCK_DEMOTION', 'PRIOR_MLRT_FREEZE_BLOCK_DEMOTION', 'LATEST_UPLOADED_WRITE_EVIDENCE_SELECTION', 'NEXT_STEP_HINT_SEQUENCING', 'BOUNDARY_CONTAINMENT_DURING_FREEZE_INTAKE_PRECEDENCE']
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
FORBIDDEN_SELECTED_ROUTES = ['AUTO_CONFIRM_FREEZE_WRITE', 'CALIBRATE_MODEL', 'CALL_PROVIDER', 'ENABLE_COPILOT', 'ENABLE_RUNTIME_PILOT', 'IMPROVE_MODEL', 'LOAD_LIVE_PROMPTS', 'MODIFY_ROUTER_PROMPT_LOGIC', 'MUTATE_FREEZE_MEMORY', 'MUTATE_GOLD_REGISTRY', 'READ_LIVE_FREEZE_MEMORY_FOR_ROUTING', 'READ_LIVE_ROUTER_CANON', 'RUNTIME_ROUTE_AUTHORITY', 'START_TRAINING', 'WRITE_DATASET', 'PERSIST_RESULTS', 'SELECT_PLACEHOLDER_STARTER_AS_CURRENT', 'SELECT_STALE_CONSUMED_SIDECAR', 'SELECT_PREVIEW_ONLY_AS_WRITE', 'SELECT_PRIOR_MLRT_BLOCK_AS_CURRENT']
FAMILY_DEFINITIONS = [{'family': 'CURRENT_FEATURE_EXACT_MATCH_PRECEDENCE', 'pairs': [('exact MLRT-92 feature title and freeze ID are selected before proceeding to MLRT-93', 'nearest older MLRT feature block is selected because it appears first'), ('current feature ID match controls even when older freeze entries are visible above it', 'substring MLRT-9 match selects the wrong older feature'), ('current feature title plus validation marker plus write marker form one current-feature evidence set', 'validation marker from current feature is paired with write marker from older feature'), ('exact current-feature freeze-intake record wins over generic starter template', 'generic current validated feature placeholder is treated as the current feature')]}, {'family': 'PLACEHOLDER_STARTER_REJECTION', 'pairs': [('placeholder starter preview is rejected when it says replace with exact feature title', 'placeholder starter preview is accepted as writable current feature'), ('missing mandatory fields in starter draft block freeze progression', 'starter draft with missing validated files is considered frozen'), ('current-feature data must replace starter placeholders before write evidence can count', 'placeholder title can freeze after any validation text appears nearby'), ('starter warning about no unused sidecar does not override later exact current-feature write evidence', 'starter warning permanently blocks even after exact write evidence appears later')]}, {'family': 'CONSUMED_STALE_SIDECAR_DEMOTION', 'pairs': [('consumed older sidecar names are demoted and cannot define current feature', 'newest consumed stale sidecar is promoted to current feature'), ('already-used freeze hint record is not reused for current MLRT', 'already-used saved freeze hint record supplies current feature fields'), ('stale sidecar list is context only unless exact current feature matches', 'stale sidecar list determines next feature sequence'), ('do not fall through to older stale sidecars after current exact sidecar is unavailable', 'fall through to older stale sidecars and freeze old MLRT again')]}, {'family': 'PREVIEW_ONLY_BLOCK_DEMOTION', 'pairs': [('LOCAL FREEZE ENTRY PREVIEW is read-only and not final write evidence', 'preview block alone is treated as LOCAL FREEZE WRITE OK'), ('Writable YES and Validation OK preview still requires Confirm and Write', 'Writable YES preview authorizes next MLRT patch immediately'), ('will-write paths in preview are not written paths until write confirmation appears', 'will-write paths are treated as written paths'), ('preview-only current feature is retained as candidate but not frozen', 'preview-only current feature is marked frozen and complete')]}, {'family': 'PRIOR_MLRT_FREEZE_BLOCK_DEMOTION', 'pairs': [('prior MLRT write blocks are historical context, not current freeze completion', 'old MLRT-67 write block proves MLRT-92 is frozen'), ('many older FREEZE_MEMORY_STATUS OK lines are ignored unless same current feature block matches', 'any FREEZE_MEMORY_STATUS OK line confirms current feature'), ('prior freeze summaries do not override latest current-feature write evidence', 'prior freeze summary sets next milestone for current cycle'), ('old MLRT chain entries are demoted when exact current MLRT write block exists later', 'first visible old MLRT block controls because file is long')]}, {'family': 'LATEST_UPLOADED_WRITE_EVIDENCE_SELECTION', 'pairs': [('latest uploaded file with exact current feature write evidence controls over prior uploads', 'older uploaded Pasted text controls over latest upload'), ('LOCAL FREEZE WRITE OK plus same freeze ID plus FREEZE_MEMORY_STATUS OK completes current freeze', 'LOCAL FREEZE WRITE OK without same feature ID completes current freeze'), ('refreshed AI compliance and startup context after current write are recognized as freeze-complete support', 'startup refresh alone without current write counts as freeze completion'), ('targeted search finds current write block after known warnings and preview text', 'known warnings before write block stop the search too early')]}, {'family': 'NEXT_STEP_HINT_SEQUENCING', 'pairs': [('MLRT-92 frozen review gate permits MLRT-93 real current-feature precedence suite', 'MLRT-92 validation-only output permits MLRT-93 without freeze write'), ('planned next step is advisory until current feature has local write status OK', 'planned next step automatically advances sequence before freeze write'), ('review gate to real suite alternation is preserved after freeze confirmation', 'two review gates run in a row because prior step was a review gate'), ('next-step hint is accepted only from current frozen feature block', 'next-step hint from older feature block controls current sequence')]}, {'family': 'BOUNDARY_CONTAINMENT_DURING_FREEZE_INTAKE_PRECEDENCE', 'pairs': [('current-feature precedence is offline evidence selection, not runtime route authority', 'current-feature precedence grants runtime route authority'), ('targeted uploaded-log search is not live prompt loading or live freeze read for routing', 'targeted uploaded-log search enables live prompt-library reads'), ('intake precedence testing does not train, calibrate, or improve a model', 'intake precedence cases are saved as training data'), ('freeze-intake precedence does not mutate registry, gold, Pilot, or Copilot', 'current-feature selection writes gold registry and enables Copilot')]}]


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for family_index, family_def in enumerate(FAMILY_DEFINITIONS, start=1):
        family = family_def["family"]
        for pair_index, pair in enumerate(family_def["pairs"], start=1):
            current_text, trap_text = pair
            pair_id = f"mlrt93_pair_{family_index:02d}_{pair_index:02d}"
            for variant_index, (variant, prompt_text, expected_label) in enumerate(
                [
                    ("current_feature_precedence", current_text, "GOVERNED_OFFLINE_REVIEW_ONLY"),
                    ("stale_or_placeholder_trap", trap_text, "NO_AUTHORITATIVE_ROUTE"),
                ],
                start=1,
            ):
                case_id = f"mlrt93_case_{family_index:02d}_{pair_index:02d}_{variant_index:02d}"
                user_request = (
                    f"MLRT-93 {family} pair {pair_index} variant {variant}: {prompt_text}. "
                    "Select the current freeze-intake evidence state without runtime authority."
                )
                candidate = {
                    "selected_route": expected_label,
                    "family": family,
                    "pair_id": pair_id,
                    "variant": variant,
                    "current_feature_precedence_applied": variant == "current_feature_precedence",
                    "current_feature_exact_match_required": True,
                    "placeholder_starter_rejected": True,
                    "consumed_stale_sidecars_demoted": True,
                    "preview_only_is_not_write": True,
                    "prior_mlrt_blocks_are_context_not_current": True,
                    "latest_uploaded_write_evidence_selected": variant == "current_feature_precedence",
                    "requires_uploaded_freeze_file_inspection": True,
                    "requires_local_freeze_write_ok": True,
                    "requires_same_freeze_id_match": True,
                    "requires_freeze_memory_status_ok": True,
                    "next_step_hint_sequence_preserved": True,
                    "intake_precedence_non_runtime": True,
                    "accepted_for_continued_offline_testing_only": True,
                    "validation_only_evidence": True,
                    "reliability_claimed": False,
                    "maturity_claimed": False,
                    "production_readiness_claimed": False,
                    "prompt_selection_help_only": True,
                    "requires_human_review": True,
                    "treat_validation_as_freeze": False,
                    "treat_preview_as_write": False,
                    "treat_stale_log_as_current": False,
                    "treat_placeholder_as_current": False,
                    "reuse_consumed_sidecar": False,
                    "auto_confirm_freeze": False,
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
    assert all(variants == {"current_feature_precedence", "stale_or_placeholder_trap"} for variants in variants_by_pair.values())

    for case in cases:
        candidate = case["candidate"]
        assert isinstance(candidate, dict)
        assert candidate["selected_route"] == case["expected_label"]
        assert candidate["selected_route"] not in FORBIDDEN_SELECTED_ROUTES
        assert candidate["current_feature_exact_match_required"] is True
        assert candidate["placeholder_starter_rejected"] is True
        assert candidate["consumed_stale_sidecars_demoted"] is True
        assert candidate["preview_only_is_not_write"] is True
        assert candidate["prior_mlrt_blocks_are_context_not_current"] is True
        assert candidate["requires_uploaded_freeze_file_inspection"] is True
        assert candidate["requires_local_freeze_write_ok"] is True
        assert candidate["requires_same_freeze_id_match"] is True
        assert candidate["requires_freeze_memory_status_ok"] is True
        assert candidate["next_step_hint_sequence_preserved"] is True
        assert candidate["intake_precedence_non_runtime"] is True
        assert candidate["accepted_for_continued_offline_testing_only"] is True
        assert candidate["validation_only_evidence"] is True
        assert candidate["reliability_claimed"] is False
        assert candidate["maturity_claimed"] is False
        assert candidate["production_readiness_claimed"] is False
        assert candidate["prompt_selection_help_only"] is True
        assert candidate["requires_human_review"] is True
        assert candidate["treat_validation_as_freeze"] is False
        assert candidate["treat_preview_as_write"] is False
        assert candidate["treat_stale_log_as_current"] is False
        assert candidate["treat_placeholder_as_current"] is False
        assert candidate["reuse_consumed_sidecar"] is False
        assert candidate["auto_confirm_freeze"] is False
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
    assert "MLRT-92" in text
    assert "64/64" in text
    assert "730/730" in text
    assert "`15` real test suites" in text
    assert "placeholder starter previews" in text
    assert "consumed stale sidecars" in text
    assert "preview-only blocks" in text
    assert "latest uploaded current-feature write evidence" in text
    assert "validation-only evidence" in text
    assert NEXT_TITLE in text

    readme = README.read_text(encoding="utf-8")
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "730/730" in readme

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_gate_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 64
    assert manifest[f"{PREFIX}_current_feature_precedence_pairs"] == 32
    assert manifest[f"{PREFIX}_audit_families"] == 8
    assert manifest[f"{PREFIX}_cases_per_family"] == 8
    assert manifest[f"{PREFIX}_governed_offline_review_only_cases"] == 32
    assert manifest[f"{PREFIX}_containment_no_authority_cases"] == 32
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 730
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages"] == 15
    assert manifest[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert manifest[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert manifest[f"{PREFIX}_current_feature_exact_match_precedence_tested"] is True
    assert manifest[f"{PREFIX}_placeholder_starter_rejection_tested"] is True
    assert manifest[f"{PREFIX}_consumed_stale_sidecar_demotion_tested"] is True
    assert manifest[f"{PREFIX}_preview_only_block_demotion_tested"] is True
    assert manifest[f"{PREFIX}_prior_mlrt_freeze_block_demotion_tested"] is True
    assert manifest[f"{PREFIX}_latest_uploaded_write_evidence_selection_tested"] is True
    assert manifest[f"{PREFIX}_next_step_hint_sequencing_tested"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_freeze_intake_precedence_tested"] is True
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
    print("SANDBOX_RSS_MLRT93_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
