# Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Contract v1

Feature ID: `rss_ml_adv_phase5_offline_real_adapter_candidate_contract_v1`

## Purpose

This phase defines a fixture-bound offline candidate envelope for a future
real adapter. The candidate is not executable in this phase. It only records
whether a candidate descriptor satisfies all boundary rules proven in the
Phase 5 real-adapter boundary contract and review gate.

## Scope

Allowed:

- immutable in-memory candidate descriptors;
- immutable in-memory candidate decisions;
- use of an already accepted Phase 5 boundary decision;
- synthetic Phase 3 fixture catalog scope declaration;
- Phase 2 offline evaluation contract declaration;
- bounded reason-code declaration;
- abstention and rejection when any forbidden capability appears.

Forbidden:

- real ML execution;
- adapter execution;
- provider calls;
- network calls;
- API keys or credentials;
- embeddings or vector stores;
- persistence or report persistence;
- prompt loading;
- prompt registry mutation;
- prompt library reads;
- freeze-memory reads or writes;
- router-canon reads;
- runtime shadow mode;
- router prompt logic modification;
- router final selection modification;
- route authority;
- advisory rankings;
- free-text advisory explanations;
- training, calibration, or model improvement;
- runtime Pilot or runtime Copilot behavior;
- MLRT-113.

## Contract

The contract module is:

`real_adapter_candidate_contract.py`

It exposes:

- `RealAdapterCandidateDescriptor`
- `RealAdapterCandidateDecision`
- `RealAdapterCandidateStatus`
- `evaluate_real_adapter_candidate`

The helper module is:

`offline_real_adapter_candidate.py`

It exposes:

- `build_phase5_offline_candidate_probe`

## Safety invariant

Acceptance means only that the descriptor is safe to keep evaluating offline.
It is not evidence of accuracy, reliability, production readiness, route
correctness, runtime permission, or final-router authority.

## Next safe step

`Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Result Review Gate v1`
