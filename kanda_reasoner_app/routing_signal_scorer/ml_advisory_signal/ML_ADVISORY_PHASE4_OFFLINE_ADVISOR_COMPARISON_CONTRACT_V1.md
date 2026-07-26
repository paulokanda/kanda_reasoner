# Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1

## Scope

Phase 4 adds a passive offline comparison contract for bounded advisory
summaries. It compares the existing NullAdvisor and MockAdvisor only through the
Phase 2 offline harness and the Phase 3 synthetic fixture catalog.

This feature is still offline, in-memory, non-runtime, and non-authoritative.
It is not real ML and it does not prove routing quality.

## Added contracts

- `OfflineAdvisorComparisonStatus`
- `OfflineAdvisorComparisonParticipant`
- `OfflineAdvisorComparisonReport`
- `compare_offline_advisor_summaries`
- `run_phase4_null_vs_mock_offline_comparison`

## Allowed behavior

- Use existing synthetic Phase 3 fixtures.
- Use existing Phase 2 offline harness summaries.
- Compare bounded status counts, abstention counts, route-invariance counts, and
  route-variance rejection counts.
- Reject summaries that do not use the same fixture IDs.

## Forbidden behavior

- No real ML.
- No provider calls.
- No embeddings or vector store.
- No persistence or report persistence.
- No prompt loading, prompt registry mutation, or prompt library read.
- No freeze-memory read or write.
- No router-canon read.
- No runtime shadow mode.
- No router prompt logic modification.
- No router final selection modification.
- No route authority.
- No advisory rankings or free-text advisory explanations.
- No training, calibration, or model improvement.
- No MLRT-113.

## Next step

After validation and freeze, the only safe next step is:

`Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Result Review Gate v1`
