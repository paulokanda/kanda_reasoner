# Phase 6 Guarded Runtime Advisory Display Implementation Readiness v1

Current feature: Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Contract Result Review Gate v1
Next candidate feature: Routing Signal Scorer ML Advisory-Signal Phase 6 Guarded Runtime Advisory Display Implementation v1

## Purpose

This readiness note defines what must be true before any future guarded runtime
advisory display implementation can be considered. It is not an implementation.
It does not authorize runtime display, runtime advisory panels, provider calls,
model execution, route authority, router prompt logic modification, or runtime
Copilot behavior.

## Minimum implementation constraints for the next feature

A future display implementation must:

1. be read-only and telemetry-only;
2. be route-invariant;
3. be final-selection-invisible;
4. be removable without changing router output;
5. fail open when advisory data is missing, invalid, late, or rejected;
6. show only bounded status/reason-code fields approved by the Phase 6 contract;
7. never show advisory rankings;
8. never show free-text advisory explanations;
9. never mutate prompt registry, prompt files, freeze memory, router canon, or
   router final decisions;
10. never call providers, open the network, use API keys, run embeddings, write
    reports, train, calibrate, or improve models;
11. never create MLRT-113;
12. preserve the governed router as final selector.

## Blocking conditions

The next implementation must be blocked if it:

- changes final router output;
- adds fallback routing based on advisory data;
- treats advisory absence as an error that blocks routing;
- displays route recommendations as authoritative;
- displays prompt rankings;
- displays free-text model explanations;
- reads prompt libraries, freeze memory, or router canon;
- executes adapters, candidates, providers, network calls, embeddings, training,
  calibration, or model improvement;
- writes hidden state or persistent reports;
- is not fully removable without changing router output.

## Validation expectation

The next implementation must include tests proving that turning the display on
or off produces identical governed router decisions. The display may expose only
bounded telemetry fields and must fail open to no display when guards fail.
