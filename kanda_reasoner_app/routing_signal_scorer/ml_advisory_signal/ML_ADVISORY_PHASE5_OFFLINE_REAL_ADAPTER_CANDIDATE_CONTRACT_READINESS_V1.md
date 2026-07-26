# Phase 5 Offline Real-Adapter Candidate Contract Readiness v1

Current feature: Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Boundary Result Review Gate v1
Next planned feature: Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Contract v1

## Purpose

This readiness document defines what must be true before any offline adapter
candidate contract can be created after the Phase 5 boundary review gate.

It does not implement an adapter candidate. It does not authorize runtime ML.
It does not authorize provider calls, network access, credentials, embeddings,
persistence, route authority, or router prompt logic modification.

## Required boundaries for the next phase

A future offline adapter candidate contract must remain:

1. offline;
2. in-memory;
3. fixture-bound;
4. non-runtime;
5. non-authoritative;
6. output-firewalled;
7. deterministic or safely stubbed unless a separately governed local model is
   explicitly approved;
8. unable to read prompt library, freeze memory, router canon, credentials,
   network resources, provider SDKs, embeddings, or vector stores.

## Allowed next topics

The next phase may define:

- adapter candidate input and output contracts;
- a disabled or deterministic local candidate adapter stub;
- fixture-only evaluation entry points;
- abstention and fail-open behavior;
- output firewall compatibility checks;
- route-invariance checks showing the router final decision is unchanged.

## Blocking rule

If the next phase attempts to execute provider-backed ML, use network calls,
load credentials, read prompt library, read freeze memory, read router canon,
write reports, persist datasets, rank prompts, change router prompt logic, alter
final route selection, or expose runtime advisory behavior, the phase must fail.

## Next title recorded by Phase 5 review gate

Routing Signal Scorer ML Advisory-Signal Phase 5 Offline Real-Adapter Candidate Contract v1
