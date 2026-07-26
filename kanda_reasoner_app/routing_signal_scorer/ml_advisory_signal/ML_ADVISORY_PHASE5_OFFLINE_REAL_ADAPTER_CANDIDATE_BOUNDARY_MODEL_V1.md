# Phase 5 Offline Real-Adapter Candidate Boundary Model v1

Feature ID: `rss_ml_adv_phase5_offline_real_adapter_candidate_contract_v1`

The candidate boundary is narrower than runtime Copilot behavior. It permits
only a fixture-bound candidate descriptor and an in-memory decision derived
from that descriptor. It has no runtime pathway and no authority over the
router.

## Candidate boundary layers

1. Phase 5 boundary decision must already be accepted.
2. Candidate descriptor must remain offline and fixture-bound.
3. Candidate descriptor must not enable real ML or adapter execution.
4. Candidate descriptor must not enable provider, network, API-key,
   embedding, vector-store, or persistence capabilities.
5. Candidate descriptor must not read prompts, freeze memory, or router canon.
6. Candidate descriptor must not modify router logic or final route selection.
7. Candidate decision must reject any enabled forbidden capability.

## Failure handling

The candidate decision rejects fail-closed. A rejected descriptor is evidence
only for boundary repair, not for adapter execution.

## Authority model

The governed router remains the final selector. Candidate acceptance cannot be
converted into route authority, prompt loading, runtime shadow mode, or runtime
Copilot behavior.
