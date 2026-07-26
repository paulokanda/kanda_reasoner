# ML Advisory Signal Phase 2 Offline Harness Boundary Model v1

The Phase 2 offline harness sits outside runtime router execution. It is a
non-authoritative test/evaluation utility that receives caller-supplied fixtures
and returns immutable summaries.

## Boundary flow

1. A caller constructs sanitized `AdvisoryInput` objects.
2. A caller supplies already-governed decision values before and after advisory.
3. The harness calls an advisor through `AdvisorProtocol`.
4. The advisory output firewall validates the result.
5. The harness compares the caller-supplied decision values.
6. The harness returns an immutable summary.

The harness does not compute the governed decision. It cannot select, rank,
replace, or override a route.

## Fail-open rule

If the advisor raises an exception or emits rejected output, the harness records
`FAIL_OPEN_ABSTAINED` with safe abstention telemetry. Evaluation continues.

## No persistence rule

No files, reports, datasets, vectors, caches, logs, registries, prompt assets,
or freeze memory entries are written by this feature.
