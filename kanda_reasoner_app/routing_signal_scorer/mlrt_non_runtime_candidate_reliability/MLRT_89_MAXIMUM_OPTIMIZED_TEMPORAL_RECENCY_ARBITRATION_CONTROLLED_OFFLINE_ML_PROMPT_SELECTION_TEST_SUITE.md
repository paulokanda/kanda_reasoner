# Routing Signal Scorer MLRT-89 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite v1

Feature ID: `rss_mlrt89_maximum_optimized_temporal_recency_arbitration_controlled_offline_ml_prompt_selection_test_suite_v1`

Positive state: `RSS_MLRT89_MAXIMUM_OPTIMIZED_TEMPORAL_RECENCY_ARBITRATION_CONTROLLED_OFFLINE_PROMPT_SELECTION_TEST_SUITE_PASSED_NON_RUNTIME_NON_AUTHORITATIVE`

## Purpose

MLRT-89 is a real maximum-optimized temporal recency arbitration controlled offline prompt-selection suite. It starts after MLRT-88 freeze and tests whether the offline ML prompt-selection evaluation can distinguish current canonical evidence from older logs, stale sidecar hints, repeated pasted output, preview-only drafts, and mismatched freeze states.

This suite exists because the workflow now has an explicit canonical evidence pattern: validation output is pasted in chat text, while freeze confirmation is uploaded as a file. MLRT-89 tests that the system must read both channels before deciding whether to advance.

## Scope

- Real test cases added: `64`
- Temporal recency pairs: `32`
- Audit families: `8`
- Cases per family: `8`
- Variants per pair: `2`
- Governed offline-review-only cases: `32`
- Containment/no-authority cases: `32`
- Expected forbidden selected routes: `0`
- Cumulative controlled offline prompt-selection coverage after this suite: `602/602` cases across `13` real test suites

## Audit families

- `LATEST_UPLOAD_VS_OLDER_FREEZE_LOG_ARBITRATION`
- `STALE_SIDECAR_HINT_VS_CURRENT_FREEZE_ARBITRATION`
- `VALIDATION_RECENCY_VS_FREEZE_RECENCY_ARBITRATION`
- `PREVIEW_TIMESTAMP_VS_WRITE_TIMESTAMP_ARBITRATION`
- `REPEATED_PASTED_OUTPUT_ARBITRATION`
- `NEXT_MILESTONE_RECENCY_ARBITRATION`
- `CONFLICTING_STATUS_LINE_ARBITRATION`
- `CANONICAL_EVIDENCE_CHANNEL_ARBITRATION`

## What the suite protects

The suite protects against false progression caused by:

- using an older uploaded freeze block as if it proved the current MLRT
- using the first `LOCAL FREEZE WRITE OK` in a long file even when it belongs to an older milestone
- treating writable preview as final write
- treating validation-only output as freeze confirmation
- treating repeated pasted validation as multiple independent state transitions
- using stale consumed sidecar hints as current next-step authority
- ignoring the uploaded freeze file because its filename is generic
- advancing from a next-milestone cue before the current feature is actually frozen

## Previous milestone

Previous milestone required before install:

`Routing Signal Scorer MLRT-88 Maximum-Optimized State-Transition Evidence Recognition Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1`

MLRT-88 accepted MLRT-87 only as validation-only evidence for continued offline testing and identified temporal recency arbitration as the next correction.

## Next milestone

After local validation and freeze of MLRT-89 with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

`Routing Signal Scorer MLRT-90 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1`

## Boundary preservation

MLRT-89 is in-memory, offline, controlled, validation-only, non-authoritative, and test-local. It does not create persistent case files, dataset files, labels, reports, gold records, registries, route authority, prompt loading, provider calls, embeddings, persistence, training, calibration, runtime Pilot, or Copilot behavior.

Preserved boundaries:

- no runtime routing
- no route authority
- no router prompt logic modification
- no prompt loading
- no live prompt-library reads
- no provider calls
- no embeddings
- no vector stores
- no network calls
- no subprocess calls
- no persistence
- no report persistence
- no training-data intake
- no dataset creation
- no model training
- no model calibration
- no model improvement
- no gold registry write
- no registry mutation
- no runtime Pilot
- no Copilot behavior
- critical boundary error budget zero

## Contract summary

MLRT-89 Maximum-Optimized Temporal Recency Arbitration Controlled Offline ML Prompt-Selection Test Suite v1, executed a 64-case maximum-optimized temporal recency arbitration in-memory offline prompt-selection test suite after MLRT-88 freeze; MLRT-88 reviewed the MLRT-87 64-case state-transition evidence recognition result as good but validation-only evidence and identified temporal recency arbitration as the next correction; MLRT-89 follows the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; MLRT-89 passed 64/64 temporal recency arbitration cases across eight balanced audit families, with 32/32 temporal recency pairs represented, two deliberately competing old-versus-current evidence variants per pair, 32 governed offline-review-only cases, and 32 containment/no-authority cases; coverage protection passed: 64/64 unique case IDs, 64/64 unique user requests, 32/32 temporal recency pairs represented, 8/8 families represented with 8 cases each, no duplicate filler, no forbidden selected routes, no persistence, no dataset files, no training data, no prompt loading, and no route authority; cumulative controlled offline prompt-selection coverage is now 602/602 cases across thirteen real test suites, but this remains validation-only evidence and not reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.
