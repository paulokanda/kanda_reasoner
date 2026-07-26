# Phase 6 Guarded Runtime Advisory Display Contract Readiness v1

Current feature: Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Result Review Gate v1
Next planned feature: Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1

## Purpose

This readiness document defines the minimum boundaries for any future Phase 6
guarded runtime advisory display contract. It is not a runtime implementation.
It does not display advisory data. It does not authorize real ML, provider calls, network access, adapter execution,
candidate execution, prompt loading, route authority, router prompt logic modification, or runtime Copilot behavior.

## Required Phase 6 contract boundaries

A future Phase 6 guarded runtime display contract must keep ML Advisory Signal:

1. read-only;
2. telemetry-only;
3. non-authoritative;
4. route-invariant;
5. final-selection-invisible;
6. prompt-loading-disabled;
7. prompt-registry-mutation-disabled;
8. freeze-memory-read-disabled;
9. router-canon-read-disabled;
10. provider-call-disabled;
11. network-disabled;
12. persistence-disabled unless a separate governed artifact explicitly permits
    a bounded local audit log;
13. fully removable without changing router output.

## Blocking rules

The next phase must fail if it attempts to:

- execute real ML or a real adapter;
- call providers or network resources;
- use API keys or credentials;
- read or mutate prompt library assets;
- read or mutate freeze memory;
- read router canon;
- modify router prompt logic;
- modify router final selection;
- rank prompts;
- generate free-text explanations;
- train, calibrate, or improve a model;
- convert advisory telemetry into route authority;
- create MLRT-113.

## Allowed next topics

The next phase may define only a guarded display contract, data-shape checks,
route-invariance requirements, abstention display semantics, failure display
semantics, and removal/no-op guarantees.

## Next title recorded by this review gate

Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract v1
