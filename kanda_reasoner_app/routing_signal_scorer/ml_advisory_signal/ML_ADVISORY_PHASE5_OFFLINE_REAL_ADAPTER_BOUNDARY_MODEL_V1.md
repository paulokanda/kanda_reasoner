# Phase 5 Offline Real-Adapter Boundary Model v1

Feature ID: rss_ml_adv_phase5_offline_real_adapter_boundary_contract_v1

## Boundary statement

The adapter boundary is descriptor-only. A future adapter can be discussed only
as metadata and contract IDs until a later governed phase explicitly creates a
separate, frozen, validated adapter implementation.

## Mandatory rejection rule

A descriptor must be rejected when any forbidden capability flag is true. The
forbidden set includes adapter execution, provider calls, network calls,
credentials, embeddings, vector stores, persistence, prompt loading, prompt
library reads, freeze memory reads, router-canon reads, router prompt logic
changes, route authority, rankings, free-text explanations, training,
calibration, model improvement, runtime Pilot behavior, and runtime Copilot
behavior.

## Data flow

```text
RealAdapterDescriptor
  -> evaluate_real_adapter_boundary
  -> RealAdapterBoundaryDecision
```

No provider, prompt library, freeze memory, router canon, or persistence store
is on this path.

## Error budget

Critical boundary error budget: 0.
