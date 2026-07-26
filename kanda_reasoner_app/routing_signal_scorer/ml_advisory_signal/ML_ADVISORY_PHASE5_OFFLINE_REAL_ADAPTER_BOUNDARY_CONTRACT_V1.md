# ML Advisory Signal Phase 5 Offline Real-Adapter Boundary Contract v1

Feature title: Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Contract v1
Feature ID: rss_ml_adv_phase5_offline_real_adapter_boundary_contract_v1

## Purpose

Phase 5 defines the boundary for describing a possible future real adapter
without enabling one. It is a contract and descriptor check only. It does not
execute an adapter, call providers, use credentials, read prompts, read freeze
memory, read router canon, persist data, train models, calibrate models, improve
models, modify router logic, or choose a route.

## Added contracts

- `RealAdapterDescriptor`: describes a possible future adapter in memory.
- `RealAdapterBoundaryDecision`: records whether the descriptor remains within
  the offline boundary.
- `evaluate_real_adapter_boundary`: rejects any descriptor that enables a
  forbidden capability.
- `build_phase5_offline_real_adapter_boundary_probe`: builds one safe
  descriptor-only probe decision.

## Allowed behavior

Phase 5 may:

1. create in-memory adapter descriptors;
2. evaluate whether descriptor flags remain safe;
3. reject any descriptor that declares a forbidden capability;
4. emit bounded in-memory decision notes.

## Forbidden behavior

Phase 5 must not:

1. execute a real adapter;
2. call providers or perform network access;
3. load API keys or credentials;
4. create embeddings or vector stores;
5. persist reports or telemetry;
6. read prompt libraries, freeze memory, or router canon;
7. load or mutate prompt registry content;
8. modify router prompt logic or final route selection;
9. create route authority, rankings, or free-text explanations;
10. train, calibrate, or improve a model;
11. create MLRT-113;
12. add real prompt-selection cases.

## Safety conclusion

Phase 5 is still offline, in-memory, non-runtime, and non-authoritative. It
prepares an adapter boundary but does not enable real ML.
