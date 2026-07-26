# ML Advisory Signal Phase 7 Read-Only Advisory Surface Wiring Implementation Readiness v1

Next planned feature: Routing Signal Scorer ML Advisory-Signal Phase 7 Read-Only Advisory Surface Wiring Implementation v1

## Readiness decision

The Phase 7 guarded advisory surface wiring contract result review gate permits
only a narrow implementation step: a read-only advisory surface wiring function
that can attach a bounded ML advisory display payload to app/router output after
canonical router final selection.

## Required implementation shape

The implementation must:

1. accept an already-final canonical router result;
2. accept already-computed AdvisoryOutput or already-built guarded display
   payload data;
3. copy the router result unchanged;
4. attach the advisory payload under a clearly separate telemetry/display key;
5. preserve fail-open behavior when advisory data is absent, invalid, blocked,
   disabled, or unavailable;
6. include a no-op/disabled path;
7. expose no route override hook;
8. expose no prompt selection hook;
9. write nothing to disk;
10. call no provider;
11. read no prompt library, freeze memory, or router canon;
12. mutate no router output fields used for final selection.

## Required tests

The implementation must include tests proving:

- router result object/fields used for final selection are unchanged;
- advisory payload is bounded and separate;
- disabled mode returns unchanged router output plus no-op metadata;
- invalid advisory payload fails open;
- no persistence, provider, prompt loading, prompt registry, freeze memory,
  router canon, or MLRT-113 artifacts are introduced;
- no advisory rankings or free-text route advice are introduced.

## Forbidden scope

No runtime UI panel activation, no route influence, no router prompt logic
modification, no runtime Copilot decision behavior, and no provider-backed ML.
