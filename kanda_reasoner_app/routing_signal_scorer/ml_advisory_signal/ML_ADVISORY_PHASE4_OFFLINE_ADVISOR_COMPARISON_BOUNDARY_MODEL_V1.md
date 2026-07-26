# ML Advisory Phase 4 Offline Advisor Comparison Boundary Model v1

Phase 4 is a comparison of already-generated offline summaries. The boundary is
narrow by design:

1. Inputs are immutable `OfflineEvaluationSummary` objects from the Phase 2
   harness.
2. Fixtures come from the Phase 3 synthetic catalog.
3. Comparison output is an immutable in-memory report.
4. The report contains no final route, no winner, no prompt ranking, no model
   score, no free-text recommendation, and no router override.
5. Fixture-set mismatch is a hard error because comparison must not infer or
   reconcile missing data.
6. Route variance remains a rejected observation, never a selected route.

The comparison may describe that one advisor abstained more often than another,
but it must not use that observation to bind prompts, select groups, mutate
registries, or change router behavior.


Explicit guard phrases: No real ML. No route authority. No MLRT-113.
