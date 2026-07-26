# Phase 7 Guarded Advisory Surface Wiring Contract Readiness v1

## Safe next title

Routing Signal Scorer ML Advisory-Signal Phase 7 Guarded Advisory Surface Wiring Contract v1

## What the next contract may allow

- automatic call after canonical router final selection;
- construction of read-only display payload from already computed AdvisoryOutput;
- response-envelope field for telemetry payload;
- visible advisory surface contract with explicit status, uncertainty, scope, and role labels;
- disable/no-op policy;
- fail-open behavior;
- typed payload schema with no free-text route advice;
- SLO/error-budget and latency/cost budget declarations;
- route-invariance tests;
- security tests for prompt injection, insecure output handling, and excessive agency.

## What the next contract must still block

- direct route influence;
- router prompt logic modification;
- router final selection modification;
- provider calls;
- adapter execution;
- runtime Copilot decision behavior;
- prompt loading;
- prompt registry mutation;
- prompt library read;
- freeze-memory read or write;
- router-canon read;
- persistence;
- free-text route recommendations.

## Route effect policy

Direct route effect remains blocked. A later separate contract may study
deterministic re-check requests, but only if the governed router remains final
and the ML advisory path never selects, ranks, overrides, or vetoes a route.
